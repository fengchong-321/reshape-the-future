# 第2周：面向对象编程与异常处理

## 本周目标

掌握 Python 面向对象编程，能设计和封装测试工具类；熟练使用异常处理机制。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| 类与对象 | 定义类、实例化、`__init__` | ⭐⭐⭐⭐⭐ |
| 实例方法与属性 | self、实例变量、类变量 | ⭐⭐⭐⭐⭐ |
| 继承 | 单继承、super()、方法重写 | ⭐⭐⭐⭐⭐ |
| 多态与封装 | 抽象类、私有属性、property | ⭐⭐⭐⭐ |
| 魔术方法 | `__str__`、`__repr__`、`__eq__` | ⭐⭐⭐ |
| 异常处理 | try/except/finally、自定义异常 | ⭐⭐⭐⭐⭐ |
| 上下文管理器 | with 语句、`__enter__`/`__exit__` | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 类与对象基础

面向对象编程（OOP）是组织代码的核心方式，测试框架（如 Pytest）大量使用 OOP。

```python
# ============================================
# 类的定义
# ============================================
class TestCase:
    """测试用例类 - 类文档字符串"""

    # 类变量 - 所有实例共享
    total_count = 0

    # 构造方法 - 创建实例时自动调用
    def __init__(self, name, priority="P1"):
        # 实例变量 - 每个实例独立
        self.name = name
        self.priority = priority
        self.status = None  # 初始状态
        self.duration = 0

        # 创建实例时计数
        TestCase.total_count += 1

    # 实例方法 - 第一个参数是 self
    def run(self):
        """执行测试用例"""
        print(f"执行测试: {self.name}")
        # 模拟执行
        import time
        time.sleep(0.1)
        self.status = "pass"
        self.duration = 0.1
        return self.status

    def get_info(self):
        """获取用例信息"""
        return {
            "name": self.name,
            "priority": self.priority,
            "status": self.status,
            "duration": self.duration
        }


# ============================================
# 创建实例（对象）
# ============================================
# 实例化 - 自动调用 __init__
case1 = TestCase("登录测试", "P0")
case2 = TestCase("搜索测试", "P1")

# 访问实例变量
print(case1.name)       # "登录测试"
print(case2.priority)   # "P1"

# 调用实例方法
case1.run()
print(case1.status)     # "pass"

# 访问类变量
print(TestCase.total_count)  # 2
print(case1.total_count)     # 2（通过实例也能访问）

# ============================================
# 类变量 vs 实例变量（重要陷阱）
# ============================================
class Counter:
    count = 0  # 类变量

    def __init__(self):
        self.count = 0  # 实例变量（同名会覆盖类变量）

c1 = Counter()
c2 = Counter()

c1.count = 10  # 修改的是实例变量
print(c1.count)  # 10
print(c2.count)  # 0（未受影响）
print(Counter.count)  # 0（类变量未变）

# 正确修改类变量
Counter.count = 100
```

---

### 2.2 方法类型

```python
class TestSuite:
    """测试套件示例"""

    # 类变量
    version = "1.0"

    def __init__(self, name):
        self.name = name
        self.cases = []

    # ============================================
    # 实例方法 - 最常用
    # ============================================
    def add_case(self, case):
        """添加测试用例"""
        self.cases.append(case)

    def run_all(self):
        """运行所有用例"""
        results = []
        for case in self.cases:
            results.append(case.run())
        return results

    # ============================================
    # 类方法 - 操作类级别的数据
    # ============================================
    @classmethod
    def from_file(cls, filepath):
        """从文件创建测试套件（工厂方法）"""
        # cls 指向类本身（不是实例）
        import json
        with open(filepath) as f:
            data = json.load(f)

        suite = cls(data["name"])  # 调用当前类的构造方法
        for case_data in data["cases"]:
            suite.add_case(case_data)
        return suite

    @classmethod
    def get_version(cls):
        """获取版本号"""
        return cls.version

    # ============================================
    # 静态方法 - 与类相关但不需要访问类/实例
    # ============================================
    @staticmethod
    def validate_case_name(name):
        """验证用例名是否合法"""
        if not name:
            return False
        if len(name) > 100:
            return False
        return True


# 使用示例
suite = TestSuite("冒烟测试")
suite.add_case("登录测试")

# 类方法调用
suite2 = TestSuite.from_file("suite.json")  # 工厂方法
print(TestSuite.get_version())  # "1.0"

# 静态方法调用
TestSuite.validate_case_name("登录")  # True
```

