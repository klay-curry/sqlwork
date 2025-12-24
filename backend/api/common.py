"""
通用API路由
无需登录即可访问的接口
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional

from database import get_db
from models import Product, Merchant, Order

router = APIRouter(prefix="/api", tags=["通用接口"])


@router.get("/products", response_model=dict, summary="获取商品列表")
def get_products(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    category: Optional[str] = Query(None, description="类目筛选"),
    db: Session = Depends(get_db)
):
    """
    获取所有上架商品（分页）
    
    无需登录即可访问
    """
    # 构建查询
    query = db.query(Product).filter(Product.status == 1)  # 仅上架商品
    
    if category:
        query = query.filter(Product.category == category)
    
    # 总数
    total = query.count()
    
    # 分页
    products = query.order_by(desc(Product.created_at)).offset((page - 1) * size).limit(size).all()
    
    # 关联商家信息
    items = []
    for product in products:
        merchant = db.query(Merchant).filter(Merchant.merchant_id == product.merchant_id).first()
        
        item = {
            "product_id": product.product_id,
            "name": product.name,
            "price": float(product.price),
            "category": product.category,
            "stock": product.stock,
            "merchant_name": merchant.name if merchant else "未知商家",
            "description": product.description
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


@router.get("/products/{product_id}", response_model=dict, summary="获取商品详情")
def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    获取单个商品详细信息
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    
    if not product:
        return {
            "code": 404,
            "message": "商品不存在"
        }
    
    # 查询商家信息
    merchant = db.query(Merchant).filter(Merchant.merchant_id == product.merchant_id).first()
    
    # 查询销量
    sales_count = db.query(func.sum(Order.quantity)).filter(
        Order.product_id == product.product_id
    ).scalar() or 0
    
    return {
        "code": 200,
        "data": {
            "product_id": product.product_id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "stock": product.stock,
            "category": product.category,
            "status": product.status,
            "sales_count": int(sales_count),
            "merchant_name": merchant.name if merchant else "未知商家",
            "created_at": product.created_at.isoformat()
        }
    }


@router.get("/categories", response_model=dict, summary="获取商品类目")
def get_categories(db: Session = Depends(get_db)):
    """
    获取所有商品类目及数量统计
    """
    categories = db.query(
        Product.category,
        func.count(Product.product_id).label('count')
    ).filter(
        Product.status == 1
    ).group_by(
        Product.category
    ).all()
    
    data = [
        {"category": item.category or "未分类", "count": item.count}
        for item in categories
    ]
    
    return {
        "code": 200,
        "data": data
    }


@router.get("/hot-products", response_model=dict, summary="获取热销商品")
def get_hot_products(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db)
):
    """
    获取热销商品列表
    """
    hot_products = db.query(
        Product,
        func.sum(Order.quantity).label('sales')
    ).join(
        Order, Product.product_id == Order.product_id
    ).filter(
        Product.status == 1
    ).group_by(
        Product.product_id
    ).order_by(
        desc('sales')
    ).limit(limit).all()
    
    items = []
    for product, sales in hot_products:
        merchant = db.query(Merchant).filter(Merchant.merchant_id == product.merchant_id).first()
        
        item = {
            "product_id": product.product_id,
            "name": product.name,
            "price": float(product.price),
            "sales_count": int(sales),
            "category": product.category,
            "merchant_name": merchant.name if merchant else "未知商家"
        }
        items.append(item)
    
    return {
        "code": 200,
        "data": items
    }
