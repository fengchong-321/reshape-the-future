# 第20周：Playwright UI 自动化

## 本周目标

掌握 Playwright UI 自动化测试框架，能编写稳定的 UI 测试脚本。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Playwright 安装 | 安装、浏览器管理 | ⭐⭐⭐⭐ |
| 定位器 | 选择器、最佳实践 | ⭐⭐⭐⭐⭐ |
| 页面操作 | 点击、输入、等待 | ⭐⭐⭐⭐⭐ |
| 断言 | 内置断言、自定义 | ⭐⭐⭐⭐⭐ |
| 高级特性 | iframe、文件、多标签 | ⭐⭐⭐⭐ |
| Page Object | 设计模式 | ⭐⭐⭐⭐⭐ |
| 并行执行 | 多浏览器、多进程 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 安装与配置

```bash
# 安装
pip install playwright pytest-playwright

# 安装浏览器
playwright install
playwright install chromium  # 只安装 Chromium
playwright install firefox

# 生成代码（录制）
playwright codegen https://example.com

# 运行测试
pytest tests/ --headed  # 显示浏览器
pytest tests/ --headed --slowmo=1000  # 慢速执行
```

```python
# ============================================
# 基础配置
# ============================================
# conftest.py
import pytest
from playwright.sync_api import Browser, Page, BrowserContext

@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    """每个测试创建新的页面"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def authenticated_page(page: Page) -> Page:
    """已登录的页面"""
    page.goto("https://example.com/login")
    page.fill("#username", "testuser")
    page.fill("#password", "password123")
    page.click("button[type=submit]")
    page.wait_for_url("**/dashboard")
    yield page

# pytest.ini
"""
[pytest]
addopts = --headed --slowmo=100 --browser chromium
"""
```

---

### 2.2 定位器（Locator）

```python
from playwright.sync_api import Page, expect

# ============================================
# 基本定位器
# ============================================
# CSS 选择器
page.locator("button").click()
page.locator(".submit-btn").click()
page.locator("#login-button").click()
page.locator("button[type=submit]").click()

# 文本定位器
page.locator("text=登录").click()
page.locator("text=/登录|Login/i").click()  # 正则

# 组合定位器
page.locator("article:has-text='测试')").click()
page.locator("div.card >> text=详情").click()

# ============================================
# 推荐的定位方式（按优先级）
# ============================================
# 1. role 定位器（最推荐）
page.get_by_role("button", name="登录").click()
page.get_by_role("link", name="首页").click()
page.get_by_role("textbox", name="用户名").fill("admin")

# 2. label 定位器
page.get_by_label("用户名").fill("admin")
page.get_by_label("密码").fill("123456")

# 3. placeholder 定位器
page.get_by_placeholder("请输入用户名").fill("admin")

# 4. text 定位器
page.get_by_text("欢迎").click()

# 5. test id 定位器（需要设置 data-testid）
page.get_by_test_id("submit-button").click()

# ============================================
# 链式定位器
# ============================================
# 在某个元素内查找
card = page.locator(".card")
card.locator("button").click()

# 过滤
page.locator("tr").filter(has_text="张三").locator("button").click()

# ============================================
# 定位器最佳实践
# ============================================
"""
1. 优先使用 role 定位器（语义化）
2. 其次使用 label/placeholder
3. 避免使用 XPath
4. 添加 data-testid 给动态元素
5. 使用稳定的属性，避免动态 class
"""
```

---

### 2.3 页面操作

```python
from playwright.sync_api import Page

def test_page_operations(page: Page):
    # ============================================
    # 导航
    # ============================================
    page.goto("https://example.com")
    page.goto("https://example.com", wait_until="networkidle")
    page.go_back()
    page.go_forward()
    page.reload()

    # ============================================
    # 输入操作
    # ============================================
    # 填写输入框
    page.fill("#username", "admin")
    page.type("#username", "admin", delay=100)  # 模拟打字

    # 清空后填写
    page.locator("#username").clear()
    page.fill("#username", "new value")

    # 勾选复选框
    page.check("#agree")
    page.uncheck("#agree")
    assert page.is_checked("#agree")

    # 选择下拉框
    page.select_option("#country", "china")
    page.select_option("#country", label="中国")
    page.select_option("#country", index=0)

    # 上传文件
    page.set_input_files("#file", "/path/to/file.pdf")
    page.set_input_files("#file", ["/path/file1.pdf", "/path/file2.pdf"])

    # ============================================
    # 点击操作
    # ============================================
    page.click("button")
    page.click("button", force=True)  # 强制点击（忽略可见性）
    page.click("button", position={"x": 10, "y": 20})  # 点击偏移位置
    page.click("button", modifiers=["Shift"])  # 带按键点击
    page.dblclick("button")  # 双击
    page.right_click("button")  # 右键

    # ============================================
    # 键盘操作
    # ============================================
    page.press("#input", "Enter")
    page.press("#input", "Control+A")  # Ctrl+A
    page.press("#input", "ArrowDown")
    page.keyboard.press("Escape")

    # 输入文本
    page.keyboard.type("hello world")

    # ============================================
    # 鼠标操作
    # ============================================
    page.mouse.click(100, 200)
    page.mouse.dblclick(100, 200)
    page.mouse.move(100, 200)
    page.mouse.down()
    page.mouse.up()

    # 拖拽
    page.drag_and_drop("#source", "#target")

    # 滚动
    page.locator("#element").scroll_into_view_if_needed()
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # ============================================
    # 等待
    # ============================================
    # 等待元素出现
    page.wait_for_selector("#element")
    page.wait_for_selector("#element", state="hidden")  # 等待消失
    page.wait_for_selector("#element", state="visible")  # 等待可见

    # 等待导航
    with page.expect_navigation():
        page.click("a")

    # 等待请求
    with page.expect_request("**/api/users"):
        page.click("button")

    # 等待响应
    with page.expect_response("**/api/users") as response:
        page.click("button")
    data = response.value().json()

    # 等待超时
    page.wait_for_timeout(1000)  # 1秒（不推荐）

    # 等待 URL
    page.wait_for_url("**/dashboard")

    # 等待加载状态
    page.wait_for_load_state("networkidle")
```

---

### 2.4 断言

```python
from playwright.sync_api import Page, expect

def test_assertions(page: Page):
    page.goto("https://example.com")

    # ============================================
    # 元素断言
    # ============================================
    # 可见性
    expect(page.locator("#element")).to_be_visible()
    expect(page.locator("#element")).to_be_hidden()
    expect(page.locator("#element")).not_to_be_visible()

    # 文本内容
    expect(page.locator("#title")).to_have_text("欢迎")
    expect(page.locator("#title")).to_contain_text("迎")
    expect(page.locator("#title")).to_have_text(re.compile(r"欢.*迎"))

    # 属性
    expect(page.locator("#input")).to_have_value("admin")
    expect(page.locator("#input")).to_be_empty()
    expect(page.locator("#link")).to_have_attribute("href", "/home")

    # 状态
    expect(page.locator("#button")).to_be_enabled()
    expect(page.locator("#button")).to_be_disabled()
    expect(page.locator("#checkbox")).to_be_checked()

    # 数量
    expect(page.locator(".item")).to_have_count(5)

    # ============================================
    # 页面断言
    # ============================================
    expect(page).to_have_title("首页")
    expect(page).to_have_title(re.compile(r"首页.*"))
    expect(page).to_have_url("https://example.com/home")
    expect(page).to_have_url(re.compile(r".*/home"))

    # ============================================
    # 截图断言
    # ============================================
    expect(page).to_have_screenshot("homepage.png")

    # ============================================
    # 自定义断言
    # ============================================
    text = page.locator("#element").text_content()
    assert "关键词" in text

    element = page.locator("#element")
    assert element.is_visible()
```

---

### 2.5 高级特性

```python
from playwright.sync_api import Page, BrowserContext

# ============================================
# iframe 操作
# ============================================
def test_iframe(page: Page):
    page.goto("https://example.com")

    # 进入 iframe
    frame = page.frame_locator("#myframe")
    frame.fill("#input", "test")
    frame.click("button")

    # 多层 iframe
    inner_frame = frame.frame_locator("#inner-frame")
    inner_frame.click("#button")

# ============================================
# 多标签页
# ============================================
def test_multiple_tabs(page: Page, context: BrowserContext):
    page.goto("https://example.com")

    # 点击打开新标签页
    with context.expect_page() as new_page_info:
        page.click("a[target=_blank]")
    new_page = new_page_info.value

    # 在新标签页操作
    new_page.fill("#search", "test")

    # 切换回原标签页
    page.bring_to_front()

    # 获取所有页面
    pages = context.pages

# ============================================
# 对话框处理
# ============================================
def test_dialog(page: Page):
    # 自动接受对话框
    page.on("dialog", lambda dialog: dialog.accept())

    # 手动处理
    def handle_dialog(dialog):
        print(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.click("button")

# ============================================
# 拦截请求
# ============================================
def test_intercept(page: Page):
    # 拦截并修改响应
    def handle_route(route):
        if "api/users" in route.request.url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"users": []}'
            )
        else:
            route.continue_()

    page.route("**/*", handle_route)
    page.goto("https://example.com")

    # Mock API
    page.route("**/api/users", lambda route: route.fulfill(
        status=200,
        body='[{"id": 1, "name": "张三"}]'
    ))

# ============================================
# 网络监控
# ============================================
def test_network(page: Page):
    # 监听请求
    page.on("request", lambda req: print(f">> {req.method} {req.url}"))

    # 监听响应
    page.on("response", lambda res: print(f"<< {res.status} {res.url}"))

# ============================================
# 设备模拟
# ============================================
def test_mobile(page: Page):
    # 模拟 iPhone
    iphone = playwright.devices["iPhone 13"]
    context = browser.new_context(**iphone)
    page = context.new_page()

    # 模拟地理位置
    context.set_geolocation({"latitude": 31.2304, "longitude": 121.4737})

    # 模拟离线
    context.set_offline(True)
```

---

### 2.6 Page Object 模式

