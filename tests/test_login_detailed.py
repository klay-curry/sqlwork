"""
测试登录API并显示详细错误信息
"""
import requests
import json

# 测试买家登录
print("=" * 70)
print("测试买家登录 API")
print("=" * 70)

login_data = {
    "username": "zhang_san",
    "password": "password123",
    "role": "user"
}

print(f"\n请求数据: {json.dumps(login_data, ensure_ascii=False)}")

try:
    response = requests.post(
        "http://localhost:8000/api/auth/login",
        json=login_data,
        timeout=5
    )
    
    print(f"\n状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"\n响应内容:")
    
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
        
    if response.status_code == 200:
        print("\n✓ 登录成功！")
    else:
        print(f"\n✗ 登录失败: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n✗ 连接失败: 无法连接到后端服务")
    print("提示: 请确保后端服务已启动 (python main.py)")
except requests.exceptions.Timeout:
    print("\n✗ 请求超时")
except Exception as e:
    print(f"\n✗ 错误: {e}")

print("\n" + "=" * 70)
