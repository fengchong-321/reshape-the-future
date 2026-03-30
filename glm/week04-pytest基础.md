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

---

**练习1：编写第一个测试用例**

**场景说明**：开始使用 Pytest 编写最基础的测试函数，理解测试发现规则。

**具体需求**：
1. 创建测试文件 `test_basic.py`
2. 编写 `test_add()` 函数，测试加法运算（1+1=2, 2+3=5）
3. 编写 `test_string()` 函数，测试字符串操作：
   - 拼接：`"hello" + " world" = "hello world"`
   - 大小写：`"hello".upper() = "HELLO"`
   - 切片：`"hello"[0] = "h"`
4. 使用 `pytest test_basic.py -v` 运行测试

**使用示例**：
```python
# tests/test_basic.py

def test_add():
    """测试加法运算"""
    # 基础加法
    assert 1 + 1 == 2
    assert 2 + 3 == 5
    # 边界情况
    assert 0 + 0 == 0
    assert -1 + 1 == 0

def test_string():
    """测试字符串操作"""
    # 拼接
    assert "hello" + " world" == "hello world"
    # 大小写
    assert "hello".upper() == "HELLO"
    assert "WORLD".lower() == "world"
    # 切片
    assert "hello"[0] == "h"
    assert "hello"[-1] == "o"
    assert "hello"[1:3] == "el"
```

**运行命令**：
```bash
# 运行单个测试文件
pytest tests/test_basic.py -v

# 运行所有测试
pytest -v

# 输出示例：
# test_basic.py::test_add PASSED
# test_basic.py::test_string PASSED
```

**验收标准**：
- [ ] 测试文件命名正确（test_*.py）
- [ ] 测试函数命名正确（test_*）
- [ ] 所有断言通过
- [ ] 能使用 pytest 命令运行测试

---

**练习2：断言练习**

**场景说明**：掌握 Pytest 的各种断言方式，能够编写全面的验证逻辑。

**具体需求**：
1. `test_equality()` - 相等/不相等断言
2. `test_comparison()` - 比较断言（>, <, >=, <=）
3. `test_membership()` - 包含断言（in, not in）
4. `test_none()` - None 断言（is None, is not None）
5. `test_type()` - 类型断言（isinstance）
6. `test_boolean()` - 布尔断言（True, False）

**使用示例**：
```python
# tests/test_assertions.py

def test_equality():
    """相等/不相等断言"""
    # 相等
    assert 1 + 1 == 2
    assert "hello" == "hello"
    # 不相等
    assert 1 != 2
    assert "hello" != "world"

def test_comparison():
    """比较断言"""
    assert 5 > 3
    assert 3 < 5
    assert 5 >= 5
    assert 3 <= 5

def test_membership():
    """包含断言"""
    # 字符串包含
    assert "hello" in "hello world"
    assert "hi" not in "hello"
    # 列表包含
    assert 1 in [1, 2, 3]
    # 字典键包含
    assert "name" in {"name": "张三"}

def test_none():
    """None 断言"""
    assert None is None
    assert "value" is not None
    result = None
    assert result is None

def test_type():
    """类型断言"""
    assert isinstance(123, int)
    assert isinstance("hello", str)
    assert isinstance([1, 2], list)
    assert isinstance({"key": "value"}, dict)

def test_boolean():
    """布尔断言"""
    assert True
    assert not False
    assert 1 == 1  # True
    assert not (1 == 2)  # False
```

**验收标准**：
- [ ] 六种断言类型都使用正确
- [ ] 每个测试函数至少包含 3 个断言
- [ ] 所有断言通过

---

**练习3：异常测试**

**场景说明**：测试代码需要验证异常是否正确抛出，Pytest 提供了 `pytest.raises` 上下文管理器。

**具体需求**：
1. 实现 `divide(a, b)` 函数，b=0 时抛出 `ValueError` 并包含消息 "除数不能为零"
2. 测试正常除法情况
3. 使用 `pytest.raises` 测试异常抛出
4. 验证异常类型和消息内容

**使用示例**：
```python
# tests/test_exceptions.py
import pytest

def divide(a, b):
    """除法函数，除零时抛出异常"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def test_divide_success():
    """测试正常除法"""
    assert divide(10, 2) == 5
    assert divide(6, 3) == 2
    assert divide(7, 2) == 3.5

def test_divide_by_zero():
    """测试除零异常"""
    # 测试异常抛出
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)

    # 验证异常消息
    assert "除数不能为零" in str(excinfo.value)
    assert excinfo.type == ValueError

def test_divide_negative():
    """测试负数除法"""
    assert divide(-10, 2) == -5
    assert divide(10, -2) == -5
    assert divide(-10, -2) == 5
```

**验收标准**：
- [ ] divide 函数正确实现
- [ ] 正常情况测试通过
- [ ] 异常测试使用 `pytest.raises`
- [ ] 验证了异常消息内容

---

**练习4：基础 fixture**

**场景说明**：fixture 是 Pytest 最强大的功能，用于提供测试数据和环境。

**具体需求**：
1. 创建 `sample_data` fixture，返回用户测试数据字典
2. 创建 `test_user_name()` 使用 fixture 验证用户名
3. 创建 `test_user_email()` 使用 fixture 验证邮箱
4. 创建 `test_user_age()` 使用 fixture 验证年龄

**使用示例**：
```python
# tests/test_fixture_basic.py
import pytest

@pytest.fixture
def sample_data():
    """提供测试用户数据"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "age": 25,
        "is_active": True
    }

def test_user_name(sample_data):
    """测试用户名"""
    assert sample_data["username"] == "testuser"
    assert len(sample_data["username"]) > 0
    assert isinstance(sample_data["username"], str)

def test_user_email(sample_data):
    """测试邮箱"""
    assert "@" in sample_data["email"]
    assert sample_data["email"].endswith(".com")

def test_user_age(sample_data):
    """测试年龄"""
    assert sample_data["age"] >= 18  # 成年
    assert sample_data["age"] < 100
    assert isinstance(sample_data["age"], int)

def test_user_active(sample_data):
    """测试激活状态"""
    assert sample_data["is_active"] is True
```

**验收标准**：
- [ ] fixture 使用 `@pytest.fixture` 装饰器
- [ ] fixture 返回有效的测试数据
- [ ] 多个测试函数复用同一 fixture
- [ ] 所有断言通过

#### 练习5：fixture 资源管理

**场景说明**：使用 fixture 管理测试资源（如临时文件），测试前创建，测试后自动清理。

**具体需求**：
1. 创建 `temp_file` fixture，在测试前创建临时文件
2. 使用 `yield` 返回文件路径
3. 测试后自动删除临时文件
4. 编写写入和读取测试用例

**使用示例**：
```python
# tests/test_fixture_resource.py
import pytest
import os

@pytest.fixture
def temp_file():
    """创建临时文件 fixture"""
    filename = "temp_test.txt"

    # Setup - 测试前创建文件
    with open(filename, "w", encoding="utf-8") as f:
        f.write("initial content")

    yield filename  # 返回给测试用例

    # Teardown - 测试后删除文件
    if os.path.exists(filename):
        os.remove(filename)

def test_write_file(temp_file):
    """测试写入文件"""
    # 写入新内容
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write("new content")

    # 验证写入成功
    with open(temp_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "new content"

def test_read_file(temp_file):
    """测试读取文件"""
    with open(temp_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "initial content"

def test_file_exists(temp_file):
    """测试文件存在"""
    assert os.path.exists(temp_file)
```

**验收标准**：
- [ ] 使用 `yield` 实现资源管理
- [ ] Setup 阶段正确创建文件
- [ ] Teardown 阶段正确删除文件
- [ ] 测试后文件被清理

---

**练习6：参数化测试基础**

**场景说明**：参数化测试可以用同一测试逻辑测试多组数据，实现数据驱动测试。

**具体需求**：
1. 定义 `is_even(n)` 函数判断奇偶
2. 使用 `@pytest.mark.parametrize` 测试该函数
3. 测试正数、负数、零
4. 至少提供 5 组测试数据

**使用示例**：
```python
# tests/test_parametrize_basic.py
import pytest

def is_even(n):
    """判断是否为偶数"""
    return n % 2 == 0

@pytest.mark.parametrize("input,expected", [
    (2, True),      # 正偶数
    (3, False),     # 正奇数
    (0, True),      # 零
    (-2, True),     # 负偶数
    (-3, False),    # 负奇数
    (100, True),    # 大偶数
    (99, False),    # 大奇数
])
def test_is_even(input, expected):
    """参数化测试奇偶判断"""
    assert is_even(input) == expected

# 使用 pytest.param 添加测试 ID
@pytest.mark.parametrize("input,expected", [
    pytest.param(2, True, id="正偶数2"),
    pytest.param(3, False, id="正奇数3"),
    pytest.param(0, True, id="零"),
    pytest.param(-2, True, id="负偶数-2"),
])
def test_is_even_with_id(input, expected):
    """带 ID 的参数化测试"""
    assert is_even(input) == expected
```

**运行命令**：
```bash
# 运行参数化测试，显示每个参数组合
pytest tests/test_parametrize_basic.py -v

# 输出示例：
# test_is_even[2-True] PASSED
# test_is_even[3-False] PASSED
# test_is_even[0-True] PASSED
```

**验收标准**：
- [ ] 正确使用 `@pytest.mark.parametrize`
- [ ] 至少 5 组测试数据
- [ ] 覆盖正数、负数、零
- [ ] 所有参数组合通过

---

**练习7：标记测试用例**

**场景说明**：使用标记对测试分类，可以按需运行特定类型的测试。

**具体需求**：
1. 使用 `@pytest.mark.smoke` 标记冒烟测试
2. 使用 `@pytest.mark.skip` 跳过测试
3. 使用 `@pytest.mark.xfail` 标记预期失败
4. 在 `pytest.ini` 中注册自定义标记

