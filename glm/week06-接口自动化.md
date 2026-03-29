# 第6周：接口自动化测试实战

## 本周目标

掌握 Requests 库的使用，能编写完整的接口自动化测试框架。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Requests 基础 | GET/POST、参数、请求头 | ⭐⭐⭐⭐⭐ |
| 会话管理 | Session、Cookie 处理 | ⭐⭐⭐⭐⭐ |
| 响应处理 | 状态码、JSON、断言 | ⭐⭐⭐⭐⭐ |
| 接口封装 | 设计模式、业务封装 | ⭐⭐⭐⭐⭐ |
| 认证处理 | Token、签名、加密 | ⭐⭐⭐⭐ |
| 文件操作 | 上传/下载 | ⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 Requests 基础

```python
import requests

# ============================================
# GET 请求
# ============================================
# 基础 GET
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

# 带参数
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1, "page": 2}
)

# 带请求头
response = requests.get(
    "https://api.example.com/users",
    headers={"Authorization": "Bearer token123"}
)

# ============================================
# POST 请求
# ============================================
# JSON 数据
response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json={"title": "测试", "body": "内容", "userId": 1}
)

# 表单数据
response = requests.post(
    "https://example.com/login",
    data={"username": "admin", "password": "123456"}
)

# 文件上传
files = {"file": open("test.txt", "rb")}
response = requests.post(
    "https://example.com/upload",
    files=files
)

# ============================================
# 其他方法
# ============================================
# PUT - 完整更新
response = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"title": "更新标题", "body": "更新内容", "userId": 1}
)

# PATCH - 部分更新
response = requests.patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"title": "只更新标题"}
)

# DELETE - 删除
response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")

# ============================================
# 响应对象
# ============================================
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

response.status_code      # 状态码：200
response.ok               # 是否成功：True
response.reason           # 状态描述："OK"
response.headers          # 响应头（字典）
response.cookies          # Cookies
response.text             # 文本内容
response.content          # 二进制内容
response.json()           # 解析 JSON

# 检查响应
if response.status_code == 200:
    data = response.json()
    print(data["title"])

# 使用 raise_for_status
response = requests.get("https://example.com/notexist")
response.raise_for_status()  # 非 2xx 抛出 HTTPError

# ============================================
# 超时与重试
# ============================================
# 超时
response = requests.get(
    "https://example.com",
    timeout=5  # 5 秒超时
)

# 分别设置连接和读取超时
response = requests.get(
    "https://example.com",
    timeout=(3, 10)  # 连接 3 秒，读取 10 秒
)

# 重试
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(
    total=3,  # 总重试次数
    backoff_factor=0.5,  # 重试间隔因子
    status_forcelist=[500, 502, 503, 504]  # 遇到这些状态码重试
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)
```

---

### 2.2 会话管理

```python
import requests

# ============================================
# 使用 Session 保持状态
# ============================================
# 不使用 Session（每次请求独立）
requests.post("https://example.com/login", json={"username": "admin"})
requests.get("https://example.com/profile")  # 没有登录状态

# 使用 Session（共享 Cookie）
session = requests.Session()
session.post("https://example.com/login", json={"username": "admin"})
session.get("https://example.com/profile")  # 有登录状态

# ============================================
# Session 全局配置
# ============================================
session = requests.Session()

# 全局请求头
session.headers.update({
    "Content-Type": "application/json",
    "User-Agent": "MyTestClient/1.0"
})

# 全局认证
session.auth = ("username", "password")

# 全局超时（需要 monkey patch）
session.request = lambda *args, **kwargs: requests.Session.request(session, *args, timeout=5, **kwargs)

# ============================================
# Cookie 操作
# ============================================
session = requests.Session()

# 获取 Cookie
response = session.get("https://example.com")
print(session.cookies.get_dict())

# 设置 Cookie
session.cookies.set("my_cookie", "value")

# 从响应获取
for cookie in response.cookies:
    print(f"{cookie.name}: {cookie.value}")
```

---

### 2.3 接口封装设计

```python
import requests
from typing import Optional, Dict, Any

# ============================================
# 基础 API 客户端
# ============================================
class APIClient:
    """API 客户端基类"""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """配置 Session"""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        # 配置重试
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        retry = Retry(total=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _build_url(self, endpoint: str) -> str:
        """构建完整 URL"""
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}{endpoint}"

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """发送请求"""
        url = self._build_url(endpoint)

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )

        # 记录日志
        self._log_request(method, url, response.status_code)

        return response

    def _log_request(self, method: str, url: str, status_code: int):
        """记录请求日志"""
        print(f"[{method}] {url} -> {status_code}")

    # 便捷方法
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)


# ============================================
# 业务 API 封装
# ============================================
class UserAPI(APIClient):
    """用户相关 API"""

    def login(self, username: str, password: str) -> requests.Response:
        """登录"""
        return self.post("/api/login", json={
            "username": username,
            "password": password
        })

    def logout(self) -> requests.Response:
        """登出"""
        return self.post("/api/logout")

    def get_profile(self) -> requests.Response:
        """获取用户信息"""
        return self.get("/api/user/profile")

    def update_profile(self, data: Dict) -> requests.Response:
        """更新用户信息"""
        return self.put("/api/user/profile", json=data)

    def get_users(self, page: int = 1, size: int = 10) -> requests.Response:
        """获取用户列表"""
        return self.get("/api/users", params={"page": page, "size": size})


class OrderAPI(APIClient):
    """订单相关 API"""

    def create_order(self, order_data: Dict) -> requests.Response:
        """创建订单"""
        return self.post("/api/orders", json=order_data)

    def get_order(self, order_id: str) -> requests.Response:
        """获取订单详情"""
        return self.get(f"/api/orders/{order_id}")

    def get_orders(self, status: str = None) -> requests.Response:
        """获取订单列表"""
        params = {"status": status} if status else {}
        return self.get("/api/orders", params=params)

    def cancel_order(self, order_id: str) -> requests.Response:
        """取消订单"""
        return self.post(f"/api/orders/{order_id}/cancel")


# ============================================
# 使用示例
# ============================================
# 初始化
user_api = UserAPI("https://api.example.com")

# 登录
login_resp = user_api.login("admin", "123456")
assert login_resp.status_code == 200
token = login_resp.json()["token"]

# 设置 Token
user_api.session.headers["Authorization"] = f"Bearer {token}"

# 获取用户信息
profile_resp = user_api.get_profile()
assert profile_resp.json()["username"] == "admin"
```

---

### 2.4 认证与签名

