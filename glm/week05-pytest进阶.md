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

#### 练习1：fixture 工厂模式基础

```python
# tests/test_factory_fixture.py
# 要求：
# 1. 创建 make_user 工厂 fixture
# 2. 支持动态创建多个用户
# 3. 测试后自动清理创建的用户

import pytest

@pytest.fixture
def make_user():
    """工厂 fixture - 动态创建用户"""
    created_users = []

    def _make_user(name, role="user"):
        user = {"id": len(created_users) + 1, "name": name, "role": role}
        created_users.append(user)
        return user

    yield _make_user
    print(f"清理 {len(created_users)} 个用户")

def test_create_multiple_users(make_user):
    user1 = make_user("张三", "admin")
    user2 = make_user("李四", "user")
    assert user1["role"] == "admin"
    assert user2["name"] == "李四"
```

#### 练习2：参数化 fixture

```python
# tests/test_param_fixture.py
# 要求：
# 1. 创建参数化的 browser fixture
# 2. 支持多种浏览器类型
# 3. 为每个参数设置测试 ID

import pytest

@pytest.fixture(params=[
    pytest.param("chrome", id="Chrome浏览器"),
    pytest.param("firefox", id="Firefox浏览器"),
    pytest.param("safari", id="Safari浏览器", marks=pytest.mark.skip),
])
def browser(request):
    return request.param

def test_browser_type(browser):
    print(f"当前浏览器: {browser}")
    assert browser in ["chrome", "firefox", "safari"]
```

#### 练习3：indirect 参数化

```python
# tests/test_indirect_param.py
# 要求：
# 1. 创建 user_data fixture 接收外部参数
# 2. 在 fixture 中进行数据预处理
# 3. 使用 indirect=True 传递参数

import pytest

@pytest.fixture
def user_data(request):
    """通过 indirect 传递参数并预处理"""
    data = request.param
    return {
        "username": data["username"].upper(),
        "age": data["age"],
        "processed": True
    }

@pytest.mark.parametrize("user_data", [
    {"username": "admin", "age": 25},
    {"username": "guest", "age": 30},
], indirect=True)
def test_indirect_user(user_data):
    assert user_data["username"].isupper()
    assert user_data["processed"] is True
```

#### 练习4：多级 conftest 配置

```python
# 项目结构：
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

# project/conftest.py
import pytest

@pytest.fixture(scope="session")
def global_config():
    """全局配置"""
    return {"app_name": "MyApp", "version": "1.0"}

# tests/api/conftest.py
@pytest.fixture
def api_base_url():
    """API 专用 fixture"""
    return "https://api.example.com"

# tests/ui/conftest.py
@pytest.fixture
def browser():
    """UI 专用 fixture"""
    return {"type": "chrome", "headless": False}
```

#### 练习5：命令行参数基础

```python
# conftest.py
# 要求：
# 1. 添加 --env 命令行参数
# 2. 添加 --browser 命令行参数
# 3. 创建对应的 fixture 获取参数值

import pytest

def pytest_addoption(parser):
    parser.addoption("--env", default="test", help="测试环境")
    parser.addoption("--browser", default="chrome", help="浏览器类型")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")

# 使用：pytest --env=prod --browser=firefox
```

#### 练习6：钩子函数入门

```python
# conftest.py
# 要求：
# 1. 实现 pytest_configure 注册自定义标记
# 2. 实现 pytest_runtest_setup 在测试前执行操作
# 3. 实现 pytest_runtest_teardown 在测试后执行操作

import pytest

def pytest_configure(config):
    """配置阶段注册标记"""
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "p0: 最高优先级")

def pytest_runtest_setup(item):
    """每个测试执行前"""
    print(f"\n>>> 开始执行: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """每个测试执行后"""
    print(f">>> 执行完成: {item.name}")
```

#### 练习7：Allure 基础装饰器

```python
# tests/test_allure_basic.py
# 要求：
# 1. 使用 @allure.feature 标注功能模块
# 2. 使用 @allure.story 标注用户故事
# 3. 使用 @allure.title 设置测试标题
# 4. 使用 @allure.severity 设置严重程度

import allure
import pytest

@allure.feature("用户管理")
@allure.story("用户登录")
class TestLogin:

    @allure.title("登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self):
        assert True

    @allure.title("登录失败-密码错误")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self):
        assert True
```

#### 练习8：Allure 步骤和附件

```python
# tests/test_allure_steps.py
# 要求：
# 1. 使用 with allure.step() 添加测试步骤
# 2. 使用 allure.attach() 添加文本附件
# 3. 使用 allure.attach.file() 添加文件附件

import allure
import pytest

@allure.step("执行登录")
def login(username, password):
    allure.attach(username, name="用户名")
    return {"token": "xxx"}

@allure.step("获取用户信息")
def get_user_info(token):
    return {"name": "张三", "age": 25}

@allure.feature("用户模块")
def test_login_flow():
    with allure.step("步骤1：登录"):
        token = login("admin", "123456")

    with allure.step("步骤2：获取用户信息"):
        user = get_user_info(token)

    with allure.step("步骤3：验证结果"):
        allure.attach(str(user), name="用户数据", attachment_type=allure.attachment_type.JSON)
        assert user["name"] == "张三"
```