**使用示例**：
```python
# tests/test_markers.py
import pytest

# 自定义标记 - 冒烟测试
@pytest.mark.smoke
def test_login_smoke():
    """冒烟测试：登录功能"""
    assert True

@pytest.mark.smoke
def test_search_smoke():
    """冒烟测试：搜索功能"""
    assert True

# 跳过测试
@pytest.mark.skip(reason="功能尚未实现")
def test_future_feature():
    """跳过的测试"""
    assert False  # 不会执行

# 条件跳过
@pytest.mark.skipif(True, reason="条件不满足")
def test_conditional_skip():
    """条件跳过"""
    pass

# 预期失败
@pytest.mark.xfail(reason="已知 Bug #123")
def test_known_bug():
    """预期失败的测试"""
    assert 1 == 2  # 会标记为 XFAIL 而不是 FAIL

# 预期失败但实际通过
@pytest.mark.xfail(reason="预期失败", strict=False)
def test_unexpected_pass():
    """意外通过的测试"""
    assert True  # 会标记为 XPASS
```

**pytest.ini 配置**：
```ini
[pytest]
markers =
    smoke: 冒烟测试
    regression: 回归测试
    slow: 慢速测试
```

**运行命令**：
```bash
# 只运行冒烟测试
pytest -m smoke

# 运行非慢速测试
pytest -m "not slow"

# 运行冒烟或回归测试
pytest -m "smoke or regression"
```

**验收标准**：
- [ ] 正确使用 `skip`、`xfail` 标记
- [ ] 在 pytest.ini 注册自定义标记
- [ ] 能使用 `-m` 参数筛选测试

---

**练习8：测试类组织**

**场景说明**：使用测试类组织相关的测试方法，使测试结构更清晰。

**具体需求**：
1. 创建 `TestCalculator` 测试类
2. 包含 `test_add`、`test_subtract`、`test_multiply`、`test_divide` 方法
3. 使用类级别 fixture 提供计算器实例
4. 测试类命名必须以 `Test` 开头

**使用示例**：
```python
# tests/test_class_organization.py
import pytest

class Calculator:
    """简单计算器类"""
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b

class TestCalculator:
    """计算器测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试方法前执行"""
        self.calc = Calculator()

    def test_add(self):
        """测试加法"""
        assert self.calc.add(1, 2) == 3
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0, 0) == 0

    def test_subtract(self):
        """测试减法"""
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(1, 1) == 0
        assert self.calc.subtract(0, 5) == -5

    def test_multiply(self):
        """测试乘法"""
        assert self.calc.multiply(2, 3) == 6
        assert self.calc.multiply(-2, 3) == -6
        assert self.calc.multiply(0, 100) == 0

    def test_divide(self):
        """测试除法"""
        assert self.calc.divide(6, 2) == 3
        assert self.calc.divide(5, 2) == 2.5

        # 测试异常
        with pytest.raises(ValueError):
            self.calc.divide(1, 0)
```

**验收标准**：
- [ ] 测试类命名以 `Test` 开头
- [ ] 使用 fixture 初始化测试对象
- [ ] 四则运算都有对应测试
- [ ] 异常测试正确实现

### 进阶练习（9-16）

---

**练习9：fixture 作用域**

**场景说明**：理解 fixture 的不同作用域（session/module/class/function），优化测试执行效率。

**具体需求**：
1. 创建 `session` 级别 fixture：`database_config`（整个测试会话只执行一次）
2. 创建 `module` 级别 fixture：`test_data`（每个模块执行一次）
3. 创建 `function` 级别 fixture：`clean_data`（每个测试函数执行一次）
4. 观察各 fixture 的执行次数

**使用示例**：
```python
# tests/test_fixture_scope.py
import pytest

@pytest.fixture(scope="session")
def database_config():
    """Session 级别：整个测试会话只执行一次"""
    print("\n=== Session 级别：数据库配置 ===")
    config = {"host": "localhost", "port": 3306}
    yield config
    print("\n=== Session 级别：关闭数据库 ===")

@pytest.fixture(scope="module")
def test_data():
    """Module 级别：每个模块执行一次"""
    print("\n=== Module 级别：加载测试数据 ===")
    data = [{"id": 1, "name": "user1"}, {"id": 2, "name": "user2"}]
    yield data
    print("\n=== Module 级别：清理测试数据 ===")

@pytest.fixture
def clean_data():
    """Function 级别：每个测试函数执行一次"""
    print("\n  >>> Function 级别：清理数据")
    yield
    print("\n  >>> Function 级别：数据清理完成")

def test_case1(database_config, test_data, clean_data):
    """测试用例1"""
    assert database_config["host"] == "localhost"
    assert len(test_data) == 2

def test_case2(database_config, test_data, clean_data):
    """测试用例2"""
    assert database_config["port"] == 3306
    assert test_data[0]["name"] == "user1"
```

**运行命令**：
```bash
pytest tests/test_fixture_scope.py -s
# 观察输出，理解各作用域的执行次数
```

**验收标准**：
- [ ] session 级别只执行一次
- [ ] module 级别每个模块执行一次
- [ ] function 级别每个测试执行一次
- [ ] 理解 yield 前后代码的执行时机

---

**练习10：conftest.py 共享 fixture**

**场景说明**：conftest.py 是 Pytest 的配置文件，用于定义共享的 fixture，无需显式导入。

**具体需求**：
1. 在 `conftest.py` 中定义 `api_client` fixture（session 级别）
2. 定义 `auth_token` fixture，依赖 `api_client`
3. 在测试文件中直接使用这些 fixture
4. 理解 conftest.py 的查找顺序

**使用示例**：
```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def api_client():
    """Session 级别的 API 客户端"""
    print("\n=== 初始化 API 客户端 ===")
    client = {
        "base_url": "https://api.example.com",
        "timeout": 30
    }
    yield client
    print("\n=== 关闭 API 客户端 ===")

@pytest.fixture
def auth_token(api_client):
    """依赖 api_client 的认证 token"""
    print("\n>>> 获取认证 token")
    # 模拟登录获取 token
    token = f"Bearer mock_token_{api_client['timeout']}"
    yield token
    print("\n>>> 清除认证 token")

# tests/test_with_conftest.py
class TestWithConftest:
    """使用 conftest 中定义的 fixture"""

    def test_api_call(self, api_client):
        """直接使用 api_client"""
        assert api_client["base_url"] == "https://api.example.com"
        assert api_client["timeout"] == 30

    def test_authenticated_call(self, auth_token):
        """使用 auth_token（依赖 api_client）"""
        assert auth_token.startswith("Bearer")
        assert "mock_token" in auth_token
```

**验收标准**：
- [ ] conftest.py 中定义 fixture
- [ ] fixture 依赖关系正确
- [ ] 测试文件无需导入即可使用

---

**练习11：多参数化组合**

**场景说明**：多个 `@pytest.mark.parametrize` 会产生笛卡尔积组合，全面测试各种情况。

**具体需求**：
1. 定义 `process_string(s, operation)` 函数
2. 使用多个参数化装饰器测试字符串操作
3. 实现笛卡尔积组合测试
4. 测试：截取、大小写转换、反转

**使用示例**：
```python
# tests/test_multi_parametrize.py
import pytest

def process_string(s, operation):
    """根据操作类型处理字符串"""
    if operation == "upper":
        return s.upper()
    elif operation == "lower":
        return s.lower()
    elif operation == "reverse":
        return s[::-1]
    elif operation == "capitalize":
        return s.capitalize()
    return s

# 多个参数化 = 笛卡尔积组合
# 3 个字符串 × 4 个操作 = 12 个测试用例
@pytest.mark.parametrize("operation", ["upper", "lower", "reverse", "capitalize"])
@pytest.mark.parametrize("input_str", ["hello", "WORLD", "PyTest"])
def test_string_operations(input_str, operation):
    """测试字符串操作组合"""
    result = process_string(input_str, operation)

    # 验证操作正确性
    if operation == "upper":
        assert result == input_str.upper()
        assert result.isupper() or result == input_str.upper()
    elif operation == "lower":
        assert result == input_str.lower()
        assert result.islower() or result == input_str.lower()
    elif operation == "reverse":
        assert result == input_str[::-1]
    elif operation == "capitalize":
        assert result == input_str.capitalize()

# 使用 pytest.param 添加 ID
@pytest.mark.parametrize("input_str,operation,expected", [
    pytest.param("hello", "upper", "HELLO", id="hello_upper"),
    pytest.param("hello", "lower", "hello", id="hello_lower"),
    pytest.param("hello", "reverse", "olleh", id="hello_reverse"),
])
def test_with_ids(input_str, operation, expected):
    """带 ID 的参数化测试"""
    assert process_string(input_str, operation) == expected
```

**验收标准**：
- [ ] 多参数化正确使用
- [ ] 理解笛卡尔积组合
- [ ] 测试 ID 可读性好

**练习12：indirect 参数化**

**场景说明**：`indirect=True` 允许将参数化数据先传递给 fixture 进行预处理，然后再传给测试函数。这在对测试数据进行转换、验证或增强时非常有用。

**具体需求**：
1. 创建 `user_data` fixture，通过 `request.param` 接收参数
2. 在 fixture 中对数据进行预处理（如：字段标准化、添加时间戳、设置默认值）
3. 使用 `indirect=True` 将参数传递给 fixture
4. 测试不同用户角色（admin、user、guest）的权限验证

