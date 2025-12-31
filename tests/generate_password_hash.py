"""
生成正确的密码哈希并生成 SQL 更新语句
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 生成用户密码哈希
user_password = "password123"
user_hash = pwd_context.hash(user_password)

# 生成商家密码哈希
merchant_password = "merchant123"
merchant_hash = pwd_context.hash(merchant_password)

print("=" * 70)
print("密码哈希生成成功")
print("=" * 70)
print(f"\n用户密码: {user_password}")
print(f"用户哈希: {user_hash}")
print(f"\n商家密码: {merchant_password}")
print(f"商家哈希: {merchant_hash}")

print("\n" + "=" * 70)
print("SQL 更新语句（复制到 MySQL 中执行）")
print("=" * 70)

sql_statements = f"""
USE online_mall;

-- 更新所有用户的密码为 password123
UPDATE users SET password_hash = '{user_hash}';

-- 更新所有商家的密码为 merchant123
UPDATE merchants SET password_hash = '{merchant_hash}';

-- 验证更新结果
SELECT username, LEFT(password_hash, 30) as pwd_preview FROM users LIMIT 2;
SELECT name, LEFT(password_hash, 30) as pwd_preview FROM merchants LIMIT 2;
"""

print(sql_statements)

print("=" * 70)
print("提示：复制上面的 SQL 语句到 MySQL 中执行即可")
print("=" * 70)

# 验证生成的哈希
print("\n" + "=" * 70)
print("验证新生成的哈希")
print("=" * 70)
user_verify = pwd_context.verify(user_password, user_hash)
merchant_verify = pwd_context.verify(merchant_password, merchant_hash)
print(f"用户密码验证: {'✓ 成功' if user_verify else '✗ 失败'}")
print(f"商家密码验证: {'✓ 成功' if merchant_verify else '✗ 失败'}")
