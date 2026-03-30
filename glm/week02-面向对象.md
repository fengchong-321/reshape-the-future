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

## 四、练习内容（20 题）

### 基础练习（1-8）

---

**练习1：定义简单类**

**场景说明**：你需要创建一个用户类，用于存储用户基本信息。

**具体需求**：
1. 创建 `User` 类
2. `__init__` 方法接收 `username`、`email`、`age` 三个参数并保存为实例属性
3. `get_info()` 方法返回格式化的用户信息字符串，如：`"用户名: zhangsan, 邮箱: zhangsan@example.com, 年龄: 25"`
4. `is_adult()` 方法判断用户是否成年（age >= 18），返回布尔值

**使用示例**：
```python
# 创建用户
user = User("zhangsan", "zhangsan@example.com", 25)

# 获取用户信息
print(user.get_info())
# 输出: 用户名: zhangsan, 邮箱: zhangsan@example.com, 年龄: 25

# 判断是否成年
print(user.is_adult())  # True

# 未成年用户
child = User("xiaoming", "xiaoming@example.com", 15)
print(child.is_adult())  # False
```

**验收标准**：
- [ ] 能正确创建 User 实例
- [ ] get_info() 返回格式正确
- [ ] is_adult() 判断逻辑正确

---

**练习2：self 理解**

**场景说明**：创建一个计数器类，理解 `self` 如何指向当前实例。

**具体需求**：
1. 创建 `Counter` 类
2. `__init__` 方法初始化 `count` 属性为 0
3. `increment()` 方法让 `count` 加 1
4. `decrement()` 方法让 `count` 减 1（不能小于 0）
5. `reset()` 方法重置 `count` 为 0
6. `get_count()` 方法返回当前 `count` 值

**使用示例**：
```python
# 创建两个独立的计数器
c1 = Counter()
c2 = Counter()

c1.increment()  # c1.count = 1
c1.increment()  # c1.count = 2
c2.increment()  # c2.count = 1

print(c1.get_count())  # 2
print(c2.get_count())  # 1

c1.decrement()  # c1.count = 1
print(c1.get_count())  # 1

# 测试边界
c1.reset()
print(c1.get_count())  # 0

c1.decrement()  # 不能小于 0
print(c1.get_count())  # 0（仍然是 0）
```

**验收标准**：
- [ ] 多个 Counter 实例互不影响
- [ ] count 不能减到负数
- [ ] reset() 正确重置为 0

---

**练习3：类属性 vs 实例属性**

**场景说明**：创建学生类，理解类属性（所有实例共享）和实例属性（每个实例独立）的区别。

**具体需求**：
1. 创建 `Student` 类
2. 类属性 `school_name = "测试学校"`（所有学生共享）
3. 实例属性 `name`（学生姓名）、`grade`（年级）
4. 实例方法 `get_info()` 返回：`"张三, 3年级, 测试学校"`
5. 类方法 `change_school(cls, new_name)` 修改学校名称
6. 静态方法 `is_passing(score)` 判断分数是否及格（>= 60）

**使用示例**：
```python
# 创建学生
s1 = Student("张三", 3)
s2 = Student("李四", 5)

print(s1.get_info())  # 张三, 3年级, 测试学校
print(s2.get_info())  # 李四, 5年级, 测试学校

# 修改学校名称（类方法）
Student.change_school("新测试学校")

print(s1.get_info())  # 张三, 3年级, 新测试学校
print(s2.get_info())  # 李四, 5年级, 新测试学校

# 判断是否及格（静态方法）
print(Student.is_passing(75))   # True
print(Student.is_passing(55))   # False
```

**验收标准**：
- [ ] 类属性被所有实例共享
- [ ] 类方法可以修改类属性
- [ ] 静态方法不需要实例就能调用

---

**练习4：继承基础**

**场景说明**：创建动物类层次，理解继承如何复用代码。

**具体需求**：
1. `Animal` 基类：
   - 属性：`name`（动物名称）
   - 方法：`speak()` 抛出 `NotImplementedError`（子类必须实现）
   - 方法：`introduce()` 返回 `"我是{name}"`

2. `Dog` 子类：
   - 继承 `Animal`
   - 重写 `speak()` 返回 `"汪汪"`

3. `Cat` 子类：
   - 继承 `Animal`
   - 重写 `speak()` 返回 `"喵喵"`

4. `Bird` 子类：
   - 继承 `Animal`
   - 重写 `speak()` 返回 `"叽叽"`
   - 新增方法 `fly()` 返回 `"飞起来了"`

**使用示例**：
```python
dog = Dog("旺财")
cat = Cat("咪咪")
bird = Bird("小鸟")

print(dog.introduce())  # 我是旺财
print(dog.speak())      # 汪汪

print(cat.introduce())  # 我是咪咪
print(cat.speak())      # 喵喵

print(bird.introduce()) # 我是小鸟
print(bird.speak())     # 叽叽
print(bird.fly())       # 飞起来了
```

**验收标准**：
- [ ] 子类正确继承父类属性和方法
- [ ] 子类正确重写父类方法
- [ ] 子类可以新增自己的方法

---

**练习5：方法重写与 super()**

**场景说明**：创建员工类，理解如何重写方法并调用父类方法。

**具体需求**：
1. `Employee` 基类：
   - 属性：`name`（姓名）、`salary`（月薪）
   - 方法：`get_bonus()` 返回奖金 `salary * 0.1`
   - 方法：`get_info()` 返回 `"员工: 张三, 月薪: 10000"`

2. `Manager` 子类：
   - 继承 `Employee`
   - 新增属性：`team_size`（团队人数）
   - 重写 `get_bonus()` 返回 `salary * 0.2 + team_size * 100`
   - 重写 `get_info()` 调用父类方法后追加 `", 团队人数: 5"`

