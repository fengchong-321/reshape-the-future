# 第5周：Pytest 进阶与 Allure 报告

## 本周目标

掌握 Pytest 高级特性，能生成专业的 Allure 测试报告。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| fixture 进阶 | yield、fixtures 依赖、factory | ⭐⭐⭐⭐ |
| conftest 进阶 | 多级 conftest、钩子函数 | ⭐⭐⭐⭐ |
| 插件开发 | 钩子函数、自定义插件 | ⭐⭐⭐ |
| Allure 报告 | 安装、集成、步骤、附件 | ⭐⭐⭐⭐⭐ |
| 测试配置 | 命令行参数、环境变量 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 fixture 进阶

```python
import pytest

# ============================================
# fixture 工厂模式
# ============================================
@pytest.fixture
def make_user():
    """工厂 fixture - 动态创建用户"""
    created_users = []

    def _make_user(name, role="user"):
        user = {"id": len(created_users) + 1, "name": name, "role": role}
        created_users.append(user)
        return user

    yield _make_user

    # 清理
    print(f"清理 {len(created_users)} 个用户")

def test_factory_fixture(make_user):
    user1 = make_user("张三", "admin")
    user2 = make_user("李四", "user")

    assert user1["name"] == "张三"
    assert user2["role"] == "user"

# ============================================
# fixture 参数化
# ============================================
@pytest.fixture(params=[
    ("admin", "admin123"),
    ("user", "user123"),
])
def credentials(request):
    """参数化 fixture"""
    return {"username": request.param[0], "password": request.param[1]}

def test_with_param_fixture(credentials):
    print(credentials)  # 会运行 2 次

# ============================================
# fixture 与 indirect 参数化
# ============================================
@pytest.fixture
def user_data(request):
    """通过 indirect 传递参数"""
    data = request.param
    # 可以在这里做数据预处理
    return {"username": data["username"].upper(), "age": data["age"]}

@pytest.mark.parametrize("user_data", [
    {"username": "admin", "age": 25},
    {"username": "user", "age": 30},
], indirect=True)
def test_indirect(user_data):
    assert user_data["username"].isupper()

# ============================================
# 使用 fixture 作为测试 ID
# ============================================
@pytest.fixture(params=[
    pytest.param({"browser": "chrome"}, id="chrome"),
    pytest.param({"browser": "firefox"}, id="firefox"),
    pytest.param({"browser": "safari"}, id="safari", marks=pytest.mark.skip),
])
def browser(request):
    return request.param["browser"]

def test_browser(browser):
    print(f"测试浏览器: {browser}")
```

---

### 2.2 conftest 进阶

```python
# ============================================
# 多级 conftest
# ============================================
# 项目结构
# project/
# ├── conftest.py          # 全局 fixture
# ├── tests/
# │   ├── conftest.py      # tests 级别 fixture
# │   ├── api/
# │   │   ├── conftest.py  # api 级别 fixture
# │   │   └── test_user.py
# │   └── ui/
# │       ├── conftest.py  # ui 级别 fixture
# │       └── test_home.py

# conftest.py 的查找顺序：
# 1. 测试文件所在目录
# 2. 父目录
# 3. 继续向上直到项目根目录

# tests/api/conftest.py
import pytest

@pytest.fixture
def api_base_url():
    """API 专用 fixture"""
    return "https://api.example.com"

# tests/ui/conftest.py
@pytest.fixture
def browser():
    """UI 专用 fixture"""
    from selenium import webdriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# ============================================
# 钩子函数
# ============================================
# conftest.py

def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="测试环境: dev, test, prod"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="浏览器: chrome, firefox, safari"
    )

@pytest.fixture(scope="session")
def env(request):
    """获取环境参数"""
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def browser_name(request):
    """获取浏览器参数"""
    return request.config.getoption("--browser")

# 使用
# pytest --env=prod --browser=firefox

def pytest_configure(config):
    """配置阶段执行"""
    # 注册自定义标记
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试"
    )

def pytest_collection_modifyitems(config, items):
    """修改收集到的测试项"""
    # 根据标记排序
    smoke_tests = []
    other_tests = []

    for item in items:
        if "smoke" in item.keywords:
            smoke_tests.append(item)
        else:
            other_tests.append(item)

    items[:] = smoke_tests + other_tests

def pytest_runtest_setup(item):
    """每个测试执行前"""
    print(f"\n开始执行: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """每个测试执行后"""
    print(f"执行完成: {item.name}")

def pytest_runtest_makereport(item, call):
    """生成测试报告钩子"""
    if call.when == "call":
        if call.excinfo is not None:
            # 测试失败时的处理
            print(f"测试失败: {item.name}")

# ============================================
# 失败截图钩子（UI 测试常用）
# ============================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 获取 fixture 中的 driver
        if "browser" in item.funcargs:
            driver = item.funcargs["browser"]
            # 截图
            driver.save_screenshot(f"screenshots/{item.name}.png")
```

---

### 2.3 Allure 报告

```bash
# 安装
pip install allure-pytest

# 安装 Allure 命令行工具（Mac）
brew install allure

# 或下载：https://github.com/allure-framework/allure2/releases
```

```python
import pytest
import allure

# ============================================
# 基本用法
# ============================================
@allure.feature("用户管理")
@allure.story("用户登录")
class TestLogin:

    @allure.title("登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self):
        """测试正常登录"""
        with allure.step("输入用户名"):
            username = "admin"
            allure.attach(username, name="用户名")

        with allure.step("输入密码"):
            password = "******"
            allure.attach(password, name="密码")

        with allure.step("点击登录按钮"):
            result = True

        with allure.step("验证登录成功"):
            assert result is True

    @allure.title("登录失败-密码错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self):
        pass

# ============================================
# Allure 装饰器
# ============================================
@allure.feature("订单模块")  # 功能模块
@allure.story("创建订单")     # 用户故事
@allure.tag("p0", "smoke")   # 标签
@allure.severity(allure.severity_level.BLOCKER)  # 严重程度
@allure.issue("BUG-123")     # 关联 Bug
@allure.testcase("TC-001")   # 关联测试用例
@allure.link("https://example.com", name="文档链接")
def test_create_order():
    pass

# severity 级别
# BLOCKER   - 阻塞
# CRITICAL  - 严重
# NORMAL    - 正常
# MINOR     - 轻微
# TRIVIAL   - 不重要

# ============================================
# 步骤和附件
# ============================================
@allure.step("执行登录")
def login(username, password):
    allure.attach(username, name="用户名", attachment_type=allure.attachment_type.TEXT)
    return {"token": "xxx"}

@allure.step("获取用户信息")
def get_user_info(token):
    return {"name": "张三", "age": 25}

def test_login_flow():
    token = login("admin", "123456")
    user = get_user_info(token)

    # 附加各种类型的内容
    allure.attach(
        '{"name": "张三"}',
        name="响应数据",
        attachment_type=allure.attachment_type.JSON
    )

    allure.attach(
        "<html><body>HTML 内容</body></html>",
        name="HTML 附件",
        attachment_type=allure.attachment_type.HTML
    )

    # 附加图片
    allure.attach.file(
        "screenshot.png",
        name="截图",
        attachment_type=allure.attachment_type.PNG
    )

# ============================================
# 动态设置
# ============================================
def test_dynamic_allure():
    # 动态设置标题
    allure.dynamic.title("动态标题")

    # 动态设置 feature/story
    allure.dynamic.feature("动态模块")
    allure.dynamic.story("动态故事")

    # 动态设置参数
    allure.dynamic.parameter("用户名", "admin")

# ============================================
# 参数化 + Allure
# ============================================
@allure.feature("参数化示例")
@pytest.mark.parametrize("username,password,expected", [
    allure.step("有效用户")(pytest.param("admin", "123456", True, id="admin用户")),
    allure.step("无效用户")(pytest.param("guest", "wrong", False, id="guest用户")),
])
def test_parameterized(username, password, expected):
    allure.dynamic.title(f"测试用户: {username}")
    assert (username == "admin") == expected
```

**生成报告：**

```bash
# 运行测试并生成 Allure 数据
pytest --alluredir=allure-results

# 生成并打开报告
allure serve allure-results

# 生成 HTML 报告
allure generate allure-results -o allure-report --clean

# 打开已生成的报告
allure open allure-report
```

---

### 2.4 完整的测试项目配置

```python
# conftest.py - 完整示例
import pytest
import allure
import requests
from pathlib import Path

# ============================================
# 命令行参数
# ============================================
def pytest_addoption(parser):
    parser.addoption("--env", default="test", help="环境")
    parser.addoption("--base-url", default=None, help="基础URL")

# ============================================
# 环境 fixture
# ============================================
@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def config(env):
    """加载配置"""
    import yaml
    config_file = Path(f"config/config.{env}.yaml")
    with open(config_file) as f:
        return yaml.safe_load(f)

# ============================================
# API 客户端 fixture
# ============================================
@pytest.fixture(scope="session")
def api_client(config, request):
    """API 客户端"""
    base_url = request.config.getoption("--base-url") or config["base_url"]

    session = requests.Session()
    session.base_url = base_url
    session.headers.update(config.get("headers", {}))

    class Client:
        def request(self, method, endpoint, **kwargs):
            url = f"{session.base_url}{endpoint}"
            response = session.request(method, url, **kwargs)

            # 记录到 Allure
            allure.attach(
                f"{method} {url}",
                name="请求",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                response.text,
                name="响应",
                attachment_type=allure.attachment_type.JSON
            )

            return response

        def get(self, endpoint, **kwargs):
            return self.request("GET", endpoint, **kwargs)

        def post(self, endpoint, **kwargs):
            return self.request("POST", endpoint, **kwargs)

    return Client()

# ============================================
# 失败截图
# ============================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 附加失败信息到 Allure
        allure.attach(
            str(report.longrepr),
            name="失败信息",
            attachment_type=allure.attachment_type.TEXT
        )
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 能编写 fixture 工厂模式
- [ ] 能配置多级 conftest.py
- [ ] 能使用 Allure 生成测试报告
- [ ] 能在报告中添加步骤和附件
- [ ] 能添加自定义命令行参数

### 应该了解

- [ ] Pytest 钩子函数
- [ ] 动态 Allure 属性

---

## 四、练习内容

### 基础练习（1-8）

---

**练习1：fixture 工厂模式基础**

**场景说明**：工厂模式 fixture 允许在测试中动态创建多个测试对象，并在测试结束后统一清理。这比普通 fixture 更灵活，适合需要创建多个相似对象的场景。

**具体需求**：
1. 创建 `make_user` 工厂 fixture，返回一个创建用户的函数
2. 支持动态创建多个用户（通过调用工厂函数）
3. 记录所有创建的用户 ID
4. 测试后自动清理创建的所有用户

**使用示例**：
```python
# tests/test_factory_fixture.py
import pytest

