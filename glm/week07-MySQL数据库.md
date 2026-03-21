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

#### 练习1：数据库和表创建

```sql
-- 要求：
-- 1. 创建数据库 test_db
-- 2. 创建用户表 users（id, username, email, age, status, created_at）
-- 3. 创建订单表 orders（id, user_id, amount, status, created_at）
-- 4. 设置主键和默认值

-- 创建数据库
CREATE DATABASE test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE test_db;

-- 创建用户表
CREATE TABLE users (
    -- 实现字段定义
);

-- 创建订单表
CREATE TABLE orders (
    -- 实现字段定义
);

-- 查看表结构
DESC users;
DESC orders;
```

#### 练习2：数据插入和查询

```sql
-- 要求：
-- 1. 向 users 表插入 5 条测试数据
-- 2. 向 orders 表插入 10 条测试数据
-- 3. 使用 SELECT 查询所有数据
-- 4. 使用 WHERE 条件查询

-- 插入用户数据
INSERT INTO users (username, email, age, status) VALUES
-- 插入 5 条数据
;

-- 插入订单数据
INSERT INTO orders (user_id, amount, status) VALUES
-- 插入 10 条数据
;

-- 查询所有用户
SELECT * FROM users;

-- 查询年龄大于 25 的用户
-- 实现查询语句

-- 查询状态为 completed 的订单
-- 实现查询语句
```

#### 练习3：条件查询和排序

```sql
-- 要求：
-- 1. 使用 BETWEEN 查询年龄范围
-- 2. 使用 IN 查询多个状态
-- 3. 使用 LIKE 模糊查询
-- 4. 使用 ORDER BY 排序

-- 查询年龄在 20-30 之间的用户
SELECT * FROM users WHERE age BETWEEN 20 AND 30;

-- 查询状态为 active 或 pending 的用户
-- 实现查询

-- 查询邮箱包含 @example.com 的用户
-- 实现查询

-- 按年龄降序排列用户
-- 实现查询

-- 按金额升序排列订单
-- 实现查询
```

#### 练习4：聚合函数和分组

```sql
-- 要求：
-- 1. 使用 COUNT 统计记录数
-- 2. 使用 AVG 计算平均值
-- 3. 使用 SUM 计算总和
-- 4. 使用 GROUP BY 分组统计

-- 统计用户总数
SELECT COUNT(*) FROM users;

-- 计算用户平均年龄
-- 实现查询

-- 计算订单总金额
-- 实现查询

-- 统计每个状态的用户数量
SELECT status, COUNT(*) as count FROM users GROUP BY status;

-- 计算每个用户的订单总金额
-- 实现查询

-- 查询订单数量超过 2 的用户
-- 实现 HAVING 查询
```

#### 练习5：多表连接查询

```sql
-- 要求：
-- 1. 使用 INNER JOIN 内连接
-- 2. 使用 LEFT JOIN 左连接
-- 3. 使用 RIGHT JOIN 右连接
-- 4. 查询用户及其订单信息

-- 内连接：查询有订单的用户
SELECT u.username, o.amount, o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 左连接：查询所有用户及其订单（包括没有订单的用户）
-- 实现查询

-- 查询每个用户的订单数量
-- 实现查询

-- 查询订单金额超过 100 的用户信息
-- 实现查询
```

#### 练习6：Python 基础连接

```python
# tests/test_db_basic.py
# 要求：
# 1. 使用 pymysql 连接数据库
# 2. 执行简单查询
# 3. 获取查询结果
# 4. 关闭连接

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
            assert len(results) > 0
            for row in results:
                print(row)

    finally:
        connection.close()

def test_insert_and_query():
    """插入数据并查询"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='test_db'
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
            assert result is not None

    finally:
        connection.close()
```

#### 练习7：Python CRUD 操作