**使用示例**：
```python
# tests/test_indirect.py
import pytest
from datetime import datetime

@pytest.fixture
def user_data(request):
    """预处理用户数据的 fixture

    indirect=True 时，request.param 接收参数化数据
    在这里可以对数据进行标准化、验证、增强等操作
    """
    data = request.param

    # 数据预处理：标准化用户名（转小写）
    data["username"] = data["username"].lower()

    # 添加时间戳
    data["created_at"] = datetime.now().isoformat()

    # 设置默认角色
    if "role" not in data:
        data["role"] = "guest"

    # 设置默认状态
    data["is_active"] = data.get("is_active", True)

    return data

def check_permission(user_data, action):
    """检查用户权限"""
    role_permissions = {
        "admin": ["read", "write", "delete", "manage"],
        "user": ["read", "write"],
        "guest": ["read"]
    }
    allowed_actions = role_permissions.get(user_data["role"], [])
    return action in allowed_actions

# 使用 indirect=True 将参数传给 fixture
@pytest.mark.parametrize("user_data", [
    {"username": "ADMIN", "role": "admin"},
    {"username": "TestUser", "role": "user"},
    {"username": "GUEST"},  # 使用默认角色
], indirect=True)
def test_user_data_preprocessing(user_data):
    """测试用户数据预处理"""
    # 验证用户名被转为小写
    assert user_data["username"].islower()

    # 验证时间戳被添加
    assert "created_at" in user_data

    # 验证默认值
    assert "role" in user_data
    assert user_data["is_active"] is True

@pytest.mark.parametrize("user_data,action,expected", [
    pytest.param(
        {"username": "admin", "role": "admin"},
        "delete",
        True,
        id="admin_delete"
    ),
    pytest.param(
        {"username": "user", "role": "user"},
        "delete",
        False,
        id="user_delete_denied"
    ),
    pytest.param(
        {"username": "guest", "role": "guest"},
        "read",
        True,
        id="guest_read"
    ),
    pytest.param(
        {"username": "guest", "role": "guest"},
        "write",
        False,
        id="guest_write_denied"
    ),
], indirect=["user_data"])
def test_user_permissions(user_data, action, expected):
    """测试用户权限检查"""
    result = check_permission(user_data, action)
    assert result == expected, f"{user_data['role']} 对 {action} 的权限应为 {expected}"
```

**运行命令**：
```bash
# 运行 indirect 参数化测试
pytest tests/test_indirect.py -v

# 输出示例：
# test_user_data_preprocessing[admin] PASSED
# test_user_permissions[admin_delete] PASSED
```

**验收标准**：
- [ ] 理解 `indirect=True` 的作用
- [ ] fixture 正确使用 `request.param` 接收参数
- [ ] 数据预处理逻辑正确（小写转换、添加字段）
- [ ] 测试覆盖多种用户角色场景

**练习13：pytest.ini 配置**

**场景说明**：`pytest.ini` 是 Pytest 的核心配置文件，用于定义测试发现规则、默认参数、自定义标记等，使团队测试风格统一。

**具体需求**：
1. 配置测试路径为 `tests/` 目录
2. 配置文件匹配模式（test_*.py 和 *_test.py）
3. 添加默认命令行参数（-v、--tb=short）
4. 注册自定义标记（smoke、regression、slow、api、ui）
5. 配置忽略警告和最低版本要求

**使用示例**：
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
    -p no:warnings
    --durations=5

# 注册自定义标记
markers =
    smoke: 冒烟测试，核心功能快速验证
    regression: 回归测试，全面功能验证
    slow: 慢速测试，执行时间超过 1s
    api: API 接口测试
    ui: UI 界面测试
    p0: 最高优先级，阻塞性问题
    p1: 高优先级，主要功能
    p2: 中优先级，次要功能

# 忽略特定警告
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning

# 最低版本要求
minversion = 7.0

# 日志配置
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
```

```python
# tests/test_with_config.py
import pytest

@pytest.mark.smoke
def test_smoke():
    """冒烟测试：核心功能验证"""
    assert True

@pytest.mark.regression
def test_regression():
    """回归测试：全面功能验证"""
    assert True

@pytest.mark.api
@pytest.mark.p0
def test_api_critical():
    """P0 优先级 API 测试"""
    assert True

@pytest.mark.slow
def test_slow_operation():
    """慢速测试：需要较长时间"""
    import time
    time.sleep(0.1)
    assert True

# 多标记组合
@pytest.mark.smoke
@pytest.mark.api
def test_smoke_api():
    """冒烟 + API 测试"""
    assert True

@pytest.mark.ui
@pytest.mark.regression
def test_ui_regression():
    """UI + 回归测试"""
    assert True
```

**运行命令**：
```bash
# 运行所有测试（使用 pytest.ini 中的默认参数）
pytest

# 只运行冒烟测试
pytest -m smoke

# 运行 P0 或 P1 优先级测试
pytest -m "p0 or p1"

# 排除慢速测试
pytest -m "not slow"

# 运行 API 测试但不运行慢速测试
pytest -m "api and not slow"

# 查看已注册的标记
pytest --markers
```

**验收标准**：
- [ ] pytest.ini 配置文件语法正确
- [ ] 测试路径配置生效
- [ ] 自定义标记注册成功（`pytest --markers` 可见）
- [ ] 默认参数生效（无需手动添加 -v）
- [ ] 能使用 -m 参数筛选测试

**练习14：登录测试模块（完整版）**

**场景说明**：登录是系统最核心的功能之一，需要测试正常登录、异常登录、边界情况等多种场景。本练习综合运用 fixture、参数化、标记等技术。

**具体需求**：
1. 使用 fixture 提供 API 客户端（模拟登录接口）
2. 使用参数化测试多种登录场景（成功、失败、边界）
3. 使用标记区分冒烟测试（smoke）和回归测试（regression）
4. 测试成功场景：正确用户名密码
5. 测试失败场景：空用户名、空密码、错误密码、锁定账户

**使用示例**：
```python
# tests/test_login.py
import pytest

# 模拟登录 API
class AuthAPI:
    """模拟认证 API"""

    def __init__(self):
        self.users = {
            "admin": {"password": "123456", "locked": False},
            "user": {"password": "password", "locked": False},
            "locked_user": {"password": "123456", "locked": True},
        }

    def login(self, username: str, password: str) -> dict:
        """登录接口"""
        # 参数校验
        if not username or not password:
            return {"success": False, "message": "用户名或密码不能为空"}

        # 用户存在性检查
        if username not in self.users:
            return {"success": False, "message": "用户不存在"}

        # 账户锁定检查
        if self.users[username]["locked"]:
            return {"success": False, "message": "账户已被锁定"}

        # 密码校验
        if self.users[username]["password"] != password:
            return {"success": False, "message": "密码错误"}

        return {"success": True, "message": "登录成功", "token": f"token_{username}"}


class TestLogin:
    """登录测试类"""

    @pytest.fixture
    def api_client(self):
        """提供认证 API 客户端"""
        return AuthAPI()

    # ============================================
    # 成功场景测试
    # ============================================
    @pytest.mark.smoke
    @pytest.mark.parametrize("username,password,expected_success", [
        pytest.param("admin", "123456", True, id="admin登录"),
        pytest.param("user", "password", True, id="普通用户登录"),
    ])
    def test_login_success(self, api_client, username, password, expected_success):
        """测试登录成功场景"""
        result = api_client.login(username, password)

        assert result["success"] == expected_success
        assert "token" in result
        assert result["message"] == "登录成功"

    # ============================================
    # 失败场景测试
    # ============================================
    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,expected_message", [
        pytest.param("", "123456", "用户名或密码不能为空", id="空用户名"),
        pytest.param("admin", "", "用户名或密码不能为空", id="空密码"),
        pytest.param("", "", "用户名或密码不能为空", id="双空"),
        pytest.param("admin", "wrong", "密码错误", id="错误密码"),
        pytest.param("unknown", "123456", "用户不存在", id="不存在的用户"),
        pytest.param("locked_user", "123456", "账户已被锁定", id="锁定账户"),
    ])
    def test_login_fail(self, api_client, username, password, expected_message):
        """测试登录失败场景"""
        result = api_client.login(username, password)

        assert result["success"] is False
        assert result["message"] == expected_message
        assert "token" not in result

    # ============================================
    # 边界和安全测试
    # ============================================
    @pytest.mark.regression
    def test_login_sql_injection_attempt(self, api_client):
        """测试 SQL 注入尝试（应被安全处理）"""
        result = api_client.login("admin' OR '1'='1", "anything")
        assert result["success"] is False
        assert result["message"] == "用户不存在"

    @pytest.mark.regression
    def test_login_xss_attempt(self, api_client):
        """测试 XSS 尝试（应被安全处理）"""
        result = api_client.login("<script>alert(1)</script>", "password")
        assert result["success"] is False
        assert result["message"] == "用户不存在"

    @pytest.mark.smoke
    def test_token_format(self, api_client):
        """测试登录成功后 token 格式"""
        result = api_client.login("admin", "123456")
        assert result["success"] is True
        assert result["token"].startswith("token_")
```

**运行命令**：
```bash
# 运行所有登录测试
pytest tests/test_login.py -v

# 只运行冒烟测试
pytest tests/test_login.py -m smoke -v

# 只运行回归测试
pytest tests/test_login.py -m regression -v

# 查看测试详情
pytest tests/test_login.py -v --tb=short
```

**验收标准**：
- [ ] API 客户端 fixture 正确实现
- [ ] 成功场景至少覆盖 2 种用户
- [ ] 失败场景至少覆盖 5 种情况
- [ ] 正确使用 smoke 和 regression 标记
- [ ] 所有断言通过

**练习15：用户 CRUD 测试**

**场景说明**：CRUD（Create、Read、Update、Delete）是业务系统最基础的操作。本练习测试用户管理模块的完整 CRUD 功能，使用 module 级别 fixture 管理测试数据。

**具体需求**：
1. 实现用户增删改查测试（4 个独立测试方法）
2. 使用 `scope="module"` 级别的 fixture 管理测试数据
3. 使用类组织测试方法
4. 每个操作都有独立测试和断言验证
5. 测试完成后自动清理数据

**使用示例**：
```python
# tests/test_user.py
import pytest
from typing import Dict, List, Optional