**使用示例**：
```python
# 普通员工
emp = Employee("张三", 10000)
print(emp.get_info())   # 员工: 张三, 月薪: 10000
print(emp.get_bonus())  # 1000.0

# 经理
mgr = Manager("李四", 20000, 5)
print(mgr.get_info())   # 员工: 李四, 月薪: 20000, 团队人数: 5
print(mgr.get_bonus())  # 4500.0 (20000*0.2 + 5*100)
```

**验收标准**：
- [ ] 正确使用 `super()` 调用父类方法
- [ ] 子类方法正确重写父类方法
- [ ] 奖金计算逻辑正确

---

**练习6：property 装饰器**

**场景说明**：创建商品类，使用 property 控制属性访问和验证。

**具体需求**：
1. 创建 `Product` 类
2. 私有属性 `_price` 存储价格
3. `@property` 装饰的 `price` getter 方法返回价格
4. `@price.setter` 装饰的 setter 方法验证价格必须 > 0，否则抛出 `ValueError`
5. `@price.deleter` 装饰的 deleter 方法打印 `"价格已删除"` 并将 `_price` 设为 0
6. 只读属性 `discount_price` 返回打 8 折后的价格（只有 getter，没有 setter）

**使用示例**：
```python
product = Product(100)

# 获取价格
print(product.price)           # 100
print(product.discount_price)  # 80.0

# 设置价格（会验证）
product.price = 200
print(product.price)           # 200

# 设置非法价格
try:
    product.price = -50
except ValueError as e:
    print(e)  # 价格必须大于0

# 尝试设置只读属性
try:
    product.discount_price = 100
except AttributeError as e:
    print(e)  # can't set attribute

# 删除价格
del product.price
print(product.price)  # 0
```

**验收标准**：
- [ ] price 验证逻辑正确
- [ ] discount_price 是只读的
- [ ] deleter 正确执行

---

**练习7：异常处理基础**

**场景说明**：编写安全除法函数，处理各种可能的异常。

**具体需求**：
1. 函数签名：`safe_divide(a, b) -> float or str`
2. 处理 `ZeroDivisionError`（除数为 0）返回 `"错误: 除数不能为0"`
3. 处理 `TypeError`（参数类型错误）返回 `"错误: 参数必须是数字"`
4. 使用 `try/except/else/finally` 完整结构
5. `finally` 块中打印日志 `"计算结束"`
6. 成功时返回计算结果

**使用示例**：
```python
# 正常计算
result = safe_divide(10, 2)
print(result)  # 5.0
# 控制台输出: 计算结束

# 除数为 0
result = safe_divide(10, 0)
print(result)  # 错误: 除数不能为0
# 控制台输出: 计算结束

# 类型错误
result = safe_divide("10", 2)
print(result)  # 错误: 参数必须是数字
# 控制台输出: 计算结束
```

**验收标准**：
- [ ] 正确处理除零异常
- [ ] 正确处理类型异常
- [ ] finally 块始终执行

---

**练习8：自定义异常**

**场景说明**：定义测试相关的异常体系，用于测试框架中。

**具体需求**：
1. `TestError` 基类：
   - 继承 `Exception`
   - 属性：`message`（错误消息）、`code`（错误码）
   - `__init__` 接收 `message` 和 `code`，默认 code=1

2. `TestNotFoundError`：
   - 继承 `TestError`
   - 默认 code=404
   - 自动设置 message 为 `"测试用例未找到"`

3. `TestTimeoutError`：
   - 继承 `TestError`
   - 默认 code=408
   - 接收 `timeout` 参数，message 为 `"测试超时: {timeout}秒"`

4. `TestAssertionError`：
   - 继承 `TestError`
   - 默认 code=400
   - 接收 `expected` 和 `actual` 参数，message 为 `"断言失败: 期望{expected}, 实际{actual}"`

**使用示例**：
```python
# 抛出测试未找到异常
raise TestNotFoundError(test_name="login_test")
# TestNotFoundError: 测试用例未找到 (code=404)

# 抛出超时异常
raise TestTimeoutError(timeout=30)
# TestTimeoutError: 测试超时: 30秒 (code=408)

# 抛出断言失败异常
raise TestAssertionError(expected=200, actual=404)
# TestAssertionError: 断言失败: 期望200, 实际404 (code=400)

# 捕获异常
try:
    raise TestTimeoutError(timeout=30)
except TestError as e:
    print(f"错误码: {e.code}, 消息: {e.message}")
# 输出: 错误码: 408, 消息: 测试超时: 30秒
```

**验收标准**：
- [ ] 异常继承关系正确
- [ ] 错误码和消息格式正确
- [ ] 可以用 `isinstance(e, TestError)` 捕获所有子异常

---

### 进阶练习（9-16）

---

**练习9：封装 HTTP 客户端类**

**场景说明**：封装一个通用的 HTTP 客户端，用于接口测试。

**具体需求**：
1. `__init__(self, base_url, timeout=30)` 初始化客户端
2. 私有属性 `_base_url`、`_timeout`、`_session`
3. `@property` 验证 `timeout` 必须 > 0
4. `@property` 验证 `base_url` 必须以 `http://` 或 `https://` 开头
5. 方法 `get(endpoint, params=None)` 发送 GET 请求
6. 方法 `post(endpoint, data=None)` 发送 POST 请求
7. 方法 `put(endpoint, data=None)` 发送 PUT 请求
8. 方法 `delete(endpoint)` 发送 DELETE 请求
9. 方法 `request_with_retry(method, endpoint, max_retry=3, **kwargs)` 支持重试
10. 所有请求自动记录日志：`"[GET] https://api.example.com/users"`

**使用示例**：
```python
client = HttpClient("https://api.example.com", timeout=10)

# 设置属性（会验证）
client.timeout = 60
client.base_url = "https://new-api.example.com"

# 无效设置会报错
try:
    client.timeout = -1
except ValueError as e:
    print(e)  # timeout 必须大于0

# 发送请求
response = client.get("/users", params={"page": 1})
# 日志: [GET] https://new-api.example.com/users

response = client.post("/users", data={"name": "test"})
# 日志: [POST] https://new-api.example.com/users

# 带重试的请求
response = client.request_with_retry("GET", "/flaky-endpoint", max_retry=3)
```

