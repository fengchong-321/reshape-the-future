# 第 8 周 - MySQL 进阶 + Python 连接

## 学习目标
掌握 MySQL 索引、事务、性能优化，能够使用 Python 连接和操作数据库。

---

## 知识点清单

### 1. 索引
**掌握程度**: 原理、创建、查看、优化

**练习资源**:
- [MySQL 索引文档](https://dev.mysql.com/doc/refman/8.0/en/optimization-indexes.html)

**练习任务**:
- 创建索引
- 查看索引
- 理解索引的工作原理
- 分析什么时候需要索引

---

### 2. 事务
**掌握程度**: ACID、隔离级别、锁

**练习任务**:
- 理解事务的 ACID 特性
- 理解四种隔离级别
- 理解脏读、不可重复读、幻读

---

### 3. 视图
**掌握程度**: CREATE VIEW、使用场景

**练习任务**:
- 创建视图
- 使用视图简化查询

---

### 4. 存储过程
**掌握程度**: 基础语法、调用

**练习任务**:
- 编写简单存储过程
- 调用存储过程

---

### 5. 触发器
**掌握程度**: 定义、使用场景

**练习任务**:
- 理解触发器的用途
- 创建触发器

---

### 6. Python 连接
**掌握程度**: pymysql/SQLAlchemy

**练习资源**:
- [PyMySQL 文档](https://github.com/PyMySQL/PyMySQL)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)

**练习任务**:
- 用 pymysql 连接数据库
- 执行 CRUD 操作
- 用 SQLAlchemy ORM

---

### 7. ORM 基础
**掌握程度**: 模型定义、查询、关联

**练习任务**:
- 定义模型类
- 实现增删改查
- 实现关联查询

---

### 8. 性能优化
**掌握程度**: EXPLAIN、慢查询日志

**练习任务**:
- 用 EXPLAIN 分析查询
- 开启慢查询日志
- 优化慢查询

---

## 本周练习任务

### 必做任务

1. **SQLAlchemy 用户管理系统**
```python
# 实现一个用户管理系统
# 功能:
# - 用户注册（增）
# - 用户信息（查）
# - 修改资料（改）
# - 删除账号（删）
# - 用户关联订单（一对多）
```

2. **银行转账示例（事务）**
```python
# 实现一个银行转账示例
# 要求:
# - 使用事务
# - 转账失败时回滚
# - 记录交易日志
```

3. **慢查询优化**
```sql
-- 1. 创建一个有 100 万行数据的表
-- 2. 编写一个慢查询
-- 3. 用 EXPLAIN 分析
-- 4. 添加索引优化
-- 5. 对比优化前后的执行时间
```

4. **索引练习**
```sql
-- 1. 为常用查询字段创建索引
-- 2. 创建复合索引
-- 3. 理解索引覆盖
-- 4. 理解最左前缀原则
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 用户管理系统能正常运行
- [ ] 能用 EXPLAIN 分析查询
- [ ] 能解释事务隔离级别
- [ ] 能使用 SQLAlchemy ORM
- [ ] 能优化慢查询

---

## SQLAlchemy 速查表

### 连接配置
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('mysql+pymysql://user:password@localhost/dbname')
Session = sessionmaker(bind=engine)
Base = declarative_base()
```

### 模型定义
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # 关联订单
    orders = relationship('Order', back_populates='user')
```

### CRUD 操作
```python
session = Session()

# 增
user = User(username='john', email='john@example.com')
session.add(user)
session.commit()

# 查
user = session.query(User).filter_by(username='john').first()
users = session.query(User).all()
users = session.query(User).filter(User.age > 18).all()

# 改
user.email = 'new@example.com'
session.commit()

# 删
session.delete(user)
session.commit()
```

### 关联查询
```python
# 查询用户及其订单
user = session.query(User).options(
    joinedload(User.orders)
).filter_by(username='john').first()

for order in user.orders:
    print(order.id, order.total_amount)
```

---

## 面试考点

### 高频面试题
1. 索引的数据结构（B+ 树）？
2. 聚簇索引和非聚簇索引的区别？
3. 什么是覆盖索引？
4. 事务的 ACID 特性？
5. 四种隔离级别及解决的问题？
6. 什么是脏读、不可重复读、幻读？
7. 什么是悲观锁和乐观锁？
8. EXPLAIN 结果中各字段的含义？

### 场景题
```sql
-- 1. 分析一个慢查询
EXPLAIN SELECT * FROM orders
WHERE user_id = 100
ORDER BY created_at DESC;

-- 2. 优化建议
-- - 为 user_id 添加索引
-- - 为 created_at 添加索引
-- - 考虑复合索引 (user_id, created_at)
```

---

## Python 连接数据库示例

### 使用 PyMySQL
```python
import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='dbname',
    charset='utf8mb4'
)

# 创建游标
cursor = conn.cursor()

# 执行查询
cursor.execute('SELECT * FROM users')
results = cursor.fetchall()

# 执行插入
cursor.execute(
    'INSERT INTO users (username, email) VALUES (%s, %s)',
    ('john', 'john@example.com')
)
conn.commit()

# 关闭连接
cursor.close()
conn.close()
```

### 使用 SQLAlchemy（完整示例）
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100))

engine = create_engine('mysql+pymysql://root:password@localhost/dbname')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# CRUD 操作
user = User(username='john', email='john@example.com')
session.add(user)
session.commit()

users = session.query(User).all()
```

---

## 每日学习检查清单

### Day 1-2: 索引 + 事务
- [ ] 学习索引原理
- [ ] 创建和查看索引
- [ ] 学习事务
- [ ] 理解隔离级别

### Day 3-4: Python 连接 + ORM
- [ ] 学习 PyMySQL
- [ ] 学习 SQLAlchemy
- [ ] 实现用户管理系统
- [ ] GitHub 提交

### Day 5-6: 性能优化
- [ ] 学习 EXPLAIN
- [ ] 开启慢查询日志
- [ ] 优化慢查询
- [ ] 银行转账示例

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成项目
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 8 周总结

### 学习内容
- 掌握了 MySQL 索引和事务
- 学会了 SQLAlchemy ORM
- 能优化慢查询

### 作品
- 用户管理系统
- 银行转账示例

### 遇到的问题
- ...

### 下周改进
- ...
```
