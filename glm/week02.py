# 定义 User 类
# 1. 包含 username, email, age 属性
# 2. __init__ 初始化
# 3. 定义 get_info() 方法返回用户信息字符串
# 4. 定义 is_adult() 方法判断是否成年


# class User:
#     def __init__(self, username, email, age):
#         self.username = username
#         self.email = email
#         self.age = age

#     def get_info(self):
#         return f"{self.username},{self.email},{self.age}"

#     def is_adult(self):
#         return self.age >= 18

# if __name__ == "__main__":
#     user = User("张三", "zhangsan@example.com", 25)
#     print(user.get_info())
#     print(user.is_adult())

# 创建 Counter 类
# 1. count 属性初始为 0
# 2. increment() 方法 count + 1
# 3. decrement() 方法 count - 1
# 4. reset() 方法重置为 0
# 5. get_count() 方法返回当前值


# class Counter:
#     def __init__(self) -> None:
#         self.count = 0

#     def increment(self):
#         self.count += 1

#     def decrement(self):
#         self.count -= 1

#     def reset(self):
#         self.count = 0

#     def get_count(self):
#         return self.count

# 创建 Student 类
# 1. 类属性 school_name = "测试学校"
# 2. 实例属性 name, grade
# 3. 实例方法 get_info()
# 4. 类方法 change_school(cls, name)
# 5. 静态方法 is_passing(score)


# class Student:
#     school_name = "测试学校"

#     def __init__(self, name, grade) -> None:
#         self.name = name
#         self.grade = grade

#     def get_info(self):
#         return f"{self.name},{self.grade}"

#     @classmethod
#     def change_school(cls, name):
#         cls.school_name = name

#     @staticmethod
#     def is_passing(score):
#         return score >= 60

# 创建动物类层次
# 1. Animal 基类：name 属性，speak() 方法
# 2. Dog 子类：继承 Animal，重写 speak() 返回 "汪汪"
# 3. Cat 子类：继承 Animal，重写 speak() 返回 "喵喵"
# 4. Bird 子类：继承 Animal，新增 fly() 方法


# class Animal:
#     def __init__(self, name) -> None:
#         self.name = name

#     def speak(self):
#         return "foo class"


# class Dog(Animal):
#     def speak(self):
#         return "wang wang"


# class Cat(Animal):
#     def speak(self):
#         return "miao miao"


# class Bird(Animal):
#     def speak(self):
#         return "ji ji"

#     def fly(self):
#         return "fly"


# if __name__ == "__main__":
#     dog = Dog("xx")
#     cat = Cat("yy")
#     bird = Bird("zz")

#     print(dog.speak())
#     print(cat.speak())
#     print(bird.speak())
#     print(bird.fly())

# # 创建员工类
# # 1. Employee 基类：name, salary, get_bonus() 返回 salary * 0.1
# # 2. Manager 子类：继承 Employee，新增 team_size
# # 3. 重写 get_bonus() 返回 salary * 0.2 + team_size * 100
# # 4. 使用 super() 调用父类方法


# class Employee:
#     def __init__(self, name, salary):
#         self.name = name
#         self.salary = salary

#     def get_bonus(self):
#         return self.salary * 0.1


# class Manager(Employee):
#     def __init__(self, name, salary, team_size):
#         super().__init__(name, salary)
#         self.team_size = team_size

#     def get_bonus(self):
#         return super().get_bonus() * 2 + self.team_size * 100


# if __name__ == "__main__":
#     emp = Employee("张三", 10000)
#     mgr = Manager("李四", 20000, 5)

#     print(f"{emp.name} 奖金：{emp.get_bonus()}")  # 1000.0
#     print(f"{mgr.name} 奖金：{mgr.get_bonus()}")  # 4000.0 + 500 = 4500.0

# # 创建 Product 类
# # 1. 私有属性 _price
# # 2. @property getter
# # 3. @price.setter 验证 price > 0
# # 4. @price.deleter 打印删除信息
# # 5. @property 只读属性 discount_price


# class Product:
#     def __init__(self, price):
#         self._price = price

#     @property
#     def price(self):
#         return self._price

#     @price.setter
#     def price(self, value):
#         if value <= 0:
#             raise ValueError("value must be > 0")
#         self._price = value

#     @price.deleter
#     def price(self):
#         print("删除价格属性")
#         del self._price

#     @property
#     def discount_price(self):
#         return self._price * 0.9

# # 编写安全除法函数
# # 1. safe_divide(a, b) 处理除零异常
# # 2. 返回结果或错误信息
# # 3. 使用 try/except/else/finally
# # 4. 记录日志

# import logging

# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )


# def safe_divide(a, b):
#     try:
#         result = a / b
#         return result
#     except ZeroDivisionError as e:
#         logging.error(f"error :{e}")
#         return "no / 0"
#     else:
#         logging.info(f"{a} / {b}= {result}")
#         return result
#     finally:
#         logging.info(f"{a} / {b}")

# # 定义测试相关异常
# # 1. TestError 基类
# # 2. TestNotFoundError 继承 TestError
# # 3. TestTimeoutError 继承 TestError
# # 4. TestAssertionError 继承 TestError
# # 5. 每个异常包含 message 和 code 属性


# class TestError(Exception):
#     def __init__(self, code, message):
#         super.__init__(message)
#         self.code = code
#         self.message = message


# class TestNotFoundError(TestError):
#     def __init__(self, code=404, message="测试没找到"):
#         super().__init__(code, message)


# class TestTimeoutError(TestError):
#     def __init__(self, code=408, message="测试超时"):
#         super().__init__(code, message)


# class TestAssertionError(TestError):
#     def __init__(self, code=422, message="断言失败"):
#         super().__init__(code, message)

# import requests
# import logging
# import time


# class HttpClient:
#     """HTTP 客户端"""

#     # 要求：
#     # 1. 支持设置 base_url 和 timeout
#     # 2. 支持 get/post/put/delete 方法
#     # 3. 自动记录请求日志
#     # 4. 支持重试机制
#     # 5. 使用 property 验证 timeout > 0
#     def __init__(self, base_url, timeout=5.0):
#         self.base_url = base_url.rstrip("/")
#         self._timeout = timeout
#         self.session = requests.Session()
#         self._setup_logging()

#     def _setup_logging(self):
#         self.logger = logging.getLogger(f"{__name__}.HttpClient")
#         if not self.logger.handlers:
#             handler = logging.StreamHandler()
#             formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
#             handler.setFormatter(formatter)
#             self.logger.addHandler(handler)
#             self.logger.setLevel(logging.INFO)

#     @property
#     def timeout(self):
#         return self._timeout

#     @timeout.setter
#     def timeout(self, value):
#         if value <= 0:
#             raise ValueError("value must be > 0")
#         self._timeout = value

#     def _request(
#         self, method: str, url: str, retries: int = 3, **kwargs
#     ) -> requests.Response:
#         full_url = f"{self.base_url}{url}"
#         kwargs.setdefault("timeout", self.timeout)

#         for attempt in range(1, retries + 1):
#             try:
#                 self.logger.info(
#                     f"Request:{method.upper()}{full_url}(attempt {attempt})"
#                 )
#                 response = self.session.request(method, full_url, **kwargs)
#                 self.logger.info(f"Response:{response.status_code}{response.reason}")
#                 return response
#             except requests.RequestException as e:
#                 self.logger.warning(f"Request failed (attempt {attempt}):{e}")
#                 if attempt == retries:
#                     raise
#                 time.sleep(2**attempt)