---

### 2.3 继承

继承是代码复用的核心机制，测试框架中大量使用继承。

```python
# ============================================
# 基类（父类）
# ============================================
class BaseTest:
    """测试基类 - 包含通用功能"""

    def __init__(self, name):
        self.name = name
        self.result = None

    def setup(self):
        """前置操作 - 子类可重写"""
        print(f"[{self.name}] 初始化测试环境")

    def teardown(self):
        """后置操作 - 子类可重写"""
        print(f"[{self.name}] 清理测试环境")

    def run(self):
        """运行测试 - 模板方法"""
        try:
            self.setup()
            self.result = self.test()  # 调用子类实现
            self.teardown()
            return self.result
        except Exception as e:
            print(f"测试失败: {e}")
            self.teardown()
            return False

    def test(self):
        """测试逻辑 - 子类必须实现"""
        raise NotImplementedError("子类必须实现 test() 方法")


# ============================================
# 子类 - 继承基类
# ============================================
class APITest(BaseTest):
    """接口测试类"""

    def __init__(self, name, url, method="GET"):
        # 调用父类构造方法
        super().__init__(name)
        self.url = url
        self.method = method
        self.response = None

    def test(self):
        """实现接口测试逻辑"""
        import requests
        self.response = requests.request(
            self.method,
            self.url,
            timeout=10
        )
        return self.response.status_code == 200


class UITest(BaseTest):
    """UI 测试类"""

    def __init__(self, name, url, element):
        super().__init__(name)
        self.url = url
        self.element = element

    def setup(self):
        """重写前置操作"""
        super().setup()  # 可以调用父类方法
        print("打开浏览器...")

    def teardown(self):
        """重写后置操作"""
        print("关闭浏览器...")
        super().teardown()

    def test(self):
        """实现 UI 测试逻辑"""
        # 模拟 UI 操作
        print(f"访问 {self.url}，检查元素 {self.element}")
        return True


# ============================================
# 多重继承（了解即可，不推荐滥用）
# ============================================
class LoggerMixin:
    """日志混入类"""
    def log(self, message):
        print(f"[LOG] {message}")


class DatabaseMixin:
    """数据库混入类"""
    def query(self, sql):
        print(f"执行 SQL: {sql}")
        return []


class APITestWithLog(APITest, LoggerMixin):
    """带日志的接口测试"""
    def test(self):
        self.log(f"开始测试: {self.name}")
        result = super().test()
        self.log(f"测试结果: {result}")
        return result


# 使用
api_test = APITest("登录接口", "https://api.example.com/login", "POST")
api_test.run()

ui_test = UITest("首页展示", "https://www.example.com", "#header")
ui_test.run()
```

---

### 2.4 封装与属性装饰器

```python
class HTTPClient:
    """HTTP 客户端封装"""

    def __init__(self, base_url):
        self._base_url = base_url      # 私有变量（约定）
        self.__secret = "xxx"           # 名称修饰（更强私有）
        self._timeout = 30
        self._session = None

    # ============================================
    # property - 把方法变成属性访问
    # ============================================
    @property
    def base_url(self):
        """获取 base_url"""
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        """设置 base_url - 可以加验证"""
        if not value.startswith("http"):
            raise ValueError("base_url 必须以 http 开头")
        self._base_url = value.rstrip("/")

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if value <= 0:
            raise ValueError("timeout 必须大于 0")
        self._timeout = value

    # ============================================
    # 私有方法
    # ============================================
    def __build_url(self, endpoint):
        """构建完整 URL（内部方法）"""
        return f"{self._base_url}{endpoint}"

    def _log_request(self, url, method):
        """记录请求日志（受保护方法）"""
        print(f"[{method}] {url}")

    # ============================================
    # 公有方法
    # ============================================
    def get(self, endpoint, params=None):
        import requests
        url = self.__build_url(endpoint)
        self._log_request(url, "GET")
        return requests.get(url, params=params, timeout=self._timeout)

    def post(self, endpoint, data=None):
        import requests
        url = self.__build_url(endpoint)
        self._log_request(url, "POST")
        return requests.post(url, json=data, timeout=self._timeout)


# 使用
client = HTTPClient("https://api.example.com")

# 通过 property 访问
print(client.base_url)       # "https://api.example.com"
client.timeout = 60          # 设置

# 验证生效
try:
    client.base_url = "invalid"  # ValueError
except ValueError as e:
    print(e)

# 私有变量仍可访问（但不推荐）
print(client._base_url)      # 可以访问（约定私有）
# print(client.__secret)     # AttributeError
print(client._HTTPClient__secret)  # 名称修饰后仍可访问（但不应该这样做）
```