**验收标准**：
- [ ] property 验证正确
- [ ] 四种 HTTP 方法都实现
- [ ] 重试机制正常工作
- [ ] 日志正确记录

---

**练习10：测试用例管理类**

**场景说明**：创建测试用例和测试套件的管理类。

**具体需求**：

**TestCase 类**：
1. 属性：`name`（用例名）、`priority`（优先级 P0-P3）、`status`（状态）、`duration`（耗时）
2. `__init__(self, name, priority="P1")` 初始化
3. `run()` 方法模拟执行（设置 status="pass"，duration=0.1）
4. `__str__()` 返回 `"TestCase(登录测试, P0)"`
5. `__lt__()` 按优先级排序（P0 < P1 < P2 < P3）
6. `__bool__()` 根据 status 判断（"pass" 为 True）

**TestSuite 类**：
1. 属性：`name`（套件名）、`cases`（用例列表）
2. `add_case(case)` 添加测试用例
3. `run_all()` 按优先级排序后执行所有用例
4. `get_report()` 返回统计报告字典：
   ```python
   {
       "total": 3,
       "passed": 2,
       "failed": 1,
       "duration": 0.3
   }
   ```

**使用示例**：
```python
# 创建测试用例
case1 = TestCase("登录测试", "P0")
case2 = TestCase("搜索测试", "P1")
case3 = TestCase("下单测试", "P0")

# 排序（按优先级）
cases = [case2, case1, case3]
cases.sort()
print([str(c) for c in cases])
# ['TestCase(登录测试, P0)', 'TestCase(下单测试, P0)', 'TestCase(搜索测试, P1)']

# 创建测试套件
suite = TestSuite("冒烟测试")
suite.add_case(case1)
suite.add_case(case2)
suite.add_case(case3)

# 执行所有用例
suite.run_all()

# 获取报告
report = suite.get_report()
print(report)
# {'total': 3, 'passed': 3, 'failed': 0, 'duration': 0.3}

# 判断用例是否通过
case1.run()
if case1:  # 调用 __bool__
    print("测试通过")
```

**验收标准**：
- [ ] 用例按优先级正确排序
- [ ] 测试报告统计正确
- [ ] `__bool__` 正确实现

---

**练习11：数据库连接管理器**

**场景说明**：使用上下文管理器管理数据库连接。

**具体需求**：
1. `__init__(self, db_path)` 初始化，接收数据库路径
2. `__enter__()` 建立连接，打印 `"连接数据库: {db_path}"`，返回 self
3. `__exit__(exc_type, exc_val, exc_tb)` 关闭连接
   - 如果有异常，打印 `"发生异常，回滚事务"` 并回滚
   - 如果没有异常，打印 `"提交事务"`
   - 最后打印 `"关闭数据库连接"`
4. 方法 `execute(sql)` 模拟执行 SQL（打印 SQL 语句）
5. 属性 `connected_time` 记录连接时长

**使用示例**：
```python
# 正常使用
with DBConnection("test.db") as db:
    db.execute("SELECT * FROM users")
# 输出:
# 连接数据库: test.db
# 执行SQL: SELECT * FROM users
# 提交事务
# 关闭数据库连接

# 发生异常
with DBConnection("test.db") as db:
    db.execute("SELECT * FROM users")
    raise ValueError("模拟错误")
# 输出:
# 连接数据库: test.db
# 执行SQL: SELECT * FROM users
# 发生异常，回滚事务
# 关闭数据库连接
```

**验收标准**：
- [ ] 正确实现 `__enter__` 和 `__exit__`
- [ ] 异常时正确回滚
- [ ] 连接正确关闭

---

**练习12：配置管理类**

**场景说明**：创建一个配置管理类，支持多种方式加载配置、点号访问和验证。这是测试框架中常用的配置管理方式。

**具体需求**：
1. **从字典加载**：`Config.from_dict(data)` 类方法
2. **从 JSON 文件加载**：`Config.from_json(filepath)` 类方法
3. **从 YAML 文件加载**：`Config.from_yaml(filepath)` 类方法（可选，需要 PyYAML）
4. **点号访问**：`config.get("db.host")` 获取嵌套配置，如：
   ```python
   config = {
       "db": {
           "host": "localhost",
           "port": 3306
       }
   }
   config.get("db.host")  # 返回 "localhost"
   config.get("db.port")  # 返回 3306
   ```
5. **环境变量覆盖**：`config.get("db.host", env_override="DB_HOST")` 支持从环境变量读取
6. **验证必填字段**：`config.validate(["db.host", "db.port"])` 验证字段存在
7. **导出为字典**：`config.to_dict()` 返回完整配置字典

**使用示例**：
```python
# 1. 从字典创建
config_data = {
    "db": {
        "host": "localhost",
        "port": 3306,
        "user": "root"
    },
    "api": {
        "base_url": "https://api.example.com",
        "timeout": 30
    }
}
config = Config.from_dict(config_data)

# 2. 点号访问嵌套配置
print(config.get("db.host"))      # "localhost"
print(config.get("db.port"))      # 3306
print(config.get("api.timeout"))  # 30

# 3. 访问不存在的键
print(config.get("db.password", default=""))  # "" (返回默认值)
print(config.get("db.password"))              # None (没有默认值返回 None)

# 4. 环境变量覆盖
import os
os.environ["DB_HOST"] = "192.168.1.100"
print(config.get("db.host", env_override="DB_HOST"))  # "192.168.1.100" (从环境变量读取)

# 5. 验证必填字段
config.validate(["db.host", "db.port"])  # 通过，不报错

try:
    config.validate(["db.host", "db.password"])
except ValueError as e:
    print(e)  # 缺少必填字段: db.password

# 6. 导出为字典
full_config = config.to_dict()
print(full_config["db"]["host"])  # "localhost"

# 7. 从 JSON 文件加载（假设有 config.json）
# config = Config.from_json("config.json")

# 8. 从 YAML 文件加载（假设有 config.yaml）
# config = Config.from_yaml("config.yaml")
```