#     def get(self, url, params=None, **kwargs):
#         return self._request("get", url, params=params, **kwargs)

#     def post(self, url, data=None, **kwargs):
#         return self._request("post", url, data=data, **kwargs)

#     def close(self):
#         self.session.close()


# if __name__ == "__main__":
#     client = HttpClient("https://jsonplaceholder.typicode.com", timeout=2.0)
#     try:
#         resp = client.get("/posts/1")
#         print(resp.json())
#     except Exception as e:
#         print(f"Error:{e}")
#     finally:
#         client.close()
# import random
# import time


# class TestCase:
#     """测试用例"""

#     # name, priority, status, duration 属性
#     # __str__ 和 __lt__（按优先级排序）
#     def __init__(self, name, priority, status, duration):
#         self.name = name
#         self.priority = priority
#         self.status = status
#         self.duration = duration

#     def __str__(self):
#         return f"[{self.priority}] {self.name}: {self.status} ({self.duration}s)"

#     def __lt__(self, other):
#         def priority_value(prio):
#             return int(prio[1:]) if prio.startswith("P") and prio[1:].isdigit() else 999

#         return priority_value(self.priority) < priority_value(other.priority)


# class TestSuite:
#     """测试套件"""

#     # add_case(), run_all(), get_report()
#     # 按优先级排序执行

#     def __init__(self):
#         self.cases = []

#     def add_case(self, test_case):
#         self.cases.append(test_case)

#     def run_all(self):
#         sorted_cases = sorted(self.cases)
#         for case in sorted_cases:
#             print(f"正在执行：{case.name}(优先级{case.priority})")
#             case.duration = round(random.uniform(0.1, 1.0), 2)
#             rand = random.random()
#             if rand < 0.8:
#                 case.status = "pass"
#             elif rand < 0.9:
#                 case.status = "fail"
#             else:
#                 case.status = "skip"
#             time.sleep(case.duration)
#             print(f"结果：{case.status}(耗时{case.duration}s)")

#     def get_report(self):
#         total = len(self.cases)
#         passed = sum(1 for c in self.cases if c.status == "pass")
#         failed = sum(1 for c in self.cases if c.status == "fail")
#         skipped = sum(1 for c in self.cases if c.status == "skip")
#         executed = [c for c in self.cases if c.status != "pending"]
#         avg_duration = (
#             sum(c.duration for c in executed) / len(executed) if executed else 0.0
#         )
#         pass_rate = (passed / total * 100) if total > 0 else 0.0

#         report = {
#             "total": total,
#             "passed": passed,
#             "failed": failed,
#             "skipped": skipped,
#             "pass_rate": f"{pass_rate:.1f}%",
#             "avg_duration": round(avg_duration, 2),
#             "details": [str(c) for c in self.cases],
#         }
#         return report

# import time
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import text

# class DBConnection:
#     """数据库连接上下文管理器"""

#     # __enter__: 建立连接
#     # __exit__: 关闭连接，异常时回滚
#     # 记录连接时间

#     def __init__(self, db_url: str):
#         self.engine = create_engine(db_url)
#         self.Session = sessionmaker(bind=self.engine)
#         self.seesion = None
#         self.start_time = None
#         self.end_time = None

#     def __enter__(self):
#         self.start_time = time.time()
#         self.seesion = self.Session()
#         # 可选：执行一次简单查询确保连接已建立（SQLAlchemy 延迟连接，首次使用时才真正连接）
#         # 如果希望立即看到连接时间，可以取消下面注释：
#         # self.session.execute("SELECT 1")
#         print(f"连接已建立，耗时：{time.time() - self.start_time:.3f}s")
#         return self.seesion

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if exc_type is not None:
#             self.seesion.rollback()
#             print(f"发生异常：{exc_val},已回滚")
#         else:
#             self.seesion.commit()

#         self.seesion.close()
#         self.end_time = time.time()
#         print(f"连接关闭，总时长：{self.end_time - self.start_time:.3f}s")
#         return False


# if __name__ == "__main__":
#     db_url = "sqlite:///:memory:"

#     with DBConnection(db_url) as session:
#         session.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))
#         session.execute(text("INSERT INTO test (name) VALUES (:name)"), {"name": "Alice"})

#     try:
#         with DBConnection(db_url) as session:
#             session.execute(text("INSERT INFO test (name) VALUES (:name)"), {"name": "Bob"})
#             raise ValueError("模拟错误")
#     except Exception as e:
#         print(f"捕获到异常：{e}")

# import os
# import json
# import copy

# try:
#     import yaml

#     YAML_AVAILABLE = True
# except ImportError:
#     YAML_AVAILABLE = False


# class Config:
#     """配置管理"""

#     # 1. 从字典/JSON/YAML 加载
#     # 2. 支持点号访问 config.get("db.host")
#     # 3. 支持环境变量覆盖
#     # 4. 验证必填字段
#     # 5. 导出为字典
#     def __init__(self, source=None, env_prefix="CONFIG_", required=None):
#         self._config = {}
#         self.env_prefix = env_prefix
#         self.required = required

#         if source is None:
#             self._config = {}
#         elif isinstance(source, dict):
#             self._config = source.copy()
#         elif isinstance(source, str):
#             self._load_from_file(source)
#         else:
#             raise TypeError("source must be dict ,str (file path),or None")

#     def _load_from_file(self, path: str):
#         if path.endswith(".json"):
#             with open(path, "r", encoding="utf-8") as f:
#                 self._config = json.load(f)
#         elif path.endswith((".yaml", ".yml")):
#             if not YAML_AVAILABLE:
#                 raise ImportError(
#                     "PyYAML is required to load YAML files.Install with: pip install pyyaml"
#                 )
#             with open(path, "r", encoding="utf-8") as f:
#                 self._config = yaml.safe_load(f)
#         else:
#             raise ValueError("Unsupported file format. Use .json, .yaml, or .yml")

#     def _apply_env_overrides(self):
#         prefix = self.env_prefix
#         for env_key, env_value in os.environ.items():
#             if env_key.startswith(prefix):
#                 config_key = env_key[len(prefix) :].lower().replace("_", ".")
#                 parsed_value = self._parse_env_value(env_value)
#                 self._set_nested(config_key, parsed_value)

#     def _parse_env_value(self, value: str):
#         value = value.strip()
#         if value == "" or value.lowr() == "null":
#             return None
#         if value.lower() == "true":
#             return True
#         if value.lower() == "false":
#             return False

#         try:
#             if "." in value:
#                 return float(value)
#             else:
#                 return int(value)
#         except ValueError:
#             return value

#     def _set_nested(self, key: str, value):
#         keys = key.split(".")
#         target = self._config
#         for k in keys[:-1]:
#             if k not in target or not isinstance(target[k], dict):
#                 target[k] = {}
#             target = target[k]
#         target[keys[-1]] = value

#     def _validate_required(self):
#         missing = []
#         for key in self.required:
#             if self.get(key) is None:
#                 missing.append(key)
#         if missing:
#             raise ValueError(
#                 f"Missing required configuration keys: {', '.join(missing)}"
#             )

