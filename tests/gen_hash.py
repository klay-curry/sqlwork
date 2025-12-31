"""
简单的密码hash生成器
只需要bcrypt库
"""
import bcrypt

# 生成用户密码 password123 的hash
user_password = b"password123"
user_hash = bcrypt.hashpw(user_password, bcrypt.gensalt()).decode('utf-8')

# 生成商家密码 merchant123 的hash  
merchant_password = b"merchant123"
merchant_hash = bcrypt.hashpw(merchant_password, bcrypt.gensalt()).decode('utf-8')

print("=" * 70)
print("测试账号密码修复SQL")
print("=" * 70)
print("\n请复制以下SQL语句，在MySQL中执行：\n")
print("-" * 70)

print(f"""
USE online_mall;

-- 更新所有用户密码为 password123
UPDATE users SET password_hash = '{user_hash}';

-- 更新所有商家密码为 merchant123
UPDATE merchants SET password_hash = '{merchant_hash}';

-- 验证更新
SELECT username, LEFT(password_hash, 30) as pwd_preview FROM users LIMIT 3;
SELECT name, LEFT(password_hash, 30) as pwd_preview FROM merchants LIMIT 3;
""")

print("-" * 70)
print("\n执行步骤：")
print("  1. 复制上面的SQL语句")
print("  2. 打开MySQL客户端（或使用命令行）")
print("  3. 粘贴并执行")
print("  4. 刷新浏览器登录页面，重新登录")
print("\n测试账号：")
print("  买家: zhang_san / password123")
print("  商家: 数码专营店 / merchant123")
print("=" * 70)
