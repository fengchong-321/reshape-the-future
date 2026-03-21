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

### 基础练习（1-8）

#### 练习1：编写第一个测试用例

```python
# tests/test_basic.py
# 要求：
# 1. 创建一个简单的测试文件 test_basic.py
# 2. 编写 test_add() 函数测试加法
# 3. 编写 test_string() 函数测试字符串操作
# 4. 使用 pytest 命令运行测试

def test_add():
    # 测试加法运算
    pass

def test_string():
    # 测试字符串操作：拼接、大小写、切片
    pass
```

#### 练习2：断言练习

```python
# tests/test_assertions.py
# 要求：编写测试函数，使用以下断言：
# 1. assert equal - 相等断言
# 2. assert not equal - 不相等断言
# 3. assert in / not in - 包含断言
# 4. assert is None / is not None - None 断言
# 5. assert isinstance - 类型断言
# 6. assert True / False - 布尔断言

def test_equality():
    pass

def test_comparison():
    pass

def test_membership():
    pass

def test_none():
    pass

def test_type():
    pass

def test_boolean():
    pass
```

#### 练习3：异常测试

```python
# tests/test_exceptions.py
# 要求：
# 1. 编写一个 divide(a, b) 函数，b=0 时抛出 ValueError
# 2. 使用 pytest.raises 测试异常抛出
# 3. 验证异常消息内容

import pytest

def divide(a, b):
    # 实现除法，b=0 时抛出 ValueError
    pass

def test_divide_success():
    # 测试正常除法
    pass

def test_divide_by_zero():
    # 测试除零异常
    pass
```

#### 练习4：基础 fixture

```python
# tests/test_fixture_basic.py
# 要求：
# 1. 创建一个 sample_data fixture，返回测试数据字典
# 2. 创建多个测试函数使用该 fixture
# 3. 验证 fixture 数据正确性

import pytest

@pytest.fixture
def sample_data():
    # 返回测试数据
    pass

def test_user_name(sample_data):
    pass

def test_user_email(sample_data):
    pass
```

#### 练习5：fixture 资源管理

```python
# tests/test_fixture_resource.py
# 要求：
# 1. 创建 temp_file fixture，在测试前创建临时文件
# 2. 使用 yield 返回文件路径
# 3. 测试后自动删除临时文件

import pytest
import os

@pytest.fixture
def temp_file():
    # 创建临时文件
    # yield 返回文件路径
    # 删除临时文件
    pass

def test_write_file(temp_file):
    # 测试写入文件
    pass

def test_read_file(temp_file):
    # 测试读取文件
    pass
```

#### 练习6：参数化测试基础

```python
# tests/test_parametrize_basic.py
# 要求：
# 1. 使用 @pytest.mark.parametrize 测试 is_even 函数
# 2. 测试正数、负数、零
# 3. 至少提供 5 组测试数据

import pytest

def is_even(n):
    return n % 2 == 0

@pytest.mark.parametrize("input,expected", [
    # 填写测试数据
])
def test_is_even(input, expected):
    pass
```

#### 练习7：标记测试用例

```python
# tests/test_markers.py
# 要求：
# 1. 使用 @pytest.mark.smoke 标记冒烟测试
# 2. 使用 @pytest.mark.skip 跳过测试
# 3. 使用 @pytest.mark.xfail 标记预期失败
# 4. 在 pytest.ini 中注册自定义标记

import pytest

@pytest.mark.smoke
def test_login_smoke():
    pass

@pytest.mark.skip(reason="功能未实现")
def test_future_feature():
    pass

@pytest.mark.xfail(reason="已知 Bug")
def test_known_bug():
    pass
```

#### 练习8：测试类组织

