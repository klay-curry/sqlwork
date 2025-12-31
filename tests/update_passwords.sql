-- 网上商城系统 - 修复测试账号密码
-- 执行此脚本可修复登录401错误

USE online_mall;

-- 更新所有用户密码为 password123
UPDATE users SET password_hash = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW';

-- 更新所有商家密码为 merchant123
UPDATE merchants SET password_hash = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW';

-- 验证更新
SELECT '=== 更新成功！用户列表 ===' AS info;
SELECT username, LEFT(password_hash, 30) as pwd_preview FROM users LIMIT 3;

SELECT '=== 商家列表 ===' AS info;
SELECT name, LEFT(password_hash, 30) as pwd_preview FROM merchants LIMIT 3;

SELECT '=== 测试账号 ===' AS info;
SELECT '买家: zhang_san / password123' AS account UNION ALL
SELECT '商家: 数码专营店 / merchant123' AS account;