---

### 2.5 魔术方法

```python
class TestCase:
    """测试用例 - 展示常用魔术方法"""

    def __init__(self, name, priority="P1"):
        self.name = name
        self.priority = priority
        self.status = None

    # ============================================
    # 对象表示
    # ============================================
    def __str__(self):
        """print() 和 str() 调用 - 用户友好"""
        return f"TestCase({self.name})"

    def __repr__(self):
        """repr() 调用 - 开发者友好，应能用于重建对象"""
        return f"TestCase(name='{self.name}', priority='{self.priority}')"

    # ============================================
    # 比较运算
    # ============================================
    def __eq__(self, other):
        """== 运算符"""
        if not isinstance(other, TestCase):
            return False
        return self.name == other.name and self.priority == other.priority

    def __lt__(self, other):
        """< 运算符 - 用于排序"""
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        return priority_order.get(self.priority, 99) < priority_order.get(other.priority, 99)

    # ============================================
    # 容器协议 - 让对象像列表一样使用
    # ============================================
    def __len__(self):
        """len() 函数"""
        return len(self.steps) if hasattr(self, 'steps') else 0

    def __bool__(self):
        """bool() 函数 - 判断真假"""
        return self.status == "pass"

    # ============================================
    # 可调用对象
    # ============================================
    def __call__(self):
        """让对象可以像函数一样调用"""
        return self.run()

    def run(self):
        print(f"执行测试: {self.name}")
        self.status = "pass"
        return True


# 使用示例
case1 = TestCase("登录测试", "P0")
case2 = TestCase("搜索测试", "P1")

print(case1)       # TestCase(登录测试) - 调用 __str__
print(repr(case1)) # TestCase(name='登录测试', priority='P0') - 调用 __repr__

case1 == case2     # False - 调用 __eq__
case1 < case2      # True - P0 < P1 - 调用 __lt__

cases = [case2, case1]
cases.sort()       # 使用 __lt__ 排序
# [TestCase(登录测试), TestCase(搜索测试)]

case1()            # 调用 __call__，相当于 case1.run()
```

---

### 2.6 异常处理

```python
# ============================================
# 基本结构
# ============================================
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("除数不能为 0")
        return None
    except TypeError as e:
        print(f"类型错误: {e}")
        return None
    except Exception as e:
        # 捕获所有异常（慎用，可能隐藏问题）
        print(f"未知错误: {e}")
        return None
    else:
        # 没有异常时执行
        print("计算成功")
        return result
    finally:
        # 无论如何都执行（清理资源）
        print("计算完成")


# ============================================
# 异常链
# ============================================
def read_config(filepath):
    try:
        with open(filepath) as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"配置文件不存在: {filepath}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"配置文件格式错误: {filepath}") from e


# ============================================
# 自定义异常
# ============================================
class TestError(Exception):
    """测试异常基类"""
    pass


class AssertionError(TestError):
    """断言失败"""
    def __init__(self, expected, actual, message=""):
        self.expected = expected
        self.actual = actual
        self.message = message
        super().__init__(f"断言失败: 期望 {expected}, 实际 {actual}. {message}")


class TimeoutError(TestError):
    """超时异常"""
    pass


class ConnectionError(TestError):
    """连接异常"""
    pass


# 使用自定义异常
def assert_equals(expected, actual, message=""):
    if expected != actual:
        raise AssertionError(expected, actual, message)


# ============================================
# 上下文管理 - 异常处理最佳实践
# ============================================
def test_with_retry(func, max_retry=3):
    """带重试的测试执行"""
    for attempt in range(max_retry):
        try:
            return func()
        except Exception as e:
            if attempt == max_retry - 1:
                raise  # 重试次数用完，抛出异常
            print(f"第 {attempt + 1} 次失败，重试中...")
            import time
            time.sleep(1)


# 使用
def flaky_test():
    import random
    if random.random() < 0.7:
        raise Exception("随机失败")
    return "成功"


result = test_with_retry(flaky_test, max_retry=5)
```