#     def get(self, key: str, default=None):
#         keys = key.split(".")
#         current = self._config
#         for k in keys:
#             if isinstance(current, dict) and k in current:
#                 current = current[k]
#             else:
#                 return default
#         return current

#     def to_dict(self):
#         return copy.deepcopy(self._config)

# **练习13：日志记录器类**

# **场景说明**：创建简易日志记录器，支持不同级别和输出目标。

# **具体需求**：
# 1. 日志级别：`INFO`、`WARN`、`ERROR`，默认级别为 `INFO`
# 2. 输出目标：支持输出到控制台和文件
# 3. 日志格式：`[2024-01-15 10:30:45] [INFO] 这是一条日志`
# 4. 使用单例模式（多次创建返回同一个实例）
# 5. 方法 `info(msg)`、`warn(msg)`、`error(msg)`
# 6. 方法 `set_level(level)` 设置最低输出级别
# 7. 方法 `set_file(filepath)` 设置日志文件路径


# import threading
# import datetime


# class Logger:
#     _instance = None
#     _lock = threading.Lock()

#     LEVELS = {"INFO": 10, "WARN": 20, "ERROR": 30}

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             with cls._lock:
#                 if cls._instance is None:
#                     cls._instance = super().__new__(cls)
#         return cls._instance

#     def __init__(self):
#         if not hasattr(self, "_initialized"):
#             self.level = self.LEVELS["INFO"]
#             self.file_path = None
#             self.file_handle = None

#     def _formatted_message(self, level, msg):
#         now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         return f"[{now}] [{level}] {msg}"

#     def _write(self, formatted_msg):
#         print(formatted_msg)

#         if self.file_path:
#             try:
#                 with open(self.file_path, "a", encoding="utf-8") as f:
#                     f.write(formatted_msg + "\n")
#             except Exception as e:
#                 print(f"[ERROR] 无法写入日志文件：{e}")

#     def _log(self, level, msg):
#         if self.LEVELS.get(level, 0) >= self.level:
#             fomatted = self._formatted_message(level, msg)
#             self._write(fomatted)

#     def info(self, msg):
#         self._log("INFO", msg)

#     def warn(self, msg):
#         self._log("WARN", msg)

#     def error(self, msg):
#         self._log("ERROR", msg)

#     def set_level(self, level):
#         if level.upper() in self.LEVELS:
#             self._level = self.LEVELS[level.upper()]
#         else:
#             print(f"无效的日志级别：{level},可选：{list(self.LEVELS.keys())}")

#     def set_file(self, filepath):
#         self.file_path = filepath
#         try:
#             with open(filepath, "a", encoding="utf-8"):
#                 pass
#         except Exception as err:
#             print(f"无法创建或写入日志文件 {filepath}: {err}")
#             self.file_path = None


# # **练习14：测试数据工厂**

# # **场景说明**：创建测试数据工厂，快速生成测试数据。

# # **具体需求**：
# # 1. `@classmethod create_user(**kwargs)` 创建用户数据：
# #    - 默认值：`{"id": 1, "name": "测试用户", "email": "test@example.com", "age": 25}`
# #    - 支持通过 kwargs 覆盖默认值

# # 2. `@classmethod create_order(**kwargs)` 创建订单数据：
# #    - 默认值：`{"order_id": "ORD001", "user_id": 1, "amount": 100.0, "status": "pending"}`

# # 3. `@classmethod create_product(**kwargs)` 创建商品数据：
# #    - 默认值：`{"product_id": 1, "name": "测试商品", "price": 99.9, "stock": 100}`

# # 4. `@classmethod create_batch(creator, count, **kwargs)` 批量生成数据：
# #    - `creator` 是上面的创建方法
# #    - `count` 是生成数量
# #    - 自动递增 ID

# # 5. `@classmethod save_to_file(data, filepath, format="json")` 保存数据到文件

# import json


# class TestDataFactory:
#     @classmethod
#     def create_user(cls, **kwargs):
#         defaults = {"id": 1, "name": "测试用户", "email": "test@example.com", "age": 25}
#         defaults.update(kwargs)
#         return defaults

#     @classmethod
#     def create_order(cls, **kwargs):
#         defaults = {
#             "order_id": "ORD001",
#             "user_id": 1,
#             "amount": 100.0,
#             "status": "pending",
#         }
#         defaults.update(cls, kwargs)
#         return defaults

#     @classmethod
#     def create_product(cls, **kwargs):
#         defaults = {"product_id": 1, "name": "测试商品", "price": 99.9, "stock": 100}
#         defaults.update(kwargs)
#         return defaults

#     @classmethod
#     def create_batch(cls, creator, count, **kwargs):
#         results = []
#         for i in range(count):
#             data = creator(**kwargs)
#             for key in list(data.keys()):
#                 if key.endswith("id"):
#                     data[key] += i
#             results.append(data)
#         return results

#     @classmethod
#     def save_to_file(data, filepath, format="json"):
#         if format.lower() == "json":
#             with open(filepath, "w", encoding="utf-8") as f:
#                 json.dumps(data, f, ensure_ascii=False, indent=2)
#         else:
#             raise ValueError("format error")


# import re
# import json


# class DataFactory:
#     _USER_DEFAULT = {
#         "id": 1,
#         "name": "测试用户",
#         "email": "test@example.com",
#         "age": 25,
#     }
#     _ORDER_DEFAULT = {
#         "order_id": "ORD001",
#         "user_id": 1,
#         "amount": 100.0,
#         "status": "pending",
#     }
#     _PRODUCT_DEFAULT = {
#         "product_id": 1,
#         "name": "测试商品",
#         "price": 99.9,
#         "stock": 100,
#     }

#     @classmethod
#     def create_user(cls, **kwargs):
#         data = cls._USER_DEFAULT.copy()
#         data.update(kwargs)
#         return data

#     @classmethod
#     def create_order(cls, **kwargs):
#         data = cls._ORDER_DEFAULT.copy()
#         data.update(kwargs)
#         return data

#     @classmethod
#     def create_product(cls, **kwargs):
#         data = cls._PRODUCT_DEFAULT.copy()
#         data.update(kwargs)
#         return data

#     @classmethod
#     def _auto_increment_id(cls, base_value, index):
#         if isinstance(base_value, int):
#             return base_value + index - 1
#         elif isinstance(base_value, str):
#             match = re.match(r"^(.*?)(\d+)$", base_value)
#             if match:
#                 prefix, num_str = match.groups()
#                 num = int(num_str)
#                 new_num = num + index - 1
#                 new_num_str = str(new_num).zfill(len(num_str))
#                 return f"{prefix}{new_num_str}"
#             else:
#                 return f"{base_value}{index}"
#         else:
#             raise TypeError(f"无法为类型{type(base_value)}自增ID")

#     @classmethod
#     def create_batch(cls, creator, count, id_field=None, **kwargs):
#         sample = creator()
#         if id_field is None:
#             for field in sample.keys():
#                 if "id" in field.lower():
#                     id_field = field
#                     break
#             if id_field is None:
#                 raise ValueError("无法自动识别 ID 字段")

#         base_id_value = kwargs.get(id_field)
#         if base_id_value is None:
#             base_id_value = sample.get(id_field)
#         if base_id_value is None:
#             raise ValueError(f"样本数据中不存在字段 '{id_field}'")

#         result = []
#         for i in range(1, count + 1):
#             new_id = cls._auto_increment_id(base_id_value, i)
#             current_kwargs = {**kwargs, id_field: new_id}

