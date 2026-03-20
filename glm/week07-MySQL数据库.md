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

### 练习1：查询练习

```sql
-- 假设有以下表结构
-- users(id, username, email, age, status, created_at)
-- orders(id, user_id, amount, status, created_at)

-- 1. 查询年龄大于25岁的活跃用户
-- 2. 统计每个年龄段的人数
-- 3. 查询有订单的用户及其订单总金额
-- 4. 查询最近7天注册的用户
-- 5. 查询消费金额前10的用户
```

### 练习2：Python 数据库操作

```python
# 实现一个完整的数据库测试类
# 包含：连接、查询、插入、更新、删除、事务
```

### 练习3：测试用例

```python
# 编写用户 CRUD 的数据库验证测试
# 使用 pytest fixture 管理数据
```

---

## 五、本周小结

1. **SQL**：测试数据验证的核心技能
2. **索引**：性能优化的关键
3. **事务**：保证数据一致性
4. **Python 操作**：自动化测试必备

### 下周预告

第8周学习 Git 版本控制。