# 模拟用户存储
class UserStore:
    """模拟用户数据库"""

    def __init__(self):
        self._users: Dict[int, Dict] = {}
        self._next_id = 1

    def create(self, name: str, email: str, age: int) -> Dict:
        """创建用户"""
        user = {
            "id": self._next_id,
            "name": name,
            "email": email,
            "age": age,
            "is_active": True
        }
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def get(self, user_id: int) -> Optional[Dict]:
        """获取用户"""
        return self._users.get(user_id)

    def get_all(self) -> List[Dict]:
        """获取所有用户"""
        return list(self._users.values())

    def update(self, user_id: int, **kwargs) -> Optional[Dict]:
        """更新用户"""
        if user_id not in self._users:
            return None
        self._users[user_id].update(kwargs)
        return self._users[user_id]

    def delete(self, user_id: int) -> bool:
        """删除用户"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def clear(self):
        """清空所有用户"""
        self._users.clear()
        self._next_id = 1


# ============================================
# Fixtures
# ============================================
@pytest.fixture(scope="module")
def user_store():
    """Module 级别的用户存储（整个模块共享）"""
    store = UserStore()
    print("\n=== 初始化用户存储 ===")
    yield store
    print("\n=== 清理用户存储 ===")
    store.clear()


@pytest.fixture
def test_user(user_store):
    """Function 级别的测试用户（每个测试独立）"""
    # 每个测试前创建一个测试用户
    user = user_store.create(
        name="Test User",
        email="test@example.com",
        age=25
    )
    yield user
    # 测试后清理该用户
    user_store.delete(user["id"])


# ============================================
# 测试类
# ============================================
class TestUserCRUD:
    """用户 CRUD 测试"""

    # ----------------------------------------
    # Create 测试
    # ----------------------------------------
    def test_create_user(self, user_store):
        """测试创建用户"""
        user = user_store.create(
            name="New User",
            email="new@example.com",
            age=30
        )

        # 验证创建结果
        assert user["id"] is not None
        assert user["name"] == "New User"
        assert user["email"] == "new@example.com"
        assert user["age"] == 30
        assert user["is_active"] is True

        # 验证可以获取到
        assert user_store.get(user["id"]) == user

    def test_create_multiple_users(self, user_store):
        """测试创建多个用户"""
        user1 = user_store.create("User1", "user1@test.com", 20)
        user2 = user_store.create("User2", "user2@test.com", 25)

        assert user1["id"] != user2["id"]
        assert len(user_store.get_all()) >= 2

    # ----------------------------------------
    # Read 测试
    # ----------------------------------------
    def test_get_user(self, test_user, user_store):
        """测试获取用户"""
        result = user_store.get(test_user["id"])

        assert result is not None
        assert result["id"] == test_user["id"]
        assert result["name"] == "Test User"

    def test_get_nonexistent_user(self, user_store):
        """测试获取不存在的用户"""
        result = user_store.get(99999)
        assert result is None

    def test_get_all_users(self, user_store):
        """测试获取所有用户"""
        # 先清空确保干净状态
        user_store.clear()

        # 创建几个用户
        user_store.create("User1", "u1@test.com", 20)
        user_store.create("User2", "u2@test.com", 25)

        users = user_store.get_all()
        assert len(users) == 2

    # ----------------------------------------
    # Update 测试
    # ----------------------------------------
    def test_update_user(self, test_user, user_store):
        """测试更新用户"""
        updated = user_store.update(
            test_user["id"],
            name="Updated Name",
            age=30
        )

        assert updated["name"] == "Updated Name"
        assert updated["age"] == 30
        assert updated["email"] == "test@example.com"  # 未修改的字段保持不变

    def test_update_nonexistent_user(self, user_store):
        """测试更新不存在的用户"""
        result = user_store.update(99999, name="New Name")
        assert result is None

    # ----------------------------------------
    # Delete 测试
    # ----------------------------------------
    def test_delete_user(self, user_store):
        """测试删除用户"""
        # 创建一个用户
        user = user_store.create("To Delete", "delete@test.com", 25)
        user_id = user["id"]

        # 删除
        result = user_store.delete(user_id)
        assert result is True

        # 验证已删除
        assert user_store.get(user_id) is None

    def test_delete_nonexistent_user(self, user_store):
        """测试删除不存在的用户"""
        result = user_store.delete(99999)
        assert result is False
```

**运行命令**：
```bash
# 运行用户 CRUD 测试
pytest tests/test_user.py -v

# 运行特定测试方法
pytest tests/test_user.py::TestUserCRUD::test_create_user -v

# 显示 print 输出
pytest tests/test_user.py -s
```

**验收标准**：
- [ ] Create 测试验证用户创建成功
- [ ] Read 测试验证用户获取正确
- [ ] Update 测试验证用户更新成功
- [ ] Delete 测试验证用户删除成功
- [ ] fixture 作用域正确使用
- [ ] 测试间相互独立，无依赖

**练习16：浮点数和近似值测试**

**场景说明**：浮点数计算存在精度问题（如 0.1 + 0.2 ≠ 0.3），直接使用 `==` 断言会失败。Pytest 提供 `pytest.approx` 解决这个问题。

**具体需求**：
1. 使用 `pytest.approx` 测试浮点数近似相等
2. 测试相对误差（`rel`）和绝对误差（`abs`）
3. 测试列表和字典中的浮点数
4. 测试科学计算场景（如平均值、标准差）
5. 理解 `pytest.approx` 的工作原理

**使用示例**：
```python
# tests/test_approx.py
import pytest
import math

# ============================================
# 基础浮点数近似测试
# ============================================
def test_float_approx_basic():
    """测试基础浮点数近似相等"""
    # 经典的浮点精度问题
    result = 0.1 + 0.2

    # ❌ 这会失败！
    # assert result == 0.3

    # ✅ 使用 pytest.approx
    assert result == pytest.approx(0.3)

    # 更多例子
    assert 1.0001 == pytest.approx(1.0, abs=0.001)
    assert 0.9999 == pytest.approx(1.0, abs=0.001)


def test_float_with_tolerance():
    """测试指定误差范围"""
    value = 10.001

    # 相对误差（相对于期望值的百分比）
    # rel=0.01 表示允许 1% 的误差
    assert value == pytest.approx(10, rel=0.01)

    # 绝对误差（固定的误差范围）
    # abs=0.01 表示允许 ±0.01 的误差
    assert value == pytest.approx(10, abs=0.01)

    # 同时指定（满足任一即可）
    assert value == pytest.approx(10, rel=0.01, abs=0.01)


def test_scientific_notation():
    """测试科学计数法"""
    # 非常小的数
    assert 1e-10 == pytest.approx(1.1e-10, rel=0.2)

    # 非常大的数
    assert 1e10 == pytest.approx(1.001e10, rel=0.001)


# ============================================
# 列表和字典中的浮点数
# ============================================
def test_list_approx():
    """测试列表中的浮点数"""
    result = [0.1 + 0.1, 0.2 + 0.2, 0.3 + 0.3]
    expected = [0.2, 0.4, 0.6]

    # 整个列表比较
    assert result == pytest.approx(expected)

    # 嵌套列表
    matrix1 = [[0.1 + 0.1, 0.2], [0.3, 0.4]]
    matrix2 = [[0.2, 0.2], [0.3, 0.4]]
    assert matrix1 == pytest.approx(matrix2)


def test_dict_approx():
    """测试字典中的浮点数"""
    result = {
        "temperature": 36.61,
        "humidity": 65.01,
        "pressure": 1013.25
    }
    expected = {
        "temperature": 36.6,
        "humidity": 65.0,
        "pressure": 1013.25
    }

    assert result == pytest.approx(expected)


def test_nested_structure_approx():
    """测试嵌套结构中的浮点数"""
    data = {
        "sensor1": [0.1 + 0.1, 0.2 + 0.2],
        "sensor2": {"value": 0.3 + 0.3}
    }
    expected = {
        "sensor1": [0.2, 0.4],
        "sensor2": {"value": 0.6}
    }

    assert data == pytest.approx(expected)


# ============================================
# 科学计算场景
# ============================================
def calculate_mean(numbers):
    """计算平均值"""
    return sum(numbers) / len(numbers)


def calculate_std(numbers):
    """计算标准差"""
    mean = calculate_mean(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    return math.sqrt(variance)


def test_mean_calculation():
    """测试平均值计算"""
    numbers = [0.1, 0.2, 0.3, 0.4, 0.5]
    mean = calculate_mean(numbers)

    # 期望值：0.3
    assert mean == pytest.approx(0.3)


def test_std_calculation():
    """测试标准差计算"""
    numbers = [1.0, 2.0, 3.0, 4.0, 5.0]
    std = calculate_std(numbers)

    # 期望标准差：√2 ≈ 1.414213562...
    assert std == pytest.approx(math.sqrt(2))


@pytest.mark.parametrize("values,expected_mean,expected_std", [
    pytest.param([1, 2, 3, 4, 5], 3.0, 1.414213562, id="1到5"),
    pytest.param([0.1, 0.2, 0.3], 0.2, 0.08164966, id="小数"),
    pytest.param([10, 20, 30], 20.0, 8.1649658, id="10的倍数"),
])
def test_statistics_parametrized(values, expected_mean, expected_std):
    """参数化测试统计计算"""
    mean = calculate_mean(values)
    std = calculate_std(values)

    assert mean == pytest.approx(expected_mean)
    assert std == pytest.approx(expected_std)


# ============================================
# 特殊情况和边界
# ============================================
def test_zero_approx():
    """测试零值近似"""
    # 零值需要特别小心，相对误差可能不适用
    assert 0.0001 == pytest.approx(0, abs=0.001)


def test_negative_approx():
    """测试负数近似"""
    assert -0.1 + (-0.2) == pytest.approx(-0.3)
    assert -10.001 == pytest.approx(-10, abs=0.01)


def test_nan_and_inf():
    """测试 NaN 和无穷大"""
    import math

    # NaN 比较总是 False
    assert math.nan != pytest.approx(math.nan)

    # 无穷大可以比较
    assert float('inf') == pytest.approx(float('inf'))
    assert float('-inf') == pytest.approx(float('-inf'))
```

**运行命令**：
```bash
# 运行浮点数测试
pytest tests/test_approx.py -v

# 运行参数化测试
pytest tests/test_approx.py::test_statistics_parametrized -v
```

**验收标准**：
- [ ] 理解浮点精度问题
- [ ] 正确使用 `pytest.approx`
- [ ] 掌握 `rel` 和 `abs` 参数
- [ ] 能测试列表和字典中的浮点数
- [ ] 所有测试通过

### 综合练习（17-20）

---

**练习17：搭建完整测试项目**

**场景说明**：在实际工作中，测试项目需要有规范的目录结构、配置文件、共享 fixture 等。本练习搭建一个完整的 Pytest 测试项目框架。

**具体需求**：
1. 创建标准项目目录结构
2. 编写 `pytest.ini` 配置文件
3. 编写根目录 `conftest.py` 全局 fixture
4. 编写测试目录 `conftest.py` 局部 fixture
5. 实现登录、用户、订单三个测试模块
6. 总共至少 15 个测试用例

**项目结构**：
```
pytest_demo/
├── pytest.ini              # Pytest 配置文件
├── conftest.py             # 全局 fixture
├── config/
│   ├── __init__.py
│   └── settings.py         # 配置管理
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # 测试级 fixture
│   ├── test_login.py       # 登录测试（5 个用例）
│   ├── test_user.py        # 用户测试（5 个用例）
│   └── test_order.py       # 订单测试（5 个用例）
├── utils/
│   ├── __init__.py
│   └── helpers.py          # 工具函数
└── requirements.txt        # 依赖列表
```

**使用示例**：

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts =
    -v
    --tb=short
    --durations=5
    -p no:warnings

markers =
    smoke: 冒烟测试
    regression: 回归测试
    api: API 测试
    slow: 慢速测试

minversion = 7.0
```

```python
# config/settings.py
"""项目配置"""

class Config:
    """基础配置"""
    BASE_URL = "https://api.example.com"
    TIMEOUT = 30
    DEBUG = False

class TestConfig(Config):
    """测试环境配置"""
    BASE_URL = "https://test.api.example.com"
    DEBUG = True

class DevConfig(Config):
    """开发环境配置"""
    BASE_URL = "http://localhost:8000"
    DEBUG = True

# 配置映射
CONFIGS = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": Config
}

def get_config(env="test"):
    """获取配置"""
    return CONFIGS.get(env, TestConfig)()
```

```python
# conftest.py（根目录）
"""全局 fixture 定义"""
import pytest
from config.settings import get_config

@pytest.fixture(scope="session")
def config(request):
    """Session 级别的配置对象"""
    # 从命令行获取环境参数，默认 test
    env = request.config.getoption("--env", default="test")
    return get_config(env)

@pytest.fixture(scope="session")
def base_url(config):
    """Session 级别的基础 URL"""
    return config.BASE_URL

def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--env",
        default="test",
        choices=["dev", "test", "prod"],
        help="测试环境: dev, test, prod"
    )
```

```python
# tests/conftest.py
"""测试级 fixture 定义"""
import pytest

@pytest.fixture
def api_client(base_url):
    """Function 级别的 API 客户端"""
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url
            self.token = None

        def set_token(self, token):
            self.token = token

        def get(self, endpoint):
            return {"status": 200, "url": f"{self.base_url}{endpoint}"}

        def post(self, endpoint, data):
            return {"status": 201, "url": f"{self.base_url}{endpoint}", "data": data}

    return APIClient(base_url)

@pytest.fixture
def auth_headers(api_client):
    """认证请求头"""
    return {
        "Authorization": f"Bearer {api_client.token}",
        "Content-Type": "application/json"
    }
```

```python
# tests/test_login.py
"""登录模块测试"""
import pytest

class TestLogin:
    """登录测试类"""

    @pytest.mark.smoke
    def test_login_success(self, api_client):
        """测试登录成功"""
        result = api_client.post("/login", {
            "username": "admin",
            "password": "123456"
        })
        assert result["status"] == 201

    @pytest.mark.smoke
    def test_login_with_token(self, api_client):
        """测试登录后获取 token"""
        api_client.set_token("mock_token_123")
        assert api_client.token == "mock_token_123"

    @pytest.mark.regression
    def test_login_empty_username(self, api_client):
        """测试空用户名"""
        result = api_client.post("/login", {"username": "", "password": "123456"})
        assert result["status"] in [201, 400]

    @pytest.mark.regression
    def test_login_empty_password(self, api_client):
        """测试空密码"""
        result = api_client.post("/login", {"username": "admin", "password": ""})
        assert result["status"] in [201, 400]

    @pytest.mark.api
    def test_logout(self, api_client):
        """测试登出"""
        result = api_client.post("/logout", {})
        assert result["status"] == 201
```

```python
# tests/test_user.py
"""用户模块测试"""
import pytest

class TestUser:
    """用户测试类"""

    @pytest.mark.smoke
    def test_get_user_list(self, api_client):
        """测试获取用户列表"""
        result = api_client.get("/users")
        assert result["status"] == 200

    @pytest.mark.regression
    def test_create_user(self, api_client):
        """测试创建用户"""
        result = api_client.post("/users", {
            "name": "Test User",
            "email": "test@example.com"
        })
        assert result["status"] == 201

    @pytest.mark.regression
    def test_get_user_by_id(self, api_client):
        """测试获取单个用户"""
        result = api_client.get("/users/1")
        assert result["status"] == 200

    @pytest.mark.regression
    def test_update_user(self, api_client):
        """测试更新用户"""
        result = api_client.post("/users/1", {"name": "Updated"})
        assert result["status"] == 201

    @pytest.mark.api
    def test_delete_user(self, api_client):
        """测试删除用户"""
        result = api_client.get("/users/1/delete")
        assert result["status"] == 200
```

```python
# tests/test_order.py
"""订单模块测试"""
import pytest

@pytest.mark.api
class TestOrder:
    """订单测试类"""

    @pytest.mark.smoke
    def test_create_order(self, api_client):
        """测试创建订单"""
        result = api_client.post("/orders", {
            "user_id": 1,
            "product_id": 100,
            "quantity": 2
        })
        assert result["status"] == 201

    @pytest.mark.regression
    def test_get_order_list(self, api_client):
        """测试获取订单列表"""
        result = api_client.get("/orders")
        assert result["status"] == 200

    @pytest.mark.regression
    def test_get_order_by_id(self, api_client):
        """测试获取订单详情"""
        result = api_client.get("/orders/1")
        assert result["status"] == 200

    @pytest.mark.regression
    def test_cancel_order(self, api_client):
        """测试取消订单"""
        result = api_client.post("/orders/1/cancel", {})
        assert result["status"] == 201

    @pytest.mark.regression
    def test_order_status_flow(self, api_client):
        """测试订单状态流转"""
        # 创建 -> 支付 -> 发货 -> 完成
        result = api_client.post("/orders", {"status": "created"})
        assert result["status"] == 201
```

```text
# requirements.txt
pytest>=7.0.0
pytest-html>=3.0.0
pytest-xdist>=3.0.0
requests>=2.28.0
```

**运行命令**：
```bash
# 运行所有测试
pytest

# 指定环境运行
pytest --env=dev
pytest --env=test

# 只运行冒烟测试
pytest -m smoke

# 并行运行
pytest -n 4

# 生成 HTML 报告
pytest --html=reports/report.html --self-contained-html
```

**验收标准**：
- [ ] 项目目录结构完整规范
- [ ] pytest.ini 配置正确
- [ ] conftest.py fixture 定义合理
- [ ] 至少 15 个测试用例全部通过
- [ ] 能使用 -m 参数筛选测试
- [ ] 能使用 --env 参数切换环境

**练习18：数据驱动测试框架**

**场景说明**：数据驱动测试（Data-Driven Testing）将测试数据与测试逻辑分离，通过外部数据文件驱动测试执行，便于维护和扩展测试用例。

**具体需求**：
1. 创建 JSON/YAML 格式的测试数据文件
2. 编写数据加载函数，从文件读取测试数据
3. 使用参数化实现数据驱动
4. 支持数据文件的动态加载和扩展
5. 实现测试数据与测试代码的完全分离

**使用示例**：

```json
# tests/data/login_cases.json
[
    {
        "id": "valid_admin",
        "description": "管理员登录成功",
        "username": "admin",
        "password": "123456",
        "expected": {"success": true, "message": "登录成功"}
    },
    {
        "id": "valid_user",
        "description": "普通用户登录成功",
        "username": "user",
        "password": "password",
        "expected": {"success": true, "message": "登录成功"}
    },
    {
        "id": "empty_username",
        "description": "空用户名",
        "username": "",
        "password": "123456",
        "expected": {"success": false, "message": "用户名不能为空"}
    },
    {
        "id": "empty_password",
        "description": "空密码",
        "username": "admin",
        "password": "",
        "expected": {"success": false, "message": "密码不能为空"}
    },
    {
        "id": "wrong_password",
        "description": "错误密码",
        "username": "admin",
        "password": "wrong",
        "expected": {"success": false, "message": "密码错误"}
    }
]
```

```json
# tests/data/calculator_cases.json
[
    {"id": "add_1", "a": 1, "b": 2, "operation": "add", "expected": 3},
    {"id": "add_2", "a": -1, "b": 1, "operation": "add", "expected": 0},
    {"id": "sub_1", "a": 5, "b": 3, "operation": "subtract", "expected": 2},
    {"id": "mul_1", "a": 4, "b": 3, "operation": "multiply", "expected": 12},
    {"id": "div_1", "a": 10, "b": 2, "operation": "divide", "expected": 5},
    {"id": "div_2", "a": 7, "b": 2, "operation": "divide", "expected": 3.5}
]
```

```python
# utils/data_loader.py
"""测试数据加载工具"""
import json
import os
from typing import List, Dict, Any

def load_json_data(filepath: str) -> List[Dict[str, Any]]:
    """
    从 JSON 文件加载测试数据

    Args:
        filepath: JSON 文件路径（相对于 tests/data/ 目录）

    Returns:
        测试数据列表
    """
    # 获取数据文件完整路径
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_dir, "tests", "data", filepath)

    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml_data(filepath: str) -> List[Dict[str, Any]]:
    """
    从 YAML 文件加载测试数据（需要安装 PyYAML）

    Args:
        filepath: YAML 文件路径

    Returns:
        测试数据列表
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("请安装 PyYAML: pip install pyyaml")

    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_dir, "tests", "data", filepath)

    with open(full_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_test_ids(data: List[Dict[str, Any]], id_key: str = "id") -> List[str]:
    """
    从测试数据中提取测试 ID

    Args:
        data: 测试数据列表
        id_key: ID 字段名

    Returns:
        测试 ID 列表
    """
    return [item.get(id_key, f"test_{i}") for i, item in enumerate(data)]
```

```python
# tests/test_data_driven.py
"""数据驱动测试示例"""
import pytest
from utils.data_loader import load_json_data, get_test_ids

# ============================================
# 登录数据驱动测试
# ============================================
# 加载测试数据
login_cases = load_json_data("login_cases.json")

@pytest.mark.parametrize("case", login_cases, ids=get_test_ids(login_cases))
def test_login_data_driven(case):
    """数据驱动登录测试"""
    # 模拟登录逻辑
    def mock_login(username, password):
        if not username:
            return {"success": False, "message": "用户名不能为空"}
        if not password:
            return {"success": False, "message": "密码不能为空"}
        if username == "admin" and password == "123456":
            return {"success": True, "message": "登录成功"}
        if username == "user" and password == "password":
            return {"success": True, "message": "登录成功"}
        return {"success": False, "message": "密码错误"}

    # 执行登录
    result = mock_login(case["username"], case["password"])

    # 验证结果
    assert result["success"] == case["expected"]["success"]
    assert result["message"] == case["expected"]["message"]


# ============================================
# 计算器数据驱动测试
# ============================================
calc_cases = load_json_data("calculator_cases.json")

def calculate(a: float, b: float, operation: str) -> float:
    """计算器函数"""
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else float("inf")
    }
    return operations.get(operation, 0)

