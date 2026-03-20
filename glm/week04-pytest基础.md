# 第4周：Pytest 基础

## 本周目标

掌握 Pytest 测试框架的核心用法，能编写规范、可维护的测试用例。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Pytest 安装与运行 | 安装、命令行、发现规则 | ⭐⭐⭐⭐ |
| 测试函数与类 | 命名规则、断言 | ⭐⭐⭐⭐⭐ |
| fixture 机制 | 基础 fixture、作用域、autouse | ⭐⭐⭐⭐⭐ |
| 参数化测试 | @pytest.mark.parametrize | ⭐⭐⭐⭐⭐ |
| 标记与跳过 | mark、skip、xfail | ⭐⭐⭐⭐ |
| 配置文件 | pytest.ini、conftest.py | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 Pytest 简介与安装

```bash
# 安装
pip install pytest

# 安装常用插件
pip install pytest-html pytest-xdist pytest-rerunfailures pytest-timeout

# 验证安装
pytest --version
```

**Pytest 的优势：**
- 语法简洁，无需继承特定类
- 强大的 fixture 机制
- 丰富的插件生态
- 自动发现测试用例
- 详细的失败信息

---

### 2.2 测试发现规则

Pytest 自动发现测试的规则：

```
1. 文件名：test_*.py 或 *_test.py
2. 类名：Test*（且不能有 __init__ 方法）
3. 函数名：test_*
```

```python
# ✅ 会被发现
# test_example.py

def test_login():
    pass

def test_search():
    pass

class TestUser:
    def test_create(self):
        pass

    def test_delete(self):
        pass

# ❌ 不会被发现
def login_test():  # 不是 test_ 开头
    pass

class UserTest:  # 不是 Test 开头
    def test_something(self):
        pass

class TestOrder:  # 有 __init__ 方法
    def __init__(self):
        pass
```

**命令行运行：**

```bash
# 运行所有测试
pytest

# 运行指定文件
pytest test_login.py

# 运行指定目录
pytest tests/

# 运行指定类
pytest test_user.py::TestUser

# 运行指定方法
pytest test_user.py::TestUser::test_login

# 详细输出
pytest -v

# 显示 print 输出
pytest -s

# 失败时停止
pytest -x

# 遇到第一个失败停止
pytest --maxfail=2

# 并行执行（需要 pytest-xdist）
pytest -n 4
```

---

### 2.3 断言

Pytest 使用 Python 原生的 `assert` 语句，但会提供详细的失败信息。

```python
# ============================================
# 基本断言
# ============================================
def test_basic_assertions():
    # 相等
    assert 1 + 1 == 2
    assert "hello" == "hello"

    # 不相等
    assert 1 != 2

    # 比较
    assert 5 > 3
    assert 3 < 5
    assert 5 >= 5
    assert 3 <= 5

    # 包含
    assert "hello" in "hello world"
    assert 1 in [1, 2, 3]
    assert "name" in {"name": "张三"}

    # 不包含
    assert "hi" not in "hello"

    # 布尔值
    assert True
    assert not False

    # None
    assert None is None
    assert "value" is not None

    # 类型
    assert isinstance(123, int)
    assert isinstance([1, 2], list)

# ============================================
# 浮点数比较（注意精度问题）
# ============================================
def test_float():
    # ❌ 可能失败（浮点精度）
    # assert 0.1 + 0.2 == 0.3

    # ✅ 使用 approx
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 1.0001 == pytest.approx(1.0, rel=1e-3)  # 相对误差
    assert 1.0001 == pytest.approx(1.0, abs=1e-3)  # 绝对误差

# ============================================
# 异常断言
# ============================================
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b

def test_exception():
    # 断言抛出异常
    with pytest.raises(ValueError) as excinfo:
        divide(1, 0)

    # 验证异常消息
    assert "除数不能为0" in str(excinfo.value)

    # 验证异常类型
    assert excinfo.type == ValueError

# 断言不抛出异常
def test_no_exception():
    with pytest.raises(Exception) as excinfo:
        divide(1, 1)
    assert excinfo.type is None  # 没有异常

# ============================================
# 警告断言
# ============================================
import warnings

def old_function():
    warnings.warn("这个函数已弃用", DeprecationWarning)
    return "result"

def test_warning():
    with pytest.warns(DeprecationWarning) as record:
        result = old_function()

    assert len(record) == 1
    assert "已弃用" in str(record[0].message)

# ============================================
# 自定义断言消息
# ============================================
def test_with_message():
    a, b = 1, 2
    assert a == b, f"期望 {a} 等于 {b}"
```

