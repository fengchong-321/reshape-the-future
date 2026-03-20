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

### 练习1：封装完整的 API 测试框架

```python
# 实现：
# 1. APIClient 基类
# 2. UserAPI 业务封装
# 3. OrderAPI 业务封装
# 4. 测试用例

# tests/test_api.py
class TestUserAPI:
    def test_login_success(self, api_client):
        pass

    def test_login_fail(self, api_client):
        pass

    def test_get_profile(self, api_client):
        pass
```

### 练习2：数据驱动接口测试

```python
# 从 CSV 读取测试数据
# 参数化执行测试
```

### 练习3：链式接口测试

```python
# 登录 -> 创建订单 -> 支付 -> 查询订单状态
```

---

## 五、本周小结

1. **Requests**：Python 接口测试的标准库
2. **Session**：保持登录状态的核心
3. **封装设计**：让测试代码更易维护
4. **认证处理**：企业级接口必备

### 下周预告

第7周学习数据库测试和 Mock 技术。
