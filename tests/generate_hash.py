#!/usr/bin/env python3
"""
生成测试账号的密码hash
用于更新数据库中的密码
"""
import sys
sys.path.insert(0, '.')

from services.auth import get_password_hash

# 生成 password123 的hash
user_password = "password123"
user_hash = get_password_hash(user_password)

# 生成 merchant123 的hash
merchant_password = "merchant123"
merchant_hash = get_password_hash(merchant_password)

print("=" * 60)
print("测试账号密码Hash")
print("=" * 60)
print(f"\n用户密码: {user_password}")
print(f"Hash值: {user_hash}")
print(f"\n商家密码: {merchant_password}")
print(f"Hash值: {merchant_hash}")
print("\n" + "=" * 60)
print("更新SQL语句（复制到MySQL中执行）：")
print("=" * 60)
print(f"\nUSE online_mall;")
print(f"\n-- 更新所有用户密码为 password123")
print(f"UPDATE users SET password_hash = '{user_hash}';")
print(f"\n-- 更新所有商家密码为 merchant123")
print(f"UPDATE merchants SET password_hash = '{merchant_hash}';")
print(f"\n-- 验证更新")
print(f"SELECT username, LEFT(password_hash, 30) as pwd_preview FROM users LIMIT 2;")
print(f"SELECT name, LEFT(password_hash, 30) as pwd_preview FROM merchants LIMIT 2;")
print("\n" + "=" * 60)
print("\n复制上面的SQL语句，在MySQL中执行即可修复登录问题！")
print("=" * 60)