@pytest.mark.parametrize("case", calc_cases, ids=get_test_ids(calc_cases))
def test_calculator_data_driven(case):
    """数据驱动计算器测试"""
    result = calculate(case["a"], case["b"], case["operation"])
    assert result == pytest.approx(case["expected"])


# ============================================
# 动态生成测试数据
# ============================================
def generate_boundary_test_cases():
    """生成边界值测试数据"""
    cases = []

    # 数值边界
    for value in [0, 1, -1, 100, -100, 999999]:
        cases.append({
            "id": f"boundary_{value}",
            "input": value,
            "description": f"边界值测试: {value}"
        })

    # 字符串边界
    for s in ["", "a", "a" * 100, " "]:
        cases.append({
            "id": f"string_boundary_{len(s)}",
            "input": s,
            "description": f"字符串边界: 长度 {len(s)}"
        })

    return cases

@pytest.mark.parametrize("case", generate_boundary_test_cases())
def test_boundary_cases(case):
    """边界值测试"""
    # 这里可以根据具体业务逻辑实现
    assert True


# ============================================
# CSV 数据驱动（扩展）
# ============================================
import csv

def load_csv_data(filepath: str) -> List[Dict[str, Any]]:
    """从 CSV 文件加载测试数据"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    full_path = os.path.join(base_dir, "tests", "data", filepath)

    with open(full_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
```

**运行命令**：
```bash
# 运行数据驱动测试
pytest tests/test_data_driven.py -v

# 查看测试 ID
pytest tests/test_data_driven.py -v --collect-only

# 只运行特定 ID 的测试
pytest tests/test_data_driven.py -k "valid" -v
```

**验收标准**：
- [ ] JSON 测试数据文件格式正确
- [ ] 数据加载函数正确实现
- [ ] 参数化正确使用外部数据
- [ ] 测试 ID 可读性好
- [ ] 支持数据文件扩展（添加新用例无需修改代码）

**练习19：命令行参数测试**

**场景说明**：在多环境测试中，需要通过命令行参数指定测试环境、配置等。本练习实现自定义命令行参数，使测试可以在不同环境下灵活运行。

**具体需求**：
1. 添加 `--env` 命令行参数（支持 dev/test/prod）
2. 添加 `--browser` 命令行参数（支持 chrome/firefox/safari）
3. 添加 `--headless` 命令行参数（无头模式开关）
4. 根据参数加载不同环境配置
5. 在测试中使用这些配置

**使用示例**：

```python
# conftest.py
"""命令行参数和全局配置"""
import pytest
from typing import Dict, Any

# ============================================
# 环境配置
# ============================================
ENVIRONMENTS = {
    "dev": {
        "base_url": "http://localhost:8000",
        "api_url": "http://localhost:8000/api/v1",
        "db_host": "localhost",
        "db_port": 3306,
        "timeout": 60,
        "debug": True
    },
    "test": {
        "base_url": "https://test.example.com",
        "api_url": "https://test.example.com/api/v1",
        "db_host": "test-db.example.com",
        "db_port": 3306,
        "timeout": 30,
        "debug": False
    },
    "prod": {
        "base_url": "https://example.com",
        "api_url": "https://example.com/api/v1",
        "db_host": "prod-db.example.com",
        "db_port": 3306,
        "timeout": 10,
        "debug": False
    }
}

BROWSER_CONFIGS = {
    "chrome": {
        "driver": "chromedriver",
        "options": ["--start-maximized", "--disable-extensions"]
    },
    "firefox": {
        "driver": "geckodriver",
        "options": ["--width=1920", "--height=1080"]
    },
    "safari": {
        "driver": "safaridriver",
        "options": []
    }
}


# ============================================
# 注册命令行参数
# ============================================
def pytest_addoption(parser):
    """注册自定义命令行参数"""

    # 环境参数
    parser.addoption(
        "--env",
        action="store",
        default="test",
        choices=["dev", "test", "prod"],
        help="测试环境: dev, test, prod (默认: test)"
    )

    # 浏览器参数
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "safari"],
        help="浏览器类型: chrome, firefox, safari (默认: chrome)"
    )

    # 无头模式
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="启用无头模式运行浏览器"
    )

    # 重试次数
    parser.addoption(
        "--reruns",
        action="store",
        default=0,
        type=int,
        help="失败重试次数 (默认: 0)"
    )

    # 并行数
    parser.addoption(
        "--workers",
        action="store",
        default=1,
        type=int,
        help="并行工作进程数 (默认: 1)"
    )


# ============================================
# Fixtures
# ============================================
@pytest.fixture(scope="session")
def env(request):
    """获取当前测试环境"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def env_config(env) -> Dict[str, Any]:
    """获取环境配置"""
    return ENVIRONMENTS[env]


