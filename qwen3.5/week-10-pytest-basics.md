# 第 10 周 - pytest 基础

## 学习目标
掌握 pytest 测试框架的核心功能，能够编写单元测试、使用 fixture、参数化测试、生成覆盖率报告。

---

## 知识点清单

### 1. 安装运行
**掌握程度**: pytest 安装、命令行参数

**练习资源**:
- [pytest 官方文档](https://docs.pytest.org/)
- [pytest 入门教程](https://docs.pytest.org/en/stable/getting-started.html)

**练习任务**:
- 安装 pytest
- 运行测试
- 理解命令行参数

---

### 2. 命名约定
**掌握程度**: test_*.py、test_* 函数

**练习任务**:
- 遵循 pytest 命名约定
- 理解为什么需要约定

---

### 3. 断言
**掌握程度**: assert、pytest.raises

**练习任务**:
- 20 道断言练习
- 测试异常抛出

---

### 4. fixture
**掌握程度**: @pytest.fixture、作用域

**练习任务**:
- 实现 setup/teardown
- 理解 fixture 的作用域（function/class/module/session）

---

### 5. parametrize
**掌握程度**: 参数化测试

**练习任务**:
- 参数化 10 个用例
- 理解参数化的优势

---

### 6. 标记
**掌握程度**: @pytest.mark、skip/xfail

**练习任务**:
- 分类测试用例
- 跳过测试
- 标记预期失败的测试

---

### 7. conftest.py
**掌握程度**: 共享 fixture

**练习任务**:
- 创建 conftest.py
- 在多个测试文件中共享 fixture

---

### 8. 覆盖率
**掌握程度**: pytest-cov、报告解读

**练习资源**:
- [pytest-cov 文档](https://pytest-cov.readthedocs.io/)

**练习任务**:
- 安装 pytest-cov
- 生成覆盖率报告
- 解读报告

---

## 本周练习任务

### 必做任务

1. **计算器模块测试**
```python
# 为一个计算器模块编写完整测试
# 功能:
# - 加法
# - 减法
# - 乘法
# - 除法
# - 边界情况（除零、负数等）

# 要求:
# - 至少 50 个测试用例
# - 使用参数化
# - 使用 fixture
# - 覆盖率 80%+
```

2. **字符串处理函数测试**
```python
# 为一组字符串处理函数编写测试
# 函数包括:
# - reverse_string(s)
# - is_palindrome(s)
# - count_vowels(s)
# - capitalize_words(s)

# 要求:
# - 参数化测试
# - 边界条件测试
```

3. **自定义 fixture**
```python
# 实现以下 fixture:
# 1. 数据库连接 fixture
# 2. 临时文件 fixture
# 3. 用户认证 fixture
```

4. **覆盖率报告**
```bash
# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 目标：覆盖率 80%+
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 50 个测试用例全部通过
- [ ] 测试覆盖率报告 80%+
- [ ] 能解释 fixture 的执行顺序
- [ ] 能使用参数化编写测试
- [ ] 能生成覆盖率报告

---

## pytest 速查表

### 安装和运行
```bash
pip install pytest pytest-cov

# 运行测试
pytest
pytest test_file.py
pytest test_file.py::test_function
pytest tests/

# 详细输出
pytest -v
pytest -v -s

# 覆盖率
pytest --cov=src --cov-report=html
```

### 断言
```python
def test_assertion():
    assert 1 + 1 == 2
    assert [1, 2] == [1, 2]
    assert {'a': 1} == {'a': 1}

def test_exception():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

### fixture
```python
import pytest

@pytest.fixture
def sample_data():
    return {'name': 'test', 'value': 42}

def test_with_fixture(sample_data):
    assert sample_data['name'] == 'test'

@pytest.fixture(scope='module')
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

### 参数化
```python
import pytest

@pytest.mark.parametrize('input,expected', [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### 标记
```python
import pytest

@pytest.mark.skip(reason='not implemented')
def test_skip():
    pass

@pytest.mark.xfail(reason='known bug')
def test_expected_fail():
    pass

@pytest.mark.slow
def test_slow():
    pass

# 运行特定标记
pytest -m slow
```

### conftest.py
```python
# conftest.py
import pytest

@pytest.fixture
def db():
    # 在所有测试文件中可用
    return create_db()
```

---

## 面试考点

### 高频面试题
1. pytest 和 unittest 的区别？
2. fixture 的作用域有哪些？
3. 参数化测试的优势？
4. conftest.py 的作用？
5. 如何跳过测试？
6. 覆盖率多少算合格？
7. 如何测试异常？

### 代码题
```python
# 1. 为以下函数编写测试
def add(a, b):
    return a + b

# 2. 使用 fixture 模拟数据库连接
# 3. 参数化测试多个输入
```

---

## 每日学习检查清单

### Day 1-2: 基础 + 断言
- [ ] 安装 pytest
- [ ] 学习命名约定
- [ ] 学习断言
- [ ] 完成 10 道断言练习

### Day 3-4: fixture
- [ ] 学习 fixture
- [ ] 理解作用域
- [ ] 创建自定义 fixture
- [ ] GitHub 提交

### Day 5-6: 参数化 + 标记 + 覆盖率
- [ ] 学习参数化
- [ ] 学习标记
- [ ] 生成覆盖率报告
- [ ] 完成计算器测试

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成剩余测试
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 10 周总结

### 学习内容
- 掌握了 pytest 基础
- 学会了 fixture 和参数化
- 能生成覆盖率报告

### 作品
- 计算器模块测试（50 个用例）
- 字符串函数测试

### 覆盖率
- 覆盖率：XX%

### 遇到的问题
- ...

### 下周改进
- ...
```
