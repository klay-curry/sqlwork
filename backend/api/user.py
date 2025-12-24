"""
买家端API路由
订单管理、商品搜索、个性化推荐
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional

from database import get_db
from models import User, Product, Order, Merchant, OrderCreate, ProductSearch
from services.auth import get_current_user
from ai.recommender import get_user_recommendations

router = APIRouter(prefix="/api/user", tags=["买家端"])


@router.get("/orders", response_model=dict, summary="获取用户订单历史")
def get_user_orders(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户所有订单（按时间倒序）
    """
    # 查询订单
    query = db.query(Order).filter(Order.user_id == user.user_id)
    total = query.count()
    
    orders = query.order_by(desc(Order.order_time)).offset((page - 1) * size).limit(size).all()
    
    # 关联查询商品和商家信息
    items = []
    for order in orders:
        product = db.query(Product).filter(Product.product_id == order.product_id).first()
        merchant = db.query(Merchant).filter(Merchant.merchant_id == order.merchant_id).first()
        
        item = {
            "order_id": order.order_id,
            "product_name": product.name if product else "已删除商品",
            "merchant_name": merchant.name if merchant else "未知商家",
            "unit_price": float(order.unit_price),
            "quantity": order.quantity,
            "total_amount": float(order.total_amount),
            "order_time": order.order_time.isoformat(),
            "status": order.status,
            "is_reviewed": bool(order.review)
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


@router.post("/orders", response_model=dict, summary="创建订单")
def create_order(
    order_data: OrderCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    用户下单
    
    - 检查库存
    - 扣减库存
    - 创建订单记录
    """
    # 查询商品
    product = db.query(Product).filter(
        Product.product_id == order_data.product_id,
        Product.status == 1  # 仅上架商品
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商品不存在或已下架"
        )
    
    # 检查库存
    if product.stock < order_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"库存不足，当前库存仅剩 {product.stock} 件"
        )
    
    # 开始事务：扣减库存并创建订单
    try:
        # 扣减库存
        product.stock -= order_data.quantity
        
        # 创建订单
        new_order = Order(
            user_id=user.user_id,
            product_id=product.product_id,
            merchant_id=product.merchant_id,
            quantity=order_data.quantity,
            unit_price=product.price,
            total_amount=product.price * order_data.quantity,
            status='pending'
        )
        
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        return {
            "code": 200,
            "message": "下单成功",
            "data": {
                "order_id": new_order.order_id,
                "product_name": product.name,
                "quantity": new_order.quantity,
                "total_amount": float(new_order.total_amount)
            }
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"下单失败：{str(e)}"
        )


@router.post("/search", response_model=dict, summary="商品搜索")
def search_products(
    search_data: ProductSearch,
    db: Session = Depends(get_db)
):
    """
    搜索商品（支持关键词、类目、价格区间筛选）
    """
    # 构建查询
    query = db.query(Product).filter(Product.status == 1)  # 仅上架商品
    
    # 关键词搜索（名称或描述）
    if search_data.keyword:
        keyword_filter = or_(
            Product.name.like(f"%{search_data.keyword}%"),
            Product.description.like(f"%{search_data.keyword}%")
        )
        query = query.filter(keyword_filter)
    
    # 类目筛选
    if search_data.category:
        query = query.filter(Product.category == search_data.category)
    
    # 价格区间
    if search_data.min_price is not None:
        query = query.filter(Product.price >= search_data.min_price)
    if search_data.max_price is not None:
        query = query.filter(Product.price <= search_data.max_price)
    
    # 执行查询
    products = query.limit(50).all()
    
    # 关联商家信息
    items = []
    for product in products:
        merchant = db.query(Merchant).filter(Merchant.merchant_id == product.merchant_id).first()
        
        item = {
            "product_id": product.product_id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "category": product.category,
            "merchant_name": merchant.name if merchant else "未知商家"
        }
        items.append(item)
    
    return {
        "code": 200,
        "data": items
    }


@router.get("/recommendations", response_model=dict, summary="获取个性化推荐")
def get_recommendations(
    limit: int = Query(10, ge=1, le=50, description="推荐数量"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取个性化商品推荐
    
    基于协同过滤算法
    """
    # 使用协同过滤推荐引擎
    recommendations = get_user_recommendations(db, user.user_id, limit)
    
    return {
        "code": 200,
        "data": recommendations
    }