#             result.append(creator(**current_kwargs))
#         return result

#     @classmethod
#     def save_to_file(cls, data, filepath, format="json"):
#         if format.lower() == "json":
#             with open(filepath, "w", encoding="utf-8") as f:
#                 json.dump(data, f, ensure_ascii=False, indent=2)
#         else:
#             raise ValueError("format error")


# if __name__ == "__main__":
#     # 1. 自动识别 ID 字段（user 的 id 是整数）
#     users = DataFactory.create_batch(DataFactory.create_user, 3, name="批量用户")
#     print("批量用户（整数ID递增）:")
#     for u in users:
#         print(f"  {u}")

#     # 2. 订单的 order_id 是字符串数字拼接
#     orders = DataFactory.create_batch(DataFactory.create_order, 3, amount=199.99)
#     print("批量订单（字符串数字递增）:")
#     for o in orders:
#         print(f"  {o}")

#     # 3. 商品自定义 ID 字段名（product_id）
#     products = DataFactory.create_batch(
#         DataFactory.create_product, 2, name="特价商品", price=49.9
#     )
#     print("批量商品（自动识别 product_id）:")
#     for p in products:
#         print(f"  {p}")

#     # 4. 手动指定 ID 字段（覆盖自动识别）
#     users_custom = DataFactory.create_batch(
#         DataFactory.create_user, 2, id_field="user_id", user_id=100, name="自定义ID"
#     )
#     print("手动指定ID字段:")
#     for u in users_custom:
#         print(f"  {u}")


# **练习15：断言库类**

# **场景说明**：创建自定义断言库，提供更友好的断言方法。

# **具体需求**：
# 1. `@staticmethod equal(actual, expected, msg="")` 断言相等
# 2. `@staticmethod not_equal(a, b, msg="")` 断言不相等
# 3. `@staticmethod contains(item, container, msg="")` 断言包含
# 4. `@staticmethod raises(func, exception, msg="")` 断言抛出异常
# 5. `@staticmethod json_equal(actual, expected, ignore_keys=[])` 比较 JSON（忽略指定键）
# 6. 所有断言失败时抛出 `AssertionError`，消息格式：`"断言失败: 期望 {expected}, 实际 {actual}. {msg}"`

# import json


# class Assert:
#     @staticmethod
#     def equal(actual, expected, msg=""):
#         if actual != expected:
#             raise AssertionError(f"断言失败: 期望 {expected}, 实际 {actual}. {msg}")

#     @staticmethod
#     def not_equal(a, b, msg=""):
#         if a == b:
#             raise AssertionError(f"断言失败: 期望 {b}, 实际 {a}. {msg}")

#     @staticmethod
#     def contains(item, container, msg=""):
#         if item not in container:
#             raise AssertionError(
#                 f"断言失败: 期望 {item}在{container}里, 实际没在. {msg}"
#             )

#     @staticmethod
#     def raises(func, exception, msg=""):
#         try:
#             func()
#         except exception:
#             return
#         except Exception as e:
#             error_msg = f"断言失败：期望抛出{exception.__name__},实际抛出{type(e).__name__}.{msg}"
#             raise AssertionError(error_msg) from e
#         else:
#             error_msg = f"断言失败：期望抛出{exception.__name__},实际未抛出异常.{msg}"
#             raise AssertionError(error_msg)

#     @staticmethod
#     def json_equal(actual, expected, ignore_keys=[], msg=""):
#         ignore_set = set(ignore_keys or [])

#         def collect_diff(obj1, obj2, path=""):
#             diffs = []
#             if path in ignore_set:
#                 return diffs

#             if type(obj1) is not type(obj2):
#                 diffs.append(
#                     path, f"类型不同：{type(obj1).__name__} vs {type(obj2).__name__}"
#                 )
#                 return diffs

#             if isinstance(obj1, dict):
#                 keys1 = set(obj1.keys())
#                 keys2 = set(obj2.keys())

#                 all_keys = keys1 | keys2
#                 for key in all_keys:
#                     child_path = f"{path}.{key}" if path else key
#                     if child_path in ignore_set:
#                         continue
#                     if key not in obj1:
#                         diffs.append((child_path, obj2[key], "缺失"))
#                     elif key not in obj2:
#                         diffs.append((child_path, "缺失", obj1[key]))
#                     else:
#                         diffs.extend(collect_diff(obj1[key], obj2[key], child_path))
#                 return diffs

#             elif isinstance(obj1, list):
#                 if len(obj1) != len(obj2):
#                     diffs.append(path, f"长度{len(obj2)}", f"长度{len(obj1)}")
#                     min_len = min(len(obj1), len(obj2))
#                     # for idx, (item1, item2) in enumerate(zip(obj1, obj2)):
#                     for idx in range(min_len):
#                         child_path = f"{path}[{idx}]"
#                         if child_path in ignore_set:
#                             continue
#                         diffs.extend(collect_diff(obj1[idx], obj2[idx], child_path))
#                     if len(obj1) > len(obj2):
#                         for idx in range(len(obj2), len(obj1)):
#                             child_path = f"{path}[{idx}]"
#                             diffs.append((child_path, "缺失", obj1[key]))
#                     elif len(obj1) < len(obj2):
#                         for idx in range(len(obj1), len(obj2)):
#                             child_path = f"{path}[{idx}]"
#                             diffs.append((child_path, obj2[key], "缺失"))
#                     return diffs
#                 else:
#                     for idx, (item1, item2) in enumerate(zip(obj1, obj2)):
#                         child_path = f"{path}[{idx}]"
#                         if child_path in ignore_set:
#                             continue
#                         diffs.extend(collect_diff(item1, item2, child_path))
#             else:
#                 if obj1 != obj2:
#                     diffs.append((path, obj2, obj1))
#                 return diffs

#         diffs = collect_diff(actual, expected)
#         if diffs:
#             diff_lines = []
#             for path, exp_val, act_val in diffs:
#                 exp_str = (
#                     json.dumps(exp_val, ensure_ascii=False, indent=2)
#                     if not isinstance(exp_val, str)
#                     else repr(exp_val)
#                 )
#                 act_str = (
#                     json.dumps(act_val, ensure_ascii=False, indent=2)
#                     if not isinstance(act_val, str)
#                     else repr(act_val)
#                 )
#                 diff_lines.append(f"  {path}:期望 {exp_str}, 实际 {act_str}")
#             diff_text = "\n".join(diff_lines)
#             # actual_str = json.dumps(actual, ensure_ascii=False, indent=2)
#             # expected_str = json.dumps(expected, ensure_ascii=False, indent=2)
#             error_msg = (
#                 # f"JSON 断言失败：期望{expected_str},实际{actual_str}.\n"
#                 f"差异详情：\n{diff_text}\n{msg}"
#             )
#             raise AssertionError(error_msg)


# # 使用示例
# if __name__ == "__main__":
#     # 测试 equal
#     Assert.equal(1, 1)  # 通过
#     try:
#         Assert.equal(1, 2, "值不匹配")
#     except AssertionError as e:
#         print(e)  # 断言失败: 期望 2, 实际 1. 值不匹配

#     # 测试 not_equal
#     Assert.not_equal(1, 2)  # 通过
#     try:
#         Assert.not_equal(1, 1)
#     except AssertionError as e:
#         print(e)