@pytest.fixture(scope="session")
def base_url(env_config) -> str:
    """获取基础 URL"""
    return env_config["base_url"]


@pytest.fixture(scope="session")
def api_url(env_config) -> str:
    """获取 API URL"""
    return env_config["api_url"]


@pytest.fixture(scope="session")
def browser(request) -> str:
    """获取浏览器类型"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request) -> bool:
    """获取无头模式设置"""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def browser_config(browser) -> Dict[str, Any]:
    """获取浏览器配置"""
    return BROWSER_CONFIGS[browser]


@pytest.fixture
def api_client(api_url, env_config):
    """API 客户端 fixture"""
    class APIClient:
        def __init__(self, base_url, timeout):
            self.base_url = base_url
            self.timeout = timeout

        def get(self, endpoint):
            print(f"GET {self.base_url}{endpoint} (timeout={self.timeout}s)")
            return {"status": 200}

        def post(self, endpoint, data):
            print(f"POST {self.base_url}{endpoint}")
            return {"status": 201, "data": data}

    return APIClient(api_url, env_config["timeout"])
```

```python
# tests/test_with_env.py
"""使用环境配置的测试"""
import pytest

class TestEnvironmentConfig:
    """环境配置测试"""

    def test_env_is_valid(self, env):
        """测试环境参数有效"""
        assert env in ["dev", "test", "prod"]

    def test_base_url_not_empty(self, base_url):
        """测试基础 URL 不为空"""
        assert base_url.startswith("http")

    def test_api_url_format(self, api_url):
        """测试 API URL 格式"""
        assert "/api" in api_url

    def test_debug_mode_dev(self, env, env_config):
        """测试开发环境开启 debug"""
        if env == "dev":
            assert env_config["debug"] is True
        else:
            assert env_config["debug"] is False

    def test_timeout_values(self, env_config):
        """测试超时配置合理"""
        assert 1 <= env_config["timeout"] <= 120


class TestBrowserConfig:
    """浏览器配置测试"""

    def test_browser_is_valid(self, browser):
        """测试浏览器类型有效"""
        assert browser in ["chrome", "firefox", "safari"]

    def test_browser_config_exists(self, browser_config):
        """测试浏览器配置存在"""
        assert "driver" in browser_config
        assert "options" in browser_config

    def test_headless_mode(self, headless, browser):
        """测试无头模式"""
        if headless:
            print(f"在 {browser} 上运行无头模式")
        assert isinstance(headless, bool)


class TestAPIClient:
    """API 客户端测试"""

    @pytest.mark.smoke
    def test_api_get(self, api_client):
        """测试 API GET 请求"""
        result = api_client.get("/users")
        assert result["status"] == 200

    @pytest.mark.smoke
    def test_api_post(self, api_client):
        """测试 API POST 请求"""
        result = api_client.post("/users", {"name": "test"})
        assert result["status"] == 201

    @pytest.mark.regression
    def test_api_url_based_on_env(self, api_client, env):
        """测试 API URL 根据环境变化"""
        if env == "dev":
            assert "localhost" in api_client.base_url
        elif env == "test":
            assert "test." in api_client.base_url
        elif env == "prod":
            assert "example.com" in api_client.base_url
            assert "test." not in api_client.base_url
```

**运行命令**：
```bash
# 在测试环境运行（默认）
pytest tests/test_with_env.py -v

# 在开发环境运行
pytest tests/test_with_env.py --env=dev -v

# 在生产环境运行（注意：生产环境要谨慎！）
pytest tests/test_with_env.py --env=prod -v

# 使用 Firefox 无头模式
pytest tests/test_with_env.py --browser=firefox --headless -v

# 组合参数
pytest tests/test_with_env.py --env=dev --browser=chrome --headless -v

# 查看帮助
pytest --help | grep -A 5 "custom options"
```

**验收标准**：
- [ ] `--env` 参数正确注册
- [ ] `--browser` 参数正确注册
- [ ] `--headless` 参数正确注册
- [ ] 环境配置根据参数正确加载
- [ ] 测试能正确使用配置值

**练习20：综合测试套件**

**场景说明**：综合运用本章所学知识，搭建一个完整的测试套件，包含 fixture、参数化、标记、配置、异常处理等技术点。

**具体需求**：
1. 使用 `conftest.py` 定义共享 fixture（多种作用域）
2. 使用参数化测试（`@pytest.mark.parametrize`）
3. 使用标记分类测试（smoke、regression、api、slow）
4. 使用 `pytest.ini` 配置
5. 测试异常和边界情况
6. 实现数据驱动测试

**使用示例**：

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts =
    -v
    --tb=short
    --durations=5

markers =
    smoke: 冒烟测试
    regression: 回归测试
    api: API 测试
    slow: 慢速测试
    p0: 最高优先级

minversion = 7.0
```

```python
# conftest.py
"""综合测试套件配置"""
import pytest
import tempfile
import shutil
import os
from typing import Dict, Any

# ============================================
# Session 级别 fixture
# ============================================
@pytest.fixture(scope="session")
def app_config():
    """Session 级别：应用配置（整个测试会话只加载一次）"""
    print("\n=== [Session] 加载应用配置 ===")
    config = {
        "app_name": "测试应用",
        "version": "1.0.0",
        "debug": True
    }
    return config


@pytest.fixture(scope="session")
def database_config():
    """Session 级别：数据库配置"""
    return {
        "host": "localhost",
        "port": 3306,
        "database": "test_db"
    }


# ============================================
# Module 级别 fixture
# ============================================
@pytest.fixture(scope="module")
def api_base_url():
    """Module 级别：API 基础 URL"""
    print("\n=== [Module] 设置 API URL ===")
    return "https://api.example.com"


# ============================================
# Class 级别 fixture
# ============================================
@pytest.fixture(scope="class")
def class_shared_data():
    """Class 级别：类共享数据"""
    print("\n  >>> [Class] 初始化共享数据")
    data = {"counter": 0, "items": []}
    yield data
    print("\n  >>> [Class] 清理共享数据")


# ============================================
# Function 级别 fixture
# ============================================
@pytest.fixture
def temp_directory():
    """Function 级别：临时目录"""
    dirpath = tempfile.mkdtemp(prefix="pytest_test_")
    print(f"\n    >>> [Function] 创建临时目录: {dirpath}")
    yield dirpath
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
        print(f"\n    >>> [Function] 删除临时目录: {dirpath}")


@pytest.fixture
def sample_user():
    """Function 级别：示例用户数据"""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "user"
    }


@pytest.fixture
def sample_products():
    """Function 级别：示例商品数据"""
    return [
        {"id": 1, "name": "商品A", "price": 100.0, "stock": 10},
        {"id": 2, "name": "商品B", "price": 200.0, "stock": 5},
        {"id": 3, "name": "商品C", "price": 50.0, "stock": 20},
    ]


# ============================================
# 带参数的 fixture
# ============================================
@pytest.fixture(params=[
    {"username": "admin", "role": "admin"},
    {"username": "user", "role": "user"},
    {"username": "guest", "role": "guest"},
], ids=["管理员", "普通用户", "访客"])
def user_with_role(request):
    """参数化 fixture：不同角色的用户"""
    return request.param
```

```python
# tests/test_comprehensive.py
"""综合测试套件"""
import pytest
import os

# ============================================
# 业务逻辑
# ============================================
class Calculator:
    """计算器类"""

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b


class UserService:
    """用户服务类"""

    def __init__(self):
        self.users = {}

    def create_user(self, user_id, username, email):
        if user_id in self.users:
            raise ValueError(f"用户 ID {user_id} 已存在")
        if not username:
            raise ValueError("用户名不能为空")
        if "@" not in email:
            raise ValueError("邮箱格式不正确")

        self.users[user_id] = {
            "id": user_id,
            "username": username,
            "email": email
        }
        return self.users[user_id]

    def get_user(self, user_id):
        return self.users.get(user_id)

    def delete_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


# ============================================
# 测试类
# ============================================
@pytest.mark.api
class TestComprehensiveSuite:
    """综合测试套件"""

    # ----------------------------------------
    # 基础测试
    # ----------------------------------------
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_smoke_suite(self, app_config, api_base_url):
        """冒烟测试：验证基础配置"""
        assert app_config["app_name"] == "测试应用"
        assert api_base_url.startswith("https://")

    @pytest.mark.smoke
    def test_app_config_loaded(self, app_config):
        """测试配置已加载"""
        assert "version" in app_config
        assert app_config["debug"] is True

    # ----------------------------------------
    # 参数化测试
    # ----------------------------------------
    @pytest.mark.parametrize("a,b,expected", [
        pytest.param(1, 2, 3, id="正数相加"),
        pytest.param(-1, 1, 0, id="正负相加"),
        pytest.param(0, 0, 0, id="零相加"),
        pytest.param(100, -50, 50, id="大数相加"),
    ])
    def test_calculator_add(self, a, b, expected):
        """参数化测试：加法"""
        assert Calculator.add(a, b) == expected

    @pytest.mark.parametrize("a,b,expected", [
        pytest.param(10, 2, 5, id="整除"),
        pytest.param(7, 2, 3.5, id="非整除"),
        pytest.param(-6, 2, -3, id="负数除法"),
    ])
    def test_calculator_divide(self, a, b, expected):
        """参数化测试：除法"""
        assert Calculator.divide(a, b) == pytest.approx(expected)

    # ----------------------------------------
    # 异常测试
    # ----------------------------------------
    @pytest.mark.regression
    def test_divide_by_zero(self):
        """测试除零异常"""
        with pytest.raises(ValueError) as excinfo:
            Calculator.divide(10, 0)
        assert "除数不能为零" in str(excinfo.value)

    @pytest.mark.regression
    def test_create_duplicate_user(self):
        """测试创建重复用户"""
        service = UserService()
        service.create_user(1, "user1", "user1@test.com")

        with pytest.raises(ValueError) as excinfo:
            service.create_user(1, "user2", "user2@test.com")
        assert "已存在" in str(excinfo.value)

    @pytest.mark.parametrize("username,email,error_msg", [
        pytest.param("", "test@test.com", "用户名不能为空", id="空用户名"),
        pytest.param("test", "invalid", "邮箱格式不正确", id="无效邮箱"),
    ])
    def test_create_user_validation(self, username, email, error_msg):
        """参数化异常测试：用户验证"""
        service = UserService()
        with pytest.raises(ValueError) as excinfo:
            service.create_user(1, username, email)
        assert error_msg in str(excinfo.value)

    # ----------------------------------------
    # fixture 使用测试
    # ----------------------------------------
    @pytest.mark.regression
    def test_temp_directory_fixture(self, temp_directory):
        """测试临时目录 fixture"""
        # 创建测试文件
        test_file = os.path.join(temp_directory, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        # 验证文件存在
        assert os.path.exists(test_file)

        # 读取验证
        with open(test_file, "r") as f:
            assert f.read() == "test content"

    @pytest.mark.regression
    def test_sample_user_fixture(self, sample_user):
        """测试示例用户 fixture"""
        assert sample_user["id"] == 1
        assert sample_user["username"] == "testuser"
        assert "@" in sample_user["email"]

    @pytest.mark.regression
    def test_sample_products_fixture(self, sample_products):
        """测试示例商品 fixture"""
        assert len(sample_products) == 3
        total_price = sum(p["price"] for p in sample_products)
        assert total_price == pytest.approx(350.0)

    # ----------------------------------------
    # 参数化 fixture 测试
    # ----------------------------------------
    @pytest.mark.regression
    def test_user_with_role(self, user_with_role):
        """测试参数化 fixture：不同角色用户"""
        assert user_with_role["role"] in ["admin", "user", "guest"]

        # 根据角色验证不同权限
        if user_with_role["role"] == "admin":
            assert user_with_role["username"] == "admin"
        elif user_with_role["role"] == "user":
            assert user_with_role["username"] == "user"
        else:
            assert user_with_role["username"] == "guest"

    # ----------------------------------------
    # 边界测试
    # ----------------------------------------
    @pytest.mark.regression
    @pytest.mark.parametrize("value", [
        pytest.param(0, id="零"),
        pytest.param(-1, id="负数"),
        pytest.param(1, id="正数"),
        pytest.param(1e10, id="大数"),
        pytest.param(-1e10, id="负大数"),
        pytest.param(0.000001, id="小数"),
    ])
    def test_boundary_values(self, value):
        """边界值测试"""
        # 零的特殊处理
        if value == 0:
            assert value == 0
        # 正数
        elif value > 0:
            assert value > 0
        # 负数
        else:
            assert value < 0

    # ----------------------------------------
    # 慢速测试示例
    # ----------------------------------------
    @pytest.mark.slow
    @pytest.mark.skip(reason="示例：跳过慢速测试")
    def test_slow_operation(self):
        """慢速测试示例（已跳过）"""
        import time
        time.sleep(5)
        assert True


# ============================================
# 类级别 fixture 测试
# ============================================
@pytest.mark.usefixtures("class_shared_data")
class TestWithClassFixture:
    """使用类级别 fixture 的测试"""

    def test_class_shared_data_1(self, class_shared_data):
        """测试类共享数据 1"""
        class_shared_data["counter"] += 1
        assert class_shared_data["counter"] == 1

    def test_class_shared_data_2(self, class_shared_data):
        """测试类共享数据 2（会累积）"""
        class_shared_data["counter"] += 1
        assert class_shared_data["counter"] == 2
```

**运行命令**：
```bash
# 运行综合测试套件
pytest tests/test_comprehensive.py -v

# 只运行冒烟测试
pytest tests/test_comprehensive.py -m smoke -v

# 运行非慢速测试
pytest tests/test_comprehensive.py -m "not slow" -v

# 显示 fixture 作用域
pytest tests/test_comprehensive.py --setup-show -v

# 生成覆盖率报告
pytest tests/test_comprehensive.py --cov=. --cov-report=html

# 详细输出
pytest tests/test_comprehensive.py -v --tb=long -s
```

**验收标准**：
- [ ] conftest.py 包含多种作用域 fixture
- [ ] 参数化测试正确使用
- [ ] 标记分类清晰（smoke、regression、api、slow）
- [ ] 异常测试覆盖边界情况
- [ ] 所有测试通过
- [ ] 能使用 -m 参数筛选测试

---

## 五、检验标准

### 自测题

---

#### 题目1：临时目录 fixture（综合考察：fixture、yield、资源管理）

**场景描述**：在测试中经常需要创建临时文件或目录，测试完成后需要清理。

**详细需求**：
1. 创建 `temp_dir` fixture，在测试前创建临时目录
2. 使用 `yield` 返回目录路径
3. 测试后自动删除整个目录
4. 编写测试用例验证临时目录功能
5. 测试完成后确认目录已被删除

**测试用例**：
```python
import pytest
import os

def test_temp_dir_fixture():
    """验证 temp_dir fixture 的功能"""
    # 使用 fixture 创建临时目录
    pass

def test_file_operations_in_temp():
    """测试在临时目录中进行文件操作"""
    # 1. 在临时目录创建文件
    # 2. 写入内容
    # 3. 读取验证
    pass
```

---

#### 题目2：参数化字符串测试（综合考察：参数化、测试 ID）

**场景描述**：对字符串反转函数进行全面的参数化测试。

**详细需求**：
1. 定义 `reverse_string(s)` 函数
2. 测试普通字符串、空字符串、单字符
3. 测试特殊字符、中文、混合内容
4. 使用 `pytest.param` 添加测试 ID
5. 至少 8 组测试数据

**测试用例**：
```python
import pytest

def reverse_string(s):
    """字符串反转"""
    return s[::-1]

# 使用 pytest.param 添加测试 ID
@pytest.mark.parametrize("input,expected", [
    pytest.param("hello", "olleh", id="普通英文"),
    pytest.param("", "", id="空字符串"),
    pytest.param("a", "a", id="单字符"),
    pytest.param("ab", "ba", id="两字符"),
    pytest.param("12345", "54321", id="数字"),
    pytest.param("Hello World", "dlroW olleH", id="带空格"),
    pytest.param("你好", "好你", id="中文"),
    pytest.param("a1b2c3", "3c2b1a", id="混合"),
])
def test_reverse_string(input, expected):
    """参数化测试字符串反转"""
    pass
```

---

#### 题目3：conftest.py 与 API 客户端（综合考察：conftest、fixture 依赖）

**场景描述**：创建全局的 API 客户端 fixture，供多个测试文件使用。

**详细需求**：
1. 在 `conftest.py` 中定义 `api_client` fixture（session 级别）
2. 定义 `auth_token` fixture 依赖 `api_client`
3. 定义 `authenticated_client` fixture 组合两者
4. 编写测试用例使用这些 fixture
5. 验证 fixture 的依赖关系

**项目结构**：
```
tests/
├── conftest.py          # 全局 fixture
├── test_api_client.py   # 测试 API 客户端
└── test_auth.py         # 测试认证
```

**测试用例**：
```python
# tests/test_api_client.py
def test_api_client_available(api_client):
    """测试 API 客户端可用"""
    pass

def test_authenticated_request(authenticated_client):
    """测试认证后的请求"""
    pass
```

---

### 答案

#### 题目1 答案

```python
# tests/conftest.py
import pytest
import tempfile
import shutil
import os

@pytest.fixture
def temp_dir():
    """临时目录 fixture"""
    # Setup - 创建临时目录
    dirpath = tempfile.mkdtemp(prefix="pytest_test_")
    print(f"\n创建临时目录: {dirpath}")

    yield dirpath  # 返回给测试用例

    # Teardown - 删除临时目录
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
        print(f"\n删除临时目录: {dirpath}")

# tests/test_temp_fixture.py
import os

def test_temp_dir_fixture(temp_dir):
    """验证临时目录 fixture 的功能"""
    # 验证目录存在
    assert os.path.exists(temp_dir)
    assert os.path.isdir(temp_dir)
    print(f"临时目录路径: {temp_dir}")

def test_file_operations_in_temp(temp_dir):
    """测试在临时目录中进行文件操作"""
    # 1. 创建文件
    filepath = os.path.join(temp_dir, "test.txt")

    # 2. 写入内容
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Hello, Pytest!")

    # 3. 读取验证
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "Hello, Pytest!"

    # 验证文件存在
    assert os.path.exists(filepath)

def test_multiple_files_in_temp(temp_dir):
    """测试在临时目录中创建多个文件"""
    files = ["file1.txt", "file2.txt", "file3.txt"]

    for filename in files:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, "w") as f:
            f.write(filename)

    # 验证所有文件都创建成功
    created_files = os.listdir(temp_dir)
    assert len(created_files) == 3
    assert set(created_files) == set(files)
```

#### 题目2 答案

```python
# tests/test_string_reverse.py
import pytest

def reverse_string(s):
    """字符串反转"""
    if not isinstance(s, str):
        raise TypeError("输入必须是字符串")
    return s[::-1]

@pytest.mark.parametrize("input,expected", [
    pytest.param("hello", "olleh", id="普通英文"),
    pytest.param("", "", id="空字符串"),
    pytest.param("a", "a", id="单字符"),
    pytest.param("ab", "ba", id="两字符"),
    pytest.param("12345", "54321", id="数字"),
    pytest.param("Hello World", "dlroW olleH", id="带空格"),
    pytest.param("你好世界", "界世好你", id="中文"),
    pytest.param("a1b2c3", "3c2b1a", id="混合"),
    pytest.param("  spaces  ", "  secaps  ", id="带空格两端"),
    pytest.param("AaBbCc", "cCbBaA", id="大小写混合"),
])
def test_reverse_string(input, expected):
    """参数化测试字符串反转"""
    result = reverse_string(input)
    assert result == expected

def test_reverse_string_type_error():
    """测试非字符串输入"""
    with pytest.raises(TypeError) as excinfo:
        reverse_string(123)
    assert "输入必须是字符串" in str(excinfo.value)

def test_reverse_preserves_original():
    """测试反转不会修改原字符串"""
    original = "hello"
    result = reverse_string(original)
    assert original == "hello"  # 原字符串不变
    assert result == "olleh"
```

#### 题目3 答案

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def api_client():
    """Session 级别的 API 客户端"""
    print("\n=== 初始化 API 客户端 ===")

    class APIClient:
        def __init__(self):
            self.base_url = "https://api.example.com"
            self.headers = {"Content-Type": "application/json"}

        def get(self, endpoint):
            """模拟 GET 请求"""
            print(f"GET {self.base_url}{endpoint}")
            return {"status": 200, "data": {}}

        def post(self, endpoint, data):
            """模拟 POST 请求"""
            print(f"POST {self.base_url}{endpoint}")
            return {"status": 201, "data": data}

        def login(self, username, password):
            """模拟登录"""
            if username == "admin" and password == "123456":
                return {"token": "mock_token_12345"}
            return {"error": "认证失败"}

    client = APIClient()
    yield client

    print("\n=== 关闭 API 客户端 ===")

@pytest.fixture
def auth_token(api_client):
    """依赖 api_client 的认证 token"""
    print("\n>>> 获取认证 token")
    result = api_client.login("admin", "123456")
    token = result.get("token")
    yield token
    print("\n>>> 清除认证 token")

@pytest.fixture
def authenticated_client(api_client, auth_token):
    """组合 api_client 和 auth_token"""
    print("\n>>> 创建认证客户端")

    class AuthenticatedClient:
        def __init__(self, client, token):
            self.client = client
            self.token = token
            self.client.headers["Authorization"] = f"Bearer {token}"

        def get(self, endpoint):
            return self.client.get(endpoint)

        def post(self, endpoint, data):
            return self.client.post(endpoint, data)

    return AuthenticatedClient(api_client, auth_token)

# tests/test_api_client.py
def test_api_client_available(api_client):
    """测试 API 客户端可用"""
    assert api_client.base_url == "https://api.example.com"
    assert "Content-Type" in api_client.headers

def test_api_client_get(api_client):
    """测试 GET 请求"""
    result = api_client.get("/users")
    assert result["status"] == 200

# tests/test_auth.py
def test_auth_token(auth_token):
    """测试认证 token"""
    assert auth_token is not None
    assert auth_token == "mock_token_12345"

def test_authenticated_request(authenticated_client):
    """测试认证后的请求"""
    result = authenticated_client.get("/profile")
    assert result["status"] == 200
```

---

### 自测检查清单

完成以上练习后，检查自己是否掌握以下能力：

#### 基础能力（必须掌握）
- [ ] 能编写基本的测试函数和测试类
- [ ] 能使用各种断言（相等、比较、包含、类型等）
- [ ] 能使用 `pytest.raises` 测试异常
- [ ] 能编写和使用 fixture
- [ ] 能使用 `@pytest.mark.parametrize` 进行参数化
- [ ] 能使用 `@pytest.mark.skip` 和 `xfail`

#### 进阶能力（应该了解）
- [ ] 理解 fixture 的各种作用域
- [ ] 能使用 conftest.py 共享 fixture
- [ ] 能使用多个参数化装饰器
- [ ] 能配置 pytest.ini

#### 实战能力（综合应用）
- [ ] 能组织规范的测试项目结构
- [ ] 能编写数据驱动测试
- [ ] 能使用标记分类测试用例
- [ ] 能处理测试中的资源管理

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
