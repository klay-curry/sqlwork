"""
API接口测试脚本
用于快速验证后端接口功能
"""
import requests
import json
from typing import Optional

# 配置
BASE_URL = "http://localhost:8000"
headers = {"Content-Type": "application/json"}


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_success(msg: str):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_error(msg: str):
    """打印错误信息"""
    print(f"{Colors.RED}✗ {msg}{Colors.END}")


def print_info(msg: str):
    """打印提示信息"""
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}{title}{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}")


def test_health_check():
    """测试健康检查接口"""
    print_section("测试 1: 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success(f"健康检查通过: {response.json()}")
            return True
        else:
            print_error(f"健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"连接失败: {str(e)}")
        print_info("请确保后端服务已启动 (python backend/main.py)")
        return False


def test_user_register():
    """测试用户注册"""
    print_section("测试 2: 用户注册")
    data = {
        "username": "test_user_001",
        "password": "test123456",
        "email": "test001@example.com",
        "phone": "13900000001"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register/user",
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            print_success(f"用户注册成功: {response.json()['username']}")
            return True
        elif response.status_code == 400:
            print_info("用户已存在（正常情况）")
            return True
        else:
            print_error(f"注册失败: {response.json()}")
            return False
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return False


def test_user_login() -> Optional[str]:
    """测试用户登录"""
    print_section("测试 3: 用户登录")
    data = {
        "username": "zhang_san",
        "password": "password123",
        "role": "user"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print_success(f"登录成功，获取Token: {token[:50]}...")
            return token
        else:
            print_error(f"登录失败: {response.json()}")
            return None
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return None


def test_merchant_login() -> Optional[str]:
    """测试商家登录"""
    print_section("测试 4: 商家登录")
    data = {
        "username": "数码专营店",
        "password": "merchant123",
        "role": "merchant"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print_success(f"商家登录成功，获取Token: {token[:50]}...")
            return token
        else:
            print_error(f"登录失败: {response.json()}")
            return None
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return None


def test_get_products():
    """测试获取商品列表（无需认证）"""
    print_section("测试 5: 获取商品列表")
    try:
        response = requests.get(f"{BASE_URL}/api/products?page=1&size=5")
        
        if response.status_code == 200:
            data = response.json()["data"]
            print_success(f"获取商品成功，共 {data['total']} 件商品")
            print_info(f"返回 {len(data['items'])} 件商品")
            for item in data['items'][:3]:
                print(f"  - {item['name']}: ¥{item['price']}")
            return True
        else:
            print_error(f"获取失败: {response.json()}")
            return False
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return False


def test_user_recommendations(token: str):
    """测试个性化推荐"""
    print_section("测试 6: 个性化推荐（AI功能）")
    try:
        response = requests.get(
            f"{BASE_URL}/api/user/recommendations?limit=5",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            recommendations = response.json()["data"]
            print_success(f"获取推荐成功，共 {len(recommendations)} 件商品")
            for item in recommendations[:3]:
                print(f"  - {item['name']} ({item['reason']})")
            return True
        else:
            print_error(f"获取失败: {response.json()}")
            return False
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return False


def test_merchant_products(token: str):
    """测试商家商品列表"""
    print_section("测试 7: 商家商品管理")
    try:
        response = requests.get(
            f"{BASE_URL}/api/merchant/products?page=1&size=5",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()["data"]
            print_success(f"获取商家商品成功，共 {data['total']} 件商品")
            for item in data['items'][:3]:
                print(f"  - {item['name']}: 库存{item['stock']}, 销量{item['sales_count']}")
            return True
        else:
            print_error(f"获取失败: {response.json()}")
            return False
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return False


def test_sales_trend(token: str):
    """测试销售趋势"""
    print_section("测试 8: 销售趋势统计")
    try:
        response = requests.get(
            f"{BASE_URL}/api/merchant/sales/trend?days=7",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()["data"]
            print_success(f"获取销售趋势成功")
            print_info(f"日期范围: {data['dates'][0]} ~ {data['dates'][-1]}")
            print_info(f"总销量: {sum(data['sales'])} 件")
            return True
        else:
            print_error(f"获取失败: {response.json()}")
            return False
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return False


def test_ai_suggestions(token: str):
    """测试AI经营建议"""
    print_section("测试 9: AI经营建议（AI功能）")
    try:
        response = requests.get(
            f"{BASE_URL}/api/merchant/ai/suggestions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            suggestions = response.json()["data"]["suggestions"]
            print_success(f"获取AI建议成功，共 {len(suggestions)} 条建议")
            for suggestion in suggestions[:3]:
                print(f"  [{suggestion['priority'].upper()}] {suggestion['product_name']}")
                print(f"    建议: {suggestion['suggestion']}")
            return True
        else:
            print_error(f"获取失败: {response.json()}")
            return False
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return False


def test_create_order(token: str):
    """测试创建订单"""
    print_section("测试 10: 创建订单")
    data = {
        "product_id": 1,
        "quantity": 1
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/user/orders",
            json=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            order_data = response.json()["data"]
            print_success(f"订单创建成功")
            print_info(f"订单ID: {order_data['order_id']}")
            print_info(f"商品: {order_data['product_name']}")
            print_info(f"总金额: ¥{order_data['total_amount']}")
            return True
        else:
            print_error(f"创建失败: {response.json()}")
            return False
    except Exception as e:
        print_error(f"请求失败: {str(e)}")
        return False


def main():
    """主测试流程"""
    print(f"{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}  网上商城系统 - API接口测试{Colors.END}")
    print(f"{Colors.GREEN}{'='*60}{Colors.END}")
    
    results = []
    
    # 1. 健康检查
    if not test_health_check():
        print_error("\n服务未启动，终止测试")
        return
    results.append(("健康检查", True))
    
    # 2. 用户注册
    results.append(("用户注册", test_user_register()))
    
    # 3. 用户登录
    user_token = test_user_login()
    results.append(("用户登录", user_token is not None))
    
    # 4. 商家登录
    merchant_token = test_merchant_login()
    results.append(("商家登录", merchant_token is not None))
    
    # 5. 获取商品列表
    results.append(("获取商品列表", test_get_products()))
    
    # 6. 用户推荐（需要用户Token）
    if user_token:
        results.append(("个性化推荐", test_user_recommendations(user_token)))
        results.append(("创建订单", test_create_order(user_token)))
    
    # 7. 商家功能（需要商家Token）
    if merchant_token:
        results.append(("商家商品列表", test_merchant_products(merchant_token)))
        results.append(("销售趋势", test_sales_trend(merchant_token)))
        results.append(("AI经营建议", test_ai_suggestions(merchant_token)))
    
    # 输出测试结果
    print_section("测试结果汇总")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✓ 通过{Colors.END}" if result else f"{Colors.RED}✗ 失败{Colors.END}"
        print(f"{name}: {status}")
    
    print(f"\n{Colors.YELLOW}总计: {passed}/{total} 测试通过{Colors.END}")
    
    if passed == total:
        print_success("\n🎉 所有测试通过！系统运行正常！")
    else:
        print_error(f"\n⚠️  有 {total - passed} 个测试失败，请检查日志")


if __name__ == "__main__":
    main()
