"""
修复测试账号密码
直接连接数据库更新密码hash
"""
import pymysql
from passlib.context import CryptContext

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 数据库配置（根据你的config.py）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '151362',  # 你的MySQL密码
    'database': 'online_mall',
    'charset': 'utf8mb4'
}

def main():
    print("=" * 60)
    print("修复测试账号密码")
    print("=" * 60)
    
    # 生成密码hash
    user_password = "password123"
    user_hash = pwd_context.hash(user_password)
    
    merchant_password = "merchant123"
    merchant_hash = pwd_context.hash(merchant_password)
    
    print(f"\n✓ 已生成密码Hash")
    print(f"  用户密码: {user_password}")
    print(f"  Hash: {user_hash[:50]}...")
    print(f"  商家密码: {merchant_password}")
    print(f"  Hash: {merchant_hash[:50]}...")
    
    # 连接数据库
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print(f"\n✓ 已连接到数据库: {DB_CONFIG['database']}")
        
        # 更新所有用户密码
        cursor.execute("UPDATE users SET password_hash = %s", (user_hash,))
        user_count = cursor.rowcount
        print(f"\n✓ 已更新 {user_count} 个用户的密码")
        
        # 更新所有商家密码
        cursor.execute("UPDATE merchants SET password_hash = %s", (merchant_hash,))
        merchant_count = cursor.rowcount
        print(f"✓ 已更新 {merchant_count} 个商家的密码")
        
        # 提交更改
        conn.commit()
        print("\n✓ 数据库更新成功！")
        
        # 验证
        cursor.execute("SELECT username FROM users LIMIT 3")
        users = cursor.fetchall()
        print(f"\n用户列表: {[u[0] for u in users]}")
        
        cursor.execute("SELECT name FROM merchants LIMIT 3")
        merchants = cursor.fetchall()
        print(f"商家列表: {[m[0] for m in merchants]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("修复完成！现在可以使用以下账号登录：")
        print("=" * 60)
        print("\n买家账号:")
        print("  用户名: zhang_san")
        print("  密码: password123")
        print("\n商家账号:")
        print("  用户名: 数码专营店")
        print("  密码: merchant123")
        print("\n" + "=" * 60)
        
    except pymysql.Error as e:
        print(f"\n✗ 数据库错误: {e}")
        print("\n请检查:")
        print("  1. MySQL服务是否运行")
        print("  2. 数据库密码是否正确（修改脚本中的DB_CONFIG）")
        print("  3. 数据库是否已初始化")
    except Exception as e:
        print(f"\n✗ 错误: {e}")

if __name__ == "__main__":
    main()
