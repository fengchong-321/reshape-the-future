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

#### 练习1：GET 请求基础

```python
# tests/test_get_requests.py
# 要求：
# 1. 使用 requests.get 发送 GET 请求
# 2. 获取响应状态码、响应体、响应头
# 3. 使用 params 传递查询参数

import requests

def test_basic_get():
    """基础 GET 请求"""
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    # 验证状态码
    # 验证响应体
    pass

def test_get_with_params():
    """带参数的 GET 请求"""
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        params={"userId": 1}
    )
    # 验证返回数据
    pass

def test_get_with_headers():
    """带请求头的 GET 请求"""
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        headers={"Accept": "application/json"}
    )
    pass
```

#### 练习2：POST 请求基础

```python
# tests/test_post_requests.py
# 要求：
# 1. 使用 requests.post 发送 JSON 数据
# 2. 使用 requests.post 发送表单数据
# 3. 验证响应数据

import requests

def test_post_json():
    """发送 JSON 数据"""
    response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json={"title": "测试", "body": "内容", "userId": 1}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "测试"

def test_post_form():
    """发送表单数据"""
    response = requests.post(
        "https://httpbin.org/post",
        data={"username": "admin", "password": "123456"}
    )
    assert response.status_code == 200
```

#### 练习3：响应处理

```python
# tests/test_response.py
# 要求：
# 1. 解析 JSON 响应
# 2. 获取响应头信息
# 3. 处理不同状态码

import requests

def test_parse_json():
    """解析 JSON 响应"""
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    data = response.json()
    # 验证 JSON 字段
    assert "id" in data
    assert "title" in data

def test_response_headers():
    """获取响应头"""
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    content_type = response.headers.get("Content-Type")
    assert "application/json" in content_type

def test_status_codes():
    """测试不同状态码"""
    # 200 OK
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
    assert response.ok is True

    # 404 Not Found
    response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
    assert response.status_code == 404
```

#### 练习4：PUT/PATCH/DELETE 请求

```python
# tests/test_http_methods.py
# 要求：
# 1. 使用 PUT 完整更新资源
# 2. 使用 PATCH 部分更新资源
# 3. 使用 DELETE 删除资源

import requests

def test_put_request():
    """PUT 请求 - 完整更新"""
    response = requests.put(
        "https://jsonplaceholder.typicode.com/posts/1",
        json={"id": 1, "title": "更新标题", "body": "更新内容", "userId": 1}
    )
    assert response.status_code == 200

def test_patch_request():
    """PATCH 请求 - 部分更新"""
    response = requests.patch(
        "https://jsonplaceholder.typicode.com/posts/1",
        json={"title": "只更新标题"}
    )
    assert response.status_code == 200

def test_delete_request():
    """DELETE 请求"""
    response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
    assert response.status_code == 200
```

#### 练习5：Session 管理基础

```python
# tests/test_session.py
# 要求：
# 1. 创建 requests.Session 对象
# 2. 使用 Session 发送多个请求
# 3. 设置全局请求头

import requests

def test_session_basic():
    """Session 基础用法"""
    session = requests.Session()

    # 设置全局请求头
    session.headers.update({"User-Agent": "MyTestClient/1.0"})

    # 发送多个请求
    response1 = session.get("https://jsonplaceholder.typicode.com/posts/1")
    response2 = session.get("https://jsonplaceholder.typicode.com/posts/2")

    assert response1.status_code == 200
    assert response2.status_code == 200

def test_session_cookies():
    """Session Cookie 管理"""
    session = requests.Session()

    # 发送请求获取 Cookie
    response = session.get("https://httpbin.org/cookies/set/test_cookie/test_value")

    # 后续请求自动携带 Cookie
    response = session.get("https://httpbin.org/cookies")
    assert "test_cookie" in response.json()["cookies"]
```

#### 练习6：超时和异常处理

```python
# tests/test_timeout.py
# 要求：
# 1. 设置请求超时
# 2. 捕获超时异常
# 3. 捕获连接异常

import requests
import pytest

def test_request_timeout():
    """测试超时设置"""
    # 设置 5 秒超时
    response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=5)
    assert response.status_code == 200

def test_timeout_exception():
    """测试超时异常"""
    with pytest.raises(requests.exceptions.Timeout):
        # 设置极短超时，预期超时
        requests.get("https://httpbin.org/delay/5", timeout=0.1)

def test_connection_error():
    """测试连接异常"""
    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get("https://this-domain-does-not-exist-12345.com")

def test_raise_for_status():
    """使用 raise_for_status"""
    response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
    with pytest.raises(requests.exceptions.HTTPError):
        response.raise_for_status()
```

#### 练习7：基础 API 客户端封装

