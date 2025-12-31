"""
测试登录API
检查认证是否正常工作
"""
import requests

# 测试买家登录
print("=" * 60)
print("测试买家登录")
print("=" * 60)

user_login_data = {
    "username": "zhang_san",
    "password": "password123",
    "role": "user"
}

try:
    response = requests.post("http://localhost:8000/api/auth/login", json=user_login_data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    if response.status_code == 200:
        print("✓ 买家登录成功！")
        data = response.json()
        print(f"Token: {data.get('access_token', '无')[:50]}...")
    else:
        print("✗ 买家登录失败")
except Exception as e:
    print(f"✗ 请求失败: {e}")
    print("提示: 请确保后端服务已启动 (python main.py)")

# 测试商家登录
print("\n" + "=" * 60)
print("测试商家登录")
print("=" * 60)

merchant_login_data = {
    "username": "数码专营店",
    "password": "merchant123",
    "role": "merchant"
}

try:
    response = requests.post("http://localhost:8000/api/auth/login", json=merchant_login_data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    if response.status_code == 200:
        print("✓ 商家登录成功！")
        data = response.json()
        print(f"Token: {data.get('access_token', '无')[:50]}...")
    else:
        print("✗ 商家登录失败")
except Exception as e:
    print(f"✗ 请求失败: {e}")
    print("提示: 请确保后端服务已启动 (python main.py)")
