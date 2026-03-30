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

--2. 统计每个城市的发件数量，按数量降序排列。
-- select count(s.location) from packages p GROUP BY s.location order by count(s.location) DESC
-- join shipments s on p.package_id = s.package_id
-- where s.status = 'pick_up'

select c.city , count(p.package_id) as send_count
from customers c
left join packages p on c.customer_id = p.sender_id
GROUP by c.city
order by send_count DESC;

--3. 找出重量大于平均重量的所有包裹，显示运单号、重量、发件人姓名。
select p.tracking_number, p.weight, c.name from packages p 
join customers c on c.customer_id = p.sender_id
where p.weight > (select avg(weight) from packages)

-- 4. 查询每个包裹的运输总耗时（从第一个状态到最后一个状态的天数），只显示已签收的包裹。
select p.tracking_number,datediff(max(s.update_time),min(s.update_time)) as transport_days from packages p
join shipments s on p.package_id = s.package_id
where s.status = 'delivered'
GROUP by p.package_id

select p.tracking_number,timestampdiff(day,min(update_time),max(update_time)) as transport_days from packages p
join shipments s on p.package_id = s.package_id
where s.status = 'delivered'
GROUP by p.package_id

5. 统计每个状态（status）的包裹数量，按数量从高到低排序。
-- select s.status,count(s.status) from shipments s
-- GROUP by s.status
-- order by count(s.status) DESC

select status , count(*) as package_count
from shipments s1
where update_time = (
    select max(update_time)
    from shipments s2
    where s2.package_id =s1.package_id
)
GROUP by status
order by package_count DESC

-- 6. 查询发件量最多的前3名客户，显示客户姓名和发件数量。
select c.name , c.count(p.package_id) as send_count 
from customers c 
join packages p on p.sender_id = c.customer_id
GROUP by c.customer_id
order by send_count desc 
limit 3

-- 7. 列出所有发生过异常（status='exception'）的包裹，显示运单号、异常发生地点、异常时间。
select p.tracking_number , s.location,s.update_time from packages p
join shipments s on p.package_id = s.package_id
where s.status = 'exception'

-- 8. 为每个包裹添加一列，显示该包裹的运输状态序号（按时间顺序），并列出每个包裹的最新状态。
select package_id, tracking_number, status, location ,update_time, 
    ROW_NUMBER() over (partition by s.package_id order by s.update_time desc) as status_seq
from shipments s
join packages p on s.package_id = p.package_id

-- 9. 查询发件人和收件人来自同一个城市的包裹，显示运单号、发件人城市、收件人城市。
select p.tracking_number,c1.city as sender_ctiy,c2.city as receiver_city from packages p 
join customers c1 on c1.customer_id = p.sender_id
join customers c2 on c2.customer_id = p.receiver_id
where c1.city = c2.city

-- 10. 计算每个客户作为收件人收到的包裹总价值（declared_value），并列出总价值超过500元的客户姓名和总价值。
select c.name , sum(p.declared_value) as total_value 
from customers c
join packages p on c.receiver_id = c.customer_id 
GROUP by c.customer_id
having total_value > 500






-- 1. 查询所有客户的姓名、电话和所在城市。
-- 提示：单表查询，全表数据。
select name,phone,city
from customers

-- 2. 查询所有重量大于 3.0 公斤的包裹，显示运单号和重量。
-- 提示：使用 WHERE 条件。
select tracking_number,weight 
from packages
where weight > 3.0

-- 3. 查询所有包裹，按创建时间从新到旧排序，显示运单号、创建时间。
-- 提示：ORDER BY ... DESC。
select tracking_number, create_time
from packages
order by create_time desc

-- 4. 统计总共有多少个包裹。
-- 提示：COUNT(*)。
select count(*) as total_packages 
from packages

-- 5. 统计每个城市的客户数量，按数量降序显示。
-- 提示：对 customers 表按 city 分组，使用 COUNT(*)。
select city,count(*) as customer_count
from customers
group by city
order by customer_count desc

-- 6. 统计每个发件人（按客户姓名）的发件数量，并显示发件人姓名和发件数量。
-- 提示：连接 customers 和 packages，按发件人分组。
select c.name as sender_name , count(p.package_id) as send_count
from customers c
left join packages p on c.customer_id = p.sender_id
group by c.customer_id
order by send_count desc