```python
# tests/test_db_crud.py
# 要求：
# 1. 实现插入操作
# 2. 实现查询操作
# 3. 实现更新操作
# 4. 实现删除操作

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
        assert cursor.lastrowid > 0

def test_read(db_connection):
    """测试查询数据"""
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", ('new_user',))
        result = cursor.fetchone()
        assert result is not None
        assert result['username'] == 'new_user'

def test_update(db_connection):
    """测试更新数据"""
    with db_connection.cursor() as cursor:
        sql = "UPDATE users SET age = %s WHERE username = %s"
        cursor.execute(sql, (35, 'new_user'))
        db_connection.commit()
        assert cursor.rowcount > 0

def test_delete(db_connection):
    """测试删除数据"""
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE username = %s", ('new_user',))
        db_connection.commit()
        assert cursor.rowcount > 0
```

#### 练习8：子查询基础

```sql
-- 要求：
-- 1. 在 WHERE 中使用子查询
-- 2. 在 FROM 中使用子查询
-- 3. 使用 EXISTS 子查询

-- 查询有订单的用户
SELECT * FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders);

-- 查询年龄大于平均年龄的用户
SELECT * FROM users
WHERE age > (SELECT AVG(age) FROM users);

-- 查询订单金额最高的用户
-- 实现子查询

-- 使用 EXISTS 查询有订单的用户
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- 统计每个用户的订单数（使用子查询）
-- 实现查询
```

### 进阶练习（9-16）

#### 练习9：数据库工具类

```python
# utils/db_helper.py
# 要求：
# 1. 封装数据库连接和操作
# 2. 支持 insert/update/delete/query 方法
# 3. 支持事务操作
# 4. 使用上下文管理器

import pymysql
from typing import List, Dict, Optional

class MySQLHelper:
    """MySQL 操作工具类"""

    def __init__(self, host, user, password, database, port=3306):
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
        self.connection = pymysql.connect(**self.config)
        return self

    def close(self):
        if self.connection:
            self.connection.close()

    def query_one(self, sql, params=None) -> Optional[Dict]:
        """查询单条"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def query_all(self, sql, params=None) -> List[Dict]:
        """查询多条"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def insert(self, table, data) -> int:
        """插入数据"""
        # 实现插入逻辑
        pass

    def update(self, table, data, where) -> int:
        """更新数据"""
        # 实现更新逻辑
        pass

    def delete(self, table, where) -> int:
        """删除数据"""
        # 实现删除逻辑
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.connection.rollback()
        self.close()
```

#### 练习10：索引创建和分析

```sql
-- 要求：
-- 1. 创建普通索引
-- 2. 创建唯一索引
-- 3. 创建组合索引
-- 4. 使用 EXPLAIN 分析查询

-- 为 username 创建索引
CREATE INDEX idx_username ON users(username);

-- 为 email 创建唯一索引
CREATE UNIQUE INDEX idx_email ON users(email);

-- 创建组合索引（status, age）
CREATE INDEX idx_status_age ON users(status, age);

-- 查看索引
SHOW INDEX FROM users;

-- 分析查询（使用索引）
EXPLAIN SELECT * FROM users WHERE username = '张三';

-- 分析查询（不使用索引）
EXPLAIN SELECT * FROM users WHERE age > 25;

-- 分析查询（组合索引最左原则）
EXPLAIN SELECT * FROM users WHERE status = 'active';
EXPLAIN SELECT * FROM users WHERE status = 'active' AND age > 20;
EXPLAIN SELECT * FROM users WHERE age > 20;  -- 不满足最左原则
```

#### 练习11：事务处理

