# 第21周：Appium 移动端测试

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

#### 练习1：环境搭建与基础脚本

**场景说明：**
作为移动端测试工程师，需要搭建 Appium 自动化测试环境并编写第一个测试脚本，验证环境配置是否正确，这是进行移动端自动化测试的第一步。

**具体需求：**
1. 安装 Appium 和相关依赖
2. 安装 UiAutomator2 驱动
3. 编写第一个 Android 测试脚本
4. 启动应用并验证包名

**使用示例：**
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

**验收标准：**
- [ ] 成功安装 Appium 并能正常运行
- [ ] UiAutomator2 驱动安装成功
- [ ] 测试脚本能成功连接到 Appium 服务器
- [ ] 应用能正常启动并验证包名正确

#### 练习2：元素定位练习

**场景说明：**
在移动端自动化测试中，元素定位是最基础且最重要的技能。不同场景需要使用不同的定位策略，比如某些元素没有 ID 但有可访问性标识，需要灵活运用多种定位方式。

**具体需求：**
1. 通过 ID 定位
2. 通过 Accessibility ID 定位
3. 通过 XPath 定位
4. 通过 UIAutomator 定位

**使用示例：**
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

**验收标准：**
- [ ] 成功使用 ID 定位方式找到元素
- [ ] 成功使用 Accessibility ID 定位方式找到元素
- [ ] 成功使用 XPath 定位方式找到元素
- [ ] 成功使用 UIAutomator 定位方式找到元素

#### 练习3：基本操作练习

**场景说明：**
在移动端应用测试中，输入文本、点击按钮、获取元素文本等是最常用的操作。掌握这些基本操作是编写有效测试用例的前提。

**具体需求：**
1. 输入文本
2. 点击按钮
3. 清除文本
4. 获取元素文本
5. 判断元素是否显示

**使用示例：**
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

**验收标准：**
- [ ] 成功向输入框输入文本
- [ ] 成功点击按钮元素
- [ ] 成功清除输入框中的文本
- [ ] 成功获取元素的文本内容
- [ ] 成功判断元素是否显示

#### 练习4：等待策略练习

**场景说明：**
移动端应用由于网络延迟、动画效果等原因，元素加载时机不确定。合理使用等待策略可以避免因元素未加载完成而导致的测试失败，提高测试稳定性。

**具体需求：**
1. 隐式等待
2. 显式等待元素出现
3. 显式等待元素可点击
4. 自定义等待条件

**使用示例：**
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

**验收标准：**
- [ ] 成功设置并使用隐式等待
- [ ] 成功使用显式等待元素出现
- [ ] 成功使用显式等待元素可点击
- [ ] 成功实现并使用自定义等待条件

#### 练习5：滑动操作练习

**场景说明：**
移动端应用经常需要滑动屏幕来查看更多内容，比如在长列表中滚动、切换轮播图、滑动删除等场景。掌握滑动操作是移动端自动化测试的必备技能。

**具体需求：**
1. 向上滑动
2. 向下滑动
3. 向左滑动
4. 向右滑动

**使用示例：**
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

**验收标准：**
- [ ] 成功实现向上滑动操作
- [ ] 成功实现向下滑动操作
- [ ] 成功实现向左滑动操作
- [ ] 成功实现向右滑动操作

#### 练习6：表单操作练习

**场景说明：**
移动端应用中经常包含各种表单，如注册页面、设置页面等。需要掌握不同表单元素的操作方法，包括输入框、复选框、单选按钮和下拉选择框。

**具体需求：**
1. 输入框操作
2. 复选框勾选
3. 单选按钮选择
4. 下拉框选择

**使用示例：**
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

**验收标准：**
- [ ] 成功向输入框输入文本
- [ ] 成功勾选复选框
- [ ] 成功选择单选按钮
- [ ] 成功选择下拉框选项

#### 练习7：键盘操作练习

**场景说明：**
在移动端测试中，经常需要模拟物理按键操作，比如输入完成后隐藏软键盘、按返回键退出页面、按回车键提交搜索等。掌握键盘操作可以更真实地模拟用户行为。

**具体需求：**
1. 隐藏键盘
2. 按返回键
3. 按回车键
4. 按菜单键

**使用示例：**
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

**验收标准：**
- [ ] 成功隐藏软键盘
- [ ] 成功按返回键
- [ ] 成功按回车键
- [ ] 成功按菜单键

#### 练习8：应用操作练习

**场景说明：**
在测试过程中，经常需要对应用进行安装、启动、关闭、后台运行等操作。比如测试应用升级场景需要先卸载旧版本，测试后台恢复场景需要将应用切换到后台。