#     # 测试 contains
#     Assert.contains(2, [1, 2, 3])  # 通过
#     try:
#         Assert.contains(4, [1, 2, 3])
#     except AssertionError as e:
#         print(e)

#     # 测试 raises
#     def raise_error():
#         raise ValueError("test error")

#     def no_error():
#         pass

#     Assert.raises(raise_error, ValueError)  # 通过
#     try:
#         Assert.raises(no_error, ValueError)
#     except AssertionError as e:
#         print(e)

#     # 测试 json_equal
#     actual = {
#         "id": 1,
#         "name": "Alice",
#         "age": 25,
#         "address": {"city": "Beijing", "zip": 100000},
#     }
#     expected = {
#         "id": 3,
#         "name": "Alice",
#         "address": {"city": "Shanghai", "zip": 200000},
#     }
#     try:
#         Assert.json_equal(actual, expected, ignore_keys=["address.city"])
#     except AssertionError as e:
#         print(e)  # 忽略 city 后，两者相等

# **练习16：API 封装类**

# **场景说明**：封装 API 接口，方便测试调用。

# **具体需求**：

# **BaseAPI 基类**：
# 1. `__init__(self, base_url)` 初始化
# 2. `send_request(method, endpoint, **kwargs)` 发送请求
# 3. `_build_url(endpoint)` 构建完整 URL（私有方法）
# 4. `_log_request(method, url)` 记录请求日志（受保护方法）

# **UserAPI 子类**：
# 1. 继承 `BaseAPI`
# 2. `login(username, password)` 登录接口，POST `/login`
# 3. `logout()` 登出接口，POST `/logout`
# 4. `get_profile()` 获取用户信息，GET `/profile`
# 5. `update_profile(data)` 更新用户信息，PUT `/profile`
# 6. `delete_account()` 删除账户，DELETE `/account`

# import requests
# import logging


# class BaseAPI:
#     def __init__(self, base_url: str):
#         self.base_url = base_url.rstrip("/")
#         self.session = requests.Session()
#         self._setup_logging()

#     def _setup_logging(self):
#         self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
#         if not self.logger.handler:
#             handler = logging.StreamHandler()
#             formatter = logging.Formatter(
#                 "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#             )
#             handler.setFormatter(formatter)
#             self.logger.addHandler(handler)
#             self.logger.setLevel(logging.INFO)

#     def send_request(self, method: str, endpoint, **kwargs):
#         method = method.lower()
#         url = self._build_url(endpoint)
#         self._log_request(method, url)
#         req_func = getattr(self.session, method, None)
#         if req_func is None:
#             raise ValueError(f"不支持的 HTTP 方法： {method}")

#         try:
#             response = req_func(url, **kwargs)
#             self.logger.info(f"Response:{response.status_code} - {response.reason}")
#             return response
#         except requests.RequestException as e:
#             self.logger.error(f"请求异常：{e}")
#             raise

#     def _build_url(self, endpoint: str):
#         endpoint = endpoint.lstrip("/")
#         return f"{self.base_url}/{endpoint}"

#     def _log_request(self, method, url):
#         self.logger.info(f"Request:{method.upper()}{url}")


# class UserAPI(BaseAPI):
#     def login(self, username: str, password: str, **kwargs):
#         data = {"username": username, "password": password}
#         return self.send_request("post", "/login", json=data, **kwargs)

#     def logout(self, **kwargs):
#         return self.send_request("post", "/logout", **kwargs)

#     def get_profile(self, **kwargs):
#         return self.send_request("get", "/profile", **kwargs)

#     def update_profile(self, data, **kwargs):
#         return self.send_request("put", "/profile", **kwargs)

#     def delete_account(self, **kwargs):
#         return self.send_request("delete", "/account", **kwargs)

# if __name__ == "__main__":
#     api = UserAPI("https://jsonplaceholder.typicode.com")

#     resp = api.get_profile()
#     print(resp.status_code)

# **练习17：迷你测试框架**

# **场景说明**：实现一个简单的测试框架，类似 Pytest 的核心功能。

# **具体需求**：

# **TestResult 类**：
# 1. 属性：`passed`（通过数）、`failed`（失败数）、`errors`（错误列表）
# 2. 方法 `add_pass()` 通过数 +1
# 3. 方法 `add_failure(test_name, error)` 记录失败
# 4. 方法 `summary()` 返回统计字符串：`"3 passed, 1 failed"`

# **TestRunner 类**：
# 1. `__init__(self, test_class)` 接收测试类
# 2. `run()` 执行所有 `test_` 开头的方法
# 3. 支持 `setup()` 在每个测试前执行
# 4. 支持 `teardown()` 在每个测试后执行
# 5. 返回 `TestResult` 对象


# class TestResult:
#     def __init__(self):
#         self.passed = 0
#         self.failed = 0
#         self.errors = []

#     def add_pass(self):
#         self.passed += 1

#     def add_failure(self, test_name, error):
#         self.failed += 1
#         error_msg = str(error) if str(error) else f"Assertion failed in {test_name}"
#         self.errors.append((test_name, error_msg))

#     def summary(self):
#         return f"{self.passed} passed, {self.failed} failed"


# class TestRunner:
#     def __init__(self, test_class):
#         self.test_class = test_class

#     def run(self):
#         result = TestResult()
#         instance = self.test_class()
#         test_methods = [
#             method
#             for method in dir(instance)
#             if method.startswith("test_") and callable(getattr(instance, method))
#         ]

#         for method_name in test_methods:
#             if hasattr(instance, "setup") and callable(instance.setup):
#                 try:
#                     instance.setup()
#                 except Exception as e:
#                     result.add_failure(method_name, f"setup failed:{e}")
#                     if hasattr(instance, "teardown") and callable(instance.teardown):
#                         try:
#                             instance.teardown()
#                         except Exception:
#                             pass
#                     continue

#             test_func = getattr(instance, method_name)
#             try:
#                 test_func()
#                 result.add_pass()
#             except AssertionError as e:
#                 result.add_failure(method_name, e)
#             except Exception as e:
#                 result.add_failure(method_name, f"unexpected error: {e}")

#             if hasattr(instance, "teardown") and callable(instance.teardown):
#                 try:
#                     instance.teardown()
#                 except Exception:
#                     pass
#         return result


# if __name__ == "__main__":

#     class MyTests:
#         def setup(self):
#             print("初始化测试环境")

#         def teardown(self):
#             print("清理测试环境")

#         def test_add(self):
#             assert 1 + 1 == 2

#         def test_subtract(self):
#             assert 2 - 1 == 1

#         def test_fail(self):
#             assert 1 == 2  # 这个会失败

#     # 运行测试
#     runner = TestRunner(MyTests)
#     result = runner.run()
#     print(result.summary())
#     # 输出: 2 passed, 1 failed
#     for name, err in result.errors:
#         print(f"FAIL: {name} -> {err}")


# **练习18：缓存装饰器类**

# **场景说明**：实现方法结果缓存，避免重复计算。

# **具体需求**：
# 1. `__init__(self, expire_seconds=60)` 设置缓存过期时间
# 2. `__call__(self, func)` 使其可以作为装饰器使用
# 3. 缓存方法的返回值
# 4. 支持设置过期时间
# 5. 方法 `clear_cache()` 手动清除缓存
# 6. 使用 `threading.Lock` 保证线程安全