-- 7. 查询所有包裹的运单号、发件人姓名、收件人姓名。
-- 提示：packages 两次连接 customers 表（分别作为发件人和收件人）。
select p.tracking_number , c1.name as sender_name ,c2.name as receiver_name
from packages p
join customers c1 on p.sender_id = c1.customer_id
join customers c2 on p.receiver_id = c2.customer_id

-- 8. 查询重量大于平均重量的包裹，显示运单号、重量。
-- 提示：先计算平均重量，再作为条件筛选（子查询或直接使用 AVG() 结果）。
select tracking_number, weight 
from packages
where weight >(
    select avg(weight) from packages
)

-- 9. 查询所有状态为 in_transit（运输中）的包裹运单号及该状态更新时间。
-- 提示：连接 shipments 和 packages，筛选状态。
select p.tracking_number, s.update_time
from packages p
join shipments s on p.package_id = s.package_id
where s.status = 'in_transit'

-- 10. 查询创建时间在 2025年3月2日 至 2025年3月3日 之间的包裹，显示运单号、创建时间。
-- 提示：BETWEEN ... AND ... 或日期比较。
select tracking_number, create_time
from packages
where create_time between '2025-03-02 00:00:00' and '2025-03-03 23:59:59'  




-- 1. 查询每个客户作为发件人和收件人的包裹数量（分别显示），如果某角色没有包裹则显示0。
-- 提示：分别统计发件和收件数量，然后全外连接（可用 UNION + 聚合模拟）。
select c.customer_id,
    c.name, 
    coalesce(s.send_cnt, 0) as send_count,
    coalesce(r.recevie_cnt, 0) as recevie_count
from customers c 
left join (
    select sender_id, count(*) as send_cnt
    from packages
    group by sender_id
) s on c.customer_id = s.sender_id
left join (
    select receiver_id, count(*) as recevie_cnt
    from packages
    group by receiver_id
) r on c.customer_id = r.receiver_id


-- 2. 找出所有包裹的运输路径（按时间顺序列出每个状态的地点），要求用逗号拼接成字符串，例如“北京→北京转运中心→上海”。
-- 提示：使用窗口函数 GROUP_CONCAT 按时间排序拼接，需注意顺序。



-- 3. 计算每个包裹从揽收到签收的总耗时（秒数），只显示已签收的包裹。
-- 提示：用 TIMESTAMPDIFF(SECOND, ...) 或 UNIX_TIMESTAMP 差值。

-- 4. 查询每个城市的收件总价值，并按总价值降序排列，只显示总价值超过500元的城市。
-- 提示：连接包裹和收件人，按城市分组，用 HAVING 过滤。

-- 5. 列出所有包裹的状态流转记录，并为每个包裹添加一列“该状态是当前包裹的第几步”（按时间正序）。
-- 提示：窗口函数 ROW_NUMBER() 搭配 PARTITION BY package_id ORDER BY update_time ASC。

-- 6. 查询发件量超过1件的客户，以及他们的发件数量、总声明价值。
-- 提示：按客户分组后用 HAVING COUNT(*) > 1，再聚合 SUM(declared_value)。

-- 7. 找出那些既是发件人又是收件人（即同一客户在包裹表中既出现在sender_id又出现在receiver_id）的客户姓名。
-- 提示：用 INNER JOIN 或 EXISTS 关联。

-- 8. 为每个包裹标记其运输状态，如果该包裹有过 exception 状态，则标记为“异常”，否则标记为“正常”。
-- 提示：用 CASE WHEN EXISTS 子查询判断是否存在异常记录。

-- 9. 查询每个客户的“净收件价值”（收到的包裹总价值 - 发出的包裹总价值），并按净价值降序显示。
-- 提示：分别计算收件总价值和发件总价值，再合并计算（可用子查询或两次聚合后连接）。

-- 10. 找出所有包裹中，运输过程中停留（状态变更）次数最多的包裹，显示运单号和停留次数（即状态记录数）。
-- 提示：对包裹分组统计状态条数，按次数降序取第一条（可用 ORDER BY + LIMIT 或窗口函数）。