**具体需求：**
1. 安装应用
2. 检查应用是否安装
3. 启动应用
4. 关闭应用
5. 后台运行应用

**使用示例：**
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

**验收标准：**
- [ ] 成功检查应用是否安装
- [ ] 成功关闭应用
- [ ] 成功启动应用
- [ ] 成功将应用切换到后台运行
- [ ] 理解卸载应用的使用场景

---

### 进阶练习（9-16）

#### 练习9：滚动到元素

**场景说明：**
在移动端应用中，列表往往很长，需要滚动的元素可能在屏幕外。使用 UIAutomator 的 UiScrollable 可以自动滚动到目标元素，提高测试效率。

**具体需求：**
1. 使用 UiScrollable 实现滚动到指定元素
2. 验证滚动后元素可见

**使用示例：**
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

**验收标准：**
- [ ] 成功使用 UiScrollable 滚动到指定元素
- [ ] 验证滚动后元素可见
- [ ] 理解 UiScrollable 的使用场景

#### 练习10：长按操作

**场景说明：**
长按是移动端常见的交互方式，比如长按消息弹出复制/删除菜单、长按图标进入编辑模式等。使用 TouchAction 可以模拟长按手势操作。

**具体需求：**
1. 使用 TouchAction 实现长按操作
2. 验证长按后的操作菜单出现

**使用示例：**
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

**验收标准：**
- [ ] 成功创建 TouchAction 对象
- [ ] 成功实现长按操作
- [ ] 验证长按后出现预期的操作菜单

#### 练习11：拖拽操作

**场景说明：**
拖拽操作在移动端应用中很常见，比如拖动排序、拖动图标到文件夹、拖拽删除等场景。需要组合使用长按、移动和释放手势来完成。

**具体需求：**
1. 使用 TouchAction 实现拖拽操作
2. 验证拖拽成功

**使用示例：**
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

**验收标准：**
- [ ] 成功实现拖拽操作
- [ ] 验证拖拽后元素位置发生变化
- [ ] 理解 TouchAction 链式调用方式

#### 练习12：Toast 消息获取

**场景说明：**
Toast 是 Android 系统中常见的轻量级提示消息，用于显示操作结果。由于 Toast 显示时间很短，需要使用特定的定位方式来捕获并验证其内容。

**具体需求：**
1. 执行触发 Toast 的操作
2. 使用 XPath 定位 Toast 消息
3. 验证 Toast 内容

**使用示例：**
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

**验收标准：**
- [ ] 成功触发 Toast 消息
- [ ] 成功定位并获取 Toast 消息
- [ ] 验证 Toast 内容符合预期

#### 练习13：WebView 操作

**场景说明：**
混合应用（Hybrid App）同时包含原生界面和 WebView 网页内容。测试时需要在原生上下文和 WebView 上下文之间切换，使用不同的定位策略。

**具体需求：**
1. 获取所有可用的上下文
2. 切换到 WebView 上下文
3. 在 WebView 中进行操作
4. 切换回原生应用上下文

**使用示例：**
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

**验收标准：**
- [ ] 成功获取所有上下文列表
- [ ] 成功切换到 WebView 上下文
- [ ] 在 WebView 中成功操作元素
- [ ] 成功切换回原生应用上下文

#### 练习14：Page Object 模式实现

**场景说明：**
Page Object 模式是自动化测试的最佳实践，将页面元素定位和操作封装成页面对象，提高代码可维护性和可复用性，便于团队协作。

**具体需求：**
1. 创建 BasePage 基类封装通用操作
2. 创建 LoginPage 页面对象类
3. 在测试用例中使用 Page Object

**使用示例：**
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

**验收标准：**
- [ ] 成功创建 BasePage 基类
- [ ] 成功创建 LoginPage 页面对象
- [ ] 测试用例中使用 Page Object 模式
- [ ] 代码结构清晰，易于维护

#### 练习15：Pytest 参数化测试

**场景说明：**
数据驱动测试是自动化测试的重要技术，通过参数化可以用同一套测试逻辑覆盖多种测试场景，如正常登录、密码错误、用户名为空等，提高测试覆盖率。

**具体需求：**
1. 使用 pytest.mark.parametrize 实现参数化
2. 覆盖多种登录场景
3. 验证不同场景的预期结果

**使用示例：**
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

**验收标准：**
- [ ] 成功使用 pytest.mark.parametrize 装饰器
- [ ] 覆盖至少 4 种不同的测试场景
- [ ] 验证成功和失败场景都能正确判断
- [ ] 测试用例结构清晰，易于扩展

#### 练习16：多点触控操作

