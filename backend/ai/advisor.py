"""
AI经营建议模块
基于规则引擎的智能建议生成
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from decimal import Decimal

from models import Product, Order, Merchant


class BusinessAdvisor:
    """
    商家经营建议生成器
    使用规则引擎分析销售数据并生成建议
    """
    
    def __init__(self, db: Session):
        """
        初始化建议生成器
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_merchant_suggestions(self, merchant_id: int) -> List[Dict]:
        """
        为商家生成经营建议
        
        Args:
            merchant_id: 商家ID
            
        Returns:
            建议列表
        """
        suggestions = []
        
        # 查询商家所有商品
        products = self.db.query(Product).filter(
            Product.merchant_id == merchant_id
        ).all()
        
        for product in products:
            # 分析每个商品并生成建议
            product_suggestion = self._analyze_product(product)
            if product_suggestion:
                suggestions.append(product_suggestion)
        
        return suggestions
    
    def _analyze_product(self, product: Product) -> Optional[Dict]:
        """
        分析单个商品并生成建议
        
        Args:
            product: 商品对象
            
        Returns:
            建议字典或None
        """
        # 计算近7天销量
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_sales = self.db.query(func.sum(Order.quantity)).filter(
            Order.product_id == product.product_id,
            Order.order_time >= seven_days_ago
        ).scalar() or 0
        
        # 计算前7天销量（7-14天前）
        fourteen_days_ago = datetime.now() - timedelta(days=14)
        previous_sales = self.db.query(func.sum(Order.quantity)).filter(
            Order.product_id == product.product_id,
            Order.order_time >= fourteen_days_ago,
            Order.order_time < seven_days_ago
        ).scalar() or 0
        
        # 计算近30天销量
        thirty_days_ago = datetime.now() - timedelta(days=30)
        monthly_sales = self.db.query(func.sum(Order.quantity)).filter(
            Order.product_id == product.product_id,
            Order.order_time >= thirty_days_ago
        ).scalar() or 0
        
        # 计算库存周转率
        turnover_rate = monthly_sales / product.stock if product.stock > 0 else 0
        
        # 计算环比变化率
        if previous_sales > 0:
            change_pct = ((recent_sales - previous_sales) / previous_sales) * 100
        else:
            change_pct = 100 if recent_sales > 0 else 0
        
        # 查询同类目平均价格
        avg_price = self.db.query(func.avg(Product.price)).filter(
            Product.category == product.category,
            Product.status == 1
        ).scalar() or 0
        
        # 应用规则引擎生成建议
        suggestion = self._apply_rules(
            product=product,
            recent_sales=int(recent_sales),
            change_pct=float(change_pct),
            turnover_rate=float(turnover_rate),
            monthly_sales=int(monthly_sales),
            avg_price=float(avg_price)
        )
        
        return suggestion
    
    def _apply_rules(
        self,
        product: Product,
        recent_sales: int,
        change_pct: float,
        turnover_rate: float,
        monthly_sales: int,
        avg_price: float
    ) -> Optional[Dict]:
        """
        应用规则引擎生成建议
        
        Args:
            product: 商品对象
            recent_sales: 近7天销量
            change_pct: 环比变化率
            turnover_rate: 库存周转率
            monthly_sales: 近30天销量
            avg_price: 同类目平均价格
            
        Returns:
            建议字典或None
        """
        suggestion_text = None
        priority = "low"  # low, medium, high
        
        # 规则1：库存预警
        if turnover_rate > 2 and product.stock < monthly_sales * 0.3:
            days_to_empty = int(product.stock / (monthly_sales / 30)) if monthly_sales > 0 else 0
            suggestion_text = f"库存不足，预计{days_to_empty}天售罄，建议及时补货"
            priority = "high"
        
        # 规则2：滞销预警
        elif recent_sales == 0 and product.stock > 50:
            suggestion_text = "商品近期零销量且库存较高，建议降价促销或优化商品描述"
            priority = "medium"
        
        # 规则3：促销建议
        elif change_pct < -10 and turnover_rate < 0.5:
            suggestion_text = f"销量环比下滑{abs(change_pct):.1f}%，建议设置限时折扣促销清库存"
            priority = "medium"
        
        # 规则4：提价机会
        elif change_pct > 20 and float(product.price) < avg_price * 0.9 and product.stock > 100:
            suggested_price = float(product.price) * 1.1
            suggestion_text = f"商品热销且价格低于市场均价，可适当提价至¥{suggested_price:.2f}增加利润"
            priority = "low"
        
        # 规则5：库存过高预警
        elif turnover_rate < 0.2 and product.stock > 200:
            suggestion_text = f"库存周转率仅{turnover_rate:.2f}，建议优化库存管理或开展促销活动"
            priority = "medium"
        
        # 规则6：补货建议
        elif turnover_rate > 1.5 and product.stock < 50:
            suggestion_text = "商品销售良好，建议增加备货量以满足需求"
            priority = "low"
        
        # 如果有建议，返回
        if suggestion_text:
            return {
                "product_id": product.product_id,
                "product_name": product.name,
                "suggestion": suggestion_text,
                "priority": priority,
                "metrics": {
                    "recent_sales": recent_sales,
                    "change_pct": round(change_pct, 2),
                    "turnover_rate": round(turnover_rate, 2),
                    "current_stock": product.stock,
                    "current_price": float(product.price),
                    "avg_category_price": round(avg_price, 2)
                },
                "generated_at": datetime.now().isoformat()
            }
        
        return None


def get_merchant_suggestions(db: Session, merchant_id: int) -> List[Dict]:
    """
    获取商家经营建议（外部调用接口）
    
    Args:
        db: 数据库会话
        merchant_id: 商家ID
        
    Returns:
        建议列表
    """
    advisor = BusinessAdvisor(db)
    suggestions = advisor.get_merchant_suggestions(merchant_id)
    
    # 按优先级排序
    priority_order = {"high": 0, "medium": 1, "low": 2}
    suggestions.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 3))
    
    return suggestions
