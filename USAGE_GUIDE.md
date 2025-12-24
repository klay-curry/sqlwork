# 网上商城系统 - 使用指南

## 📋 目录
1. [环境准备](#环境准备)
2. [安装部署](#安装部署)
3. [API使用示例](#api使用示例)
4. [测试账号](#测试账号)
5. [常见问题](#常见问题)

---

## 环境准备

### 必需软件
- **Python 3.9+**
- **MySQL 8.0**
- **Git**（可选）

### 可选软件
- **Docker Desktop**（用于容器化部署）
- **Postman**（用于API测试）
- **MySQL Workbench**（数据库管理工具）

---

## 安装部署

### 方式一：快速启动（推荐新手）

#### Windows用户
1. **打开PowerShell**（以管理员身份）
2. **执行启动脚本**
   ```powershell
   cd d:\PyCharm\code\pythonProject2\sqlwork
   .\start.ps1
   ```
3. **按提示操作**
   - 脚本会自动检查Python和MySQL
   - 安装Python依赖
   - 提示初始化数据库
   - 启动后端服务

#### 数据库初始化
```bash
# 连接MySQL
mysql -u root -p

# 执行SQL脚本
source database/schema.sql
source database/seed_data.sql

# 验证数据
USE online_mall;
SELECT COUNT(*) FROM products;  # 应返回30条
```

### 方式二：手动安装（推荐有经验用户）

#### 1. 克隆项目（如果从Git获取）
```bash
git clone <repository_url>
cd sqlwork
```

#### 2. 创建虚拟环境
```bash
cd backend
python -m venv venv

# Windows激活
venv\Scripts\activate

# Linux/Mac激活
source venv/bin/activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 4. 配置环境变量
```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件
# 修改数据库连接信息
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/online_mall
```

#### 5. 初始化数据库
```bash
mysql -u root -p < ../database/schema.sql
mysql -u root -p < ../database/seed_data.sql
```

#### 6. 启动服务
```bash
python main.py

# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 7. 验证启动
打开浏览器访问：
- **API文档**：http://localhost:8000/docs
- **健康检查**：http://localhost:8000/health
- **测试页面**：打开项目根目录的 `index.html`

### 方式三：Docker部署（推荐生产环境）

#### 1. 确保Docker已安装
```bash
docker --version
docker-compose --version
```

#### 2. 启动所有服务
```bash
# 在项目根目录执行
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
```

#### 3. 访问服务
- **后端API**：http://localhost:8000
- **MySQL**：localhost:3306

#### 4. 停止服务
```bash
docker-compose down

# 删除数据卷（慎用，会清空数据）
docker-compose down -v
```

---

## API使用示例

### 1. 用户注册
```bash
curl -X POST "http://localhost:8000/api/auth/register/user" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "password123",
    "email": "test@example.com",
    "phone": "13800138000"
  }'
```

**响应示例**：
```json
{
  "user_id": 6,
  "username": "test_user",
  "email": "test@example.com",
  "phone": "13800138000",
  "created_at": "2025-12-24T10:30:00"
}
```

### 2. 用户登录
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "zhang_san",
    "password": "password123",
    "role": "user"
  }'
```

**响应示例**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

**⚠️ 重要**：复制 `access_token`，后续请求需要使用

### 3. 获取个性化推荐（需要Token）
```bash
curl -X GET "http://localhost:8000/api/user/recommendations?limit=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**响应示例**：
```json
{
  "code": 200,
  "data": [
    {
      "product_id": 5,
      "name": "无线鼠标",
      "price": 89.00,
      "category": "数码",
      "merchant_name": "数码专营店",
      "reason": "基于您的购买历史推荐"
    }
  ]
}
```

### 4. 商家获取AI经营建议
```bash
# 先以商家身份登录
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "数码专营店",
    "password": "merchant123",
    "role": "merchant"
  }'

# 使用返回的Token获取建议
curl -X GET "http://localhost:8000/api/merchant/ai/suggestions" \
  -H "Authorization: Bearer YOUR_MERCHANT_TOKEN"
```

**响应示例**：
```json
{
  "code": 200,
  "data": {
    "suggestions": [
      {
        "product_id": 3,
        "product_name": "充电宝20000毫安",
        "suggestion": "库存不足，预计5天售罄，建议及时补货",
        "priority": "high",
        "metrics": {
          "recent_sales": 15,
          "change_pct": 25.5,
          "turnover_rate": 2.3,
          "current_stock": 45
        }
      }
    ]
  }
}
```

### 5. 创建订单
```bash
curl -X POST "http://localhost:8000/api/user/orders" \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

---

## 测试账号

### 买家账号（5个）
| 用户名 | 密码 | 说明 |
|--------|------|------|
| zhang_san | password123 | 测试用户1（有购买历史） |
| li_si | password123 | 测试用户2 |
| wang_wu | password123 | 测试用户3 |
| zhao_liu | password123 | 测试用户4 |
| sun_qi | password123 | 测试用户5 |

### 商家账号（4个）
| 商家名称 | 密码 | 类目 |
|---------|------|------|
| 数码专营店 | merchant123 | 数码产品 |
| 时尚服饰馆 | merchant123 | 服装鞋帽 |
| 家居生活店 | merchant123 | 家居用品 |
| 美食特产铺 | merchant123 | 食品 |

---

## 使用Swagger进行交互式测试

### 1. 打开Swagger文档
浏览器访问：http://localhost:8000/docs

### 2. 登录获取Token
1. 找到 **POST /api/auth/login** 接口
2. 点击 **Try it out**
3. 填写请求体：
   ```json
   {
     "username": "zhang_san",
     "password": "password123",
     "role": "user"
   }
   ```
4. 点击 **Execute**
5. 复制响应中的 `access_token`

### 3. 设置认证
1. 点击页面右上角 **🔒 Authorize** 按钮
2. 在弹窗中输入：`Bearer YOUR_ACCESS_TOKEN`
3. 点击 **Authorize**
4. 关闭弹窗

### 4. 测试需要认证的接口
现在可以测试任何需要认证的接口，例如：
- **GET /api/user/recommendations** - 获取推荐
- **GET /api/user/orders** - 查看订单
- **POST /api/user/orders** - 创建订单

---

## 运行自动化测试

### 1. 确保后端服务已启动
```bash
cd backend
python main.py
```

### 2. 新开一个终端，运行测试脚本
```bash
cd backend
python test_api.py
```

### 3. 查看测试结果
脚本会自动测试10个接口，输出类似：
```
============================================================
  网上商城系统 - API接口测试
============================================================

============================================================
测试 1: 健康检查
============================================================
✓ 健康检查通过: {'status': 'healthy', 'database': 'connected'}

============================================================
测试 2: 用户注册
============================================================
ℹ 用户已存在（正常情况）

...

============================================================
测试结果汇总
============================================================
健康检查: ✓ 通过
用户注册: ✓ 通过
用户登录: ✓ 通过
...

总计: 10/10 测试通过

🎉 所有测试通过！系统运行正常！
```

---

## 常见问题

### Q1: 启动时提示"连接数据库失败"
**A**: 检查以下几点：
1. MySQL服务是否启动
2. 数据库 `online_mall` 是否已创建
3. `config.py` 或 `.env` 中的数据库密码是否正确
4. 防火墙是否阻止了3306端口

**解决方法**：
```bash
# 检查MySQL服务状态
# Windows
Get-Service MySQL*

# 启动MySQL服务
net start MySQL80

# 验证数据库
mysql -u root -p
SHOW DATABASES;
USE online_mall;
```

### Q2: 导入依赖时出现错误
**A**: 可能是网络问题或Python版本不兼容

**解决方法**：
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者逐个安装
pip install fastapi uvicorn sqlalchemy pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: Token认证失败
**A**: 可能是Token过期或格式错误

**解决方法**：
1. 重新登录获取新Token
2. 确保请求头格式为：`Authorization: Bearer YOUR_TOKEN`
3. 注意 "Bearer" 后有一个空格

### Q4: 推荐接口返回热门商品而不是个性化推荐
**A**: 这是正常的冷启动策略

**说明**：
- 新用户没有购买历史，返回热门商品
- 至少购买2件不同商品后，推荐算法才会生效
- 可以使用测试账号 `zhang_san`，该用户有购买历史

### Q5: Docker启动后无法访问
**A**: 检查容器状态和端口映射

**解决方法**：
```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs backend

# 检查端口占用
# Windows
netstat -ano | findstr :8000

# 重启容器
docker-compose restart
```

### Q6: 数据库表创建失败
**A**: 可能是权限问题或SQL语法错误

**解决方法**：
```bash
# 确保使用root用户或有足够权限
mysql -u root -p

# 手动执行SQL
USE online_mall;
source d:/PyCharm/code/pythonProject2/sqlwork/database/schema.sql;

# 检查表是否创建成功
SHOW TABLES;
```

---

## 性能优化建议

### 1. 数据库优化
- 定期分析并优化查询：`ANALYZE TABLE products;`
- 清理慢查询日志
- 增加数据库连接池大小（修改 `database.py`）

### 2. 缓存策略
- 使用Redis缓存热门商品列表
- 缓存推荐结果（24小时过期）
- 缓存商品相似度矩阵

### 3. API限流
建议在生产环境添加限流中间件：
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

---

## 下一步学习

### 扩展功能建议
1. **实现购物车**：支持多商品批量下单
2. **添加评价系统**：商品评分和评论
3. **优惠券功能**：满减、折扣券
4. **订单物流**：物流状态跟踪
5. **实时推送**：WebSocket消息通知

### 学习资源
- **FastAPI官方文档**：https://fastapi.tiangolo.com/zh/
- **SQLAlchemy教程**：https://docs.sqlalchemy.org/
- **Vue3官方文档**：https://cn.vuejs.org/
- **ECharts示例**：https://echarts.apache.org/examples/

---

## 技术支持

如有问题，请：
1. 查看日志文件（后端会在终端输出详细日志）
2. 访问Swagger文档测试接口
3. 运行 `test_api.py` 自动化测试
4. 提交Issue到项目仓库

---

**祝使用愉快！🎉**