**实现提示**：
```python
class Config:
    def __init__(self, data):
        self._data = data

    def get(self, key, default=None, env_override=None):
        """点号访问嵌套字典"""
        # 1. 先检查环境变量
        if env_override:
            import os
            env_value = os.environ.get(env_override)
            if env_value is not None:
                return env_value

        # 2. 按点号分割，逐层访问
        keys = key.split(".")
        value = self._data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def validate(self, required_keys):
        """验证必填字段"""
        missing = []
        for key in required_keys:
            if self.get(key) is None:
                missing.append(key)
        if missing:
            raise ValueError(f"缺少必填字段: {', '.join(missing)}")

    def to_dict(self):
        """导出为字典"""
        return self._data.copy()

    @classmethod
    def from_dict(cls, data):
        """从字典创建"""
        return cls(data)

    @classmethod
    def from_json(cls, filepath):
        """从 JSON 文件加载"""
        import json
        with open(filepath, 'r') as f:
            return cls(json.load(f))

    @classmethod
    def from_yaml(cls, filepath):
        """从 YAML 文件加载"""
        try:
            import yaml
            with open(filepath, 'r') as f:
                return cls(yaml.safe_load(f))
        except ImportError:
            raise ImportError("需要安装 PyYAML: pip install pyyaml")
```

**验收标准**：
- [ ] 点号访问正确解析嵌套配置
- [ ] 环境变量覆盖正常工作
- [ ] 验证必填字段正确报错
- [ ] 能从 JSON 文件加载
- [ ] to_dict() 返回正确的字典

---

**练习13：日志记录器类**

**场景说明**：创建简易日志记录器，支持不同级别和输出目标。

**具体需求**：
1. 日志级别：`INFO`、`WARN`、`ERROR`，默认级别为 `INFO`
2. 输出目标：支持输出到控制台和文件
3. 日志格式：`[2024-01-15 10:30:45] [INFO] 这是一条日志`
4. 使用单例模式（多次创建返回同一个实例）
5. 方法 `info(msg)`、`warn(msg)`、`error(msg)`
6. 方法 `set_level(level)` 设置最低输出级别
7. 方法 `set_file(filepath)` 设置日志文件路径

**使用示例**：
```python
# 获取日志实例（单例）
logger1 = Logger()
logger2 = Logger()
print(logger1 is logger2)  # True

# 设置输出文件
logger1.set_file("app.log")

# 记录日志
logger1.info("程序启动")
# [2024-01-15 10:30:45] [INFO] 程序启动

logger1.warn("配置文件不存在，使用默认配置")
# [2024-01-15 10:30:45] [WARN] 配置文件不存在，使用默认配置

logger1.error("连接数据库失败")
# [2024-01-15 10:30:45] [ERROR] 连接数据库失败

# 设置日志级别
logger1.set_level("ERROR")
logger1.info("这条不会输出")  # 级别不够
logger1.error("这条会输出")   # ERROR >= ERROR
```

**验收标准**：
- [ ] 单例模式正确实现
- [ ] 日志格式正确
- [ ] 日志级别过滤正确
- [ ] 能输出到文件

---

**练习14：测试数据工厂**

**场景说明**：创建测试数据工厂，快速生成测试数据。

**具体需求**：
1. `@classmethod create_user(**kwargs)` 创建用户数据：
   - 默认值：`{"id": 1, "name": "测试用户", "email": "test@example.com", "age": 25}`
   - 支持通过 kwargs 覆盖默认值

2. `@classmethod create_order(**kwargs)` 创建订单数据：
   - 默认值：`{"order_id": "ORD001", "user_id": 1, "amount": 100.0, "status": "pending"}`

3. `@classmethod create_product(**kwargs)` 创建商品数据：
   - 默认值：`{"product_id": 1, "name": "测试商品", "price": 99.9, "stock": 100}`

4. `@classmethod create_batch(creator, count, **kwargs)` 批量生成数据：
   - `creator` 是上面的创建方法
   - `count` 是生成数量
   - 自动递增 ID

5. `@classmethod save_to_file(data, filepath, format="json")` 保存数据到文件

**使用示例**：
```python
# 创建单个用户
user = TestDataFactory.create_user()
print(user)
# {'id': 1, 'name': '测试用户', 'email': 'test@example.com', 'age': 25}

# 覆盖默认值
user = TestDataFactory.create_user(name="张三", age=30)
print(user)
# {'id': 1, 'name': '张三', 'email': 'test@example.com', 'age': 30}

# 批量创建用户
users = TestDataFactory.create_batch(TestDataFactory.create_user, 3)
print(len(users))  # 3
print(users[0]['id'])  # 1
print(users[1]['id'])  # 2
print(users[2]['id'])  # 3

# 保存到文件
TestDataFactory.save_to_file(users, "users.json")
```

**验收标准**：
- [ ] 默认值正确
- [ ] kwargs 覆盖正确
- [ ] 批量生成 ID 递增
- [ ] 文件保存正确

---

**练习15：断言库类**

**场景说明**：创建自定义断言库，提供更友好的断言方法。

**具体需求**：
1. `@staticmethod equal(actual, expected, msg="")` 断言相等
2. `@staticmethod not_equal(a, b, msg="")` 断言不相等
3. `@staticmethod contains(item, container, msg="")` 断言包含
4. `@staticmethod raises(func, exception, msg="")` 断言抛出异常
5. `@staticmethod json_equal(actual, expected, ignore_keys=[])` 比较 JSON（忽略指定键）
6. 所有断言失败时抛出 `AssertionError`，消息格式：`"断言失败: 期望 {expected}, 实际 {actual}. {msg}"`