```python
# ============================================
# Page Object 示例
# ============================================
# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    """登录页面"""

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_label("用户名")
        self.password_input = page.get_by_label("密码")
        self.login_button = page.get_by_role("button", name="登录")
        self.error_message = page.locator(".error-message")

    def navigate(self):
        """导航到登录页"""
        self.page.goto("/login")
        return self

    def login(self, username: str, password: str):
        """执行登录"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def expect_error(self, message: str):
        """验证错误消息"""
        expect(self.error_message).to_have_text(message)

    def expect_login_success(self):
        """验证登录成功"""
        expect(self.page).to_have_url("**/dashboard")


# pages/home_page.py
class HomePage:
    """首页"""

    def __init__(self, page: Page):
        self.page = page
        self.welcome_text = page.locator(".welcome")
        self.user_menu = page.locator(".user-menu")

    def navigate(self):
        self.page.goto("/")
        return self

    def is_logged_in(self) -> bool:
        return self.user_menu.is_visible()

    def logout(self):
        self.user_menu.click()
        self.page.get_by_text("退出").click()


# ============================================
# 测试用例
# ============================================
# tests/test_login.py
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage

class TestLogin:

    def test_login_success(self, page):
        login_page = LoginPage(page)
        home_page = HomePage(page)

        # 导航到登录页
        login_page.navigate()

        # 执行登录
        login_page.login("admin", "password123")

        # 验证登录成功
        login_page.expect_login_success()
        assert home_page.is_logged_in()

    def test_login_wrong_password(self, page):
        login_page = LoginPage(page)

        login_page.navigate()
        login_page.login("admin", "wrongpassword")

        login_page.expect_error("用户名或密码错误")


# ============================================
# Base Page 模式
# ============================================
class BasePage:
    """页面基类"""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str):
        self.page.goto(f"{self.base_url}{path}")

    def wait_for_loading(self):
        self.page.wait_for_selector(".loading", state="hidden")

    def take_screenshot(self, name: str):
        self.page.screenshot(path=f"screenshots/{name}.png")


class ProductPage(BasePage):
    """商品页面"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.product_list = page.locator(".product-item")
        self.search_input = page.get_by_placeholder("搜索商品")

    def search(self, keyword: str):
        self.search_input.fill(keyword)
        self.page.keyboard.press("Enter")
        self.wait_for_loading()

    def get_product_names(self) -> list:
        return self.product_list.all_inner_texts()
```

---

### 2.7 并行执行与配置

```python
# ============================================
# pytest 配置
# ============================================
# pytest.ini
"""
[pytest]
addopts = 
    --headed
    --browser chromium
    --browser firefox
    --browser webkit
    --slowmo=100
    --video=retain-on-failure
    --screenshot=only-on-failure
    --trace=retain-on-failure
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
"""

# ============================================
# conftest.py 完整配置
# ============================================
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "headless": True,
        "args": ["--start-maximized"]
    }

@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "videos/",
        "trace": "retain-on-failure"
    }

@pytest.fixture(scope="function")
def page(browser: Browser, browser_context_args):
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    yield page
    context.close()

# ============================================
# 并行执行
# ============================================
# 安装：pip install pytest-xdist
# 运行：pytest -n 4  # 4个进程并行

# ============================================
# 失败重试
# ============================================
# 安装：pip install pytest-rerunfailures
# 运行：pytest --reruns 3 --reruns-delay 1
```

---

## 三、学到什么程度

### 必须掌握

- [ ] Playwright 基础操作
- [ ] 定位器使用
- [ ] 断言方法
- [ ] Page Object 模式

### 应该了解

- [ ] 请求拦截
- [ ] 并行执行
- [ ] 视频录制

---

## 四、练习内容（20 题）

### 基础练习（1-8）

---

**练习1：环境搭建与基础脚本**

**场景说明**：作为测试工程师，你需要搭建 Playwright 自动化测试环境，并编写第一个测试脚本来验证环境配置是否正确。

**具体需求**：
1. 使用 pip 安装 `playwright` 和 `pytest-playwright`
2. 安装 Chromium 浏览器（`playwright install chromium`）
3. 编写测试脚本访问 `https://example.com`
4. 使用 `expect` 断言验证页面标题包含 "Example Domain"
5. 使用 `sync_playwright` 上下文管理器管理浏览器生命周期

**使用示例**：
```python
from playwright.sync_api import sync_playwright, expect

def test_first_script():
    """第一个 Playwright 测试脚本"""
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 访问页面
        page.goto("https://example.com")

        # 验证标题
        expect(page).to_have_title("Example Domain")

        # 关闭浏览器
        browser.close()

# 预期输出：测试通过，浏览器打开并访问 example.com
```

**验收标准**：
- [ ] Playwright 安装成功，无报错
- [ ] Chromium 浏览器安装成功
- [ ] 测试脚本能正常启动浏览器
- [ ] 页面标题断言通过

---

**练习2：定位器使用**

**场景说明**：在编写 UI 自动化测试时，定位元素是最核心的技能。你需要掌握 Playwright 推荐的各种定位方式。

**具体需求**：
1. 使用 `get_by_role` 定位一个按钮（如"提交"按钮）
2. 使用 `get_by_label` 定位一个输入框（通过 label 文本）
3. 使用 `get_by_text` 定位一个链接或文本元素
4. 使用 `get_by_test_id` 定位一个带有 `data-testid` 属性的元素
5. 使用 `get_by_placeholder` 定位一个输入框（通过 placeholder 文本）

**使用示例**：
```python
from playwright.sync_api import Page

def test_locators(page: Page):
    page.goto("https://example.com/form")

    # 1. 使用 role 定位按钮
    submit_button = page.get_by_role("button", name="提交")
    submit_button.click()

    # 2. 使用 label 定位输入框
    username_input = page.get_by_label("用户名")
    username_input.fill("admin")

    # 3. 使用 text 定位链接
    home_link = page.get_by_text("返回首页")
    home_link.click()

    # 4. 使用 test_id 定位元素
    logout_button = page.get_by_test_id("logout-btn")
    logout_button.click()

    # 5. 使用 placeholder 定位
    search_input = page.get_by_placeholder("请输入搜索关键词")
    search_input.fill("Playwright")
```

**验收标准**：
- [ ] 能正确使用 role 定位器
- [ ] 能正确使用 label 定位器
- [ ] 能正确使用 text 定位器
- [ ] 能正确使用 test_id 定位器
- [ ] 能正确使用 placeholder 定位器

---

**练习3：表单操作练习**

**场景说明**：登录功能是 Web 应用最常见的功能，编写登录表单测试是 UI 自动化的基础。

**具体需求**：
1. 打开登录页面 `https://example.com/login`
2. 使用 `fill()` 方法填写用户名输入框
3. 使用 `fill()` 方法填写密码输入框
4. 使用 `check()` 方法勾选"记住我"复选框
5. 使用 `click()` 方法点击登录按钮
6. 使用 `expect` 断言验证登录成功（检查 URL 或欢迎信息）

**使用示例**：
```python
from playwright.sync_api import Page, expect

def test_login_form(page: Page):
    # 打开登录页面
    page.goto("https://example.com/login")

    # 填写用户名
    page.get_by_label("用户名").fill("testuser")

    # 填写密码
    page.get_by_label("密码").fill("password123")

    # 勾选"记住我"
    page.get_by_label("记住我").check()

    # 点击登录按钮
    page.get_by_role("button", name="登录").click()

    # 验证登录成功（检查 URL 跳转）
    expect(page).to_have_url("**/dashboard")

    # 验证欢迎信息
    welcome = page.locator(".welcome-message")
    expect(welcome).to_contain_text("欢迎")

# 预期输出：测试通过，成功登录并跳转到 dashboard 页面
```

**验收标准**：
- [ ] 能正确填写文本输入框
- [ ] 能正确勾选复选框
- [ ] 能正确点击按钮
- [ ] 登录成功后 URL 断言通过
- [ ] 登录成功后页面元素断言通过

---

**练习4：下拉框与文件上传**

**场景说明**：在用户注册或商品筛选场景中，经常需要操作下拉框和上传文件。

**具体需求**：
1. 使用 `select_option()` 方法选择下拉框选项（按 value、label 或 index）
2. 使用 `set_input_files()` 方法上传单个文件
3. 使用 `set_input_files()` 方法上传多个文件
4. 验证下拉框选中值正确
5. 验证文件上传成功

**使用示例**：
```python
from playwright.sync_api import Page, expect
import os

def test_select_and_upload(page: Page):
    page.goto("https://example.com/form")

    # ========== 下拉框操作 ==========
    # 按 value 选择
    page.select_option("#country", value="china")

    # 按 label（显示文本）选择
    page.select_option("#city", label="北京")

    # 按索引选择
    page.select_option("#gender", index=1)  # 选择第二个选项

    # 验证选中值
    selected_value = page.locator("#country").input_value()
    assert selected_value == "china"

    # ========== 文件上传 ==========
    # 上传单个文件
    page.set_input_files("#avatar", "/path/to/avatar.jpg")

    # 上传多个文件
    page.set_input_files("#documents", [
        "/path/to/doc1.pdf",
        "/path/to/doc2.pdf"
    ])

    # 清空已上传的文件
    page.set_input_files("#avatar", [])

    # 验证文件上传成功
    expect(page.locator(".upload-success")).to_be_visible()
```

**验收标准**：
- [ ] 能使用三种方式选择下拉框选项
- [ ] 能上传单个文件
- [ ] 能上传多个文件
- [ ] 能清空已上传文件
- [ ] 能验证操作结果

---

**练习5：等待策略**

**场景说明**：现代 Web 应用大量使用 AJAX 和动态加载，掌握正确的等待策略是编写稳定测试的关键。

**具体需求**：
1. 使用 `wait_for_selector()` 等待元素出现/消失
2. 使用 `wait_for_load_state()` 等待页面加载完成
3. 使用 `expect_navigation()` 等待导航完成
4. 使用 `expect_request()` 等待请求发出
5. 使用 `expect_response()` 等待响应返回

