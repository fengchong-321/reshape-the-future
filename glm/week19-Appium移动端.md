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

## 四、练习内容

### 基础练习（1-8）

**练习1：环境搭建与基础脚本**

完成以下任务：
1. 安装 Appium 和相关依赖
2. 安装 UiAutomator2 驱动
3. 编写第一个 Android 测试脚本
4. 启动应用并验证包名

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options

def test_first_appium_script():
    """第一个 Appium 测试脚本"""
    options = UiAutomator2Options()
    # 请配置以下参数：
    # options.platform_name = ?
    # options.device_name = ?
    # options.app = ?
    # options.app_package = ?
    # options.app_activity = ?

    driver = webdriver.Remote("http://localhost:4723", options=options)

    # 验证应用已启动
    assert driver.current_package == "com.example.app"

    driver.quit()
```

**练习2：元素定位练习**

使用不同的定位方式找到以下元素：
1. 通过 ID 定位
2. 通过 Accessibility ID 定位
3. 通过 XPath 定位
4. 通过 UIAutomator 定位

```python
from appium.webdriver.common.appiumby import AppiumBy

def test_element_location(driver):
    # 通过 ID 定位
    element1 = driver.find_element(AppiumBy.___, "com.example:id/username")

    # 通过 Accessibility ID 定位
    element2 = driver.find_element(AppiumBy.___, "登录按钮")

    # 通过 XPath 定位
    element3 = driver.find_element(AppiumBy.___,
        "//android.widget.EditText[@text='用户名']")

    # 通过 UIAutomator 定位
    element4 = driver.find_element(AppiumBy.___,
        'new UiSelector().text("登录")')
```

**练习3：基本操作练习**

编写测试脚本完成以下操作：
1. 输入文本
2. 点击按钮
3. 清除文本
4. 获取元素文本
5. 判断元素是否显示

```python
def test_basic_operations(driver):
    # 输入用户名
    username = driver.find_element(AppiumBy.ID, "com.example:id/username")
    username.___("admin")

    # 输入密码
    password = driver.find_element(AppiumBy.ID, "com.example:id/password")
    password.___("123456")

    # 点击登录
    login_btn = driver.find_element(AppiumBy.ID, "com.example:id/login")
    login_btn.___

    # 获取欢迎文本
    welcome = driver.find_element(AppiumBy.ID, "com.example:id/welcome")
    text = welcome.___

    # 验证元素显示
    assert welcome.___
```

**练习4：等待策略练习**

使用不同的等待方式：
1. 隐式等待
2. 显式等待元素出现
3. 显式等待元素可点击
4. 自定义等待条件

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_waiting_strategies(driver):
    # 隐式等待
    driver.implicitly_wait(10)

    # 显式等待元素出现
    wait = WebDriverWait(driver, 10)
    element = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, "com.example:id/element"))
    )

    # 显式等待元素可点击
    clickable = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.example:id/button"))
    )

    # 自定义等待条件
    def text_equals(driver):
        el = driver.find_element(AppiumBy.ID, "com.example:id/status")
        return el.text == "成功"

    wait.until(text_equals)
```

**练习5：滑动操作练习**

编写测试脚本实现以下滑动：
1. 向上滑动
2. 向下滑动
3. 向左滑动
4. 向右滑动

```python
def test_swipe_operations(driver):
    # 获取屏幕尺寸
    size = driver.get_window_size()
    width = size['width']
    height = size['height']

    # 向上滑动（内容向下）
    driver.swide(___, ___, ___, ___, 500)

    # 向下滑动（内容向上）
    driver.swide(___, ___, ___, ___, 500)

    # 向左滑动
    driver.swide(___, ___, ___, ___, 500)

    # 向右滑动
    driver.swide(___, ___, ___, ___, 500)
```

**练习6：表单操作练习**

编写测试脚本完成以下表单操作：
1. 输入框操作
2. 复选框勾选
3. 单选按钮选择
4. 下拉框选择

```python
def test_form_operations(driver):
    # 输入文本
    driver.find_element(AppiumBy.ID, "name").send_keys("张三")

    # 勾选复选框
    checkbox = driver.find_element(AppiumBy.ID, "agree")
    if not checkbox.is_selected():
        checkbox.click()

    # 选择单选按钮
    driver.find_element(AppiumBy.ID, "gender_male").click()

    # 选择下拉框（通过文本点击）
    driver.find_element(AppiumBy.XPATH,
        "//android.widget.TextView[@text='北京']").click()
```

**练习7：键盘操作练习**

