# 第 11 周 - pytest 进阶

## 学习目标
掌握 pytest 的高级功能，能够开发 pytest 插件、使用 mock 测试、并行执行测试、集成 CI/CD。

---

## 知识点清单

### 1. fixture 进阶
**掌握程度**: 依赖、yield、autouse

**练习资源**:
- [pytest fixture 文档](https://docs.pytest.org/en/stable/fixtures.html)

**练习任务**:
- 实现 fixture 依赖
- 使用 yield 进行 teardown
- 实现 autouse fixture

---

### 2. mock
**掌握程度**: unittest.mock、patch

**练习资源**:
- [unittest.mock 文档](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-mock 文档](https://pytest-mock.readthedocs.io/)

**练习任务**:
- 模拟外部 API 调用
- 模拟数据库操作
- 模拟文件系统操作

---

### 3. 插件开发
**掌握程度**: pytest_plugins、hook

**练习资源**:
- [pytest 插件开发文档](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)

**练习任务**:
- 开发一个简单的 pytest 插件
- 实现自定义命令行参数
- 实现自定义 hook

---

### 4. 并行执行
**掌握程度**: pytest-xdist

**练习资源**:
- [pytest-xdist 文档](https://pytest-xdist.readthedocs.io/)

**练习任务**:
- 安装 pytest-xdist
- 并行执行测试
- 理解并行测试的注意事项

---

### 5. 测试数据
**掌握程度**: Faker、数据工厂

**练习资源**:
- [Faker 文档](https://faker.readthedocs.io/)

**练习任务**:
- 使用 Faker 生成测试数据
- 实现数据工厂模式

---

### 6. 报告
**掌握程度**: pytest-html、allure

**练习资源**:
- [pytest-html 文档](https://github.com/pytest-dev/pytest-html)
- [Allure 文档](https://docs.qameta.io/allure/)

**练习任务**:
- 生成 HTML 报告
- 集成 Allure
- 美化测试报告

---

### 7. CI 集成
**掌握程度**: GitHub Actions 运行测试

**练习资源**:
- [GitHub Actions 文档](https://docs.github.com/en/actions)

**练习任务**:
- 配置 GitHub Actions
- 自动运行测试
- 上传覆盖率报告

---

### 8. 最佳实践
**掌握程度**: 测试组织、命名、隔离

**练习任务**:
- 遵循测试最佳实践
- 保持测试独立
- 理解测试设计模式

---

## 本周练习任务

### 必做任务

1. **API 客户端测试（含 mock）**
```python
# 为一个 API 客户端编写完整测试
# 要求:
# - mock 外部 API 调用
# - 测试成功场景
# - 测试失败场景
# - 测试超时场景
# - 覆盖率 90%+
```

2. **pytest 插件开发**
```python
# 开发一个 pytest 插件
# 功能示例:
# - 自动截图（测试失败时）
# - 自定义标记
# - 自定义报告

# 要求:
# - 插件能正常工作
# - 能被其他项目使用
# - 发布到 PyPI（可选）
```

3. **GitHub Actions 集成**
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

4. **Allure 报告集成**
```bash
# 安装
pip install allure-pytest

# 运行并生成报告
pytest --alluredir=./allure-results
allure generate ./allure-results --clean -o ./allure-report
allure serve ./allure-results
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] API 测试覆盖率 90%+
- [ ] 插件能正常工作并被其他项目使用
- [ ] GitHub Actions 绿色通过
- [ ] 能解释 mock 的工作原理
- [ ] 能生成 Allure 报告
- [ ] 博客：《pytest 插件开发实践》

---

## pytest 进阶速查表

### fixture 进阶
```python
import pytest

# fixture 依赖
@pytest.fixture
def db():
    return Database()

@pytest.fixture
def client(db):
    return Client(db)

# yield fixture
@pytest.fixture
def temp_file():
    f = tempfile.NamedTemporaryFile()
    yield f
    f.close()

# autouse fixture
@pytest.fixture(autouse=True)
def setup_db():
    setup_database()
    yield
    teardown_database()
```

### mock
```python
from unittest.mock import Mock, patch
import pytest

# 使用 Mock
def test_with_mock():
    mock_api = Mock()
    mock_api.get.return_value = {'status': 'ok'}
    result = call_api(mock_api)
    assert result == 'success'
    mock_api.get.assert_called_once()

# 使用 patch
@patch('module.api_call')
def test_with_patch(mock_api):
    mock_api.return_value = {'status': 'ok'}
    result = function_under_test()
    assert result == 'success'

# 使用 pytest-mock
def test_with_fixture_mock(mocker):
    mocker.patch('module.api_call', return_value={'status': 'ok'})
```

### 并行执行
```bash
# 安装
pip install pytest-xdist

# 运行（使用所有 CPU 核心）
pytest -n auto

# 运行（指定进程数）
pytest -n 4
```

### 测试数据生成
```python
from faker import Faker

fake = Faker()

@pytest.fixture
def user_data():
    return {
        'name': fake.name(),
        'email': fake.email(),
        'address': fake.address()
    }
```

---

## 面试考点

### 高频面试题
1. 什么是 mock？为什么需要 mock？
2. pytest 插件如何开发？
3. 如何并行执行测试？
4. 如何测试异步代码？
5. 如何测试依赖外部服务的代码？
6. Allure 报告的优势？
7. CI/CD 中如何配置测试？

### 代码题
```python
# 1. 为以下代码编写测试（使用 mock）
class UserService:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_user(self, user_id):
        response = self.api_client.get(f'/users/{user_id}')
        return response.json()

# 2. 开发一个 pytest 插件，记录每个测试的执行时间
```

---

## 每日学习检查清单

### Day 1-2: fixture 进阶 + mock
- [ ] 学习 fixture 依赖
- [ ] 学习 yield fixture
- [ ] 学习 mock
- [ ] 完成 API 客户端测试

### Day 3-4: 插件开发
- [ ] 学习插件开发
- [ ] 实现自定义 hook
- [ ] 开发 pytest 插件
- [ ] 写博客

### Day 5-6: 并行 + 报告 + CI
- [ ] 学习 pytest-xdist
- [ ] 学习 Allure 报告
- [ ] 配置 GitHub Actions
- [ ] 上传覆盖率

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成项目
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 11 周总结

### 学习内容
- 掌握了 pytest 进阶
- 学会了 mock 测试
- 能开发 pytest 插件

### 作品
- API 客户端测试
- pytest 插件
- GitHub Actions 配置

### 遇到的问题
- ...

### 下周改进
- ...
```
