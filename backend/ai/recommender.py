"""
协同过滤推荐引擎
基于物品的协同过滤算法（Item-Based Collaborative Filtering）
"""
import numpy as np
import pandas as pd
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Order, Product, Merchant


class RecommendationEngine:
    """
    推荐引擎类
    实现基于物品的协同过滤算法
    """
    
    def __init__(self, db: Session):
        """
        初始化推荐引擎
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self.user_item_matrix = None
        self.item_similarity = None
    
    def build_user_item_matrix(self):
        """
        构建用户-商品评分矩阵
        使用购买次数作为隐式评分
        """
        # 查询所有订单数据
        orders = self.db.query(
            Order.user_id,
            Order.product_id,
            func.count(Order.order_id).label('purchase_count')
        ).group_by(
            Order.user_id, Order.product_id
        ).all()
        
        if not orders:
            return None
        
        # 转换为DataFrame
        data = [
            {"user_id": order.user_id, "product_id": order.product_id, "rating": order.purchase_count}
            for order in orders
        ]
        df = pd.DataFrame(data)
        
        # 构建用户-商品矩阵（透视表）
        matrix = df.pivot_table(
            index='user_id',
            columns='product_id',
            values='rating',
            fill_value=0
        )
        
        self.user_item_matrix = matrix
        return matrix
    
    def calculate_item_similarity(self):
        """
        计算商品相似度矩阵
        使用余弦相似度
        """
        if self.user_item_matrix is None:
            self.build_user_item_matrix()
        
        if self.user_item_matrix is None or self.user_item_matrix.shape[0] == 0:
            return None
        
        # 转置矩阵（商品为行，用户为列）
        item_matrix = self.user_item_matrix.T
        
        # 计算余弦相似度
        from sklearn.metrics.pairwise import cosine_similarity
        similarity = cosine_similarity(item_matrix)
        
        # 转换为DataFrame
        self.item_similarity = pd.DataFrame(
            similarity,
            index=item_matrix.index,
            columns=item_matrix.index
        )
        
        return self.item_similarity
    
    def get_user_recommendations(self, user_id: int, top_n: int = 10) -> List[Dict]:
        """
        为用户生成个性化推荐
        
        Args:
            user_id: 用户ID
            top_n: 推荐数量
            
        Returns:
            推荐商品列表
        """
        # 构建相似度矩阵
        if self.item_similarity is None:
            self.calculate_item_similarity()
        
        # 如果数据不足，返回热门商品
        if self.item_similarity is None:
            return self._get_hot_products(top_n)
        
        # 查询用户已购买的商品
        user_orders = self.db.query(Order.product_id).filter(
            Order.user_id == user_id
        ).distinct().all()
        
        purchased_items = [order.product_id for order in user_orders]
        
        if not purchased_items:
            # 新用户，返回热门商品
            return self._get_hot_products(top_n)
        
        # 计算推荐分数
        recommendations = {}
        
        for item_id in purchased_items:
            if item_id not in self.item_similarity.columns:
                continue
            
            # 获取与该商品相似的商品
            similar_items = self.item_similarity[item_id].sort_values(ascending=False)
            
            for sim_item_id, similarity_score in similar_items.items():
                # 跳过已购买的商品
                if sim_item_id in purchased_items:
                    continue
                
                # 累加相似度分数
                if sim_item_id not in recommendations:
                    recommendations[sim_item_id] = 0
                recommendations[sim_item_id] += similarity_score
        
        # 排序并取Top N
        sorted_recommendations = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        # 查询商品详情
        result = []
        for product_id, score in sorted_recommendations:
            product = self.db.query(Product).filter(
                Product.product_id == product_id,
                Product.status == 1  # 仅上架商品
            ).first()
            
            if product:
                merchant = self.db.query(Merchant).filter(
                    Merchant.merchant_id == product.merchant_id
                ).first()
                
                result.append({
                    "product_id": product.product_id,
                    "name": product.name,
                    "price": float(product.price),
                    "category": product.category,
                    "merchant_name": merchant.name if merchant else "未知商家",
                    "reason": "基于您的购买历史推荐",
                    "score": float(score)
                })
        
        # 如果推荐不足，补充热门商品
        if len(result) < top_n:
            hot_products = self._get_hot_products(top_n - len(result), exclude_ids=[r["product_id"] for r in result])
            result.extend(hot_products)
        
        return result
    
    def _get_hot_products(self, top_n: int, exclude_ids: List[int] = None) -> List[Dict]:
        """
        获取热门商品（兜底策略）
        
        Args:
            top_n: 返回数量
            exclude_ids: 需要排除的商品ID列表
            
        Returns:
            热门商品列表
        """
        query = self.db.query(
            Product,
            func.sum(Order.quantity).label('sales')
        ).join(
            Order, Product.product_id == Order.product_id, isouter=True
        ).filter(
            Product.status == 1
        )
        
        if exclude_ids:
            query = query.filter(~Product.product_id.in_(exclude_ids))
        
        hot_products = query.group_by(
            Product.product_id
        ).order_by(
            func.sum(Order.quantity).desc()
        ).limit(top_n).all()
        
        result = []
        for product, sales in hot_products:
            merchant = self.db.query(Merchant).filter(
                Merchant.merchant_id == product.merchant_id
            ).first()
            
            result.append({
                "product_id": product.product_id,
                "name": product.name,
                "price": float(product.price),
                "category": product.category,
                "merchant_name": merchant.name if merchant else "未知商家",
                "reason": "热门商品推荐"
            })
        
        return result


def get_user_recommendations(db: Session, user_id: int, top_n: int = 10) -> List[Dict]:
    """
    为用户生成推荐列表（外部调用接口）
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        top_n: 推荐数量
        
    Returns:
        推荐商品列表
    """
    engine = RecommendationEngine(db)
    return engine.get_user_recommendations(user_id, top_n)