**使用示例**：
```python
# 相等断言
Assert.equal(1 + 1, 2)
Assert.equal("hello".upper(), "HELLO")

# 不相等断言
Assert.not_equal(1, 2)

# 包含断言
Assert.contains("world", "hello world")
Assert.contains(3, [1, 2, 3])

# 异常断言
def divide_by_zero():
    return 1 / 0

Assert.raises(divide_by_zero, ZeroDivisionError)

# JSON 比较（忽略某些键）
actual = {"id": 1, "name": "test", "created_at": "2024-01-15"}
expected = {"id": 1, "name": "test", "created_at": "2024-01-16"}
Assert.json_equal(actual, expected, ignore_keys=["created_at"])  # 通过

# 断言失败示例
try:
    Assert.equal(1, 2, "数字应该相等")
except AssertionError as e:
    print(e)
    # 断言失败: 期望 2, 实际 1. 数字应该相等
```

**验收标准**：
- [ ] 所有断言方法正确实现
- [ ] 失败消息格式正确
- [ ] json_equal 正确忽略指定键

---

**练习16：API 封装类**

**场景说明**：封装 API 接口，方便测试调用。

**具体需求**：

**BaseAPI 基类**：
1. `__init__(self, base_url)` 初始化
2. `send_request(method, endpoint, **kwargs)` 发送请求
3. `_build_url(endpoint)` 构建完整 URL（私有方法）
4. `_log_request(method, url)` 记录请求日志（受保护方法）

**UserAPI 子类**：
1. 继承 `BaseAPI`
2. `login(username, password)` 登录接口，POST `/login`
3. `logout()` 登出接口，POST `/logout`
4. `get_profile()` 获取用户信息，GET `/profile`
5. `update_profile(data)` 更新用户信息，PUT `/profile`
6. `delete_account()` 删除账户，DELETE `/account`

**使用示例**：
```python
# 创建 API 客户端
api = UserAPI("https://api.example.com")

# 登录
response = api.login("zhangsan", "password123")
# 日志: [POST] https://api.example.com/login

# 获取用户信息
profile = api.get_profile()
# 日志: [GET] https://api.example.com/profile

# 更新用户信息
api.update_profile({"name": "新名字"})
# 日志: [PUT] https://api.example.com/profile

# 登出
api.logout()
# 日志: [POST] https://api.example.com/logout
```

**验收标准**：
- [ ] 正确继承 BaseAPI
- [ ] 所有接口方法正确实现
- [ ] 日志正确记录

---

### 综合练习（17-20）

---

**练习17：迷你测试框架**

**场景说明**：实现一个简单的测试框架，类似 Pytest 的核心功能。

**具体需求**：

**TestResult 类**：
1. 属性：`passed`（通过数）、`failed`（失败数）、`errors`（错误列表）
2. 方法 `add_pass()` 通过数 +1
3. 方法 `add_failure(test_name, error)` 记录失败
4. 方法 `summary()` 返回统计字符串：`"3 passed, 1 failed"`

**TestRunner 类**：
1. `__init__(self, test_class)` 接收测试类
2. `run()` 执行所有 `test_` 开头的方法
3. 支持 `setup()` 在每个测试前执行
4. 支持 `teardown()` 在每个测试后执行
5. 返回 `TestResult` 对象

**使用示例**：
```python
class MyTests:
    def setup(self):
        print("初始化测试环境")

    def teardown(self):
        print("清理测试环境")

    def test_add(self):
        assert 1 + 1 == 2

    def test_subtract(self):
        assert 2 - 1 == 1

    def test_fail(self):
        assert 1 == 2  # 这个会失败

# 运行测试
runner = TestRunner(MyTests)
result = runner.run()
print(result.summary())
# 输出: 2 passed, 1 failed
```

**验收标准**：
- [ ] 自动发现 test_ 方法
- [ ] setup/teardown 正确执行
- [ ] 测试结果统计正确

---

**练习18：缓存装饰器类**

**场景说明**：实现方法结果缓存，避免重复计算。

**具体需求**：
1. `__init__(self, expire_seconds=60)` 设置缓存过期时间
2. `__call__(self, func)` 使其可以作为装饰器使用
3. 缓存方法的返回值
4. 支持设置过期时间
5. 方法 `clear_cache()` 手动清除缓存
6. 使用 `threading.Lock` 保证线程安全

**使用示例**：
```python
import time

@CacheDecorator(expire_seconds=2)
def expensive_computation(n):
    print(f"计算中... n={n}")
    time.sleep(1)  # 模拟耗时计算
    return n * n

# 第一次调用（会执行计算）
result1 = expensive_computation(5)
# 输出: 计算中... n=5
print(result1)  # 25

# 第二次调用（使用缓存）
result2 = expensive_computation(5)
# 不输出 "计算中..."
print(result2)  # 25

# 等待缓存过期
time.sleep(3)
result3 = expensive_computation(5)
# 输出: 计算中... n=5（重新计算）
print(result3)  # 25

# 手动清除缓存
expensive_computation.clear_cache()
```

**验收标准**：
- [ ] 缓存功能正常
- [ ] 过期时间正确
- [ ] 手动清除缓存有效
- [ ] 线程安全

---

**练习19：插件系统**

**场景说明**：实现一个简单的插件管理系统。

**具体需求**：
1. `register(plugin)` 注册插件（插件是包含 `name` 属性的对象）
2. `load(path)` 从 Python 文件加载插件
3. `execute(hook_name, *args)` 执行所有插件的指定钩子方法
4. `get_plugins()` 获取所有已注册插件
5. `unload(plugin_name)` 卸载指定插件

**使用示例**：
```python
# 定义插件
class LogPlugin:
    name = "logger"

    def before_test(self, test_name):
        print(f"[日志] 开始测试: {test_name}")

    def after_test(self, test_name, result):
        print(f"[日志] 测试完成: {test_name}, 结果: {result}")

class ReportPlugin:
    name = "reporter"

    def before_test(self, test_name):
        print(f"[报告] 记录测试开始: {test_name}")

    def after_test(self, test_name, result):
        print(f"[报告] 记录测试结果: {test_name} -> {result}")

# 使用插件管理器
manager = PluginManager()
manager.register(LogPlugin())
manager.register(ReportPlugin())

# 执行钩子
manager.execute("before_test", "登录测试")
# 输出:
# [日志] 开始测试: 登录测试
# [报告] 记录测试开始: 登录测试

manager.execute("after_test", "登录测试", "pass")
# 输出:
# [日志] 测试完成: 登录测试, 结果: pass
# [报告] 记录测试结果: 登录测试 -> pass

# 获取所有插件
plugins = manager.get_plugins()
print([p.name for p in plugins])  # ['logger', 'reporter']

# 卸载插件
manager.unload("logger")
print([p.name for p in manager.get_plugins()])  # ['reporter']
```