```python
import requests
import hashlib
import hmac
import time
import json
from typing import Dict

# ============================================
# Token 认证
# ============================================
class TokenAuth:
    """Token 认证"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def login(self, username: str, password: str):
        """登录获取 Token"""
        response = self.session.post(
            f"{self.base_url}/login",
            json={"username": username, "password": password}
        )
        data = response.json()
        self.token = data["token"]
        self.session.headers["Authorization"] = f"Bearer {self.token}"
        return response

    def request(self, method: str, url: str, **kwargs):
        """带 Token 的请求"""
        if not self.token:
            raise Exception("请先登录")

        response = self.session.request(method, f"{self.base_url}{url}", **kwargs)

        # Token 过期处理
        if response.status_code == 401:
            self.token = None
            raise Exception("Token 已过期，请重新登录")

        return response


# ============================================
# API 签名
# ============================================
class SignedAPI:
    """带签名的 API 客户端"""

    def __init__(self, base_url: str, app_id: str, app_secret: str):
        self.base_url = base_url
        self.app_id = app_id
        self.app_secret = app_secret
        self.session = requests.Session()

    def _generate_signature(self, params: Dict, timestamp: int) -> str:
        """生成签名"""
        # 1. 参数排序
        sorted_params = sorted(params.items())

        # 2. 拼接字符串
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

        # 3. 加入密钥和时间戳
        sign_str = f"{param_str}&timestamp={timestamp}&secret={self.app_secret}"

        # 4. 计算签名（根据接口要求选择算法）
        signature = hashlib.md5(sign_str.encode()).hexdigest().upper()

        return signature

    def request(self, method: str, endpoint: str, params: Dict = None, **kwargs):
        """带签名的请求"""
        params = params or {}
        timestamp = int(time.time())

        # 添加公共参数
        params["app_id"] = self.app_id
        params["timestamp"] = timestamp

        # 生成签名
        signature = self._generate_signature(params, timestamp)
        params["sign"] = signature

        # 发送请求
        url = f"{self.base_url}{endpoint}"
        if method.upper() == "GET":
            return self.session.get(url, params=params, **kwargs)
        else:
            return self.session.request(method, url, json=params, **kwargs)


# ============================================
# HMAC 签名
# ============================================
class HMACAuth:
    """HMAC 认证"""

    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.secret_key = secret_key

    def sign(self, data: str) -> str:
        """HMAC-SHA256 签名"""
        return hmac.new(
            self.secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

    def get_headers(self, method: str, path: str, body: str = "") -> Dict:
        """获取认证头"""
        timestamp = str(int(time.time()))
        string_to_sign = f"{method}\n{path}\n{timestamp}\n{body}"

        signature = self.sign(string_to_sign)

        return {
            "X-Access-Key": self.access_key,
            "X-Timestamp": timestamp,
            "X-Signature": signature
        }
```

---

### 2.5 文件上传下载

```python
import requests
from pathlib import Path

# ============================================
# 文件上传
# ============================================
# 简单上传
files = {"file": open("test.txt", "rb")}
response = requests.post("https://example.com/upload", files=files)

# 指定文件名和类型
files = {
    "file": ("test.txt", open("test.txt", "rb"), "text/plain")
}
response = requests.post("https://example.com/upload", files=files)

# 多文件上传
files = [
    ("files", ("file1.txt", open("file1.txt", "rb"))),
    ("files", ("file2.txt", open("file2.txt", "rb"))),
]
response = requests.post("https://example.com/upload", files=files)

# 文件 + 表单数据
files = {"file": open("test.txt", "rb")}
data = {"description": "测试文件"}
response = requests.post("https://example.com/upload", files=files, data=data)

# ============================================
# 文件下载
# ============================================
# 下载到内存
response = requests.get("https://example.com/file.pdf")
content = response.content

# 下载到文件
response = requests.get("https://example.com/file.pdf", stream=True)
with open("downloaded.pdf", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

# 带进度条下载
def download_with_progress(url: str, filepath: str):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    with open(filepath, "wb") as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            progress = downloaded / total_size * 100 if total_size > 0 else 0
            print(f"\r下载进度: {progress:.1f}%", end="")

    print("\n下载完成")

# ============================================
# 封装文件操作
# ============================================
class FileAPI:
    """文件 API"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def upload(self, filepath: str, folder: str = "") -> dict:
        """上传文件"""
        path = Path(filepath)
        files = {
            "file": (path.name, open(path, "rb"))
        }
        data = {"folder": folder} if folder else {}

        response = self.session.post(
            f"{self.base_url}/upload",
            files=files,
            data=data
        )
        response.raise_for_status()
        return response.json()

    def download(self, file_id: str, save_path: str) -> str:
        """下载文件"""
        response = self.session.get(
            f"{self.base_url}/download/{file_id}",
            stream=True
        )
        response.raise_for_status()

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return save_path
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 能熟练使用 requests 发送各种请求
- [ ] 能使用 Session 管理登录状态
- [ ] 能设计接口封装类
- [ ] 能处理 Token 认证

### 应该了解

- [ ] API 签名机制
- [ ] 文件上传下载

---

## 四、练习内容

### 基础练习（1-8）

---

**练习1：GET 请求基础**

**场景说明**：你需要测试一个公开的 REST API，验证 GET 请求能够正确获取数据。

**具体需求**：
1. 使用 `requests.get()` 发送基础 GET 请求到 `https://jsonplaceholder.typicode.com/posts/1`
2. 获取并验证响应状态码为 200
3. 获取并解析 JSON 响应体，验证包含 `id`、`title`、`body` 字段
4. 使用 `params` 参数传递查询参数 `userId=1`
5. 使用 `headers` 参数设置请求头 `Accept: application/json`

**使用示例**：
```python
import requests

# 基础 GET 请求
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)  # 200
print(response.json()["title"])  # 文章标题

# 带参数的 GET 请求
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1}
)
print(len(response.json()))  # 返回该用户的文章数量

# 带请求头的 GET 请求
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    headers={"Accept": "application/json"}
)
print(response.headers["Content-Type"])  # application/json
```

**验收标准**：
- [ ] 能正确发送 GET 请求并获取响应
- [ ] 能正确解析 JSON 响应体
- [ ] 能使用 params 传递查询参数
- [ ] 能设置自定义请求头

---

---

**练习2：POST 请求基础**

**场景说明**：你需要测试用户创建功能，验证 POST 请求能够正确提交数据。

**具体需求**：
1. 使用 `requests.post()` 发送 JSON 格式数据创建文章
2. 使用 `json` 参数发送 JSON 数据，`data` 参数发送表单数据
3. 验证响应状态码为 201（创建成功）
4. 验证响应体中返回的数据与提交的数据一致
5. 理解 `json` 参数和 `data` 参数的区别

**使用示例**：
```python
import requests

# 发送 JSON 数据创建文章
response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json={"title": "测试文章", "body": "这是内容", "userId": 1}
)
print(response.status_code)  # 201
print(response.json()["title"])  # "测试文章"
print(response.json()["id"])  # 自动生成的 ID

# 发送表单数据（常用于登录）
response = requests.post(
    "https://httpbin.org/post",
    data={"username": "admin", "password": "123456"}
)
print(response.status_code)  # 200
print(response.json()["form"]["username"])  # "admin"
```

**验收标准**：
- [ ] 能正确发送 JSON 格式的 POST 请求
- [ ] 能正确发送表单格式的 POST 请求
- [ ] 能验证响应状态码和响应体
- [ ] 理解 json 和 data 参数的区别

---

---

**练习3：响应处理**

**场景说明**：在接口测试中，需要正确解析各种响应格式并处理不同的状态码。

