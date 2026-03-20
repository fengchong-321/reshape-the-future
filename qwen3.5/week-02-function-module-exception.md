# 第 2 周 - 函数 + 模块 + 异常

## 学习目标
掌握 Python 函数定义、模块管理、包使用和异常处理，能够编写结构良好的代码。

---

## 知识点清单

### 1. 函数定义
**掌握程度**: 理解参数传递（位置/关键字/默认/*args/**kwargs）

**练习资源**:
- [Python 函数文档](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)

**练习任务**:
- 编写 10 个不同参数类型的函数
- 解释"可变默认参数陷阱"并写出正确写法

---

### 2. 作用域
**掌握程度**: LEGB 规则、global/nonlocal

**练习资源**:
- [Python 作用域规则](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)

**练习任务**:
- 5 道作用域练习题（预测变量查找结果）
- 编写示例演示 global 和 nonlocal 的区别

---

### 3. 返回值
**掌握程度**: 单值/多值返回、None 处理

**练习任务**:
- 5 道返回值练习题
- 实现一个多返回值函数（如：同时返回最大值和最小值）

---

### 4. Lambda
**掌握程度**: 理解匿名函数使用场景

**练习任务**:
- 用 lambda 改写 5 个普通函数
- 理解 map/filter/sorted 中 lambda 的使用

---

### 5. 模块导入
**掌握程度**: import/from...import/别名、循环导入问题

**练习资源**:
- [Python 模块文档](https://docs.python.org/3/tutorial/modules.html)

**练习任务**:
- 创建一个包含 5 个函数的模块
- 在另一个文件中导入并使用
- 画出模块导入流程图

---

### 6. 包管理
**掌握程度**: pip、requirements.txt、虚拟环境

**练习资源**:
- [pip 官方文档](https://pip.pypa.io/en/stable/)
- [venv 文档](https://docs.python.org/3/library/venv.html)

**练习任务**:
- 创建虚拟环境
- 安装 3 个第三方包（如 requests、pytest、black）
- 生成 requirements.txt

---

### 7. 异常处理
**掌握程度**: try/except/else/finally、自定义异常

**练习资源**:
- [Python 异常处理文档](https://docs.python.org/3/tutorial/errors.html)

**练习任务**:
- 10 道异常处理练习题
- 实现一个自定义异常类
- 编写一个带完整异常处理的程序

---

## 本周练习任务

### 必做任务

1. **计算器模块**
```python
# 实现一个计算器，支持加减乘除
# 要求:
# - 处理除零异常
# - 处理类型错误
# - 支持链式调用
# - 记录计算历史
```

2. **文件处理工具**
```python
# 实现一个文件处理工具
# 功能:
# - 读取文件内容
# - 解析 JSON/YAML
# - 统计行数、词数
# - 处理文件不存在的异常
```

3. **LeetCode**: 20 道函数相关题目

4. **GitHub 提交**: 至少 15 次提交

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 计算器模块通过 20 个测试用例
- [ ] 能口头解释"可变默认参数为什么危险"
- [ ] GitHub 提交记录 15+
- [ ] 能解释 LEGB 规则
- [ ] 能编写自定义异常类
- [ ] 能使用虚拟环境管理依赖

---

## 面试考点

### 高频面试题
1. Python 函数参数传递是值传递还是引用传递？
2. *args 和 **kwargs 的区别？
3. 什么是闭包？举例说明
4. @decorator 的作用和实现原理？
5. try/except/else/finally 的执行顺序？

### 代码题
```python
# 1. 写出以下代码的输出
def func(a, b=[]):
    b.append(a)
    return b

print(func(1))
print(func(2))
print(func(3))

# 2. 改写为正确写法
```

---

## 每日学习检查清单

### Day 1-2: 函数
- [ ] 学习函数定义和参数传递
- [ ] 完成 10 道函数练习题
- [ ] GitHub 提交
- [ ] 写学习笔记

### Day 3: 作用域 + Lambda
- [ ] 学习 LEGB 规则
- [ ] 完成 5 道作用域题
- [ ] 学习 lambda 使用
- [ ] GitHub 提交

### Day 4-5: 模块 + 包管理
- [ ] 学习模块导入
- [ ] 创建虚拟环境
- [ ] 安装第三方包
- [ ] GitHub 提交

### Day 6-7: 异常处理 + 复习
- [ ] 学习异常处理
- [ ] 完成 10 道异常题
- [ ] 编写完整项目
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 2 周总结

### 学习内容
- 掌握了函数参数传递的各种方式
- 理解了作用域规则
- 学会了异常处理

### 遇到的问题
- 可变默认参数陷阱（已解决）
- 循环导入问题（已解决）

### GitHub 提交
- 提交次数: XX 次
- 仓库链接：...

### 代码示例
```python
# 记录学到的重要代码片段
```

### 下周改进
- ...
```
