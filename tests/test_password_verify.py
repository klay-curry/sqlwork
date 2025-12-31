"""
测试密码验证
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 数据库中的哈希值
db_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

# 测试不同的密码
test_passwords = ["password123", "123456", "admin", "merchant123"]

print("=" * 60)
print("测试密码验证")
print("=" * 60)
print(f"数据库哈希值: {db_hash}")
print(f"哈希值长度: {len(db_hash)}")
print()

for pwd in test_passwords:
    try:
        result = pwd_context.verify(pwd, db_hash)
        print(f"密码 '{pwd}': {'✓ 匹配' if result else '✗ 不匹配'}")
    except Exception as e:
        print(f"密码 '{pwd}': ✗ 验证出错 - {e}")

# 生成新的哈希值
print("\n" + "=" * 60)
print("生成新的密码哈希")
print("=" * 60)
new_hash = pwd_context.hash("password123")
print(f"password123 的新哈希: {new_hash}")
print(f"新哈希长度: {len(new_hash)}")

# 验证新哈希
try:
    result = pwd_context.verify("password123", new_hash)
    print(f"新哈希验证: {'✓ 成功' if result else '✗ 失败'}")
except Exception as e:
    print(f"新哈希验证出错: {e}")
