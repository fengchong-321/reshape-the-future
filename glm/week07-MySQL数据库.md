# 第7周：MySQL 数据库深入

## 本周目标

掌握 MySQL 数据库操作，能进行数据库测试和数据验证。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| MySQL 基础 | 安装、数据类型、表操作 | ⭐⭐⭐⭐ |
| SQL 查询 | SELECT、WHERE、JOIN | ⭐⭐⭐⭐⭐ |
| 高级查询 | 子查询、聚合、分组 | ⭐⭐⭐⭐⭐ |
| 索引优化 | 索引类型、执行计划 | ⭐⭐⭐⭐ |
| 事务 | ACID、隔离级别 | ⭐⭐⭐⭐⭐ |
| Python 操作 | pymysql、ORM | ⭐⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 MySQL 基础

```sql
-- ============================================
-- 数据类型
-- ============================================
-- 数值类型
INT         -- 整数
BIGINT      -- 大整数
DECIMAL(10,2)  -- 精确小数
FLOAT       -- 浮点数

-- 字符串类型
CHAR(10)    -- 固定长度
VARCHAR(255) -- 可变长度
TEXT        -- 长文本

-- 日期时间类型
DATE        -- 日期
TIME        -- 时间
DATETIME    -- 日期时间
TIMESTAMP   -- 时间戳

-- ============================================
-- 数据库和表操作
-- ============================================
-- 创建数据库
CREATE DATABASE test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE test_db;

-- 创建表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    age INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 查看表结构
DESC users;
SHOW CREATE TABLE users;

-- 修改表
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users MODIFY COLUMN age TINYINT;

-- 删除表
DROP TABLE IF EXISTS users;

-- ============================================
-- 数据操作（CRUD）
-- ============================================
-- 插入
INSERT INTO users (username, email, age) VALUES ('张三', 'zhangsan@example.com', 25);
INSERT INTO users (username, email) VALUES 
    ('李四', 'lisi@example.com'),
    ('王五', 'wangwu@example.com');

-- 查询
SELECT * FROM users;
SELECT id, username, email FROM users WHERE age > 20;
SELECT DISTINCT status FROM users;

-- 更新
UPDATE users SET age = 26, status = 'active' WHERE id = 1;
UPDATE users SET status = 'inactive' WHERE age < 18;

-- 删除
DELETE FROM users WHERE id = 1;
DELETE FROM users WHERE status = 'inactive';
TRUNCATE TABLE users;  -- 清空表（重置自增ID）
```

---

### 2.2 SQL 查询进阶

```sql
-- ============================================
-- 条件查询
-- ============================================
-- 基本条件
SELECT * FROM users WHERE age = 25;
SELECT * FROM users WHERE age != 25;
SELECT * FROM users WHERE age > 20 AND age < 30;
SELECT * FROM users WHERE age BETWEEN 20 AND 30;
SELECT * FROM users WHERE age IN (20, 25, 30);
SELECT * FROM users WHERE username LIKE '张%';  -- % 任意字符
SELECT * FROM users WHERE username LIKE '张_';  -- _ 单个字符
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;

-- ============================================
-- 排序和限制
-- ============================================
SELECT * FROM users ORDER BY age;              -- 升序
SELECT * FROM users ORDER BY age DESC;         -- 降序
SELECT * FROM users ORDER BY status, age DESC; -- 多字段排序

SELECT * FROM users LIMIT 10;                  -- 前10条
SELECT * FROM users LIMIT 10 OFFSET 20;        -- 从第20条开始取10条
SELECT * FROM users LIMIT 20, 10;              -- 同上

-- ============================================
-- 聚合函数
-- ============================================
SELECT COUNT(*) FROM users;                    -- 总数
SELECT COUNT(DISTINCT status) FROM users;      -- 去重计数
SELECT AVG(age) FROM users;                    -- 平均值
SELECT SUM(age) FROM users;                    -- 求和
SELECT MAX(age), MIN(age) FROM users;          -- 最大最小值

-- ============================================
-- 分组
-- ============================================
-- 基本分组
SELECT status, COUNT(*) as count 
FROM users 
GROUP BY status;

-- 分组过滤（HAVING vs WHERE）
SELECT status, AVG(age) as avg_age 
FROM users 
WHERE age > 0               -- 过滤分组前的数据
GROUP BY status 
HAVING AVG(age) > 25        -- 过滤分组后的数据
ORDER BY avg_age DESC;

-- ============================================
-- 多表连接
-- ============================================
-- 假设有以下表
-- users(id, username, email)
-- orders(id, user_id, amount, status)

-- 内连接（只返回匹配的记录）
SELECT u.username, o.amount, o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 左连接（返回左表所有记录）
SELECT u.username, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 右连接（返回右表所有记录）
SELECT u.username, o.amount
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- 自连接（同一表连接）
SELECT e1.name AS employee, e2.name AS manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;

-- 多表连接
SELECT u.username, o.amount, p.product_name
FROM users u
INNER JOIN orders o ON u.id = o.user_id
INNER JOIN products p ON o.product_id = p.id
WHERE o.status = 'completed';

-- ============================================
-- 子查询
-- ============================================
-- WHERE 子句中的子查询
SELECT * FROM users 
WHERE id IN (SELECT DISTINCT user_id FROM orders WHERE amount > 1000);

SELECT * FROM users 
WHERE age > (SELECT AVG(age) FROM users);

-- FROM 子句中的子查询
SELECT status, avg_age
FROM (
    SELECT status, AVG(age) as avg_age
    FROM users
    GROUP BY status
) AS t
WHERE avg_age > 25;

-- EXISTS 子查询
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- ============================================
-- UNION
-- ============================================
-- 合并结果（去重）
SELECT username FROM users
UNION
SELECT name FROM customers;

-- 合并结果（不去重）
SELECT username FROM users
UNION ALL
SELECT name FROM customers;
```

---

### 2.3 索引与性能优化

```sql
-- ============================================
-- 索引类型
-- ============================================
-- 主键索引（自动创建）
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50)
);

-- 唯一索引
CREATE UNIQUE INDEX idx_email ON users(email);
ALTER TABLE users ADD UNIQUE INDEX idx_email (email);

-- 普通索引
CREATE INDEX idx_username ON users(username);
ALTER TABLE users ADD INDEX idx_username (username);

-- 组合索引（最左前缀原则）
CREATE INDEX idx_status_age ON users(status, age);
-- 有效查询：
-- WHERE status = 'active'
-- WHERE status = 'active' AND age > 20
-- 无效查询：
-- WHERE age > 20  （不满足最左前缀）

-- 全文索引
CREATE FULLTEXT INDEX idx_content ON articles(content);

-- 删除索引
DROP INDEX idx_username ON users;
ALTER TABLE users DROP INDEX idx_username;

-- 查看索引
SHOW INDEX FROM users;

-- ============================================
-- 执行计划分析
-- ============================================
EXPLAIN SELECT * FROM users WHERE username = '张三';

/*
关键字段：
- id: 查询顺序
- select_type: 查询类型（SIMPLE, PRIMARY, SUBQUERY等）
- table: 表名
- type: 访问类型（从好到差）
  * system/const: 主键或唯一索引
  * eq_ref: 唯一索引扫描
  * ref: 非唯一索引扫描
  * range: 范围扫描
  * index: 全索引扫描
  * ALL: 全表扫描（需要优化）
- key: 使用的索引
- rows: 预估扫描行数
- Extra: 额外信息
  * Using index: 覆盖索引
  * Using where: WHERE 过滤
  * Using filesort: 文件排序（需要优化）
  * Using temporary: 临时表（需要优化）
*/

-- ============================================
-- 慢查询分析
-- ============================================
-- 开启慢查询日志
SET GLOBAL slow_query_log = ON;
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';
SET GLOBAL long_query_time = 1;  -- 超过1秒的查询

-- 查看慢查询
SHOW VARIABLES LIKE 'slow_query%';

-- ============================================
-- 优化建议
-- ============================================
/*
1. 避免 SELECT *
2. 使用 LIMIT 分页
3. 避免在 WHERE 中对字段进行函数操作
4. 避免 != 或 <> 导致索引失效
5. 避免 OR 导致索引失效（用 UNION 替代）
6. 组合索引遵循最左前缀原则
7. 大表使用分区
8. 定期分析表
*/
ANALYZE TABLE users;
OPTIMIZE TABLE users;
```

---

### 2.4 事务

```sql
-- ============================================
-- 事务基础
-- ============================================
-- ACID 特性
/*
A - Atomicity（原子性）：事务要么全部成功，要么全部失败
C - Consistency（一致性）：事务前后数据保持一致
I - Isolation（隔离性）：并发事务之间互不影响
D - Durability（持久性）：事务提交后永久保存
*/

-- 事务操作
START TRANSACTION;  -- 或 BEGIN

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;   -- 提交
-- 或
ROLLBACK; -- 回滚

-- 保存点
START TRANSACTION;
INSERT INTO orders (...) VALUES (...);
SAVEPOINT order_created;

INSERT INTO order_items (...) VALUES (...);
-- 如果失败
ROLLBACK TO order_created;

COMMIT;

-- ============================================
-- 隔离级别
-- ============================================
-- 查看隔离级别
SELECT @@transaction_isolation;

-- 设置隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;

/*
隔离级别（从低到高）：

1. READ UNCOMMITTED（读未提交）
   - 问题：脏读、不可重复读、幻读
   - 几乎不用

2. READ COMMITTED（读已提交）
   - 问题：不可重复读、幻读
   - Oracle 默认

3. REPEATABLE READ（可重复读）- MySQL 默认
   - 问题：幻读（但 MySQL 通过 MVCC 解决了）
   - 推荐

4. SERIALIZABLE（串行化）
   - 无问题，但性能最差
   - 极少使用

问题说明：
- 脏读：读到其他事务未提交的数据
- 不可重复读：同一事务中两次读取结果不同（修改导致）
- 幻读：同一事务中两次读取结果不同（插入/删除导致）
*/

-- ============================================
-- 锁
-- ============================================
-- 共享锁（读锁）
SELECT * FROM users WHERE id = 1 LOCK IN SHARE MODE;

-- 排他锁（写锁）
SELECT * FROM users WHERE id = 1 FOR UPDATE;

-- 行锁 vs 表锁
-- InnoDB 默认行锁，MyISAM 只有表锁

-- 查看锁
SHOW ENGINE INNODB STATUS;
SELECT * FROM information_schema.INNODB_LOCKS;
```

---

### 2.5 Python 操作 MySQL

