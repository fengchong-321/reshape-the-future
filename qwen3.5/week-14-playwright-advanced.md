# 第 14 周 - UI 自动化进阶

## 学习目标
掌握 Playwright 的高级功能，能够使用 POM 模式组织代码、实现数据驱动测试、配置失败自动截图。

---

## 知识点清单

### 1. POM 模式
**掌握程度**: Page Object Model 设计

**练习资源**:
- [Page Object Model](https://playwright.dev/python/docs/pom)

**练习任务**:
- 用 POM 重构现有脚本
- 理解 POM 的优势

---

### 2. 数据驱动
**掌握程度**: Excel/CSV/YAML 数据源

**练习任务**:
- 从 YAML 读取测试数据
- 实现数据驱动测试

---

### 3. 截图录屏
**掌握程度**: 失败自动截图、全程录屏

**练习任务**:
- 配置失败自动截图
- 配置全程录屏
- 管理截图和录像文件

---

### 4. 浏览器上下文
**掌握程度**: 多用户场景、隔离

**练习任务**:
- 创建多个浏览器上下文
- 模拟多用户场景

---

### 5. 移动端模拟
**掌握程度**: 视口、userAgent、触摸

**练习任务**:
- 模拟手机浏览器
- 模拟平板浏览器
- 测试响应式布局

---

### 6. 网络拦截
**掌握程度**: route、mock 响应

**练习任务**:
- 拦截请求
- mock 响应数据
- 模拟慢网络

---

### 7. 文件处理
**掌握程度**: 下载/上传、路径配置

**练习任务**:
- 处理文件下载
- 处理文件上传
- 配置文件下载路径

---

### 8. 认证处理
**掌握程度**: cookie/storageState

**练习任务**:
- 保存登录状态
- 复用登录状态
- 跳过登录步骤

---

## 本周练习任务

### 必做任务

1. **POM 重构**
```python
# 用 POM 模式重构第 13 周的电商测试
# 要求:
# - 每个页面一个 Page 类
# - 页面元素和方法分离
# - 测试代码只调用 Page 方法
# - 代码行数减少 30%

# 示例结构:
# pages/
#   base_page.py
#   home_page.py
#   product_page.py
#   cart_page.py
# tests/
#   test_checkout.py
```

2. **数据驱动测试**
```python
# 实现数据驱动测试
# 从 YAML 读取测试数据:
# test_data.yaml:
#   login_tests:
#     - username: test1
#       password: pass1
#       expected: success
#     - username: test2
#       password: wrong
#       expected: failure

# 要求:
# - 能运行 20+ 用例
# - 失败用例有详细报告
```

3. **失败自动截图**
```python
# 配置失败自动截图
# 要求:
# - 测试失败时自动截图
# - 截图包含时间戳
# - 截图保存到指定目录
```

4. **多用户场景测试**
```python
# 模拟多用户场景
# 例如:
# - 用户 A 添加商品到购物车
# - 用户 B 同时浏览同一商品
# - 验证库存变化

# 要求:
# - 使用多个浏览器上下文
# - 数据隔离
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] POM 重构后代码行数减少 30%
- [ ] 数据驱动测试能运行 20+ 用例
- [ ] 博客：《Playwright POM 模式实践》
- [ ] 能配置失败自动截图
- [ ] 能模拟多用户场景

---

## POM 模式示例

### Page 基类
```python
# pages/base_page.py
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url):
        self.page.goto(url)

    def wait_for_element(self, selector, timeout=5000):
        return self.page.wait_for_selector(selector, timeout=timeout)
```

### 首页 Page
```python
# pages/home_page.py
from playwright.sync_api import expect
from .base_page import BasePage

class HomePage(BasePage):
    URL = 'https://example.com'

    # 定位器
    LOGIN_BUTTON = 'a[href="/login"]'
    SEARCH_INPUT = 'input[name="q"]'

    def open(self):
        self.goto(self.URL)

    def search(self, keyword):
        self.page.fill(self.SEARCH_INPUT, keyword)
        self.page.press(self.SEARCH_INPUT, 'Enter')
        return SearchResultsPage(self.page)

    def click_login(self):
        self.page.click(self.LOGIN_BUTTON)
        return LoginPage(self.page)
```

### 测试代码
```python
# tests/test_search.py
import pytest
from pages.home_page import HomePage

@pytest.fixture
def home_page(page):
    home = HomePage(page)
    home.open()
    return home

def test_search(home_page):
    results = home_page.search('laptop')
    assert results.get_count() > 0
```

---

## 数据驱动测试

### YAML 数据文件
```yaml
# test_data.yaml
login_tests:
  - username: test1
    password: pass1
    expected: success
    description: 正确密码
  - username: test1
    password: wrong
    expected: failure
    description: 错误密码
  - username: ''
    password: pass1
    expected: failure
    description: 用户名为空
```

### 读取数据
```python
# tests/test_login.py
import pytest
import yaml
from pages.login_page import LoginPage

with open('test_data.yaml') as f:
    test_data = yaml.safe_load(f)

@pytest.mark.parametrize('data', test_data['login_tests'])
def test_login(login_page, data):
    result = login_page.login(data['username'], data['password'])
    if data['expected'] == 'success':
        assert result.is_logged_in()
    else:
        assert result.has_error()
```

---

## 面试考点

### 高频面试题
1. POM 模式的优势？
2. 如何实现数据驱动测试？
3. 如何处理测试失败后的截图？
4. 如何模拟多用户场景？
5. 如何 mock 网络请求？
6. 如何保存和复用登录状态？
7. 如何测试响应式布局？

### 代码题
```python
# 1. 用 POM 模式设计一个登录页面
class LoginPage:
    # 实现...
    pass

# 2. 实现数据驱动测试
# 从 CSV 文件读取测试数据
```

---

## 每日学习检查清单

### Day 1-2: POM 模式
- [ ] 学习 POM 概念
- [ ] 设计 Page 类
- [ ] 重构现有代码
- [ ] GitHub 提交

### Day 3-4: 数据驱动 + 截图录屏
- [ ] 学习数据驱动
- [ ] 创建 YAML 数据文件
- [ ] 配置失败截图
- [ ] GitHub 提交

### Day 5-6: 多用户 + 网络拦截 + 认证
- [ ] 学习浏览器上下文
- [ ] 学习网络拦截
- [ ] 学习认证处理
- [ ] 完成多用户测试

### Day 7: 复习 + 博客
- [ ] 复习本周内容
- [ ] 写博客《Playwright POM 模式实践》
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 14 周总结

### 学习内容
- 掌握了 POM 模式
- 学会了数据驱动测试
- 能配置失败截图

### 作品
- POM 重构项目
- 数据驱动测试

### 遇到的问题
- ...

### 下周改进
- ...
```