---

### 2.4 fixture 基础

fixture 是 Pytest 最强大的功能，用于测试前的准备和测试后的清理。

```python
import pytest

# ============================================
# 基础 fixture
# ============================================
@pytest.fixture
def sample_data():
    """提供测试数据"""
    return {"username": "admin", "password": "123456"}

def test_login(sample_data):  # fixture 名作为参数
    """使用 fixture"""
    assert sample_data["username"] == "admin"

# ============================================
# fixture 做资源管理
# ============================================
@pytest.fixture
def temp_file():
    """创建临时文件，测试后删除"""
    import os
    filename = "temp_test.txt"

    # setup - 测试前执行
    with open(filename, "w") as f:
        f.write("test content")

    yield filename  # yield 返回给测试用例

    # teardown - 测试后执行
    if os.path.exists(filename):
        os.remove(filename)

def test_file_operation(temp_file):
    """使用临时文件 fixture"""
    with open(temp_file, "r") as f:
        content = f.read()
    assert content == "test content"

# ============================================
# fixture 作用域
# ============================================
# scope="function"  - 每个测试函数执行一次（默认）
# scope="class"     - 每个测试类执行一次
# scope="module"    - 每个模块执行一次
# scope="package"   - 每个包执行一次
# scope="session"   - 整个测试会话执行一次

@pytest.fixture(scope="module")
def database_connection():
    """模块级别的数据库连接"""
    print("\n连接数据库...")
    conn = {"connected": True}
    yield conn
    print("\n关闭数据库连接...")
    conn["connected"] = False

def test_query1(database_connection):
    assert database_connection["connected"] is True

def test_query2(database_connection):
    # 复用同一个连接
    assert database_connection["connected"] is True

# ============================================
# autouse - 自动使用
# ============================================
@pytest.fixture(autouse=True)
def setup_teardown():
    """每个测试自动执行"""
    print("\n测试前准备")
    yield
    print("\n测试后清理")

def test_something():
    print("执行测试")
# 输出顺序：测试前准备 -> 执行测试 -> 测试后清理

# ============================================
# fixture 依赖
# ============================================
@pytest.fixture
def config():
    """基础配置"""
    return {"base_url": "https://api.example.com"}

@pytest.fixture
def api_client(config):  # 依赖 config fixture
    """API 客户端"""
    class Client:
        def __init__(self, base_url):
            self.base_url = base_url

        def get(self, endpoint):
            return f"GET {self.base_url}{endpoint}"

    return Client(config["base_url"])

def test_api(api_client):
    """使用依赖 fixture"""
    response = api_client.get("/users")
    assert "GET https://api.example.com/users" == response

# ============================================
# fixture 返回多个值
# ============================================
@pytest.fixture
def user_data():
    """返回多个测试数据"""
    return (
        {"username": "admin", "role": "admin"},
        {"username": "user", "role": "user"}
    )

def test_users(user_data):
    admin, normal_user = user_data
    assert admin["role"] == "admin"
```

---

### 2.5 conftest.py - 共享 fixture

```python
# tests/conftest.py
"""
conftest.py 是 Pytest 的配置文件
- 自动被同目录及子目录的测试发现
- 用于定义共享的 fixture
- 无需显式 import
"""

import pytest
import requests

# ============================================
# 全局 fixture
# ============================================
@pytest.fixture(scope="session")
def base_url():
    """API 基础 URL"""
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def api_session():
    """共享的 requests Session"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()

@pytest.fixture
def api_client(base_url, api_session):
    """API 客户端 fixture"""
    class APIClient:
        def __init__(self, base_url, session):
            self.base_url = base_url
            self.session = session

        def get(self, endpoint):
            return self.session.get(f"{self.base_url}{endpoint}")

        def post(self, endpoint, data):
            return self.session.post(f"{self.base_url}{endpoint}", json=data)

    return APIClient(base_url, api_session)

# ============================================
# 测试数据 fixture
# ============================================
@pytest.fixture
def valid_user():
    """有效用户数据"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "username": "testuser"
    }

@pytest.fixture(params=[
    {"name": "", "email": "test@example.com"},
    {"name": "Test", "email": ""},
    {"name": "Test", "email": "invalid"},
])
def invalid_user(request):
    """无效用户数据（参数化）"""
    return request.param

# ============================================
# 环境切换
# ============================================
@pytest.fixture(scope="session")
def env_config(request):
    """根据命令行参数选择环境"""
    env = request.config.getoption("--env", default="test")

    configs = {
        "dev": {"base_url": "http://localhost:8000"},
        "test": {"base_url": "https://test.api.example.com"},
        "prod": {"base_url": "https://api.example.com"}
    }

    return configs[env]

# pytest.ini 中添加
# [pytest]
# addopts = --env=test
```