```python
# tests/test_transaction.py
# 要求：
# 1. 实现银行转账事务
# 2. 测试事务回滚
# 3. 测试事务提交

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
    """测试事务提交"""
    try:
        cursor = db.cursor()

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
        balance_a = cursor.fetchone()[0]
        cursor.execute("SELECT balance FROM accounts WHERE id = 2")
        balance_b = cursor.fetchone()[0]

        print(f"A 账户余额: {balance_a}, B 账户余额: {balance_b}")

    except Exception as e:
        db.rollback()
        raise e

def test_transaction_rollback(db):
    """测试事务回滚"""
    cursor = db.cursor()

    # 记录原始余额
    cursor.execute("SELECT balance FROM accounts WHERE id = 1")
    original_balance = cursor.fetchone()[0]

    try:
        db.begin()
        cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        # 模拟错误
        raise Exception("模拟错误")
    except:
        db.rollback()

    # 验证余额未变
    cursor.execute("SELECT balance FROM accounts WHERE id = 1")
    current_balance = cursor.fetchone()[0]
    assert current_balance == original_balance
```

#### 练习12：批量操作

```python
# tests/test_batch_operations.py
# 要求：
# 1. 实现批量插入
# 2. 实现批量更新
# 3. 比较单条和批量操作的性能

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
                ('user1', 'user1@example.com', 20),
                ('user2', 'user2@example.com', 25),
                ('user3', 'user3@example.com', 30),
            ]

            # 批量插入
            sql = "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)"
            affected = cursor.executemany(sql, users)
            connection.commit()

            print(f"批量插入 {affected} 条记录")

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

    connection.close()
```

#### 练习13：数据库测试 fixture

```python
# tests/conftest.py
# 要求：
# 1. 创建 session 级别的数据库连接 fixture
# 2. 创建 function 级别的数据清理 fixture
# 3. 创建测试数据准备 fixture

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

@pytest.fixture
def clean_users(db):
    """清理用户表"""
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM users")
        db.commit()
    yield

@pytest.fixture
def test_user(db, clean_users):
    """准备测试用户"""
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
            ('test_user', 'test@example.com', 25)
        )
        db.commit()
        user_id = cursor.lastrowid

    yield {"id": user_id, "username": "test_user"}

    # 清理
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
    yield
```

#### 练习14：API + 数据库验证测试

```python
# tests/test_api_db.py
# 要求：
# 1. 调用 API 创建用户
# 2. 验证数据库中的数据
# 3. 调用 API 更新用户
# 4. 验证数据库中的更新

import pytest
import requests

class TestUserAPIDB:

    def test_create_user_db_verify(self, db, clean_users):
        """创建用户 - 数据库验证"""
        # API 创建用户
        response = requests.post(
            "http://localhost:8000/api/users",
            json={"username": "api_user", "email": "api@test.com", "age": 28}
        )
        assert response.status_code == 201
        user_id = response.json()["id"]

        # 数据库验证
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (user_id,)
            )
            user = cursor.fetchone()

        assert user is not None
        assert user["username"] == "api_user"
        assert user["email"] == "api@test.com"
        assert user["age"] == 28

    def test_update_user_db_verify(self, db, test_user):
        """更新用户 - 数据库验证"""
        # API 更新用户
        response = requests.put(
            f"http://localhost:8000/api/users/{test_user['id']}",
            json={"age": 30}
        )
        assert response.status_code == 200

        # 数据库验证
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT age FROM users WHERE id = %s",
                (test_user['id'],)
            )
            user = cursor.fetchone()

        assert user["age"] == 30

    def test_delete_user_db_verify(self, db, test_user):
        """删除用户 - 数据库验证"""
        # API 删除用户
        response = requests.delete(
            f"http://localhost:8000/api/users/{test_user['id']}"
        )
        assert response.status_code == 200

        # 数据库验证
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (test_user['id'],)
            )
            user = cursor.fetchone()

        assert user is None
```

#### 练习15：数据驱动数据库测试