```python
# 安装：pip install pymysql

import pymysql
from contextlib import contextmanager
from typing import List, Dict, Optional, Any

# ============================================
# 基础连接
# ============================================
def basic_connection():
    """基础连接示例"""
    # 创建连接
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        database='test_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # 返回字典
    )

    try:
        with connection.cursor() as cursor:
            # 查询
            cursor.execute("SELECT * FROM users WHERE id = %s", (1,))
            result = cursor.fetchone()
            print(result)

            # 插入
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                ('张三', 'zhangsan@example.com')
            )
            connection.commit()

    finally:
        connection.close()

# ============================================
# 数据库工具类
# ============================================
class MySQLHelper:
    """MySQL 操作工具类"""

    def __init__(self, host: str, user: str, password: str, 
                 database: str, port: int = 3306):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.connection = None

    def connect(self):
        """建立连接"""
        self.connection = pymysql.connect(**self.config)
        return self.connection

    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute(self, sql: str, params: tuple = None) -> int:
        """执行 SQL（INSERT/UPDATE/DELETE）"""
        with self.connection.cursor() as cursor:
            affected = cursor.execute(sql, params)
            self.connection.commit()
            return affected

    def query_one(self, sql: str, params: tuple = None) -> Optional[Dict]:
        """查询单条"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def query_all(self, sql: str, params: tuple = None) -> List[Dict]:
        """查询多条"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def insert(self, table: str, data: Dict) -> int:
        """插入数据，返回自增ID"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        with self.connection.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            self.connection.commit()
            return cursor.lastrowid

    def insert_batch(self, table: str, data_list: List[Dict]) -> int:
        """批量插入"""
        if not data_list:
            return 0

        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['%s'] * len(data_list[0]))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        values = [tuple(d.values()) for d in data_list]

        with self.connection.cursor() as cursor:
            affected = cursor.executemany(sql, values)
            self.connection.commit()
            return affected

    def update(self, table: str, data: Dict, where: Dict) -> int:
        """更新数据"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        with self.connection.cursor() as cursor:
            affected = cursor.execute(sql, tuple(data.values()) + tuple(where.values()))
            self.connection.commit()
            return affected

    def delete(self, table: str, where: Dict) -> int:
        """删除数据"""
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        with self.connection.cursor() as cursor:
            affected = cursor.execute(sql, tuple(where.values()))
            self.connection.commit()
            return affected

    def transaction(self):
        """开始事务"""
        self.connection.begin()
        return self

    def commit(self):
        """提交事务"""
        self.connection.commit()

    def rollback(self):
        """回滚事务"""
        self.connection.rollback()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.connection.rollback()
        self.close()

# ============================================
# 使用示例
# ============================================
# 基本使用
with MySQLHelper('localhost', 'root', 'password', 'test_db') as db:
    # 查询
    users = db.query_all("SELECT * FROM users WHERE age > %s", (20,))
    
    # 插入
    user_id = db.insert('users', {
        'username': '李四',
        'email': 'lisi@example.com',
        'age': 28
    })
    
    # 更新
    db.update('users', {'age': 29}, {'id': user_id})
    
    # 删除
    db.delete('users', {'id': user_id})

# 事务使用
with MySQLHelper('localhost', 'root', 'password', 'test_db') as db:
    try:
        db.transaction()
        db.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        db.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
        db.commit()
    except Exception as e:
        db.rollback()
        raise
```

---

### 2.6 数据库测试实践

```python
import pytest
import pymysql

# ============================================
# Pytest Fixture
# ============================================
@pytest.fixture(scope="module")
def db():
    """数据库连接 fixture"""
    db = MySQLHelper('localhost', 'root', 'password', 'test_db')
    db.connect()
    yield db
    db.close()

@pytest.fixture
def clean_users(db):
    """清理用户表"""
    db.execute("DELETE FROM users")
    db.connection.commit()
    yield

# ============================================
# 测试用例
# ============================================
class TestUserAPI:

    def test_create_user_db(self, db, clean_users, api_client):
        """测试创建用户 - 验证数据库"""
        # API 创建
        response = api_client.post("/users", json={
            "username": "test_user",
            "email": "test@example.com"
        })
        assert response.status_code == 201

        # 验证数据库
        user = db.query_one(
            "SELECT * FROM users WHERE username = %s",
            ("test_user",)
        )
        assert user is not None
        assert user["email"] == "test@example.com"

    def test_update_user_db(self, db, api_client):
        """测试更新用户 - 验证数据库"""
        # 准备数据
        user_id = db.insert("users", {
            "username": "update_test",
            "email": "update@example.com"
        })

        # API 更新
        response = api_client.put(f"/users/{user_id}", json={
            "email": "updated@example.com"
        })
        assert response.status_code == 200

        # 验证数据库
        user = db.query_one("SELECT * FROM users WHERE id = %s", (user_id,))
        assert user["email"] == "updated@example.com"

# ============================================
# 数据驱动测试
# ============================================
@pytest.mark.parametrize("username,email,expected", [
    ("user1", "user1@example.com", True),
    ("user2", "user2@example.com", True),
    ("", "user3@example.com", False),  # 用户名为空
    ("user4", "", False),  # 邮箱为空
])
def test_create_user_data_driven(db, clean_users, api_client, username, email, expected):
    """数据驱动测试"""
    response = api_client.post("/users", json={
        "username": username,
        "email": email
    })

    if expected:
        assert response.status_code == 201
        user = db.query_one("SELECT * FROM users WHERE username = %s", (username,))
        assert user is not None
    else:
        assert response.status_code == 400

# ============================================
# 测试数据准备
# ============================================
@pytest.fixture
def test_users(db):
    """准备测试用户数据"""
    users = [
        {"username": "user1", "email": "user1@test.com", "age": 25},
        {"username": "user2", "email": "user2@test.com", "age": 30},
        {"username": "user3", "email": "user3@test.com", "age": 35},
    ]
    
    user_ids = db.insert_batch("users", users)
    yield user_ids
    
    # 清理
    db.execute("DELETE FROM users WHERE id IN (%s, %s, %s)", tuple(user_ids))

def test_with_test_data(db, test_users):
    """使用准备好的测试数据"""
    users = db.query_all("SELECT * FROM users WHERE id IN (%s, %s, %s)", tuple(test_users))
    assert len(users) == 3
```

---

## 三、学到什么程度

### 必须掌握

- [ ] SQL 基础查询（SELECT, WHERE, JOIN）
- [ ] 聚合和分组
- [ ] Python 操作 MySQL
- [ ] 事务的基本概念

### 应该了解

- [ ] 索引优化
- [ ] 执行计划分析
- [ ] 隔离级别

---

## 四、练习内容

### 基础练习（1-8）

---

#### 练习1：数据库和表创建

**场景说明**：作为测试工程师，你需要为一个电商系统创建测试数据库和基础表结构。

**具体需求**：
1. 创建数据库 `test_db`，字符集为 `utf8mb4`
2. 创建用户表 `users`，包含以下字段：
   - `id`：主键，自增
   - `username`：用户名，非空，唯一
   - `email`：邮箱，非空
   - `age`：年龄，默认值 0
   - `status`：状态，枚举值('active', 'inactive')，默认 'active'
   - `created_at`：创建时间，默认当前时间
3. 创建订单表 `orders`，包含以下字段：
   - `id`：主键，自增
   - `user_id`：用户ID，外键关联 users 表
   - `amount`：金额，DECIMAL(10,2)
   - `status`：订单状态，枚举值('pending', 'completed', 'cancelled')
   - `created_at`：创建时间

**使用示例**：
```sql
-- 创建数据库
CREATE DATABASE test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE test_db;

-- 创建用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    age INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建订单表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 验证表结构
DESC users;
DESC orders;
SHOW CREATE TABLE users;
```

**验收标准**：
- [ ] 数据库创建成功，字符集正确
- [ ] users 表结构正确，包含所有字段
- [ ] orders 表结构正确，外键关联正确
- [ ] 默认值和约束设置正确

---

---

#### 练习2：数据插入和查询

**场景说明**：你需要为测试准备基础数据，并验证数据插入和查询功能。

**具体需求**：
1. 向 `users` 表插入 5 条测试数据，包含不同的用户名、邮箱和年龄
2. 向 `orders` 表插入 10 条测试数据，关联不同的用户
3. 使用 `SELECT *` 查询所有数据
4. 使用 `WHERE` 条件查询年龄大于 25 的用户
5. 使用 `WHERE` 条件查询状态为 completed 的订单

**使用示例**：
```sql
-- 插入用户数据
INSERT INTO users (username, email, age, status) VALUES
    ('张三', 'zhangsan@example.com', 25, 'active'),
    ('李四', 'lisi@example.com', 30, 'active'),
    ('王五', 'wangwu@example.com', 22, 'inactive'),
    ('赵六', 'zhaoliu@example.com', 28, 'active'),
    ('钱七', 'qianqi@example.com', 35, 'active');

-- 插入订单数据
INSERT INTO orders (user_id, amount, status) VALUES
    (1, 100.00, 'completed'),
    (1, 200.50, 'pending'),
    (2, 150.00, 'completed'),
    (2, 300.00, 'completed'),
    (2, 50.00, 'cancelled'),
    (3, 500.00, 'pending'),
    (4, 80.00, 'completed'),
    (4, 120.00, 'pending'),
    (5, 600.00, 'completed'),
    (5, 450.00, 'completed');

-- 查询所有用户
SELECT * FROM users;

-- 查询年龄大于 25 的用户
SELECT * FROM users WHERE age > 25;

-- 查询状态为 completed 的订单
SELECT * FROM orders WHERE status = 'completed';

-- 验证插入数量
SELECT COUNT(*) as user_count FROM users;  -- 应该返回 5
SELECT COUNT(*) as order_count FROM orders; -- 应该返回 10
```

**验收标准**：
- [ ] 成功插入 5 条用户数据
- [ ] 成功插入 10 条订单数据
- [ ] WHERE 条件查询结果正确
- [ ] 理解 INSERT 和 SELECT 基本语法

---

---

#### 练习3：条件查询和排序

**场景说明**：你需要从数据库中筛选特定条件的数据，这在测试数据验证中非常常见。

**具体需求**：
1. 使用 `BETWEEN` 查询年龄在 20-30 之间的用户
2. 使用 `IN` 查询状态为 active 或 pending 的数据
3. 使用 `LIKE` 模糊查询邮箱包含特定字符串的用户
4. 使用 `ORDER BY` 按年龄降序排列用户
5. 使用 `ORDER BY` 按金额升序排列订单

**使用示例**：
```sql
-- 查询年龄在 20-30 之间的用户
SELECT * FROM users WHERE age BETWEEN 20 AND 30;

-- 查询状态为 active 的用户
SELECT * FROM users WHERE status IN ('active');

-- 查询订单状态为 pending 或 completed 的订单
SELECT * FROM orders WHERE status IN ('pending', 'completed');

-- 查询邮箱包含 @example.com 的用户
SELECT * FROM users WHERE email LIKE '%@example.com';

-- 查询用户名以"张"开头的用户
SELECT * FROM users WHERE username LIKE '张%';

-- 按年龄降序排列用户
SELECT * FROM users ORDER BY age DESC;

-- 按金额升序排列订单
SELECT * FROM orders ORDER BY amount ASC;

-- 多字段排序：先按状态排序，再按金额降序
SELECT * FROM orders ORDER BY status, amount DESC;

-- 使用 LIMIT 获取前3名消费最高的订单
SELECT * FROM orders ORDER BY amount DESC LIMIT 3;
```