**使用示例**：
```python
from playwright.sync_api import Page, expect

def test_waiting_strategies(page: Page):
    page.goto("https://example.com")

    # ========== 等待元素 ==========
    # 等待元素出现（可见）
    page.wait_for_selector(".loading", state="hidden")
    page.wait_for_selector(".content", state="visible")

    # 等待元素可点击（附加状态）
    page.get_by_role("button", name="提交").wait_for(state="visible")

    # ========== 等待页面加载 ==========
    page.wait_for_load_state("networkidle")  # 等待网络空闲
    page.wait_for_load_state("domcontentloaded")  # 等待 DOM 加载

    # ========== 等待导航 ==========
    with page.expect_navigation():
        page.click("a[href='/about']")

    # 等待特定 URL
    page.wait_for_url("**/about")

    # ========== 等待网络请求 ==========
    # 等待请求发出
    with page.expect_request("**/api/users") as req:
        page.click("#load-users")
    request = req.value
    print(f"请求 URL: {request.url}")

    # 等待响应返回
    with page.expect_response("**/api/users") as res:
        page.click("#load-users")
    response = res.value
    data = response.json()
    print(f"响应数据: {data}")
```

**验收标准**：
- [ ] 能正确等待元素出现/消失
- [ ] 能正确等待页面加载状态
- [ ] 能正确等待导航完成
- [ ] 能正确等待网络请求
- [ ] 能正确获取响应数据

---

**练习6：断言练习**

**场景说明**：Playwright 提供了强大的 `expect` 断言库，支持自动等待和重试，是编写稳定测试的利器。

**具体需求**：
1. 使用 `to_be_visible()` 验证元素可见
2. 使用 `to_have_text()` 和 `to_contain_text()` 验证文本内容
3. 使用 `to_have_value()` 验证输入框的值
4. 使用 `to_have_count()` 验证元素数量
5. 使用 `to_have_url()` 和 `to_have_title()` 验证页面信息

**使用示例**：
```python
from playwright.sync_api import Page, expect

def test_assertions(page: Page):
    page.goto("https://example.com")

    # ========== 元素可见性断言 ==========
    expect(page.locator("#header")).to_be_visible()
    expect(page.locator("#hidden-element")).to_be_hidden()
    expect(page.locator("#removed")).not_to_be_visible()

    # ========== 文本内容断言 ==========
    expect(page.locator("#title")).to_have_text("欢迎来到首页")
    expect(page.locator("#title")).to_contain_text("欢迎")

    # 使用正则表达式
    import re
    expect(page.locator("#title")).to_have_text(re.compile(r"欢迎.*首页"))

    # ========== 输入框值断言 ==========
    page.fill("#search", "Playwright")
    expect(page.locator("#search")).to_have_value("Playwright")
    expect(page.locator("#empty-input")).to_be_empty()

    # ========== 元素数量断言 ==========
    expect(page.locator(".product-item")).to_have_count(5)

    # ========== 页面断言 ==========
    expect(page).to_have_url("https://example.com/home")
    expect(page).to_have_url(re.compile(r".*/home"))
    expect(page).to_have_title("首页 - 示例网站")

    # ========== 元素状态断言 ==========
    expect(page.locator("#submit-btn")).to_be_enabled()
    expect(page.locator("#disabled-btn")).to_be_disabled()
    expect(page.locator("#agree-checkbox")).to_be_checked()

    # ========== 属性断言 ==========
    expect(page.locator("#link")).to_have_attribute("href", "/about")
    expect(page.locator("#link")).to_have_attribute("target", "_blank")
```

**验收标准**：
- [ ] 能正确使用可见性断言
- [ ] 能正确使用文本断言（精确匹配和包含）
- [ ] 能正确使用值断言
- [ ] 能正确使用数量断言
- [ ] 能正确使用页面 URL 和标题断言
- [ ] 能正确使用元素状态断言

---

**练习7：键盘和鼠标操作**

**场景说明**：某些交互场景需要模拟复杂的键盘和鼠标操作，如快捷键、拖拽等。

**具体需求**：
1. 使用 `keyboard.type()` 模拟键盘逐字输入
2. 使用 `keyboard.press()` 模拟按键（Enter、Escape、Ctrl+A 等）
3. 使用 `mouse.click()` 模拟鼠标点击指定坐标
4. 使用 `mouse.move()` 模拟鼠标移动
5. 使用 `drag_and_drop()` 模拟拖拽操作

**使用示例**：
```python
from playwright.sync_api import Page

def test_keyboard_mouse(page: Page):
    page.goto("https://example.com/interactive")

    # ========== 键盘操作 ==========
    # 聚焦输入框
    page.locator("#editor").click()

    # 逐字输入（模拟打字）
    page.keyboard.type("Hello World", delay=100)  # 每个字符间隔 100ms

    # 按键操作
    page.keyboard.press("Enter")
    page.keyboard.press("Control+A")  # 全选
    page.keyboard.press("Control+C")  # 复制
    page.keyboard.press("Control+V")  # 粘贴
    page.keyboard.press("Escape")

    # 使用 page.press() 在指定元素上按键
    page.press("#input", "Control+A")
    page.press("#input", "Backspace")

    # ========== 鼠标操作 ==========
    # 点击指定坐标
    page.mouse.click(100, 200)

    # 双击
    page.mouse.dblclick(100, 200)

    # 右键点击
    page.mouse.click(100, 200, button="right")

    # 移动鼠标
    page.mouse.move(300, 400)

    # 按住和释放（用于绘制等场景）
    page.mouse.down()
    page.mouse.move(400, 500)
    page.mouse.up()

    # ========== 拖拽操作 ==========
    # 简单拖拽
    page.drag_and_drop("#source", "#target")

    # 手动拖拽（更精细控制）
    source = page.locator("#draggable")
    target = page.locator("#dropzone")

    # 获取元素位置并拖拽
    source_box = source.bounding_box()
    target_box = target.bounding_box()

    page.mouse.move(source_box["x"] + source_box["width"]/2,
                    source_box["y"] + source_box["height"]/2)
    page.mouse.down()
    page.mouse.move(target_box["x"] + target_box["width"]/2,
                    target_box["y"] + target_box["height"]/2)
    page.mouse.up()
```

**验收标准**：
- [ ] 能正确模拟键盘输入
- [ ] 能正确使用快捷键组合
- [ ] 能正确模拟鼠标点击
- [ ] 能正确模拟鼠标移动
- [ ] 能正确执行拖拽操作

---

**练习8：多页面操作**

**场景说明**：测试中经常需要处理多标签页或多窗口场景，如点击链接打开新页面、OAuth 登录等。

**具体需求**：
1. 使用 `context.expect_page()` 监听新页面打开
2. 在新标签页中执行操作
3. 使用 `page.bring_to_front()` 切换回原标签页
4. 使用 `context.pages` 获取所有页面列表
5. 使用 `page.close()` 关闭指定页面

**使用示例**：
```python
from playwright.sync_api import Page, BrowserContext, expect

def test_multiple_pages(page: Page, context: BrowserContext):
    page.goto("https://example.com")

    # ========== 打开新标签页 ==========
    # 方式1：监听新页面
    with context.expect_page() as new_page_info:
        page.click("a[target=_blank]")  # 点击打开新标签的链接
    new_page = new_page_info.value

    # 在新标签页中操作
    new_page.wait_for_load_state()
    expect(new_page).to_have_title("新页面标题")
    new_page.fill("#search", "测试")

    # ========== 切换页面 ==========
    # 切换回原标签页
    page.bring_to_front()
    expect(page).to_have_title("Example Domain")

    # ========== 获取所有页面 ==========
    all_pages = context.pages
    print(f"当前打开 {len(all_pages)} 个页面")
    for p in all_pages:
        print(f"  - {p.title()}")

    # ========== 关闭页面 ==========
    new_page.close()

    # ========== 打开指定 URL 的新页面 ==========
    new_page2 = context.new_page()
    new_page2.goto("https://example.com/about")

    # 验证
    assert len(context.pages) == 2  # 原页面 + 新页面2
```

**验收标准**：
- [ ] 能正确监听和获取新打开的页面
- [ ] 能在新标签页中执行操作
- [ ] 能正确切换页面
- [ ] 能获取所有页面列表
- [ ] 能正确关闭页面

---

### 进阶练习（9-16）

---

**练习9：iframe 操作**

**场景说明**：许多网站使用 iframe 嵌入第三方内容（如支付网关、地图等），测试时需要进入 iframe 进行操作。

**具体需求**：
1. 使用 `frame_locator()` 进入 iframe
2. 在 iframe 中定位和操作元素
3. 处理多层嵌套 iframe
4. 在 iframe 和主页面之间切换

**使用示例**：
```python
from playwright.sync_api import Page, expect

def test_iframe(page: Page):
    page.goto("https://example.com/iframe-demo")

    # ========== 进入 iframe ==========
    # 使用选择器进入 iframe
    frame = page.frame_locator("#myframe")

    # 在 iframe 中定位和操作元素
    frame.get_by_label("用户名").fill("admin")
    frame.get_by_label("密码").fill("password")
    frame.get_by_role("button", name="登录").click()

    # 在 iframe 中使用断言
    expect(frame.locator(".welcome")).to_contain_text("欢迎")

    # ========== 多层嵌套 iframe ==========
    # 进入外层 iframe
    outer_frame = page.frame_locator("#outer-frame")

    # 进入内层 iframe
    inner_frame = outer_frame.frame_locator("#inner-frame")

    # 在内层 iframe 中操作
    inner_frame.get_by_role("button", name="确认").click()

    # ========== 操作完成后回到主页面 ==========
    # 直接使用 page 对象操作主页面
    page.get_by_role("link", name="返回").click()

def test_multiple_iframes(page: Page):
    """处理页面中的多个 iframe"""
    page.goto("https://example.com/multi-iframe")

    # 获取所有 iframe
    frames = page.frames
    print(f"页面共有 {len(frames)} 个 frame（包含主页面）")

    # 操作不同的 iframe
    left_frame = page.frame_locator("#left-panel")
    right_frame = page.frame_locator("#right-panel")

    left_frame.get_by_text("菜单1").click()
    expect(right_frame.locator(".content")).to_contain_text("菜单1内容")
```

**验收标准**：
- [ ] 能正确进入 iframe
- [ ] 能在 iframe 中定位和操作元素
- [ ] 能处理嵌套 iframe
- [ ] 能在 iframe 和主页面之间正确切换

---

**练习10：请求拦截与 Mock**

**场景说明**：在前端测试中，有时需要 Mock API 响应以测试各种边界情况，或者修改请求/响应来验证功能。

**具体需求**：
1. 使用 `page.route()` 拦截请求
2. 使用 `route.fulfill()` Mock API 响应
3. 使用 `route.continue_()` 继续请求
4. 使用 `route.abort()` 中止请求
5. 修改请求头或请求体