**具体需求**：
1. 使用 `response.json()` 解析 JSON 响应
2. 使用 `response.headers` 获取响应头信息
3. 使用 `response.status_code` 和 `response.ok` 判断请求是否成功
4. 使用 `response.raise_for_status()` 在状态码非 2xx 时抛出异常
5. 处理常见的 HTTP 状态码：200、201、400、404、500

**使用示例**：
```python
import requests

# 解析 JSON 响应
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
data = response.json()
print(data["id"])      # 1
print(data["title"])   # 文章标题

# 获取响应头
content_type = response.headers.get("Content-Type")
print(content_type)    # application/json; charset=utf-8

# 判断请求成功
print(response.status_code)  # 200
print(response.ok)           # True

# 使用 raise_for_status
try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
    response.raise_for_status()  # 404 会抛出 HTTPError
except requests.exceptions.HTTPError as e:
    print(f"请求失败: {e}")
```

**验收标准**：
- [ ] 能正确解析 JSON 格式的响应体
- [ ] 能获取并使用响应头信息
- [ ] 能判断和处理不同的 HTTP 状态码
- [ ] 能使用 raise_for_status() 处理错误响应

---

---

**练习4：PUT/PATCH/DELETE 请求**

**场景说明**：完成资源的 CRUD 操作，理解 PUT（完整更新）、PATCH（部分更新）和 DELETE（删除）的区别。

**具体需求**：
1. 使用 `requests.put()` 完整更新资源（需要传递所有字段）
2. 使用 `requests.patch()` 部分更新资源（只传递需要更新的字段）
3. 使用 `requests.delete()` 删除资源
4. 理解 PUT 和 PATCH 的语义区别
5. 验证各种操作的响应状态码

**使用示例**：
```python
import requests

# PUT 请求 - 完整更新（需要传所有字段）
response = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"id": 1, "title": "更新后的标题", "body": "更新后的内容", "userId": 1}
)
print(response.status_code)  # 200
print(response.json()["title"])  # "更新后的标题"

# PATCH 请求 - 部分更新（只传需要更新的字段）
response = requests.patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json={"title": "只更新标题"}
)
print(response.status_code)  # 200
print(response.json()["title"])  # "只更新标题"

# DELETE 请求 - 删除资源
response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)  # 200
```

**验收标准**：
- [ ] 能正确使用 PUT 请求完整更新资源
- [ ] 能正确使用 PATCH 请求部分更新资源
- [ ] 能正确使用 DELETE 请求删除资源
- [ ] 理解 PUT 和 PATCH 的语义区别

---

---

**练习5：Session 管理基础**

**场景说明**：在接口测试中，需要保持登录状态，多个请求之间共享 Cookie 和 Session。

**具体需求**：
1. 创建 `requests.Session()` 对象
2. 使用 Session 发送多个请求，自动保持 Cookie
3. 使用 `session.headers.update()` 设置全局请求头
4. 验证 Session 能自动管理 Cookie
5. 理解 Session 与独立请求的区别

**使用示例**：
```python
import requests

# 创建 Session
session = requests.Session()

# 设置全局请求头（所有请求都会携带）
session.headers.update({
    "User-Agent": "MyTestClient/1.0",
    "Accept": "application/json"
})

# 使用 Session 发送多个请求
response1 = session.get("https://jsonplaceholder.typicode.com/posts/1")
response2 = session.get("https://jsonplaceholder.typicode.com/posts/2")

print(response1.status_code)  # 200
print(response2.status_code)  # 200

# Cookie 自动管理
session.get("https://httpbin.org/cookies/set/session_id/abc123")
response = session.get("https://httpbin.org/cookies")
print(response.json()["cookies"])  # {"session_id": "abc123"}

# 关闭 Session
session.close()
```

**验收标准**：
- [ ] 能正确创建和使用 Session 对象
- [ ] 能设置全局请求头
- [ ] 能验证 Cookie 自动管理功能
- [ ] 理解 Session 的使用场景

---

**练习6：超时和异常处理**

**场景说明**：在网络不稳定或服务器响应慢的情况下，需要正确处理超时和连接异常。
**具体需求**：
1. 使用 `timeout` 参数设置请求超时时间（秒）
2. 捕获 `requests.exceptions.Timeout` 超时异常
3. 捕获 `requests.exceptions.ConnectionError` 连接异常
4. 使用 `response.raise_for_status()` 在状态码非 2xx 时抛出异常
5. 理解不同异常类型的使用场景
**使用示例**：
```python
import requests

# 设置超时
response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=5)
print(response.status_code)  # 200

# 处理超时异常
try:
    requests.get("https://httpbin.org/delay/5", timeout=0.1)
except requests.exceptions.Timeout as e:
    print(f"请求超时: {e}")

# 处理连接异常
try:
    requests.get("https://this-domain-does-not-exist-12345.com")
except requests.exceptions.ConnectionError as e:
    print(f"连接失败: {e}")

# 使用 raise_for_status 处理 HTTP 错误
response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
try:
    response.raise_for_status()  # 404 会抛出 HTTPError
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e}")
```
**验收标准**：
- [ ] 能正确设置请求超时
- [ ] 能捕获超时异常 Timeout
- [ ] 能捕获连接异常 ConnectionError
- [ ] 能使用 raise_for_status() 处理 HTTP 错误

---

**练习7：基础 API 客户端封装**

**场景说明**：为了提高代码复用性，需要封装一个通用的 API 客户端基类。
**具体需求**：
1. 创建 `APIClient` 类，封装常用的 HTTP 请求方法
2. 构造函数接收 `base_url` 和 `timeout` 参数
3. 实现 `get(endpoint, **kwargs)` 方法发送 GET 请求
4. 实现 `post(endpoint, **kwargs)` 方法发送 POST 请求
5. 自动拼接完整 URL（base_url + endpoint）
6. 所有请求自动应用 timeout 设置
**使用示例**：
```python
import requests

class APIClient:
    """API 客户端基类"""

    def __init__(self, base_url, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint, **kwargs):
        """GET 请求"""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, timeout=self.timeout, **kwargs)

    def post(self, endpoint, **kwargs):
        """POST 请求"""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, timeout=self.timeout, **kwargs)

# 使用
client = APIClient("https://jsonplaceholder.typicode.com")

# GET 请求
response = client.get("/posts/1")
print(response.status_code)  # 200

# POST 请求
response = client.post("/posts", json={"title": "测试", "body": "内容", "userId": 1})
print(response.status_code)  # 201
```
**验收标准**：
- [ ] 能正确创建 APIClient 类
- [ ] 能自动拼接 base_url 和 endpoint
- [ ] GET 和 POST 方法正常工作
- [ ] timeout 配置生效

---

**练习8：文件上传基础**