**验收标准**：
- [ ] BETWEEN 查询结果正确
- [ ] IN 查询结果正确
- [ ] LIKE 模糊查询结果正确
- [ ] ORDER BY 排序结果正确
- [ ] 理解 ASC 和 DESC 的区别

---

---

#### 练习4：聚合函数和分组

**场景说明**：你需要统计和汇总测试数据，这在生成测试报告时非常有用。

**具体需求**：
1. 使用 `COUNT` 统计记录总数
2. 使用 `AVG` 计算平均值
3. 使用 `SUM` 计算总和
4. 使用 `MAX` 和 `MIN` 获取最大最小值
5. 使用 `GROUP BY` 分组统计
6. 使用 `HAVING` 过滤分组结果

**使用示例**：
```sql
-- 统计用户总数
SELECT COUNT(*) as total_users FROM users;

-- 计算用户平均年龄
SELECT AVG(age) as avg_age FROM users;

-- 计算订单总金额
SELECT SUM(amount) as total_amount FROM orders;

-- 获取最大和最小订单金额
SELECT MAX(amount) as max_amount, MIN(amount) as min_amount FROM orders;

-- 统计每个状态的用户数量
SELECT status, COUNT(*) as count
FROM users
GROUP BY status;

-- 计算每个用户的订单总金额
SELECT user_id, COUNT(*) as order_count, SUM(amount) as total_amount
FROM orders
GROUP BY user_id;

-- 查询订单数量超过 2 的用户（使用 HAVING）
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 2;

-- 综合示例：按用户分组统计，筛选总金额大于 300 的用户
SELECT
    user_id,
    COUNT(*) as order_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM orders
GROUP BY user_id
HAVING SUM(amount) > 300
ORDER BY total_amount DESC;
```

**验收标准**：
- [ ] COUNT 统计正确
- [ ] AVG、SUM 计算正确
- [ ] GROUP BY 分组正确
- [ ] 理解 HAVING 和 WHERE 的区别

---

---

#### 练习5：多表连接查询

**场景说明**：在实际测试中，经常需要关联多个表来验证数据的完整性。

**具体需求**：
1. 使用 `INNER JOIN` 内连接查询有订单的用户
2. 使用 `LEFT JOIN` 左连接查询所有用户及其订单（包括没有订单的用户）
3. 使用 `RIGHT JOIN` 右连接查询所有订单及其用户
4. 查询每个用户的订单数量和总金额

**使用示例**：
```sql
-- 内连接：查询有订单的用户及其订单信息
SELECT u.username, u.email, o.amount, o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 左连接：查询所有用户及其订单（包括没有订单的用户）
SELECT u.username, o.amount, o.status
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 右连接：查询所有订单及其用户信息
SELECT u.username, o.amount, o.status
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- 查询每个用户的订单数量
SELECT
    u.username,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.amount), 0) as total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username;

-- 查询订单金额超过 100 的用户信息
SELECT DISTINCT u.username, u.email
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.amount > 100;

-- 多表连接：查询用户、订单及订单详情
SELECT
    u.username,
    o.id as order_id,
    o.amount,
    o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
ORDER BY o.amount DESC;
```

**验收标准**：
- [ ] INNER JOIN 结果正确
- [ ] LEFT JOIN 包含没有订单的用户
- [ ] 理解不同 JOIN 类型的区别
- [ ] 多表查询语法正确

---

---

#### 练习6：Python 基础连接

**场景说明**：使用 Python 的 pymysql 库连接 MySQL 数据库，执行基本的查询操作。

**具体需求**：
1. 使用 `pymysql.connect()` 创建数据库连接
2. 使用 `cursor.execute()` 执行 SQL 查询
3. 使用 `fetchone()` 和 `fetchall()` 获取查询结果
4. 使用 `try/finally` 确保连接正确关闭
5. 实现插入数据并查询验证的功能

**使用示例**：
```python
# tests/test_db_basic.py
import pymysql

def test_basic_connection():
    """基础数据库连接测试"""
    # 创建连接
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        database='test_db',
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            # 执行查询
            cursor.execute("SELECT * FROM users LIMIT 5")
            results = cursor.fetchall()

            # 验证结果
            assert len(results) > 0, "应该有查询结果"
            for row in results:
                print(row)

    finally:
        connection.close()


def test_insert_and_query():
    """插入数据并查询验证"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db',
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            # 插入数据
            cursor.execute(
                "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                ('test_user', 'test@example.com', 25)
            )
            connection.commit()

            # 查询验证
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                ('test_user',)
            )
            result = cursor.fetchone()
            assert result is not None, "插入的数据应该能查到"

    finally:
        connection.close()


def test_with_dict_cursor():
    """使用字典游标"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users LIMIT 1")
            result = cursor.fetchone()

            # 可以通过字段名访问
            print(result['username'])
            print(result['email'])

    finally:
        connection.close()
```
```

**验收标准**：
- [ ] 能够成功连接数据库
- [ ] 查询结果正确获取
- [ ] 插入操作成功执行
- [ ] 连接正确关闭
- [ ] 理解 DictCursor 的使用

---

---

#### 练习7：Python CRUD 操作

**场景说明**：封装数据库的增删改查操作，这是测试中最常用的数据库操作。

**具体需求**：
1. 使用 pytest fixture 管理数据库连接
2. 实现插入（Create）操作并返回自增ID
3. 实现查询（Read）操作，支持单条和多条查询
4. 实现更新（Update）操作，返回影响行数
5. 实现删除（Delete）操作，返回影响行数

**使用示例**：
```python
# tests/test_db_crud.py
import pymysql
import pytest

@pytest.fixture
def db_connection():
    """数据库连接 fixture"""
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    yield conn
    conn.close()


def test_create(db_connection):
    """测试插入数据"""
    with db_connection.cursor() as cursor:
        sql = "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)"
        cursor.execute(sql, ('new_user', 'new@example.com', 30))
        db_connection.commit()
        user_id = cursor.lastrowid
        assert user_id > 0, "插入成功应返回自增ID"
        print(f"插入成功，用户ID: {user_id}")


def test_read(db_connection):
    """测试查询数据"""
    with db_connection.cursor() as cursor:
        # 查询单条
        cursor.execute("SELECT * FROM users WHERE username = %s", ('new_user',))
        result = cursor.fetchone()
        assert result is not None, "应该能查到数据"
        assert result['username'] == 'new_user'
        assert result['email'] == 'new@example.com'

        # 查询多条
        cursor.execute("SELECT * FROM users WHERE age > %s", (20,))
        results = cursor.fetchall()
        assert len(results) > 0, "应该能查到多条数据"
        print(f"查询到 {len(results)} 条记录")


def test_update(db_connection):
    """测试更新数据"""
    with db_connection.cursor() as cursor:
        # 更新前查询
        cursor.execute("SELECT age FROM users WHERE username = %s", ('new_user',))
        old_age = cursor.fetchone()['age']

        # 执行更新
        sql = "UPDATE users SET age = %s WHERE username = %s"
        cursor.execute(sql, (35, 'new_user'))
        db_connection.commit()

        # 验证更新
        cursor.execute("SELECT age FROM users WHERE username = %s", ('new_user',))
        new_age = cursor.fetchone()['age']
        assert new_age == 35, f"年龄应更新为35，实际为{new_age}"
        assert cursor.rowcount > 0, "应该影响至少1行"


def test_delete(db_connection):
    """测试删除数据"""
    with db_connection.cursor() as cursor:
        # 先插入一条测试数据
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s)",
            ('to_delete', 'delete@test.com')
        )
        db_connection.commit()

        # 执行删除
        cursor.execute("DELETE FROM users WHERE username = %s", ('to_delete',))
        db_connection.commit()

        # 验证删除
        cursor.execute("SELECT * FROM users WHERE username = %s", ('to_delete',))
        result = cursor.fetchone()
        assert result is None, "删除后应该查不到数据"
        assert cursor.rowcount > 0, "应该影响至少1行"


def test_crud_integration(db_connection):
    """CRUD 集成测试"""
    with db_connection.cursor() as cursor:
        # Create
        cursor.execute(
            "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
            ('integration_user', 'integration@test.com', 25)
        )
        db_connection.commit()
        user_id = cursor.lastrowid

        # Read
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        assert user['username'] == 'integration_user'

        # Update
        cursor.execute("UPDATE users SET age = %s WHERE id = %s", (26, user_id))
        db_connection.commit()

        cursor.execute("SELECT age FROM users WHERE id = %s", (user_id,))
        assert cursor.fetchone()['age'] == 26

        # Delete
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db_connection.commit()

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        assert cursor.fetchone() is None
```
```

**验收标准**：
- [ ] 插入操作返回正确的自增ID
- [ ] 查询操作能正确获取单条和多条数据
- [ ] 更新操作能正确修改数据
- [ ] 删除操作能正确删除数据
- [ ] 理解 `rowcount` 和 `lastrowid` 的含义

---

---

#### 练习8：子查询基础

**场景说明**：子查询可以在一个查询中嵌套另一个查询，用于复杂的条件筛选和数据验证。

**具体需求**：
1. 在 `WHERE` 子句中使用子查询筛选数据
2. 在 `FROM` 子句中使用子查询（派生表）
3. 使用 `EXISTS` 子查询判断记录是否存在
4. 使用子查询进行比较操作

**使用示例**：
```sql
-- 查询有订单的用户
SELECT * FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders);

-- 查询年龄大于平均年龄的用户
SELECT * FROM users
WHERE age > (SELECT AVG(age) FROM users);

-- 查询订单金额最高的用户信息
SELECT * FROM users
WHERE id = (
    SELECT user_id FROM orders
    ORDER BY amount DESC
    LIMIT 1
);

-- 使用 EXISTS 查询有订单的用户
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- 使用 NOT EXISTS 查询没有订单的用户
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- 在 FROM 中使用子查询（派生表）
SELECT avg_age, COUNT(*) as count
FROM (
    SELECT user_id, AVG(amount) as avg_order
    FROM orders
    GROUP BY user_id
) as user_avg
JOIN users u ON user_avg.user_id = u.id
GROUP BY avg_age;

-- 统计每个用户的订单数（使用子查询关联）
SELECT
    u.username,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
    (SELECT SUM(amount) FROM orders o WHERE o.user_id = u.id) as total_amount
FROM users u;

-- 查询订单金额高于用户平均订单金额的订单
SELECT * FROM orders o1
WHERE amount > (
    SELECT AVG(amount) FROM orders o2
    WHERE o2.user_id = o1.user_id
);
```