**使用示例**：
```python
from playwright.sync_api import Page, expect
import json

def test_request_intercept(page: Page):
    # ========== Mock API 响应 ==========
    # 拦截并返回 Mock 数据
    page.route("**/api/users", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps([
            {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
            {"id": 2, "name": "李四", "email": "lisi@example.com"}
        ])
    ))

    page.goto("https://example.com/users")
    expect(page.locator(".user-item")).to_have_count(2)

def test_modify_request(page: Page):
    """修改请求"""
    def handle_route(route):
        # 获取原始请求
        request = route.request

        # 修改请求头
        headers = request.headers.copy()
        headers["X-Custom-Header"] = "test-value"

        # 继续请求（带修改后的头）
        route.continue_(headers=headers)

    page.route("**/api/*", handle_route)
    page.goto("https://example.com")

def test_abort_request(page: Page):
    """中止特定请求（如阻止广告或追踪脚本）"""
    # 阻止所有图片加载（加速测试）
    page.route("**/*.{png,jpg,jpeg,gif,svg}", lambda route: route.abort())

    # 阻止特定域名请求
    page.route("**/analytics/**", lambda route: route.abort())

    page.goto("https://example.com")

def test_mock_different_responses(page: Page):
    """根据场景 Mock 不同响应"""
    def handle_user_api(route):
        request = route.request
        url = request.url

        if "users/1" in url:
            # 返回单个用户
            route.fulfill(
                status=200,
                body=json.dumps({"id": 1, "name": "张三"})
            )
        elif "users" in url:
            # 返回用户列表
            route.fulfill(
                status=200,
                body=json.dumps([{"id": 1, "name": "张三"}])
            )
        else:
            route.continue_()

    page.route("**/api/**", handle_user_api)
```

**验收标准**：
- [ ] 能正确拦截请求
- [ ] 能 Mock API 响应
- [ ] 能修改请求头
- [ ] 能中止特定请求
- [ ] 能根据不同场景返回不同响应

---

**练习11：对话框处理**

**场景说明**：JavaScript 的 alert、confirm、prompt 对话框需要特殊处理，Playwright 默认会自动关闭它们。

**具体需求**：
1. 使用 `page.on("dialog")` 监听对话框
2. 使用 `dialog.accept()` 接受对话框
3. 使用 `dialog.dismiss()` 取消对话框
4. 使用 `dialog.message()` 获取对话框消息
5. 使用 `dialog.input_value()` 获取 prompt 输入值

**使用示例**：
```python
from playwright.sync_api import Page, expect

def test_alert_dialog(page: Page):
    """处理 alert 对话框"""
    # 监听对话框并自动接受
    page.on("dialog", lambda dialog: dialog.accept())

    # 或者手动处理
    def handle_dialog(dialog):
        print(f"对话框消息: {dialog.message}")
        assert "确定要删除吗" in dialog.message
        dialog.accept()

    page.on("dialog", handle_dialog)

    # 触发对话框
    page.goto("https://example.com")
    page.click("#delete-button")

def test_confirm_dialog(page: Page):
    """处理 confirm 对话框"""
    dialog_message = []

    def handle_confirm(dialog):
        dialog_message.append(dialog.message)
        dialog.accept()  # 点击"确定"
        # dialog.dismiss()  # 点击"取消"

    page.on("dialog", handle_confirm)

    page.goto("https://example.com")
    page.click("#confirm-action")

    assert "确认操作" in dialog_message[0]

def test_prompt_dialog(page: Page):
    """处理 prompt 对话框"""
    def handle_prompt(dialog):
        print(f"对话框消息: {dialog.message}")
        print(f"默认值: {dialog.default_value}")
        # 接受并输入值
        dialog.accept("我的输入")

    page.on("dialog", handle_prompt)

    page.goto("https://example.com")
    page.click("#prompt-button")

def test_dialog_with_expect(page: Page):
    """验证对话框后的页面状态"""
    page.on("dialog", lambda dialog: dialog.accept())

    page.goto("https://example.com")
    page.click("#delete-button")

    # 验证删除后的状态
    expect(page.locator(".success-message")).to_have_text("删除成功")
```

**验收标准**：
- [ ] 能正确监听对话框事件
- [ ] 能接受/取消对话框
- [ ] 能获取对话框消息
- [ ] 能在 prompt 中输入值
- [ ] 能验证对话框操作后的页面状态

---

**练习12：Page Object 模式实现**

**场景说明**：Page Object 模式是 UI 自动化的最佳实践，它将页面元素和操作封装成类，提高代码可维护性和复用性。

**具体需求**：

**LoginPage 类**：
1. 在 `__init__` 中定义所有定位器
2. `navigate()` 方法导航到登录页
3. `login(username, password)` 方法执行登录
4. `expect_error(message)` 方法验证错误消息
5. `expect_login_success()` 方法验证登录成功

**HomePage 类**：
1. 定义首页的定位器
2. `is_logged_in()` 方法检查登录状态
3. `logout()` 方法执行登出

**使用示例**：
```python
# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    """登录页面"""

    def __init__(self, page: Page):
        self.page = page
        # 定义定位器
        self.username_input = page.get_by_label("用户名")
        self.password_input = page.get_by_label("密码")
        self.remember_checkbox = page.get_by_label("记住我")
        self.login_button = page.get_by_role("button", name="登录")
        self.error_message = page.locator(".error-message")
        self.forgot_password_link = page.get_by_text("忘记密码")

    def navigate(self):
        """导航到登录页"""
        self.page.goto("/login")
        return self

    def login(self, username: str, password: str, remember: bool = False):
        """执行登录"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        if remember:
            self.remember_checkbox.check()
        self.login_button.click()
        return self

    def expect_error(self, message: str):
        """验证错误消息"""
        expect(self.error_message).to_have_text(message)
        return self

    def expect_login_success(self):
        """验证登录成功"""
        expect(self.page).to_have_url("**/dashboard")
        return self

    def click_forgot_password(self):
        """点击忘记密码"""
        self.forgot_password_link.click()
        return self


# pages/home_page.py
class HomePage:
    """首页"""

    def __init__(self, page: Page):
        self.page = page
        self.welcome_text = page.locator(".welcome")
        self.user_menu = page.locator(".user-menu")
        self.logout_link = page.get_by_text("退出")

    def navigate(self):
        """导航到首页"""
        self.page.goto("/")
        return self

    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self.user_menu.is_visible()

    def logout(self):
        """执行登出"""
        self.user_menu.click()
        self.logout_link.click()
        return self

    def get_welcome_text(self) -> str:
        """获取欢迎文本"""
        return self.welcome_text.text_content()


# tests/test_login.py
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage

class TestLogin:

    def test_login_success(self, page):
        """测试登录成功"""
        login_page = LoginPage(page)
        home_page = HomePage(page)

        # 导航并登录
        login_page.navigate()
        login_page.login("admin", "password123")

        # 验证登录成功
        login_page.expect_login_success()
        assert home_page.is_logged_in()

    def test_login_wrong_password(self, page):
        """测试密码错误"""
        login_page = LoginPage(page)

        login_page.navigate()
        login_page.login("admin", "wrongpassword")

        login_page.expect_error("用户名或密码错误")

    def test_login_empty_username(self, page):
        """测试用户名为空"""
        login_page = LoginPage(page)

        login_page.navigate()
        login_page.login("", "password123")

        login_page.expect_error("请输入用户名")
```

**验收标准**：
- [ ] LoginPage 类正确封装所有元素和操作
- [ ] HomePage 类正确封装首页功能
- [ ] 测试用例代码清晰简洁
- [ ] 支持链式调用
- [ ] 断言方法使用 expect

---

**练习13：数据驱动测试**

**场景说明**：使用 pytest 的参数化功能实现数据驱动测试，减少重复代码，提高测试覆盖率。

**具体需求**：
1. 使用 `@pytest.mark.parametrize` 实现参数化
2. 使用 CSV/JSON 文件作为测试数据源
3. 实现登录场景的数据驱动测试
4. 实现搜索场景的数据驱动测试
5. 生成带参数的测试报告

**使用示例**：
```python
import pytest
import json
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

# ========== 简单参数化 ==========
@pytest.mark.parametrize("username,password,expected_result", [
    ("admin", "123456", "success"),
    ("admin", "wrongpassword", "密码错误"),
    ("", "123456", "请输入用户名"),
    ("admin", "", "请输入密码"),
    ("unknown", "123456", "用户不存在"),
])
def test_login_data_driven(page: Page, username, password, expected_result):
    """数据驱动登录测试"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)

    if expected_result == "success":
        login_page.expect_login_success()
    else:
        login_page.expect_error(expected_result)


# ========== 使用 JSON 数据文件 ==========
# test_data/login_data.json
"""
[
    {"username": "admin", "password": "123456", "expected": "success"},
    {"username": "admin", "password": "wrong", "expected": "密码错误"}
]
"""

def load_login_data():
    """从 JSON 文件加载测试数据"""
    with open("test_data/login_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("data", load_login_data())
def test_login_from_json(page: Page, data):
    """从 JSON 文件读取测试数据"""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(data["username"], data["password"])

    if data["expected"] == "success":
        login_page.expect_login_success()
    else:
        login_page.expect_error(data["expected"])


# ========== 搜索功能数据驱动测试 ==========
@pytest.mark.parametrize("keyword,expected_count", [
    ("手机", 10),
    ("电脑", 5),
    ("不存在的商品", 0),
    ("", 20),  # 空搜索显示全部
])
def test_search_products(page: Page, keyword, expected_count):
    """数据驱动搜索测试"""
    page.goto("https://example.com/search")

    # 执行搜索
    search_input = page.get_by_placeholder("搜索商品")
    search_input.fill(keyword)
    page.keyboard.press("Enter")

    # 等待结果加载
    page.wait_for_selector(".product-list")

    # 验证结果数量
    if expected_count == 0:
        expect(page.locator(".no-results")).to_be_visible()
    else:
        expect(page.locator(".product-item")).to_have_count(expected_count)


# ========== 多参数组合测试 ==========
@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
@pytest.mark.parametrize("viewport", [
    {"width": 1920, "height": 1080},  # 桌面
    {"width": 375, "height": 667},    # 移动端
])
def test_responsive_design(browser_type, viewport):
    """测试响应式设计（需要配置 conftest.py）"""
    pass
```

