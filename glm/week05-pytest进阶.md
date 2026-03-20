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

### 练习1：用户 API 测试套件

使用 Allure 完整标注的用户 API 测试

### 练习2：多环境配置

支持 dev/test/prod 环境切换

### 练习3：生成报告

运行测试并生成 Allure HTML 报告

---

## 五、本周小结

1. **fixture 进阶**：工厂模式、参数化、indirect
2. **conftest**：多级配置、钩子函数
3. **Allure**：专业测试报告必备技能

### 下周预告

第6周开始接口自动化测试实战。