**验收标准**：
- [ ] WHERE 子查询结果正确
- [ ] EXISTS 子查询结果正确
- [ ] FROM 子查询语法正确
- [ ] 理解相关子查询和非相关子查询的区别

---

### 进阶练习（9-16）

---

#### 练习9：数据库工具类

**场景说明**：封装一个通用的 MySQL 操作工具类，简化数据库操作代码，提高测试代码的可维护性。

**具体需求**：
1. `__init__(host, user, password, database, port=3306)` 初始化配置
2. `connect()` 建立数据库连接
3. `close()` 关闭连接
4. `query_one(sql, params)` 查询单条记录
5. `query_all(sql, params)` 查询多条记录
6. `insert(table, data)` 插入数据，返回自增ID
7. `update(table, data, where)` 更新数据，返回影响行数
8. `delete(table, where)` 删除数据，返回影响行数
9. 实现 `__enter__` 和 `__exit__` 支持上下文管理器

**使用示例**：
```python
# utils/db_helper.py
import pymysql
from typing import List, Dict, Optional

class MySQLHelper:
    """MySQL 操作工具类"""

    def __init__(self, host: str, user: str, password: str,
                 database: str, port: int = 3306):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.connection = None

    def connect(self):
        """建立连接"""
        self.connection = pymysql.connect(**self.config)
        return self

    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def query_one(self, sql: str, params: tuple = None) -> Optional[Dict]:
        """查询单条"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def query_all(self, sql: str, params: tuple = None) -> List[Dict]:
        """查询多条"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def insert(self, table: str, data: Dict) -> int:
        """插入数据，返回自增ID"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        with self.connection.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            self.connection.commit()
            return cursor.lastrowid

    def update(self, table: str, data: Dict, where: Dict) -> int:
        """更新数据"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        with self.connection.cursor() as cursor:
            affected = cursor.execute(sql, tuple(data.values()) + tuple(where.values()))
            self.connection.commit()
            return affected

    def delete(self, table: str, where: Dict) -> int:
        """删除数据"""
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        with self.connection.cursor() as cursor:
            affected = cursor.execute(sql, tuple(where.values()))
            self.connection.commit()
            return affected

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.connection.rollback()
        self.close()


# 使用示例
with MySQLHelper('localhost', 'root', 'password', 'test_db') as db:
    # 查询
    users = db.query_all("SELECT * FROM users WHERE age > %s", (20,))

    # 插入
    user_id = db.insert('users', {
        'username': 'test_user',
        'email': 'test@example.com',
        'age': 25
    })

    # 更新
    affected = db.update('users', {'age': 26}, {'id': user_id})

    # 删除
    affected = db.delete('users', {'id': user_id})
```
```

**验收标准**：
- [ ] 工具类能正确连接和关闭数据库
- [ ] 查询方法返回正确的结果格式
- [ ] insert 方法返回自增ID
- [ ] update/delete 方法返回影响行数
- [ ] 上下文管理器正确工作

---

---

#### 练习10：索引创建和分析

**场景说明**：索引是数据库性能优化的关键，理解索引的创建和使用对于测试性能问题非常重要。

**具体需求**：
1. 创建普通索引
2. 创建唯一索引
3. 创建组合索引（复合索引）
4. 使用 `EXPLAIN` 分析查询执行计划
5. 理解索引最左前缀原则

**使用示例**：
```sql
-- 为 username 创建普通索引
CREATE INDEX idx_username ON users(username);

-- 为 email 创建唯一索引
CREATE UNIQUE INDEX idx_email ON users(email);

-- 创建组合索引（status, age）
CREATE INDEX idx_status_age ON users(status, age);

-- 查看表的所有索引
SHOW INDEX FROM users;

-- 分析查询（使用索引）
EXPLAIN SELECT * FROM users WHERE username = '张三';
-- 关注 key 字段，应该显示 idx_username

-- 分析查询（不使用索引 - 全表扫描）
EXPLAIN SELECT * FROM users WHERE age > 25;
-- type 字段可能显示 ALL，表示全表扫描

-- 分析组合索引（最左前缀原则）
-- 有效：使用 status（索引第一列）
EXPLAIN SELECT * FROM users WHERE status = 'active';
-- key 字段应显示 idx_status_age

-- 有效：使用 status 和 age（索引前两列）
EXPLAIN SELECT * FROM users WHERE status = 'active' AND age > 20;
-- key 字段应显示 idx_status_age

-- 无效：只使用 age（不满足最左前缀）
EXPLAIN SELECT * FROM users WHERE age > 20;
-- key 字段应为 NULL，不使用组合索引

-- 删除索引
DROP INDEX idx_username ON users;
ALTER TABLE users DROP INDEX idx_email;

-- 强制使用索引
SELECT * FROM users FORCE INDEX (idx_username) WHERE username = '张三';

-- 查看索引使用情况
SELECT
    INDEX_NAME,
    CARDINALITY,
    SEQ_IN_INDEX
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'test_db' AND TABLE_NAME = 'users';
```

**验收标准**：
- [ ] 能正确创建各种类型的索引
- [ ] 能使用 EXPLAIN 分析查询
- [ ] 理解 type 字段的含义（ALL, index, range, ref, const）
- [ ] 理解组合索引最左前缀原则

---

---

#### 练习11：事务处理

**场景说明**：事务用于保证数据的一致性，在银行转账等场景中必须使用事务。

**具体需求**：
1. 理解事务的 ACID 特性
2. 实现银行转账事务（A账户减钱，B账户加钱）
3. 测试事务提交（成功场景）
4. 测试事务回滚（失败场景）
5. 使用 try/except/finally 保证事务正确处理

**使用示例**：
```python
# tests/test_transaction.py
import pymysql
import pytest

@pytest.fixture
def db():
    """数据库连接 fixture"""
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db',
        charset='utf8mb4'
    )
    yield conn
    conn.close()


def test_transaction_commit(db):
    """测试事务提交 - 银行转账成功"""
    cursor = db.cursor()

    # 查询转账前余额
    cursor.execute("SELECT balance FROM accounts WHERE id = 1")
    balance_a_before = cursor.fetchone()[0]
    cursor.execute("SELECT balance FROM accounts WHERE id = 2")
    balance_b_before = cursor.fetchone()[0]

    try:
        # 开始事务
        db.begin()

        # 转账操作：A 账户减 100
        cursor.execute(
            "UPDATE accounts SET balance = balance - 100 WHERE id = 1"
        )
        # 转账操作：B 账户加 100
        cursor.execute(
            "UPDATE accounts SET balance = balance + 100 WHERE id = 2"
        )

        # 提交事务
        db.commit()

        # 验证结果
        cursor.execute("SELECT balance FROM accounts WHERE id = 1")
        balance_a_after = cursor.fetchone()[0]
        cursor.execute("SELECT balance FROM accounts WHERE id = 2")
        balance_b_after = cursor.fetchone()[0]

        assert balance_a_after == balance_a_before - 100
        assert balance_b_after == balance_b_before + 100
        print(f"转账成功: A={balance_a_after}, B={balance_b_after}")

    except Exception as e:
        db.rollback()
        raise e


def test_transaction_rollback(db):
    """测试事务回滚 - 转账失败"""
    cursor = db.cursor()

    # 记录原始余额
    cursor.execute("SELECT balance FROM accounts WHERE id = 1")
    original_balance = cursor.fetchone()[0]

    try:
        db.begin()

        # A 账户减钱
        cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")

        # 模拟错误（比如 B 账户不存在）
        raise Exception("模拟转账失败")

        # 这行不会执行
        cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 999")

        db.commit()

    except Exception as e:
        # 发生异常，回滚事务
        db.rollback()
        print(f"事务已回滚: {e}")

    # 验证余额未变
    cursor.execute("SELECT balance FROM accounts WHERE id = 1")
    current_balance = cursor.fetchone()[0]
    assert current_balance == original_balance, "回滚后余额应该不变"


def test_transaction_with_context_manager():
    """使用上下文管理器处理事务"""
    class TransactionManager:
        def __init__(self, connection):
            self.conn = connection

        def __enter__(self):
            self.conn.begin()
            return self.conn.cursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                self.conn.rollback()
                print("事务已回滚")
            else:
                self.conn.commit()
                print("事务已提交")
            return False

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db'
    )

    try:
        with TransactionManager(conn) as cursor:
            cursor.execute("UPDATE accounts SET balance = balance - 50 WHERE id = 1")
            cursor.execute("UPDATE accounts SET balance = balance + 50 WHERE id = 2")
        # 自动提交
    except Exception:
        # 自动回滚
        pass
    finally:
        conn.close()
```
```

**验收标准**：
- [ ] 理解事务的 ACID 特性
- [ ] 能正确实现事务提交
- [ ] 能正确实现事务回滚
- [ ] 异常时数据能正确恢复

---

---

#### 练习12：批量操作

**场景说明**：在测试数据准备时，批量操作可以大幅提高效率。

**具体需求**：
1. 使用 `executemany()` 实现批量插入
2. 比较单条插入和批量插入的性能差异
3. 实现批量更新操作
4. 理解批量操作的优势和适用场景

