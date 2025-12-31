# 测试与调试工具目录

本目录包含项目开发过程中使用的测试脚本、调试工具和临时修复脚本。

## 📁 文件分类

### 🧪 API测试脚本
- **test_api.py** (11KB) - 完整的API自动化测试套件，包含10个测试用例
- **test_login.py** - 登录API测试
- **test_login_detailed.py** - 详细的登录测试（带调试信息）
- **test_backend_direct.py** - 后端直连测试
- **test_password_verify.py** - 密码验证测试

### 🐛 调试工具
- **debug_login.py** - 登录功能调试工具
- **fix_login.py** - 登录问题修复脚本
- **fix_password.py** - 密码问题修复工具

### 🔐 密码工具
- **generate_hash.py** - 密码哈希生成工具
- **generate_password_hash.py** - 密码哈希生成器
- **gen_hash.py** - 哈希生成器（简化版）

### 📝 数据库脚本
- **update_passwords.sql** - 密码更新SQL脚本
- **backend_update_passwords.sql** - 后端密码更新脚本

## 🚀 使用说明

### 运行API测试
```bash
# 确保后端服务已启动
cd backend
python main.py

# 在另一个终端运行测试
cd tests
python test_api.py
```

### 生成密码哈希
```bash
cd tests
python generate_hash.py
# 按提示输入密码，获得bcrypt哈希值
```

### 测试登录功能
```bash
cd tests
python test_login_detailed.py
# 会显示详细的请求和响应信息
```

## ⚠️ 注意事项

1. **这些文件仅用于开发和调试**
   - 不应部署到生产环境
   - 包含测试数据和调试代码

2. **依赖要求**
   - 大部分脚本需要 `requests` 库
   - 密码工具需要 `bcrypt` 库
   - 确保已安装：`pip install requests bcrypt`

3. **后端服务**
   - 测试脚本默认连接 `http://localhost:8000`
   - 运行测试前请确保后端服务已启动

## 📊 测试覆盖

test_api.py 包含以下测试：
- ✅ 健康检查
- ✅ 用户注册
- ✅ 用户登录
- ✅ 商品列表查询
- ✅ 商品详情查询
- ✅ 创建订单
- ✅ 个性化推荐
- ✅ 销售趋势查询
- ✅ 热销商品查询
- ✅ AI经营建议

## 🔧 常见用途

### 问题排查
当遇到登录或认证问题时：
1. 运行 `debug_login.py` 查看详细错误信息
2. 使用 `test_password_verify.py` 验证密码是否正确
3. 如需重置密码，使用 `update_passwords.sql`

### 功能验证
在修改代码后：
1. 运行 `test_api.py` 确保所有API正常工作
2. 使用特定测试脚本验证单个功能

---
**目录用途**: 开发调试工具集合  
**环境**: 开发环境专用  
**更新时间**: 2025年12月29日