**场景说明：**
多点触控是移动端特有的交互方式，如双指缩放图片、地图缩放等。使用 MultiAction 可以同时控制多个手指的操作，模拟复杂的手势。

**具体需求：**
1. 创建多个 TouchAction 对象
2. 使用 MultiAction 组合多个手势
3. 实现双指缩放操作

**使用示例：**
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

**验收标准：**
- [ ] 成功创建多个 TouchAction 对象
- [ ] 成功使用 MultiAction 组合手势
- [ ] 成功实现双指缩放操作
- [ ] 理解多点触控的应用场景

---

### 综合练习（17-20）

#### 练习17：完整的移动端购物流程测试

**场景说明：**
电商类应用是移动端最常见的应用类型之一，完整的购物流程测试涵盖了登录、搜索、浏览、加购、下单等多个环节，是综合运用 Appium 技能的最佳实践。

**具体需求：**
1. 用户登录
2. 搜索商品
3. 查看商品详情
4. 添加到购物车
5. 结算下单
6. 验证订单状态

**使用示例：**
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

**验收标准：**
- [ ] 成功实现所有 Page Objects
- [ ] 完整的购物流程测试通过
- [ ] 测试代码结构清晰
- [ ] 验证订单状态正确

#### 练习18：混合应用测试

**场景说明：**
混合应用（Hybrid App）结合了原生应用和 Web 技术的优势，测试时需要在原生和 WebView 上下文之间频繁切换。这是移动端测试工程师必须掌握的高级技能。

**具体需求：**
1. 在原生界面进行操作
2. 切换到 WebView 上下文
3. 在 WebView 中进行测试
4. WebView 操作触发原生功能
5. 切换回原生上下文验证结果

**使用示例：**
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

**验收标准：**
- [ ] 成功识别并切换到 WebView 上下文
- [ ] 在 WebView 中成功操作元素
- [ ] 成功切换回原生上下文
- [ ] 理解混合应用的测试策略

#### 练习19：设备特性测试

**场景说明：**
移动端应用经常需要使用设备特性，如摄像头拍照、相册选择图片、获取地理位置、网络状态等。Appium 提供了模拟这些设备特性的能力，便于进行相关功能的测试。

**具体需求：**
1. 摄像头调用
2. 相册选择
3. 地理位置模拟
4. 网络状态切换

**使用示例：**
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

**验收标准：**
- [ ] 成功触发摄像头功能
- [ ] 成功模拟地理位置
- [ ] 成功切换网络状态
- [ ] 理解设备特性测试的应用场景

#### 练习20：CI/CD 集成配置

**场景说明：**
将移动端自动化测试集成到 CI/CD 流水线中，可以在每次代码提交时自动运行测试，及早发现问题。GitHub Actions 提供了方便的 Android 模拟器支持，适合运行 Appium 测试。

**具体需求：**
1. 配置 GitHub Actions 工作流
2. 设置多 API 级别的矩阵测试
3. 自动安装 Appium 和驱动
4. 运行测试并收集失败截图

**使用示例：**
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

**验收标准：**
- [ ] 成功配置 GitHub Actions 工作流
- [ ] 多 API 级别矩阵测试配置正确
- [ ] Appium 和驱动自动安装成功
- [ ] 测试失败时自动上传截图

---

## 五、检验标准

### 验证题1：移动端登录功能测试

**场景描述**：为移动端应用编写完整的登录功能测试，验证对 Appium 基础操作的掌握。

**详细需求**：
1. 使用 Page Object 模式封装登录页面
2. 实现登录成功和失败的测试用例
3. 使用参数化测试多种登录场景
4. 验证错误提示信息

**测试用例**：
```python
import pytest
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage:
    """登录页面 Page Object - 请实现"""

    def __init__(self, driver):
        self.driver = driver
        # TODO: 定义定位器

    def navigate(self):
        # TODO: 导航到登录页
        pass

    def login(self, username: str, password: str):
        # TODO: 执行登录
        pass

    def get_error_message(self) -> str:
        # TODO: 获取错误消息
        pass


class TestLogin:
    def test_login_success(self, driver):
        """测试登录成功"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("testuser", "password123")
        # TODO: 验证登录成功

    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "password123", "请输入用户名"),
        ("testuser", "", "请输入密码"),
        ("testuser", "wrong", "用户名或密码错误"),
    ])
    def test_login_failures(self, driver, username, password, expected_error):
        """测试登录失败场景"""
        # TODO: 实现测试
        pass
```

