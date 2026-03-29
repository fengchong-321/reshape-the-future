-- SQL 练习文件
-- 选中要执行的语句，按 Cmd + Enter 运行

-- 1. 查看所有客户
SELECT * FROM customers;

-- 2. 查询重量超过2公斤的包裹
SELECT * FROM packages WHERE weight > 2;

-- 3. 查询北京的客户
SELECT * FROM customers WHERE city = '北京';

-- 4. 统计每个城市的客户数量
SELECT city, COUNT(*) as num FROM customers GROUP BY city;

-- 5. 查询包裹详情（关联寄件人和收件人）
SELECT
    p.tracking_number,
    s.name as sender_name,
    r.name as receiver_name,
    p.weight,
    p.declared_value
FROM
    packages p
    JOIN customers s ON p.sender_id = s.customer_id
    JOIN customers r ON p.receiver_id = r.customer_id;

-- 6. 查询每个包裹的最新状态
SELECT p.tracking_number, sh.status, sh.location, sh.update_time
FROM packages p
    JOIN shipments sh ON p.package_id = sh.package_id
WHERE
    sh.update_time = (
        SELECT MAX(update_time)
        FROM shipments
        WHERE
            package_id = p.package_id
    );

-- 1. 查询所有已签收（delivered）的包裹的运单号、发件人姓名、收件人姓名。
select * from packages

select * from shipments sh

select distinct p.tracking_number,c1.name as sender , c2.name as recevier from packages p
join shipments s on p.package_id = s.package_id
join customers c1 on p.sender_id = c1.customer_id
join customers c2 on p.receiver_id = c2.customer_id
where s.status = 'delivered'