---

### 2.7 上下文管理器

```python
# ============================================
# 类方式实现上下文管理器
# ============================================
class Timer:
    """计时器上下文管理器"""

    def __init__(self, name=""):
        self.name = name
        self.start_time = None
        self.elapsed = None

    def __enter__(self):
        """进入 with 块时调用"""
        import time
        self.start_time = time.time()
        return self  # 返回值赋给 as 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开 with 块时调用"""
        import time
        self.elapsed = time.time() - self.start_time
        print(f"[{self.name}] 耗时: {self.elapsed:.2f} 秒")

        # 返回 True 会抑制异常
        if exc_type is not None:
            print(f"发生异常: {exc_val}")
            return False  # 不抑制，让异常继续传播


# 使用
with Timer("登录测试") as t:
    import time
    time.sleep(0.5)
# [登录测试] 耗时: 0.50 秒


# ============================================
# contextlib 方式（更简洁）
# ============================================
from contextlib import contextmanager

@contextmanager
def db_transaction(db):
    """数据库事务上下文"""
    try:
        yield db  # yield 的值赋给 as 后面的变量
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ============================================
# 实用示例：测试环境管理
# ============================================
class TestEnvironment:
    """测试环境上下文管理器"""

    def __init__(self, env_name):
        self.env_name = env_name
        self.original_env = None

    def __enter__(self):
        # 保存原始环境
        import os
        self.original_env = os.environ.copy()

        # 设置测试环境
        os.environ["TEST_ENV"] = self.env_name
        print(f"切换到 {self.env_name} 环境")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 恢复原始环境
        import os
        os.environ.clear()
        os.environ.update(self.original_env)
        print("恢复原始环境")


# 使用
with TestEnvironment("test"):
    import os
    print(os.environ["TEST_ENV"])  # "test"
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 能定义简单的类，包含 `__init__` 和实例方法
- [ ] 理解 `self` 的含义
- [ ] 能使用继承复用代码
- [ ] 能使用 try/except 处理常见异常
- [ ] 能编写简单的上下文管理器

### 应该了解

- [ ] 类方法和静态方法的区别
- [ ] property 装饰器的使用
- [ ] 自定义异常的设计
- [ ] 魔术方法的常见用途

---

## 四、练习内容

### 练习1：封装 HTTP 客户端类

```python
# 实现 HttpClient 类，要求：
# 1. 支持设置 base_url 和 timeout
# 2. 支持 get/post 方法
# 3. 自动记录请求日志
# 4. 支持重试机制
# 5. 使用 property 验证参数

class HttpClient:
    """HTTP 客户端"""
    pass

# 测试代码
client = HttpClient("https://jsonplaceholder.typicode.com")
response = client.get("/posts/1")
print(response.json())

client.timeout = 60
try:
    client.timeout = -1  # 应该抛出异常
except ValueError as e:
    print(e)
```

### 练习2：测试用例管理类

```python
# 实现 TestCase 和 TestSuite 类

class TestCase:
    """测试用例"""
    # 要求：
    # 1. 包含 name, priority, status, duration 属性
    # 2. 实现 __str__ 和 __lt__（按优先级排序）
    # 3. 实现 run() 方法（模拟执行）
    pass


class TestSuite:
    """测试套件"""
    # 要求：
    # 1. 可以添加多个 TestCase
    # 2. 实现 run_all() 运行所有用例
    # 3. 实现 get_report() 生成报告
    # 4. 按优先级排序执行
    pass


# 测试代码
suite = TestSuite("冒烟测试")
suite.add_case(TestCase("登录测试", "P0"))
suite.add_case(TestCase("搜索测试", "P1"))
suite.add_case(TestCase("支付测试", "P0"))

suite.run_all()
print(suite.get_report())
```

### 练习3：数据库连接管理器

```python
# 实现数据库连接的上下文管理器

