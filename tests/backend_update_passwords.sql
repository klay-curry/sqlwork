USE online_mall;

-- 更新所有用户的密码为 password123
UPDATE users SET password_hash = '$2b$12$FLfPcTrjlEczMNS4Rd7qc.VM8flp0CRvdZw/DdBvrJY.vI3mxosqO';

-- 更新所有商家的密码为 merchant123
UPDATE merchants SET password_hash = '$2b$12$maX06u/VRxL98DSQ5B1gFu17.kxS7Y2RRD1UyAsxeeRkOhmcViYTi';

-- 验证更新结果
SELECT '--- 用户密码哈希 ---' as info;
SELECT username, password_hash FROM users LIMIT 2;

SELECT '--- 商家密码哈希 ---' as info;
SELECT name, password_hash FROM merchants LIMIT 2;
