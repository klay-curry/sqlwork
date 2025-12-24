-- 网上商城系统数据库表结构
-- MySQL 8.0+

-- 创建数据库
CREATE DATABASE IF NOT EXISTS online_mall CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE online_mall;

-- 删除已存在的表（按依赖关系倒序删除）
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS merchants;
DROP TABLE IF EXISTS users;

-- ============================================
-- 用户表 (users)
-- ============================================
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户唯一标识',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '登录用户名',
    password_hash VARCHAR(128) NOT NULL COMMENT 'bcrypt加密后的密码',
    email VARCHAR(100) NOT NULL COMMENT '用户邮箱',
    phone VARCHAR(15) DEFAULT NULL COMMENT '联系电话',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 商家表 (merchants)
-- ============================================
CREATE TABLE merchants (
    merchant_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '商家唯一标识',
    name VARCHAR(100) NOT NULL COMMENT '商家名称',
    contact_person VARCHAR(50) DEFAULT NULL COMMENT '联系人姓名',
    phone VARCHAR(15) DEFAULT NULL COMMENT '联系电话',
    password_hash VARCHAR(128) NOT NULL COMMENT 'bcrypt加密后的密码',
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '入驻时间',
    
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商家表';

-- ============================================
-- 商品表 (products)
-- ============================================
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '商品唯一标识',
    merchant_id BIGINT NOT NULL COMMENT '所属商家ID',
    name VARCHAR(100) NOT NULL COMMENT '商品名称',
    description TEXT DEFAULT NULL COMMENT '商品详细描述',
    price DECIMAL(10,2) NOT NULL COMMENT '商品价格',
    stock INT DEFAULT 0 COMMENT '库存数量',
    category VARCHAR(50) DEFAULT NULL COMMENT '商品类目',
    status TINYINT DEFAULT 1 COMMENT '1=上架, 2=下架',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    INDEX idx_merchant_status (merchant_id, status),
    INDEX idx_category_status (category, status),
    FULLTEXT INDEX ft_search (name, description),
    
    CONSTRAINT chk_price_positive CHECK (price > 0),
    CONSTRAINT chk_stock_nonnegative CHECK (stock >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品表';

-- ============================================
-- 订单表 (orders)
-- ============================================
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '订单唯一标识',
    user_id BIGINT NOT NULL COMMENT '买家ID',
    product_id BIGINT NOT NULL COMMENT '商品ID',
    merchant_id BIGINT NOT NULL COMMENT '商家ID',
    quantity INT NOT NULL COMMENT '购买数量',
    unit_price DECIMAL(10,2) NOT NULL COMMENT '下单时单价',
    total_amount DECIMAL(10,2) NOT NULL COMMENT '订单总金额',
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '订单状态',
    review TEXT DEFAULT NULL COMMENT '买家评价内容',
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE RESTRICT,
    INDEX idx_user_time (user_id, order_time),
    INDEX idx_merchant_time (merchant_id, order_time),
    INDEX idx_product (product_id),
    
    CONSTRAINT chk_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_unit_price_positive CHECK (unit_price > 0),
    CONSTRAINT chk_total_positive CHECK (total_amount > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- ============================================
-- 触发器：确保订单总金额正确
-- ============================================
DELIMITER //
CREATE TRIGGER trg_orders_before_insert
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    SET NEW.total_amount = NEW.unit_price * NEW.quantity;
END//

CREATE TRIGGER trg_orders_before_update
BEFORE UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.quantity != OLD.quantity OR NEW.unit_price != OLD.unit_price THEN
        SET NEW.total_amount = NEW.unit_price * NEW.quantity;
    END IF;
END//
DELIMITER ;

-- ============================================
-- 视图：商品销量统计
-- ============================================
CREATE OR REPLACE VIEW view_product_sales AS
SELECT 
    p.product_id,
    p.name,
    p.merchant_id,
    p.category,
    p.price,
    p.stock,
    COALESCE(SUM(o.quantity), 0) AS total_sales,
    COUNT(DISTINCT o.order_id) AS order_count
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_id, p.name, p.merchant_id, p.category, p.price, p.stock;

-- ============================================
-- 数据库初始化完成
-- ============================================