**验收标准**：
- [ ] 插件注册和卸载正确
- [ ] 钩子执行正确
- [ ] 插件列表获取正确

---

**练习20：状态机**

**场景说明**：实现测试用例状态机，管理测试状态流转。

**具体需求**：
1. 初始状态为 `"pending"`
2. 状态流转规则：
   - `pending` → `running`
   - `running` → `passed` / `failed` / `skipped`
   - 只能按规则流转，非法流转抛出 `ValueError`
3. `transition(to_state)` 状态转换
4. `can_transition(to_state)` 检查是否可转换（返回布尔值）
5. `get_history()` 获取状态历史列表
6. `@property state` 只读属性获取当前状态

**使用示例**：
```python
# 创建状态机
sm = TestStateMachine()
print(sm.state)  # pending

# 检查是否可以转换
print(sm.can_transition("running"))  # True
print(sm.can_transition("passed"))   # False（不能直接从 pending 到 passed）

# 执行转换
sm.transition("running")
print(sm.state)  # running

sm.transition("passed")
print(sm.state)  # passed

# 非法转换
try:
    sm.transition("running")  # passed 不能转到 running
except ValueError as e:
    print(e)  # 非法状态转换: passed -> running

# 查看历史
print(sm.get_history())
# ['pending', 'running', 'passed']

# 测试失败场景
sm2 = TestStateMachine()
sm2.transition("running")
sm2.transition("failed")
print(sm2.state)  # failed
print(sm2.get_history())
# ['pending', 'running', 'failed']

# 测试跳过场景
sm3 = TestStateMachine()
sm3.transition("running")
sm3.transition("skipped")
print(sm3.state)  # skipped
```

**验收标准**：
- [ ] 状态转换规则正确
- [ ] 非法转换正确报错
- [ ] 状态历史正确记录
- [ ] state 属性只读

---

## 五、检验标准

### 自测题

---

#### 题目1：类设计（综合考察：类定义、property、魔术方法）

**场景**：设计一个用户管理系统中的 `User` 类。

**需求**：
1. 包含 `username`、`email`、`age` 三个属性
2. `email` 设置时验证格式（必须包含 `@` 和 `.`）
3. `age` 设置时验证范围（0-150 的整数）
4. 实现 `__lt__` 比较运算符（按年龄比较）
5. 实现 `__eq__` 比较运算符（按用户名比较）
6. 实现 `__str__` 返回用户友好字符串：`"用户: 张三 (25岁)"`

**测试用例**：
```python
# 测试1：正常创建
user1 = User("zhangsan", "zhangsan@example.com", 25)
user2 = User("lisi", "lisi@example.com", 30)

print(user1)  # 用户: zhangsan (25岁)
print(user1 < user2)  # True (25 < 30)

# 测试2：邮箱验证
try:
    user = User("test", "invalid-email", 20)
except ValueError as e:
    print(e)  # 邮箱格式不正确

# 测试3：年龄验证
try:
    user = User("test", "test@example.com", 200)
except ValueError as e:
    print(e)  # 年龄必须在0-150之间

# 测试4：比较运算
users = [user2, user1]
users.sort()
print([u.username for u in users])  # ['zhangsan', 'lisi']
```

---

#### 题目2：继承体系设计（综合考察：继承、super()、方法重写）

**场景**：设计 API 测试框架的类层次结构。

**需求**：

**BaseAPI 基类**：
1. `__init__(self, base_url, timeout=30)` 初始化
2. `send_request(method, endpoint, **kwargs)` 发送请求
3. `_build_url(endpoint)` 构建完整 URL（私有方法）
4. `_log(method, url)` 记录日志（受保护方法）

**UserAPI 子类**：
1. 继承 `BaseAPI`
2. `login(username, password)` 登录
3. `get_profile()` 获取用户信息
4. `update_profile(data)` 更新用户信息

**OrderAPI 子类**：
1. 继承 `BaseAPI`
2. `create_order(data)` 创建订单
3. `get_orders()` 获取订单列表
4. `cancel_order(order_id)` 取消订单

**测试用例**：
```python
# 模拟 requests（测试时使用）
class MockResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}

    def json(self):
        return self._json

# 测试基类功能
api = UserAPI("https://api.example.com")
print(api._build_url("/login"))  # https://api.example.com/login

# 测试继承
user_api = UserAPI("https://api.example.com")
order_api = OrderAPI("https://api.example.com")

print(isinstance(user_api, BaseAPI))  # True
print(isinstance(order_api, BaseAPI))  # True
```

---

#### 题目3：异常处理与上下文管理（综合考察：自定义异常、try/except、上下文管理器）

**场景**：实现一个配置文件加载器，包含完整的异常处理。

**需求**：

**自定义异常**：
1. `ConfigError` 基类
2. `ConfigFileNotFoundError(ConfigError)` 文件不存在
3. `ConfigFormatError(ConfigError)` JSON 格式错误
4. `ConfigValidationError(ConfigError)` 字段验证失败

**load_config 函数**：
1. 从 JSON 文件加载配置
2. 文件不存在时抛出 `ConfigFileNotFoundError`
3. JSON 格式错误时抛出 `ConfigFormatError`
4. 必要字段缺失时抛出 `ConfigValidationError`
5. 使用 `try/except/finally` 确保资源释放
6. 支持验证必填字段