```python
# tests/test_class_organization.py
# 要求：
# 1. 创建 TestCalculator 测试类
# 2. 包含 test_add, test_subtract, test_multiply, test_divide 方法
# 3. 使用类级别的 fixture 提供计算器实例

import pytest

class TestCalculator:
    @pytest.fixture(autouse=True)
    def setup(self):
        # 初始化计算器
        pass

    def test_add(self):
        pass

    def test_subtract(self):
        pass

    def test_multiply(self):
        pass

    def test_divide(self):
        pass
```

### 进阶练习（9-16）

#### 练习9：fixture 作用域

```python
# tests/test_fixture_scope.py
# 要求：
# 1. 创建 session 级别 fixture：database_config
# 2. 创建 module 级别 fixture：test_data
# 3. 创建 function 级别 fixture：clean_data
# 4. 观察各 fixture 的执行次数

import pytest

@pytest.fixture(scope="session")
def database_config():
    print("\n=== Session 级别：数据库配置 ===")
    yield {"host": "localhost", "port": 3306}

@pytest.fixture(scope="module")
def test_data():
    print("\n=== Module 级别：测试数据 ===")
    yield [{"id": 1, "name": "user1"}]

@pytest.fixture
def clean_data():
    print("\n=== Function 级别：清理数据 ===")
    yield

def test_case1(database_config, test_data, clean_data):
    pass

def test_case2(database_config, test_data, clean_data):
    pass
```

#### 练习10：conftest.py 共享 fixture

```python
# tests/conftest.py
# 要求：
# 1. 在 conftest.py 中定义共享 fixture
# 2. 创建 api_client fixture（session 级别）
# 3. 创建 auth_token fixture 依赖 api_client

import pytest

@pytest.fixture(scope="session")
def api_client():
    # 返回模拟的 API 客户端
    pass

@pytest.fixture
def auth_token(api_client):
    # 模拟登录获取 token
    pass

# tests/test_with_conftest.py
# 在另一个文件中使用 conftest 中定义的 fixture
class TestWithConftest:
    def test_api_call(self, api_client):
        pass

    def test_authenticated_call(self, auth_token):
        pass
```

#### 练习11：多参数化组合

```python
# tests/test_multi_parametrize.py
# 要求：
# 1. 使用多个 @pytest.mark.parametrize 装饰器
# 2. 测试字符串处理函数：截取、大小写转换
# 3. 实现笛卡尔积组合测试

import pytest

def process_string(s, operation):
    """根据操作类型处理字符串"""
    if operation == "upper":
        return s.upper()
    elif operation == "lower":
        return s.lower()
    elif operation == "reverse":
        return s[::-1]
    return s

@pytest.mark.parametrize("operation", ["upper", "lower", "reverse"])
@pytest.mark.parametrize("input_str", ["hello", "WORLD", "PyTest"])
def test_string_operations(input_str, operation):
    # 测试不同字符串和操作的组合
    pass
```

#### 练习12：indirect 参数化

```python
# tests/test_indirect.py
# 要求：
# 1. 创建 user_data fixture，通过 request.param 接收参数
# 2. 在 fixture 中对数据进行预处理
# 3. 使用 indirect=True 将参数传递给 fixture

import pytest

@pytest.fixture
def user_data(request):
    """预处理用户数据"""
    data = request.param
    # 数据预处理：转大写、添加时间戳等
    return data

@pytest.mark.parametrize("user_data", [
    {"name": "admin", "role": "admin"},
    {"name": "user", "role": "guest"},
], indirect=True)
def test_with_indirect(user_data):
    pass
```

#### 练习13：pytest.ini 配置

```ini
# pytest.ini
# 要求：
# 1. 配置测试路径
# 2. 配置文件匹配模式
# 3. 添加默认命令行参数
# 4. 注册自定义标记

[pytest]
# 填写配置内容
```

```python
# tests/test_with_config.py
# 使用 pytest.ini 中注册的标记
import pytest

@pytest.mark.smoke
def test_smoke():
    pass

@pytest.mark.regression
def test_regression():
    pass
```

#### 练习14：登录测试模块（完整版）