**验收标准**：
- [ ] 能正确使用 parametrize 装饰器
- [ ] 能从外部文件读取测试数据
- [ ] 测试用例能正确处理不同参数
- [ ] 测试报告显示参数信息
- [ ] 代码无重复

---

**练习14：截图和视频录制**

**场景说明**：测试失败时，截图和视频是调试的重要工具，Playwright 提供了完善的截图和录制功能。

**具体需求**：
1. 使用 `page.screenshot()` 手动截图
2. 配置失败时自动截图
3. 配置测试视频录制
4. 使用 `page.trace` 记录测试追踪
5. 截取特定元素

**使用示例**：
```python
from playwright.sync_api import Page, expect
import os

def test_screenshot_manual(page: Page):
    """手动截图"""
    page.goto("https://example.com")

    # 创建截图目录
    os.makedirs("screenshots", exist_ok=True)

    # 全页面截图
    page.screenshot(path="screenshots/homepage.png")

    # 全页面截图（完整滚动）
    page.screenshot(path="screenshots/fullpage.png", full_page=True)

    # 特定元素截图
    page.locator("#header").screenshot(path="screenshots/header.png")

    # 截图并返回字节流
    screenshot_bytes = page.screenshot()
    assert len(screenshot_bytes) > 0


# conftest.py 配置
import pytest
from playwright.sync_api import Browser

@pytest.fixture(scope="function")
def page_with_recording(browser: Browser):
    """配置视频录制的 page fixture"""
    context = browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720}
    )
    page = context.new_page()
    yield page
    # 保存视频
    video_path = page.video.path()
    print(f"视频保存到: {video_path}")
    context.close()


# pytest.ini 配置
"""
[pytest]
addopts =
    --headed
    --video=retain-on-failure
    --screenshot=only-on-failure
    --trace=retain-on-failure
"""

def test_with_trace(page: Page):
    """使用 trace 记录"""
    # 开始追踪
    context = page.context
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page.goto("https://example.com")
    page.click("#button")

    # 停止追踪并保存
    context.tracing.stop(path="traces/trace.zip")

    # 查看追踪：npx playwright show-trace traces/trace.zip


def test_failure_screenshot(page: Page):
    """失败时自动截图（通过 pytest hook）"""
    page.goto("https://example.com")

    # 这个断言失败时会自动截图
    expect(page.locator("#non-existent")).to_be_visible()
```

**conftest.py 失败截图 Hook**：
```python
# conftest.py
import pytest
from playwright.sync_api import Page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 获取 page fixture
        if "page" in item.funcargs:
            page: Page = item.funcargs["page"]
            # 保存截图
            screenshot_path = f"screenshots/{item.name}_failure.png"
            page.screenshot(path=screenshot_path)
            print(f"\n失败截图已保存: {screenshot_path}")
```

**验收标准**：
- [ ] 能手动截取全页面和元素截图
- [ ] 能配置失败自动截图
- [ ] 能配置视频录制
- [ ] 能使用 trace 功能
- [ ] 能通过 pytest hook 实现失败截图

---

**练习15：并行执行配置**

**场景说明**：测试用例数量增多后，串行执行会耗费大量时间，配置并行执行可以显著提升效率。

**具体需求**：
1. 安装 `pytest-xdist` 插件
2. 配置 `pytest.ini` 支持并行
3. 使用 `-n` 参数指定进程数
4. 处理测试数据隔离问题
5. 配置测试分组

**使用示例**：
```bash
# 安装并行执行插件
pip install pytest-xdist

# 并行执行命令
pytest -n 4 tests/                    # 4 个进程并行
pytest -n auto tests/                 # 自动检测 CPU 核心数
pytest -n 4 --dist loadfile tests/    # 按文件分配（同一文件在同一个进程）
pytest -n 4 --dist loadscope tests/   # 按类/模块分配
```

```python
# tests/test_parallel_1.py
import pytest
from playwright.sync_api import Page, expect

class TestParallel1:
    """并行测试组 1"""

    def test_case_1(self, page: Page):
        page.goto("https://example.com/page1")
        expect(page).to_have_title("Page 1")

    def test_case_2(self, page: Page):
        page.goto("https://example.com/page2")
        expect(page).to_have_title("Page 2")


# tests/test_parallel_2.py
class TestParallel2:
    """并行测试组 2"""

    def test_case_3(self, page: Page):
        page.goto("https://example.com/page3")
        expect(page).to_have_title("Page 3")
```

```ini
# pytest.ini
[pytest]
addopts =
    --headed
    --browser chromium
    -n 4
    --dist loadfile
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

```python
# conftest.py - 处理数据隔离
import pytest
from playwright.sync_api import Browser

@pytest.fixture(scope="function")
def isolated_page(browser: Browser):
    """每个测试使用独立的上下文，确保数据隔离"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def authenticated_page(browser: Browser):
    """预登录的页面（每个进程独立登录）"""
    context = browser.new_context()
    page = context.new_page()

    # 登录操作
    page.goto("https://example.com/login")
    page.fill("#username", "testuser")
    page.fill("#password", "password")
    page.click("button[type=submit]")
    page.wait_for_url("**/dashboard")

    yield page
    context.close()
```

**验收标准**：
- [ ] 能配置并行执行
- [ ] 能指定并行进程数
- [ ] 测试数据隔离正确
- [ ] 测试报告正确显示
- [ ] 执行时间显著减少

---

**练习16：设备模拟**

**场景说明**：测试响应式网站或移动端应用时，需要模拟不同的设备和环境。

**具体需求**：
1. 使用 Playwright 内置设备配置模拟 iPhone、Android 等
2. 模拟不同的视口大小
3. 模拟地理位置
4. 模拟离线状态
5. 模拟不同的语言和时区

**使用示例**：
```python
from playwright.sync_api import BrowserContext, Page, Playwright
import pytest

def test_mobile_simulation(browser):
    """模拟 iPhone 13"""
    # 使用内置设备配置
    iphone_13 = playwright.devices["iPhone 13"]

    context = browser.new_context(
        **iphone_13,
        locale="zh-CN",
        timezone_id="Asia/Shanghai"
    )
    page = context.new_page()

    page.goto("https://example.com")

    # 验证移动端布局
    expect(page.locator(".mobile-menu")).to_be_visible()

    context.close()


def test_custom_viewport(browser):
    """自定义视口大小"""
    context = browser.new_context(
        viewport={"width": 375, "height": 667},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True
    )
    page = context.new_page()
    page.goto("https://example.com")
    context.close()


def test_geolocation(browser):
    """模拟地理位置"""
    context = browser.new_context(
        geolocation={"latitude": 31.2304, "longitude": 121.4737},  # 上海
        permissions=["geolocation"]
    )
    page = context.new_page()

    page.goto("https://example.com/map")
    page.click("#get-location")

    # 验证位置显示
    expect(page.locator(".location")).to_contain_text("上海")

    # 更新位置
    context.set_geolocation({"latitude": 39.9042, "longitude": 116.4074})  # 北京

    context.close()


def test_offline_mode(browser):
    """模拟离线状态"""
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://example.com")

    # 设置离线
    context.set_offline(True)

    # 尝试访问网络资源
    with page.expect_response("**/api/data") as response:
        page.click("#refresh")
    assert response.value().status == 0 or response.value().ok == False

    # 恢复在线
    context.set_offline(False)

    context.close()


# 使用 pytest 参数化测试多个设备
@pytest.mark.parametrize("device_name", ["iPhone 13", "Pixel 5", "iPad Pro"])
def test_responsive_design(browser, device_name):
    """测试多个设备的响应式设计"""
    device = playwright.devices[device_name]
    context = browser.new_context(**device)
    page = context.new_page()

    page.goto("https://example.com")

    # 验证页面适配
    expect(page.locator("body")).to_be_visible()

    # 截图保存
    page.screenshot(path=f"screenshots/{device_name.replace(' ', '_')}.png")

    context.close()
```

**验收标准**：
- [ ] 能正确模拟移动设备
- [ ] 能自定义视口大小
- [ ] 能模拟地理位置
- [ ] 能模拟离线状态
- [ ] 能测试响应式布局

---

### 综合练习（17-20）

---

**练习17：完整的电商购物流程测试**

**场景说明**：作为测试工程师，你需要为电商网站编写端到端的购物流程测试。这是一个典型的业务流程测试，涉及多个页面的协作，需要使用 Page Object 模式来组织代码，确保测试的可维护性和可复用性。

**具体需求**：
1. 使用 Page Object 模式设计页面类，包含：LoginPage、HomePage、SearchPage、ProductPage、CartPage、CheckoutPage、OrderPage
2. 实现用户登录功能，验证登录成功后跳转到首页
3. 实现商品搜索功能，支持关键词搜索和筛选
4. 实现添加商品到购物车，验证购物车数量更新
5. 实现修改购物车商品数量，验证总价重新计算
6. 实现结算下单流程，填写收货地址和支付方式
7. 验证订单创建成功，订单状态正确

**使用示例**：
```python
# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    """登录页面"""

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("请输入用户名")
        self.password_input = page.get_by_placeholder("请输入密码")
        self.login_button = page.get_by_role("button", name="登录")
        self.error_message = page.locator(".error-message")

    def navigate(self):
        """导航到登录页"""
        self.page.goto("/login")
        return self

    def login(self, username: str, password: str):
        """执行登录"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def expect_login_success(self):
        """验证登录成功"""
        expect(self.page).to_have_url("**/home")


# pages/search_page.py
class SearchPage:
    """搜索页面"""

    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.get_by_placeholder("搜索商品")
        self.search_button = page.get_by_role("button", name="搜索")
        self.product_list = page.locator(".product-item")

    def search(self, keyword: str):
        """搜索商品"""
        self.search_input.fill(keyword)
        self.search_button.click()
        return self

    def get_product_by_name(self, name: str):
        """根据名称获取商品"""
        return self.product_list.filter(has_text=name)

    def add_to_cart(self, product_name: str):
        """添加商品到购物车"""
        product = self.get_product_by_name(product_name)
        product.get_by_role("button", name="加入购物车").click()
        return self