**完整答案**：
```python
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """登录页面 Page Object"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # 定位器
        self.username_input = (AppiumBy.ID, "com.example.app:id/username")
        self.password_input = (AppiumBy.ID, "com.example.app:id/password")
        self.login_button = (AppiumBy.ID, "com.example.app:id/login")
        self.error_message = (AppiumBy.ID, "com.example.app:id/error")

    def navigate(self):
        """导航到登录页"""
        self.driver.startActivity("com.example.app", ".LoginActivity")
        return self

    def login(self, username: str, password: str):
        """执行登录"""
        self.wait.until(EC.presence_of_element_located(self.username_input)).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
        return self

    def get_error_message(self) -> str:
        """获取错误消息"""
        element = self.wait.until(EC.presence_of_element_located(self.error_message))
        return element.text


class TestLogin:
    """登录功能测试"""

    def test_login_success(self, driver):
        """测试登录成功"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("testuser", "password123")

        # 验证登录成功 - 检查是否跳转到首页
        welcome = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.example.app:id/welcome"))
        )
        assert "欢迎" in welcome.text

    @pytest.mark.parametrize("username,password,expected_error", [
        ("", "password123", "请输入用户名"),
        ("testuser", "", "请输入密码"),
        ("testuser", "wrong", "用户名或密码错误"),
    ])
    def test_login_failures(self, driver, username, password, expected_error):
        """测试登录失败场景"""
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(username, password)

        error = login_page.get_error_message()
        assert expected_error in error
```

**自测检查清单**：
- [ ] LoginPage 类正确封装所有元素和操作
- [ ] 测试用例代码清晰简洁
- [ ] 参数化测试正确实现
- [ ] 断言方法正确使用

---

### 验证题2：移动端滑动操作测试

**场景描述**：测试移动端常见的滑动操作，验证对手势操作的掌握。

**详细需求**：
1. 实现向上、向下、向左、向右滑动
2. 实现滚动到指定元素
3. 实现长按操作

**测试用例**：
```python
class TestSwipe:
    """滑动操作测试"""

    def test_swipe_up(self, driver):
        """测试向上滑动"""
        # TODO: 实现向上滑动并验证
        pass

    def test_swipe_down(self, driver):
        """测试向下滑动"""
        # TODO: 实现向下滑动并验证
        pass

    def test_scroll_to_element(self, driver):
        """测试滚动到指定元素"""
        # TODO: 实现滚动到指定元素
        pass

    def test_long_press(self, driver):
        """测试长按操作"""
        # TODO: 实现长按操作
        pass
```

**完整答案**：
```python
from appium.webdriver.common.touch_action import TouchAction


class TestSwipe:
    """滑动操作测试"""

    def test_swipe_up(self, driver):
        """测试向上滑动"""
        size = driver.get_window_size()
        x = size['width'] // 2
        y1 = int(size['height'] * 0.8)
        y2 = int(size['height'] * 0.2)

        # 记录滑动前的元素
        element_before = driver.find_element(AppiumBy.ID, "top_element")

        # 向上滑动
        driver.swipe(x, y1, x, y2, 500)

        # 验证元素不可见
        assert not element_before.is_displayed()

    def test_swipe_down(self, driver):
        """测试向下滑动"""
        size = driver.get_window_size()
        x = size['width'] // 2
        y1 = int(size['height'] * 0.2)
        y2 = int(size['height'] * 0.8)

        driver.swipe(x, y1, x, y2, 500)

    def test_scroll_to_element(self, driver):
        """测试滚动到指定元素"""
        # 使用 UIAutomator 滚动到元素
        element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().text("目标元素"))'
        )

        assert element.is_displayed()

    def test_long_press(self, driver):
        """测试长按操作"""
        element = driver.find_element(AppiumBy.ID, "item")

        action = TouchAction(driver)
        action.long_press(element).perform()

        # 验证长按后的操作菜单出现
        menu = driver.find_element(AppiumBy.ID, "context_menu")
        assert menu.is_displayed()
```

**自测检查清单**：
- [ ] 能正确实现各方向滑动
- [ ] 能正确使用 UIAutomator 滚动
- [ ] 能正确实现长按操作
- [ ] 能正确验证操作结果

---

### 验证题3：混合应用测试

**场景描述**：测试混合应用（原生 + WebView），验证对上下文切换的掌握。

**详细需求**：
1. 获取所有上下文
2. 切换到 WebView 上下文
3. 在 WebView 中执行操作
4. 切换回原生上下文

**测试用例**：
```python
class TestHybridApp:
    """混合应用测试"""

    def test_context_switch(self, driver):
        """测试上下文切换"""
        # TODO: 实现上下文切换测试
        pass

    def test_webview_operation(self, driver):
        """测试 WebView 操作"""
        # TODO: 实现 WebView 操作测试
        pass
```

