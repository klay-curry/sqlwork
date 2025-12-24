-- 网上商城系统测试数据
-- 依赖：schema.sql 必须先执行

USE online_mall;

-- ============================================
-- 插入测试用户数据
-- ============================================
-- 密码都是 'password123' 的bcrypt加密结果
INSERT INTO users (username, password_hash, email, phone) VALUES
('zhang_san', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq', 'zhangsan@example.com', '13800138001'),
('li_si', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq', 'lisi@example.com', '13800138002'),
('wang_wu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq', 'wangwu@example.com', '13800138003'),
('zhao_liu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq', 'zhaoliu@example.com', '13800138004'),
('sun_qi', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq', 'sunqi@example.com', '13800138005');

-- ============================================
-- 插入测试商家数据
-- ============================================
-- 密码都是 'merchant123' 的bcrypt加密结果
INSERT INTO merchants (name, contact_person, phone, password_hash) VALUES
('数码专营店', '李经理', '13900139001', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq'),
('时尚服饰馆', '王经理', '13900139002', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq'),
('家居生活店', '张经理', '13900139003', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq'),
('美食特产铺', '赵经理', '13900139004', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEm3Dq');

-- ============================================
-- 插入测试商品数据
-- ============================================
-- 商家1：数码专营店
INSERT INTO products (merchant_id, name, description, price, stock, category, status) VALUES
(1, '无线蓝牙耳机', '高音质降噪，续航30小时，支持快充', 299.00, 150, '数码', 1),
(1, '手机支架', '车载桌面两用，360度旋转', 29.90, 500, '数码', 1),
(1, '充电宝20000毫安', '快充双口输出，LED电量显示', 129.00, 200, '数码', 1),
(1, 'Type-C数据线', '尼龙编织，支持100W快充', 39.90, 800, '数码', 1),
(1, '无线鼠标', '静音设计，人体工学，2.4G连接', 89.00, 300, '数码', 1),
(1, '机械键盘', '青轴RGB背光，全键无冲', 399.00, 100, '数码', 1),
(1, '手机壳iPhone15', '透明防摔，精准开孔', 49.00, 600, '数码', 1),
(1, '钢化膜', '高清防指纹，9H硬度', 19.90, 1000, '数码', 1);

-- 商家2：时尚服饰馆
INSERT INTO products (merchant_id, name, description, price, stock, category, status) VALUES
(2, '男士T恤纯棉', '100%精梳棉，透气舒适', 89.00, 200, '服饰', 1),
(2, '女士连衣裙', '法式优雅，显瘦收腰', 199.00, 150, '服饰', 1),
(2, '运动鞋跑步鞋', '轻便透气，缓震回弹', 299.00, 180, '服饰', 1),
(2, '牛仔裤男', '修身小脚，弹力面料', 159.00, 220, '服饰', 1),
(2, '羽绒服加厚', '90%白鸭绒，保暖防风', 599.00, 80, '服饰', 1),
(2, '围巾针织款', '柔软亲肤，多色可选', 39.00, 300, '服饰', 1),
(2, '皮带商务款', '头层牛皮，自动扣', 99.00, 150, '服饰', 1);

-- 商家3：家居生活店
INSERT INTO products (merchant_id, name, description, price, stock, category, status) VALUES
(3, '乳胶枕记忆枕', '人体工学，护颈助眠', 129.00, 100, '家居', 1),
(3, '四件套纯棉', '60支长绒棉，亲肤柔软', 299.00, 80, '家居', 1),
(3, '懒人沙发', '可拆洗，多角度调节', 399.00, 50, '家居', 1),
(3, '收纳箱塑料', '大容量，可叠加', 49.00, 200, '家居', 1),
(3, '台灯护眼', '无频闪，三档调光', 159.00, 120, '家居', 1),
(3, '挂钩免打孔', '强力粘胶，承重5kg', 9.90, 500, '家居', 1),
(3, '垃圾桶分类', '按压开盖，双层设计', 79.00, 150, '家居', 1);

-- 商家4：美食特产铺
INSERT INTO products (merchant_id, name, description, price, stock, category, status) VALUES
(4, '坚果礼盒装', '每日坚果混合装，独立小包', 99.00, 300, '食品', 1),
(4, '茶叶铁观音', '原产地直供，清香回甘', 168.00, 100, '食品', 1),
(4, '牛肉干内蒙古', '手撕风干，原汁原味', 59.00, 200, '食品', 1),
(4, '蜂蜜土蜂蜜', '纯天然无添加，500g装', 89.00, 150, '食品', 1),
(4, '红枣新疆若羌', '香甜核小，补血养颜', 39.00, 400, '食品', 1);

-- ============================================
-- 插入测试订单数据（模拟历史购买记录）
-- ============================================
-- 用户1：zhang_san 购买记录
INSERT INTO orders (user_id, product_id, merchant_id, quantity, unit_price, status, order_time) VALUES
(1, 1, 1, 1, 299.00, 'completed', '2025-12-01 10:30:00'),
(1, 3, 1, 1, 129.00, 'completed', '2025-12-03 14:20:00'),
(1, 9, 2, 2, 89.00, 'completed', '2025-12-05 16:45:00'),
(1, 15, 3, 1, 129.00, 'completed', '2025-12-08 11:10:00'),
(1, 22, 4, 3, 99.00, 'completed', '2025-12-10 09:25:00');

-- 用户2：li_si 购买记录
INSERT INTO orders (user_id, product_id, merchant_id, quantity, unit_price, status, order_time) VALUES
(2, 1, 1, 2, 299.00, 'completed', '2025-12-02 15:00:00'),
(2, 2, 1, 1, 29.90, 'completed', '2025-12-04 10:30:00'),
(2, 10, 2, 1, 199.00, 'completed', '2025-12-06 13:40:00'),
(2, 16, 3, 2, 299.00, 'completed', '2025-12-07 17:20:00'),
(2, 23, 4, 1, 168.00, 'pending', '2025-12-20 14:15:00');

-- 用户3：wang_wu 购买记录
INSERT INTO orders (user_id, product_id, merchant_id, quantity, unit_price, status, order_time) VALUES
(3, 3, 1, 1, 129.00, 'completed', '2025-12-01 11:25:00'),
(3, 5, 1, 1, 89.00, 'completed', '2025-12-05 09:50:00'),
(3, 11, 2, 1, 299.00, 'completed', '2025-12-09 16:30:00'),
(3, 17, 3, 1, 399.00, 'completed', '2025-12-12 10:45:00'),
(3, 25, 4, 2, 39.00, 'completed', '2025-12-15 13:20:00');

-- 用户4：zhao_liu 购买记录
INSERT INTO orders (user_id, product_id, merchant_id, quantity, unit_price, status, order_time) VALUES
(4, 4, 1, 3, 39.90, 'completed', '2025-12-03 08:15:00'),
(4, 6, 1, 1, 399.00, 'completed', '2025-12-06 14:40:00'),
(4, 12, 2, 2, 159.00, 'completed', '2025-12-10 11:30:00'),
(4, 18, 3, 3, 49.00, 'completed', '2025-12-13 15:50:00'),
(4, 24, 4, 1, 59.00, 'pending', '2025-12-22 09:10:00');

-- 用户5：sun_qi 购买记录
INSERT INTO orders (user_id, product_id, merchant_id, quantity, unit_price, status, order_time) VALUES
(5, 7, 1, 2, 49.00, 'completed', '2025-12-02 16:20:00'),
(5, 8, 1, 5, 19.90, 'completed', '2025-12-04 12:35:00'),
(5, 13, 2, 1, 599.00, 'completed', '2025-12-08 10:15:00'),
(5, 19, 3, 2, 159.00, 'completed', '2025-12-11 14:25:00'),
(5, 22, 4, 2, 99.00, 'completed', '2025-12-14 11:40:00');

-- 添加更多近期订单（用于趋势分析）
INSERT INTO orders (user_id, product_id, merchant_id, quantity, unit_price, status, order_time) VALUES
(1, 5, 1, 1, 89.00, 'completed', '2025-12-16 10:00:00'),
(2, 11, 2, 1, 299.00, 'completed', '2025-12-17 14:30:00'),
(3, 15, 3, 1, 129.00, 'completed', '2025-12-18 09:20:00'),
(4, 22, 4, 4, 99.00, 'completed', '2025-12-19 16:45:00'),
(5, 1, 1, 1, 299.00, 'completed', '2025-12-20 11:15:00'),
(1, 10, 2, 2, 199.00, 'completed', '2025-12-21 13:50:00'),
(2, 3, 1, 1, 129.00, 'completed', '2025-12-22 15:30:00'),
(3, 23, 4, 1, 168.00, 'completed', '2025-12-23 10:40:00');

-- ============================================
-- 验证数据插入
-- ============================================
SELECT '=== 数据统计 ===' AS info;
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS merchant_count FROM merchants;
SELECT COUNT(*) AS product_count FROM products;
SELECT COUNT(*) AS order_count FROM orders;

SELECT '=== 商品销量Top5 ===' AS info;
SELECT name, total_sales FROM view_product_sales ORDER BY total_sales DESC LIMIT 5;

-- ============================================
-- 测试数据初始化完成
-- ============================================
