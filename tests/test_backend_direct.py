"""
直接测试后端认证逻辑
"""
import sys
sys.path.insert(0, 'd:/PyCharm/code/pythonProject2/sqlwork/backend')

try:
    print("=" * 70)
    print("测试后端认证逻辑")
    print("=" * 70)
    
    print("\n1. 导入模块...")
    from database import SessionLocal
    from models import User
    from services.auth import verify_password, authenticate_user
    
    print("✓ 模块导入成功")
    
    print("\n2. 创建数据库会话...")
    db = SessionLocal()
    print("✓ 数据库会话创建成功")
    
    print("\n3. 查询用户 zhang_san...")
    user = db.query(User).filter(User.username == "zhang_san").first()
    
    if user:
        print(f"✓ 找到用户: {user.username}")
        print(f"  用户ID: {user.user_id}")
        print(f"  密码hash: {user.password_hash[:60]}...")
        
        print("\n4. 测试密码验证...")
        try:
            result = verify_password("password123", user.password_hash)
            print(f"✓ 密码验证结果: {result}")
        except Exception as e:
            print(f"✗ 密码验证失败: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n5. 测试完整认证流程...")
        try:
            auth_user = authenticate_user(db, "zhang_san", "password123")
            if auth_user:
                print(f"✓ 认证成功: {auth_user.username}")
            else:
                print("✗ 认证失败: 返回None")
        except Exception as e:
            print(f"✗ 认证过程出错: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("✗ 未找到用户 zhang_san")
    
    db.close()
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback
    traceback.print_exc()
