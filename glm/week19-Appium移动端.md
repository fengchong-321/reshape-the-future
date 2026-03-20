# 第19周：Appium 移动端测试

## 本周目标

掌握 Appium 移动端自动化测试，能编写 Android/iOS 测试脚本。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Appium 安装 | 环境搭建、驱动安装 | ⭐⭐⭐⭐ |
| 元素定位 | UI Automator、XPath | ⭐⭐⭐⭐⭐ |
| 基本操作 | 点击、输入、滑动 | ⭐⭐⭐⭐⭐ |
| 高级操作 | 手势、多点触控 | ⭐⭐⭐⭐ |
| Pytest 集成 | 测试框架集成 | ⭐⭐⭐⭐⭐ |
| Page Object | 移动端 PO 模式 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 环境搭建

```bash
# ============================================
# 前置条件
# ============================================
# 1. 安装 Node.js
# 2. 安装 Java JDK 8+
# 3. 安装 Android SDK（Android 测试）
# 4. 安装 Xcode（iOS 测试，仅 Mac）

# ============================================
# 安装 Appium
# ============================================
# 方式1：NPM
npm install -g appium
appium --version

# 方式2：Appium Inspector（GUI）
# 下载：https://github.com/appium/appium-inspector/releases

# 安装驱动
appium driver install uiautomator2  # Android
appium driver install xcuitest     # iOS

# 查看已安装驱动
appium driver list

# ============================================
# 安装 Python 客户端
# ============================================
pip install Appium-Python-Client

# ============================================
# Android 环境变量
# ============================================
# ~/.bashrc 或 ~/.zshrc
export ANDROID_HOME=/Users/xxx/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin

# ============================================
# 启动 Appium
# ============================================
appium  # 默认 4723 端口
appium -p 4724  # 指定端口
```

---

### 2.2 基础脚本

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

# ============================================
# Android 配置
# ============================================
def create_android_driver():
    """创建 Android 驱动"""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.automation_name = "UiAutomator2"
    
    # 应用配置
    options.app = "/path/to/app.apk"
    options.app_package = "com.example.app"
    options.app_activity = ".MainActivity"
    
    # 其他选项
    options.no_reset = False  # 每次重置应用
    options.new_command_timeout = 600
    
    driver = webdriver.Remote(
        "http://localhost:4723",
        options=options
    )
    return driver

# ============================================
# iOS 配置
# ============================================
def create_ios_driver():
    """创建 iOS 驱动"""
    from appium.options.ios import XCUITestOptions
    
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.device_name = "iPhone 14"
    options.platform_version = "16.0"
    options.automation_name = "XCUITest"
    options.app = "/path/to/app.app"
    
    driver = webdriver.Remote(
        "http://localhost:4723",
        options=options
    )
    return driver

# ============================================
# 基本操作
# ============================================
def test_basic_operations():
    driver = create_android_driver()
    
    try:
        # 元素定位
        element = driver.find_element(AppiumBy.ID, "com.example.app:id/username")
        
        # 输入文本
        element.send_keys("admin")
        
        # 点击
        driver.find_element(AppiumBy.ID, "com.example.app:id/login").click()
        
        # 获取文本
        text = driver.find_element(AppiumBy.ID, "com.example.app:id/title").text
        
        # 清除文本
        element.clear()
        
        # 判断是否显示
        is_displayed = element.is_displayed()
        
    finally:
        driver.quit()
```

---

### 2.3 元素定位

```python
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

# ============================================
# 定位方式
# ============================================
# ID 定位（最常用）
element = driver.find_element(AppiumBy.ID, "com.example.app:id/username")

# Accessibility ID
element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "登录按钮")

# Class Name
element = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")

# XPath
element = driver.find_element(
    AppiumBy.XPATH, 
    "//android.widget.EditText[@text='用户名']"
)

# Android UIAutomator
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("登录")'
)

# 组合条件
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.Button").text("登录")'
)

# iOS Predicate
element = driver.find_element(
    AppiumBy.IOS_PREDICATE,
    "name == '登录' AND visible == 1"
)

# ============================================
# 定位技巧
# ============================================
# 文本包含
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().textContains("登录")'
)

# 通过描述定位
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().description("登录按钮")'
)

# 通过资源ID定位
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.example:id/login")'
)

# 父子关系
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.LinearLayout").childSelector(
        new UiSelector().text("登录")
    )'
)

# ============================================
# 等待元素
# ============================================
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 显式等待
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((AppiumBy.ID, "com.example:id/username"))
)