**使用示例**：
```python
# tests/test_batch_operations.py
import pymysql
import pytest
import time

def test_batch_insert():
    """测试批量插入"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db',
        charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            # 准备批量数据
            users = [
                ('batch_user1', 'batch1@example.com', 20),
                ('batch_user2', 'batch2@example.com', 25),
                ('batch_user3', 'batch3@example.com', 30),
                ('batch_user4', 'batch4@example.com', 35),
                ('batch_user5', 'batch5@example.com', 40),
            ]

            # 批量插入
            sql = "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)"
            affected = cursor.executemany(sql, users)
            connection.commit()

            print(f"批量插入 {affected} 条记录")
            assert affected == len(users)

            # 验证插入结果
            cursor.execute(
                "SELECT * FROM users WHERE username LIKE 'batch_user%'"
            )
            results = cursor.fetchall()
            assert len(results) == len(users)

    finally:
        connection.close()


def test_performance_comparison():
    """性能对比：单条插入 vs 批量插入"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db'
    )

    n = 100  # 插入数量

    # 单条插入
    start = time.time()
    with connection.cursor() as cursor:
        for i in range(n):
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                (f'single_{i}', f'single_{i}@test.com')
            )
        connection.commit()
    single_time = time.time() - start

    # 批量插入
    start = time.time()
    with connection.cursor() as cursor:
        users = [(f'batch_{i}', f'batch_{i}@test.com') for i in range(n)]
        cursor.executemany(
            "INSERT INTO users (username, email) VALUES (%s, %s)",
            users
        )
        connection.commit()
    batch_time = time.time() - start

    print(f"单条插入 {n} 条: {single_time:.3f}s")
    print(f"批量插入 {n} 条: {batch_time:.3f}s")
    print(f"批量插入快 {single_time/batch_time:.1f} 倍")

    # 批量插入应该更快
    assert batch_time < single_time, "批量插入应该更快"

    connection.close()


def test_batch_update():
    """测试批量更新"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 批量更新数据
            updates = [
                (26, 'batch_user1'),
                (27, 'batch_user2'),
                (28, 'batch_user3'),
            ]

            sql = "UPDATE users SET age = %s WHERE username = %s"
            affected = cursor.executemany(sql, updates)
            connection.commit()

            print(f"批量更新 {affected} 条记录")

    finally:
        connection.close()


def test_batch_with_chunk():
    """分批处理大量数据"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db'
    )

    # 准备 1000 条数据
    total = 1000
    chunk_size = 100  # 每批 100 条

    users = [(f'chunk_{i}', f'chunk_{i}@test.com', 25) for i in range(total)]

    try:
        with connection.cursor() as cursor:
            # 分批插入
            for i in range(0, total, chunk_size):
                chunk = users[i:i + chunk_size]
                cursor.executemany(
                    "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                    chunk
                )
                connection.commit()
                print(f"已插入 {min(i + chunk_size, total)}/{total} 条")

    finally:
        connection.close()
```
```

**验收标准**：
- [ ] executemany 批量插入正确
- [ ] 性能对比测试显示批量插入更快
- [ ] 理解分批处理大量数据的方法
- [ ] 知道批量操作的适用场景

---

---

#### 练习13：数据库测试 fixture

**场景说明**：使用 pytest fixture 管理数据库测试的连接、数据准备和清理。

**具体需求**：
1. 创建 session 级别的数据库连接 fixture（整个测试会话共享）
2. 创建 function 级别的数据清理 fixture（每个测试后清理）
3. 创建测试数据准备 fixture，自动准备和清理测试数据
4. 使用 yield 实现测试后自动清理

**使用示例**：
```python
# tests/conftest.py
import pytest
import pymysql

@pytest.fixture(scope="session")
def db():
    """Session 级别数据库连接"""
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    yield conn
    conn.close()
    print("数据库连接已关闭")


@pytest.fixture
def clean_users(db):
    """清理用户表 - 每个测试后执行"""
    yield
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM users")
        db.commit()
    print("用户表已清理")


@pytest.fixture
def clean_orders(db):
    """清理订单表 - 每个测试后执行"""
    yield
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM orders")
        db.commit()
    print("订单表已清理")


@pytest.fixture
def test_user(db, clean_users):
    """准备单个测试用户"""
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
            ('test_user', 'test@example.com', 25)
        )
        db.commit()
        user_id = cursor.lastrowid

    yield {"id": user_id, "username": "test_user", "email": "test@example.com"}

    # fixture 清理（虽然 clean_users 会清理，但这里演示如何单独清理）
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()


@pytest.fixture
def test_users(db, clean_users):
    """准备多个测试用户"""
    users = [
        ('user1', 'user1@test.com', 20),
        ('user2', 'user2@test.com', 25),
        ('user3', 'user3@test.com', 30),
    ]
    with db.cursor() as cursor:
        cursor.executemany(
            "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
            users
        )
        db.commit()
    yield users


@pytest.fixture
def test_order(db, test_user, clean_orders):
    """准备测试订单"""
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO orders (user_id, amount, status) VALUES (%s, %s, %s)",
            (test_user['id'], 100.00, 'pending')
        )
        db.commit()
        order_id = cursor.lastrowid

    yield {"id": order_id, "user_id": test_user['id'], "amount": 100.00}


# tests/test_with_fixtures.py
def test_with_single_user(db, test_user):
    """使用单个测试用户"""
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (test_user['id'],)
        )
        user = cursor.fetchone()

    assert user is not None
    assert user['username'] == 'test_user'


def test_with_multiple_users(db, test_users):
    """使用多个测试用户"""
    with db.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()

    assert result['count'] == len(test_users)


def test_user_with_order(db, test_order):
    """使用带订单的测试用户"""
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM orders WHERE id = %s",
            (test_order['id'],)
        )
        order = cursor.fetchone()

    assert order is not None
    assert order['amount'] == 100.00
```
```

**验收标准**：
- [ ] session 级别 fixture 正确共享连接
- [ ] function 级别 fixture 正确清理数据
- [ ] 测试数据 fixture 正确准备和清理
- [ ] 理解 fixture 的作用域（scope）

---

---

#### 练习14：API + 数据库验证测试

**场景说明**：在接口测试中，不仅要验证 API 响应，还要验证数据库中的数据是否正确。

**具体需求**：
1. 调用 API 创建用户，验证数据库中的数据
2. 调用 API 更新用户，验证数据库中的更新
3. 调用 API 删除用户，验证数据库中的删除
4. 验证 API 响应和数据库数据的一致性

**使用示例**：
```python
# tests/test_api_db.py
import pytest
import requests

class TestUserAPIDB:
    """API + 数据库集成测试"""

    def test_create_user_db_verify(self, db, clean_users):
        """创建用户 - 数据库验证"""
        # 1. 调用 API 创建用户
        response = requests.post(
            "http://localhost:8000/api/users",
            json={
                "username": "api_user",
                "email": "api@test.com",
                "age": 28
            }
        )

        # 2. 验证 API 响应
        assert response.status_code == 201
        user_id = response.json()["id"]

        # 3. 验证数据库
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (user_id,)
            )
            user = cursor.fetchone()

        assert user is not None, "数据库中应该有该用户"
        assert user["username"] == "api_user"
        assert user["email"] == "api@test.com"
        assert user["age"] == 28

    def test_update_user_db_verify(self, db, test_user):
        """更新用户 - 数据库验证"""
        # 1. 调用 API 更新用户
        response = requests.put(
            f"http://localhost:8000/api/users/{test_user['id']}",
            json={"age": 30}
        )

        # 2. 验证 API 响应
        assert response.status_code == 200

        # 3. 验证数据库
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT age FROM users WHERE id = %s",
                (test_user['id'],)
            )
            user = cursor.fetchone()

        assert user["age"] == 30, "年龄应该更新为30"

    def test_delete_user_db_verify(self, db, test_user):
        """删除用户 - 数据库验证"""
        # 1. 调用 API 删除用户
        response = requests.delete(
            f"http://localhost:8000/api/users/{test_user['id']}"
        )

        # 2. 验证 API 响应
        assert response.status_code == 200

        # 3. 验证数据库（用户应该不存在）
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (test_user['id'],)
            )
            user = cursor.fetchone()

        assert user is None, "用户应该被删除"

    def test_create_order_verify_user_balance(self, db, test_user):
        """创建订单 - 验证用户余额变化"""
        # 1. 查询用户当前余额
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT balance FROM users WHERE id = %s",
                (test_user['id'],)
            )
            balance_before = cursor.fetchone()["balance"]

        # 2. 创建订单
        order_amount = 100.00
        response = requests.post(
            "http://localhost:8000/api/orders",
            json={
                "user_id": test_user['id'],
                "amount": order_amount
            }
        )
        assert response.status_code == 201

        # 3. 验证余额扣除
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT balance FROM users WHERE id = %s",
                (test_user['id'],)
            )
            balance_after = cursor.fetchone()["balance"]

        assert balance_after == balance_before - order_amount
```
```

**验收标准**：
- [ ] API 响应验证正确
- [ ] 数据库数据验证正确
- [ ] 理解 API 测试和数据库验证的结合
- [ ] 测试数据正确清理

---

---

#### 练习15：数据驱动数据库测试

**场景说明**：使用数据驱动方式执行数据库测试，提高测试覆盖率。

**具体需求**：
1. 从 CSV 文件读取测试数据
2. 使用 `@pytest.mark.parametrize` 参数化执行测试
3. 验证不同场景下的数据插入结果
4. 处理预期失败的情况

**使用示例**：
```python
# tests/test_data_driven_db.py
import pytest
import csv
import pymysql

def load_user_data():
    """从 CSV 加载用户数据"""
    with open('tests/data/users.csv') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


# tests/data/users.csv 内容示例：
# username,email,age,expected
# user1,user1@test.com,20,success
# user2,user2@test.com,25,success
# ,empty@test.com,30,fail
# user3,,35,fail


@pytest.mark.parametrize("data", load_user_data())
def test_create_user_data_driven(db, clean_users, data):
    """数据驱动测试 - 创建用户"""
    username = data["username"]
    email = data["email"]
    age = int(data["age"])
    expected = data["expected"]

    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                (username, email, age)
            )
            db.commit()

            if expected == "success":
                # 验证插入成功
                cursor.execute(
                    "SELECT * FROM users WHERE username = %s",
                    (username,)
                )
                user = cursor.fetchone()
                assert user is not None, "数据应该插入成功"
                assert user["email"] == email
            else:
                # 预期失败但成功了
                pytest.fail(f"预期失败但成功了: {data}")

    except (pymysql.err.IntegrityError, pymysql.err.InternalError) as e:
        # 预期失败的情况
        if expected == "fail":
            print(f"预期失败: {e}")
        else:
            raise


# 使用 pytest 参数化直接定义数据
@pytest.mark.parametrize("username,email,age,expected", [
    ("valid_user", "valid@test.com", 25, "success"),
    ("", "no_name@test.com", 30, "fail"),  # 用户名为空
    ("no_email", "", 25, "fail"),  # 邮箱为空
    ("negative_age", "neg@test.com", -1, "fail"),  # 负数年龄
])
def test_create_user_inline_params(db, clean_users, username, email, age, expected):
    """内联参数化测试"""
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                (username, email, age)
            )
            db.commit()

            if expected == "success":
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                assert cursor.fetchone() is not None

    except (pymysql.err.IntegrityError, pymysql.err.InternalError):
        if expected == "success":
            pytest.fail("预期成功但失败了")
```
```

**验收标准**：
- [ ] 能从外部文件加载测试数据
- [ ] 参数化测试正确执行
- [ ] 能正确处理预期失败的情况
- [ ] 理解数据驱动测试的优势

---

---

#### 练习16：复杂查询练习

**场景说明**：掌握复杂 SQL 查询技巧，用于数据分析和测试数据验证。

**具体需求**：
1. 实现复杂的多表连接查询
2. 使用窗口函数（ROW_NUMBER, RANK）
3. 使用公用表表达式（CTE）
4. 使用 CASE WHEN 进行条件分组