### 进阶练习（9-16）

#### 练习9：fixture 依赖链

```python
# tests/test_fixture_chain.py
# 要求：
# 1. 创建 config fixture（session 级别）
# 2. 创建 db_connection fixture 依赖 config
# 3. 创建 test_data fixture 依赖 db_connection
# 4. 验证 fixture 依赖关系

import pytest

@pytest.fixture(scope="session")
def config():
    return {"db_host": "localhost", "db_port": 3306}

@pytest.fixture(scope="module")
def db_connection(config):
    print(f"连接数据库: {config['db_host']}")
    conn = {"connected": True}
    yield conn
    print("关闭数据库连接")

@pytest.fixture
def test_data(db_connection):
    return [{"id": 1, "name": "user1"}]

def test_with_dependencies(test_data, db_connection, config):
    assert db_connection["connected"]
    assert len(test_data) == 1
```

#### 练习10：测试排序钩子

```python
# conftest.py
# 要求：
# 1. 实现 pytest_collection_modifyitems 钩子
# 2. 将冒烟测试排在前面
# 3. 其他测试排在后面

import pytest

def pytest_collection_modifyitems(config, items):
    """修改测试执行顺序"""
    smoke_tests = []
    other_tests = []

    for item in items:
        if "smoke" in item.keywords:
            smoke_tests.append(item)
        else:
            other_tests.append(item)

    items[:] = smoke_tests + other_tests

# tests/test_order.py
@pytest.mark.smoke
def test_smoke_1():
    pass

def test_other_1():
    pass

@pytest.mark.smoke
def test_smoke_2():
    pass
```

#### 练习11：失败截图钩子

```python
# conftest.py
# 要求：
# 1. 实现 pytest_runtest_makereport 钩子
# 2. 测试失败时自动截图
# 3. 将截图附加到 Allure 报告

import pytest
import allure

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 获取 fixture 中的 driver
        if "browser" in item.funcargs:
            driver = item.funcargs["browser"]
            # 截图并附加到 Allure
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"{item.name}_失败截图",
                attachment_type=allure.attachment_type.PNG
            )

        # 附加失败信息
        allure.attach(
            str(report.longrepr),
            name="失败详情",
            attachment_type=allure.attachment_type.TEXT
        )
```

#### 练习12：动态 Allure 属性

```python
# tests/test_allure_dynamic.py
# 要求：
# 1. 使用 allure.dynamic.title() 动态设置标题
# 2. 使用 allure.dynamic.feature() 动态设置模块
# 3. 在参数化测试中使用动态属性

import allure
import pytest

@pytest.mark.parametrize("username,role", [
    ("admin", "管理员"),
    ("user", "普通用户"),
    ("guest", "访客"),
])
def test_dynamic_allure(username, role):
    # 动态设置标题
    allure.dynamic.title(f"测试用户: {username} ({role})")

    # 动态设置参数
    allure.dynamic.parameter("用户名", username)
    allure.dynamic.parameter("角色", role)

    # 动态设置描述
    allure.dynamic.description(f"正在测试 {role} 的权限")

    assert username is not None
```

#### 练习13：Allure 关联管理

```python
# tests/test_allure_links.py
# 要求：
# 1. 使用 @allure.issue 关联 Bug
# 2. 使用 @allure.testcase 关联测试用例
# 3. 使用 @allure.link 添加文档链接

import allure
import pytest

@allure.feature("订单模块")
@allure.story("创建订单")
@allure.issue("BUG-123", name="订单创建失败")
@allure.testcase("TC-001", name="创建订单测试用例")
@allure.link("https://docs.example.com/orders", name="订单API文档")
def test_create_order_with_links():
    """测试创建订单，关联相关资源"""
    assert True

@allure.tag("p0", "smoke")
@allure.severity(allure.severity_level.BLOCKER)
def test_critical_with_tags():
    """带标签和严重程度的测试"""
    assert True
```

#### 练习14：多环境配置管理

```python
# config/config.test.yaml
# base_url: https://test.api.example.com
# timeout: 30

# config/config.prod.yaml
# base_url: https://api.example.com
# timeout: 60

# conftest.py
import pytest
import yaml
from pathlib import Path

def pytest_addoption(parser):
    parser.addoption("--env", default="test", help="环境: dev, test, prod")

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    config_file = Path(f"config/config.{env}.yaml")
    with open(config_file) as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def api_client(config):
    import requests
    session = requests.Session()
    session.base_url = config["base_url"]
    yield session
    session.close()

# tests/test_with_config.py
def test_with_env_config(config, api_client):
    assert config["base_url"] is not None
```

#### 练习15：完整 API 测试套件