编写测试脚本实现以下键盘操作：
1. 隐藏键盘
2. 按返回键
3. 按回车键
4. 按菜单键

```python
def test_keyboard_operations(driver):
    # 输入完成后隐藏键盘
    driver.find_element(AppiumBy.ID, "search").send_keys("test")
    driver.___

    # 按返回键
    driver.press_keycode(___)  # KEYCODE_BACK = 4

    # 按回车键
    driver.press_keycode(___)  # KEYCODE_ENTER = 66

    # 按菜单键
    driver.press_keycode(___)  # KEYCODE_MENU = 82
```

**练习8：应用操作练习**

编写测试脚本实现以下应用操作：
1. 安装应用
2. 检查应用是否安装
3. 启动应用
4. 关闭应用
5. 后台运行应用

```python
def test_app_operations(driver):
    # 检查应用是否安装
    is_installed = driver.___("com.example.app")
    assert is_installed

    # 关闭应用
    driver.___

    # 启动应用
    driver.___("com.example.app")

    # 后台运行 5 秒
    driver.___(5)

    # 卸载应用（谨慎使用）
    # driver.remove_app("com.example.app")
```

---

### 进阶练习（9-16）

**练习9：滚动到元素**

编写测试脚本实现滚动到指定元素：

```python
def test_scroll_to_element(driver):
    # 使用 UIAutomator 滚动到元素
    element = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))' +
        '.scrollIntoView(new UiSelector().text("目标元素"))'
    )

    # 验证元素可见
    assert element.is_displayed()
```

**练习10：长按操作**

编写测试脚本实现长按操作：

```python
from appium.webdriver.common.touch_action import TouchAction

def test_long_press(driver):
    element = driver.find_element(AppiumBy.ID, "item")

    # 创建 TouchAction
    action = TouchAction(driver)

    # 长按元素
    action.long_press(element).perform()

    # 验证长按后的操作菜单出现
    menu = driver.find_element(AppiumBy.ID, "context_menu")
    assert menu.is_displayed()
```

**练习11：拖拽操作**

编写测试脚本实现拖拽操作：

```python
def test_drag_and_drop(driver):
    source = driver.find_element(AppiumBy.ID, "source")
    target = driver.find_element(AppiumBy.ID, "target")

    # 使用 TouchAction 实现拖拽
    action = TouchAction(driver)
    action.long_press(source).move_to(target).release().perform()

    # 验证拖拽成功
    assert source.location != target.location
```

**练习12：Toast 消息获取**

编写测试脚本获取 Toast 消息：

```python
def test_get_toast(driver):
    # 执行触发 Toast 的操作
    driver.find_element(AppiumBy.ID, "submit").click()

    # 获取 Toast 消息
    toast = driver.find_element(
        AppiumBy.XPATH,
        "//android.widget.Toast"
    )

    # 验证 Toast 内容
    assert "操作成功" in toast.text
```

**练习13：WebView 操作**

编写测试脚本处理 WebView：

```python
def test_webview(driver):
    # 获取所有上下文
    contexts = driver.___
    print("Available contexts:", contexts)

    # 切换到 WebView
    driver.switch_to.___("WEBVIEW_com.example.app")

    # 在 WebView 中操作（使用 Selenium 定位方式）
    from selenium.webdriver.common.by import By
    driver.find_element(By.ID, "username").send_keys("admin")

    # 切换回原生应用
    driver.switch_to.___("NATIVE_APP")
```

**练习14：Page Object 模式实现**

为登录页面实现 Page Object 模式：

```python
# pages/base_page.py
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_by_id(self, id_):
        return self.driver.find_element(AppiumBy.ID, id_)

    def swipe_up(self):
        size = self.driver.get_window_size()
        x = size['width'] // 2
        y1 = int(size['height'] * 0.8)
        y2 = int(size['height'] * 0.2)
        self.driver.swipe(x, y1, x, y2, 500)

# pages/login_page.py
class LoginPage(BasePage):
    USERNAME_ID = "com.example:id/username"
    PASSWORD_ID = "com.example:id/password"
    LOGIN_BTN_ID = "com.example:id/login"

    def login(self, username, password):
        self.find_by_id(self.USERNAME_ID).send_keys(username)
        self.find_by_id(self.PASSWORD_ID).send_keys(password)
        self.find_by_id(self.LOGIN_BTN_ID).click()
        return self

# tests/test_login.py
class TestLogin:
    def test_login_success(self, driver):
        login_page = LoginPage(driver)
        login_page.login("admin", "123456")
        # 验证登录成功
```

**练习15：Pytest 参数化测试**