**使用示例**：
```sql
-- 1. 查询每个用户的订单统计
SELECT
    u.id,
    u.username,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.amount), 0) as total_amount,
    COALESCE(AVG(o.amount), 0) as avg_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username
ORDER BY total_amount DESC;

-- 2. 查询每个用户的最近订单（使用子查询）
SELECT u.username, o.amount, o.created_at
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at = (
    SELECT MAX(created_at) FROM orders WHERE user_id = u.id
);

-- 3. 使用 CTE 查询消费排名
WITH user_spending AS (
    SELECT user_id, SUM(amount) as total
    FROM orders
    GROUP BY user_id
)
SELECT u.username, us.total,
       RANK() OVER (ORDER BY us.total DESC) as rank
FROM user_spending us
JOIN users u ON us.user_id = u.id;

-- 4. 使用 ROW_NUMBER 窗口函数
SELECT
    username,
    amount,
    created_at,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount DESC) as rank_by_amount
FROM orders;

-- 5. 分组统计：按年龄段统计用户消费情况
SELECT
    CASE
        WHEN age < 20 THEN '0-19'
        WHEN age < 30 THEN '20-29'
        WHEN age < 40 THEN '30-39'
        ELSE '40+'
    END as age_group,
    COUNT(DISTINCT u.id) as user_count,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.amount), 0) as total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY
    CASE
        WHEN age < 20 THEN '0-19'
        WHEN age < 30 THEN '20-29'
        WHEN age < 40 THEN '30-39'
        ELSE '40+'
    END
ORDER BY age_group;

-- 6. 查询连续下单的用户（同一天有多个订单）
SELECT user_id, DATE(created_at) as order_date, COUNT(*) as order_count
FROM orders
GROUP BY user_id, DATE(created_at)
HAVING COUNT(*) > 1;

-- 7. 使用 EXISTS 查询高消费用户
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id
    GROUP BY o.user_id
    HAVING SUM(o.amount) > 500
);
```

**验收标准**：
- [ ] 多表连接查询结果正确
- [ ] 窗口函数使用正确
- [ ] CTE 语法正确
- [ ] CASE WHEN 条件分组正确

---

### 综合练习（17-20）

---

#### 练习17：完整数据库测试类

**场景说明**：实现一个企业级的数据库管理类，包含连接管理、事务处理和错误处理。

**具体需求**：
1. `DatabaseManager` 类包含完整的 CRUD 操作
2. 使用上下文管理器管理连接
3. 支持事务操作
4. 包含错误处理和日志记录

**使用示例**：
```python
# utils/database_manager.py
import pymysql
from contextlib import contextmanager
from typing import List, Dict, Optional, Any

class DatabaseManager:
    """数据库管理器"""

    def __init__(self, host: str, user: str, password: str,
                 database: str, port: int = 3306):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self._connection = None

    def get_connection(self):
        """获取连接"""
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(**self.config)
        return self._connection

    def close(self):
        """关闭连接"""
        if self._connection and self._connection.open:
            self._connection.close()
            self._connection = None

    @contextmanager
    def connection(self):
        """上下文管理器"""
        conn = self.get_connection()
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            # 不在这里关闭连接，允许复用
            pass

    def query(self, sql: str, params: tuple = None) -> List[Dict]:
        """查询数据"""
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()

    def query_one(self, sql: str, params: tuple = None) -> Optional[Dict]:
        """查询单条"""
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()

    def execute(self, sql: str, params: tuple = None) -> int:
        """执行 SQL"""
        with self.connection() as conn:
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, params)
                conn.commit()
                return affected

    def insert(self, table: str, data: Dict) -> int:
        """插入数据"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, tuple(data.values()))
                conn.commit()
                return cursor.lastrowid

    def insert_batch(self, table: str, data_list: List[Dict]) -> int:
        """批量插入"""
        if not data_list:
            return 0

        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['%s'] * len(data_list[0]))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        values = [tuple(d.values()) for d in data_list]

        with self.connection() as conn:
            with conn.cursor() as cursor:
                affected = cursor.executemany(sql, values)
                conn.commit()
                return affected

    def update(self, table: str, data: Dict, where: Dict) -> int:
        """更新数据"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        with self.connection() as conn:
            with conn.cursor() as cursor:
                affected = cursor.execute(
                    sql,
                    tuple(data.values()) + tuple(where.values())
                )
                conn.commit()
                return affected

    def delete(self, table: str, where: Dict) -> int:
        """删除数据"""
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        with self.connection() as conn:
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, tuple(where.values()))
                conn.commit()
                return affected

    def transaction(self, operations: List[tuple]) -> bool:
        """执行事务"""
        with self.connection() as conn:
            try:
                with conn.cursor() as cursor:
                    for sql, params in operations:
                        cursor.execute(sql, params)
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 测试用例
import pytest

class TestDatabaseManager:

    @pytest.fixture
    def db(self):
        return DatabaseManager('localhost', 'root', 'password', 'test_db')

    def test_query(self, db):
        users = db.query("SELECT * FROM users LIMIT 10")
        assert isinstance(users, list)

    def test_insert(self, db):
        user_id = db.insert('users', {
            'username': 'test_user',
            'email': 'test@test.com',
            'age': 25
        })
        assert user_id > 0

    def test_update(self, db):
        affected = db.update('users', {'age': 26}, {'username': 'test_user'})
        assert affected >= 0

    def test_delete(self, db):
        affected = db.delete('users', {'username': 'test_user'})
        assert affected >= 0

    def test_transaction(self, db):
        operations = [
            ("UPDATE accounts SET balance = balance - 100 WHERE id = 1", None),
            ("UPDATE accounts SET balance = balance + 100 WHERE id = 2", None),
        ]
        result = db.transaction(operations)
        assert result is True
```
```

**验收标准**：
- [ ] DatabaseManager 类功能完整
- [ ] CRUD 操作正确
- [ ] 事务处理正确
- [ ] 错误处理完善

---

#### 练习18：数据库测试框架

**场景说明**：在大型测试项目中，需要设计一套可复用的测试框架，包含数据工厂、验证工具和快照比较功能，提高测试代码的可维护性和可读性。

**具体需求**：
1. 创建 `DataFactory` 测试数据工厂类：
   - `create_user(**kwargs)` 方法创建用户数据，支持自定义覆盖默认值
   - `create_order(user_id, **kwargs)` 方法创建订单数据
   - 所有方法返回字典格式的数据
2. 创建 `DataValidator` 数据验证工具类：
   - `user_exists(username)` 验证用户是否存在
   - `verify_user_data(user_id, expected)` 验证用户数据是否匹配预期
   - `count_orders(user_id)` 统计用户订单数量
3. 实现测试框架的完整测试用例
4. 支持数据快照比较功能

**使用示例**：
```python
# tests/test_db_framework.py
import pytest
import json
from datetime import datetime

class DataFactory:
    """测试数据工厂"""

    @staticmethod
    def create_user(**kwargs):
        """创建用户数据"""
        default = {
            'username': f'user_{datetime.now().timestamp()}',
            'email': f'user_{datetime.now().timestamp()}@test.com',
            'age': 25,
            'status': 'active'
        }
        default.update(kwargs)
        return default

    @staticmethod
    def create_order(user_id, **kwargs):
        """创建订单数据"""
        default = {
            'user_id': user_id,
            'amount': 100.00,
            'status': 'pending'
        }
        default.update(kwargs)
        return default

class DataValidator:
    """数据验证工具"""

    def __init__(self, db):
        self.db = db

    def user_exists(self, username):
        """验证用户存在"""
        result = self.db.query(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )
        return len(result) > 0

    def verify_user_data(self, user_id, expected):
        """验证用户数据"""
        result = self.db.query(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )
        if not result:
            return False
        actual = result[0]
        for key, value in expected.items():
            if actual.get(key) != value:
                return False
        return True

    def count_orders(self, user_id):
        """统计用户订单数"""
        result = self.db.query(
            "SELECT COUNT(*) as count FROM orders WHERE user_id = %s",
            (user_id,)
        )
        return result[0]['count']

    def snapshot_compare(self, table, where, snapshot_file):
        """数据快照比较"""
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        current_data = self.db.query(sql, tuple(where.values()))

        # 加载快照
        with open(snapshot_file, 'r') as f:
            snapshot = json.load(f)

        return current_data == snapshot

# 测试用例
class TestDataFramework:

    @pytest.fixture
    def factory(self):
        return DataFactory()

    @pytest.fixture
    def validator(self, db):
        return DataValidator(db)

    def test_create_user_with_factory(self, db, factory, validator, clean_users):
        """使用工厂创建测试数据"""
        user_data = factory.create_user(username='factory_user')
        user_id = db.insert('users', user_data)

        assert validator.user_exists('factory_user')
        assert validator.verify_user_data(user_id, {'username': 'factory_user'})

    def test_create_order_with_factory(self, db, factory, validator, clean_users):
        """创建订单测试"""
        user_data = factory.create_user()
        user_id = db.insert('users', user_data)

        order_data = factory.create_order(user_id, amount=200.00)
        db.insert('orders', order_data)

        assert validator.count_orders(user_id) == 1

    def test_factory_default_values(self, factory):
        """测试工厂默认值"""
        user = factory.create_user()
        assert 'username' in user
        assert 'email' in user
        assert user['age'] == 25
        assert user['status'] == 'active'

    def test_factory_custom_values(self, factory):
        """测试工厂自定义值"""
        user = factory.create_user(username='custom_user', age=30)
        assert user['username'] == 'custom_user'
        assert user['age'] == 30
```

**验收标准**：
- [ ] DataFactory 类能正确生成默认用户和订单数据
- [ ] DataFactory 支持通过 kwargs 覆盖默认值
- [ ] DataValidator 能正确验证用户是否存在
- [ ] DataValidator 能正确验证用户数据
- [ ] DataValidator 能正确统计订单数量
- [ ] 测试用例全部通过

#### 练习19：数据库性能测试

**场景说明**：在测试大型系统时，需要验证数据库操作的性能指标，包括批量插入、索引查询和并发查询的性能，确保系统在高负载下仍能正常工作。

**具体需求**：
1. 测试批量插入性能：
   - 插入 1000 条记录
   - 记录执行时间
   - 验证插入时间在合理范围内（如 5 秒内）
2. 测试索引查询性能：
   - 比较有索引和无索引查询的耗时差异
   - 使用 `EXPLAIN` 分析查询执行计划
3. 测试并发查询性能：
   - 使用 `ThreadPoolExecutor` 模拟并发请求
   - 验证并发场景下数据库的稳定性

**使用示例**：
```python
# tests/test_db_performance.py
import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor

