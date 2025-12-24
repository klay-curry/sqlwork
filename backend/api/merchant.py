"""
商家端API路由
商品管理、订单管理、数据统计
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal

from database import get_db
from models import Merchant, Product, Order, User
from models import ProductCreate, ProductUpdate, ProductResponse, OrderResponse
from models import SalesTrendResponse, TopProductResponse, CategoryDistributionResponse
from services.auth import get_current_merchant
from ai.advisor import get_merchant_suggestions

router = APIRouter(prefix="/api/merchant", tags=["商家端"])


@router.get("/products", response_model=dict, summary="获取商家商品列表")
def get_merchant_products(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[int] = Query(None, description="商品状态筛选"),
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    获取当前商家所有商品（分页）
    
    返回商品列表及销量统计
    """
    # 构建查询
    query = db.query(Product).filter(Product.merchant_id == merchant.merchant_id)
    
    if status is not None:
        query = query.filter(Product.status == status)
    
    # 总数
    total = query.count()
    
    # 分页
    products = query.order_by(desc(Product.created_at)).offset((page - 1) * size).limit(size).all()
    
    # 查询销量
    items = []
    for product in products:
        sales_count = db.query(func.sum(Order.quantity)).filter(
            Order.product_id == product.product_id
        ).scalar() or 0
        
        item = {
            "product_id": product.product_id,
            "name": product.name,
            "price": float(product.price),
            "stock": product.stock,
            "sales_count": int(sales_count),
            "category": product.category,
            "status": product.status,
            "created_at": product.created_at.isoformat()
        }
        items.append(item)
    
    return {
        "code": 200,
        "data": {
            "total": total,
            "page": page,
            "size": size,
            "items": items
        }
    }


@router.post("/products", response_model=ProductResponse, summary="创建商品")
def create_product(
    product_data: ProductCreate,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    创建新商品
    """
    new_product = Product(
        merchant_id=merchant.merchant_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category=product_data.category,
        status=product_data.status
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.put("/products/{product_id}", response_model=ProductResponse, summary="更新商品")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    更新商品信息
    """
    # 查询商品
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.merchant_id == merchant.merchant_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在或无权限操作"
        )
    
    # 更新字段
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/products/{product_id}", summary="删除商品")
def delete_product(
    product_id: int,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    删除商品
    """
    product = db.query(Product).filter(
        Product.product_id == product_id,
        Product.merchant_id == merchant.merchant_id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在或无权限操作"
        )
    
    db.delete(product)
    db.commit()
    
    return {"code": 200, "message": "商品删除成功"}


@router.get("/orders", response_model=dict, summary="获取商家订单列表")
def get_merchant_orders(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="订单状态筛选"),
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    获取商家所有订单（按时间倒序）
    """
    # 构建查询
    query = db.query(Order).filter(Order.merchant_id == merchant.merchant_id)
    
    if status:
        query = query.filter(Order.status == status)
    
    # 总数
    total = query.count()
    
    # 分页
    orders = query.order_by(desc(Order.order_time)).offset((page - 1) * size).limit(size).all()
    
    # 关联查询用户和商品信息
    items = []
    for order in orders:
        user = db.query(User).filter(User.user_id == order.user_id).first()
        product = db.query(Product).filter(Product.product_id == order.product_id).first()
        
        item = {
            "order_id": order.order_id,
            "buyer_username": user.username if user else "未知",
            "product_name": product.name if product else "已删除商品",
            "quantity": order.quantity,
            "unit_price": float(order.unit_price),
            "total_amount": float(order.total_amount),
            "order_time": order.order_time.isoformat(),
            "status": order.status
        }
        items.append(item)
    
    return {
        "code": 200,
        "data": {
            "total": total,
            "page": page,
            "size": size,
            "items": items
        }
    }


@router.get("/sales/trend", response_model=dict, summary="销售趋势统计")
def get_sales_trend(
    days: int = Query(30, ge=1, le=365, description="统计天数"),
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    获取近N天销量趋势数据（用于折线图）
    """
    # 计算起始日期
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)
    
    # 查询每日销量
    daily_sales = db.query(
        func.date(Order.order_time).label('date'),
        func.count(Order.order_id).label('sales')
    ).filter(
        Order.merchant_id == merchant.merchant_id,
        func.date(Order.order_time) >= start_date,
        func.date(Order.order_time) <= end_date
    ).group_by(
        func.date(Order.order_time)
    ).all()
    
    # 构建完整日期序列（填充缺失日期为0）
    sales_dict = {str(item.date): item.sales for item in daily_sales}
    
    dates = []
    sales = []
    current_date = start_date
    while current_date <= end_date:
        date_str = str(current_date)
        dates.append(date_str)
        sales.append(sales_dict.get(date_str, 0))
        current_date += timedelta(days=1)
    
    return {
        "code": 200,
        "data": {
            "dates": dates,
            "sales": sales
        }
    }


@router.get("/products/top", response_model=dict, summary="销量Top商品")
def get_top_products(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    获取销量Top N商品（用于柱状图）
    """
    # 查询商品销量
    top_products = db.query(
        Product.name,
        func.sum(Order.quantity).label('sales')
    ).join(
        Order, Product.product_id == Order.product_id
    ).filter(
        Product.merchant_id == merchant.merchant_id
    ).group_by(
        Product.product_id, Product.name
    ).order_by(
        desc('sales')
    ).limit(limit).all()
    
    data = [{"name": item.name, "sales": int(item.sales)} for item in top_products]
    
    return {
        "code": 200,
        "data": data
    }


@router.get("/category/distribution", response_model=dict, summary="类目销售分布")
def get_category_distribution(
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    获取各类目销售占比（用于饼图）
    """
    # 查询类目销量
    category_sales = db.query(
        Product.category,
        func.sum(Order.quantity).label('value')
    ).join(
        Order, Product.product_id == Order.product_id
    ).filter(
        Product.merchant_id == merchant.merchant_id
    ).group_by(
        Product.category
    ).all()
    
    data = [
        {"name": item.category or "未分类", "value": int(item.value)} 
        for item in category_sales
    ]
    
    return {
        "code": 200,
        "data": data
    }


@router.get("/ai/suggestions", response_model=dict, summary="获取AI经营建议")
def get_ai_suggestions(
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """
    获取AI生成的经营建议
    
    基于规则引擎分析销售数据
    """
    suggestions = get_merchant_suggestions(db, merchant.merchant_id)
    
    return {
        "code": 200,
        "data": {
            "suggestions": suggestions
        }
    }
