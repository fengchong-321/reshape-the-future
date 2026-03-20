# 第 16 周 - 移动端测试 + 自动化综合

## 学习目标
了解移动端测试基础，能够使用 Appium 进行基本的移动端自动化测试。

---

## 知识点清单

### 1. Appium 原理
**掌握程度**: 架构、Driver、Inspector

**练习资源**:
- [Appium 官方文档](http://appium.io/)
- [Appium 入门教程](https://github.com/appium/appium/blob/master/docs/zh-cn/about.md)

**练习任务**:
- 理解 Appium 的工作原理
- 理解 Client-Server 架构

---

### 2. 环境搭建
**掌握程度**: Android SDK、模拟器

**练习任务**:
- 安装 Android SDK
- 配置模拟器
- 安装 Appium Desktop

---

### 3. 定位策略
**掌握程度**: accessibilityId/XPath/uiautomator

**练习任务**:
- 用 3 种方式定位元素
- 理解各种定位方式的优缺点

---

### 4. 手势操作
**掌握程度**: tap/swipe/pinch

**练习任务**:
- 实现点击操作
- 实现滑动操作
- 实现缩放手势

---

### 5. 混合应用
**掌握程度**: WebView、context 切换

**练习任务**:
- 理解 Native 和 WebView 的区别
- 实现 context 切换

---

### 6. 云测试平台
**掌握程度**: BrowserStack/SauceLabs

**练习任务**:
- 注册云测试平台
- 跑一次云测试

---

### 7. 自动化对比
**掌握程度**: Web vs 移动差异

**练习任务**:
- 列出 10 个不同点
- 理解各自的特点

---

### 8. 综合实践
**掌握程度**: Web+ 移动统一框架

**练习任务**:
- 复用代码结构
- 设计统一框架

---

## 本周练习任务

### 必做任务

1. **Android 应用测试**
```python
# 为一个 Android 应用编写 20 个自动化测试
# 例如：待办事项应用

# 测试内容:
# - 添加待办
# - 编辑待办
# - 删除待办
# - 标记完成

# 要求:
# - 使用 accessibilityId 定位
# - 失败自动截图
# - 生成测试报告
```

2. **Web vs 移动端对比**
```python
# 对比同一功能的 Web 和移动端测试脚本
# 例如：登录功能

# 要求:
# - 列出代码差异
# - 列出定位方式差异
# - 列出测试策略差异
```

3. **自动化测试框架设计文档**
```markdown
# 自动化测试框架设计

## 架构设计
- 分层结构
- 模块划分

## 技术选型
- Web 自动化：Playwright
- 接口自动化：requests + pytest
- 移动端自动化：Appium

## 代码复用
- 公共组件
- 工具函数

## 报告系统
- Allure 报告
- 自定义报告

## CI/CD 集成
- GitHub Actions
- Jenkins
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 移动端测试能跑通完整流程
- [ ] 能解释 Appium 的工作原理
- [ ] 输出《自动化测试框架设计》文档
- [ ] 能对比 Web 和移动端测试
- [ ] 阶段二总结：技术栈自评

---

## Appium 速查表

### 安装配置
```bash
# 安装 Appium
npm install -g appium

# 安装 Android SDK
# 下载：https://developer.android.com/studio#command-tools

# 配置环境变量
export ANDROID_HOME=~/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

### 启动 Appium Server
```bash
appium
```

### 基础脚本
```python
from appium import webdriver

caps = {
    'platformName': 'Android',
    'deviceName': 'emulator-5554',
    'appPackage': 'com.example.app',
    'appActivity': '.MainActivity',
    'automationName': 'UiAutomator2'
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)

# 查找元素
el = driver.find_element('accessibility id', 'login_button')
el.click()

# 输入文本
el = driver.find_element('xpath', '//android.widget.EditText')
el.send_keys('Hello')

driver.quit()
```

### 定位方式
```python
# accessibilityId（推荐）
driver.find_element('accessibility id', 'login_button')

# XPath
driver.find_element('xpath', '//android.widget.Button[@text="登录"]')

# uiautomator
driver.find_element('-android uiautomator', 'new UiSelector().text("登录")')

# className
driver.find_element('class name', 'android.widget.Button')

# id
driver.find_element('id', 'com.example.app:id/login_button')
```

### 手势操作
```python
from appium.webdriver.common.touch_action import TouchAction

# 点击
TouchAction(driver).tap(element).perform()

# 滑动
TouchAction(driver).press(x=100, y=500).move_to(x=100, y=200).release().perform()

# 长按
TouchAction(driver).long_press(element).perform()
```

### context 切换
```python
# 获取所有 context
contexts = driver.contexts

# 切换到 WebView
driver.switch_to.context('WEBVIEW_com.example.app')

# 切换回 Native
driver.switch_to.context('NATIVE_APP')
```

---

## 面试考点

### 高频面试题
1. Appium 的工作原理？
2. 移动端定位方式有哪些？
3. 如何处理弹窗？
4. 如何切换 WebView？
5. 移动端和 Web 测试的区别？
6. 如何处理不同分辨率？
7. 如何提高测试稳定性？

### 代码题
```python
# 1. 编写一个登录测试
def test_login(driver):
    driver.find_element('id', 'username').send_keys('test')
    driver.find_element('id', 'password').send_keys('pass')
    driver.find_element('id', 'login').click()
    assert 'home' in driver.current_activity

# 2. 处理 WebView 中的元素
```

---

## 每日学习检查清单

### Day 1-2: Appium 基础 + 环境
- [ ] 学习 Appium 原理
- [ ] 安装 Android SDK
- [ ] 配置模拟器
- [ ] 启动 Appium Server

### Day 3-4: 定位 + 手势
- [ ] 学习定位方式
- [ ] 学习手势操作
- [ ] 完成 10 个基础脚本
- [ ] GitHub 提交

### Day 5-6: 混合应用 + 对比
- [ ] 学习 WebView 处理
- [ ] 对比 Web 和移动端
- [ ] 完成 Android 测试
- [ ] 编写框架设计文档

### Day 7: 复习 + 总结
- [ ] 复习本周内容
- [ ] 阶段二总结
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 16 周总结

### 学习内容
- 掌握了 Appium 基础
- 学会了移动端测试
- 理解了自动化框架设计

### 作品
- Android 自动化测试
- 自动化测试框架设计文档

### 遇到的问题
- ...

### 阶段二总结
- UI 自动化：已掌握
- 接口自动化：已掌握
- Web 开发：待学习
- DevOps: 待学习

### 下周改进
- ...
```
