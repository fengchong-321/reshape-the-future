# 第 7 周 - MySQL 基础

## 学习目标
掌握 MySQL 数据库的基本操作，能够熟练编写 SQL 语句进行数据查询和管理。

---

## 知识点清单

### 1. 安装配置
**掌握程度**: 本地安装 MySQL、用户权限

**练习资源**:
- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [MySQL 教程 - 菜鸟教程](https://www.runoob.com/mysql/mysql-tutorial.html)

**练习任务**:
- 本地安装 MySQL（或用 Docker 运行）
- 创建用户并授权
- 连接数据库

---

### 2. 数据类型
**掌握程度**: int/varchar/text/datetime/decimal

**练习任务**:
- 理解每种类型的用途
- 为场景选择合适的数据类型

---

### 3. DDL（数据定义语言）
**掌握程度**: CREATE/ALTER/DROP TABLE

**练习任务**:
- 创建表
- 修改表结构（添加列、修改列、删除列）
- 删除表

---

### 4. DML（数据操作语言）
**掌握程度**: INSERT/UPDATE/DELETE

**练习任务**:
- 插入数据
- 更新数据
- 删除数据
- 理解 DELETE 和 TRUNCATE 的区别

---

### 5. 简单查询
**掌握程度**: SELECT/WHERE/ORDER BY/LIMIT

**练习任务**:
- 20 道简单查询练习
- 条件过滤
- 排序和分页

---

### 6. 聚合函数
**掌握程度**: COUNT/SUM/AVG/MAX/MIN

**练习任务**:
- 10 道聚合查询练习
- 分组统计

---

### 7. 分组
**掌握程度**: GROUP BY/HAVING

**练习任务**:
- 10 道分组查询练习
- 理解 WHERE 和 HAVING 的区别

---

### 8. 连接
**掌握程度**: INNER/LEFT/RIGHT JOIN

**练习任务**:
- 15 道连接查询练习
- 理解各种 JOIN 的区别

---

## 本周练习任务

### 必做任务

1. **环境搭建**
```bash
# 选项 1: 本地安装 MySQL
# 选项 2: Docker 运行 MySQL
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0
```

2. **创建电商数据库**
```sql
-- 创建数据库和表
CREATE DATABASE ecommerce;
USE ecommerce;

-- 创建用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建商品表
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建订单表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status TINYINT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建订单明细表
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

3. **SQL 练习题（50 道）**
- 牛客网 SQL 练习：https://www.nowcoder.com/exam/oj?tab=SQL%E7%AF%87&topicId=199
- LeetCode Database 题目

4. **插入测试数据**
```sql
-- 每个表至少插入 20 条测试数据
-- 用于后续查询练习
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 50 道 SQL 题 AC 率 90%+
- [ ] 能设计一个电商数据库 schema（5 张表）
- [ ] 能解释 JOIN 的工作原理
- [ ] 能编写复杂查询语句
- [ ] 理解事务的基本概念

---

## SQL 语句速查表

### 基础查询
```sql
SELECT * FROM table;
SELECT col1, col2 FROM table;
SELECT DISTINCT col FROM table;
SELECT COUNT(*) FROM table;
```

### 条件过滤
```sql
SELECT * FROM table WHERE col = value;
SELECT * FROM table WHERE col > value;
SELECT * FROM table WHERE col LIKE '%pattern%';
SELECT * FROM table WHERE col IN (v1, v2);
SELECT * FROM table WHERE col BETWEEN v1 AND v2;
SELECT * FROM table WHERE col IS NULL;
```

### 排序和分页
```sql
SELECT * FROM table ORDER BY col DESC;
SELECT * FROM table ORDER BY col1, col2 DESC;
SELECT * FROM table LIMIT 10;
SELECT * FROM table LIMIT 10 OFFSET 20;
```

### 聚合和分组
```sql
SELECT COUNT(*), SUM(col), AVG(col) FROM table;
SELECT col, COUNT(*) FROM table GROUP BY col;
SELECT col, COUNT(*) FROM table GROUP BY col HAVING COUNT(*) > 5;
```

### 连接查询
```sql
-- INNER JOIN
SELECT a.*, b.* FROM a INNER JOIN b ON a.id = b.a_id;

-- LEFT JOIN
SELECT a.*, b.* FROM a LEFT JOIN b ON a.id = b.a_id;

-- RIGHT JOIN
SELECT a.*, b.* FROM a RIGHT JOIN b ON a.id = b.a_id;

-- 多表连接
SELECT * FROM a
JOIN b ON a.id = b.a_id
JOIN c ON b.id = c.b_id;
```

### 子查询
```sql
SELECT * FROM table WHERE col IN (SELECT col FROM table2);
SELECT * FROM table WHERE col > (SELECT AVG(col) FROM table);
```

---

## 面试考点

### 高频面试题
1. INNER JOIN 和 LEFT JOIN 的区别？
2. WHERE 和 HAVING 的区别？
3. COUNT(*) 和 COUNT(col) 的区别？
4. 什么是主键、外键、索引？
5. 什么是事务？ACID 特性？
6. 什么是视图？有什么作用？
7. 什么是存储过程？

### 场景题
```sql
-- 1. 查询每个用户的订单数量
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id;

-- 2. 查询消费总额最高的前 10 个用户
SELECT u.username, SUM(o.total_amount) as total
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY total DESC
LIMIT 10;

-- 3. 查询没有下过单的用户
SELECT * FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM orders);

-- 4. 查询每个商品的销售数量
SELECT p.name, SUM(oi.quantity) as total_sold
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id;
```

---

## 每日学习检查清单

### Day 1-2: 安装 + 基础
- [ ] 安装 MySQL
- [ ] 学习数据类型
- [ ] 学习 DDL
- [ ] 创建数据库和表

### Day 3-4: DML + 简单查询
- [ ] 学习 INSERT/UPDATE/DELETE
- [ ] 学习 SELECT/WHERE
- [ ] 完成 20 道查询题
- [ ] 插入测试数据

### Day 5-6: 聚合 + 分组 + 连接
- [ ] 学习聚合函数
- [ ] 学习 GROUP BY/HAVING
- [ ] 学习 JOIN
- [ ] 完成 30 道练习题

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成剩余练习
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 7 周总结

### 学习内容
- 掌握了 MySQL 基础
- 能编写 SQL 查询
- 理解了 JOIN

### 练习题
- 完成题目数：XX
- AC 率：XX%

### 遇到的问题
- ...

### 下周改进
- ...
```