# pages/cart_page.py
class CartPage:
    """购物车页面"""

    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart-item")
        self.total_price = page.locator(".total-price")
        self.checkout_button = page.get_by_role("button", name="去结算")

    def navigate(self):
        """导航到购物车"""
        self.page.goto("/cart")
        return self

    def get_item_count(self) -> int:
        """获取购物车商品数量"""
        return self.cart_items.count()

    def update_quantity(self, product_name: str, quantity: int):
        """修改商品数量"""
        item = self.cart_items.filter(has_text=product_name)
        item.locator(".quantity-input").fill(str(quantity))
        return self

    def remove_item(self, product_name: str):
        """删除商品"""
        item = self.cart_items.filter(has_text=product_name)
        item.get_by_role("button", name="删除").click()
        return self

    def proceed_to_checkout(self):
        """去结算"""
        self.checkout_button.click()
        return self


# pages/checkout_page.py
class CheckoutPage:
    """结算页面"""

    def __init__(self, page: Page):
        self.page = page
        self.address_input = page.get_by_label("收货地址")
        self.phone_input = page.get_by_label("联系电话")
        self.submit_button = page.get_by_role("button", name="提交订单")

    def fill_address(self, address: str):
        """填写收货地址"""
        self.address_input.fill(address)
        return self

    def fill_phone(self, phone: str):
        """填写联系电话"""
        self.phone_input.fill(phone)
        return self

    def submit_order(self):
        """提交订单"""
        self.submit_button.click()
        return self


# pages/order_page.py
class OrderPage:
    """订单页面"""

    def __init__(self, page: Page):
        self.page = page
        self.order_status = page.locator(".order-status")
        self.order_number = page.locator(".order-number")

    def expect_order_success(self):
        """验证订单创建成功"""
        expect(self.order_status).to_have_text("待支付")
        expect(self.order_number).to_be_visible()


# tests/test_shopping_flow.py
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.order_page import OrderPage


class TestShopping:
    """电商购物流程测试"""

    def test_complete_shopping_flow(self, page: Page):
        """测试完整购物流程"""
        # 1. 用户登录
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("testuser", "password123")
        login_page.expect_login_success()

        # 2. 搜索商品
        search_page = SearchPage(page)
        search_page.search("iPhone 15")
        expect(search_page.product_list.first).to_be_visible()

        # 3. 添加到购物车
        search_page.add_to_cart("iPhone 15 Pro")
        expect(page.locator(".cart-badge")).to_have_text("1")

        # 4. 修改购物车数量
        cart_page = CartPage(page)
        cart_page.navigate()
        cart_page.update_quantity("iPhone 15 Pro", 2)
        expect(cart_page.total_price).to_contain_text("19998")

        # 5. 结算下单
        cart_page.proceed_to_checkout()
        checkout_page = CheckoutPage(page)
        checkout_page.fill_address("北京市朝阳区xxx街道")
        checkout_page.fill_phone("13800138000")
        checkout_page.submit_order()

        # 6. 验证订单状态
        order_page = OrderPage(page)
        order_page.expect_order_success()
```

**验收标准**：
- [ ] 所有 Page Object 类实现完整，包含必要的定位器和方法
- [ ] 登录流程测试通过，能正确验证登录状态
- [ ] 搜索功能测试通过，能正确显示搜索结果
- [ ] 购物车操作测试通过，数量和价格计算正确
- [ ] 结算流程测试通过，订单创建成功
- [ ] 代码结构清晰，遵循 Page Object 设计模式

---

**练习18：API 与 UI 混合测试**

**场景说明**：在真实项目中，纯 UI 测试往往效率较低且不稳定。通过 API 创建测试数据、UI 验证显示、API 验证数据变化的方式，可以大幅提升测试效率和稳定性。这种混合测试策略是现代自动化测试的最佳实践。

**具体需求**：
1. 使用 Playwright 的 APIRequestContext 通过 API 创建测试数据（用户、商品等）
2. UI 层验证数据是否正确显示在页面上
3. 在 UI 层执行操作（如删除、编辑）
4. 再次通过 API 验证数据变化是否正确持久化
5. 使用 fixtures 管理 API 请求上下文和测试数据
6. 实现测试数据的自动清理

**使用示例**：
```python
# conftest.py
import pytest
from playwright.sync_api import APIRequestContext

@pytest.fixture(scope="session")
def api_request_context(playwright):
    """API 请求上下文"""
    request_context = playwright.request.new_context(
        base_url="https://api.example.com"
    )
    yield request_context
    request_context.dispose()