```python
# tests/test_data_driven_db.py
# 要求：
# 1. 从 CSV 文件读取测试数据
# 2. 参数化执行数据库测试
# 3. 验证数据插入结果

import pytest
import csv

def load_user_data():
    """从 CSV 加载用户数据"""
    with open('tests/data/users.csv') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

# tests/data/users.csv
# username,email,age,expected
# user1,user1@test.com,20,success
# user2,user2@test.com,25,success
# ,empty@test.com,30,fail
# user3,,35,fail

@pytest.mark.parametrize("data", load_user_data())
def test_create_user_data_driven(db, clean_users, data):
    """数据驱动测试 - 创建用户"""
    import pymysql

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
                assert user is not None
                assert user["email"] == email
            else:
                assert False, "预期失败但成功了"

    except pymysql.err.IntegrityError:
        # 预期失败的情况
        assert expected == "fail"
```

#### 练习16：复杂查询练习

```sql
-- 要求：
-- 1. 实现复杂的多表连接查询
-- 2. 使用窗口函数
-- 3. 使用公用表表达式（CTE）

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

-- 4. 查询连续 3 天都有订单的用户
-- 实现查询

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
    SUM(o.amount) as total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY age_group
ORDER BY age_group;
```

### 综合练习（17-20）

#### 练习17：完整数据库测试类

```python
# tests/test_db_complete.py
# 要求：
# 1. 实现完整的数据库操作类
# 2. 包含连接池管理
# 3. 包含事务管理
# 4. 包含错误处理

import pymysql
from pymysql import Pool
from contextlib import contextmanager
from typing import List, Dict, Optional

class DatabaseManager:
    """数据库管理器"""

    def __init__(self, host, user, password, database, port=3306, pool_size=5):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.pool_size = pool_size
        self._pool = None

    def get_connection(self):
        """获取连接"""
        return pymysql.connect(**self.config)

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
            conn.close()

    def query(self, sql, params=None) -> List[Dict]:
        """查询数据"""
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()

    def execute(self, sql, params=None) -> int:
        """执行 SQL"""
        with self.connection() as conn:
            with conn.cursor() as cursor:
                affected = cursor.execute(sql, params)
                conn.commit()
                return affected

    def insert(self, table, data) -> int:
        """插入数据"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, tuple(data.values()))
                conn.commit()
                return cursor.lastrowid

    def transaction(self, operations):
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

# 测试用例
class TestDatabaseManager:

    @pytest.fixture
    def db(self):
        return DatabaseManager('localhost', 'root', 'password', 'test_db')

    def test_query(self, db):
        users = db.query("SELECT * FROM users LIMIT 10")
        assert isinstance(users, list)

    def test_insert(self, db):
        user_id = db.insert('users', {
            'username': 'test',
            'email': 'test@test.com',
            'age': 25
        })
        assert user_id > 0

    def test_transaction(self, db):
        operations = [
            ("UPDATE accounts SET balance = balance - 100 WHERE id = 1", None),
            ("UPDATE accounts SET balance = balance + 100 WHERE id = 2", None),
        ]
        result = db.transaction(operations)
        assert result is True
```

#### 练习18：数据库测试框架

```python
# tests/test_db_framework.py
# 要求：
# 1. 创建测试数据工厂
# 2. 实现数据验证工具
# 3. 支持数据快照比较

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
```

#### 练习19：数据库性能测试

```python
# tests/test_db_performance.py
# 要求：
# 1. 测试批量插入性能
# 2. 测试索引查询性能
# 3. 测试并发查询性能

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
```

#### 练习20：综合数据库测试项目

```python
# 要求：整合所学知识，完成企业级数据库测试项目
# 1. 数据库连接池管理
# 2. 测试数据工厂
# 3. 数据验证工具
# 4. 性能测试
# 5. API + 数据库集成测试
# 6. 测试报告生成

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
```

---

## 五、本周小结

1. **SQL**：测试数据验证的核心技能
2. **索引**：性能优化的关键
3. **事务**：保证数据一致性
4. **Python 操作**：自动化测试必备

### 下周预告

第8周学习 Git 版本控制。