**完整答案**：
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestHybridApp:
    """混合应用测试"""

    def test_context_switch(self, driver):
        """测试上下文切换"""
        # 打开 WebView 页面
        driver.find_element(AppiumBy.ID, "open_webview").click()

        # 等待 WebView 加载
        WebDriverWait(driver, 10).until(
            lambda d: len(d.contexts) > 1
        )

        # 获取所有上下文
        contexts = driver.contexts
        print(f"可用上下文: {contexts}")

        # 找到 WebView 上下文
        webview_context = None
        for context in contexts:
            if "WEBVIEW" in context:
                webview_context = context
                break

        assert webview_context is not None, "未找到 WebView 上下文"

        # 切换到 WebView
        driver.switch_to.context(webview_context)

        # 验证切换成功
        assert "WEBVIEW" in driver.current_context

        # 切换回原生
        driver.switch_to.context("NATIVE_APP")
        assert driver.current_context == "NATIVE_APP"

    def test_webview_operation(self, driver):
        """测试 WebView 操作"""
        # 打开 WebView 页面
        driver.find_element(AppiumBy.ID, "open_webview").click()

        # 等待并切换到 WebView
        WebDriverWait(driver, 10).until(
            lambda d: any("WEBVIEW" in c for c in d.contexts)
        )

        webview_context = [c for c in driver.contexts if "WEBVIEW" in c][0]
        driver.switch_to.context(webview_context)

        # 在 WebView 中操作（使用 Selenium 定位方式）
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        search_input.send_keys("测试搜索")

        search_button = driver.find_element(By.ID, "search_button")
        search_button.click()

        # 验证搜索结果
        results = driver.find_elements(By.CLASS_NAME, "result_item")
        assert len(results) > 0

        # 切换回原生
        driver.switch_to.context("NATIVE_APP")
```

**自测检查清单**：
- [ ] 能正确获取所有上下文
- [ ] 能正确切换到 WebView
- [ ] 能在 WebView 中使用 Selenium 定位
- [ ] 能正确切换回原生上下文

---

### 验证题4：Pytest 集成测试

**场景描述**：配置完整的 Pytest + Appium 测试框架，验证对测试框架集成的掌握。

**详细需求**：
1. 编写 conftest.py 配置文件
2. 实现失败自动截图
3. 实现参数化测试
4. 配置测试报告

**测试用例**：
```python
# conftest.py
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

# TODO: 实现 driver fixture
# TODO: 实现失败截图 hook

# tests/test_search.py
class TestSearch:
    @pytest.mark.parametrize("keyword,expected_count", [
        ("手机", 10),
        ("电脑", 5),
        ("平板", 3),
    ])
    def test_search(self, driver, keyword, expected_count):
        # TODO: 实现搜索测试
        pass
```

**完整答案**：
```python
# conftest.py
import pytest
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
def driver():
    """Appium 驱动 fixture"""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.automation_name = "UiAutomator2"
    options.app = "/path/to/app.apk"
    options.no_reset = False
    options.new_command_timeout = 600

    driver = webdriver.Remote("http://localhost:4723", options=options)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # 创建截图目录
            os.makedirs("screenshots", exist_ok=True)
            # 保存截图
            screenshot_path = f"screenshots/{item.name}_failure.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n失败截图已保存: {screenshot_path}")


# tests/test_search.py
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSearch:
    """搜索功能测试"""

    @pytest.mark.parametrize("keyword,expected_count", [
        ("手机", 10),
        ("电脑", 5),
        ("平板", 3),
    ])
    def test_search(self, driver, keyword, expected_count):
        """测试搜索功能"""
        # 点击搜索框
        search_icon = driver.find_element(AppiumBy.ID, "com.example.app:id/search_icon")
        search_icon.click()

        # 输入搜索关键词
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.example.app:id/search_input"))
        )
        search_input.send_keys(keyword)

        # 点击搜索按钮
        driver.find_element(AppiumBy.ID, "com.example.app:id/search_button").click()

        # 等待结果加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.example.app:id/result_list"))
        )

        # 验证结果数量
        results = driver.find_elements(AppiumBy.ID, "com.example.app:id/result_item")
        assert len(results) == expected_count, f"期望 {expected_count} 个结果，实际 {len(results)} 个"
```

**自测检查清单**：
- [ ] conftest.py 正确配置
- [ ] driver fixture 正确实现
- [ ] 失败截图 hook 正确实现
- [ ] 参数化测试正确实现
- [ ] 断言正确

---

## 六、本周小结