@pytest.fixture
def make_user():
    """工厂 fixture - 动态创建用户

    返回一个函数，每次调用创建一个新用户
    测试结束后自动清理所有创建的用户
    """
    created_users = []  # 记录创建的用户

    def _make_user(name, role="user", email=None):
        """创建用户的工厂函数

        Args:
            name: 用户名
            role: 角色（默认 user）
            email: 邮箱（可选）

        Returns:
            创建的用户字典
        """
        user_id = len(created_users) + 1
        user = {
            "id": user_id,
            "name": name,
            "role": role,
            "email": email or f"{name}@example.com"
        }
        created_users.append(user)
        print(f"创建用户: {user}")
        return user

    # 返回工厂函数
    yield _make_user

    # Teardown: 清理所有创建的用户
    print(f"\n清理 {len(created_users)} 个用户")
    created_users.clear()


def test_create_single_user(make_user):
    """测试创建单个用户"""
    user = make_user("张三", role="admin")

    assert user["id"] == 1
    assert user["name"] == "张三"
    assert user["role"] == "admin"
    assert "张三@example.com" in user["email"]


def test_create_multiple_users(make_user):
    """测试创建多个用户"""
    user1 = make_user("张三", role="admin")
    user2 = make_user("李四", role="user")
    user3 = make_user("王五", role="guest")

    # 验证每个用户的 ID 唯一
    assert user1["id"] == 1
    assert user2["id"] == 2
    assert user3["id"] == 3

    # 验证角色正确
    assert user1["role"] == "admin"
    assert user2["role"] == "user"
    assert user3["role"] == "guest"


def test_create_user_with_custom_email(make_user):
    """测试使用自定义邮箱创建用户"""
    user = make_user("测试用户", email="custom@test.com")

    assert user["email"] == "custom@test.com"
    assert user["name"] == "测试用户"
```

**验收标准**：
- [ ] fixture 返回的是函数（工厂模式）
- [ ] 能创建多个用户且 ID 递增
- [ ] 支持默认参数和自定义参数
- [ ] 测试结束后自动清理

---

**练习2：参数化 fixture**

**场景说明**：参数化 fixture 自动为每组参数生成独立的测试运行，适合需要在多种配置/环境下验证同一逻辑的场景。

**具体需求**：
1. 创建参数化的 `browser` fixture
2. 支持三种浏览器类型（chrome、firefox、safari）
3. 为每个参数设置清晰的测试 ID
4. safari 浏览器暂时跳过测试

**使用示例**：
```python
# tests/test_param_fixture.py
import pytest

@pytest.fixture(params=[
    pytest.param("chrome", id="Chrome浏览器"),
    pytest.param("firefox", id="Firefox浏览器"),
    pytest.param("safari", id="Safari浏览器", marks=pytest.mark.skip(reason="Safari 暂不支持")),
])
def browser(request):
    """参数化 fixture：多种浏览器类型

    每个参数会生成一个独立的测试运行
    request.param 包含当前参数值
    """
    browser_type = request.param
    print(f"\n初始化 {browser_type} 浏览器...")
    return browser_type


def test_browser_initialization(browser):
    """测试浏览器初始化"""
    print(f"当前浏览器: {browser}")
    assert browser in ["chrome", "firefox", "safari"]


def test_browser_navigation(browser):
    """测试浏览器导航功能"""
    print(f"在 {browser} 中执行导航测试")
    # 模拟导航操作
    assert browser is not None


# 带有更多参数的 fixture
@pytest.fixture(params=[
    pytest.param({"browser": "chrome", "version": "120.0"}, id="Chrome_120"),
    pytest.param({"browser": "firefox", "version": "121.0"}, id="Firefox_121"),
])
def browser_config(request):
    """参数化 fixture：浏览器配置对象"""
    return request.param


def test_with_browser_config(browser_config):
    """测试使用浏览器配置"""
    assert "browser" in browser_config
    assert "version" in browser_config
    print(f"测试浏览器: {browser_config['browser']} v{browser_config['version']}")
```

**运行命令**：
```bash
# 运行参数化 fixture 测试
pytest tests/test_param_fixture.py -v

# 输出示例：
# test_browser_initialization[Chrome浏览器] PASSED
# test_browser_initialization[Firefox浏览器] PASSED
# test_browser_initialization[Safari浏览器] SKIPPED
```

**验收标准**：
- [ ] fixture 正确使用 params 参数
- [ ] 每个参数都有清晰的测试 ID
- [ ] 跳过标记正确使用
- [ ] 测试针对每个参数独立运行

---

**练习3：indirect 参数化**

**场景说明**：`indirect=True` 允许将参数化数据先传递给 fixture 进行预处理，然后再传给测试函数。适合需要对测试数据进行转换、验证或增强的场景。

**具体需求**：
1. 创建 `user_data` fixture，通过 `request.param` 接收外部参数
2. 在 fixture 中进行数据预处理（如：用户名转大写、添加处理标记）
3. 使用 `indirect=True` 将参数传递给 fixture
4. 测试预处理后的数据

**使用示例**：
```python
# tests/test_indirect_param.py
import pytest

@pytest.fixture
def user_data(request):
    """通过 indirect 传递参数并预处理的 fixture

    request.param 接收外部传入的参数化数据
    在这里进行数据预处理（标准化、验证、增强等）
    """
    # 获取原始数据
    data = request.param

    # 数据预处理
    processed_data = {
        "username": data["username"].upper(),  # 用户名转大写
        "age": data["age"],
        "processed": True,  # 添加处理标记
        "is_adult": data["age"] >= 18,  # 计算是否成年
        "email": data.get("email", f"{data['username'].lower()}@test.com")  # 默认邮箱
    }

    return processed_data


@pytest.mark.parametrize("user_data", [
    {"username": "admin", "age": 25, "email": "admin@company.com"},
    {"username": "guest", "age": 16},  # 未成年，无邮箱
    {"username": "TestUser", "age": 30},
], indirect=True)
def test_indirect_user(user_data):
    """测试 indirect 参数化的用户数据"""
    # 验证预处理结果
    assert user_data["username"].isupper(), "用户名应被转为大写"
    assert user_data["processed"] is True, "应有处理标记"

    # 验证年龄计算
    if user_data["age"] >= 18:
        assert user_data["is_adult"] is True
    else:
        assert user_data["is_adult"] is False


@pytest.mark.parametrize("user_data,expected_adult", [
    pytest.param({"username": "adult1", "age": 25}, True, id="25岁成年"),
    pytest.param({"username": "adult2", "age": 18}, True, id="18岁成年"),
    pytest.param({"username": "child", "age": 16}, False, id="16岁未成年"),
], indirect=["user_data"])
def test_adult_check(user_data, expected_adult):
    """测试成年判断逻辑"""
    assert user_data["is_adult"] == expected_adult
```

**验收标准**：
- [ ] 理解 `indirect=True` 的作用
- [ ] fixture 正确使用 `request.param`
- [ ] 数据预处理逻辑正确
- [ ] 测试验证了预处理结果

---

**练习4：多级 conftest 配置**

**场景说明**：conftest.py 支持多级配置，子目录的 conftest.py 可以使用父目录的 fixture，实现分层配置管理。

**具体需求**：
1. 创建项目根目录的全局 conftest.py（session 级别配置）
2. 创建 tests/api 目录的 API 专用 conftest.py
3. 创建 tests/ui 目录的 UI 专用 conftest.py
4. 验证 fixture 的层级继承关系

**使用示例**：

```python
# project/conftest.py（根目录）
import pytest

@pytest.fixture(scope="session")
def global_config():
    """全局配置：整个测试会话共享"""
    print("\n=== 加载全局配置 ===")
    return {
        "app_name": "MyApp",
        "version": "1.0.0",
        "debug": True
    }

@pytest.fixture(scope="session")
def test_environment():
    """全局测试环境"""
    return "test"


# tests/conftest.py（tests 目录）
import pytest

@pytest.fixture(scope="module")
def test_data():
    """tests 级别的测试数据"""
    return {"default_user": "test_user"}


# tests/api/conftest.py
import pytest

@pytest.fixture
def api_base_url(global_config):
    """API 专用 fixture，依赖全局配置"""
    print("\n  >>> 初始化 API 客户端")
    return f"https://api.{global_config['app_name'].lower()}.com"

@pytest.fixture
def api_client(api_base_url):
    """API 客户端 fixture"""
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url

        def get(self, endpoint):
            return {"url": f"{self.base_url}{endpoint}"}

    return APIClient(api_base_url)


# tests/ui/conftest.py
import pytest

@pytest.fixture
def browser_config(global_config):
    """UI 专用 fixture，依赖全局配置"""
    return {
        "type": "chrome",
        "headless": not global_config["debug"],
        "window_size": (1920, 1080)
    }