```python
# tests/test_user_api.py
# 要求：
# 1. 使用 Allure 完整标注
# 2. 包含增删改查测试
# 3. 每个测试有清晰的步骤

import allure
import pytest

@allure.feature("用户管理")
class TestUserAPI:

    @allure.story("创建用户")
    @allure.title("创建新用户")
    def test_create_user(self, api_client):
        with allure.step("准备用户数据"):
            user_data = {"name": "张三", "email": "zhangsan@example.com"}

        with allure.step("发送创建请求"):
            response = api_client.post("/users", json=user_data)
            allure.attach(str(response.json()), name="响应")

        with allure.step("验证响应"):
            assert response.status_code == 201

    @allure.story("查询用户")
    @allure.title("获取用户列表")
    def test_get_users(self, api_client):
        with allure.step("发送查询请求"):
            response = api_client.get("/users")

        with allure.step("验证响应"):
            assert response.status_code == 200
```

#### 练习16：生成和查看报告

```bash
# 要求：
# 1. 安装 allure-pytest 和 allure 命令行工具
# 2. 运行测试生成 Allure 数据
# 3. 生成 HTML 报告
# 4. 在报告中查看测试结果

# 安装
pip install allure-pytest
brew install allure  # Mac

# 运行测试并生成数据
pytest --alluredir=allure-results

# 生成并打开报告
allure serve allure-results

# 生成静态报告
allure generate allure-results -o allure-report --clean

# 打开已生成的报告
allure open allure-report
```

### 综合练习（17-20）

#### 练习17：用户 API 测试套件（完整版）

```python
# tests/test_user_api_complete.py
# 要求：
# 1. 使用 Allure 完整标注的用户 API 测试
# 2. 包含登录、CRUD、权限测试
# 3. 每个测试有 feature、story、title、severity

import allure
import pytest

@allure.feature("用户管理")
@allure.story("用户认证")
class TestUserAuth:

    @allure.title("用户登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self, api_client):
        with allure.step("输入正确的用户名密码"):
            pass

        with allure.step("验证登录成功"):
            pass

    @allure.title("用户登录失败-密码错误")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, api_client):
        pass

@allure.feature("用户管理")
@allure.story("用户CRUD")
class TestUserCRUD:

    @allure.title("创建用户")
    def test_create_user(self, api_client):
        pass

    @allure.title("查询用户")
    def test_get_user(self, api_client):
        pass

    @allure.title("更新用户")
    def test_update_user(self, api_client):
        pass

    @allure.title("删除用户")
    def test_delete_user(self, api_client):
        pass
```

#### 练习18：多环境测试框架

```python
# 要求：
# 1. 支持 dev/test/prod 环境切换
# 2. 每个环境有独立配置文件
# 3. 使用命令行参数指定环境

# 项目结构：
# config/
# ├── config.dev.yaml
# ├── config.test.yaml
# └── config.prod.yaml
# tests/
# ├── conftest.py
# └── test_api.py

# conftest.py
import pytest
import yaml
from pathlib import Path

def pytest_addoption(parser):
    parser.addoption("--env", default="test")

@pytest.fixture(scope="session")
def env_config(request):
    env = request.config.getoption("--env")
    config_path = Path(f"config/config.{env}.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)

# 运行：pytest --env=prod
```

#### 练习19：自定义插件开发

```python
# plugins/custom_reporter.py
# 要求：
# 1. 开发自定义 pytest 插件
# 2. 实现测试结果统计
# 3. 生成自定义报告

import pytest

class CustomReporter:
    """自定义报告插件"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()

        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1
            elif report.skipped:
                self.skipped += 1

    def pytest_sessionfinish(self, session):
        print(f"\n=== 测试统计 ===")
        print(f"通过: {self.passed}")
        print(f"失败: {self.failed}")
        print(f"跳过: {self.skipped}")

# 在 conftest.py 中注册
# pytest_plugins = ["plugins.custom_reporter"]
```

#### 练习20：综合测试项目

```python
# 要求：整合所学知识，搭建完整测试项目
# 1. 多级 conftest.py 配置
# 2. 自定义命令行参数
# 3. fixture 工厂模式
# 4. Allure 报告集成
# 5. 钩子函数实现失败截图
# 6. 多环境配置支持

# 项目结构：
# project/
# ├── pytest.ini
# ├── conftest.py           # 全局配置
# ├── config/
# │   ├── config.dev.yaml
# │   ├── config.test.yaml
# │   └── config.prod.yaml
# ├── tests/
# │   ├── conftest.py       # 测试级配置
# │   ├── api/
# │   │   ├── conftest.py
# │   │   ├── test_user.py
# │   │   └── test_order.py
# │   └── ui/
# │       ├── conftest.py
# │       └── test_home.py
# ├── plugins/
# │   └── custom_reporter.py
# └── requirements.txt

# 运行命令：
# pytest --env=test --alluredir=allure-results
# allure serve allure-results
```

---

## 五、本周小结

1. **fixture 进阶**：工厂模式、参数化、indirect
2. **conftest**：多级配置、钩子函数
3. **Allure**：专业测试报告必备技能

### 下周预告

第6周开始接口自动化测试实战。
