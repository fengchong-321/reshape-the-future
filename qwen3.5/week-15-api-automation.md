# 第 15 周 - 接口自动化

## 学习目标
掌握 HTTP 协议基础和接口自动化测试，能够使用 requests 库编写完整的接口测试用例。

---

## 知识点清单

### 1. HTTP 基础
**掌握程度**: 方法/状态码/头/体

**练习资源**:
- [HTTP 协议详解](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)
- [HTTP 状态码](https://httpstatuses.com/)

**练习任务**:
- 理解常见 HTTP 方法（GET/POST/PUT/DELETE）
- 记忆常见状态码（200/201/400/401/403/404/500）
- 理解请求头和响应头

---

### 2. requests 库
**掌握程度**: get/post/put/delete

**练习资源**:
- [requests 官方文档](https://requests.readthedocs.io/)
- [requests 快速入门](https://requests.readthedocs.io/en/latest/user/quickstart/)

**练习任务**:
- 发送各种 HTTP 请求
- 处理响应
- 处理超时

---

### 3. 会话管理
**掌握程度**: Session、cookie 持久化

**练习任务**:
- 使用 Session 保持登录状态
- 理解 cookie 的工作原理

---

### 4. 认证
**掌握程度**: Basic/Bearer/OAuth2

**练习任务**:
- 实现 Basic 认证
- 实现 Bearer Token 认证
- 理解 OAuth2 流程

---

### 5. 文件上传
**掌握程度**: multipart/form-data

**练习任务**:
- 上传文件
- 上传多文件

---

### 6. 接口测试设计
**掌握程度**: 用例组织、断言策略

**练习任务**:
- 设计 50 个接口测试用例
- 理解接口测试分层

---

### 7. 数据驱动
**掌握程度**: 外部数据源、参数化

**练习任务**:
- 从外部文件读取测试数据
- 实现参数化测试

---

### 8. 报告
**掌握程度**: Allure、HTML 报告

**练习任务**:
- 集成 Allure
- 生成测试报告

---

## 本周练习任务

### 必做任务

1. **RESTful API 测试**
```python
# 为 JSONPlaceholder API 编写完整测试
# API: https://jsonplaceholder.typicode.com/

# 测试内容:
# - GET /posts - 获取文章列表
# - GET /posts/1 - 获取单篇文章
# - POST /posts - 创建文章
# - PUT /posts/1 - 更新文章
# - DELETE /posts/1 - 删除文章

# 要求:
# - 50 个测试用例
# - 覆盖率 90%+
# - Allure 报告
```

2. **接口自动化框架**
```python
# 实现一个接口自动化框架
# 目录结构:
# api_tests/
#   common/
#     client.py       # HTTP 客户端
#     config.py       # 配置
#   apis/
#     user_api.py     # 用户相关 API
#     post_api.py     # 文章相关 API
#   tests/
#     test_user.py
#     test_post.py
#   conftest.py
#   pytest.ini

# 要求:
# - 支持数据驱动
# - 支持 Allure 报告
# - 支持 CI/CD
```

3. **认证测试**
```python
# 实现三种认证测试:
# 1. Basic 认证
# 2. Bearer Token 认证
# 3. API Key 认证

# 要求:
# - 理解每种认证的差异
# - 能正确处理认证失败
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 50 个接口测试用例全部通过
- [ ] Allure 报告能展示趋势图
- [ ] 能解释接口测试的分层策略
- [ ] 能处理各种认证方式
- [ ] 能编写接口自动化框架

---

## requests 速查表

### 基础请求
```python
import requests

# GET 请求
response = requests.get('https://api.example.com/users')

# 带参数
response = requests.get('https://api.example.com/users', params={'page': 1})

# POST 请求
response = requests.post('https://api.example.com/users', json={'name': 'test'})

# PUT 请求
response = requests.put('https://api.example.com/users/1', json={'name': 'updated'})

# DELETE 请求
response = requests.delete('https://api.example.com/users/1')
```

### 处理响应
```python
# 状态码
print(response.status_code)

# 响应头
print(response.headers)

# 响应体
print(response.text)
print(response.json())

# 断言
assert response.status_code == 200
assert response.json()['id'] == 1
```

### Session 管理
```python
session = requests.Session()

# 登录
session.post('https://api.example.com/login', json={
    'username': 'test',
    'password': 'password'
})

# 保持登录状态发送请求
response = session.get('https://api.example.com/profile')
```

### 认证
```python
# Basic 认证
response = requests.get('https://api.example.com/admin',
    auth=('user', 'pass'))

# Bearer Token
headers = {'Authorization': 'Bearer <token>'}
response = requests.get('https://api.example.com/users', headers=headers)

# API Key
headers = {'X-API-Key': 'your-api-key'}
response = requests.get('https://api.example.com/users', headers=headers)
```

### 文件上传
```python
# 上传单个文件
with open('file.txt', 'rb') as f:
    files = {'file': f}
    response = requests.post('https://api.example.com/upload', files=files)

# 上传多个文件
files = [
    ('files', ('file1.txt', open('file1.txt', 'rb'))),
    ('files', ('file2.txt', open('file2.txt', 'rb')))
]
response = requests.post('https://api.example.com/upload', files=files)
```

### 超时和重试
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 超时
response = requests.get('https://api.example.com/users', timeout=5)

# 重试策略
session = requests.Session()
retry = Retry(total=3, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

---

## 面试考点

### 高频面试题
1. GET 和 POST 的区别？
2. 常见 HTTP 状态码的含义？
3. Cookie 和 Session 的区别？
4. 什么是幂等性？
5. 如何处理接口依赖？
6. 接口测试如何断言？
7. 什么是 Mock？如何使用？

### 代码题
```python
# 1. 封装一个 HTTP 客户端
class APIClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def get(self, path, **kwargs):
        # 实现...
        pass

# 2. 为登录接口编写测试
# POST /api/login
# 请求：{"username": "test", "password": "pass"}
# 响应：{"token": "xxx", "user": {...}}
```

---

## 每日学习检查清单

### Day 1-2: HTTP 基础 + requests
- [ ] 学习 HTTP 协议
- [ ] 学习 requests 库
- [ ] 完成基础请求练习
- [ ] GitHub 提交

### Day 3-4: 会话 + 认证
- [ ] 学习 Session 管理
- [ ] 学习认证方式
- [ ] 完成认证测试
- [ ] GitHub 提交

### Day 5-6: 接口测试设计 + 报告
- [ ] 设计 50 个测试用例
- [ ] 集成 Allure
- [ ] 生成测试报告
- [ ] 完成自动化框架

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成剩余测试
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 15 周总结

### 学习内容
- 掌握了 HTTP 协议
- 学会了 requests 库
- 能编写接口自动化框架

### 作品
- RESTful API 测试
- 接口自动化框架

### 遇到的问题
- ...

### 下周改进
- ...
```
