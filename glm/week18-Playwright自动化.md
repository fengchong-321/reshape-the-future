# 第18周：Playwright UI 自动化

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

## 四、本周小结

1. **Playwright**：比 Selenium 更现代的选择
2. **定位器**：优先语义化定位
3. **Page Object**：测试代码可维护性的关键

### 下周预告

第19周学习 Appium 移动端测试。