@pytest.fixture
def browser(browser_config):
    """浏览器 fixture"""
    print(f"\n  >>> 启动浏览器: {browser_config['type']}")
    return {"driver": browser_config["type"], "started": True}
```

```python
# tests/api/test_user_api.py
import pytest

def test_api_with_global_config(api_client, global_config):
    """测试 API 使用全局配置"""
    assert global_config["app_name"] == "MyApp"
    assert "api.myapp.com" in api_client.base_url


# tests/ui/test_home_ui.py
import pytest

def test_ui_with_browser(browser, global_config):
    """测试 UI 使用浏览器和全局配置"""
    assert browser["started"] is True
    assert global_config["debug"] is True
```

**项目结构**：
```
project/
├── conftest.py          # 全局 fixture
├── tests/
│   ├── conftest.py      # tests 级别 fixture
│   ├── api/
│   │   ├── conftest.py  # api 级别 fixture
│   │   └── test_user.py
│   └── ui/
│       ├── conftest.py  # ui 级别 fixture
│       └── test_home.py
```

**验收标准**：
- [ ] 根目录 conftest.py 提供全局 fixture
- [ ] 子目录 conftest.py 提供专用 fixture
- [ ] 子目录 fixture 能使用父目录 fixture
- [ ] fixture 作用域正确

---

**练习5：命令行参数基础**

**场景说明**：通过 `pytest_addoption` 钩子添加自定义命令行参数，使测试可以根据参数动态调整行为（如环境、浏览器等）。

**具体需求**：
1. 添加 `--env` 命令行参数（支持 dev/test/prod）
2. 添加 `--browser` 命令行参数（支持 chrome/firefox）
3. 创建对应的 fixture 获取参数值
4. 在测试中使用这些参数

**使用示例**：
```python
# conftest.py
import pytest

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
        choices=["chrome", "firefox"],
        help="浏览器类型: chrome, firefox (默认: chrome)"
    )

    # 超时参数
    parser.addoption(
        "--timeout",
        action="store",
        default=30,
        type=int,
        help="请求超时时间（秒）"
    )


@pytest.fixture(scope="session")
def env(request):
    """获取环境参数"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def browser_name(request):
    """获取浏览器参数"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def timeout(request):
    """获取超时参数"""
    return request.config.getoption("--timeout")


@pytest.fixture(scope="session")
def config(env, timeout):
    """根据环境参数返回配置"""
    configs = {
        "dev": {"url": "http://localhost:8000", "debug": True},
        "test": {"url": "https://test.example.com", "debug": False},
        "prod": {"url": "https://example.com", "debug": False}
    }
    config = configs[env].copy()
    config["timeout"] = timeout
    return config
```

```python
# tests/test_with_cli_args.py
import pytest

def test_env_parameter(env):
    """测试环境参数"""
    assert env in ["dev", "test", "prod"]
    print(f"当前环境: {env}")

def test_browser_parameter(browser_name):
    """测试浏览器参数"""
    assert browser_name in ["chrome", "firefox"]
    print(f"当前浏览器: {browser_name}")

def test_config_based_on_env(config, env):
    """测试配置根据环境变化"""
    if env == "dev":
        assert config["debug"] is True
        assert "localhost" in config["url"]
    elif env == "prod":
        assert config["debug"] is False
        assert "example.com" in config["url"]
```

**运行命令**：
```bash
# 使用默认参数
pytest tests/test_with_cli_args.py -v

# 指定环境
pytest tests/test_with_cli_args.py --env=prod -v

# 指定浏览器和超时
pytest tests/test_with_cli_args.py --browser=firefox --timeout=60 -v
```

**验收标准**：
- [ ] `pytest_addoption` 正确注册参数
- [ ] fixture 能正确获取参数值
- [ ] 参数有默认值
- [ ] 能通过命令行覆盖参数

---

**练习6：钩子函数入门**

**场景说明**：Pytest 钩子函数允许在测试生命周期的特定时机执行自定义代码，如注册标记、测试前后操作、报告生成等。

**具体需求**：
1. 实现 `pytest_configure` 注册自定义标记
2. 实现 `pytest_runtest_setup` 在每个测试前执行操作
3. 实现 `pytest_runtest_teardown` 在每个测试后执行操作
4. 实现测试计时功能

**使用示例**：
```python
# conftest.py
import pytest
import time

# ============================================
# 配置阶段钩子
# ============================================
def pytest_configure(config):
    """配置阶段：注册自定义标记和初始化"""
    # 注册自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试，核心功能验证")
    config.addinivalue_line("markers", "p0: 最高优先级，阻塞性问题")
    config.addinivalue_line("markers", "p1: 高优先级，主要功能")
    config.addinivalue_line("markers", "slow: 慢速测试，执行时间超过 1s")

    print("\n=== Pytest 配置完成 ===")


# ============================================
# 测试执行阶段钩子
# ============================================
# 存储测试开始时间
test_start_times = {}

def pytest_runtest_setup(item):
    """每个测试执行前"""
    # 记录开始时间
    test_start_times[item.name] = time.time()

    # 打印测试信息
    print(f"\n>>> 开始执行: {item.name}")

    # 检查标记
    markers = [m.name for m in item.iter_markers()]
    if markers:
        print(f"    标记: {', '.join(markers)}")


def pytest_runtest_teardown(item, nextitem):
    """每个测试执行后"""
    # 计算执行时间
    if item.name in test_start_times:
        duration = time.time() - test_start_times[item.name]
        print(f">>> 执行完成: {item.name} (耗时: {duration:.3f}s)")
        del test_start_times[item.name]

    if nextitem:
        print(f"    下一个测试: {nextitem.name}")


def pytest_runtest_call(item):
    """测试执行时"""
    pass  # 可以在这里添加监控逻辑


# ============================================
# 报告生成钩子
# ============================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """生成测试报告的钩子"""
    outcome = yield
    report = outcome.get_result()

    # 只在测试调用阶段处理
    if call.when == "call":
        if report.passed:
            print(f"    ✓ 测试通过")
        elif report.failed:
            print(f"    ✗ 测试失败")
            # 可以在这里添加失败处理逻辑
        elif report.skipped:
            print(f"    ○ 测试跳过")


