"""
数据库ORM模型定义
SQLAlchemy模型类
"""
from sqlalchemy import Column, BigInteger, String, Integer, DECIMAL, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """用户表模型"""
    __tablename__ = "users"
    
    user_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户唯一标识')
    username = Column(String(50), unique=True, nullable=False, index=True, comment='登录用户名')
    password_hash = Column(String(128), nullable=False, comment='bcrypt加密后的密码')
    email = Column(String(100), nullable=False, index=True, comment='用户邮箱')
    phone = Column(String(15), comment='联系电话')
    created_at = Column(DateTime, server_default=func.now(), comment='注册时间')
    
    # 关系
    orders = relationship("Order", back_populates="user")


class Merchant(Base):
    """商家表模型"""
    __tablename__ = "merchants"
    
    merchant_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='商家唯一标识')
    name = Column(String(100), nullable=False, index=True, comment='商家名称')
    contact_person = Column(String(50), comment='联系人姓名')
    phone = Column(String(15), comment='联系电话')
    password_hash = Column(String(128), nullable=False, comment='bcrypt加密后的密码')
    registered_at = Column(DateTime, server_default=func.now(), comment='入驻时间')
    
    # 关系
    products = relationship("Product", back_populates="merchant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="merchant")


class Product(Base):
    """商品表模型"""
    __tablename__ = "products"
    
    product_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='商品唯一标识')
    merchant_id = Column(BigInteger, ForeignKey('merchants.merchant_id', ondelete='CASCADE'), nullable=False, comment='所属商家ID')
    name = Column(String(100), nullable=False, comment='商品名称')
    description = Column(Text, comment='商品详细描述')
    price = Column(DECIMAL(10, 2), nullable=False, comment='商品价格')
    stock = Column(Integer, default=0, comment='库存数量')
    category = Column(String(50), comment='商品类目')
    status = Column(Integer, default=1, comment='1=上架, 2=下架')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    
    # 关系
    merchant = relationship("Merchant", back_populates="products")
    orders = relationship("Order", back_populates="product")
    
    # 组合索引
    __table_args__ = (
        Index('idx_merchant_status', 'merchant_id', 'status'),
        Index('idx_category_status', 'category', 'status'),
    )


class Order(Base):
    """订单表模型"""
    __tablename__ = "orders"
    
    order_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='订单唯一标识')
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='RESTRICT'), nullable=False, comment='买家ID')
    product_id = Column(BigInteger, ForeignKey('products.product_id', ondelete='RESTRICT'), nullable=False, comment='商品ID')
    merchant_id = Column(BigInteger, ForeignKey('merchants.merchant_id', ondelete='RESTRICT'), nullable=False, comment='商家ID')
    quantity = Column(Integer, nullable=False, comment='购买数量')
    unit_price = Column(DECIMAL(10, 2), nullable=False, comment='下单时单价')
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment='订单总金额')
    order_time = Column(DateTime, server_default=func.now(), comment='下单时间')
    status = Column(String(20), default='pending', comment='订单状态')
    review = Column(Text, comment='买家评价内容')
    
    # 关系
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    merchant = relationship("Merchant", back_populates="orders")
    
    # 组合索引
    __table_args__ = (
        Index('idx_user_time', 'user_id', 'order_time'),
        Index('idx_merchant_time', 'merchant_id', 'order_time'),
        Index('idx_product', 'product_id'),
    )