# import functools
# import threading
# import time


# class CacheDecorator:
#     def __init__(self, expire_seconds=60):
#         self.expire_seconds = expire_seconds
#         self._cache = {}
#         self._lock = threading.Lock()

#     def __call__(self, func):
#         @functools.wraps(func)
#         def warpper(*args, **kwargs):
#             key = (args, frozenset(kwargs.items()))
#             with self._lock:
#                 if key in self._cache:
#                     value, timestamp = self._cache[key]
#                     if time.time() - timestamp <= self.expire_seconds:
#                         print("读的缓存")
#                         return value

#             result = func(*args, **kwargs)
#             with self._lock:
#                 self._cache[key] = (result, time.time())
#             print("没读缓存")
#             return result

#         def clear_cache():
#             with self._lock:
#                 self._cache.clear()
#                 print("清除缓存")

#         warpper.clear_cache = clear_cache
#         return warpper


# if __name__ == "__main__":

#     @CacheDecorator(expire_seconds=2)
#     def expensive_computation(n):
#         print(f"计算中... n={n}")
#         time.sleep(1)  # 模拟耗时计算
#         return n * n

#     # 第一次调用（会执行计算）
#     result1 = expensive_computation(5)
#     # 输出: 计算中... n=5
#     print(result1)  # 25

#     # 第二次调用（使用缓存）
#     result2 = expensive_computation(5)
#     # 不输出 "计算中..."
#     print(result2)  # 25

#     # 等待缓存过期
#     time.sleep(3)
#     result3 = expensive_computation(5)
#     # 输出: 计算中... n=5（重新计算）
#     print(result3)  # 25

#     # 手动清除缓存
#     expensive_computation.clear_cache()


# **练习19：插件系统**

# **场景说明**：实现一个简单的插件管理系统。

# **具体需求**：
# 1. `register(plugin)` 注册插件（插件是包含 `name` 属性的对象）
# 2. `load(path)` 从 Python 文件加载插件
# 3. `execute(hook_name, *args)` 执行所有插件的指定钩子方法
# 4. `get_plugins()` 获取所有已注册插件
# 5. `unload(plugin_name)` 卸载指定插件


# import importlib
# import sys


# class PluginManager:
#     """简单的插件管理器"""

#     def __init__(self):
#         self._plugins = {}

#     def register(self, plugin):
#         if not hasattr(plugin, "name") or not plugin.name:
#             raise ValueError("插件必须包含非空 name 属性")
#         if plugin.name in self._plugins:
#             raise ValueError(f"插件 {plugin.name} 已存在")
#         self._plugins[plugin.name] = plugin

#     def load(self, path):
#         module_name = f"_plugin_{hash(path)}"
#         spec = importlib.util.spec_from_file_location(module_name, path)
#         if spec is None:
#             raise ImportError(f"无法加载模块：{path}")
#         module = importlib.util.module_from_spec(spec)
#         sys.modules[module_name] = module
#         try:
#             spec.loader.exec_module(module)
#         except Exception as e:
#             raise ImportError(f"加载插件文件失败：{path},错误：{e}")

#         for attr_name in dir(module):
#             if attr_name.startswith("_"):
#                 continue
#             obj = getattr(module, attr_name)
#             if hasattr(obj, "name") and obj.name:
#                 self.register(obj)

#     def execute(self, hook_name, *args):
#         for plugin in self._plugins.values():
#             if hasattr(plugin, hook_name):
#                 method = getattr(plugin, hook_name)
#                 method(*args)

#     def get_plugins(self):
#         return list(self._plugins.values())

#     def unload(self, plugin_name):
#         if plugin_name not in self._plugins:
#             raise KeyError(f"插件 {plugin_name} 不存在")
#         del self._plugins[plugin_name]


# class LogPlugin:
#     name = "logger"

#     def before_test(self, test_name):
#         print(f"[日志] 开始测试: {test_name}")

#     def after_test(self, test_name, result):
#         print(f"[日志] 测试完成: {test_name}, 结果: {result}")


# class ReportPlugin:
#     name = "reporter"

#     def before_test(self, test_name):
#         print(f"[报告] 记录测试开始: {test_name}")

#     def after_test(self, test_name, result):
#         print(f"[报告] 记录测试结果: {test_name} -> {result}")


# # 使用插件管理器
# manager = PluginManager()
# manager.register(LogPlugin())
# manager.register(ReportPlugin())

# # 执行钩子
# manager.execute("before_test", "登录测试")
# # 输出:
# # [日志] 开始测试: 登录测试
# # [报告] 记录测试开始: 登录测试

# manager.execute("after_test", "登录测试", "pass")
# # 输出:
# # [日志] 测试完成: 登录测试, 结果: pass
# # [报告] 记录测试结果: 登录测试 -> pass

# # 获取所有插件
# plugins = manager.get_plugins()
# print([p.name for p in plugins])  # ['logger', 'reporter']

# # 卸载插件
# manager.unload("logger")
# print([p.name for p in manager.get_plugins()])  # ['reporter']


# # **练习20：状态机**

# # **场景说明**：实现测试用例状态机，管理测试状态流转。

# # **具体需求**：
# # 1. 初始状态为 `"pending"`
# # 2. 状态流转规则：
# #    - `pending` → `running`
# #    - `running` → `passed` / `failed` / `skipped`
# #    - 只能按规则流转，非法流转抛出 `ValueError`
# # 3. `transition(to_state)` 状态转换
# # 4. `can_transition(to_state)` 检查是否可转换（返回布尔值）
# # 5. `get_history()` 获取状态历史列表
# # 6. `@property state` 只读属性获取当前状态


# class TestStateMachine:
#     # 允许的状态转换规则
#     _transitions = {
#         "pending": {"running"},
#         "running": {"passed", "failed", "skipped"},
#         # 终点状态不允许再转换
#         "passed": set(),
#         "failed": set(),
#         "skipped": set(),
#     }

#     def __init__(self):
#         self._state: str = "pending"
#         self._history = ["pending"]

#     @property
#     def state(self):
#         return self._state

#     def can_transition(self, to_state: str):
#         return to_state in self._transitions.get(self._state, set())

#     def transition(self, to_state: str):

#         if not self.can_transition(to_state):
#             raise ValueError(f"{to_state} 不能转到 {self.state}")

#         self._state = to_state
#         self._history.append(self._state)

#     def get_history(self):
#         return self._history.copy()


# if __name__ == "__main__":
#     # 创建状态机
#     sm = TestStateMachine()
#     print(sm.state)  # pending

#     # 检查是否可以转换
#     print(sm.can_transition("running"))  # True
#     print(sm.can_transition("passed"))  # False（不能直接从 pending 到 passed）

#     # 执行转换
#     sm.transition("running")
#     print(sm.state)  # running

#     sm.transition("passed")
#     print(sm.state)  # passed

#     # 非法转换
#     try:
#         sm.transition("running")  # passed 不能转到 running
#     except ValueError as e:
#         print(e)  # 非法状态转换: passed -> running

#     # 查看历史
#     print(sm.get_history())
#     # ['pending', 'running', 'passed']

#     # 测试失败场景
#     sm2 = TestStateMachine()
#     sm2.transition("running")
#     sm2.transition("failed")
#     print(sm2.state)  # failed
#     print(sm2.get_history())
#     # ['pending', 'running', 'failed']

