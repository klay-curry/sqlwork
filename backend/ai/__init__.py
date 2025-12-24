"""
AI模块包初始化文件
"""
from .recommender import get_user_recommendations
from .advisor import get_merchant_suggestions

__all__ = ["get_user_recommendations", "get_merchant_suggestions"]