```python
# tests/test_login.py
# 要求：
# 1. 使用 fixture 提供 API 客户端
# 2. 使用参数化测试多种登录场景
# 3. 使用标记区分冒烟测试和回归测试
# 4. 测试成功和失败场景

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

#### 练习15：用户 CRUD 测试

```python
# tests/test_user.py
# 要求：
# 1. 实现用户增删改查测试
# 2. 使用 module 级别的 fixture 管理测试数据
# 3. 每个 CRUD 操作都有独立测试

import pytest

@pytest.fixture(scope="module")
def test_user():
    """创建测试用户"""
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

#### 练习16：浮点数和近似值测试

```python
# tests/test_approx.py
# 要求：
# 1. 使用 pytest.approx 测试浮点数
# 2. 测试相对误差和绝对误差
# 3. 测试列表和字典中的近似值

import pytest

def test_float_approx():
    # 测试浮点数近似相等
    result = 0.1 + 0.2
    assert result == pytest.approx(0.3)

def test_with_tolerance():
    # 测试指定误差范围
    pass

def test_list_approx():
    # 测试列表中的浮点数
    pass

def test_dict_approx():
    # 测试字典中的浮点数
    pass
```

### 综合练习（17-20）

#### 练习17：搭建完整测试项目

```
# 要求：创建完整项目结构
pytest_demo/
├── pytest.ini              # 配置文件
├── conftest.py             # 全局 fixture
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # 测试级 fixture
│   ├── test_login.py       # 登录测试
│   ├── test_user.py        # 用户测试
│   └── test_order.py       # 订单测试
├── config/
│   └── settings.py         # 配置
└── requirements.txt        # 依赖
```

```python
# pytest.ini 配置示例
# conftest.py fixture 示例
# 至少编写 15 个测试用例
```

#### 练习18：数据驱动测试框架

```python
# tests/test_data_driven.py
# 要求：
# 1. 从 JSON 文件读取测试数据
# 2. 动态生成测试用例
# 3. 支持数据文件的扩展

import pytest
import json

def load_test_data(filepath):
    """从 JSON 文件加载测试数据"""
    pass

# test_data.json 内容示例：
# [
#   {"input": 1, "expected": 2},
#   {"input": 5, "expected": 10}
# ]

@pytest.mark.parametrize("data", load_test_data("tests/data/test_cases.json"))
def test_data_driven(data):
    pass
```

#### 练习19：命令行参数测试

```python
# conftest.py
# 要求：
# 1. 添加 --env 命令行参数
# 2. 根据参数加载不同配置
# 3. 在测试中使用配置

import pytest

def pytest_addoption(parser):
    parser.addoption("--env", default="test", help="测试环境")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def config(env):
    # 根据环境返回配置
    configs = {
        "dev": {"url": "http://localhost:8000"},
        "test": {"url": "https://test.example.com"},
        "prod": {"url": "https://example.com"}
    }
    return configs[env]

# tests/test_with_env.py
def test_with_config(config):
    # 使用环境配置
    pass
```

#### 练习20：综合测试套件

```python
# tests/test_suite.py
# 要求：整合所学知识，完成以下任务：
# 1. 使用 conftest.py 定义共享 fixture
# 2. 使用多种作用域的 fixture
# 3. 使用参数化测试
# 4. 使用标记分类测试
# 5. 使用 pytest.ini 配置
# 6. 测试异常和边界情况

import pytest

# 定义测试类和测试函数
class TestComplete:
    """综合测试套件"""

    @pytest.mark.smoke
    def test_smoke_suite(self, api_client):
        pass

    @pytest.mark.parametrize("case", [
        {"input": "valid", "expected": True},
        {"input": "invalid", "expected": False},
    ])
    def test_parameterized_suite(self, case):
        pass

    def test_exception_handling(self):
        with pytest.raises(ValueError):
            raise ValueError("测试异常")

# 运行命令：
# pytest -v --env=test -m smoke
# pytest -v --env=test tests/test_suite.py
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
