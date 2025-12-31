"""
调试登录功能 - 直接测试数据库和认证逻辑
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal
from models import User, Merchant
from services.auth import verify_password

def test_login():
    print("=" * 70)
    print("调试登录功能")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # 测试用户登录
        print("\n1. 查询用户 zhang_san")
        user = db.query(User).filter(User.username == "zhang_san").first()
        
        if user:
            print(f"✓ 找到用户: {user.username}")
            print(f"  用户ID: {user.user_id}")
            print(f"  密码hash前30位: {user.password_hash[:30]}...")
            
            # 测试密码验证
            print("\n2. 测试密码验证")
            try:
                is_valid = verify_password("password123", user.password_hash)
                print(f"  验证'password123': {is_valid}")
            except Exception as e:
                print(f"  ✗ 密码验证出错: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("✗ 未找到用户 zhang_san")
        
        # 测试商家登录
        print("\n3. 查询商家 数码专营店")
        merchant = db.query(Merchant).filter(Merchant.name == "数码专营店").first()
        
        if merchant:
            print(f"✓ 找到商家: {merchant.name}")
            print(f"  商家ID: {merchant.merchant_id}")
            print(f"  密码hash前30位: {merchant.password_hash[:30]}...")
            
            # 测试密码验证
            print("\n4. 测试商家密码验证")
            try:
                is_valid = verify_password("merchant123", merchant.password_hash)
                print(f"  验证'merchant123': {is_valid}")
            except Exception as e:
                print(f"  ✗ 密码验证出错: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("✗ 未找到商家 数码专营店")
            
    except Exception as e:
        print(f"\n✗ 数据库错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_login()
