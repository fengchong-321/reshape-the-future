# 第 17 周 - HTML/CSS/JavaScript

## 学习目标
掌握 Web 前端三件套基础，能够独立实现静态页面和简单交互。

---

## 知识点清单

### 1. HTML 语义化
**掌握程度**: 标签含义、SEO、无障碍

**练习资源**:
- [MDN HTML 文档](https://developer.mozilla.org/zh-CN/docs/Web/HTML)
- [HTML 语义化](https://www.w3.org/TR/using-aria/)

**练习任务**:
- 理解常用 HTML 标签的语义
- 写语义化的 HTML 结构

---

### 2. 表单
**掌握程度**: input 类型、验证、无障碍

**练习任务**:
- 实现完整表单
- 理解表单验证

---

### 3. CSS 基础
**掌握程度**: 选择器、盒模型、继承

**练习资源**:
- [MDN CSS 文档](https://developer.mozilla.org/zh-CN/docs/Web/CSS)

**练习任务**:
- 理解盒模型
- 理解 CSS 继承和层叠

---

### 4. 布局
**掌握程度**: Flexbox、Grid

**练习任务**:
- 实现 Flexbox 布局
- 实现 Grid 布局
- 实现 3 种常见布局

---

### 5. 响应式
**掌握程度**: 媒体查询、移动优先

**练习任务**:
- 实现响应式页面
- 适配手机和桌面

---

### 6. JS 基础
**掌握程度**: 变量、函数、DOM 操作

**练习资源**:
- [MDN JavaScript 文档](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript)

**练习任务**:
- 理解变量声明（var/let/const）
- 理解函数声明

---

### 7. 事件
**掌握程度**: 监听、冒泡、委托

**练习任务**:
- 实现事件监听
- 理解事件冒泡
- 实现事件委托

---

### 8. 异步
**掌握程度**: Promise、async/await

**练习任务**:
- 理解 Promise
- 使用 async/await
- 调用 API

---

## 本周练习任务

### 必做任务

1. **静态页面（5 个）**
```
1. 个人简历页面
2. 产品展示页面
3. 博客列表页
4. 博客详情页
5. 联系表单页面

要求:
- HTML 语义化
- CSS 样式美观
- 响应式布局
- 通过 W3C 验证
```

2. **待办事项应用**
```javascript
// 实现一个纯前端待办事项应用
// 功能:
// - 添加待办
// - 标记完成
// - 删除待办
// - 过滤显示（全部/未完成/已完成）
// - 本地存储（localStorage）

// 要求:
// - 原生 JavaScript 实现
// - 代码结构清晰
```

3. **Lighthouse 优化**
```
// 使用 Chrome DevTools 的 Lighthouse 测试
// 目标:
// - Performance: 80+
// - Accessibility: 80+
// - Best Practices: 80+
// - SEO: 80+
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 5 个页面都能在手机和桌面正常显示
- [ ] 待办应用能增删改查
- [ ] Lighthouse 分数 80+
- [ ] 能解释盒模型
- [ ] 能解释事件委托

---

## HTML 速查表

### 常用标签
```html
<!-- 语义化标签 -->
<header>...</header>
<nav>...</nav>
<main>...</main>
<article>...</article>
<section>...</section>
<aside>...</aside>
<footer>...</footer>

<!-- 表单 -->
<form>
  <input type="text" name="username" required>
  <input type="email" name="email">
  <input type="password" name="password">
  <input type="checkbox" name="agree">
  <input type="radio" name="gender" value="male">
  <select name="country">
    <option value="cn">中国</option>
  </select>
  <textarea name="message"></textarea>
  <button type="submit">提交</button>
</form>
```

---

## CSS 速查表

### 选择器
```css
/* 元素选择器 */
p { color: red; }

/* 类选择器 */
.className { color: red; }

/* ID 选择器 */
#idName { color: red; }

/* 属性选择器 */
input[type="text"] { border: 1px solid #ccc; }

/* 伪类选择器 */
a:hover { color: blue; }
li:nth-child(odd) { background: #f0f0f0; }

/* 组合选择器 */
.parent .child { }
ul > li { }
h1 + p { }
```

### Flexbox
```css
.container {
  display: flex;
  justify-content: center;  /* 主轴对齐 */
  align-items: center;       /* 交叉轴对齐 */
  gap: 10px;                 /* 间距 */
}
```

### Grid
```css
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
```

### 响应式
```css
/* 移动优先 */
.container {
  padding: 10px;
}

/* 平板 */
@media (min-width: 768px) {
  .container {
    padding: 20px;
  }
}

/* 桌面 */
@media (min-width: 1024px) {
  .container {
    padding: 30px;
  }
}
```

---

## JavaScript 速查表

### DOM 操作
```javascript
// 获取元素
const el = document.querySelector('.class');
const els = document.querySelectorAll('li');

// 修改内容
el.textContent = 'Hello';
el.innerHTML = '<strong>Hello</strong>';

// 修改样式
el.style.color = 'red';
el.classList.add('active');
el.classList.remove('hidden');

// 创建元素
const newEl = document.createElement('div');
newEl.textContent = 'New';
el.appendChild(newEl);
```

### 事件监听
```javascript
// 添加事件监听
el.addEventListener('click', (e) => {
  console.log('clicked');
});

// 事件委托
document.querySelector('ul').addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    console.log('li clicked');
  }
});
```

### 异步
```javascript
// Promise
fetch('https://api.example.com/data')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

// async/await
async function fetchData() {
  try {
    const res = await fetch('https://api.example.com/data');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(err);
  }
}
```

---

## 面试考点

### 高频面试题
1. HTML 语义化的好处？
2. 盒模型的组成？
3. Flexbox 和 Grid 的区别？
4. 事件冒泡和捕获？
5. 事件委托的优势？
6. let/const/var 的区别？
7. Promise 的三种状态？
8. 什么是闭包？

### 代码题
```javascript
// 1. 实现事件委托
// 2. 用 fetch 获取数据并渲染
// 3. 实现一个响应式布局
```

---

## 每日学习检查清单

### Day 1-2: HTML + CSS 基础
- [ ] 学习 HTML 标签
- [ ] 学习 CSS 选择器
- [ ] 完成 2 个静态页面
- [ ] GitHub 提交

### Day 3-4: 布局 + 响应式
- [ ] 学习 Flexbox
- [ ] 学习 Grid
- [ ] 学习媒体查询
- [ ] 完成 3 个响应式页面

### Day 5-6: JavaScript
- [ ] 学习 JS 基础
- [ ] 学习 DOM 操作
- [ ] 学习事件
- [ ] 学习异步
- [ ] 完成待办应用

### Day 7: 复习
- [ ] 复习本周内容
- [ ] Lighthouse 测试
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 17 周总结

### 学习内容
- 掌握了 HTML/CSS/JS 基础
- 能实现静态页面
- 能实现简单交互

### 作品
- 5 个静态页面
- 待办事项应用

### 遇到的问题
- ...

### 下周改进
- ...
```
