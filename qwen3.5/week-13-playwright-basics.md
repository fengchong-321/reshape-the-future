# 第 13 周 - UI 自动化基础（Playwright）

## 学习目标
掌握 Playwright 测试框架的核心功能，能够编写 Web UI 自动化测试脚本。

---

## 知识点清单

### 1. 安装配置
**掌握程度**: playwright install、浏览器下载

**练习资源**:
- [Playwright 官方文档](https://playwright.dev/python/)
- [Playwright Python 入门](https://playwright.dev/python/docs/intro)

**练习任务**:
- 安装 Playwright
- 下载浏览器
- 运行示例脚本

---

### 2. 页面导航
**掌握程度**: goto、waitForURL、reload

**练习任务**:
- 打开页面
- 等待页面加载
- 刷新页面

---

### 3. 定位器
**掌握程度**: CSS/XPath/text/role/testid

**练习任务**:
- 用 5 种方式定位同一元素
- 理解优先使用 role 的原因

---

### 4. 元素操作
**掌握程度**: click/fill/check/select

**练习任务**:
- 点击按钮
- 填写表单
- 勾选复选框
- 选择下拉框

---

### 5. 断言
**掌握程度**: toHaveText/toBeVisible/toHaveAttribute

**练习任务**:
- 20 道断言练习
- 理解软断言和硬断言

---

### 6. 等待策略
**掌握程度**: waitForSelector/waitForTimeout

**练习任务**:
- 理解隐式等待和显式等待
- 实现智能等待

---

### 7. 弹窗处理
**掌握程度**: alert/confirm/prompt

**练习任务**:
- 处理 alert 弹窗
- 处理 confirm 弹窗
- 处理 prompt 弹窗

---

### 8. iframe
**掌握程度**: frameLocator、切换

**练习任务**:
- 定位 iframe 内元素
- 操作 iframe 内表单

---

## 本周练习任务

### 必做任务

1. **基础脚本练习（10 个场景）**
```python
# 为以下场景编写自动化脚本:
# 1. 打开百度并搜索关键词
# 2. 打开 GitHub 并查找仓库
# 3. 登录知乎
# 4. 填写并提交表单
# 5. 下拉选择
# 6. 文件上传
# 7. 文件下载
# 8. 截图
# 9. 录屏
# 10. 多标签页操作
```

2. **电商网站完整测试**
```python
# 实现一个完整的电商网站测试
# 流程:
# 1. 打开首页
# 2. 搜索商品
# 3. 浏览商品列表
# 4. 进入商品详情
# 5. 添加到购物车
# 6. 结算
# 7. 提交订单

# 要求:
# - 每个步骤都有断言
# - 失败自动截图
# - 生成测试报告
```

3. **定位器练习**
```python
# 对同一元素使用 5 种不同方式定位
# 1. CSS 选择器
# 2. XPath
# 3. text 定位
# 4. role 定位
# 5. testid 定位

# 对比各种方式的优缺点
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 20 个自动化脚本全部通过
- [ ] 能解释为什么优先用 role 定位
- [ ] GitHub 提交 `playwright-practice` 仓库
- [ ] 能处理常见的 UI 交互
- [ ] 能实现智能等待

---

## Playwright 速查表

### 安装和配置
```bash
# 安装
pip install playwright

# 下载浏览器
playwright install

# 下载所有浏览器（Chromium、Firefox、WebKit）
playwright install --all
```

### 基础脚本
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://example.com')
    print(page.title())
    browser.close()
```

### 定位器
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')

    # CSS 选择器
    page.locator('.btn-primary')

    # XPath
    page.locator('//button[@type="submit"]')

    # text 定位
    page.locator(text='登录')

    # role 定位（推荐）
    page.locator('button[role="button"]')
    page.get_by_role('button', name='提交')

    # testid 定位
    page.locator('[data-testid="submit-btn"]')

    browser.close()
```

### 元素操作
```python
# 点击
page.click('button')
page.locator('button').click()

# 填写输入框
page.fill('input[name="username"]', 'testuser')
page.type('input', 'text')  # 逐个字符输入

# 勾选复选框
page.check('input[type="checkbox"]')
page.uncheck('input[type="checkbox"]')

# 下拉选择
page.select_option('select', 'value')

# 获取文本
text = page.inner_text('.title')
html = page.inner_html('.content')
```

### 断言
```python
from playwright.sync_api import expect

# 文本断言
expect(page.locator('.title')).to_have_text('Welcome')

# 可见性断言
expect(page.locator('.modal')).to_be_visible()

# 属性断言
expect(page.locator('input')).to_have_attribute('type', 'text')

# 计数断言
expect(page.locator('li')).to_have_count(5)

# URL 断言
expect(page).to_have_url('https://example.com/home')
```

### 等待
```python
# 等待元素出现
page.wait_for_selector('.loaded')

# 等待导航完成
page.wait_for_url('**/home')

# 等待网络请求
page.wait_for_response('**/api/data')

# 固定等待（不推荐）
page.wait_for_timeout(1000)
```

### 弹窗处理
```python
# 处理 alert
page.on('dialog', lambda dialog: dialog.accept())
page.click('.alert-btn')

# 处理 confirm
page.on('dialog', lambda dialog: dialog.accept() if dialog.message == '确认？' else dialog.dismiss())

# 处理 prompt
page.on('dialog', lambda dialog: dialog.accept('输入内容'))
```

### iframe 处理
```python
# 定位 iframe
frame = page.frame_locator('iframe[name="content"]')

# 操作 iframe 内元素
frame.locator('button').click()
frame.fill('input', 'text')
```

### 截图和录屏
```python
# 截图
page.screenshot(path='screenshot.png')
page.locator('.element').screenshot(path='element.png')

# 录屏（需要配置）
context = browser.new_context(record_video_dir='videos/')
page = context.new_page()
# ... 操作 ...
context.close()
```

---

## 面试考点

### 高频面试题
1. Playwright 和 Selenium 的区别？
2. 什么是智能等待？如何实现？
3. 为什么优先使用 role 定位？
4. 如何处理 iframe？
5. 如何处理弹窗？
6. 如何实现失败自动截图？
7. 什么是 Page Object Model？

### 代码题
```python
# 1. 编写一个登录测试
def test_login(page):
    page.goto('https://example.com/login')
    page.fill('input[name="username"]', 'test')
    page.fill('input[name="password"]', 'password')
    page.click('button[type="submit"]')
    expect(page).to_have_url('**/home')

# 2. 处理动态加载的内容
```

---

## 每日学习检查清单

### Day 1-2: 安装 + 基础
- [ ] 安装 Playwright
- [ ] 学习页面导航
- [ ] 学习定位器
- [ ] 完成 5 个基础脚本

### Day 3-4: 元素操作 + 断言
- [ ] 学习元素操作
- [ ] 学习断言
- [ ] 完成 10 个断言练习
- [ ] GitHub 提交

### Day 5-6: 等待 + 弹窗 + iframe
- [ ] 学习等待策略
- [ ] 学习弹窗处理
- [ ] 学习 iframe 处理
- [ ] 完成电商网站测试

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成剩余脚本
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 13 周总结

### 学习内容
- 掌握了 Playwright 基础
- 能编写 UI 自动化脚本
- 理解了智能等待

### 作品
- 基础脚本 10 个
- 电商网站完整测试

### 遇到的问题
- ...

### 下周改进
- ...
```