# 等待可点击
element = wait.until(
    EC.element_to_be_clickable((AppiumBy.ID, "com.example:id/login"))
)

# 自定义等待条件
def element_has_text(driver):
    element = driver.find_element(AppiumBy.ID, "status")
    return element.text == "成功"

wait.until(element_has_text)
```

---

### 2.4 手势操作

```python
from appium.webdriver.common.touch_action import TouchAction

# ============================================
# 点击
# ============================================
# 元素点击
element = driver.find_element(AppiumBy.ID, "button")
element.click()

# 坐标点击
driver.tap([(100, 200)])

# ============================================
# 滑动
# ============================================
# 使用 swipe
driver.swipe(100, 500, 100, 200, 500)  # x1, y1, x2, y2, duration

# 向上滑动（内容向下）
def swipe_up(driver):
    size = driver.get_window_size()
    x = size['width'] // 2
    y1 = size['height'] * 0.8
    y2 = size['height'] * 0.2
    driver.swipe(x, y1, x, y2, 500)

# 向下滑动
def swipe_down(driver):
    size = driver.get_window_size()
    x = size['width'] // 2
    y1 = size['height'] * 0.2
    y2 = size['height'] * 0.8
    driver.swipe(x, y1, x, y2, 500)

# 左右滑动
def swipe_left(driver):
    size = driver.get_window_size()
    y = size['height'] // 2
    x1 = size['width'] * 0.8
    x2 = size['width'] * 0.2
    driver.swipe(x1, y, x2, y, 500)

# ============================================
# 滚动到元素
# ============================================
# Android UIAutomator 滚动
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(
        new UiSelector().text("目标元素")
    )'
)

# iOS 滚动
element = driver.find_element(
    AppiumBy.IOS_PREDICATE,
    "name == '目标元素'"
)

# ============================================
# 长按
# ============================================
action = TouchAction(driver)
element = driver.find_element(AppiumBy.ID, "item")
action.long_press(element).perform()

# 长按后拖拽
action.long_press(element).move_to(target).release().perform()

# ============================================
# 多点触控
# ============================================
from appium.webdriver.common.multi_action import MultiAction

# 双指缩放
action1 = TouchAction(driver)
action2 = TouchAction(driver)

action1.press(x=100, y=100).move_to(x=50, y=50)
action2.press(x=200, y=200).move_to(x=250, y=250)

multi_action = MultiAction(driver)
multi_action.add(action1, action2)
multi_action.perform()

# ============================================
# 手势密码
# ============================================
def draw_pattern(driver, points):
    """绘制手势密码"""
    action = TouchAction(driver)
    first = True
    
    for point in points:
        if first:
            action.press(x=point[0], y=point[1])
            first = False
        else:
            action.move_to(x=point[0], y=point[1])
    
    action.release().perform()
```

---

### 2.5 高级功能

```python
# ============================================
# 键盘操作
# ============================================
# 隐藏键盘
driver.hide_keyboard()

# 按键
driver.press_keycode(4)  # Android 返回键
driver.press_keycode(66)  # 回车键

# 常用键码
KEYCODE_HOME = 3
KEYCODE_BACK = 4
KEYCODE_MENU = 82
KEYCODE_ENTER = 66
KEYCODE_SEARCH = 84

# ============================================
# 屏幕操作
# ============================================
# 截图
driver.save_screenshot("screenshot.png")

# 获取屏幕尺寸
size = driver.get_window_size()
width = size['width']
height = size['height']

# 获取源码
source = driver.page_source

# ============================================
# 应用操作
# ============================================
# 安装应用
driver.install_app("/path/to/app.apk")

# 卸载应用
driver.remove_app("com.example.app")

# 检查应用是否安装
is_installed = driver.is_app_installed("com.example.app")

# 启动应用
driver.activate_app("com.example.app")

# 关闭应用
driver.close_app()

# 重置应用
driver.reset()

# 后台运行
driver.background_app(5)  # 后台5秒

# ============================================
# Toast 消息
# ============================================
# Android 获取 Toast
toast = driver.find_element(
    AppiumBy.XPATH,
    "//android.widget.Toast"
)
print(toast.text)

# ============================================
# WebView 操作
# ============================================
# 切换到 WebView
contexts = driver.contexts  # 获取所有上下文
driver.switch_to.context("WEBVIEW_com.example.app")

# 在 WebView 中操作
driver.find_element(By.ID, "username").send_keys("admin")

# 切换回原生
driver.switch_to.context("NATIVE_APP")

# ============================================
# 文件操作
# ============================================
# 推送文件到设备
driver.push_file("/sdcard/test.txt", "Hello World")