**场景说明**：在接口测试中，经常需要测试文件上传功能，如头像上传、文档上传等。
**具体需求**：
1. 使用 `files` 参数上传单个文件
2. 指定上传文件的文件名和 MIME 类型： `files = {"file": ("filename.txt", file_object, "text/plain")}`
3. 上传文件同时传递其他表单参数
4. 使用 `tempfile` 创建临时测试文件，测试完成后自动清理
**使用示例**：
```python
import requests
import tempfile
import os

# 创建临时测试文件
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
    f.write("这是测试内容")
    temp_path = f.name

try:
    # 简单上传
    files = {"file": open(temp_path, "rb")}
    response = requests.post("https://httpbin.org/post", files=files)
    print(response.status_code)  # 200

    # 指定文件名和 MIME 类型
    files = {"file": ("custom_name.txt", open(temp_path, "rb"), "text/plain")}
    response = requests.post("https://httpbin.org/post", files=files)
    print(response.json()["files"]["file"])  # 文件内容

    # 上传文件同时传递其他参数
    files = {"file": open(temp_path, "rb")}
    data = {"description": "测试文件", "category": "test"}
    response = requests.post("https://httpbin.org/post", files=files, data=data)
finally:
    os.unlink(temp_path)  # 清理临时文件
```
**验收标准**：
- [ ] 能正确上传单个文件
- [ ] 能指定文件名和 MIME 类型
- [ ] 能同时上传文件和表单数据
- [ ] 测试完成后能清理临时文件

---

### 进阶练习（9-16）

---

**练习9：完整 API 客户端封装**