# ============================================
# 会话级别钩子
# ============================================
def pytest_sessionstart(session):
    """测试会话开始"""
    print("\n" + "=" * 50)
    print("测试会话开始")
    print("=" * 50)


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束"""
    print("\n" + "=" * 50)
    print(f"测试会话结束 (退出状态: {exitstatus})")
    print("=" * 50)
```

```python
# tests/test_with_hooks.py
import pytest

@pytest.mark.smoke
@pytest.mark.p0
def test_smoke_with_hooks():
    """带标记的冒烟测试"""
    assert True

@pytest.mark.slow
def test_slow_with_hooks():
    """慢速测试"""
    import time
    time.sleep(0.1)
    assert True

def test_normal_with_hooks():
    """普通测试"""
    assert 1 + 1 == 2
```

**验收标准**：
- [ ] `pytest_configure` 正确注册标记
- [ ] `pytest_runtest_setup` 在测试前执行
- [ ] `pytest_runtest_teardown` 在测试后执行
- [ ] 能看到测试执行时间

---

**练习7：Allure 基础装饰器**

**场景说明**：Allure 报告是专业的测试报告工具，通过装饰器可以标注测试的功能模块、严重程度、关联信息等，使报告更加清晰。

**具体需求**：
1. 使用 `@allure.feature` 标注功能模块
2. 使用 `@allure.story` 标注用户故事
3. 使用 `@allure.title` 设置测试标题
4. 使用 `@allure.severity` 设置严重程度
5. 理解各种严重程度的含义

**使用示例**：
```python
# tests/test_allure_basic.py
import allure
import pytest

# 严重程度说明：
# BLOCKER  - 阻塞级别，系统无法使用
# CRITICAL - 严重级别，核心功能受损
# NORMAL   - 正常级别，一般功能问题
# MINOR    - 轻微级别，次要功能问题
# TRIVIAL  - 不重要，UI/文案问题


@allure.feature("用户管理")
@allure.story("用户登录")
class TestLogin:
    """用户登录测试类"""

    @allure.title("登录成功 - 正确的用户名和密码")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self):
        """测试正常登录功能"""
        # BLOCKER: 登录是系统入口，必须可用
        assert True

    @allure.title("登录失败 - 密码错误")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self):
        """测试密码错误时的提示"""
        # CRITICAL: 安全相关，重要但可绕过
        assert True

    @allure.title("登录失败 - 用户名为空")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_username(self):
        """测试用户名为空时的验证"""
        assert True


@allure.feature("用户管理")
@allure.story("用户注册")
class TestRegister:
    """用户注册测试类"""

    @allure.title("注册成功 - 完整信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_success(self):
        """测试正常注册"""
        assert True

    @allure.title("注册失败 - 用户名已存在")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_duplicate_username(self):
        """测试重复用户名"""
        assert True


@allure.feature("订单管理")
@allure.story("创建订单")
@allure.title("创建订单成功")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_order():
    """测试创建订单"""
    assert True


# 使用标签和链接
@allure.feature("支付模块")
@allure.story("支付宝支付")
@allure.title("支付宝支付成功")
@allure.tag("支付", "第三方")
@allure.severity(allure.severity_level.BLOCKER)
@allure.issue("BUG-001", name="支付超时问题")
@allure.testcase("TC-PAY-001", name="支付宝支付测试用例")
@allure.link("https://docs.example.com/pay", name="支付API文档")
def test_alipay():
    """测试支付宝支付"""
    assert True
```

**运行命令**：
```bash
# 运行测试并生成 Allure 数据
pytest tests/test_allure_basic.py --alluredir=allure-results

# 生成并打开报告
allure serve allure-results
```

**验收标准**：
- [ ] 正确使用 `@allure.feature`
- [ ] 正确使用 `@allure.story`
- [ ] 正确使用 `@allure.title`
- [ ] 理解各种 severity 级别
- [ ] 能生成 Allure 报告

---

**练习8：Allure 步骤和附件**

**场景说明**：Allure 的步骤（step）和附件（attach）功能可以让测试报告展示详细的执行过程和中间数据，便于问题定位。

**具体需求**：
1. 使用 `with allure.step()` 添加测试步骤
2. 使用 `allure.attach()` 添加文本附件
3. 使用 `allure.attach.file()` 添加文件附件
4. 使用 `@allure.step` 装饰器标记函数

**使用示例**：
```python
# tests/test_allure_steps.py
import allure
import pytest
import json
import tempfile
import os

# ============================================
# 步骤装饰器
# ============================================
@allure.step("执行登录操作")
def login(username, password):
    """登录函数，会被标记为一个步骤"""
    # 附件：记录用户名（密码要脱敏）
    allure.attach(username, name="用户名", attachment_type=allure.attachment_type.TEXT)
    allure.attach("******", name="密码", attachment_type=allure.attachment_type.TEXT)

    # 模拟登录
    if username == "admin" and password == "123456":
        return {"success": True, "token": "admin_token_xxx"}
    return {"success": False, "error": "认证失败"}


@allure.step("获取用户信息")
def get_user_info(token):
    """获取用户信息"""
    if token:
        return {"name": "张三", "age": 25, "role": "admin"}
    return None


@allure.step("验证用户权限")
def check_permission(user, action):
    """验证用户权限"""
    permissions = {
        "admin": ["read", "write", "delete"],
        "user": ["read", "write"]
    }
    role = user.get("role", "guest")
    return action in permissions.get(role, [])


# ============================================
# 测试用例
# ============================================
@allure.feature("用户模块")
@allure.story("登录流程")
@allure.title("完整登录流程测试")
def test_login_flow():
    """测试完整的登录流程"""

    # 步骤1：登录
    with allure.step("步骤1：执行登录"):
        result = login("admin", "123456")
        allure.attach(
            json.dumps(result, ensure_ascii=False),
            name="登录结果",
            attachment_type=allure.attachment_type.JSON
        )
        assert result["success"] is True

    # 步骤2：获取用户信息
    with allure.step("步骤2：获取用户信息"):
        user = get_user_info(result["token"])
        allure.attach(
            json.dumps(user, ensure_ascii=False, indent=2),
            name="用户信息",
            attachment_type=allure.attachment_type.JSON
        )
        assert user is not None
        assert user["name"] == "张三"

    # 步骤3：验证权限
    with allure.step("步骤3：验证用户权限"):
        can_delete = check_permission(user, "delete")
        allure.attach(f"删除权限: {can_delete}", name="权限检查结果")
        assert can_delete is True


@allure.feature("附件示例")
@allure.title("测试各种附件类型")
def test_attachment_types():
    """测试各种类型的附件"""

    # 文本附件
    with allure.step("添加文本附件"):
        allure.attach("这是普通文本内容", name="文本附件")

    # JSON 附件
    with allure.step("添加 JSON 附件"):
        data = {"name": "测试", "items": [1, 2, 3]}
        allure.attach(
            json.dumps(data, ensure_ascii=False, indent=2),
            name="JSON数据",
            attachment_type=allure.attachment_type.JSON
        )

    # HTML 附件
    with allure.step("添加 HTML 附件"):
        html = """
        <html>
            <body>
                <h1>测试报告</h1>
                <p style="color: green;">测试通过</p>
            </body>
        </html>
        """
        allure.attach(html, name="HTML内容", attachment_type=allure.attachment_type.HTML)

    # CSV 附件
    with allure.step("添加 CSV 附件"):
        csv_content = "name,age,city\n张三,25,北京\n李四,30,上海"
        allure.attach(csv_content, name="CSV数据", attachment_type=allure.attachment_type.CSV)

    assert True


@allure.feature("附件示例")
@allure.title("测试文件附件")
def test_file_attachment():
    """测试文件附件"""

    with allure.step("创建并附加临时文件"):
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("这是临时文件的内容\n用于测试 Allure 文件附件功能")
            temp_file = f.name

        try:
            # 附加文件
            allure.attach.file(
                temp_file,
                name="临时文件附件",
                attachment_type=allure.attachment_type.TXT
            )

            assert os.path.exists(temp_file)
        finally:
            # 清理临时文件
            os.unlink(temp_file)
```

**验收标准**：
- [ ] 正确使用 `with allure.step()`
- [ ] 正确使用 `@allure.step` 装饰器
- [ ] 正确使用 `allure.attach()` 添加各种类型附件
- [ ] 正确使用 `allure.attach.file()` 添加文件
- [ ] 报告中能看到步骤和附件

### 进阶练习（9-16）

---

**练习9：fixture 依赖链**

**场景说明**：fixture 可以依赖其他 fixture，形成依赖链。Pytest 会自动按依赖顺序初始化 fixture，这对于需要多层资源初始化的场景非常有用。

**具体需求**：
1. 创建 `config` fixture（session 级别）：提供全局配置
2. 创建 `db_connection` fixture 依赖 `config`：根据配置连接数据库
3. 创建 `test_data` fixture 依赖 `db_connection`：准备测试数据
4. 验证 fixture 依赖关系和执行顺序

**使用示例**：
```python
# tests/test_fixture_chain.py
import pytest

# ============================================
# Session 级别：全局配置
# ============================================
@pytest.fixture(scope="session")
def config():
    """Session 级别的配置 fixture

    整个测试会话只执行一次
    """
    print("\n=== [Session] 加载配置 ===")
    return {
        "db_host": "localhost",
        "db_port": 3306,
        "db_name": "test_db"
    }


# ============================================
# Module 级别：数据库连接
# ============================================
@pytest.fixture(scope="module")
def db_connection(config):
    """Module 级别的数据库连接 fixture

    依赖 config fixture，每个模块执行一次
    """
    print(f"\n=== [Module] 连接数据库: {config['db_host']}:{config['db_port']} ===")
    conn = {
        "connected": True,
        "host": config["db_host"],
        "port": config["db_port"]
    }
    yield conn
    print(f"\n=== [Module] 关闭数据库连接 ===")
    conn["connected"] = False


# ============================================
# Function 级别：测试数据
# ============================================
@pytest.fixture
def test_data(db_connection):
    """Function 级别的测试数据 fixture

    依赖 db_connection fixture，每个测试函数执行一次
    """
    print(f"\n  >>> [Function] 准备测试数据（数据库已连接: {db_connection['connected']}）")
    return [
        {"id": 1, "name": "user1", "email": "user1@test.com"},
        {"id": 2, "name": "user2", "email": "user2@test.com"}
    ]


# ============================================
# 测试用例
# ============================================
def test_with_dependencies(test_data, db_connection, config):
    """测试使用依赖链上的所有 fixture"""
    # 验证配置
    assert config["db_host"] == "localhost"
    assert config["db_port"] == 3306

    # 验证数据库连接
    assert db_connection["connected"] is True

    # 验证测试数据
    assert len(test_data) == 2
    assert test_data[0]["name"] == "user1"


def test_with_test_data(test_data):
    """测试只使用 test_data fixture

    注意：虽然只请求 test_data，但其依赖的 db_connection 和 config
    也会自动被初始化
    """
    assert len(test_data) == 2
    for user in test_data:
        assert "id" in user
        assert "email" in user
```

**运行命令**：
```bash
# 运行并查看 fixture 执行顺序
pytest tests/test_fixture_chain.py -s -v

# 查看 fixture 依赖关系
pytest tests/test_fixture_chain.py --setup-show
```

**验收标准**：
- [ ] fixture 依赖关系正确
- [ ] fixture 按依赖顺序初始化
- [ ] 不同作用域的 fixture 执行次数正确
- [ ] 所有断言通过

---

**练习10：测试排序钩子**

**场景说明**：`pytest_collection_modifyitems` 钩子可以修改测试收集结果，实现测试排序、过滤等功能。常用于将冒烟测试优先执行。

**具体需求**：
1. 实现 `pytest_collection_modifyitems` 钩子
2. 将标记为 `smoke` 的测试排在前面
3. 其他测试排在后面
4. 保持同组测试的原始顺序

**使用示例**：
```python
# conftest.py
import pytest

def pytest_collection_modifyitems(config, items):
    """修改测试收集结果的钩子

    Args:
        config: pytest 配置对象
        items: 收集到的测试项列表（可修改）
    """
    # 分组：冒烟测试 vs 其他测试
    smoke_tests = []
    other_tests = []

    for item in items:
        if "smoke" in item.keywords:
            smoke_tests.append(item)
        else:
            other_tests.append(item)

    # 冒烟测试排前面，其他测试排后面
    items[:] = smoke_tests + other_tests

    # 打印排序信息
    print(f"\n测试排序完成: {len(smoke_tests)} 个冒烟测试, {len(other_tests)} 个其他测试")


# 注册 smoke 标记
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: 冒烟测试，优先执行")
```

```python
# tests/test_order.py
import pytest

# 注意：这些测试的执行顺序会被钩子修改

@pytest.mark.smoke
def test_smoke_1():
    """冒烟测试 1 - 应该先执行"""
    print("执行 smoke_1")
    assert True

def test_other_1():
    """其他测试 1 - 应该后执行"""
    print("执行 other_1")
    assert True

@pytest.mark.smoke
def test_smoke_2():
    """冒烟测试 2 - 应该先执行"""
    print("执行 smoke_2")
    assert True

def test_other_2():
    """其他测试 2 - 应该后执行"""
    print("执行 other_2")
    assert True

@pytest.mark.smoke
def test_smoke_3():
    """冒烟测试 3 - 应该先执行"""
    print("执行 smoke_3")
    assert True
```

**运行命令**：
```bash
# 运行并观察执行顺序
pytest tests/test_order.py -v -s

# 预期输出顺序：
# test_smoke_1 -> test_smoke_2 -> test_smoke_3 -> test_other_1 -> test_other_2
```

**验收标准**：
- [ ] 钩子正确实现
- [ ] 冒烟测试优先执行
- [ ] 同组内保持原始顺序
- [ ] 所有测试通过

---

**练习11：失败截图钩子**

**场景说明**：在 UI 自动化测试中，测试失败时自动截图是常见需求。通过 `pytest_runtest_makereport` 钩子可以捕获失败并执行截图操作。

**具体需求**：
1. 实现 `pytest_runtest_makereport` 钩子
2. 测试失败时自动获取浏览器截图
3. 将截图附加到 Allure 报告
4. 附加失败详情到报告

**使用示例**：
```python
# conftest.py
import pytest
import allure

# ============================================
# 失败截图钩子
# ============================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """生成测试报告的钩子

    当测试失败时自动截图并附加到 Allure 报告
    """
    # 执行测试并获取结果
    outcome = yield
    report = outcome.get_result()

    # 只在测试调用阶段且失败时处理
    if report.when == "call" and report.failed:
        # 获取测试名称
        test_name = item.name

        # 1. 尝试获取浏览器 fixture 并截图
        if "browser" in item.funcargs:
            driver = item.funcargs["browser"]

            # 检查 driver 是否有截图方法
            if hasattr(driver, "get_screenshot_as_png"):
                try:
                    screenshot = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name=f"{test_name}_失败截图",
                        attachment_type=allure.attachment_type.PNG
                    )
                    print(f"\n已保存失败截图: {test_name}")
                except Exception as e:
                    print(f"\n截图失败: {e}")

        # 2. 附加失败详情到报告
        allure.attach(
            str(report.longrepr),
            name="失败详情",
            attachment_type=allure.attachment_type.TEXT
        )

        # 3. 附加测试元数据
        allure.attach(
            f"测试名称: {test_name}\n"
            f"测试文件: {item.location[0]}\n"
            f"失败时间: {call.start}",
            name="测试信息",
            attachment_type=allure.attachment_type.TEXT
        )


# ============================================
# 模拟浏览器 fixture
# ============================================
@pytest.fixture
def browser():
    """模拟浏览器 fixture"""
    class MockBrowser:
        def __init__(self):
            self.url = "https://example.com"

        def get_screenshot_as_png(self):
            """模拟截图方法"""
            # 实际项目中会返回真实的截图
            return b"mock_screenshot_data"

        def quit(self):
            pass

    driver = MockBrowser()
    yield driver
    driver.quit()
```

```python
# tests/test_screenshot.py
import pytest
import allure

@allure.feature("UI测试")
@allure.story("页面测试")
class TestWithScreenshot:

    def test_success_with_browser(self, browser):
        """这个测试会通过，不会触发截图"""
        assert browser.url == "https://example.com"

    @allure.title("这个测试会失败并截图")
    def test_fail_with_screenshot(self, browser):
        """这个测试会失败，触发截图"""
        assert False, "故意失败以测试截图功能"

    def test_fail_no_browser(self):
        """没有浏览器的失败测试"""
        assert False, "没有浏览器，无法截图"
```

**验收标准**：
- [ ] 钩子正确实现
- [ ] 失败时自动截图
- [ ] 截图附加到 Allure 报告
- [ ] 失败详情正确记录

---

**练习12：动态 Allure 属性**

**场景说明**：除了使用装饰器静态设置 Allure 属性外，还可以在测试执行过程中动态设置标题、描述、参数等属性，特别适合参数化测试。

**具体需求**：
1. 使用 `allure.dynamic.title()` 动态设置测试标题
2. 使用 `allure.dynamic.feature()` 和 `story()` 动态设置模块
3. 在参数化测试中使用动态属性
4. 动态添加描述信息

**使用示例**：
```python
# tests/test_allure_dynamic.py
import allure
import pytest

# ============================================
# 动态标题示例
# ============================================
@pytest.mark.parametrize("username,role,expected_level", [
    ("admin", "管理员", 1),
    ("user", "普通用户", 2),
    ("guest", "访客", 3),
])
def test_user_permissions_dynamic(username, role, expected_level):
    """测试用户权限（动态标题）"""

    # 动态设置标题
    allure.dynamic.title(f"测试用户权限: {username} ({role})")

    # 动态设置描述
    allure.dynamic.description(f"""
    ## 测试描述
    验证用户 **{username}** 的权限级别是否正确。

    - 角色: {role}
    - 预期级别: {expected_level}
    """)

    # 动态设置参数（显示在报告中）
    allure.dynamic.parameter("用户名", username)
    allure.dynamic.parameter("角色", role)
    allure.dynamic.parameter("预期级别", expected_level)

    # 动态设置严重程度
    if expected_level == 1:
        allure.dynamic.severity(allure.severity_level.BLOCKER)
    else:
        allure.dynamic.severity(allure.severity_level.NORMAL)

    # 模拟权限检查
    user_level = {"admin": 1, "user": 2, "guest": 3}.get(username, 99)
    assert user_level == expected_level


# ============================================
# 动态 feature/story 示例
# ============================================
test_cases = [
    {"module": "用户管理", "feature": "登录", "case": "正常登录", "result": "pass"},
    {"module": "用户管理", "feature": "登录", "case": "密码错误", "result": "fail"},
    {"module": "订单管理", "feature": "创建订单", "case": "创建成功", "result": "pass"},
]

@pytest.mark.parametrize("case", test_cases, ids=lambda x: x["case"])
def test_dynamic_feature_story(case):
    """测试动态设置 feature 和 story"""

    # 动态设置模块和功能
    allure.dynamic.feature(case["module"])
    allure.dynamic.story(case["feature"])
    allure.dynamic.title(case["case"])

    # 根据结果设置严重程度
    if case["result"] == "fail":
        allure.dynamic.severity(allure.severity_level.CRITICAL)
    else:
        allure.dynamic.severity(allure.severity_level.NORMAL)

    # 添加附件记录测试数据
    allure.attach(
        str(case),
        name="测试数据",
        attachment_type=allure.attachment_type.TEXT
    )

    assert case["result"] == "pass"


# ============================================
# 动态标签示例
# ============================================
def test_add_tags_dynamically():
    """测试动态添加标签"""

    # 动态设置标题
    allure.dynamic.title("动态添加标签的测试")

    # 动态添加标签
    allure.dynamic.tag("动态标签1")
    allure.dynamic.tag("动态标签2")

    # 动态添加链接
    allure.dynamic.link("https://example.com/docs", name="相关文档")

    assert True
```

**验收标准**：
- [ ] 正确使用 `allure.dynamic.title()`
- [ ] 正确使用 `allure.dynamic.feature()` 和 `story()`
- [ ] 参数化测试中动态属性生效
- [ ] 报告中能看到动态设置的属性

---

**练习13：Allure 关联管理**

**场景说明**：Allure 支持将测试与 Bug、测试用例、文档等资源关联，方便在报告中直接跳转查看相关信息。

**具体需求**：
1. 使用 `@allure.issue` 关联 Bug
2. 使用 `@allure.testcase` 关联测试用例
3. 使用 `@allure.link` 添加文档链接
4. 使用 `@allure.tag` 添加标签分类

**使用示例**：
```python
# tests/test_allure_links.py
import allure
import pytest

# ============================================
# 关联 Bug 示例
# ============================================
@allure.feature("订单模块")
@allure.story("创建订单")
@allure.title("创建订单 - 正常流程")
@allure.issue("BUG-123", name="订单金额计算错误")
@allure.issue("BUG-456", name="订单状态同步延迟")
@allure.testcase("TC-ORDER-001", name="创建订单测试用例")
@allure.link("https://docs.example.com/api/orders", name="订单API文档")
@allure.link("https://jira.example.com/browse/BUG-123", name="JIRA Bug")
def test_create_order_with_links():
    """测试创建订单，关联相关资源

    点击报告中的链接可以跳转到：
    - Bug 详情
    - 测试用例文档
    - API 文档
    """
    with allure.step("准备订单数据"):
        order_data = {"product_id": 1, "quantity": 2}
        allure.attach(str(order_data), name="订单数据")

    with allure.step("创建订单"):
        # 模拟创建订单
        result = {"order_id": 1001, "status": "created"}
        allure.attach(str(result), name="创建结果")

    assert result["status"] == "created"


# ============================================
# 标签分类示例
# ============================================
@allure.feature("支付模块")
@allure.story("支付宝支付")
@allure.title("支付宝支付成功")
@allure.tag("支付", "第三方", "支付宝")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase("TC-PAY-001")
def test_alipay_success():
    """测试支付宝支付成功流程"""
    assert True


@allure.feature("支付模块")
@allure.story("微信支付")
@allure.title("微信支付成功")
@allure.tag("支付", "第三方", "微信")
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase("TC-PAY-002")
def test_wechat_pay_success():
    """测试微信支付成功流程"""
    assert True


# ============================================
# 动态关联示例
# ============================================
@pytest.mark.parametrize("bug_id,bug_name", [
    ("BUG-001", "登录超时"),
    ("BUG-002", "密码明文存储"),
])
def test_with_dynamic_issue_link(bug_id, bug_name):
    """测试动态添加 Bug 关联"""

    # 动态设置标题
    allure.dynamic.title(f"关联 {bug_name} 的测试")

    # 动态添加 Bug 链接
    allure.dynamic.link(
        f"https://jira.example.com/browse/{bug_id}",
        name=f"Bug: {bug_name}"
    )

    assert True
```

**验收标准**：
- [ ] 正确使用 `@allure.issue` 关联 Bug
- [ ] 正确使用 `@allure.testcase` 关联测试用例
- [ ] 正确使用 `@allure.link` 添加链接
- [ ] 正确使用 `@allure.tag` 添加标签
- [ ] 报告中链接可点击跳转

---

**练习14：多环境配置管理**

**场景说明**：在实际项目中，需要在开发、测试、生产等不同环境运行测试。通过配置文件和命令行参数实现环境切换是常见做法。

**具体需求**：
1. 为 dev/test/prod 环境创建独立配置文件
2. 通过 `--env` 命令行参数选择环境
3. fixture 根据环境加载对应配置
4. 测试使用当前环境的配置

**使用示例**：

```yaml
# config/config.dev.yaml
base_url: http://localhost:8000
api_url: http://localhost:8000/api/v1
timeout: 60
debug: true
database:
  host: localhost
  port: 3306
  name: dev_db
```

```yaml
# config/config.test.yaml
base_url: https://test.example.com
api_url: https://test.example.com/api/v1
timeout: 30
debug: false
database:
  host: test-db.example.com
  port: 3306
  name: test_db
```

```yaml
# config/config.prod.yaml
base_url: https://example.com
api_url: https://example.com/api/v1
timeout: 10
debug: false
database:
  host: prod-db.example.com
  port: 3306
  name: prod_db
```

```python
# conftest.py
import pytest
import yaml
from pathlib import Path

def pytest_addoption(parser):
    """注册环境参数"""
    parser.addoption(
        "--env",
        default="test",
        choices=["dev", "test", "prod"],
        help="测试环境: dev, test, prod"
    )


@pytest.fixture(scope="session")
def env(request):
    """获取当前环境"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def config(env):
    """加载环境配置"""
    config_file = Path(f"config/config.{env}.yaml")

    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}")

    with open(config_file, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    print(f"\n=== 加载 {env} 环境配置 ===")
    print(f"    Base URL: {cfg['base_url']}")
    print(f"    Debug: {cfg['debug']}")

    return cfg


@pytest.fixture(scope="session")
def api_client(config):
    """API 客户端（根据环境配置）"""
    import requests

    session = requests.Session()
    session.base_url = config["api_url"]
    session.timeout = config["timeout"]

    if config["debug"]:
        print(f"\n    API 客户端已初始化: {session.base_url}")

    yield session
    session.close()
```

```python
# tests/test_with_config.py
import allure
import pytest

@allure.feature("环境配置测试")
def test_config_loaded(config, env):
    """测试配置已正确加载"""
    assert config["base_url"] is not None
    assert config["database"]["host"] is not None

    # 根据环境验证不同配置
    if env == "dev":
        assert config["debug"] is True
        assert "localhost" in config["base_url"]
    elif env == "prod":
        assert config["debug"] is False
        assert "example.com" in config["base_url"]


@allure.feature("API测试")
def test_api_with_config(api_client, config):
    """测试 API 使用环境配置"""
    # API 客户端已根据环境配置初始化
    assert api_client.base_url == config["api_url"]
    assert api_client.timeout == config["timeout"]
```

**运行命令**：
```bash
# 在测试环境运行
pytest tests/test_with_config.py --env=test -v

# 在开发环境运行
pytest tests/test_with_config.py --env=dev -v

# 生成 Allure 报告
pytest tests/test_with_config.py --env=test --alluredir=allure-results
allure serve allure-results
```

**验收标准**：
- [ ] 配置文件格式正确
- [ ] `--env` 参数正确注册
- [ ] fixture 正确加载配置
- [ ] 测试能使用环境配置

---

**练习15：完整 API 测试套件**

**场景说明**：综合运用 Allure 装饰器、步骤、附件等功能，编写专业的 API 测试套件。

**具体需求**：
1. 使用 Allure 完整标注（feature、story、title、severity）
2. 包含增删改查测试
3. 每个测试有清晰的步骤
4. 请求和响应作为附件记录

**使用示例**：
```python
# tests/test_user_api_complete.py
import allure
import pytest
import json

# ============================================
# 模拟 API 客户端
# ============================================
class MockAPIClient:
    """模拟 API 客户端"""

    def __init__(self):
        self.base_url = "https://api.example.com"
        self._users = {}
        self._next_id = 1

    def post(self, endpoint, json_data):
        """POST 请求"""
        if endpoint == "/users":
            user = {
                "id": self._next_id,
                **json_data
            }
            self._users[self._next_id] = user
            self._next_id += 1
            return MockResponse(201, user)

        return MockResponse(404, {"error": "Not found"})

    def get(self, endpoint):
        """GET 请求"""
        if endpoint == "/users":
            return MockResponse(200, list(self._users.values()))
        elif endpoint.startswith("/users/"):
            user_id = int(endpoint.split("/")[-1])
            if user_id in self._users:
                return MockResponse(200, self._users[user_id])
            return MockResponse(404, {"error": "User not found"})

        return MockResponse(404, {"error": "Not found"})

    def put(self, endpoint, json_data):
        """PUT 请求"""
        if endpoint.startswith("/users/"):
            user_id = int(endpoint.split("/")[-1])
            if user_id in self._users:
                self._users[user_id].update(json_data)
                return MockResponse(200, self._users[user_id])
            return MockResponse(404, {"error": "User not found"})

        return MockResponse(404, {"error": "Not found"})

    def delete(self, endpoint):
        """DELETE 请求"""
        if endpoint.startswith("/users/"):
            user_id = int(endpoint.split("/")[-1])
            if user_id in self._users:
                del self._users[user_id]
                return MockResponse(204, {})
            return MockResponse(404, {"error": "User not found"})

        return MockResponse(404, {"error": "Not found"})


class MockResponse:
    """模拟响应对象"""

    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data


@pytest.fixture
def api_client():
    """API 客户端 fixture"""
    return MockAPIClient()


# ============================================
# 测试类
# ============================================
@allure.feature("用户管理")
@allure.story("用户CRUD")
class TestUserAPI:
    """用户 API 完整测试"""

    # ----------------------------------------
    # 创建用户
    # ----------------------------------------
    @allure.title("创建新用户")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, api_client):
        """测试创建用户"""

        with allure.step("准备用户数据"):
            user_data = {
                "name": "张三",
                "email": "zhangsan@example.com",
                "age": 25
            }
            allure.attach(
                json.dumps(user_data, ensure_ascii=False, indent=2),
                name="请求数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("发送创建请求"):
            response = api_client.post("/users", json_data=user_data)
            allure.attach(
                json.dumps(response.json(), ensure_ascii=False, indent=2),
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("验证响应"):
            assert response.status_code == 201
            assert response.json()["id"] is not None
            assert response.json()["name"] == "张三"

    # ----------------------------------------
    # 查询用户列表
    # ----------------------------------------
    @allure.title("获取用户列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_users(self, api_client):
        """测试获取用户列表"""

        with allure.step("创建测试用户"):
            api_client.post("/users", json_data={"name": "用户1", "email": "user1@test.com"})
            api_client.post("/users", json_data={"name": "用户2", "email": "user2@test.com"})

        with allure.step("发送查询请求"):
            response = api_client.get("/users")
            allure.attach(
                json.dumps(response.json(), ensure_ascii=False, indent=2),
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("验证响应"):
            assert response.status_code == 200
            assert len(response.json()) >= 2

    # ----------------------------------------
    # 查询单个用户
    # ----------------------------------------
    @allure.title("获取单个用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_by_id(self, api_client):
        """测试获取单个用户"""

        with allure.step("创建测试用户"):
            create_response = api_client.post("/users", json_data={
                "name": "测试用户",
                "email": "test@test.com"
            })
            user_id = create_response.json()["id"]

        with allure.step("发送查询请求"):
            response = api_client.get(f"/users/{user_id}")
            allure.attach(
                json.dumps(response.json(), ensure_ascii=False, indent=2),
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("验证响应"):
            assert response.status_code == 200
            assert response.json()["id"] == user_id

    # ----------------------------------------
    # 更新用户
    # ----------------------------------------
    @allure.title("更新用户信息")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self, api_client):
        """测试更新用户"""

        with allure.step("创建测试用户"):
            create_response = api_client.post("/users", json_data={
                "name": "原始名称",
                "email": "original@test.com"
            })
            user_id = create_response.json()["id"]

        with allure.step("发送更新请求"):
            update_data = {"name": "更新名称", "age": 30}
            response = api_client.put(f"/users/{user_id}", json_data=update_data)
            allure.attach(
                json.dumps(response.json(), ensure_ascii=False, indent=2),
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("验证响应"):
            assert response.status_code == 200
            assert response.json()["name"] == "更新名称"
            assert response.json()["age"] == 30

    # ----------------------------------------
    # 删除用户
    # ----------------------------------------
    @allure.title("删除用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user(self, api_client):
        """测试删除用户"""

        with allure.step("创建测试用户"):
            create_response = api_client.post("/users", json_data={
                "name": "待删除用户",
                "email": "delete@test.com"
            })
            user_id = create_response.json()["id"]

        with allure.step("发送删除请求"):
            response = api_client.delete(f"/users/{user_id}")

        with allure.step("验证删除成功"):
            assert response.status_code == 204

        with allure.step("验证用户已不存在"):
            get_response = api_client.get(f"/users/{user_id}")
            assert get_response.status_code == 404
```

**验收标准**：
- [ ] 所有测试有完整的 Allure 标注
- [ ] 每个测试有清晰的步骤
- [ ] 请求和响应作为附件记录
- [ ] CRUD 操作全部覆盖

---

**练习16：生成和查看报告**

**场景说明**：掌握 Allure 报告的生成和查看方法，能够在实际项目中使用。

**具体需求**：
1. 安装 allure-pytest 插件和 allure 命令行工具
2. 运行测试生成 Allure 数据
3. 使用 `allure serve` 生成并打开报告
4. 使用 `allure generate` 生成静态报告

**安装步骤**：
```bash
# 1. 安装 Python 插件
pip install allure-pytest

# 2. 安装 Allure 命令行工具

# Mac (使用 Homebrew)
brew install allure

# Windows (使用 Scoop)
scoop install allure

# 或下载安装
# https://github.com/allure-framework/allure2/releases
# 下载后解压并添加到 PATH
```

**运行命令**：
```bash
# 运行测试并生成 Allure 数据
pytest tests/ --alluredir=allure-results

# 带详细输出
pytest tests/ -v --alluredir=allure-results

# 只运行冒烟测试
pytest tests/ -m smoke --alluredir=allure-results

# 生成并打开报告（推荐）
allure serve allure-results

# 生成静态 HTML 报告
allure generate allure-results -o allure-report --clean

# 打开已生成的报告
allure open allure-report

# 指定端口打开
allure open allure-report -p 8888
```

**报告功能说明**：
```
Allure 报告主要功能：

1. 概览页面
   - 测试统计
   - 通过率
   - 执行时间分布

2. 功能分类
   - 按 Feature 分组
   - 按 Story 分组
   - 按严重程度分组

3. 测试详情
   - 测试步骤
   - 附件（截图、日志）
   - 参数化数据
   - 关联链接

4. 图表分析
   - 趋势图
   - 持续时间图
   - 分类统计图

5. 时间线
   - 测试执行顺序
   - 并行执行情况
```

**CI/CD 集成示例**：
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install allure-pytest

      - name: Run tests
        run: pytest tests/ --alluredir=allure-results

      - name: Generate Allure report
        uses: simple-elf/allure-report-action@v1
        if: always()
        with:
          allure_results: allure-results
          allure_report: allure-report

      - name: Publish report
        uses: peaceiris/actions-gh-pages@v3
        if: always()
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: allure-report
```

**验收标准**：
- [ ] allure-pytest 安装成功
- [ ] allure 命令行工具安装成功
- [ ] 能生成 Allure 报告
- [ ] 能查看报告中的测试详情

# 打开已生成的报告
allure open allure-report
```

### 综合练习（17-20）

---

**练习17：用户 API 测试套件（完整版）**

**场景说明**：综合运用 Allure 报告的所有功能，编写一个完整的用户 API 测试套件，包含认证、CRUD、权限测试。

**具体需求**：
1. 使用 Allure 完整标注（feature、story、title、severity）
2. 包含登录认证测试（成功/失败场景）
3. 包含用户 CRUD 测试（增删改查）
4. 每个测试有清晰的步骤和附件

**使用示例**：
```python
# tests/test_user_api_complete.py
import allure
import pytest
import json

# ============================================
# 模拟 API 和数据
# ============================================
class MockUserAPI:
    """模拟用户 API"""
    def __init__(self):
        self._users = {}
        self._tokens = {}
        self._next_id = 1

    def login(self, username, password):
        if username == "admin" and password == "123456":
            token = f"token_{username}"
            self._tokens[username] = token
            return {"success": True, "token": token}
        return {"success": False, "error": "认证失败"}

    def create_user(self, token, data):
        if not token or not token.startswith("token_"):
            return {"status": 401, "error": "未授权"}
        user = {"id": self._next_id, **data}
        self._users[self._next_id] = user
        self._next_id += 1
        return {"status": 201, "data": user}

    def get_user(self, token, user_id):
        if user_id in self._users:
            return {"status": 200, "data": self._users[user_id]}
        return {"status": 404, "error": "用户不存在"}

    def update_user(self, token, user_id, data):
        if user_id in self._users:
            self._users[user_id].update(data)
            return {"status": 200, "data": self._users[user_id]}
        return {"status": 404, "error": "用户不存在"}

    def delete_user(self, token, user_id):
        if user_id in self._users:
            del self._users[user_id]
            return {"status": 204}
        return {"status": 404, "error": "用户不存在"}

    def list_users(self, token):
        return {"status": 200, "data": list(self._users.values())}


@pytest.fixture
def api():
    return MockUserAPI()


# ============================================
# 认证测试
# ============================================
@allure.feature("用户管理")
@allure.story("用户认证")
class TestUserAuth:
    """用户认证测试"""

    @allure.title("用户登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.issue("AUTH-001", name="登录功能")
    def test_login_success(self, api):
        """测试登录成功"""

        with allure.step("准备登录数据"):
            credentials = {"username": "admin", "password": "123456"}
            allure.attach(json.dumps(credentials), name="登录凭证")

        with allure.step("执行登录"):
            result = api.login(**credentials)
            allure.attach(json.dumps(result), name="登录结果")

        with allure.step("验证登录成功"):
            assert result["success"] is True
            assert "token" in result

    @allure.title("用户登录失败-密码错误")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, api):
        """测试密码错误"""

        with allure.step("使用错误密码登录"):
            result = api.login("admin", "wrong_password")

        with allure.step("验证登录失败"):
            assert result["success"] is False
            assert "error" in result


# ============================================
# CRUD 测试
# ============================================
@allure.feature("用户管理")
@allure.story("用户CRUD")
class TestUserCRUD:
    """用户 CRUD 测试"""

    @allure.title("创建用户")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, api):
        """测试创建用户"""

        with allure.step("获取认证 Token"):
            login_result = api.login("admin", "123456")
            token = login_result["token"]

        with allure.step("准备用户数据"):
            user_data = {"name": "张三", "email": "zhangsan@example.com", "role": "user"}
            allure.attach(json.dumps(user_data, ensure_ascii=False), name="用户数据")

        with allure.step("发送创建请求"):
            result = api.create_user(token, user_data)
            allure.attach(json.dumps(result, ensure_ascii=False), name="响应数据")

        with allure.step("验证创建成功"):
            assert result["status"] == 201
            assert result["data"]["id"] is not None

    @allure.title("查询用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user(self, api):
        """测试查询用户"""

        with allure.step("准备测试数据"):
            token = api.login("admin", "123456")["token"]
            created = api.create_user(token, {"name": "测试用户", "email": "test@test.com"})
            user_id = created["data"]["id"]

        with allure.step("查询用户"):
            result = api.get_user(token, user_id)
            allure.attach(json.dumps(result, ensure_ascii=False), name="查询结果")

        with allure.step("验证查询结果"):
            assert result["status"] == 200
            assert result["data"]["name"] == "测试用户"

    @allure.title("更新用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user(self, api):
        """测试更新用户"""

        with allure.step("准备测试数据"):
            token = api.login("admin", "123456")["token"]
            created = api.create_user(token, {"name": "原始名称", "email": "test@test.com"})
            user_id = created["data"]["id"]

        with allure.step("更新用户信息"):
            update_data = {"name": "更新名称", "age": 25}
            result = api.update_user(token, user_id, update_data)
            allure.attach(json.dumps(result, ensure_ascii=False), name="更新结果")

        with allure.step("验证更新成功"):
            assert result["status"] == 200
            assert result["data"]["name"] == "更新名称"

    @allure.title("删除用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user(self, api):
        """测试删除用户"""

        with allure.step("准备测试数据"):
            token = api.login("admin", "123456")["token"]
            created = api.create_user(token, {"name": "待删除", "email": "delete@test.com"})
            user_id = created["data"]["id"]

        with allure.step("删除用户"):
            result = api.delete_user(token, user_id)

        with allure.step("验证删除成功"):
            assert result["status"] == 204

        with allure.step("验证用户已不存在"):
            get_result = api.get_user(token, user_id)
            assert get_result["status"] == 404
```

**验收标准**：
- [ ] 所有测试有完整的 Allure 标注
- [ ] 认证测试覆盖成功和失败场景
- [ ] CRUD 测试覆盖增删改查
- [ ] 每个测试有清晰的步骤和附件

---

**练习18：多环境测试框架**

**场景说明**：搭建支持多环境（dev/test/prod）的测试框架，每个环境有独立配置，通过命令行参数切换。

**具体需求**：
1. 支持 dev/test/prod 三种环境
2. 每个环境有独立的 YAML 配置文件
3. 使用 `--env` 命令行参数指定环境
4. fixture 根据环境自动加载配置

**使用示例**：

```yaml
# config/config.dev.yaml
base_url: http://localhost:8000
api_url: http://localhost:8000/api/v1
timeout: 60
debug: true
database:
  host: localhost
  port: 3306
  name: dev_db
users:
  admin:
    username: admin
    password: admin123
```

```yaml
# config/config.test.yaml
base_url: https://test.example.com
api_url: https://test.example.com/api/v1
timeout: 30
debug: false
database:
  host: test-db.example.com
  port: 3306
  name: test_db
users:
  admin:
    username: admin
    password: test123
```

```yaml
# config/config.prod.yaml
base_url: https://example.com
api_url: https://example.com/api/v1
timeout: 10
debug: false
database:
  host: prod-db.example.com
  port: 3306
  name: prod_db
users:
  admin:
    username: admin
    password: prod123
```

```python
# conftest.py
import pytest
import yaml
import allure
from pathlib import Path

def pytest_addoption(parser):
    """注册环境参数"""
    parser.addoption(
        "--env",
        default="test",
        choices=["dev", "test", "prod"],
        help="测试环境: dev, test, prod"
    )


@pytest.fixture(scope="session")
def env(request):
    """获取当前环境"""
    env_value = request.config.getoption("--env")
    # 设置 Allure 报告的环境信息
    allure.environment(environment=env_value)
    return env_value


@pytest.fixture(scope="session")
def config(env):
    """加载环境配置"""
    config_path = Path(f"config/config.{env}.yaml")

    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    print(f"\n=== 加载 {env} 环境配置 ===")
    print(f"    Base URL: {cfg['base_url']}")
    print(f"    Debug Mode: {cfg['debug']}")

    return cfg


@pytest.fixture(scope="session")
def api_client(config):
    """API 客户端"""
    import requests

    session = requests.Session()
    session.base_url = config["api_url"]
    session.timeout = config["timeout"]

    yield session
    session.close()


@pytest.fixture
def admin_user(config):
    """管理员用户信息"""
    return config["users"]["admin"]
```

```python
# tests/test_multi_env.py
import allure
import pytest

@allure.feature("环境配置")
class TestEnvironment:

    @allure.title("验证环境配置加载")
    def test_config_loaded(self, config, env):
        """测试配置已正确加载"""
        assert config["base_url"] is not None
        assert config["database"]["host"] is not None

        # 根据环境验证不同配置
        if env == "dev":
            assert config["debug"] is True
            assert "localhost" in config["base_url"]
        elif env == "prod":
            assert config["debug"] is False

    @allure.title("验证管理员用户配置")
    def test_admin_user_config(self, admin_user, env):
        """测试管理员配置"""
        assert admin_user["username"] == "admin"
        assert admin_user["password"] is not None
```

**运行命令**：
```bash
# 在测试环境运行
pytest tests/ --env=test --alluredir=allure-results

# 在开发环境运行
pytest tests/ --env=dev -v

# 生成报告
allure serve allure-results
```

**验收标准**：
- [ ] 配置文件格式正确
- [ ] `--env` 参数正确注册
- [ ] 不同环境加载不同配置
- [ ] Allure 报告显示环境信息

---

**练习19：自定义插件开发**

**场景说明**：开发自定义 Pytest 插件，实现测试结果统计、自定义报告输出等功能。

**具体需求**：
1. 开发自定义 pytest 插件
2. 实现测试结果统计（通过/失败/跳过）
3. 计算测试执行时间
4. 生成自定义汇总报告

**使用示例**：

```python
# plugins/custom_reporter.py
"""自定义测试报告插件"""
import pytest
import time
from datetime import datetime


class CustomReporter:
    """自定义报告插件

    功能：
    1. 统计测试结果
    2. 计算执行时间
    3. 生成汇总报告
    """

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors = 0
        self.xfailed = 0
        self.xpassed = 0

        self.start_time = None
        self.end_time = None

        self.failed_tests = []
        self.test_durations = {}

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """捕获测试结果"""
        outcome = yield
        report = outcome.get_result()

        # 只在测试调用阶段统计
        if report.when == "call":
            # 记录执行时间
            self.test_durations[item.name] = call.duration

            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1
                self.failed_tests.append({
                    "name": item.name,
                    "error": str(call.excinfo) if call.excinfo else "Unknown"
                })
            elif report.skipped:
                self.skipped += 1

        # 统计 xfailed 和 xpassed
        if hasattr(report, "wasxfail"):
            if report.passed:
                self.xpassed += 1
            else:
                self.xfailed += 1

    def pytest_sessionstart(self, session):
        """测试会话开始"""
        self.start_time = datetime.now()
        print(f"\n{'=' * 60}")
        print(f"测试开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 60}")

    def pytest_sessionfinish(self, session, exitstatus):
        """测试会话结束"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()

        total = self.passed + self.failed + self.skipped + self.xfailed + self.xpassed
        pass_rate = (self.passed / total * 100) if total > 0 else 0

        print(f"\n{'=' * 60}")
        print("📊 测试结果汇总")
        print(f"{'=' * 60}")
        print(f"✅ 通过:   {self.passed:4d}")
        print(f"❌ 失败:   {self.failed:4d}")
        print(f"⏭️  跳过:   {self.skipped:4d}")
        print(f"⚠️  预期失败: {self.xfailed:4d}")
        print(f"🎉 意外通过: {self.xpassed:4d}")
        print(f"{'=' * 60}")
        print(f"📝 总计:   {total:4d}")
        print(f"📈 通过率: {pass_rate:.1f}%")
        print(f"⏱️  耗时:   {duration:.2f} 秒")
        print(f"{'=' * 60}")

        # 显示失败的测试
        if self.failed_tests:
            print("\n❌ 失败的测试:")
            for test in self.failed_tests:
                print(f"   - {test['name']}")
                print(f"     错误: {test['error'][:100]}...")

        # 显示最慢的测试
        if self.test_durations:
            print("\n🐢 最慢的 5 个测试:")
            sorted_tests = sorted(
                self.test_durations.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            for name, dur in sorted_tests:
                print(f"   - {name}: {dur:.3f}s")

        print(f"\n测试结束时间: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 60}\n")


# 创建插件实例
reporter = CustomReporter()


# 注册钩子
@pytest.hookimpl
def pytest_runtest_makereport(item, call):
    return reporter.pytest_runtest_makereport(item, call)


@pytest.hookimpl
def pytest_sessionstart(session):
    return reporter.pytest_sessionstart(session)


@pytest.hookimpl
def pytest_sessionfinish(session, exitstatus):
    return reporter.pytest_sessionfinish(session, exitstatus)
```

```python
# conftest.py
"""注册自定义插件"""

# 方式1：直接引用
from plugins.custom_reporter import reporter

# 方式2：使用 pytest_plugins
# pytest_plugins = ["plugins.custom_reporter"]
```

```python
# tests/test_with_plugin.py
import pytest

def test_pass_1():
    """这个测试会通过"""
    assert True

def test_pass_2():
    """这个测试会通过"""
    assert 1 + 1 == 2

def test_fail_1():
    """这个测试会失败"""
    assert False, "故意失败"

@pytest.mark.skip(reason="演示跳过")
def test_skip_1():
    """这个测试会被跳过"""
    assert True

@pytest.mark.xfail(reason="预期失败")
def test_xfail_1():
    """这个测试预期失败"""
    assert False
```

**验收标准**：
- [ ] 插件正确注册
- [ ] 统计数据准确
- [ ] 汇总报告格式清晰
- [ ] 显示失败的测试详情

---

**练习20：综合测试项目**

**场景说明**：整合所学知识，搭建一个完整的测试项目框架。

**具体需求**：
1. 多级 conftest.py 配置（全局/测试/API/UI）
2. 自定义命令行参数（--env, --browser, --headless）
3. fixture 工厂模式（动态创建测试数据）
4. Allure 报告集成
5. 钩子函数实现失败截图
6. 多环境配置支持

**项目结构**：
```
pytest_project/
├── pytest.ini              # Pytest 配置
├── conftest.py             # 全局配置
├── config/
│   ├── config.dev.yaml     # 开发环境配置
│   ├── config.test.yaml    # 测试环境配置
│   └── config.prod.yaml    # 生产环境配置
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # 测试级配置
│   ├── api/
│   │   ├── __init__.py
│   │   ├── conftest.py     # API 专用配置
│   │   ├── test_user.py    # 用户 API 测试
│   │   └── test_order.py   # 订单 API 测试
│   └── ui/
│       ├── __init__.py
│       ├── conftest.py     # UI 专用配置
│       └── test_home.py    # 首页 UI 测试
├── plugins/
│   ├── __init__.py
│   └── custom_reporter.py  # 自定义报告插件
├── utils/
│   ├── __init__.py
│   └── helpers.py          # 工具函数
├── allure-results/         # Allure 结果目录
└── requirements.txt        # 依赖列表
```

**配置文件示例**：

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
    --alluredir=allure-results
    -p no:warnings

markers =
    smoke: 冒烟测试
    regression: 回归测试
    api: API 测试
    ui: UI 测试
    p0: 最高优先级
    p1: 高优先级

minversion = 7.0
```

```python
# conftest.py（全局）
"""全局配置文件"""
import pytest
import yaml
import allure
from pathlib import Path

# ============================================
# 命令行参数
# ============================================
def pytest_addoption(parser):
    parser.addoption("--env", default="test", choices=["dev", "test", "prod"])
    parser.addoption("--browser", default="chrome", choices=["chrome", "firefox"])
    parser.addoption("--headless", action="store_true", default=False)


# ============================================
# 环境配置
# ============================================
@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def config(env):
    config_path = Path(f"config/config.{env}.yaml")
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # 设置 Allure 环境信息
    allure.environment(
        Environment=env,
        BaseURL=cfg["base_url"],
        Browser=request.config.getoption("--browser")
    )
    return cfg


# ============================================
# 工厂 fixture
# ============================================
@pytest.fixture
def make_user():
    """用户工厂 fixture"""
    created = []

    def _create(name, email, role="user"):
        user = {"id": len(created) + 1, "name": name, "email": email, "role": role}
        created.append(user)
        return user

    yield _create
    created.clear()


# ============================================
# 失败截图钩子
# ============================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "browser" in item.funcargs:
            driver = item.funcargs["browser"]
            if hasattr(driver, "get_screenshot_as_png"):
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"{item.name}_失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
```

```python
# tests/conftest.py
"""测试级配置"""
import pytest

@pytest.fixture(scope="module")
def test_data():
    """模块级测试数据"""
    return {
        "default_user": {"name": "test", "email": "test@test.com"}
    }
```

```python
# tests/api/conftest.py
"""API 测试专用配置"""
import pytest

@pytest.fixture
def api_client(config):
    """API 客户端"""
    import requests

    session = requests.Session()
    session.base_url = config["api_url"]

    yield session
    session.close()


@pytest.fixture
def auth_token(api_client):
    """认证 Token"""
    # 实际项目中这里会调用登录接口
    return "mock_token_xxx"
```

**运行命令**：
```bash
# 运行所有测试
pytest --env=test --alluredir=allure-results

# 只运行 API 测试
pytest tests/api/ -m api --env=test

# 只运行冒烟测试
pytest -m smoke --env=test

# 生成报告
allure serve allure-results
```

**验收标准**：
- [ ] 项目结构完整
- [ ] 多级 conftest 配置正确
- [ ] 命令行参数正常工作
- [ ] Allure 报告生成成功
- [ ] 工厂 fixture 可用
- [ ] 失败截图功能正常