**ConfigLoader 上下文管理器**：
1. `__enter__` 加载配置文件
2. `__exit__` 清理资源，记录日志
3. `get(key, default=None)` 获取配置项
4. `validate(required_keys)` 验证必填字段

**测试用例**：
```python
import json
import os
import tempfile

# 创建临时配置文件
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump({"db_host": "localhost", "db_port": 3306}, f)
    config_file = f.name

# 测试1：正常加载
try:
    config = load_config(config_file, required_keys=["db_host", "db_port"])
    print(config)  # {'db_host': 'localhost', 'db_port': 3306}
except ConfigError as e:
    print(f"配置错误: {e}")

# 测试2：文件不存在
try:
    config = load_config("not_exist.json")
except ConfigFileNotFoundError as e:
    print(e)  # 配置文件不存在: not_exist.json

# 测试3：格式错误
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    f.write("{invalid json}")
    bad_file = f.name

try:
    config = load_config(bad_file)
except ConfigFormatError as e:
    print(e)  # 配置文件格式错误: ...

# 测试4：缺少必填字段
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump({"db_host": "localhost"}, f)  # 缺少 db_port
    missing_file = f.name

try:
    config = load_config(missing_file, required_keys=["db_host", "db_port"])
except ConfigValidationError as e:
    print(e)  # 缺少必填字段: ['db_port']

# 测试5：使用上下文管理器
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump({"api_key": "12345", "timeout": 30}, f)
    ctx_file = f.name

with ConfigLoader(ctx_file) as loader:
    print(loader.get("api_key"))  # 12345
    print(loader.get("not_exist", "default"))  # default

# 清理临时文件
os.unlink(config_file)
os.unlink(bad_file)
os.unlink(missing_file)
os.unlink(ctx_file)
```

---

#### 题目4：综合应用（综合考察：所有知识点）

**场景**：实现一个简单的测试用例运行器。

**需求**：

**TestCase 类**：
1. 属性：`name`、`priority`（P0-P3）、`status`、`duration`
2. `run()` 执行测试（模拟）
3. `__str__` 返回用例信息
4. `__lt__` 按优先级排序
5. `__bool__` 根据状态判断
6. `__call__` 直接调用等同于 run()

**TestSuite 类**：
1. 管理多个测试用例
2. `add_case(case)` 添加用例
3. `run_all()` 按优先级执行所有用例
4. `get_report()` 返回统计报告

**TestRunner 上下文管理器**：
1. `__enter__` 初始化测试环境
2. `__exit__` 清理测试环境，生成报告
3. 支持异常时清理

**自定义异常**：
1. `TestError` 基类
2. `TestFailedError` 测试失败
3. `TestTimeoutError` 测试超时

**测试用例**：
```python
# 创建测试用例
case1 = TestCase("登录测试", "P0")
case2 = TestCase("搜索测试", "P1")
case3 = TestCase("下单测试", "P0")

# 测试排序
cases = [case2, case1, case3]
cases.sort()
print([str(c) for c in cases])
# ['TestCase(登录测试, P0)', 'TestCase(下单测试, P0)', 'TestCase(搜索测试, P1)']

# 测试执行
result = case1()
print(case1.status)  # pass
if case1:  # __bool__
    print("测试通过")

# 创建测试套件
suite = TestSuite("冒烟测试")
suite.add_case(case1)
suite.add_case(case2)

# 使用上下文管理器运行
with TestRunner("测试报告") as runner:
    suite.run_all()
    print(suite.get_report())
# {'total': 2, 'passed': 2, 'failed': 0, 'duration': 0.2}
```

---

### 答案

#### 题目1 答案

```python
import re

class User:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email   # 通过 setter 验证
        self.age = age       # 通过 setter 验证

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # 简单验证：必须包含 @ 和 .
        if not value or '@' not in value or '.' not in value:
            raise ValueError("邮箱格式不正确")
        self._email = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0 or value > 150:
            raise ValueError("年龄必须在0-150之间")
        self._age = value

    def __str__(self):
        return f"用户: {self.username} ({self.age}岁)"

    def __lt__(self, other):
        """按年龄比较"""
        if not isinstance(other, User):
            return NotImplemented
        return self.age < other.age

    def __eq__(self, other):
        """按用户名比较"""
        if not isinstance(other, User):
            return NotImplemented
        return self.username == other.username
```

#### 题目2 答案

```python
import requests

class BaseAPI:
    """API 基类"""

    def __init__(self, base_url, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _build_url(self, endpoint):
        """构建完整 URL（私有方法）"""
        return f"{self.base_url}{endpoint}"

    def _log(self, method, url):
        """记录请求日志（受保护方法）"""
        print(f"[{method}] {url}")

    def send_request(self, method, endpoint, **kwargs):
        """发送请求"""
        url = self._build_url(endpoint)
        self._log(method, url)
        return self.session.request(method, url, timeout=self.timeout, **kwargs)


class UserAPI(BaseAPI):
    """用户 API"""

    def login(self, username, password):
        """登录"""
        return self.send_request("POST", "/login", json={
            "username": username,
            "password": password
        })

    def get_profile(self):
        """获取用户信息"""
        return self.send_request("GET", "/profile")

    def update_profile(self, data):
        """更新用户信息"""
        return self.send_request("PUT", "/profile", json=data)


class OrderAPI(BaseAPI):
    """订单 API"""

    def create_order(self, data):
        """创建订单"""
        return self.send_request("POST", "/orders", json=data)

    def get_orders(self):
        """获取订单列表"""
        return self.send_request("GET", "/orders")

    def cancel_order(self, order_id):
        """取消订单"""
        return self.send_request("DELETE", f"/orders/{order_id}")
```

#### 题目3 答案