**场景说明**：企业级接口测试需要一个功能完善的 API 客户端，支持多种 HTTP 方法、自动重试和日志记录。
**具体需求**：
1. 支持 GET/POST/PUT/PATCH/DELETE 五种 HTTP 方法
2. 配置自动重试机制（遇到 500/502/503/504 状态码自动重试）
3. 记录请求日志（方法、URL、状态码）
4. 使用 `requests.adapters.HTTPAdapter` 和 `urllib3.util.retry.Retry` 实现重试
5. 所有请求方法通过统一的 `request()` 方法实现
**使用示例**：
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    """完整 API 客户端"""

    def __init__(self, base_url, timeout=30, retry_times=3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self._setup_retry(retry_times)

    def _setup_retry(self, retry_times):
        """配置自动重试"""
        retry = Retry(
            total=retry_times,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(self, method, endpoint, **kwargs):
        """统一请求方法"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        self._log_request(method, url, response.status_code)
        return response

    def _log_request(self, method, url, status_code):
        print(f"[{method}] {url} -> {status_code}")

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

# 使用
client = APIClient("https://jsonplaceholder.typicode.com", retry_times=3)
response = client.get("/posts/1")
# 输出: [GET] https://jsonplaceholder.typicode.com/posts/1 -> 200
```
**验收标准**：
- [ ] 支持五种 HTTP 方法
- [ ] 自动重试机制正常工作
- [ ] 请求日志正确记录
- [ ] 超时配置生效

---

**练习10：业务 API 封装**

**场景说明**：将通用的 API 客户端扩展为具体的业务 API 类，如用户 API、订单 API。
**具体需求**：
1. 创建 `UserAPI` 类封装用户相关接口（登录、获取信息、更新、登出）
2. 登录成功后自动保存 Token 到请求头
3. 创建 `OrderAPI` 类封装订单相关接口（创建、查询、列表）
4. 支持共享 Session 实现状态共享
5. 业务方法返回 Response 对象
**使用示例**：
```python
import requests

class UserAPI:
    """用户 API 封装"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def login(self, username, password):
        """登录"""
        response = self.session.post(
            f"{self.base_url}/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.session.headers["Authorization"] = f"Bearer {self.token}"
        return response

    def get_profile(self):
        """获取用户信息"""
        return self.session.get(f"{self.base_url}/user/profile")

    def logout(self):
        """登出"""
        response = self.session.post(f"{self.base_url}/logout")
        self.token = None
        self.session.headers.pop("Authorization", None)
        return response

# 使用
user_api = UserAPI("https://api.example.com")
login_resp = user_api.login("admin", "123456")
print(login_resp.status_code)  # 200

profile_resp = user_api.get_profile()
print(profile_resp.json()["username"])  # admin
```
**验收标准**：
- [ ] UserAPI 类正确封装用户接口
- [ ] 登录后自动保存 Token
- [ ] 业务方法返回正确的 Response
- [ ] 能共享 Session 状态

---

**练习11：Token 认证**

**场景说明**：大多数 API 需要认证，Token 认证是最常见的方式。
**具体需求**：
1. 实现 `TokenAuth` 类管理 Token 认证
2. `login()` 方法获取 Token 并保存到请求头
3. `request()` 方法检查 Token 是否存在
4. Token 过期（401 状态码）时抛出异常提示重新登录
5. 所有认证请求自动携带 Authorization 头
**使用示例**：
```python
import requests

class TokenAuth:
    """Token 认证管理"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def login(self, username, password):
        """登录获取 Token"""
        response = self.session.post(
            f"{self.base_url}/api/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json()["token"]
            self.session.headers["Authorization"] = f"Bearer {self.token}"
        return response

    def request(self, method, endpoint, **kwargs):
        """带认证的请求"""
        if not self.token:
            raise Exception("请先登录")

        response = self.session.request(
            method, f"{self.base_url}{endpoint}", **kwargs
        )

        # Token 过期处理
        if response.status_code == 401:
            raise Exception("Token 已过期，请重新登录")

        return response

# 使用
auth = TokenAuth("https://api.example.com")
auth.login("admin", "123456")
profile_resp = auth.request("GET", "/api/user/profile")
print(profile_resp.status_code)  # 200
```

**练习12：API 签名**

**场景说明**：许多开放平台 API（如支付宝、微信、阿里云）要求请求必须携带签名，用于验证请求的合法性和完整性，防止请求被篡改。

**具体需求**：
1. 实现 `SignedAPI` 类，支持 API 签名机制
2. 签名算法：将参数按 key 排序，拼接成字符串，加入密钥和时间戳，计算 MD5
3. 每个请求自动添加公共参数：`app_id`、`timestamp`、`sign`
4. 支持 GET 和 POST 请求的签名处理
5. 可选：实现 HMAC-SHA256 签名方式

**使用示例**：
```python
import hashlib
import hmac
import time
import requests

class SignedAPI:
    """带签名的 API 客户端"""

    def __init__(self, base_url, app_id, app_secret):
        self.base_url = base_url
        self.app_id = app_id
        self.app_secret = app_secret
        self.session = requests.Session()

    def _generate_sign(self, params, timestamp):
        """生成签名"""
        # 1. 参数排序
        sorted_params = sorted(params.items())
        # 2. 拼接字符串
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        # 3. 加入密钥和时间戳
        sign_str = f"{param_str}&timestamp={timestamp}&secret={self.app_secret}"
        # 4. MD5 签名
        return hashlib.md5(sign_str.encode()).hexdigest().upper()

    def _generate_hmac_sign(self, params, timestamp):
        """生成 HMAC-SHA256 签名"""
        sorted_params = sorted(params.items())
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        sign_str = f"{param_str}&timestamp={timestamp}"
        return hmac.new(
            self.app_secret.encode(),
            sign_str.encode(),
            hashlib.sha256
        ).hexdigest().upper()

    def request(self, method, endpoint, params=None):
        """带签名的请求"""
        params = params or {}
        timestamp = int(time.time())

        # 添加公共参数
        params["app_id"] = self.app_id
        params["timestamp"] = timestamp
        params["sign"] = self._generate_sign(params, timestamp)

        url = f"{self.base_url}{endpoint}"
        if method.upper() == "GET":
            return self.session.get(url, params=params)
        else:
            return self.session.request(method, url, json=params)

# 使用示例
api = SignedAPI(
    base_url="https://api.example.com",
    app_id="your_app_id",
    app_secret="your_app_secret"
)

# 发送带签名的请求
response = api.request("GET", "/user/info", {"user_id": 123})
print(response.status_code)
print(response.json())

# 验证签名生成逻辑
sign = api._generate_sign({"user_id": 123, "app_id": "test"}, 1704067200)
print(f"签名: {sign}")
```

**验收标准**：
- [ ] 能正确实现参数排序和拼接
- [ ] 能生成正确的 MD5 签名
- [ ] 请求自动携带 app_id、timestamp、sign 参数
- [ ] GET 和 POST 请求都能正确签名
- [ ] 可选：实现 HMAC-SHA256 签名

**练习13：文件下载**

**场景说明**：在接口测试中，经常需要下载测试报告、导出数据文件或验证文件下载接口的功能。

**具体需求**：
1. 实现下载文件到内存的方法（适用于小文件）
2. 实现下载文件保存到本地的方法（使用流式下载，适用于大文件）
3. 实现带进度条显示的下载方法
4. 使用 `stream=True` 参数进行流式下载
5. 使用 `response.iter_content()` 分块读取内容

**使用示例**：
```python
import requests
from pathlib import Path

def download_to_memory(url):
    """下载文件到内存"""
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def download_to_file(url, save_path):
    """下载文件保存到本地（流式下载）"""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return Path(save_path).exists()

def download_with_progress(url, save_path):
    """带进度条的下载"""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                progress = downloaded / total_size * 100
                print(f"\r下载进度: {progress:.1f}%", end="")

    print("\n下载完成")
    return downloaded

# 使用示例
if __name__ == "__main__":
    # 下载到内存
    content = download_to_memory("https://httpbin.org/bytes/1024")
    print(f"下载到内存: {len(content)} bytes")

    # 下载到文件
    success = download_to_file("https://httpbin.org/image/png", "/tmp/test_image.png")
    print(f"下载到文件: {'成功' if success else '失败'}")

    # 带进度条下载
    size = download_with_progress(
        "https://httpbin.org/bytes/102400",
        "/tmp/test_file.bin"
    )
    print(f"下载大小: {size} bytes")

    # 清理测试文件
    Path("/tmp/test_image.png").unlink(missing_ok=True)
    Path("/tmp/test_file.bin").unlink(missing_ok=True)
```

**验收标准**：
- [ ] 能正确下载文件到内存
- [ ] 能使用流式下载保存大文件
- [ ] 能实现进度条显示功能
- [ ] 理解 `stream=True` 的作用
- [ ] 下载完成后能正确清理临时文件

**练习14：数据驱动接口测试**

**场景说明**：在接口测试中，需要用多组数据验证同一个接口，使用数据驱动可以将测试数据与测试代码分离，提高测试覆盖率。

**具体需求**：
1. 实现从 CSV 文件读取测试数据的方法
2. 实现从 JSON 文件读取测试数据的方法
3. 使用 `@pytest.mark.parametrize` 实现参数化测试
4. 测试数据与测试代码分离，便于维护
5. 支持动态加载测试数据

**使用示例**：
```python
import pytest
import csv
import json
import requests
from pathlib import Path

def load_csv_data(filepath):
    """从 CSV 加载测试数据"""
    test_data = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_data.append(row)
    return test_data

def load_json_data(filepath):
    """从 JSON 加载测试数据"""
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

# 准备测试数据文件
# tests/data/login_data.csv 内容：
# username,password,expected_status
# admin,123456,200
# admin,wrong,401
# ,123456,400
# guest,123456,403

# tests/data/users.json 内容：
# [
#   {"name": "user1", "email": "user1@test.com"},
#   {"name": "user2", "email": "user2@test.com"}
# ]

# 使用 CSV 数据进行参数化测试
@pytest.mark.parametrize("data", load_csv_data("tests/data/login_data.csv"))
def test_login_csv(data):
    """使用 CSV 数据测试登录接口"""
    response = requests.post(
        "https://api.example.com/login",
        json={
            "username": data["username"],
            "password": data["password"]
        }
    )
    assert response.status_code == int(data["expected_status"])

# 使用 JSON 数据进行参数化测试
@pytest.mark.parametrize("user", load_json_data("tests/data/users.json"))
def test_create_user_json(user):
    """使用 JSON 数据测试创建用户接口"""
    response = requests.post(
        "https://api.example.com/users",
        json=user
    )
    assert response.status_code == 201

# 使用 pytest.fixture 加载数据
@pytest.fixture
def login_test_data():
    """登录测试数据 fixture"""
    return load_csv_data("tests/data/login_data.csv")

def test_login_with_fixture(login_test_data):
    """使用 fixture 加载测试数据"""
    for data in login_test_data:
        response = requests.post(
            "https://api.example.com/login",
            json={"username": data["username"], "password": data["password"]}
        )
        assert response.status_code == int(data["expected_status"])

# 运行命令：
# pytest tests/test_data_driven.py -v
```

**验收标准**：
- [ ] 能从 CSV 文件正确读取测试数据
- [ ] 能从 JSON 文件正确读取测试数据
- [ ] 能使用 `@pytest.mark.parametrize` 实现参数化
- [ ] 测试数据文件格式正确
- [ ] 测试用例能正确使用数据驱动执行

**练习15：链式接口测试**

**场景说明**：在实际业务中，接口往往存在依赖关系，如"登录 -> 创建订单 -> 支付 -> 查询订单"是一个完整的业务流程，需要验证整个链路的正确性。

**具体需求**：
1. 实现完整的业务流程测试：登录 -> 创建订单 -> 支付 -> 查询订单状态
2. 上一步的响应数据作为下一步的输入（如订单 ID）
3. 使用 pytest fixture 管理登录状态
4. 每个步骤都要有断言验证
5. 使用 Allure 记录测试步骤

**使用示例**：
```python
import pytest
import requests
import allure

# ============================================
# Fixture 配置
# ============================================
@pytest.fixture
def api_client():
    """创建 API 客户端"""
    session = requests.Session()
    session.base_url = "https://api.example.com"
    yield session
    session.close()

@pytest.fixture
def logged_in_client(api_client):
    """登录后的客户端（自动处理登录）"""
    response = api_client.post(
        f"{api_client.base_url}/login",
        json={"username": "admin", "password": "123456"}
    )
    assert response.status_code == 200, "登录失败"
    token = response.json()["token"]
    api_client.headers["Authorization"] = f"Bearer {token}"
    return api_client

# ============================================
# 链式接口测试
# ============================================
@allure.feature("订单管理")
@allure.story("订单流程")
class TestOrderFlow:

    @allure.title("完整订单流程测试：创建-支付-查询")
    def test_complete_order_flow(self, logged_in_client):
        """完整订单流程测试：登录 -> 创建订单 -> 支付 -> 查询"""

        # 步骤1：创建订单
        with allure.step("步骤1：创建订单"):
            order_data = {"product_id": 1, "quantity": 2}
            create_resp = logged_in_client.post(
                f"{logged_in_client.base_url}/orders",
                json=order_data
            )
            allure.attach(str(order_data), name="订单数据", attachment_type=allure.attachment_type.JSON)
            assert create_resp.status_code == 201, f"创建订单失败: {create_resp.text}"
            order_id = create_resp.json()["order_id"]
            allure.attach(f"订单ID: {order_id}", name="创建结果")

        # 步骤2：支付订单
        with allure.step("步骤2：支付订单"):
            pay_data = {"payment_method": "credit_card"}
            pay_resp = logged_in_client.post(
                f"{logged_in_client.base_url}/orders/{order_id}/pay",
                json=pay_data
            )
            assert pay_resp.status_code == 200, f"支付失败: {pay_resp.text}"
            assert pay_resp.json()["payment_status"] == "success"

        # 步骤3：查询订单状态
        with allure.step("步骤3：查询订单状态"):
            status_resp = logged_in_client.get(
                f"{logged_in_client.base_url}/orders/{order_id}"
            )
            assert status_resp.status_code == 200
            order_status = status_resp.json()["status"]
            assert order_status == "paid", f"订单状态异常: {order_status}"
            allure.attach(str(status_resp.json()), name="订单详情")

    @allure.title("订单取消流程测试")
    def test_cancel_order_flow(self, logged_in_client):
        """订单取消流程：创建订单 -> 取消订单 -> 验证状态"""

        # 创建订单
        create_resp = logged_in_client.post(
            f"{logged_in_client.base_url}/orders",
            json={"product_id": 2, "quantity": 1}
        )
        assert create_resp.status_code == 201
        order_id = create_resp.json()["order_id"]

        # 取消订单
        cancel_resp = logged_in_client.post(
            f"{logged_in_client.base_url}/orders/{order_id}/cancel"
        )
        assert cancel_resp.status_code == 200

        # 验证状态
        status_resp = logged_in_client.get(
            f"{logged_in_client.base_url}/orders/{order_id}"
        )
        assert status_resp.json()["status"] == "cancelled"

# 运行命令：
# pytest tests/test_chain_api.py --alluredir=reports/allure-results -v
```

**验收标准**：
- [ ] 能使用 fixture 管理登录状态
- [ ] 链式接口测试中，上一步的输出能作为下一步的输入
- [ ] 每个步骤都有明确的断言
- [ ] 使用 Allure 记录测试步骤
- [ ] 测试失败时能准确定位到哪个步骤出错

**练习16：接口测试报告**

**场景说明**：在接口自动化测试中，需要生成详细的测试报告，记录请求参数、响应数据、测试步骤，便于问题定位和测试结果展示。

**具体需求**：
1. 使用 Allure 框架生成测试报告
2. 使用 `@allure.feature` 和 `@allure.story` 组织测试用例
3. 使用 `allure.attach` 记录请求和响应数据
4. 使用 `allure.step` 添加步骤说明
5. 使用 `@allure.title` 设置测试用例标题

**使用示例**：
```python
import allure
import pytest
import requests
import json

# ============================================
# 用户管理接口测试（带 Allure 报告）
# ============================================
@allure.feature("用户管理")
@allure.link(url="https://api-docs.example.com/user", name="接口文档")
class TestUserAPI:

    @allure.story("用户登录")
    @allure.title("用户登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self):
        """测试用户登录成功场景"""

        with allure.step("步骤1：准备登录数据"):
            login_data = {"username": "admin", "password": "123456"}
            # 记录请求数据（隐藏敏感信息）
            safe_data = {"username": "admin", "password": "******"}
            allure.attach(
                json.dumps(safe_data, ensure_ascii=False, indent=2),
                name="请求数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("步骤2：发送登录请求"):
            response = requests.post(
                "https://api.example.com/login",
                json=login_data
            )
            # 记录响应数据
            allure.attach(
                response.text,
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("步骤3：验证响应结果"):
            assert response.status_code == 200, f"登录失败，状态码: {response.status_code}"
            response_data = response.json()
            assert "token" in response_data, "响应中缺少 token"
            allure.attach(f"Token: {response_data['token'][:20]}...", name="认证令牌")

    @allure.story("用户登录")
    @allure.title("用户登录失败-密码错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self):
        """测试密码错误场景"""

        with allure.step("发送错误的登录请求"):
            response = requests.post(
                "https://api.example.com/login",
                json={"username": "admin", "password": "wrong_password"}
            )
            allure.attach(response.text, name="响应数据")

        with allure.step("验证返回错误信息"):
            assert response.status_code == 401
            assert response.json()["error"] == "密码错误"

    @allure.story("用户信息")
    @allure.title("获取用户信息")
    def test_get_user_profile(self):
        """测试获取用户信息"""

        with allure.step("步骤1：登录获取 Token"):
            login_resp = requests.post(
                "https://api.example.com/login",
                json={"username": "admin", "password": "123456"}
            )
            token = login_resp.json()["token"]

        with allure.step("步骤2：获取用户信息"):
            response = requests.get(
                "https://api.example.com/user/profile",
                headers={"Authorization": f"Bearer {token}"}
            )
            allure.attach(response.text, name="用户信息")

        with allure.step("步骤3：验证用户信息"):
            assert response.status_code == 200
            user_data = response.json()
            assert "username" in user_data
            assert "email" in user_data

# 运行命令：
# pytest tests/test_with_allure.py --alluredir=reports/allure-results -v
# 生成报告：
# allure serve reports/allure-results
```

**验收标准**：
- [ ] 能正确配置 Allure 报告
- [ ] 能使用 `@allure.feature` 和 `@allure.story` 组织用例
- [ ] 能使用 `allure.attach` 记录请求和响应
- [ ] 能使用 `allure.step` 添加步骤说明
- [ ] 测试报告清晰展示测试过程和结果

### 综合练习（17-20）

---

**练习17：完整 API 测试框架**

**场景说明**：企业级接口测试需要一个完整的测试框架，包含配置管理、API 封装、测试用例、工具函数等模块。

**具体需求**：
1. 搭建分层架构：配置层、API 层、测试层、工具层
2. 实现基础 API 客户端，支持重试、超时、日志
3. 封装业务 API（用户 API、订单 API）
4. 使用 pytest fixture 管理测试资源
5. 支持环境配置切换（dev/test/prod）

**使用示例**：
```
项目结构：
api_test_framework/
├── config/
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── dev.yaml           # 开发环境配置
│   └── test.yaml          # 测试环境配置
├── api/
│   ├── __init__.py
│   ├── client.py          # 基础客户端
│   ├── user_api.py        # 用户 API
│   └── order_api.py       # 订单 API
├── tests/
│   ├── conftest.py        # pytest 配置
│   ├── test_user.py       # 用户测试
│   └── test_order.py      # 订单测试
├── utils/
│   ├── __init__.py
│   ├── data_loader.py     # 数据加载
│   └── logger.py          # 日志工具
├── pytest.ini
└── requirements.txt
```

```python
# config/config.py - 配置管理
import yaml
from pathlib import Path

class Config:
    """配置管理类"""
    def __init__(self, env="dev"):
        config_file = Path(__file__).parent / f"{env}.yaml"
        with open(config_file, encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

    @property
    def base_url(self):
        return self._config["base_url"]

    @property
    def timeout(self):
        return self._config.get("timeout", 30)

# api/client.py - 基础客户端
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    """完整的 API 客户端"""

    def __init__(self, base_url, timeout=30, retry_times=3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self._setup_retry(retry_times)

    def _setup_retry(self, retry_times):
        retry = Retry(total=retry_times, backoff_factor=0.5,
                      status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        print(f"[{method}] {url} -> {response.status_code}")
        return response

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

# api/user_api.py - 用户 API
class UserAPI(APIClient):
    """用户相关 API"""

    def login(self, username, password):
        return self.post("/api/login", json={"username": username, "password": password})

    def get_profile(self):
        return self.get("/api/user/profile")

    def logout(self):
        return self.post("/api/logout")

# tests/conftest.py - Pytest 配置
import pytest
from config.config import Config
from api.user_api import UserAPI
from api.order_api import OrderAPI

@pytest.fixture(scope="session")
def config():
    return Config(env="test")

@pytest.fixture(scope="session")
def api_client(config):
    return APIClient(config.base_url, config.timeout)

@pytest.fixture
def user_api(config):
    return UserAPI(config.base_url)

@pytest.fixture
def auth_token(user_api):
    response = user_api.login("admin", "123456")
    return response.json()["token"]
```

**验收标准**：
- [ ] 项目结构清晰，分层合理
- [ ] 基础客户端支持重试、超时、日志
- [ ] 业务 API 封装完整
- [ ] 使用 fixture 管理测试资源
- [ ] 支持环境配置切换

**练习18：接口自动化测试套件**

**场景说明**：针对一个完整的业务系统，编写全面的接口测试套件，覆盖用户管理和订单管理的所有核心接口。

**具体需求**：
1. 实现完整的用户 CRUD 测试（创建、查询、更新、删除）
2. 实现完整的订单流程测试（创建、支付、查询、取消）
3. 使用 Allure 生成测试报告
4. 测试用例分类：正向用例、异常用例、边界用例
5. 使用 pytest marker 标记测试用例

**使用示例**：
```python
import allure
import pytest
import requests

# ============================================
# 用户管理测试套件
# ============================================
@allure.feature("用户管理")
class TestUserSuite:

    @allure.story("用户认证")
    @allure.title("用户登录成功")
    @pytest.mark.smoke
    def test_login_success(self, user_api):
        """测试登录成功"""
        with allure.step("发送登录请求"):
            response = user_api.login("admin", "123456")
            allure.attach(response.text, name="响应数据")
        with allure.step("验证登录结果"):
            assert response.status_code == 200
            assert "token" in response.json()

    @allure.story("用户认证")
    @allure.title("用户登录失败-密码错误")
    @pytest.mark.negative
    def test_login_fail(self, user_api):
        """测试登录失败"""
        response = user_api.login("admin", "wrong_password")
        assert response.status_code == 401

    @allure.story("用户信息")
    @allure.title("获取用户信息")
    @pytest.mark.smoke
    def test_get_profile(self, user_api, auth_token):
        """测试获取用户信息"""
        user_api.session.headers["Authorization"] = f"Bearer {auth_token}"
        response = user_api.get_profile()
        assert response.status_code == 200
        assert "username" in response.json()

    @allure.story("用户信息")
    @allure.title("更新用户信息")
    @pytest.mark.regression
    def test_update_profile(self, user_api, auth_token):
        """测试更新用户信息"""
        user_api.session.headers["Authorization"] = f"Bearer {auth_token}"
        update_data = {"nickname": "新昵称", "email": "new@example.com"}
        response = user_api.update_profile(update_data)
        assert response.status_code == 200

# ============================================
# 订单管理测试套件
# ============================================
@allure.feature("订单管理")
class TestOrderSuite:

    @allure.story("订单流程")
    @allure.title("创建订单")
    @pytest.mark.smoke
    def test_create_order(self, order_api, auth_token):
        """测试创建订单"""
        order_api.session.headers["Authorization"] = f"Bearer {auth_token}"
        order_data = {"product_id": 1, "quantity": 2}
        response = order_api.create_order(order_data)
        assert response.status_code == 201
        assert "order_id" in response.json()

    @allure.story("订单流程")
    @allure.title("支付订单")
    @pytest.mark.regression
    def test_pay_order(self, order_api, auth_token):
        """测试支付订单"""
        order_api.session.headers["Authorization"] = f"Bearer {auth_token}"
        # 先创建订单
        create_resp = order_api.create_order({"product_id": 1, "quantity": 1})
        order_id = create_resp.json()["order_id"]
        # 支付订单
        pay_resp = order_api.pay_order(order_id, {"payment_method": "credit_card"})
        assert pay_resp.status_code == 200

    @allure.story("订单流程")
    @allure.title("查询订单")
    def test_query_order(self, order_api, auth_token):
        """测试查询订单"""
        order_api.session.headers["Authorization"] = f"Bearer {auth_token}"
        response = order_api.get_orders()
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @allure.story("订单流程")
    @allure.title("取消订单")
    @pytest.mark.negative
    def test_cancel_order(self, order_api, auth_token):
        """测试取消订单"""
        order_api.session.headers["Authorization"] = f"Bearer {auth_token}"
        # 先创建订单
        create_resp = order_api.create_order({"product_id": 1, "quantity": 1})
        order_id = create_resp.json()["order_id"]
        # 取消订单
        cancel_resp = order_api.cancel_order(order_id)
        assert cancel_resp.status_code == 200

# 运行命令：
# pytest tests/test_complete_suite.py --alluredir=reports/allure-results -v
# 只运行冒烟测试：pytest -m smoke tests/
```

**验收标准**：
- [ ] 用户 CRUD 测试用例完整
- [ ] 订单流程测试用例完整
- [ ] 使用 pytest marker 分类测试用例
- [ ] 使用 Allure 生成测试报告
- [ ] 包含正向和异常测试用例

**练习19：接口性能测试**

**场景说明**：在接口测试中，除了验证功能正确性，还需要验证接口的响应时间和并发处理能力。

**具体需求**：
1. 测试接口响应时间，验证是否在预期范围内
2. 使用 `concurrent.futures` 实现并发请求测试
3. 统计接口响应时间的 P50、P90、P99 指标
4. 使用 pytest-xdist 实现分布式并发测试
5. 生成性能测试报告

**使用示例**：
```python
import pytest
import requests
import time
import concurrent.futures
from statistics import mean, median

# ============================================
# 响应时间测试
# ============================================
@pytest.mark.parametrize("endpoint", [
    "/posts",
    "/comments",
    "/users",
])
def test_response_time(endpoint):
    """测试接口响应时间"""
    url = f"https://jsonplaceholder.typicode.com{endpoint}"

    # 多次请求取平均值
    response_times = []
    for _ in range(5):
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        response_times.append(end_time - start_time)

    avg_time = mean(response_times)
    print(f"\n{endpoint} 响应时间统计:")
    print(f"  平均: {avg_time:.3f}s")
    print(f"  最小: {min(response_times):.3f}s")
    print(f"  最大: {max(response_times):.3f}s")

    assert response.status_code == 200
    assert avg_time < 2.0, f"响应时间超过 2 秒: {avg_time:.3f}s"

# ============================================
# 并发请求测试
# ============================================
def test_concurrent_requests():
    """测试并发请求处理能力"""
    url = "https://jsonplaceholder.typicode.com/posts/1"
    num_requests = 20

    def make_request(i):
        start = time.time()
        response = requests.get(url)
        end = time.time()
        return {"status": response.status_code, "time": end - start}

    # 使用线程池并发请求
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, i) for i in range(num_requests)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    # 统计结果
    success_count = sum(1 for r in results if r["status"] == 200)
    times = sorted([r["time"] for r in results])

    print(f"\n并发测试结果:")
    print(f"  总请求数: {num_requests}")
    print(f"  成功数: {success_count}")
    print(f"  成功率: {success_count/num_requests*100:.1f}%")
    print(f"  P50: {times[len(times)//2]:.3f}s")
    print(f"  P90: {times[int(len(times)*0.9)]:.3f}s")
    print(f"  P99: {times[int(len(times)*0.99)]:.3f}s")

    assert success_count == num_requests, f"部分请求失败: {success_count}/{num_requests}"
    assert times[int(len(times)*0.9)] < 3.0, "P90 响应时间超过 3 秒"

# ============================================
# 接口压力测试
# ============================================
@pytest.mark.slow
def test_stress_test():
    """接口压力测试"""
    url = "https://jsonplaceholder.typicode.com/posts"
    durations = []

    # 持续发送请求 10 秒
    start_time = time.time()
    request_count = 0
    while time.time() - start_time < 10:
        resp = requests.get(url)
        durations.append(resp.elapsed.total_seconds())
        request_count += 1

    print(f"\n压力测试结果:")
    print(f"  总请求数: {request_count}")
    print(f"  QPS: {request_count/10:.1f}")
    print(f"  平均响应时间: {mean(durations):.3f}s")

    assert request_count > 50, "QPS 过低"

# 运行命令：
# 普通运行：pytest tests/test_performance.py -v -s
# 并发运行（4个进程）：pytest -n 4 tests/test_performance.py -v
```

**验收标准**：
- [ ] 能正确测量接口响应时间
- [ ] 能使用线程池实现并发请求
- [ ] 能计算 P50、P90、P99 响应时间指标
- [ ] 能使用 pytest-xdist 进行分布式测试
- [ ] 测试结果包含详细的性能数据

**练习20：接口测试最佳实践项目**

**场景说明**：整合本周所学知识，搭建一个企业级的接口自动化测试项目，具备完整的分层架构、数据驱动、环境切换和 CI/CD 集成能力。

**具体需求**：
1. 分层设计：API 层（基础客户端）、业务层（业务 API）、测试层（测试用例）
2. 数据驱动：支持 YAML/JSON/CSV 多种格式的测试数据文件
3. 环境切换：支持 dev/test/prod 环境配置
4. 报告生成：Allure 报告 + 钉钉/邮件通知
5. CI/CD 集成：提供 Jenkins/GitHub Actions 配置示例

**项目结构**：
```
api_automation/
├── config/
│   ├── config.dev.yaml      # 开发环境配置
│   ├── config.test.yaml     # 测试环境配置
│   └── config.prod.yaml     # 生产环境配置
├── api/
│   ├── __init__.py
│   ├── base_client.py       # 基础 API 客户端
│   ├── user_api.py          # 用户相关 API
│   ├── order_api.py         # 订单相关 API
│   └── auth.py              # 认证模块
├── tests/
│   ├── conftest.py          # Pytest 配置和 fixture
│   ├── test_user/
│   │   ├── test_login.py    # 登录测试
│   │   └── test_profile.py  # 用户信息测试
│   ├── test_order/
│   │   ├── test_create.py   # 创建订单测试
│   │   └── test_flow.py     # 订单流程测试
│   └── data/
│       ├── login.csv        # 登录测试数据
│       └── users.json       # 用户测试数据
├── utils/
│   ├── data_loader.py       # 数据加载工具
│   ├── logger.py            # 日志工具
│   └── notification.py      # 通知工具
├── reports/
│   └── allure-results/      # Allure 报告目录
├── pytest.ini               # Pytest 配置文件
├── conftest.py              # 全局配置
├── requirements.txt         # 依赖包
└── README.md                # 项目说明
```

**核心代码示例**：
```python
# config/config.test.yaml
base_url: "https://test-api.example.com"
timeout: 30
retry_times: 3
notification:
  dingtalk_webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
  email:
    smtp_server: "smtp.example.com"
    recipients: ["qa@example.com"]

# api/base_client.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class BaseClient:
    """基础 API 客户端"""

    def __init__(self, config):
        self.base_url = config["base_url"]
        self.timeout = config["timeout"]
        self.session = requests.Session()
        self._setup_retry(config.get("retry_times", 3))

    def _setup_retry(self, retry_times):
        retry = Retry(total=retry_times, backoff_factor=0.5,
                     status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        return response

# utils/data_loader.py
import yaml
import json
import csv

def load_yaml(filepath):
    """加载 YAML 配置"""
    with open(filepath, encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_json(filepath):
    """加载 JSON 数据"""
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def load_csv(filepath):
    """加载 CSV 数据"""
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

# conftest.py
import pytest
import yaml
from pathlib import Path

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help="环境: dev/test/prod")

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    config_path = Path(f"config/config.{env}.yaml")
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def api_client(config):
    from api.base_client import BaseClient
    return BaseClient(config)
```

**运行命令**：
```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试（测试环境）
pytest --env=test --alluredir=reports/allure-results

# 运行测试（开发环境）
pytest --env=dev --alluredir=reports/allure-results

# 生成 Allure 报告
allure serve reports/allure-results

# 并发运行
pytest -n 4 --env=test --alluredir=reports/allure-results
```

**验收标准**：
- [ ] 项目结构清晰，分层合理
- [ ] 支持 dev/test/prod 环境切换
- [ ] 支持 YAML/JSON/CSV 数据驱动
- [ ] Allure 报告生成正确
- [ ] 包含 CI/CD 配置示例
- [ ] README 文档完整

---

## 五、本周小结

1. **Requests**：Python 接口测试的标准库
2. **Session**：保持登录状态的核心
3. **封装设计**：让测试代码更易维护
4. **认证处理**：企业级接口必备

### 下周预告

第7周学习数据库测试和 Mock 技术。
