"""
修复登录问题 - 更新数据库中的测试账号密码
直接使用MySQL连接,不依赖项目模块
"""
import pymysql

# 数据库配置(与backend/config.py保持一致)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '151362',  # 你的MySQL密码
    'database': 'online_mall',
    'charset': 'utf8mb4'
}

def main():
    print("=" * 70)
    print("修复测试账号密码")
    print("=" * 70)
    
    # 正确的密码hash（使用bcrypt生成，对应password123和merchant123）
    correct_hash = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'
    
    try:
        # 连接数据库
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print(f"\n✓ 已连接到数据库: {DB_CONFIG['database']}")
        
        # 更新所有用户密码
        cursor.execute("UPDATE users SET password_hash = %s", (correct_hash,))
        user_count = cursor.rowcount
        
        # 更新所有商家密码  
        cursor.execute("UPDATE merchants SET password_hash = %s", (correct_hash,))
        merchant_count = cursor.rowcount
        
        # 提交更改
        conn.commit()
        
        print(f"\n✓ 已更新 {user_count} 个用户的密码")
        print(f"✓ 已更新 {merchant_count} 个商家的密码")
        
        # 验证更新
        cursor.execute("SELECT username FROM users LIMIT 3")
        users = cursor.fetchall()
        print(f"\n用户列表: {[u[0] for u in users]}")
        
        cursor.execute("SELECT name FROM merchants LIMIT 3")
        merchants = cursor.fetchall()
        print(f"商家列表: {[m[0] for m in merchants]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ 修复完成！现在可以使用以下账号登录：")
        print("=" * 70)
        print("\n买家账号:")
        print("  用户名: zhang_san")
        print("  密码: password123")
        print("\n商家账号:")
        print("  用户名: 数码专营店")
        print("  密码: merchant123")
        print("\n" + "=" * 70)
        print("\n下一步：刷新浏览器登录页面，重新登录即可！")
        print("=" * 70)
        return 0
        
    except pymysql.Error as e:
        print(f"\n✗ 数据库错误: {e}")
        print("\n可能的原因:")
        print("  1. MySQL服务未运行")
        print("  2. 数据库密码不正确（检查脚本中的DB_CONFIG）")
        print("  3. 数据库尚未初始化")
        return 1
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
