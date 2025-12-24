"""
认证工具模块
JWT Token生成和验证、密码加密
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from models import User, Merchant, TokenData

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer认证
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 加密后的密码
        
    Returns:
        bool: 密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    密码加密
    
    Args:
        password: 明文密码
        
    Returns:
        str: 加密后的密码
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    
    Args:
        data: 要编码的数据字典
        expires_delta: 过期时间差
        
    Returns:
        str: JWT令牌
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """
    解码JWT令牌
    
    Args:
        token: JWT令牌
        
    Returns:
        TokenData: 令牌载荷数据
        
    Raises:
        HTTPException: 令牌无效或过期
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: Optional[int] = payload.get("user_id")
        merchant_id: Optional[int] = payload.get("merchant_id")
        role: str = payload.get("role")
        
        if role is None:
            raise credentials_exception
            
        token_data = TokenData(user_id=user_id, merchant_id=merchant_id, role=role)
        return token_data
        
    except JWTError:
        raise credentials_exception


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    
    Args:
        credentials: HTTP Bearer凭证
        db: 数据库会话
        
    Returns:
        User: 当前用户对象
        
    Raises:
        HTTPException: 未授权或用户不存在
    """
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    if token_data.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足：需要用户身份"
        )
    
    user = db.query(User).filter(User.user_id == token_data.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return user


def get_current_merchant(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Merchant:
    """
    获取当前登录商家
    
    Args:
        credentials: HTTP Bearer凭证
        db: 数据库会话
        
    Returns:
        Merchant: 当前商家对象
        
    Raises:
        HTTPException: 未授权或商家不存在
    """
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    if token_data.role != "merchant":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足：需要商家身份"
        )
    
    merchant = db.query(Merchant).filter(Merchant.merchant_id == token_data.merchant_id).first()
    if merchant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商家不存在"
        )
    
    return merchant


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    认证用户
    
    Args:
        db: 数据库会话
        username: 用户名
        password: 密码
        
    Returns:
        Optional[User]: 用户对象或None
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def authenticate_merchant(db: Session, name: str, password: str) -> Optional[Merchant]:
    """
    认证商家
    
    Args:
        db: 数据库会话
        name: 商家名称
        password: 密码
        
    Returns:
        Optional[Merchant]: 商家对象或None
    """
    merchant = db.query(Merchant).filter(Merchant.name == name).first()
    if not merchant:
        return None
    if not verify_password(password, merchant.password_hash):
        return None
    return merchant
