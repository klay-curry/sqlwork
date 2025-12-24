"""
认证相关API路由
用户/商家注册、登录
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from models import User, Merchant, UserRegister, UserLogin, MerchantRegister, Token, UserResponse, MerchantResponse
from services.auth import (
    get_password_hash,
    authenticate_user,
    authenticate_merchant,
    create_access_token
)
from config import settings

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register/user", response_model=UserResponse, summary="用户注册")
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    用户注册接口
    
    - **username**: 用户名（唯一）
    - **password**: 密码
    - **email**: 邮箱
    - **phone**: 手机号（可选）
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建新用户
    new_user = User(
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        email=user_data.email,
        phone=user_data.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/register/merchant", response_model=MerchantResponse, summary="商家注册")
def register_merchant(merchant_data: MerchantRegister, db: Session = Depends(get_db)):
    """
    商家注册接口
    
    - **name**: 商家名称（唯一）
    - **password**: 密码
    - **contact_person**: 联系人（可选）
    - **phone**: 联系电话（可选）
    """
    # 检查商家名称是否已存在
    existing_merchant = db.query(Merchant).filter(Merchant.name == merchant_data.name).first()
    if existing_merchant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="商家名称已存在"
        )
    
    # 创建新商家
    new_merchant = Merchant(
        name=merchant_data.name,
        password_hash=get_password_hash(merchant_data.password),
        contact_person=merchant_data.contact_person,
        phone=merchant_data.phone
    )
    
    db.add(new_merchant)
    db.commit()
    db.refresh(new_merchant)
    
    return new_merchant


@router.post("/login", response_model=Token, summary="登录")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    统一登录接口
    
    - **username**: 用户名或商家名称
    - **password**: 密码
    - **role**: 角色类型（user=买家, merchant=商家）
    """
    if login_data.role == "user":
        # 用户登录
        user = authenticate_user(db, login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 生成JWT Token
        access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user.user_id, "role": "user"},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    elif login_data.role == "merchant":
        # 商家登录
        merchant = authenticate_merchant(db, login_data.username, login_data.password)
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="商家名称或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 生成JWT Token
        access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"merchant_id": merchant.merchant_id, "role": "merchant"},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的角色类型，必须是 user 或 merchant"
        )