使用 pytest 参数化实现数据驱动测试：

```python
import pytest

class TestLogin:
    @pytest.mark.parametrize("username,password,expected", [
        ("admin", "123456", "success"),
        ("admin", "wrong", "密码错误"),
        ("", "123456", "请输入用户名"),
        ("admin", "", "请输入密码"),
    ])
    def test_login_scenarios(self, driver, username, password, expected):
        login_page = LoginPage(driver)
        login_page.login(username, password)

        if expected == "success":
            # 验证登录成功
            assert login_page.is_logged_in()
        else:
            # 验证错误消息
            error = login_page.get_error_message()
            assert expected in error
```

**练习16：多点触控操作**

编写测试脚本实现双指缩放：

```python
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction

def test_pinch_zoom(driver):
    # 双指缩放
    action1 = TouchAction(driver)
    action2 = TouchAction(driver)

    # 手指1：从中心向左上移动
    action1.press(x=300, y=300).move_to(x=200, y=200)

    # 手指2：从中心向右下移动
    action2.press(x=300, y=300).move_to(x=400, y=400)

    # 同时执行
    multi = MultiAction(driver)
    multi.add(action1, action2)
    multi.perform()
```

---

### 综合练习（17-20）

**练习17：完整的移动端购物流程测试**

使用 Page Object 模式实现移动端购物流程测试：
1. 用户登录
2. 搜索商品
3. 查看商品详情
4. 添加到购物车
5. 结算下单
6. 验证订单状态

```python
# 需要实现的 Page Objects：
# - LoginPage
# - HomePage
# - SearchPage
# - ProductDetailPage
# - CartPage
# - CheckoutPage
# - OrderPage

class TestMobileShopping:
    def test_complete_shopping_flow(self, driver):
        # 1. 登录
        login_page = LoginPage(driver)
        login_page.login("user", "password")

        # 2. 搜索商品
        home_page = HomePage(driver)
        home_page.search("手机")

        # 3. 查看详情并加入购物车
        search_page = SearchPage(driver)
        search_page.click_first_product()

        # 4. 结算下单
        # 5. 验证订单
        pass
```

**练习18：混合应用测试**

编写测试脚本测试混合应用（原生 + WebView）：

```python
class TestHybridApp:
    def test_native_to_webview(self, driver):
        # 在原生界面操作
        driver.find_element(AppiumBy.ID, "open_web").click()

        # 等待 WebView 加载
        import time
        time.sleep(2)

        # 切换到 WebView
        contexts = driver.contexts
        webview_context = [c for c in contexts if "WEBVIEW" in c][0]
        driver.switch_to.context(webview_context)

        # 在 WebView 中测试
        from selenium.webdriver.common.by import By
        driver.find_element(By.ID, "web_element").click()

        # 切换回原生
        driver.switch_to.context("NATIVE_APP")

    def test_webview_to_native(self, driver):
        # WebView 操作触发原生功能
        pass
```

**练习19：设备特性测试**

编写测试脚本测试设备特性：
1. 摄像头调用
2. 相册选择
3. 地理位置模拟
4. 网络状态切换

```python
class TestDeviceFeatures:
    def test_camera(self, driver):
        # 触发拍照
        driver.find_element(AppiumBy.ID, "take_photo").click()

        # 授权摄像头（如果需要）
        # 确认拍照
        pass

    def test_location(self, driver):
        # 模拟地理位置
        driver.set_location(31.2304, 121.4737, 10)

        # 验证位置相关功能
        driver.find_element(AppiumBy.ID, "get_location").click()

    def test_network(self, driver):
        # 模拟网络切换
        driver.set_network_connection(1)  # 飞行模式
        driver.set_network_connection(4)  # 数据网络
        driver.set_network_connection(2)  # WiFi
```

**练习20：CI/CD 集成配置**

完成移动端测试的 CI/CD 配置：

```yaml
# .github/workflows/appium.yml
name: Appium Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  android-test:
    runs-on: macos-latest
    strategy:
      matrix:
        api-level: [29, 30]
        target: [google_apis]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          java-version: '11'

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Appium
        run: |
          npm install -g appium
          appium driver install uiautomator2

      - name: Run Tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: ${{ matrix.api-level }}
          target: ${{ matrix.target }}
          script: pytest tests/ -v

      - name: Upload Screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: screenshots
          path: screenshots/
```

```python
# conftest.py 完整配置
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.automation_name = "UiAutomator2"
    options.app = "/path/to/app.apk"
    options.no_reset = False

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            driver.save_screenshot(f"screenshots/{item.name}.png")
```
