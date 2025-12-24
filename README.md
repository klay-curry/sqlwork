# 网上商城系统

> 基于 FastAPI + Vue3 + MySQL 的全栈电商系统，集成AI推荐与智能经营建议

## 📋 项目简介

本项目是一个融合AI能力的网上商城系统，包含以下核心功能：

- **双角色系统**：买家端 + 商家端
- **智能推荐**：基于协同过滤算法的个性化商品推荐
- **经营建议**：基于规则引擎的AI经营策略生成
- **数据可视化**：ECharts图表展示销售趋势、排行榜、类目分布
- **完整CRUD**：商品管理、订单管理、用户管理

## 🛠️ 技术栈

### 后端
- **框架**：FastAPI 0.109.0
- **数据库**：MySQL 8.0
- **ORM**：SQLAlchemy 2.0
- **认证**：JWT (python-jose)
- **AI库**：scikit-learn, pandas, numpy

### 前端（待实现）
- **框架**：Vue 3 + Element Plus
- **可视化**：ECharts 5.x
- **状态管理**：Pinia
- **HTTP客户端**：Axios

## 📁 项目结构

```
sqlwork/
├── backend/                 # 后端代码
│   ├── api/                # API路由
│   │   ├── auth.py        # 认证接口
│   │   ├── merchant.py    # 商家端接口
│   │   ├── user.py        # 买家端接口
│   │   └── common.py      # 通用接口
│   ├── models/             # 数据模型
│   │   ├── models.py      # ORM模型
│   │   └── schemas.py     # Pydantic Schema
│   ├── services/           # 业务逻辑
│   │   └── auth.py        # 认证服务
│   ├── ai/                 # AI模块
│   │   ├── recommender.py # 协同过滤推荐
│   │   └── advisor.py     # 经营建议生成
│   ├── config.py           # 配置管理
│   ├── database.py         # 数据库连接
│   ├── main.py             # FastAPI应用入口
│   └── requirements.txt    # Python依赖
├── database/                # 数据库文件
│   ├── schema.sql          # 表结构DDL
│   └── seed_data.sql       # 测试数据
├── frontend/                # 前端代码（待实现）
├── docker-compose.yml       # Docker编排
└── README.md               # 项目文档
```

## 🚀 快速开始

### 方式一：本地运行

#### 1. 准备环境
- Python 3.9+
- MySQL 8.0
- Node.js 16+ (如需运行前端)

#### 2. 初始化数据库
```bash
# 连接MySQL并执行
mysql -u root -p

# 在MySQL中执行
source database/schema.sql
source database/seed_data.sql
```

#### 3. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

#### 4. 配置环境变量
```bash
# 复制配置文件
cp .env.example .env

# 修改 .env 文件中的数据库连接信息
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/online_mall
```

#### 5. 启动后端服务
```bash
python main.py
# 或使用 uvicorn
uvicorn main:app --reload
```

后端服务启动在：http://localhost:8000
API文档地址：http://localhost:8000/docs

### 方式二：Docker部署

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📖 API接口文档

### 认证接口

#### 用户注册
```http
POST /api/auth/register/user
Content-Type: application/json

{
  "username": "zhang_san",
  "password": "password123",
  "email": "zhangsan@example.com",
  "phone": "13800138001"
}
```

#### 用户登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "zhang_san",
  "password": "password123",
  "role": "user"
}
```

### 商家端接口（需认证）

#### 获取商品列表
```http
GET /api/merchant/products?page=1&size=20
Authorization: Bearer {token}
```

#### 获取销售趋势
```http
GET /api/merchant/sales/trend?days=30
Authorization: Bearer {token}
```

#### 获取AI经营建议
```http
GET /api/merchant/ai/suggestions
Authorization: Bearer {token}
```

### 买家端接口（需认证）

#### 获取个性化推荐
```http
GET /api/user/recommendations?limit=10
Authorization: Bearer {token}
```

#### 创建订单
```http
POST /api/user/orders
Authorization: Bearer {token}
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

### 通用接口（无需认证）

#### 获取商品列表
```http
GET /api/products?page=1&size=20&category=数码
```

#### 获取热销商品
```http
GET /api/hot-products?limit=10
```

完整API文档请访问：http://localhost:8000/docs

## 🎯 核心功能说明

### 1. 协同过滤推荐算法

- **算法类型**：Item-Based Collaborative Filtering
- **数据来源**：用户历史订单
- **相似度计算**：余弦相似度
- **冷启动策略**：返回热门商品

**实现逻辑**：
1. 构建用户-商品评分矩阵（购买次数作为隐式评分）
2. 计算商品之间的相似度矩阵
3. 根据用户已购商品，推荐相似商品
4. 新用户返回热门商品兜底

### 2. AI经营建议系统

基于规则引擎，分析以下指标生成建议：

| 规则名称 | 触发条件 | 建议示例 |
|---------|---------|---------|
| 库存预警 | 周转率>2 且库存<月销*0.3 | "预计X天售罄，建议及时补货" |
| 滞销预警 | 近7天零销量且库存>50 | "建议降价促销或优化描述" |
| 促销建议 | 环比下滑>10% 且周转率<0.5 | "销量下滑X%，建议限时折扣" |
| 提价机会 | 环比增长>20% 且价格低于均价 | "可适当提价增加利润" |

### 3. 数据可视化（前端待实现）

- **销售趋势图**：折线图展示近N天销量变化
- **热销商品榜**：柱状图展示Top商品
- **类目分布图**：饼图展示各类目占比

## 🧪 测试数据

系统已预置测试数据：

- **用户**：5个测试用户（密码：password123）
- **商家**：4个测试商家（密码：merchant123）
- **商品**：30个商品，覆盖数码、服饰、家居、食品等类目
- **订单**：33条历史订单记录

测试账号：
```
买家：zhang_san / password123
商家：数码专营店 / merchant123
```

## 📊 数据库设计

### 核心表结构

- **users**: 用户表（user_id, username, email, password_hash）
- **merchants**: 商家表（merchant_id, name, password_hash）
- **products**: 商品表（product_id, merchant_id, name, price, stock, category）
- **orders**: 订单表（order_id, user_id, product_id, quantity, total_amount）

### ER关系
```
users 1--N orders N--1 products N--1 merchants
```

## 🔧 开发指南

### 添加新的API接口

1. 在 `backend/api/` 目录下对应文件添加路由函数
2. 定义Pydantic Schema（如需）
3. 实现业务逻辑
4. 访问 /docs 查看自动生成的API文档

### 扩展AI功能

- **推荐算法优化**：修改 `backend/ai/recommender.py`
- **添加新规则**：在 `backend/ai/advisor.py` 的 `_apply_rules` 方法中添加

## 📝 待办事项

- [ ] 前端Vue3项目初始化
- [ ] 实现商家数据看板页面
- [ ] 实现买家商品浏览页面
- [ ] 集成ECharts数据可视化
- [ ] 编写单元测试
- [ ] 性能优化（缓存、索引）
- [ ] 部署到生产环境

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📮 联系方式

如有问题，请提交Issue或联系开发者。

---

**注**：本项目为课程设计作品，仅供学习交流使用。
