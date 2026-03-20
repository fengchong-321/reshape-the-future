# 第 19 周 - FastAPI 后端

## 学习目标
掌握 FastAPI 框架的核心功能，能够使用 Python 编写 RESTful API。

---

## 知识点清单

### 1. 安装运行
**掌握程度**: uvicorn、热加载

**练习资源**:
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [FastAPI 入门教程](https://fastapi.tiangolo.com/tutorial/)

**练习任务**:
- 安装 FastAPI 和 uvicorn
- 启动开发服务器
- 理解热加载

---

### 2. 路由
**掌握程度**: path params、query params

**练习任务**:
- 定义路由
- 处理路径参数
- 处理查询参数

---

### 3. 请求体
**掌握程度**: Pydantic 模型、验证

**练习资源**:
- [Pydantic 文档](https://docs.pydantic.dev/)

**练习任务**:
- 定义 Pydantic 模型
- 验证请求数据

---

### 4. 响应
**掌握程度**: 响应模型、状态码

**练习任务**:
- 定义响应模型
- 设置状态码

---

### 5. 依赖注入
**掌握程度**: Depends、复用逻辑

**练习任务**:
- 实现依赖注入
- 实现认证依赖

---

### 6. 数据库
**掌握程度**: SQLAlchemy、异步

**练习任务**:
- 集成 SQLAlchemy
- 实现 CRUD 操作

---

### 7. 认证
**掌握程度**: JWT、OAuth2

**练习任务**:
- 实现 JWT 认证
- 实现 OAuth2 密码流程

---

### 8. 文档
**掌握程度**: Swagger、ReDoc

**练习任务**:
- 理解自动生成的 API 文档
- 使用 Swagger UI 测试接口

---

## 本周练习任务

### 必做任务

1. **用户管理 API**
```python
# 实现一个用户管理 API
# 功能:
# - POST /users - 创建用户
# - GET /users - 获取用户列表
# - GET /users/{id} - 获取用户详情
# - PUT /users/{id} - 更新用户
# - DELETE /users/{id} - 删除用户

# 要求:
# - 使用 Pydantic 验证
# - 使用 SQLAlchemy ORM
# - 使用 pytest 测试
```

2. **博客 API**
```python
# 实现一个博客 API
# 功能:
# - 文章 CRUD
# - 评论功能
# - 标签系统
# - 用户认证

# 要求:
# - 完整的 RESTful 设计
# - 分页支持
# - 过滤支持
```

3. **API 测试**
```python
# 为 API 编写完整测试
# 要求:
# - 使用 TestClient
# - 50 个测试用例
# - 覆盖率 90%+
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] API 通过 50 个测试用例
- [ ] Swagger 文档完整
- [ ] 能解释依赖注入的工作原理
- [ ] 能实现 JWT 认证
- [ ] 能集成数据库

---

## FastAPI 速查表

### 安装
```bash
pip install fastapi uvicorn sqlalchemy pydantic
pip install python-jose[cryptography]  # JWT
pip install passlib[bcrypt]  # 密码加密
```

### 基础示例
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### Pydantic 模型
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
```

### 路由定义
```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    return user

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### 依赖注入
```python
from fastapi import Depends, HTTPException

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Header(...)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401)
    return user

@app.get("/users/me")
def read_current_user(user: User = Depends(get_current_user)):
    return user
```

### SQLAlchemy 集成
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
```

### JWT 认证
```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

## 面试考点

### 高频面试题
1. FastAPI 和 Flask/Django 的区别？
2. 什么是依赖注入？
3. Pydantic 的作用？
4. 如何实现 JWT 认证？
5. 异步和同步的区别？
6. 如何文件上传？
7. 如何实现分页？

### 代码题
```python
# 1. 实现一个 CRUD API
# 2. 实现 JWT 认证
# 3. 实现文件上传
```

---

## 每日学习检查清单

### Day 1-2: 基础 + 路由
- [ ] 安装 FastAPI
- [ ] 学习路由定义
- [ ] 完成基础 API
- [ ] GitHub 提交

### Day 3-4: 请求体 + 响应
- [ ] 学习 Pydantic
- [ ] 学习响应模型
- [ ] 完成用户 API
- [ ] GitHub 提交

### Day 5-6: 依赖 + 数据库 + 认证
- [ ] 学习依赖注入
- [ ] 学习 SQLAlchemy
- [ ] 学习 JWT 认证
- [ ] 完成博客 API

### Day 7: 复习 + 测试
- [ ] 复习本周内容
- [ ] 编写 API 测试
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 19 周总结

### 学习内容
- 掌握了 FastAPI 基础
- 能编写 RESTful API
- 能实现认证

### 作品
- 用户管理 API
- 博客 API

### 遇到的问题
- ...

### 下周改进
- ...
```