#     # 测试跳过场景
#     sm3 = TestStateMachine()
#     sm3.transition("running")
#     sm3.transition("skipped")
#     print(sm3.state)  # skipped


# #### 题目1：类设计（综合考察：类定义、property、魔术方法）

# **场景**：设计一个用户管理系统中的 `User` 类。

# **需求**：
# 1. 包含 `username`、`email`、`age` 三个属性
# 2. `email` 设置时验证格式（必须包含 `@` 和 `.`）
# 3. `age` 设置时验证范围（0-150 的整数）
# 4. 实现 `__lt__` 比较运算符（按年龄比较）
# 5. 实现 `__eq__` 比较运算符（按用户名比较）
# 6. 实现 `__str__` 返回用户友好字符串：`"用户: 张三 (25岁)"`
# import re


# class User:
#     def __init__(self, username, email, age):
#         self.username = username
#         self.email = email
#         self.age = age

#     @property
#     def email(self):
#         return self._email

#     @email.setter
#     def email(self, value):
#         if not re.match(r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", value):
#             raise ValueError("email error")
#         self._email = value

#     @property
#     def age(self):
#         return self._age

#     @age.setter
#     def age(self, value):
#         if not isinstance(value, int) or not (0 <= value <= 150):
#             raise ValueError("age error")
#         self._age = value

#     def __lt__(self, other):
#         if not isinstance(other, User):
#             return NotImplemented
#         return self.age < other.age

#     def __eq__(self, other):
#         if not isinstance(other, User):
#             return NotImplemented
#         return self.username == other.username

#     def __str__(self):
#         return f"用户:{self.username}（{self.age}岁）"


# if __name__ == "__main__":
#     # 测试1：正常创建
#     user1 = User("zhangsan", "zhangsan@example.com", 25)
#     user2 = User("lisi", "lisi@example.com", 30)

#     print(user1)  # 用户: zhangsan (25岁)
#     print(user1 < user2)  # True (25 < 30)

#     # 测试2：邮箱验证
#     try:
#         user = User("test", "invalid-email", 20)
#     except ValueError as e:
#         print(e)  # 邮箱格式不正确

#     # 测试3：年龄验证
#     try:
#         user = User("test", "test@example.com", 200)
#     except ValueError as e:
#         print(e)  # 年龄必须在0-150之间

#     # 测试4：比较运算
#     users = [user2, user1]
#     users.sort()
#     print([u.username for u in users])  # ['zhangsan', 'lisi']


# # #### 题目2：继承体系设计（综合考察：继承、super()、方法重写）

# # **场景**：设计 API 测试框架的类层次结构。

# # **需求**：

# # **BaseAPI 基类**：
# # 1. `__init__(self, base_url, timeout=30)` 初始化
# # 2. `send_request(method, endpoint, **kwargs)` 发送请求
# # 3. `_build_url(endpoint)` 构建完整 URL（私有方法）
# # 4. `_log(method, url)` 记录日志（受保护方法）

# # **UserAPI 子类**：
# # 1. 继承 `BaseAPI`
# # 2. `login(username, password)` 登录
# # 3. `get_profile()` 获取用户信息
# # 4. `update_profile(data)` 更新用户信息

# # **OrderAPI 子类**：
# # 1. 继承 `BaseAPI`
# # 2. `create_order(data)` 创建订单
# # 3. `get_orders()` 获取订单列表
# # 4. `cancel_order(order_id)` 取消订单
# import logging
# import requests


# class BaseAPI:
#     def __init__(self, base_url: str, timeout=30):
#         self.base_url = base_url.rstrip("/")
#         self.timeout = timeout
#         self.session = requests.Session()

#     def _setup_logging(self):
#         self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
#         if not self.logger.handler:
#             handler = logging.StreamHandler()
#             formatter = logging.Formatter(
#                 "%(asctime)s - %(name)s - %(levelname)s - %(messgae)s"
#             )
#             handler.setFormatter(formatter)
#             self.logger.addHandler(handler)
#             self.logger.setLevel(logging.INFO)

#     def send_request(self, method, endpoint, **kwargs) -> requests.Response:
#         method = method.lower()
#         url = self._build_url(endpoint)
#         self._log(method, url)
#         func = getattr(self.session, method, None)
#         if func is None:
#             raise ValueError("method error")

#         if "timeout" not in kwargs:
#             kwargs["timeout"] = self.timeout
#         try:
#             response = func(url, **kwargs)
#             self.logger.info(f"Response:{response.status_code} - {response.reason}")
#         except requests.RequestException as e:
#             self.logger.error(f"请求错误：{e}")
#             raise

#     def _build_url(self, endpoint: str):
#         endpoint = endpoint.rstrip("/")
#         return f"{self.base_url}/{endpoint}"

#     def _log(self, method, url):
#         self.logger.info(f"Request [{method}] {url}")


# class UserAPI(BaseAPI):
#     def login(self, username, password):
#         payload = {"username": username, "password": password}
#         return self.send_request("post", "/login", json=payload)

#     def get_profile(self):
#         self.send_request("get", "/profile")

#     def update_profile(self, data):
#         self.send_request("put", "/profile", data)


# class OrderAPI(BaseAPI):
#     def create_order(self, data):
#         self.send_request("post", "/orders", json=data)

#     def get_orders(self):
#         self.send_request("get", "/orders")

#     def cancel_order(self, order_id):
#         self.send_request("post", f"/orders/{order_id}")


# if __name__ == "__main__":

#     class MockResponse:
#         def __init__(self, status_code=200, json_data=None):
#             self.status_code = status_code
#             self._json = json_data or {}

#         def json(self):
#             return self._json

#     # 测试基类功能
#     api = UserAPI("https://api.example.com")
#     print(api._build_url("/login"))  # https://api.example.com/login

#     # 测试继承
#     user_api = UserAPI("https://api.example.com")
#     order_api = OrderAPI("https://api.example.com")

#     print(isinstance(user_api, BaseAPI))  # True
#     print(isinstance(order_api, BaseAPI))  # True


# # #### 题目3：异常处理与上下文管理（综合考察：自定义异常、try/except、上下文管理器）

# # **场景**：实现一个配置文件加载器，包含完整的异常处理。

# # **需求**：

# # **自定义异常**：
# # 1. `ConfigError` 基类
# # 2. `ConfigFileNotFoundError(ConfigError)` 文件不存在
# # 3. `ConfigFormatError(ConfigError)` JSON 格式错误
# # 4. `ConfigValidationError(ConfigError)` 字段验证失败

# # **load_config 函数**：
# # 1. 从 JSON 文件加载配置
# # 2. 文件不存在时抛出 `ConfigFileNotFoundError`
# # 3. JSON 格式错误时抛出 `ConfigFormatError`
# # 4. 必要字段缺失时抛出 `ConfigValidationError`
# # 5. 使用 `try/except/finally` 确保资源释放
# # 6. 支持验证必填字段

# # **ConfigLoader 上下文管理器**：
# # 1. `__enter__` 加载配置文件
# # 2. `__exit__` 清理资源，记录日志
# # 3. `get(key, default=None)` 获取配置项
# # 4. `validate(required_keys)` 验证必填字段

# import logging
# import json
# import os
# import tempfile


# class ConfigError(Exception):
#     pass


# class ConfigFileNotFoundError(ConfigError):
#     pass