```python
# api/client.py
# 要求：
# 1. 创建 APIClient 基类
# 2. 封装 get/post 方法
# 3. 支持超时配置

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
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        return response

    def post(self, endpoint, **kwargs):
        """POST 请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, timeout=self.timeout, **kwargs)
        return response

# tests/test_client.py
def test_api_client():
    client = APIClient("https://jsonplaceholder.typicode.com")
    response = client.get("/posts/1")
    assert response.status_code == 200
```

#### 练习8：文件上传基础

```python
# tests/test_file_upload.py
# 要求：
# 1. 上传单个文件
# 2. 设置文件名和 MIME 类型
# 3. 上传文件同时传递其他参数

import requests
import tempfile
import os

def test_upload_single_file():
    """上传单个文件"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("test content")
        temp_path = f.name

    try:
        files = {"file": open(temp_path, "rb")}
        response = requests.post("https://httpbin.org/post", files=files)
        assert response.status_code == 200
    finally:
        os.unlink(temp_path)

def test_upload_with_filename():
    """指定文件名和类型上传"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("test content")
        temp_path = f.name

    try:
        files = {"file": ("custom_name.txt", open(temp_path, "rb"), "text/plain")}
        response = requests.post("https://httpbin.org/post", files=files)
        assert response.status_code == 200
    finally:
        os.unlink(temp_path)
```

### 进阶练习（9-16）

#### 练习9：完整 API 客户端封装

```python
# api/client.py
# 要求：
# 1. 支持 GET/POST/PUT/PATCH/DELETE 方法
# 2. 自动重试机制
# 3. 请求日志记录

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
        response = self.session.request(
            method, url, timeout=self.timeout, **kwargs
        )
        self._log_request(method, url, response.status_code)
        return response

    def _log_request(self, method, url, status_code):
        """记录请求日志"""
        print(f"[{method}] {url} -> {status_code}")

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)
```

#### 练习10：业务 API 封装

```python
# api/user_api.py
# 要求：
# 1. 创建 UserAPI 类封装用户相关接口
# 2. 实现登录、获取用户信息、更新用户等方法
# 3. 自动处理 Token

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

    def update_profile(self, data):
        """更新用户信息"""
        return self.session.put(f"{self.base_url}/user/profile", json=data)

    def logout(self):
        """登出"""
        response = self.session.post(f"{self.base_url}/logout")
        self.token = None
        self.session.headers.pop("Authorization", None)
        return response

# api/order_api.py
class OrderAPI:
    """订单 API 封装"""

    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def create_order(self, order_data):
        return self.session.post(f"{self.base_url}/orders", json=order_data)

    def get_order(self, order_id):
        return self.session.get(f"{self.base_url}/orders/{order_id}")

    def list_orders(self, status=None):
        params = {"status": status} if status else {}
        return self.session.get(f"{self.base_url}/orders", params=params)
```

#### 练习11：Token 认证

```python
# tests/test_token_auth.py
# 要求：
# 1. 实现登录获取 Token
# 2. 后续请求自动携带 Token
# 3. Token 过期自动重新登录

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

def test_token_auth():
    auth = TokenAuth("https://api.example.com")
    # 登录
    login_resp = auth.login("admin", "123456")
    assert login_resp.status_code == 200
    # 获取用户信息
    profile_resp = auth.request("GET", "/api/user/profile")
    assert profile_resp.status_code == 200
```

#### 练习12：API 签名

```python
# api/signed_client.py
# 要求：
# 1. 实现 API 签名生成
# 2. 参数排序后拼接
# 3. 使用 MD5 或 HMAC-SHA256 签名

import hashlib
import hmac
import time

class SignedAPI:
    """带签名的 API 客户端"""

    def __init__(self, base_url, app_id, app_secret):
        self.base_url = base_url
        self.app_id = app_id
        self.app_secret = app_secret

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

    def request(self, method, endpoint, params=None):
        """带签名的请求"""
        import requests

        params = params or {}
        timestamp = int(time.time())

        # 添加公共参数
        params["app_id"] = self.app_id
        params["timestamp"] = timestamp
        params["sign"] = self._generate_sign(params, timestamp)

        url = f"{self.base_url}{endpoint}"
        if method.upper() == "GET":
            return requests.get(url, params=params)
        else:
            return requests.request(method, url, json=params)
```

#### 练习13：文件下载