class DBConnection:
    """数据库连接上下文管理器"""
    # 要求：
    # 1. 进入时建立连接
    # 2. 离开时关闭连接
    # 3. 发生异常时回滚事务
    # 4. 记录连接时间
    pass

# 测试代码
with DBConnection("localhost", "test_db") as db:
    db.execute("SELECT * FROM users")
```

### 练习4：自定义测试框架

```python
# 实现一个迷你测试框架

class TestResult:
    """测试结果"""
    pass


class TestRunner:
    """测试运行器"""
    # 要求：
    # 1. 收集所有测试用例
    # 2. 执行并收集结果
    # 3. 支持前置/后置操作
    # 4. 生成统计报告
    pass


# 使用示例
class MyTests:
    def test_login(self):
        assert True

    def test_search(self):
        assert False


runner = TestRunner()
runner.load(MyTests)
result = runner.run()
print(result.summary())
```

---

## 五、检验标准

### 自测题

#### 题目1：类设计
设计一个 `User` 类，要求：
- 包含 username, email, age 属性
- email 设置时验证格式
- age 设置时验证范围（0-150）
- 实现比较运算符（按年龄比较）

#### 题目2：继承
设计类层次：
- `BaseAPI` 基类：包含 send_request 方法
- `UserAPI` 子类：继承 BaseAPI，封装用户相关接口
- `OrderAPI` 子类：继承 BaseAPI，封装订单相关接口

#### 题目3：异常处理
实现一个配置加载函数，要求：
- 文件不存在时抛出自定义异常
- JSON 格式错误时抛出自定义异常
- 必要字段缺失时抛出自定义异常
- 使用 try/except/finally 确保资源释放

### 答案

```python
# 题目1
import re

class User:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email  # 通过 setter 验证
        self.age = age      # 通过 setter 验证

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            raise ValueError("邮箱格式不正确")
        self._email = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0 or value > 150:
            raise ValueError("年龄必须在 0-150 之间")
        self._age = value

    def __lt__(self, other):
        return self.age < other.age

    def __eq__(self, other):
        return self.username == other.username


# 题目2
import requests

class BaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def send_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method, url, **kwargs)


class UserAPI(BaseAPI):
    def login(self, username, password):
        return self.send_request("POST", "/login", json={
            "username": username,
            "password": password
        })

    def get_profile(self):
        return self.send_request("GET", "/profile")


class OrderAPI(BaseAPI):
    def create_order(self, data):
        return self.send_request("POST", "/orders", json=data)

    def get_orders(self):
        return self.send_request("GET", "/orders")


# 题目3
class ConfigError(Exception):
    pass

class ConfigFileNotFoundError(ConfigError):
    pass

class ConfigFormatError(ConfigError):
    pass

class ConfigValidationError(ConfigError):
    pass

def load_config(filepath, required_keys=None):
    """加载配置文件"""
    required_keys = required_keys or []

    try:
        with open(filepath, 'r') as f:
            import json
            config = json.load(f)
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"配置文件不存在: {filepath}")
    except json.JSONDecodeError as e:
        raise ConfigFormatError(f"配置文件格式错误: {e}")
    finally:
        print("配置加载完成")

    # 验证必要字段
    missing = [k for k in required_keys if k not in config]
    if missing:
        raise ConfigValidationError(f"缺少必要字段: {missing}")

    return config
```

---

## 六、本周小结

### 核心要点

1. **类与对象**：Python 一切皆对象，理解 `self` 是关键
2. **继承**：代码复用的利器，测试框架大量使用
3. **封装**：通过 property 和私有变量控制访问
4. **异常处理**：让程序更健壮，测试更可靠
5. **上下文管理器**：资源管理的最佳实践

### 在测试工作中的应用

| OOP 概念 | 测试应用场景 |
|---------|-------------|
| 类 | 封装测试用例、测试工具 |
| 继承 | BaseTest → APITest / UITest |
| 封装 | 隐藏实现细节，暴露简洁接口 |
| 异常处理 | 测试失败处理、重试机制 |
| 上下文管理器 | 数据库连接、浏览器驱动管理 |

### 下周预告

第3周将学习文件操作与模块化，包括 JSON/YAML 配置处理、CSV 数据驱动、项目结构组织等。