class TestDatabasePerformance:

    def test_bulk_insert_performance(self, db):
        """测试批量插入性能"""
        n = 1000
        users = [
            (f'perf_user_{i}', f'perf_{i}@test.com', 25)
            for i in range(n)
        ]

        start = time.time()
        with db.connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                    users
                )
                conn.commit()
        elapsed = time.time() - start

        print(f"批量插入 {n} 条记录耗时: {elapsed:.3f}s")
        assert elapsed < 5.0  # 应在 5 秒内完成

    def test_index_query_performance(self, db):
        """测试索引查询性能"""
        # 无索引查询
        start = time.time()
        db.query("SELECT * FROM users WHERE age = 25")
        no_index_time = time.time() - start

        # 有索引查询（假设已创建索引）
        start = time.time()
        db.query("SELECT * FROM users WHERE username = 'perf_user_500'")
        index_time = time.time() - start

        print(f"无索引查询: {no_index_time:.4f}s")
        print(f"有索引查询: {index_time:.4f}s")

    def test_concurrent_queries(self, db):
        """测试并发查询"""
        def query_task(i):
            return db.query(f"SELECT * FROM users LIMIT 10")

        concurrent_count = 10
        start = time.time()

        with ThreadPoolExecutor(max_workers=concurrent_count) as executor:
            results = list(executor.map(query_task, range(concurrent_count)))

        elapsed = time.time() - start

        print(f"并发 {concurrent_count} 个查询耗时: {elapsed:.3f}s")
        assert len(results) == concurrent_count

    def test_single_vs_batch_insert(self, db):
        """单条插入 vs 批量插入性能对比"""
        n = 100

        # 单条插入
        start = time.time()
        for i in range(n):
            db.execute(
                "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                (f'single_{i}', f'single_{i}@test.com', 25)
            )
        single_time = time.time() - start

        # 批量插入
        start = time.time()
        users = [(f'batch_{i}', f'batch_{i}@test.com', 25) for i in range(n)]
        with db.connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                    users
                )
                conn.commit()
        batch_time = time.time() - start

        print(f"单条插入 {n} 条: {single_time:.3f}s")
        print(f"批量插入 {n} 条: {batch_time:.3f}s")
        print(f"批量插入快 {single_time/batch_time:.1f} 倍")
        assert batch_time < single_time
```

**验收标准**：
- [ ] 批量插入 1000 条记录在 5 秒内完成
- [ ] 索引查询比无索引查询更快
- [ ] 并发查询能正确执行并返回结果
- [ ] 理解批量操作的性能优势
- [ ] 能够分析查询性能瓶颈

#### 练习20：综合数据库测试项目

**场景说明**：整合本周所学知识，完成一个企业级数据库测试项目，包含连接池管理、数据工厂、验证工具、性能测试和 API 集成测试，形成完整的测试解决方案。

**具体需求**：
1. 项目结构设计：
   - `config/` - 配置文件目录
   - `db/` - 数据库连接和管理模块
   - `factories/` - 测试数据工厂
   - `validators/` - 数据验证工具
   - `tests/` - 测试用例
   - `scripts/` - 数据库初始化脚本
2. 实现核心功能：
   - 数据库连接池管理
   - 测试数据工厂（用户、订单）
   - 数据验证工具
   - 性能测试用例
   - API + 数据库集成测试
3. 编写完整的集成测试用例

**使用示例**：
```python
# 项目结构：
# db_test_project/
# ├── config/
# │   └── database.yaml
# ├── db/
# │   ├── __init__.py
# │   ├── connection.py
# │   ├── manager.py
# │   └── pool.py
# ├── factories/
# │   ├── __init__.py
# │   ├── user_factory.py
# │   └── order_factory.py
# ├── validators/
# │   ├── __init__.py
# │   └── data_validator.py
# ├── tests/
# │   ├── conftest.py
# │   ├── test_user_crud.py
# │   ├── test_order_flow.py
# │   ├── test_performance.py
# │   └── test_api_integration.py
# ├── scripts/
# │   ├── init_db.sql
# │   └── seed_data.sql
# └── requirements.txt

# tests/conftest.py
import pytest
from db.manager import DatabaseManager
from factories.user_factory import UserFactory
from factories.order_factory import OrderFactory
from validators.data_validator import DataValidator

@pytest.fixture(scope="session")
def db():
    """Session 级别数据库连接"""
    manager = DatabaseManager.from_config("config/database.yaml")
    yield manager
    manager.close()

@pytest.fixture
def user_factory():
    return UserFactory()

@pytest.fixture
def order_factory():
    return OrderFactory()

@pytest.fixture
def validator(db):
    return DataValidator(db)

@pytest.fixture
def clean_db(db):
    """清理测试数据"""
    db.execute("DELETE FROM orders")
    db.execute("DELETE FROM users")
    yield

# 完整的集成测试示例
class TestUserOrderIntegration:

    def test_complete_user_order_flow(self, db, user_factory, order_factory, validator, clean_db):
        """完整的用户订单流程测试"""

        # 1. 创建用户
        user_data = user_factory.create(username='integration_user')
        user_id = db.insert('users', user_data)
        assert validator.user_exists('integration_user')

        # 2. 创建订单
        order_data = order_factory.create(user_id, amount=500.00)
        order_id = db.insert('orders', order_data)
        assert validator.count_orders(user_id) == 1

        # 3. 更新订单状态
        db.execute(
            "UPDATE orders SET status = 'completed' WHERE id = %s",
            (order_id,)
        )

        # 4. 验证最终状态
        orders = db.query(
            "SELECT * FROM orders WHERE user_id = %s AND status = 'completed'",
            (user_id,)
        )
        assert len(orders) == 1
        assert orders[0]['amount'] == 500.00

    def test_user_order_with_transaction(self, db, user_factory, order_factory, clean_db):
        """事务测试 - 用户创建和订单创建"""

        user_data = user_factory.create(username='trans_user')

        try:
            # 开始事务
            db.connection().begin()

            # 创建用户
            user_id = db.insert('users', user_data)

            # 创建多个订单
            for amount in [100, 200, 300]:
                order_data = order_factory.create(user_id, amount=amount)
                db.insert('orders', order_data)

            # 提交事务
            db.connection().commit()

            # 验证
            assert db.query_one(
                "SELECT COUNT(*) as count FROM orders WHERE user_id = %s",
                (user_id,)
            )['count'] == 3

        except Exception as e:
            db.connection().rollback()
            raise e

    def test_data_integrity(self, db, user_factory, order_factory, validator, clean_db):
        """数据完整性测试"""
        # 创建用户
        user_data = user_factory.create(username='integrity_user', age=30)
        user_id = db.insert('users', user_data)

        # 验证数据完整性
        assert validator.verify_user_data(user_id, {
            'username': 'integrity_user',
            'age': 30
        })

        # 测试外键约束
        with pytest.raises(Exception):
            # 尝试插入不存在的用户ID的订单
            db.insert('orders', {
                'user_id': 99999,
                'amount': 100.00
            })
```

**验收标准**：
- [ ] 项目结构清晰，模块划分合理
- [ ] 数据库连接池正常工作
- [ ] 测试数据工厂能正确生成数据
- [ ] 数据验证工具功能完整
- [ ] 集成测试用例全部通过
- [ ] 事务处理正确

---

## 五、检验标准

### 自测题

---

#### 题目1：数据库连接工具类设计

**场景描述**：设计一个可复用的数据库连接工具类，支持连接池、事务和上下文管理器，用于企业级测试项目中的数据库操作管理。

**详细需求**：
1. `MySQLPool` 类：
   - `__init__(config, pool_size=5)` 接收数据库配置字典和连接池大小
   - `get_connection()` 从连接池获取连接
   - `close_all()` 关闭所有连接
   - `_init_pool()` 初始化连接池（私有方法）
   - `_create_connection()` 创建新连接（私有方法）
   - `_return_connection(conn)` 归还连接到连接池（私有方法）
2. 支持使用 `with` 语句的上下文管理
3. 支持事务的自动提交和回滚
4. 实现查询方法 `query_one()`, `query_all()`
5. 实现执行方法 `execute()`, `insert()`, `update()`, `delete()`
6. 实现连接包装器 `_ConnectionWrapper` 类

**测试用例**：
```python
# 测试连接池
pool = MySQLPool({
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'test_db'
})

# 获取连接
with pool.get_connection() as conn:
    result = conn.query_one("SELECT * FROM users LIMIT 1")
    assert result is not None

# 插入数据
user_id = pool.insert('users', {
    'username': 'pool_test',
    'email': 'pool@test.com'
})
assert user_id > 0

# 更新数据
affected = pool.update('users', {'age': 30}, {'id': user_id})
assert affected > 0

# 查询验证
user = pool.query_one("SELECT * FROM users WHERE id = %s", (user_id,))
assert user['age'] == 30

# 删除数据
affected = pool.delete('users', {'id': user_id})
assert affected > 0

# 关闭连接池
pool.close_all()
```

**完整答案**：
```python
import pymysql
from typing import List, Dict, Optional, Any
from contextlib import contextmanager
import threading

class MySQLPool:
    """MySQL 连接池管理类"""

    def __init__(self, config: Dict[str, Any], pool_size: int = 5):
        self.config = config
        self.pool_size = pool_size
        self._pool: List = []
        self._lock = threading.Lock()
        self._init_pool()

    def _init_pool(self):
        """初始化连接池"""
        for _ in range(self.pool_size):
            conn = self._create_connection()
            self._pool.append(conn)

    def _create_connection(self):
        """创建新连接"""
        config = self.config.copy()
        config['cursorclass'] = pymysql.cursors.DictCursor
        return pymysql.connect(**config)

    def get_connection(self):
        """获取连接"""
        with self._lock:
            if self._pool:
                conn = self._pool.pop()
            else:
                conn = self._create_connection()
        return _ConnectionWrapper(conn, self)

    def _return_connection(self, conn):
        """归还连接"""
        with self._lock:
            if len(self._pool) < self.pool_size:
                self._pool.append(conn)
            else:
                conn.close()

    def close_all(self):
        """关闭所有连接"""
        with self._lock:
            for conn in self._pool:
                conn.close()
            self._pool.clear()

    def query_one(self, sql: str, params: tuple = None) -> Optional[Dict]:
        """查询单条"""
        with self.get_connection() as conn:
            return conn.query_one(sql, params)

    def query_all(self, sql: str, params: tuple = None) -> List[Dict]:
        """查询多条"""
        with self.get_connection() as conn:
            return conn.query_all(sql, params)

    def execute(self, sql: str, params: tuple = None) -> int:
        """执行 SQL"""
        with self.get_connection() as conn:
            return conn.execute(sql, params)

    def insert(self, table: str, data: Dict) -> int:
        """插入数据"""
        with self.get_connection() as conn:
            return conn.insert(table, data)

    def update(self, table: str, data: Dict, where: Dict) -> int:
        """更新数据"""
        with self.get_connection() as conn:
            return conn.update(table, data, where)

    def delete(self, table: str, where: Dict) -> int:
        """删除数据"""
        with self.get_connection() as conn:
            return conn.delete(table, where)