# class ConfigFormatError(ConfigError):
#     pass


# class ConfigValidationError(ConfigError):
#     pass


# def load_config(file_path, required_keys=None):
#     file_handle = None
#     try:
#         try:
#             file_handle = open(file_path, "r", encoding="utf-8")
#         except FileNotFoundError as e:
#             raise ConfigFileNotFoundError(f"配置文件不存在：{file_path}") from e

#         try:
#             config = json.load(file_handle)
#         except json.JSONDecodeError as e:
#             raise ConfigFormatError(f"配置文件格式错误：{file_path}") from e

#         if required_keys:
#             missing = [key for key in required_keys if key not in config]
#             if missing:
#                 raise ConfigValidationError(f"缺少必填字段：{missing}")
#         return config
#     finally:
#         if file_handle:
#             file_handle.close()


# class ConfigLoader:
#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         self._config = None

#     def __enter__(self):
#         logging.info(f"开始加载配置文件：{self.file_path}")
#         try:
#             self._config = load_config(self.file_path)
#         except ConfigError as e:
#             logging.error(f"加载配置失败：{e}")
#             raise
#         logging.info("配置文件加载成功")
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if exc_type is not None:
#             logging.error(f"配置使用过程中发生异常：{exc_val}")
#         else:
#             logging.info("配置使用结束，正常退出")
#         self._config = None
#         return False

#     def get(self, key, default=None):
#         if self._config is None:
#             raise RuntimeError("配置尚未加载或已关闭")
#         keys = key.split(".")
#         current = self._config
#         for k in keys:
#             if isinstance(current, dict) and k in current:
#                 current = current[k]
#             else:
#                 return default
#         return current

#     def validate(self, required_keys):
#         if self._config is None:
#             raise RuntimeError("配置尚未加载或已关闭")
#         missing = [k for k in required_keys if self.get(k) is None]
#         if missing:
#             raise ConfigValidationError(f"缺少必填字段：{missing}")
#         logging.info("配置验证通过，所有必填字段存在")


# if __name__ == "__main__":
#     # 创建临时配置文件
#     with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
#         json.dump({"db_host": "localhost", "db_port": 3306}, f)
#         config_file = f.name

#     # 测试1：正常加载
#     try:
#         config = load_config(config_file, required_keys=["db_host", "db_port"])
#         print(config)  # {'db_host': 'localhost', 'db_port': 3306}
#     except ConfigError as e:
#         print(f"配置错误: {e}")

#     # 测试2：文件不存在
#     try:
#         config = load_config("not_exist.json")
#     except ConfigFileNotFoundError as e:
#         print(e)  # 配置文件不存在: not_exist.json

#     # 测试3：格式错误
#     with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
#         f.write("{invalid json}")
#         bad_file = f.name

#     try:
#         config = load_config(bad_file)
#     except ConfigFormatError as e:
#         print(e)  # 配置文件格式错误: ...

#     # 测试4：缺少必填字段
#     with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
#         json.dump({"db_host": "localhost"}, f)  # 缺少 db_port
#         missing_file = f.name

#     try:
#         config = load_config(missing_file, required_keys=["db_host", "db_port"])
#     except ConfigValidationError as e:
#         print(e)  # 缺少必填字段: ['db_port']

#     # 测试5：使用上下文管理器
#     with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
#         json.dump({"api_key": "12345", "timeout": 30}, f)
#         ctx_file = f.name

#     with ConfigLoader(ctx_file) as loader:
#         print(loader.get("api_key"))  # 12345
#         print(loader.get("not_exist", "default"))  # default

#     # 清理临时文件
#     os.unlink(config_file)
#     os.unlink(bad_file)
#     os.unlink(missing_file)
#     os.unlink(ctx_file)


# #### 题目4：综合应用（综合考察：所有知识点）

# **场景**：实现一个简单的测试用例运行器。

# **需求**：

# **TestCase 类**：
# 1. 属性：`name`、`priority`（P0-P3）、`status`、`duration`
# 2. `run()` 执行测试（模拟）
# 3. `__str__` 返回用例信息
# 4. `__lt__` 按优先级排序
# 5. `__bool__` 根据状态判断
# 6. `__call__` 直接调用等同于 run()

# **TestSuite 类**：
# 1. 管理多个测试用例
# 2. `add_case(case)` 添加用例
# 3. `run_all()` 按优先级执行所有用例
# 4. `get_report()` 返回统计报告

# **TestRunner 上下文管理器**：
# 1. `__enter__` 初始化测试环境
# 2. `__exit__` 清理测试环境，生成报告
# 3. 支持异常时清理

# **自定义异常**：
# 1. `TestError` 基类
# 2. `TestFailedError` 测试失败
# 3. `TestTimeoutError` 测试超时

import random
import time
# items = ["pass", "fail"]
# weights = [0.8, 0.2]
# print(random.choice(items))
# print(random.choices(items, weights=weights)[0])


class TestCase:
    PRIORITY = {"P0": 0, "P1": 10, "P2": 20, "P3": 30}

    def __init__(self, name, priority="P2"):
        self.name = name
        self.priority = priority
        self.status = "pending"
        self.duration = 0.0
        self.timeout = 30

    def run(self):
        self.status = "running"
        start = time.time()
        self.duration = random.uniform(0.1, 0.5)
        time.sleep(self.duration)
        # items = ["pass", "fail"]
        # weights = [0.8, 0.2]
        # self.status = random.choices(items, weights=weights)[0]
        # self.duration = random.randint(1, 3)
        prob = {"P0": 1.0, "P1": 0.9, "P2": 0.8, "P3": 0.7}.get(self.priority, 0.8)
        if random.random() < prob:
            self.status = "pass"
        else:
            self.status = "fail"
            raise TestFailedError(f"测试失败：{self.name}")

    def __str__(self):
        return f"TestCase {self.name},{self.priority}"

    def __lt__(self, other: "TestCase"):
        # if isinstance(other, TestCase):
        #     raise ValueError("need TestCase")
        self_num = self.PRIORITY.get(self.priority, 99)
        other_num = self.PRIORITY.get(self.priority, 99)
        return self_num < other_num

    def __bool__(self):
        return self.status == "pass"

    def __call__(self):
        self.run()


class TestSuite:
    def __init__(self, name="default suite") -> None:
        self.name = name
        self.cases = []

    def add_case(self, case):
        self.cases.append(case)

    def run_all(self):
        self.cases.sort()
        for case in self.cases:
            case()

    def get_report(self):
        total = len(self.cases)
        passed = sum([1 for x in self.cases if x.status == "pass"])
        failed = sum([1 for x in self.cases if x.status == "fail"])
        duration = sum([x.duration for x in self.cases])
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "duration": round(duration, 2),
        }


class TestRunner:
    def __init__(self, report_name="Test Report") -> None:
        self.report_name = report_name
        self.start_time = None

    def __enter__(self):
        print(f"开始测试运行器：{self.report_name}")
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        print(f"测试运行结束，总耗时:{elapsed:.2f} 秒")
        if exc_type:
            print(f"捕获到异常：{exc_type.__name__}:{exc_val}")
        else:
            print("测试运行正常结束")
        return False


class TestError(Exception):
    pass


class TestFailedError(TestError):
    pass


class TestTimeoutError(TestError):
    pass


if __name__ == "__main__":  
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