@pytest.fixture
def test_user(api_request_context: APIRequestContext):
    """创建测试用户"""
    # 通过 API 创建用户
    response = api_request_context.post("/api/users", data={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    user_data = response.json()
    yield user_data

    # 清理：删除测试用户
    api_request_context.delete(f"/api/users/{user_data['id']}")


# tests/test_api_ui_hybrid.py
import pytest
from playwright.sync_api import Page, APIRequestContext, expect


class TestAPIUIHybrid:
    """API 与 UI 混合测试"""

    def test_create_user_via_api_verify_via_ui(
        self,
        page: Page,
        api_request_context: APIRequestContext,
        test_user
    ):
        """通过 API 创建用户，UI 验证显示"""
        # 1. 通过 API 创建用户（已通过 fixture 完成）

        # 2. UI 验证用户显示
        page.goto("/admin/users")
        user_row = page.locator(f".user-row:has-text('{test_user['username']}')")
        expect(user_row).to_be_visible()
        expect(user_row).to_contain_text(test_user["email"])

    def test_delete_user_via_ui_verify_via_api(
        self,
        page: Page,
        api_request_context: APIRequestContext,
        test_user
    ):
        """UI 删除用户，API 验证数据变化"""
        # 1. UI 层删除用户
        page.goto("/admin/users")
        user_row = page.locator(f".user-row:has-text('{test_user['username']}')")
        user_row.get_by_role("button", name="删除").click()

        # 确认删除
        page.get_by_role("button", name="确认").click()

        # 2. 验证 UI 上用户已消失
        expect(page.locator(f".user-row:has-text('{test_user['username']}'))")).not_to_be_visible()

        # 3. API 验证用户已被删除
        response = api_request_context.get(f"/api/users/{test_user['id']}")
        assert response.status == 404, "用户应该已被删除"

    def test_update_product_via_ui_verify_via_api(
        self,
        page: Page,
        api_request_context: APIRequestContext
    ):
        """UI 更新商品，API 验证数据变化"""
        # 1. 通过 API 创建商品
        create_response = api_request_context.post("/api/products", data={
            "name": "测试商品",
            "price": 100,
            "stock": 50
        })
        product = create_response.json()

        try:
            # 2. UI 层修改商品
            page.goto(f"/admin/products/{product['id']}/edit")
            page.get_by_label("商品名称").fill("更新后的商品名称")
            page.get_by_label("价格").fill("150")
            page.get_by_role("button", name="保存").click()

            # 3. 验证 UI 提示成功
            expect(page.locator(".success-message")).to_contain_text("保存成功")

            # 4. API 验证数据已更新
            get_response = api_request_context.get(f"/api/products/{product['id']}")
            updated_product = get_response.json()
            assert updated_product["name"] == "更新后的商品名称"
            assert updated_product["price"] == 150
        finally:
            # 清理：删除测试商品
            api_request_context.delete(f"/api/products/{product['id']}")

    def test_batch_create_and_verify(
        self,
        page: Page,
        api_request_context: APIRequestContext
    ):
        """批量创建数据并验证"""
        # 1. 通过 API 批量创建用户
        users = []
        for i in range(5):
            response = api_request_context.post("/api/users", data={
                "username": f"batch_user_{i}",
                "email": f"batch_{i}@example.com"
            })
            users.append(response.json())

        try:
            # 2. UI 验证所有用户显示
            page.goto("/admin/users")
            for user in users:
                expect(page.locator(f"text={user['username']}")).to_be_visible()

            # 3. 验证用户数量
            expect(page.locator(".user-row")).to_have_count(5)
        finally:
            # 清理
            for user in users:
                api_request_context.delete(f"/api/users/{user['id']}")
```

**验收标准**：
- [ ] 能使用 APIRequestContext 发送 API 请求
- [ ] 能通过 API 创建测试数据
- [ ] UI 层能正确验证 API 创建的数据
- [ ] API 层能正确验证 UI 操作后的数据变化
- [ ] 测试数据能自动清理
- [ ] 测试用例独立，不互相依赖

---

**练习19：性能测试集成**

**场景说明**：性能是用户体验的关键指标。在 UI 自动化测试中集成性能监控，可以在功能测试的同时收集性能数据，及时发现性能退化。Playwright 提供了丰富的 API 来获取页面性能指标。

**具体需求**：
1. 使用 `page.evaluate()` 获取 Navigation Timing API 的性能数据
2. 使用 `page.metrics()` 获取页面运行时指标
3. 监控关键性能指标：FCP（首次内容绘制）、LCP（最大内容绘制）、CLS（累积布局偏移）
4. 监控网络请求数量和大小
5. 设置性能阈值并断言
6. 生成性能报告，包含趋势分析

**使用示例**：
```python
# tests/test_performance.py
import pytest
import json
from playwright.sync_api import Page, expect
from typing import Dict, Any


class PerformanceMonitor:
    """性能监控工具类"""

    def __init__(self, page: Page):
        self.page = page
        self.metrics = {}

    def collect_navigation_timing(self) -> Dict[str, Any]:
        """收集导航计时数据"""
        return self.page.evaluate("""() => {
            const timing = window.performance.timing;
            return {
                dns: timing.domainLookupEnd - timing.domainLookupStart,
                tcp: timing.connectEnd - timing.connectStart,
                request: timing.responseStart - timing.requestStart,
                response: timing.responseEnd - timing.responseStart,
                domProcessing: timing.domComplete - timing.domLoading,
                loadComplete: timing.loadEventEnd - timing.navigationStart,
                domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart
            };
        }""")

    def collect_paint_timing(self) -> Dict[str, Any]:
        """收集绘制计时数据"""
        return self.page.evaluate("""() => {
            const entries = window.performance.getEntriesByType('paint');
            const result = {};
            entries.forEach(entry => {
                result[entry.name] = entry.startTime;
            });
            return result;
        }""")

    def collect_web_vitals(self) -> Dict[str, Any]:
        """收集 Web Vitals 指标"""
        return self.page.evaluate("""() => {
            return new Promise((resolve) => {
                const vitals = {};

                // LCP - 最大内容绘制
                const lcpEntries = window.performance.getEntriesByType('largest-contentful-paint');
                if (lcpEntries.length > 0) {
                    vitals.lcp = lcpEntries[lcpEntries.length - 1].startTime;
                }

                // FCP - 首次内容绘制
                const fcpEntries = window.performance.getEntriesByName('first-contentful-paint');
                if (fcpEntries.length > 0) {
                    vitals.fcp = fcpEntries[0].startTime;
                }

                // CLS - 累积布局偏移
                let clsValue = 0;
                const clsEntries = window.performance.getEntriesByType('layout-shift');
                clsEntries.forEach(entry => {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                });
                vitals.cls = clsValue;

                resolve(vitals);
            });
        }""")

    def collect_resource_timing(self) -> list:
        """收集资源加载计时"""
        return self.page.evaluate("""() => {
            const resources = window.performance.getEntriesByType('resource');
            return resources.map(r => ({
                name: r.name,
                duration: r.duration,
                size: r.transferSize,
                type: r.initiatorType
            }));
        }""")

    def collect_runtime_metrics(self) -> Dict[str, Any]:
        """收集运行时指标"""
        return self.page.metrics()

    def generate_report(self) -> Dict[str, Any]:
        """生成性能报告"""
        return {
            "navigation": self.collect_navigation_timing(),
            "paint": self.collect_paint_timing(),
            "web_vitals": self.collect_web_vitals(),
            "resources": self.collect_resource_timing(),
            "runtime": self.collect_runtime_metrics()
        }


class TestPerformance:
    """性能测试"""

    def test_page_load_performance(self, page: Page):
        """测试页面加载性能"""
        monitor = PerformanceMonitor(page)

        # 访问页面并等待加载完成
        page.goto("https://example.com", wait_until="networkidle")

        # 收集导航计时
        nav_timing = monitor.collect_navigation_timing()

        # 验证加载时间
        assert nav_timing["loadComplete"] < 3000, \
            f"页面加载时间过长: {nav_timing['loadComplete']}ms"
        assert nav_timing["domContentLoaded"] < 2000, \
            f"DOM 内容加载时间过长: {nav_timing['domContentLoaded']}ms"

    def test_web_vitals(self, page: Page):
        """测试 Web Vitals 指标"""
        monitor = PerformanceMonitor(page)

        page.goto("https://example.com", wait_until="networkidle")

        # 收集 Web Vitals
        vitals = monitor.collect_web_vitals()

        # 验证关键指标
        # FCP 应小于 1.8s（良好）
        if "first-contentful-paint" in vitals:
            assert vitals["first-contentful-paint"] < 1800, \
                f"FCP 过高: {vitals['first-contentful-paint']}ms"

        # LCP 应小于 2.5s（良好）
        if "lcp" in vitals:
            assert vitals["lcp"] < 2500, \
                f"LCP 过高: {vitals['lcp']}ms"

        # CLS 应小于 0.1（良好）
        if "cls" in vitals:
            assert vitals["cls"] < 0.1, \
                f"CLS 过高: {vitals['cls']}"

    def test_resource_size(self, page: Page):
        """测试资源大小"""
        monitor = PerformanceMonitor(page)

        page.goto("https://example.com", wait_until="networkidle")

        # 收集资源加载信息
        resources = monitor.collect_resource_timing()

        # 统计总大小
        total_size = sum(r["size"] for r in resources)
        total_size_mb = total_size / (1024 * 1024)

        # 验证总大小不超过 5MB
        assert total_size_mb < 5, f"资源总大小过大: {total_size_mb:.2f}MB"

        # 验证单个资源大小
        for resource in resources:
            size_kb = resource["size"] / 1024
            assert size_kb < 500, \
                f"资源 {resource['name']} 过大: {size_kb:.2f}KB"

    def test_network_requests(self, page: Page):
        """测试网络请求数量"""
        requests = []

        # 监听请求
        page.on("request", lambda req: requests.append(req))

        page.goto("https://example.com", wait_until="networkidle")

        # 统计请求
        total_requests = len(requests)
        api_requests = [r for r in requests if "/api/" in r.url]
        js_requests = [r for r in requests if r.resource_type == "script"]
        css_requests = [r for r in requests if r.resource_type == "stylesheet"]

        # 验证请求数量
        assert total_requests < 50, f"请求数量过多: {total_requests}"
        assert len(api_requests) < 10, f"API 请求数量过多: {len(api_requests)}"

        print(f"总请求数: {total_requests}")
        print(f"API 请求: {len(api_requests)}")
        print(f"JS 文件: {len(js_requests)}")
        print(f"CSS 文件: {len(css_requests)}")

    def test_performance_report(self, page: Page):
        """生成完整性能报告"""
        monitor = PerformanceMonitor(page)

        page.goto("https://example.com", wait_until="networkidle")

        # 生成报告
        report = monitor.generate_report()

        # 输出报告
        print("\n========== 性能报告 ==========")
        print(f"DNS 查询时间: {report['navigation']['dns']}ms")
        print(f"TCP 连接时间: {report['navigation']['tcp']}ms")
        print(f"请求时间: {report['navigation']['request']}ms")
        print(f"响应时间: {report['navigation']['response']}ms")
        print(f"DOM 处理时间: {report['navigation']['domProcessing']}ms")
        print(f"完全加载时间: {report['navigation']['loadComplete']}ms")
        print(f"资源数量: {len(report['resources'])}")
        print("==============================\n")

        # 保存报告到文件
        with open("performance_report.json", "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
```

**验收标准**：
- [ ] 能正确收集 Navigation Timing 数据
- [ ] 能正确收集 Web Vitals 指标（FCP、LCP、CLS）
- [ ] 能监控网络请求数量和大小
- [ ] 能设置性能阈值并进行断言
- [ ] 能生成性能报告
- [ ] 性能指标在合理范围内

---

**练习20：CI/CD 集成配置**

**场景说明**：将 UI 自动化测试集成到 CI/CD 流水线是实现持续测试的关键。需要配置 GitHub Actions 自动运行测试、生成报告、发送通知，并归档测试结果，确保每次代码提交都能自动验证质量。

**具体需求**：
1. 编写完整的 GitHub Actions 配置文件，支持多浏览器并行测试
2. 配置测试报告生成（HTML 报告、Allure 报告）
3. 配置失败通知（邮件、Slack、钉钉）
4. 配置测试结果归档（截图、视频、日志）
5. 配置缓存策略加速测试执行
6. 配置定时执行和手动触发

**使用示例**：

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # 每天 UTC 时间 0:00 执行（北京时间 8:00）
    - cron: '0 0 * * *'
  workflow_dispatch:
    # 支持手动触发
    inputs:
      browser:
        description: 'Browser to test'
        required: true
        default: 'chromium'
        type: choice
        options:
          - chromium
          - firefox
          - webkit
          - all

env:
  # 环境变量
  TEST_URL: ${{ secrets.TEST_URL }}
  TEST_USER: ${{ secrets.TEST_USER }}
  TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox, webkit]
        shard: [1/4, 2/4, 3/4, 4/4]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest-playwright allure-pytest

      - name: Install Playwright browsers
        run: playwright install --with-deps ${{ matrix.browser }}
        env:
          PLAYWRIGHT_BROWSERS_PATH: ${{ github.workspace }}/browsers

      - name: Cache Playwright browsers
        uses: actions/cache@v4
        with:
          path: ${{ github.workspace }}/browsers
          key: ${{ runner.os }}-playwright-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-playwright-

      - name: Run Playwright tests
        run: |
          pytest tests/ \
            --browser ${{ matrix.browser }} \
            --shard=${{ matrix.shard }} \
            --headed \
            --video=retain-on-failure \
            --screenshot=only-on-failure \
            --trace=retain-on-failure \
            --alluredir=allure-results \
            --html=report.html \
            --self-contained-html \
            -v
        env:
          CI: true

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.browser }}-${{ matrix.shard }}
          path: |
            report.html
            allure-results/
            test-results/
          retention-days: 30

      - name: Upload screenshots and videos
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: failure-artifacts-${{ matrix.browser }}-${{ matrix.shard }}
          path: |
            test-results/
            videos/
            screenshots/
          retention-days: 30

  merge-reports:
    needs: test
    runs-on: ubuntu-latest
    if: always()

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: all-results

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Allure
        run: |
          sudo apt-add-repository ppa:qameta/allure
          sudo apt-get update
          sudo apt-get install allure

      - name: Generate Allure report
        run: |
          allure generate all-results/*/allure-results -o allure-report --clean

      - name: Upload Allure report
        uses: actions/upload-artifact@v4
        with:
          name: allure-report
          path: allure-report/
          retention-days: 30

      - name: Deploy report to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./allure-report

  notify:
    needs: [test, merge-reports]
    runs-on: ubuntu-latest
    if: always()

    steps:
      - name: Send Slack notification on success
        if: success()
        uses: 8398a7/action-slack@v3
        with:
          status: success
          text: |
            Playwright 测试通过
            分支: ${{ github.ref_name }}
            提交: ${{ github.sha }}
            报告: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

      - name: Send Slack notification on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          text: |
            Playwright 测试失败
            分支: ${{ github.ref_name }}
            提交: ${{ github.sha }}
            请检查: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

      - name: Send email notification
        if: failure()
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: Playwright 测试失败 - ${{ github.repository }}
          to: qa-team@example.com
          from: CI/CD Bot
          body: |
            Playwright 测试失败
            仓库: ${{ github.repository }}
            分支: ${{ github.ref_name }}
            提交: ${{ github.sha }}
            详情: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

```python
# pytest.ini - 完整配置
"""
[pytest]
# 测试路径
testpaths = tests

# 默认参数
addopts =
    -v
    --tb=short
    --headed
    --browser chromium
    --slowmo=100
    --video=retain-on-failure
    --screenshot=only-on-failure
    --trace=retain-on-failure
    --output=test-results
    --html=report.html
    --self-contained-html

# 标记
markers =
    smoke: 冒烟测试
    regression: 回归测试
    slow: 慢速测试
    skip_ci: 跳过 CI 测试

# 环境变量
env =
    CI=true
    TEST_ENV=staging

# 日志配置
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# 最小版本
minversion = 7.0
"""

# conftest.py - 测试配置
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
import os


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """浏览器启动参数"""
    return {
        **browser_type_launch_args,
        "headless": os.getenv("CI", "false") == "true",
        "args": ["--disable-gpu", "--no-sandbox"]
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """浏览器上下文参数"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "videos/",
        "record_har_path": "har/",
    }


@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    """每个测试创建新的页面"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(autouse=True)
def setup_test_environment(page: Page):
    """自动设置测试环境"""
    # 设置默认超时
    page.set_default_timeout(10000)
    yield
    # 测试结束后的清理


def pytest_configure(config):
    """pytest 配置"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )


def pytest_collection_modifyitems(config, items):
    """根据标记修改测试项"""
    if config.getoption("-m", default=None) is None:
        # 默认跳过标记为 skip_ci 的测试
        skip_ci = pytest.mark.skip(reason="跳过 CI 测试")
        for item in items:
            if "skip_ci" in item.keywords:
                item.add_marker(skip_ci)
```

```bash
# requirements.txt
pytest>=7.0.0
pytest-playwright>=0.4.0
pytest-html>=3.2.0
allure-pytest>=2.13.0
pytest-xdist>=3.0.0
python-dotenv>=1.0.0
```

```bash
# 运行命令示例
# 本地运行所有测试
pytest tests/

# 运行冒烟测试
pytest tests/ -m smoke

# 并行运行（4个进程）
pytest tests/ -n 4

# 运行特定浏览器
pytest tests/ --browser firefox

# 分片运行（CI 中使用）
pytest tests/ --shard=1/4

# 生成 Allure 报告
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

**验收标准**：
- [ ] GitHub Actions 配置文件完整，能成功运行
- [ ] 支持多浏览器并行测试
- [ ] 测试失败时能正确归档截图和视频
- [ ] 能生成 HTML 和 Allure 测试报告
- [ ] 配置了失败通知（Slack 或邮件）
- [ ] 配置了浏览器缓存加速执行
- [ ] pytest.ini 配置完整合理

---

## 五、检验标准

### 自测题

---

#### 题目1：登录功能测试（综合考察：定位器、表单操作、断言）

**场景**：为某电商网站编写登录功能的自动化测试。

**需求**：
1. 创建 `LoginPage` Page Object 类
2. 实现登录成功和失败场景的测试
3. 使用数据驱动测试多种登录场景
4. 验证错误提示信息

**测试用例**：
```python
import pytest
from playwright.sync_api import Page, expect

class LoginPage:
    """登录页面 Page Object - 请实现"""

    def __init__(self, page: Page):
        self.page = page
        # TODO: 定义定位器

    def navigate(self):
        # TODO: 导航到登录页
        pass

    def login(self, username: str, password: str):
        # TODO: 执行登录
        pass


class TestLogin:
    def test_login_success(self, page: Page):
        """测试登录成功"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("testuser", "password123")
        expect(page).to_have_url("**/dashboard")

    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "password123", "请输入用户名"),
        ("testuser", "", "请输入密码"),
        ("testuser", "wrong", "用户名或密码错误"),
    ])
    def test_login_failures(self, page: Page, username, password, expected_error):
        """测试登录失败场景"""
        # TODO: 实现测试
        pass
```

---

#### 题目2：购物车功能测试（综合考察：Page Object、元素操作、断言）

**场景**：为购物车功能编写完整的测试用例。

**需求**：
1. 创建 `CartPage` Page Object 类
2. 实现添加商品、修改数量、删除商品功能
3. 验证购物车总价计算

**测试用例**：
```python
class CartPage:
    """购物车页面 Page Object - 请实现"""

    def __init__(self, page: Page):
        self.page = page
        # TODO: 定义定位器

    def add_item(self, product_name: str, quantity: int = 1):
        # TODO: 添加商品
        pass

    def update_quantity(self, product_name: str, quantity: int):
        # TODO: 修改数量
        pass

    def remove_item(self, product_name: str):
        # TODO: 删除商品
        pass


class TestCart:
    def test_add_to_cart(self, page: Page):
        """测试添加商品"""
        # TODO: 实现测试
        pass

    def test_update_quantity(self, page: Page):
        """测试修改数量"""
        # TODO: 实现测试
        pass
```

---

#### 题目3：API Mock 测试（综合考察：请求拦截、Mock 响应）

**场景**：使用 Playwright 的请求拦截功能 Mock API 响应，测试前端不同状态。

**需求**：
1. Mock 用户列表 API 返回指定数据
2. Mock 错误响应（500、404 等）
3. 验证请求参数

**测试用例**：
```python
import json
from playwright.sync_api import Page, expect

class TestAPIMock:
    def test_mock_user_list(self, page: Page):
        """Mock 用户列表 API"""
        # TODO: Mock /api/users 返回指定数据
        pass

    def test_mock_error_response(self, page: Page):
        """Mock 错误响应"""
        # TODO: Mock /api/users 返回 500 错误
        pass
```

---

#### 题目4：多设备测试（综合考察：设备模拟、并行执行）

**场景**：配置测试在多个设备上运行，验证响应式布局。

**需求**：
1. 配置 iPhone 和 Android 设备模拟
2. 验证响应式布局
3. 生成多设备测试报告

**测试用例**：
```python
import pytest

class TestCrossDevice:
    @pytest.mark.parametrize("device_name", ["iPhone 13", "Pixel 5", "iPad Pro"])
    def test_responsive_design(self, device_name: str):
        """测试响应式设计"""
        # TODO: 实现测试
        pass
```

---

### 答案

#### 题目1 答案

```python
import pytest
from playwright.sync_api import Page, expect


class LoginPage:
    """登录页面 Page Object"""

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("请输入用户名")
        self.password_input = page.get_by_placeholder("请输入密码")
        self.login_button = page.get_by_role("button", name="登录")
        self.error_message = page.locator(".error-message")

    def navigate(self):
        """导航到登录页"""
        self.page.goto("/login")
        return self

    def login(self, username: str, password: str):
        """执行登录"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self


class TestLogin:
    """登录功能测试"""

    def test_login_success(self, page: Page):
        """测试登录成功"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("testuser", "password123")
        expect(page).to_have_url("**/dashboard")

    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "password123", "请输入用户名"),
        ("testuser", "", "请输入密码"),
        ("testuser", "wrong", "用户名或密码错误"),
    ])
    def test_login_failures(self, page: Page, username, password, expected_error):
        """测试登录失败场景"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(username, password)
        expect(login_page.error_message).to_have_text(expected_error)
```

#### 题目2 答案

```python
from playwright.sync_api import Page, expect


class CartPage:
    """购物车页面 Page Object"""

    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart-item")
        self.total_price = page.locator(".total-price")

    def navigate(self):
        self.page.goto("/cart")
        return self

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def update_quantity(self, product_name: str, quantity: int):
        item = self.cart_items.filter(has_text=product_name)
        item.locator(".quantity-input").fill(str(quantity))
        return self

    def remove_item(self, product_name: str):
        item = self.cart_items.filter(has_text=product_name)
        item.get_by_role("button", name="删除").click()
        return self


class TestCart:
    """购物车功能测试"""

    def test_add_to_cart(self, page: Page):
        """测试添加商品"""
        page.goto("/product/1")
        page.get_by_role("button", name="加入购物车").click()
        expect(page.locator(".success-message")).to_be_visible()

        cart_page = CartPage(page)
        cart_page.navigate()
        assert cart_page.get_item_count() == 1

    def test_update_quantity(self, page: Page):
        """测试修改数量"""
        cart_page = CartPage(page)
        cart_page.navigate()
        cart_page.update_quantity("商品A", 3)
        expect(cart_page.total_price).to_contain_text("300")
```

#### 题目3 答案

```python
import json
from playwright.sync_api import Page, expect


class TestAPIMock:
    """API Mock 测试"""

    def test_mock_user_list(self, page: Page):
        """Mock 用户列表 API"""
        mock_data = [
            {"id": 1, "name": "张三"},
            {"id": 2, "name": "李四"}
        ]
        page.route("**/api/users", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_data)
        ))

        page.goto("/users")
        expect(page.locator(".user-item")).to_have_count(2)

    def test_mock_error_response(self, page: Page):
        """Mock 错误响应"""
        page.route("**/api/users", lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"error": "服务器错误"})
        ))

        page.goto("/users")
        expect(page.locator(".error-message")).to_contain_text("服务器错误")
```

#### 题目4 答案

```python
import pytest
from playwright.sync_api import Playwright, expect


class TestCrossDevice:
    """多设备测试"""

    @pytest.mark.parametrize("device_name", ["iPhone 13", "Pixel 5", "iPad Pro"])
    def test_responsive_design(self, playwright: Playwright, device_name: str):
        """测试响应式设计"""
        device = playwright.devices[device_name]
        browser = playwright.chromium.launch()
        context = browser.new_context(**device)
        page = context.new_page()

        try:
            page.goto("/")
            expect(page.locator("body")).to_be_visible()

            if "iPhone" in device_name or "Pixel" in device_name:
                expect(page.locator(".mobile-menu")).to_be_visible()
            else:
                expect(page.locator(".desktop-menu")).to_be_visible()
        finally:
            context.close()
            browser.close()
```

---

### 自测检查清单

完成以上练习后，检查自己是否掌握以下能力：

#### 基础能力（必须掌握）
- [ ] 能安装和配置 Playwright 环境
- [ ] 能使用各种定位器（role、label、text、test_id）
- [ ] 能进行基本的页面操作（点击、输入、选择）
- [ ] 能使用 expect 断言验证结果
- [ ] 能编写简单的测试脚本

#### 进阶能力（应该了解）
- [ ] 能使用 Page Object 模式组织测试代码
- [ ] 能处理 iframe、多标签页、对话框
- [ ] 能使用请求拦截和 Mock 功能
- [ ] 能配置并行执行
- [ ] 能模拟不同设备和环境

#### 实战能力（综合应用）
- [ ] 能编写完整的业务流程测试
- [ ] 能集成 API 和 UI 混合测试
- [ ] 能配置 CI/CD 流水线
- [ ] 能进行简单的性能监控
- [ ] 能生成和管理测试报告