class _ConnectionWrapper:
    """连接包装器，支持上下文管理"""

    def __init__(self, conn, pool):
        self._conn = conn
        self._pool = pool

    def query_one(self, sql: str, params: tuple = None) -> Optional[Dict]:
        with self._conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def query_all(self, sql: str, params: tuple = None) -> List[Dict]:
        with self._conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute(self, sql: str, params: tuple = None) -> int:
        with self._conn.cursor() as cursor:
            affected = cursor.execute(sql, params)
            self._conn.commit()
            return affected

    def insert(self, table: str, data: Dict) -> int:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        with self._conn.cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            self._conn.commit()
            return cursor.lastrowid

    def update(self, table: str, data: Dict, where: Dict) -> int:
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        with self._conn.cursor() as cursor:
            affected = cursor.execute(sql, tuple(data.values()) + tuple(where.values()))
            self._conn.commit()
            return affected

    def delete(self, table: str, where: Dict) -> int:
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        with self._conn.cursor() as cursor:
            affected = cursor.execute(sql, tuple(where.values()))
            self._conn.commit()
            return affected

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._conn.rollback()
        self._pool._return_connection(self._conn)
        return False
```

**自测检查清单**：
- [ ] 连接池正确初始化，默认包含 5 个连接
- [ ] `get_connection()` 能正确获取连接，池空时创建新连接
- [ ] 连接使用后正确归还到连接池
- [ ] 事务在异常时正确回滚
- [ ] CRUD 操作正确执行并返回预期结果
- [ ] `close_all()` 能关闭所有连接
- [ ] 支持上下文管理器（`with` 语句）

---

#### 题目2：数据库测试框架设计

**场景描述**：设计一个完整的数据库测试框架，包含数据工厂、验证工具和测试基类，用于标准化测试数据创建和验证流程，提高测试代码的可维护性。

**详细需求**：
1. `DataFactory` 类：
   - `create_user(**kwargs)` 创建用户数据，返回包含默认值的字典
   - `create_order(user_id, **kwargs)` 创建订单数据
   - `create_batch(creator, count, **kwargs)` 批量创建数据
   - 所有方法支持通过 kwargs 覆盖默认值
2. `DataValidator` 类：
   - `user_exists(username)` 验证用户是否存在，返回布尔值
   - `verify_user_data(user_id, expected)` 验证用户数据是否匹配预期
   - `count_records(table, where)` 统计指定条件的记录数
3. `BaseDBTest` 类：
   - 提供 `setup()` 和 `teardown()` 方法
   - `_created_ids` 字典跟踪创建的记录
   - `track_created(table, record_id)` 跟踪创建的记录
   - `create_and_track_user(**kwargs)` 创建用户并自动跟踪
   - `teardown()` 自动清理所有跟踪的测试数据

**测试用例**：
```python
# 创建工厂和验证器
factory = DataFactory()
validator = DataValidator(db)

# 创建单个用户
user_data = factory.create_user(username='test_user')
user_id = db.insert('users', user_data)

# 验证用户存在
assert validator.user_exists('test_user')

# 验证用户数据
assert validator.verify_user_data(user_id, {'username': 'test_user'})

# 批量创建用户
users = factory.create_batch(factory.create_user, 5)
assert len(users) == 5

# 统计记录数
count = validator.count_records('users', {'status': 'active'})
print(f"活跃用户数: {count}")

# 使用 BaseDBTest
test = BaseDBTest(db)
test.setup()
user_id = test.create_and_track_user(username='auto_clean_user')
# ... 执行测试 ...
test.teardown()  # 自动清理创建的用户
```

**完整答案**：
```python
from datetime import datetime
from typing import Dict, List, Any, Callable
import time

class DataFactory:
    """测试数据工厂"""

    @staticmethod
    def create_user(**kwargs) -> Dict:
        """创建用户数据"""
        default = {
            'username': f'user_{int(time.time() * 1000)}',
            'email': f'user_{int(time.time() * 1000)}@test.com',
            'age': 25,
            'status': 'active'
        }
        default.update(kwargs)
        return default

    @staticmethod
    def create_order(user_id: int, **kwargs) -> Dict:
        """创建订单数据"""
        default = {
            'user_id': user_id,
            'amount': 100.00,
            'status': 'pending',
            'created_at': datetime.now()
        }
        default.update(kwargs)
        return default

    @staticmethod
    def create_batch(creator: Callable, count: int, **kwargs) -> List[Dict]:
        """批量创建数据"""
        return [creator(**kwargs) for _ in range(count)]


class DataValidator:
    """数据验证工具"""

    def __init__(self, db):
        self.db = db

    def user_exists(self, username: str) -> bool:
        """验证用户存在"""
        result = self.db.query_one(
            "SELECT id FROM users WHERE username = %s",
            (username,)
        )
        return result is not None

    def verify_user_data(self, user_id: int, expected: Dict) -> bool:
        """验证用户数据"""
        result = self.db.query_one(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )
        if not result:
            return False
        for key, value in expected.items():
            if result.get(key) != value:
                return False
        return True

    def count_records(self, table: str, where: Dict = None) -> int:
        """统计记录数"""
        if where:
            where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
            sql = f"SELECT COUNT(*) as count FROM {table} WHERE {where_clause}"
            result = self.db.query_one(sql, tuple(where.values()))
        else:
            sql = f"SELECT COUNT(*) as count FROM {table}"
            result = self.db.query_one(sql)
        return result['count'] if result else 0


class BaseDBTest:
    """数据库测试基类"""

    def __init__(self, db):
        self.db = db
        self.factory = DataFactory()
        self.validator = DataValidator(db)
        self._created_ids = {'users': [], 'orders': []}

    def setup(self):
        """测试前置"""
        pass

    def teardown(self):
        """测试后置 - 清理测试数据"""
        for table, ids in self._created_ids.items():
            if ids:
                placeholders = ','.join(['%s'] * len(ids))
                self.db.execute(f"DELETE FROM {table} WHERE id IN ({placeholders})", tuple(ids))

    def track_created(self, table: str, record_id: int):
        """跟踪创建的记录"""
        if table in self._created_ids:
            self._created_ids[table].append(record_id)

    def create_and_track_user(self, **kwargs) -> int:
        """创建用户并跟踪"""
        user_data = self.factory.create_user(**kwargs)
        user_id = self.db.insert('users', user_data)
        self.track_created('users', user_id)
        return user_id
```

**自测检查清单**：
- [ ] DataFactory.create_user() 正确生成包含所有默认字段的字典
- [ ] DataFactory 支持通过 kwargs 覆盖默认值
- [ ] DataFactory.create_batch() 能批量创建指定数量的数据
- [ ] DataValidator.user_exists() 正确返回用户是否存在
- [ ] DataValidator.verify_user_data() 正确比较预期和实际数据
- [ ] DataValidator.count_records() 正确统计记录数
- [ ] BaseDBTest.setup() 和 teardown() 正确工作
- [ ] BaseDBTest 能跟踪并自动清理创建的记录

---

#### 题目3：复杂 SQL 查询验证

**场景描述**：作为测试工程师，需要验证复杂 SQL 查询的正确性，包括多表连接、子查询和聚合函数，用于数据分析和测试数据验证。

**详细需求**：
1. 查询每个用户的订单统计：
   - 包含用户 ID、用户名、邮箱
   - 统计总订单数、总金额、平均金额
   - 使用 LEFT JOIN 包含没有订单的用户
   - 使用 COALESCE 处理 NULL 值
2. 查询消费金额排名前 10 的用户：
   - 只统计已完成（completed）状态的订单
   - 显示订单数和总消费金额
3. 查询每个状态下的订单数量和总金额：
   - 包含订单数、总金额、平均金额、最小金额、最大金额
4. 查询最近 7 天每天的新用户数：
   - 按日期分组统计
   - 使用日期函数筛选
5. 查询没有订单的用户：
   - 使用 LEFT JOIN + IS NULL 实现
   - 同时提供 NOT EXISTS 和 NOT IN 两种替代方案

**测试用例**：
```sql
-- 1. 用户订单统计
SELECT
    u.username,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.amount), 0) as total_amount,
    COALESCE(AVG(o.amount), 0) as avg_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username
ORDER BY total_amount DESC;

-- 2. 消费前10用户
SELECT
    u.username,
    SUM(o.amount) as total_spent
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
GROUP BY u.id, u.username
ORDER BY total_spent DESC
LIMIT 10;

-- 3. 订单状态统计
SELECT
    status,
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders
GROUP BY status;

-- 4. 最近7天新用户
SELECT
    DATE(created_at) as date,
    COUNT(*) as new_users
FROM users
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY DATE(created_at)
ORDER BY date;

-- 5. 没有订单的用户
SELECT u.username, u.email
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

**完整答案**：
```sql
-- 1. 用户订单统计（包含没有订单的用户）
SELECT
    u.id,
    u.username,
    u.email,
    COUNT(o.id) as order_count,
    COALESCE(SUM(o.amount), 0) as total_amount,
    COALESCE(AVG(o.amount), 0) as avg_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username, u.email
ORDER BY total_amount DESC;

-- 2. 消费前10用户（只统计已完成订单）
SELECT
    u.id,
    u.username,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_spent
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
GROUP BY u.id, u.username
ORDER BY total_spent DESC
LIMIT 10;

-- 3. 订单状态统计（包含各状态的订单数和金额）
SELECT
    status,
    COUNT(*) as order_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount
FROM orders
GROUP BY status
ORDER BY order_count DESC;

-- 4. 最近7天每天新用户数
SELECT
    DATE(created_at) as date,
    COUNT(*) as new_users
FROM users
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- 5. 没有订单的用户
SELECT
    u.id,
    u.username,
    u.email,
    u.created_at
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL
ORDER BY u.created_at DESC;

-- 额外：使用 NOT EXISTS 实现
SELECT u.username, u.email
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- 额外：使用子查询实现
SELECT username, email
FROM users
WHERE id NOT IN (
    SELECT DISTINCT user_id FROM orders WHERE user_id IS NOT NULL
);
```

**自测检查清单**：
- [ ] LEFT JOIN 正确包含没有订单的用户（order_count 为 0）
- [ ] COALESCE 正确处理 NULL 值（将 NULL 转为 0）
- [ ] GROUP BY 包含所有非聚合列（符合 SQL 标准）
- [ ] INNER JOIN 只返回有订单的用户
- [ ] WHERE 条件正确过滤已完成的订单
- [ ] 日期函数 DATE() 和 DATE_SUB() 使用正确
- [ ] 理解 LEFT JOIN + IS NULL、NOT EXISTS、NOT IN 三种查询无订单用户的方式及性能差异

---

## 六、本周小结
1. **SQL**：测试数据验证的核心技能
2. **索引**：性能优化的关键
3. **事务**：保证数据一致性
4. **Python 操作**：自动化测试必备

### 下周预告

第8周学习 Git 版本控制。