# 从设备拉取文件
content = driver.pull_file("/sdcard/test.txt")
```

---

### 2.6 Pytest 集成

```python
# ============================================
# conftest.py
# ============================================
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope="function")
def driver():
    """Appium 驱动 fixture"""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app = "/path/to/app.apk"
    options.no_reset = False
    
    driver = webdriver.Remote(
        "http://localhost:4723",
        options=options
    )
    
    yield driver
    
    driver.quit()

# ============================================
# 测试用例
# ============================================
# tests/test_login.py
import pytest
from appium.webdriver.common.appiumby import AppiumBy

class TestLogin:
    """登录测试"""

    def test_login_success(self, driver):
        """测试登录成功"""
        # 输入用户名
        username = driver.find_element(
            AppiumBy.ID, "com.example.app:id/username"
        )
        username.send_keys("admin")
        
        # 输入密码
        password = driver.find_element(
            AppiumBy.ID, "com.example.app:id/password"
        )
        password.send_keys("123456")
        
        # 点击登录
        login_btn = driver.find_element(
            AppiumBy.ID, "com.example.app:id/login"
        )
        login_btn.click()
        
        # 验证
        welcome = driver.find_element(
            AppiumBy.ID, "com.example.app:id/welcome"
        )
        assert welcome.text == "欢迎, admin"

    @pytest.mark.parametrize("username,password", [
        ("admin", "wrong"),
        ("", "123456"),
        ("admin", ""),
    ])
    def test_login_fail(self, driver, username, password):
        """测试登录失败"""
        # ... 登录操作
        
        # 验证错误提示
        error = driver.find_element(
            AppiumBy.ID, "com.example.app:id/error"
        )
        assert error.is_displayed()

# ============================================
# 运行测试
# ============================================
# pytest tests/ -v --tb=short
```

---

### 2.7 Page Object 模式

```python
# ============================================
# pages/base_page.py
# ============================================
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """页面基类"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element_by_id(self, id_):
        """通过 ID 定位"""
        return self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, id_))
        )
    
    def find_element_by_text(self, text):
        """通过文本定位"""
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{text}")'
        )
    
    def swipe_up(self):
        """向上滑动"""
        size = self.driver.get_window_size()
        x = size['width'] // 2
        y1 = int(size['height'] * 0.8)
        y2 = int(size['height'] * 0.2)
        self.driver.swipe(x, y1, x, y2, 500)
    
    def swipe_to_element(self, text):
        """滑动到指定元素"""
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{text}"))'
        )

# ============================================
# pages/login_page.py
# ============================================
class LoginPage(BasePage):
    """登录页面"""
    
    # 定位器
    USERNAME_ID = "com.example.app:id/username"
    PASSWORD_ID = "com.example.app:id/password"
    LOGIN_BTN_ID = "com.example.app:id/login"
    ERROR_ID = "com.example.app:id/error"
    
    def login(self, username: str, password: str):
        """执行登录"""
        self.find_element_by_id(self.USERNAME_ID).send_keys(username)
        self.find_element_by_id(self.PASSWORD_ID).send_keys(password)
        self.find_element_by_id(self.LOGIN_BTN_ID).click()
        return self
    
    def get_error_message(self) -> str:
        """获取错误消息"""
        return self.find_element_by_id(self.ERROR_ID).text

# ============================================
# pages/home_page.py
# ============================================
class HomePage(BasePage):
    """首页"""
    
    WELCOME_ID = "com.example.app:id/welcome"
    MENU_ID = "com.example.app:id/menu"
    
    def get_welcome_text(self) -> str:
        return self.find_element_by_id(self.WELCOME_ID).text
    
    def is_logged_in(self) -> bool:
        try:
            return self.find_element_by_id(self.MENU_ID).is_displayed()
        except:
            return False

# ============================================
# 测试用例
# ============================================
class TestLogin:
    
    def test_login_success(self, driver):
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        
        login_page.login("admin", "123456")
        
        assert home_page.is_logged_in()
        assert "admin" in home_page.get_welcome_text()
```

---

## 三、学到什么程度

### 必须掌握

- [ ] Appium 环境搭建
- [ ] 元素定位
- [ ] 基本操作
- [ ] Pytest 集成

### 应该了解

- [ ] 手势操作
- [ ] WebView 混合应用

---

## 四、本周小结

1. **Appium**：移动端自动化标准
2. **手势操作**：模拟用户真实操作
3. **Page Object**：提高测试可维护性

### 下周预告

第20周综合项目实战。
