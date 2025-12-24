"""
Pydantic Schema定义
用于API请求/响应数据验证
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ============================================
# 用户相关Schema
# ============================================
class UserRegister(BaseModel):
    """用户注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    email: EmailStr = Field(..., description="邮箱")
    phone: Optional[str] = Field(None, max_length=15, description="手机号")


class UserLogin(BaseModel):
    """用户登录请求"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    role: str = Field(..., description="角色类型：user 或 merchant")


class UserResponse(BaseModel):
    """用户信息响应"""
    user_id: int
    username: str
    email: str
    phone: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# 商家相关Schema
# ============================================
class MerchantRegister(BaseModel):
    """商家注册请求"""
    name: str = Field(..., max_length=100, description="商家名称")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    phone: Optional[str] = Field(None, max_length=15, description="联系电话")
    password: str = Field(..., min_length=6, description="密码")


class MerchantResponse(BaseModel):
    """商家信息响应"""
    merchant_id: int
    name: str
    contact_person: Optional[str]
    phone: Optional[str]
    registered_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# 商品相关Schema
# ============================================
class ProductCreate(BaseModel):
    """商品创建请求"""
    name: str = Field(..., max_length=100, description="商品名称")
    description: Optional[str] = Field(None, description="商品描述")
    price: Decimal = Field(..., gt=0, description="商品价格")
    stock: int = Field(..., ge=0, description="库存数量")
    category: Optional[str] = Field(None, max_length=50, description="商品类目")
    status: int = Field(default=1, description="商品状态：1=上架, 2=下架")


class ProductUpdate(BaseModel):
    """商品更新请求"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)
    status: Optional[int] = None


class ProductResponse(BaseModel):
    """商品信息响应"""
    product_id: int
    merchant_id: int
    name: str
    description: Optional[str]
    price: Decimal
    stock: int
    category: Optional[str]
    status: int
    created_at: datetime
    sales_count: Optional[int] = 0  # 销量（需要关联查询）
    merchant_name: Optional[str] = None  # 商家名称（关联查询）
    
    class Config:
        from_attributes = True


# ============================================
# 订单相关Schema
# ============================================
class OrderCreate(BaseModel):
    """订单创建请求"""
    product_id: int = Field(..., description="商品ID")
    quantity: int = Field(..., gt=0, description="购买数量")


class OrderResponse(BaseModel):
    """订单信息响应"""
    order_id: int
    user_id: int
    product_id: int
    merchant_id: int
    quantity: int
    unit_price: Decimal
    total_amount: Decimal
    order_time: datetime
    status: str
    review: Optional[str]
    
    # 关联信息
    product_name: Optional[str] = None
    merchant_name: Optional[str] = None
    buyer_username: Optional[str] = None
    is_reviewed: bool = False
    
    class Config:
        from_attributes = True


# ============================================
# 认证相关Schema
# ============================================
class Token(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token载荷数据"""
    user_id: Optional[int] = None
    merchant_id: Optional[int] = None
    role: str  # "user" or "merchant"


# ============================================
# 搜索相关Schema
# ============================================
class ProductSearch(BaseModel):
    """商品搜索请求"""
    keyword: str = Field(..., min_length=1, description="搜索关键词")
    category: Optional[str] = None
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)


# ============================================
# 统计数据Schema
# ============================================
class SalesTrendResponse(BaseModel):
    """销售趋势响应"""
    dates: List[str]
    sales: List[int]


class TopProductResponse(BaseModel):
    """热销商品响应"""
    name: str
    sales: int


class CategoryDistributionResponse(BaseModel):
    """类目分布响应"""
    name: str
    value: int


# ============================================
# 通用响应Schema
# ============================================
class APIResponse(BaseModel):
    """统一API响应格式"""
    code: int = 200
    message: str = "success"
    data: Optional[dict | list] = None


class PaginationResponse(BaseModel):
    """分页响应"""
    total: int
    page: int
    size: int
    items: List[dict]