---

### 2.6 参数化测试

```python
import pytest

# ============================================
# 基础参数化
# ============================================
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (10, 20),
])
def test_double(input, expected):
    """测试翻倍函数"""
    assert input * 2 == expected

# ============================================
# 参数化 + 描述
# ============================================
@pytest.mark.parametrize("input,expected", [
    pytest.param(1, 2, id="positive"),
    pytest.param(-1, -2, id="negative"),
    pytest.param(0, 0, id="zero"),
])
def test_double_with_id(input, expected):
    assert input * 2 == expected

# ============================================
# 多个参数化装饰器（笛卡尔积）
# ============================================
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    """4 个组合：1*10, 1*20, 2*10, 2*20"""
    pass

# ============================================
# 参数化类
# ============================================
@pytest.mark.parametrize("username,password,expected", [
    ("admin", "123456", True),
    ("admin", "wrong", False),
    ("", "123456", False),
])
class TestLogin:
    def test_login_api(self, username, password, expected):
        # 每组参数运行一次整个类
        pass

    def test_login_ui(self, username, password, expected):
        pass

# ============================================
# 从文件加载参数化数据
# ============================================
import json

def load_test_data(filepath):
    """从 JSON 文件加载测试数据"""
    with open(filepath) as f:
        return json.load(f)

@pytest.mark.parametrize("data", load_test_data("test_data.json"))
def test_from_file(data):
    """从文件加载测试数据"""
    pass

# ============================================
# 动态参数化
# ============================================
def generate_test_cases():
    """动态生成测试用例"""
    cases = []
    for i in range(10):
        cases.append(pytest.param(i, i**2, id=f"square_{i}"))
    return cases

@pytest.mark.parametrize("input,expected", generate_test_cases())
def test_dynamic(input, expected):
    assert input ** 2 == expected
```

---

### 2.7 标记（Markers）

```python
import pytest

# ============================================
# 内置标记
# ============================================

# skip - 跳过测试
@pytest.mark.skip(reason="功能未实现")
def test_future_feature():
    pass

# skipif - 条件跳过
@pytest.mark.skipif(
    sys.version_info < (3, 8),
    reason="需要 Python 3.8+"
)
def test_python38_feature():
    pass

# xfail - 预期失败
@pytest.mark.xfail(reason="已知 Bug #123")
def test_known_bug():
    assert 1 == 2  # 会标记为 XFAIL 而不是 FAIL

# xfail + 严格模式（如果通过则失败）
@pytest.mark.xfail(reason="预期失败", strict=True)
def test_should_fail():
    assert 1 == 1  # 会标记为 FAIL

# ============================================
# 自定义标记
# ============================================
# 在 pytest.ini 中注册
"""
[pytest]
markers =
    smoke: 冒烟测试
    regression: 回归测试
    slow: 慢速测试
    api: API 测试
    ui: UI 测试
"""

@pytest.mark.smoke
def test_login():
    pass

@pytest.mark.regression
@pytest.mark.api
def test_create_user():
    pass

# 多个标记
@pytest.mark.smoke
@pytest.mark.p0
def test_critical():
    pass

# ============================================
# 使用标记运行测试
# ============================================
# pytest -m smoke        # 只运行冒烟测试
# pytest -m "smoke and api"  # 冒烟且是 API 测试
# pytest -m "smoke or regression"  # 冒烟或回归
# pytest -m "not slow"   # 不是慢速测试
```

---

