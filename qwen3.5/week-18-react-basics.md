# 第 18 周 - React 基础

## 学习目标
掌握 React 基础概念，能够使用 React 编写组件和实现简单应用。

---

## 知识点清单

### 1. JSX 语法
**掌握程度**: 表达式、条件、列表

**练习资源**:
- [React 官方文档](https://react.dev/)
- [React 入门教程](https://react.dev/learn)

**练习任务**:
- 理解 JSX 和 HTML 的区别
- 在 JSX 中使用表达式
- 条件渲染
- 列表渲染

---

### 2. 组件
**掌握程度**: 函数组件、props

**练习任务**:
- 编写函数组件
- 理解 props 传递
- 拆分组件

---

### 3. 状态
**掌握程度**: useState、状态提升

**练习任务**:
- 使用 useState 管理状态
- 理解状态提升

---

### 4. 副作用
**掌握程度**: useEffect、清理

**练习任务**:
- 使用 useEffect 处理副作用
- 理解依赖数组
- 实现清理函数

---

### 5. 表单
**掌握程度**: 受控组件、验证

**练习任务**:
- 实现受控组件
- 实现表单验证

---

### 6. 路由
**掌握程度**: React Router、导航

**练习资源**:
- [React Router 文档](https://reactrouter.com/)

**练习任务**:
- 配置路由
- 实现页面跳转
- 实现参数传递

---

### 7. 状态管理
**掌握程度**: Context、useReducer

**练习任务**:
- 使用 Context 共享状态
- 使用 useReducer 管理复杂状态

---

### 8. 自定义 Hook
**掌握程度**: 逻辑复用

**练习任务**:
- 提取自定义 Hook
- 理解 Hook 使用规则

---

## 本周练习任务

### 必做任务

1. **博客系统前端**
```
功能:
- 文章列表页
- 文章详情页
- 文章发布页
- 文章编辑页

要求:
- 使用 React Router
- 组件拆分合理
- 代码通过 ESLint
```

2. **Dashboard 应用**
```
功能:
- 数据图表展示
- 数据表格
- 过滤和搜索
- 分页

要求:
- 使用 Context 管理状态
- 使用自定义 Hook
- 响应式布局
```

3. **ESLint 配置**
```javascript
// .eslintrc.js
module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
  },
  plugins: ['react'],
  rules: {
    // 自定义规则
  },
};
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 两个应用都能正常运行
- [ ] 组件拆分合理（单文件<200 行）
- [ ] 博客：《React 核心概念整理》
- [ ] 能解释 useState 和 useReducer 的区别
- [ ] 能解释 useEffect 的执行时机

---

## React 速查表

### 创建项目
```bash
# 使用 Vite（推荐）
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev

# 或使用 Create React App
npx create-react-app my-app
```

### 基础组件
```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加
      </button>
    </div>
  );
}
```

### Props
```jsx
function Welcome({ name, age }) {
  return <h1>Hello, {name}. You are {age} years old.</h1>;
}

// 使用
<Welcome name="Alice" age={25} />
```

### useEffect
```jsx
import { useState, useEffect } from 'react';

function Example() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData().then(setData);

    // 清理函数
    return () => {
      cleanup();
    };
  }, []); // 依赖数组

  return <div>{data}</div>;
}
```

### React Router
```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/user/:id" element={<User />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Context
```jsx
import { createContext, useContext } from 'react';

const ThemeContext = createContext();

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  const theme = useContext(ThemeContext);
  return <div>Theme: {theme}</div>;
}
```

### 自定义 Hook
```jsx
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      });
  }, [url]);

  return { data, loading };
}

// 使用
function UserProfile() {
  const { data, loading } = useFetch('/api/user');
  // ...
}
```

---

## 面试考点

### 高频面试题
1. React 的优势？
2. 虚拟 DOM 是什么？
3. useState 和 useReducer 的区别？
4. useEffect 的执行时机？
5. 什么是受控组件？
6. 什么是 keys？为什么需要？
7. 什么是高阶组件？
8. Context 的适用场景？

### 代码题
```jsx
// 1. 实现一个计数器
// 2. 实现一个表单组件
// 3. 实现一个数据获取组件
```

---

## 每日学习检查清单

### Day 1-2: JSX + 组件
- [ ] 学习 JSX 语法
- [ ] 学习组件和 props
- [ ] 完成基础组件练习
- [ ] GitHub 提交

### Day 3-4: 状态 + 副作用
- [ ] 学习 useState
- [ ] 学习 useEffect
- [ ] 完成计数器应用
- [ ] GitHub 提交

### Day 5-6: 路由 + Context
- [ ] 学习 React Router
- [ ] 学习 Context
- [ ] 学习自定义 Hook
- [ ] 完成博客系统

### Day 7: 复习 + 博客
- [ ] 复习本周内容
- [ ] 写博客《React 核心概念》
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 18 周总结

### 学习内容
- 掌握了 React 基础
- 能编写组件
- 能实现简单应用

### 作品
- 博客系统前端
- Dashboard 应用

### 遇到的问题
- ...

### 下周改进
- ...
```