```python
# tests/test_file_download.py
# 要求：
# 1. 下载文件到内存
# 2. 下载文件保存到本地
# 3. 实现带进度条的下载

import requests
from pathlib import Path

def test_download_to_memory():
    """下载文件到内存"""
    response = requests.get("https://httpbin.org/image/png")
    assert response.status_code == 200
    content = response.content
    assert len(content) > 0

def test_download_to_file():
    """下载文件保存到本地"""
    response = requests.get("https://httpbin.org/image/png", stream=True)
    save_path = "/tmp/downloaded.png"

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    assert Path(save_path).exists()
    Path(save_path).unlink()  # 清理

def test_download_with_progress():
    """带进度条的下载"""
    url = "https://httpbin.org/bytes/102400"  # 100KB
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))

    downloaded = 0
    for chunk in response.iter_content(chunk_size=8192):
        downloaded += len(chunk)
        progress = downloaded / total_size * 100 if total_size > 0 else 0
        print(f"\r下载进度: {progress:.1f}%", end="")

    print("\n下载完成")
    assert downloaded == total_size
```

#### 练习14：数据驱动接口测试

```python
# tests/test_data_driven.py
# 要求：
# 1. 从 CSV 文件读取测试数据
# 2. 从 JSON 文件读取测试数据
# 3. 参数化执行测试

import pytest
import csv
import json

def load_csv_data(filepath):
    """从 CSV 加载测试数据"""
    test_data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_data.append(row)
    return test_data

def load_json_data(filepath):
    """从 JSON 加载测试数据"""
    with open(filepath) as f:
        return json.load(f)

# test_data/login_data.csv
# username,password,expected_status
# admin,123456,200
# admin,wrong,401
# ,123456,400

@pytest.mark.parametrize("data", load_csv_data("tests/data/login_data.csv"))
def test_login_csv(data):
    import requests
    response = requests.post(
        "https://api.example.com/login",
        json={"username": data["username"], "password": data["password"]}
    )
    assert response.status_code == int(data["expected_status"])

# test_data/users.json
# [{"name": "user1"}, {"name": "user2"}]

@pytest.mark.parametrize("user", load_json_data("tests/data/users.json"))
def test_create_user_json(user):
    import requests
    response = requests.post(
        "https://api.example.com/users",
        json=user
    )
    assert response.status_code == 201
```

#### 练习15：链式接口测试

```python
# tests/test_chain_api.py
# 要求：
# 1. 实现登录 -> 创建订单 -> 支付 -> 查询订单状态的链式测试
# 2. 上一步的响应作为下一步的输入
# 3. 使用 fixture 管理测试数据

import pytest
import requests

@pytest.fixture
def api_client():
    session = requests.Session()
    session.base_url = "https://api.example.com"
    return session

@pytest.fixture
def logged_in_client(api_client):
    """登录后的客户端"""
    response = api_client.post(
        f"{api_client.base_url}/login",
        json={"username": "admin", "password": "123456"}
    )
    token = response.json()["token"]
    api_client.headers["Authorization"] = f"Bearer {token}"
    return api_client

class TestOrderFlow:

    def test_complete_order_flow(self, logged_in_client):
        """完整订单流程测试"""

        # 步骤1：创建订单
        order_data = {"product_id": 1, "quantity": 2}
        create_resp = logged_in_client.post(
            f"{logged_in_client.base_url}/orders",
            json=order_data
        )
        assert create_resp.status_code == 201
        order_id = create_resp.json()["order_id"]

        # 步骤2：支付订单
        pay_resp = logged_in_client.post(
            f"{logged_in_client.base_url}/orders/{order_id}/pay",
            json={"payment_method": "credit_card"}
        )
        assert pay_resp.status_code == 200

        # 步骤3：查询订单状态
        status_resp = logged_in_client.get(
            f"{logged_in_client.base_url}/orders/{order_id}"
        )
        assert status_resp.status_code == 200
        assert status_resp.json()["status"] == "paid"
```

#### 练习16：接口测试报告

```python
# tests/test_with_allure.py
# 要求：
# 1. 使用 Allure 记录请求和响应
# 2. 添加步骤说明
# 3. 关联接口文档

import allure
import pytest
import requests

@allure.feature("用户管理")
class TestUserAPI:

    @allure.story("用户登录")
    @allure.title("用户登录成功")
    def test_login_with_allure(self):
        with allure.step("发送登录请求"):
            response = requests.post(
                "https://api.example.com/login",
                json={"username": "admin", "password": "123456"}
            )
            # 记录请求
            allure.attach(
                '{"username": "admin", "password": "******"}',
                name="请求数据",
                attachment_type=allure.attachment_type.JSON
            )
            # 记录响应
            allure.attach(
                response.text,
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("验证响应"):
            assert response.status_code == 200
            assert "token" in response.json()
```

### 综合练习（17-20）

#### 练习17：完整 API 测试框架