### 2.8 pytest.ini 配置

```ini
# pytest.ini
[pytest]
# 测试路径
testpaths = tests

# 文件匹配模式
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# 默认命令行参数
addopts =
    -v
    --tb=short
    --html=reports/report.html
    --self-contained-html

# 注册自定义标记
markers =
    smoke: 冒烟测试
    regression: 回归测试
    p0: 最高优先级
    p1: 高优先级
    p2: 中优先级
    slow: 慢速测试

# 忽略警告
filterwarnings =
    ignore::DeprecationWarning

# 最小版本
minversion = 7.0
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 能编写基本的测试函数和测试类
- [ ] 能使用 assert 进行各种断言
- [ ] 能编写和使用 fixture
- [ ] 能使用 @pytest.mark.parametrize 进行参数化
- [ ] 能使用 @pytest.mark.skip 和 xfail
- [ ] 能配置 pytest.ini

### 应该了解

- [ ] fixture 的各种作用域
- [ ] conftest.py 的用法
- [ ] 命令行参数

---

## 四、练习内容

### 练习1：登录测试模块

```python
# tests/test_login.py
# 实现：
# 1. 使用 fixture 提供 API 客户端
# 2. 使用参数化测试多种登录场景
# 3. 使用标记区分冒烟测试和回归测试

import pytest

class TestLogin:
    @pytest.fixture
    def api_client(self):
        # 返回 API 客户端
        pass

    @pytest.mark.smoke
    @pytest.mark.parametrize("username,password,expected", [
        ("admin", "123456", True),
        ("user", "password", True),
    ])
    def test_login_success(self, api_client, username, password, expected):
        pass

    @pytest.mark.parametrize("username,password", [
        ("", "123456"),
        ("admin", ""),
        ("admin", "wrong"),
    ])
    def test_login_fail(self, api_client, username, password):
        pass
```

### 练习2：用户 CRUD 测试

```python
# tests/test_user.py
# 实现用户增删改查测试
# 使用 module 级别的 fixture 管理测试数据

import pytest

@pytest.fixture(scope="module")
def test_user():
    """创建测试用户"""
    # 创建用户
    user = {"id": 1, "name": "Test User"}
    yield user
    # 清理用户

class TestUserCRUD:
    def test_create_user(self, test_user):
        pass

    def test_get_user(self, test_user):
        pass

    def test_update_user(self, test_user):
        pass

    def test_delete_user(self, test_user):
        pass
```

### 练习3：搭建测试项目

```
# 创建完整项目结构
pytest_demo/
├── pytest.ini
├── conftest.py
├── tests/
│   ├── __init__.py
│   ├── test_login.py
│   ├── test_user.py
│   └── test_order.py
└── requirements.txt
```

---

## 五、检验标准

### 自测题

1. 编写一个 fixture，在测试前创建临时目录，测试后删除
2. 使用参数化测试字符串反转函数
3. 编写 conftest.py，提供全局的 API 客户端 fixture

### 答案

```python
# 1. 临时目录 fixture
import pytest
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)

def test_file_in_temp(temp_dir):
    import os
    filepath = os.path.join(temp_dir, "test.txt")
    with open(filepath, "w") as f:
        f.write("test")
    assert os.path.exists(filepath)

# 2. 参数化字符串反转
@pytest.mark.parametrize("input,expected", [
    ("hello", "olleh"),
    ("", ""),
    ("a", "a"),
    ("ab", "ba"),
    ("12345", "54321"),
])
def test_reverse(input, expected):
    assert input[::-1] == expected

# 3. conftest.py
# tests/conftest.py
import pytest
import requests

@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.base_url = "https://api.example.com"

    class Client:
        def get(self, endpoint):
            return session.get(f"{session.base_url}{endpoint}")

        def post(self, endpoint, data):
            return session.post(f"{session.base_url}{endpoint}", json=data)

    return Client()
```

---

## 六、本周小结

### 核心要点

1. **测试发现**：test_*.py, Test*, test_*
2. **断言**：assert + pytest.approx + pytest.raises
3. **fixture**：测试资源的生命周期管理
4. **参数化**：@pytest.mark.parametrize 数据驱动
5. **标记**：分类和筛选测试用例

### 下周预告

第5周学习 Pytest 进阶和 Allure 报告。