```python
import json
from contextlib import contextmanager

# ================================
# 自定义异常
# ================================
class ConfigError(Exception):
    """配置错误基类"""
    pass


class ConfigFileNotFoundError(ConfigError):
    """配置文件不存在"""
    pass


class ConfigFormatError(ConfigError):
    """配置文件格式错误"""
    pass


class ConfigValidationError(ConfigError):
    """配置验证失败"""
    pass


# ================================
# 配置加载函数
# ================================
def load_config(filepath, required_keys=None):
    """加载配置文件"""
    required_keys = required_keys or []
    config = None
    file = None

    try:
        file = open(filepath, 'r', encoding='utf-8')
        config = json.load(file)
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"配置文件不存在: {filepath}")
    except json.JSONDecodeError as e:
        raise ConfigFormatError(f"配置文件格式错误: {e}")
    finally:
        if file:
            file.close()
            print("配置文件已关闭")

    # 验证必要字段
    missing = [k for k in required_keys if k not in config]
    if missing:
        raise ConfigValidationError(f"缺少必填字段: {missing}")

    return config


# ================================
# 配置加载器（上下文管理器）
# ================================
class ConfigLoader:
    """配置加载器上下文管理器"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.config = None
        self._file = None

    def __enter__(self):
        """进入上下文"""
        try:
            self._file = open(self.filepath, 'r', encoding='utf-8')
            self.config = json.load(self._file)
            print(f"配置加载成功: {self.filepath}")
            return self
        except FileNotFoundError:
            raise ConfigFileNotFoundError(f"配置文件不存在: {self.filepath}")
        except json.JSONDecodeError as e:
            raise ConfigFormatError(f"配置文件格式错误: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if self._file:
            self._file.close()
            print("配置文件已关闭")

        if exc_type is not None:
            print(f"发生异常: {exc_val}")

        return False  # 不抑制异常

    def get(self, key, default=None):
        """获取配置项"""
        if self.config is None:
            return default
        return self.config.get(key, default)

    def validate(self, required_keys):
        """验证必填字段"""
        if self.config is None:
            raise ConfigError("配置未加载")

        missing = [k for k in required_keys if k not in self.config]
        if missing:
            raise ConfigValidationError(f"缺少必填字段: {missing}")
        return True
```

#### 题目4 答案

```python
import time

# ================================
# 自定义异常
# ================================
class TestError(Exception):
    """测试错误基类"""
    pass


class TestFailedError(TestError):
    """测试失败"""
    def __init__(self, test_name, message=""):
        self.test_name = test_name
        super().__init__(f"测试失败 [{test_name}]: {message}")


class TestTimeoutError(TestError):
    """测试超时"""
    def __init__(self, test_name, timeout):
        self.test_name = test_name
        self.timeout = timeout
        super().__init__(f"测试超时 [{test_name}]: {timeout}秒")


# ================================
# 测试用例类
# ================================
class TestCase:
    """测试用例"""

    # 优先级映射（用于排序）
    PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

    def __init__(self, name, priority="P1"):
        self.name = name
        self.priority = priority
        self.status = None  # pending, passed, failed
        self.duration = 0
        self.error = None

    def run(self):
        """执行测试（模拟）"""
        start_time = time.time()

        try:
            # 模拟测试执行
            time.sleep(0.1)
            self.status = "passed"
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
        finally:
            self.duration = time.time() - start_time

        return self.status == "passed"

    def __str__(self):
        return f"TestCase({self.name}, {self.priority})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        """按优先级排序"""
        if not isinstance(other, TestCase):
            return NotImplemented
        return (self.PRIORITY_ORDER.get(self.priority, 99) <
                self.PRIORITY_ORDER.get(other.priority, 99))

    def __bool__(self):
        """根据状态判断"""
        return self.status == "passed"

    def __call__(self):
        """直接调用等同于 run()"""
        return self.run()


# ================================
# 测试套件类
# ================================
class TestSuite:
    """测试套件"""

    def __init__(self, name):
        self.name = name
        self.cases = []
        self.results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "duration": 0
        }

    def add_case(self, case):
        """添加测试用例"""
        self.cases.append(case)

    def run_all(self):
        """按优先级执行所有用例"""
        # 按优先级排序
        sorted_cases = sorted(self.cases)

        for case in sorted_cases:
            case.run()

        return self.get_report()

    def get_report(self):
        """获取统计报告"""
        self.results["total"] = len(self.cases)
        self.results["passed"] = sum(1 for c in self.cases if c.status == "passed")
        self.results["failed"] = sum(1 for c in self.cases if c.status == "failed")
        self.results["duration"] = sum(c.duration for c in self.cases)

        return self.results


# ================================
# 测试运行器（上下文管理器）
# ================================
class TestRunner:
    """测试运行器"""

    def __init__(self, report_name="测试报告"):
        self.report_name = report_name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        """进入上下文"""
        self.start_time = time.time()
        print(f"{'='*50}")
        print(f"开始执行: {self.report_name}")
        print(f"{'='*50}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        self.end_time = time.time()
        total_time = self.end_time - self.start_time

        print(f"{'='*50}")
        print(f"执行完成: {self.report_name}")
        print(f"总耗时: {total_time:.2f}秒")

        if exc_type is not None:
            print(f"发生异常: {exc_val}")

        print(f"{'='*50}")

        return False  # 不抑制异常
```

---

### 自测检查清单

完成以上练习后，检查自己是否掌握以下能力：

#### 基础能力（必须掌握）
- [ ] 能定义简单的类，包含 `__init__` 和实例方法
- [ ] 理解 `self` 的含义（指向当前实例）
- [ ] 能使用继承复用代码
- [ ] 能使用 `super()` 调用父类方法
- [ ] 能使用 try/except 处理常见异常
- [ ] 能编写简单的上下文管理器

#### 进阶能力（应该了解）
- [ ] 理解类方法和静态方法的区别
- [ ] 能使用 property 装饰器控制属性访问
- [ ] 能设计自定义异常体系
- [ ] 能使用魔术方法增强类的功能
- [ ] 能综合运用 OOP 知识设计测试工具类

#### 实战能力（综合应用）
- [ ] 能设计完整的类层次结构
- [ ] 能将异常处理与上下文管理器结合
- [ ] 能实现简单的测试框架
- [ ] 能编写可复用的工具类

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