```python
# 项目结构：
# api_test_framework/
# ├── config/
# │   └── settings.py
# ├── api/
# │   ├── client.py
# │   ├── user_api.py
# │   └── order_api.py
# ├── tests/
# │   ├── conftest.py
# │   ├── test_user.py
# │   └── test_order.py
# ├── utils/
# │   └── data_loader.py
# └── requirements.txt

# api/client.py - 基础客户端
class APIClient:
    """完整的 API 客户端"""
    # 实现所有 HTTP 方法
    # 支持重试、超时、日志
    pass

# api/user_api.py - 用户 API
class UserAPI(APIClient):
    """用户相关 API"""
    def login(self, username, password): pass
    def logout(self): pass
    def get_profile(self): pass
    def update_profile(self, data): pass

# api/order_api.py - 订单 API
class OrderAPI(APIClient):
    """订单相关 API"""
    def create_order(self, data): pass
    def get_order(self, order_id): pass
    def cancel_order(self, order_id): pass

# tests/conftest.py - Pytest 配置
@pytest.fixture(scope="session")
def api_client():
    return APIClient("https://api.example.com")

@pytest.fixture
def user_api(api_client):
    return UserAPI(api_client.base_url)

@pytest.fixture
def auth_token(user_api):
    response = user_api.login("admin", "123456")
    return response.json()["token"]
```

#### 练习18：接口自动化测试套件

```python
# tests/test_complete_suite.py
# 要求：
# 1. 完整的用户 CRUD 测试
# 2. 完整的订单流程测试
# 3. 使用 Allure 生成报告

import allure
import pytest

@allure.feature("用户管理")
class TestUserSuite:

    @allure.story("用户认证")
    def test_login_success(self, user_api):
        """登录成功"""
        pass

    def test_login_fail(self, user_api):
        """登录失败"""
        pass

    @allure.story("用户信息")
    def test_get_profile(self, user_api, auth_token):
        """获取用户信息"""
        pass

    def test_update_profile(self, user_api, auth_token):
        """更新用户信息"""
        pass

@allure.feature("订单管理")
class TestOrderSuite:

    @allure.story("订单流程")
    def test_create_order(self, order_api, auth_token):
        """创建订单"""
        pass

    def test_pay_order(self, order_api, auth_token):
        """支付订单"""
        pass

    def test_query_order(self, order_api, auth_token):
        """查询订单"""
        pass

    def test_cancel_order(self, order_api, auth_token):
        """取消订单"""
        pass
```

#### 练习19：接口性能测试

```python
# tests/test_performance.py
# 要求：
# 1. 使用 pytest-xdist 并发测试
# 2. 统计接口响应时间
# 3. 验证接口性能指标

import pytest
import requests
import time

@pytest.mark.parametrize("endpoint", [
    "/posts",
    "/comments",
    "/users",
])
def test_response_time(endpoint):
    """测试接口响应时间"""
    url = f"https://jsonplaceholder.typicode.com{endpoint}"

    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    response_time = end_time - start_time
    print(f"{endpoint} 响应时间: {response_time:.3f}s")

    assert response.status_code == 200
    assert response_time < 2.0  # 响应时间小于 2 秒

def test_concurrent_requests():
    """并发请求测试"""
    import concurrent.futures

    def make_request(i):
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        return response.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(make_request, range(10)))

    assert all(status == 200 for status in results)

# 运行并发测试：pytest -n 4 tests/test_performance.py
```

#### 练习20：接口测试最佳实践项目

```python
# 要求：整合所学知识，搭建企业级接口测试项目
# 1. 分层设计：API 层、业务层、测试层
# 2. 数据驱动：支持 YAML/JSON/CSV 数据文件
# 3. 环境切换：支持 dev/test/prod 环境
# 4. 报告生成：Allure 报告 + 钉钉/邮件通知
# 5. CI/CD 集成：Jenkins/GitHub Actions 配置

# 项目结构：
# api_automation/
# ├── config/
# │   ├── config.dev.yaml
# │   ├── config.test.yaml
# │   └── config.prod.yaml
# ├── api/
# │   ├── __init__.py
# │   ├── base_client.py
# │   ├── user_api.py
# │   ├── order_api.py
# │   └── auth.py
# ├── tests/
# │   ├── conftest.py
# │   ├── test_user/
# │   │   ├── test_login.py
# │   │   └── test_profile.py
# │   ├── test_order/
# │   │   ├── test_create.py
# │   │   └── test_flow.py
# │   └── data/
# │       ├── login.csv
# │       └── users.json
# ├── utils/
# │   ├── data_loader.py
# │   ├── logger.py
# │   └── notification.py
# ├── reports/
# ├── pytest.ini
# ├── conftest.py
# └── requirements.txt

# 运行命令：
# pytest --env=test --alluredir=reports/allure-results
# allure serve reports/allure-results
```

---

## 五、本周小结

1. **Requests**：Python 接口测试的标准库
2. **Session**：保持登录状态的核心
3. **封装设计**：让测试代码更易维护
4. **认证处理**：企业级接口必备

### 下周预告

第7周学习数据库测试和 Mock 技术。
