# 第1周：Python 基础语法与数据结构

## 本周目标

掌握 Python 核心语法，能熟练使用列表、字典、字符串处理测试数据。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| 变量与数据类型 | int, float, str, bool, None | ⭐⭐⭐ |
| 列表 | 增删改查、切片、推导式 | ⭐⭐⭐⭐⭐ |
| 字典 | 键值操作、嵌套、遍历 | ⭐⭐⭐⭐⭐ |
| 字符串 | 格式化、常用方法、正则入门 | ⭐⭐⭐⭐ |
| 控制流 | if/elif/else, for, while | ⭐⭐⭐⭐ |
| 函数 | 定义、参数、返回值、作用域 | ⭐⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 变量与数据类型

Python 是动态类型语言，不需要声明变量类型。

```python
# 基本数据类型
name = "张三"          # 字符串 str
age = 36              # 整数 int
salary = 15000.50     # 浮点数 float
is_tester = True      # 布尔值 bool
nothing = None        # 空值 NoneType

# 查看类型
print(type(name))     # <class 'str'>
print(type(age))      # <class 'int'>

# 类型转换
str(123)              # "123"
int("456")            # 456
float("3.14")         # 3.14
bool(0)               # False（0、空字符串、空列表、None 都是 False）
bool("hello")         # True

# 测试场景：从配置文件读取的值通常是字符串，需要转换
timeout = int(config.get("timeout", "30"))  # 默认值是字符串，转成 int
```

**类型判断的最佳实践：**

```python
# 不推荐：用 type() 判断
if type(x) == list:
    pass

# 推荐：用 isinstance() 判断
if isinstance(x, list):
    pass

# isinstance 支持多个类型
if isinstance(x, (int, float)):
    print("x 是数字")
```

---

### 2.2 列表（List）- 最常用的数据结构

列表是有序、可变的序列，测试工作中 80% 的数据都用列表存储。

```python
# 创建列表
cases = ["登录测试", "搜索测试", "支付测试"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, None]  # 可以混合类型（但不推荐）

# 空列表
empty1 = []
empty2 = list()

# ============================================
# 访问元素 - 索引从 0 开始
# ============================================
cases = ["登录", "搜索", "支付", "订单", "退出"]

cases[0]          # "登录" - 第一个
cases[2]          # "支付" - 第三个
cases[-1]         # "退出" - 最后一个
cases[-2]         # "订单" - 倒数第二个

# 索引越界会报错
# cases[10]       # IndexError: list index out of range

# ============================================
# 切片 - 获取子列表 [start:end:step]
# ============================================
cases = ["登录", "搜索", "支付", "订单", "退出"]

cases[1:3]        # ["搜索", "支付"] - 索引 1 到 2（不含 3）
cases[:3]         # ["登录", "搜索", "支付"] - 前 3 个
cases[2:]         # ["支付", "订单", "退出"] - 从索引 2 到末尾
cases[::2]        # ["登录", "支付", "退出"] - 每隔一个取一个
cases[::-1]       # ["退出", "订单", "支付", "搜索", "登录"] - 反转

# 测试场景：分批执行测试用例
all_cases = list(range(100))   # 100 个用例
batch1 = all_cases[:25]        # 第一批 25 个
batch2 = all_cases[25:50]      # 第二批 25 个

# ============================================
# 修改列表
# ============================================
cases = ["登录", "搜索"]

cases[0] = "用户登录"           # 修改元素
cases.append("支付")            # 末尾添加
cases.insert(1, "注册")         # 指定位置插入
cases.extend(["订单", "退出"])   # 批量添加

# ============================================
# 删除元素
# ============================================
cases = ["登录", "搜索", "支付", "订单"]

cases.remove("搜索")            # 按值删除（只删第一个匹配的）
del cases[0]                    # 按索引删除
popped = cases.pop()            # 弹出最后一个并返回
popped = cases.pop(0)           # 弹出指定索引

# ============================================
# 常用操作
# ============================================
cases = ["登录", "搜索", "支付"]

len(cases)              # 3 - 长度
"登录" in cases         # True - 成员判断
cases.count("登录")     # 1 - 统计出现次数
cases.index("搜索")     # 1 - 找到第一个索引

# 排序
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()                    # 原地排序 [1, 1, 2, 3, 4, 5, 6, 9]
numbers.sort(reverse=True)        # 降序
numbers.reverse()                 # 反转

# 复制列表（重要！）
a = [1, 2, 3]
b = a              # 错误！b 和 a 指向同一个对象
c = a.copy()       # 正确！创建新列表
d = a[:]           # 正确！切片创建新列表
e = list(a)        # 正确！list() 创建新列表
```

**列表推导式 - Python 特色语法：**

```python
# 传统写法
squares = []
for i in range(10):
    squares.append(i ** 2)

# 列表推导式
squares = [i ** 2 for i in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件过滤
evens = [i for i in range(20) if i % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 测试场景：提取失败的用例名
results = [
    {"name": "登录", "status": "pass"},
    {"name": "搜索", "status": "fail"},
    {"name": "支付", "status": "fail"},
]
failed = [r["name"] for r in results if r["status"] == "fail"]
# ["搜索", "支付"]

# 嵌套推导式（二维列表）
matrix = [[i * j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

---

### 2.3 字典（Dict）- 存储结构化数据

字典是键值对集合，键必须不可变（通常用字符串），值可以是任意类型。

```python
# 创建字典
user = {
    "username": "zhangsan",
    "password": "123456",
    "age": 28,
    "is_vip": True
}

# 空字典
empty1 = {}
empty2 = dict()

# 从列表创建
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = dict(zip(keys, values))  # {"a": 1, "b": 2, "c": 3}

# ============================================
# 访问元素
# ============================================
user = {"username": "zhangsan", "age": 28}

user["username"]              # "zhangsan" - 直接访问
user.get("email")             # None - 键不存在返回 None
user.get("email", "未设置")   # "未设置" - 键不存在返回默认值

# get() 是安全访问，推荐使用
# user["email"]               # KeyError: 'email'

# ============================================
# 修改字典
# ============================================
user = {"username": "zhangsan"}

user["age"] = 28              # 添加新键值
user["username"] = "lisi"     # 修改已有键
user.update({"email": "test@example.com", "phone": "13800000000"})

# 删除
del user["age"]               # 删除键值对
email = user.pop("email")     # 删除并返回值
user.clear()                  # 清空字典

# ============================================
# 遍历字典
# ============================================
user = {"username": "zhangsan", "age": 28, "city": "上海"}

# 遍历键
for key in user:              # 等同于 user.keys()
    print(key)

# 遍历值
for value in user.values():
    print(value)

# 遍历键值对（最常用）
for key, value in user.items():
    print(f"{key}: {value}")

# ============================================
# 嵌套字典 - 测试数据常见格式
# ============================================
test_data = {
    "login": {
        "valid": [
            {"username": "admin", "password": "123456"},
            {"username": "user", "password": "abcdef"},
        ],
        "invalid": [
            {"username": "", "password": "123456"},
            {"username": "admin", "password": ""},
        ]
    },
    "search": {
        "keywords": ["酒店", "机票", "火车票"]
    }
}

# 访问嵌套数据
test_data["login"]["valid"][0]["username"]  # "admin"
```

**字典推导式：**

```python
# 键值互换
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
# {1: "a", 2: "b", 3: "c"}

# 过滤
scores = {"张三": 85, "李四": 92, "王五": 78}
passed = {name: score for name, score in scores.items() if score >= 80}
# {"张三": 85, "李四": 92}
```

---

### 2.4 字符串处理

```python
# 创建字符串
s1 = "hello"
s2 = 'world'
s3 = """多行
字符串"""

# 转义
path = "C:\\Users\\test"      # \\ 表示反斜杠
quote = "He said \"hello\""   # \" 表示引号

# 原始字符串（不转义）
raw_path = r"C:\Users\test"   # 常用于正则表达式、文件路径

# ============================================
# 字符串格式化 - 三种方式
# ============================================
name = "张三"
age = 28

# 1. f-string（推荐，Python 3.6+）
message = f"我叫{name}，今年{age}岁"
print(f"明年{age + 1}岁")      # 支持表达式

# 2. format() 方法
message = "我叫{}，今年{}岁".format(name, age)
message = "我叫{name}，今年{age}岁".format(name="李四", age=30)

# 3. % 格式化（旧式，不推荐）
message = "我叫%s，今年%d岁" % (name, age)

# ============================================
# 常用方法
# ============================================
s = "  Hello, World!  "

s.strip()                # "Hello, World!" - 去首尾空白
s.lower()                # "  hello, world!  " - 转小写
s.upper()                # "  HELLO, WORLD!  " - 转大写
s.replace("World", "Python")  # 替换

# 分割与连接
"a,b,c".split(",")       # ["a", "b", "c"] - 分割
",".join(["a", "b", "c"]) # "a,b,c" - 连接

# 判断方法
"123".isdigit()          # True - 是否全数字
"abc".isalpha()          # True - 是否全字母
"hello".startswith("he") # True - 是否以某字符串开头
"hello".endswith("lo")   # True - 是否以某字符串结尾

# 查找
"hello world".find("world")  # 6 - 找到返回索引，没找到返回 -1
"hello world".index("world") # 6 - 找到返回索引，没找到报错

# ============================================
# 正则表达式入门
# ============================================
import re

# 匹配
pattern = r"\d+"  # 匹配数字
text = "订单号：12345，金额：678.90"

re.search(pattern, text)       # 找到第一个匹配
re.findall(pattern, text)      # 找到所有匹配 ["12345", "678", "90"]
re.findall(r"\d+\.?\d*", text) # 匹配浮点数 ["12345", "678.90"]

# 替换
re.sub(r"\d+", "xxx", text)    # "订单号：xxx，金额：xxx"

# 分割
re.split(r"[,，]", "a,b，c")   # ["a", "b", "c"]

# 测试场景：提取日志中的信息
log = "[2024-01-15 10:30:45] ERROR - 登录失败，用户名不存在"
match = re.search(r"\[(.*?)\] (\w+) - (.*)", log)
if match:
    timestamp, level, message = match.groups()
    # timestamp = "2024-01-15 10:30:45"
    # level = "ERROR"
    # message = "登录失败，用户名不存在"
```

---

### 2.5 控制流

```python
# ============================================
# 条件判断
# ============================================
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"

# 三元表达式
result = "通过" if score >= 60 else "不通过"

# 多条件判断
age = 25
is_vip = True

if age >= 18 and is_vip:
    print("成年VIP用户")

if age < 12 or age > 65:
    print("特殊年龄段")

# ============================================
# for 循环
# ============================================
# 遍历列表
cases = ["登录", "搜索", "支付"]
for case in cases:
    print(f"执行: {case}")

# 遍历带索引
for i, case in enumerate(cases):
    print(f"第{i+1}个用例: {case}")

# 遍历范围
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 10, 2):   # 1, 3, 5, 7, 9
    print(i)

# 同时遍历多个列表
names = ["登录", "搜索"]
priorities = ["P0", "P1"]
for name, priority in zip(names, priorities):
    print(f"{name}: {priority}")

# ============================================
# while 循环
# ============================================
count = 0
while count < 5:
    print(count)
    count += 1

# 带条件的循环（重试场景）
retry = 0
max_retry = 3
success = False

while retry < max_retry and not success:
    result = execute_test()
    if result == "pass":
        success = True
    retry += 1

# ============================================
# break, continue, else
# ============================================
# break - 跳出循环
for i in range(10):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# continue - 跳过本次迭代
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4

# for-else：循环正常结束执行 else
for i in range(5):
    if i == 10:
        break
else:
    print("循环正常结束")  # 会执行

for i in range(5):
    if i == 3:
        break
else:
    print("循环正常结束")  # 不会执行
```

---

### 2.6 函数

```python
# ============================================
# 函数定义
# ============================================
def greet(name):
    """打招呼函数（这是文档字符串）"""
    return f"Hello, {name}!"

message = greet("张三")  # "Hello, 张三!"

# 无返回值函数
def log_info(message):
    print(f"[INFO] {message}")
    # 隐式返回 None

# ============================================
# 参数类型
# ============================================
# 位置参数
def add(a, b):
    return a + b

add(1, 2)  # 3

# 默认参数
def greet(name, greeting="你好"):
    return f"{greeting}, {name}!"

greet("张三")              # "你好, 张三!"
greet("张三", "早上好")    # "早上好, 张三!"

# 关键字参数
def create_user(username, email, age=18, is_vip=False):
    return {"username": username, "email": email, "age": age, "is_vip": is_vip}

create_user(
    username="zhangsan",
    email="test@example.com",
    is_vip=True  # 可以跳过 age
)

# *args - 可变位置参数
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

sum_all(1, 2, 3, 4, 5)  # 15

# **kwargs - 可变关键字参数
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="张三", age=28, city="上海")

# 组合使用
def test_case(name, *steps, **options):
    print(f"测试用例: {name}")
    print(f"步骤: {steps}")
    print(f"选项: {options}")

test_case(
    "登录测试",
    "打开登录页", "输入用户名", "输入密码", "点击登录",
    retry=3, timeout=30
)
# 测试用例: 登录测试
# 步骤: ('打开登录页', '输入用户名', '输入密码', '点击登录')
# 选项: {'retry': 3, 'timeout': 30}

# ============================================
# 返回多个值（实际返回元组）
# ============================================
def get_test_result():
    return "登录测试", "pass", 1.5

name, status, duration = get_test_result()

# ============================================
# 作用域
# ============================================
x = 10  # 全局变量

def foo():
    x = 20  # 局部变量（不会修改全局 x）
    print(x)  # 20

def bar():
    global x  # 声明使用全局变量
    x = 30    # 修改全局 x

foo()
print(x)  # 10
bar()
print(x)  # 30

# ============================================
# Lambda 函数 - 匿名函数
# ============================================
# 普通函数
def square(x):
    return x ** 2

# Lambda
square = lambda x: x ** 2

# 常用场景：排序
users = [{"name": "张三", "age": 25}, {"name": "李四", "age": 30}]
users.sort(key=lambda u: u["age"])  # 按年龄排序

# 常用场景：过滤
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4, 6]
```

---

## 三、学到什么程度

### 必须掌握（能独立完成）

- [ ] 能熟练使用列表存储和操作测试数据
- [ ] 能使用字典存储配置信息和测试结果
- [ ] 能使用 f-string 格式化字符串
- [ ] 能编写带参数和返回值的函数
- [ ] 能使用列表推导式简化代码
- [ ] 能使用 enumerate 和 zip 遍历数据

### 应该了解（知道怎么查）

- [ ] 深拷贝 vs 浅拷贝
- [ ] 字符串的编码问题
- [ ] 正则表达式常用语法

---

## 四、练习内容

### 练习1：测试数据统计

```python
# 给定测试结果数据
test_results = [
    {"name": "登录测试", "status": "pass", "duration": 1.2},
    {"name": "搜索测试", "status": "fail", "duration": 2.5},
    {"name": "支付测试", "status": "pass", "duration": 3.1},
    {"name": "订单测试", "status": "fail", "duration": 1.8},
    {"name": "退出测试", "status": "pass", "duration": 0.5},
    {"name": "注册测试", "status": "pass", "duration": 2.0},
    {"name": "收藏测试", "status": "skip", "duration": 0.0},
]

# 任务1：统计各状态的用例数量
# 期望输出: {"pass": 4, "fail": 2, "skip": 1}

# 任务2：找出所有失败的用例名
# 期望输出: ["搜索测试", "订单测试"]

# 任务3：计算通过用例的平均耗时
# 期望输出: 1.7

# 任务4：按耗时降序排列
# 期望输出: [{"name": "支付测试", ...}, {"name": "搜索测试", ...}, ...]
```

### 练习2：配置文件处理

```python
# 给定配置字典
config = {
    "base_url": "https://api.ctrip.com",
    "timeout": 30,
    "retry": 3,
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer xxx"
    },
    "environments": {
        "dev": "https://dev.ctrip.com",
        "test": "https://test.ctrip.com",
        "prod": "https://api.ctrip.com"
    }
}

# 任务1：编写函数 get_config(key, default=None)
# 支持点号访问嵌套配置
# get_config("headers.Content-Type") 返回 "application/json"
# get_config("timeout") 返回 30
# get_config("not_exist", "default") 返回 "default"

# 任务2：编写函数 switch_env(env_name)
# 将 base_url 切换到指定环境
```

### 练习3：日志解析

```python
# 给定日志字符串
logs = """
[2024-01-15 10:30:45] INFO  - 测试开始
[2024-01-15 10:30:46] INFO  - 执行登录测试
[2024-01-15 10:30:47] ERROR - 登录失败：用户名不存在
[2024-01-15 10:30:48] INFO  - 执行搜索测试
[2024-01-15 10:30:49] WARN  - 响应时间过长：2.5s
[2024-01-15 10:30:50] INFO  - 搜索测试通过
[2024-01-15 10:30:51] INFO  - 测试结束
"""

# 任务1：提取所有 ERROR 级别的日志
# 任务2：统计各级别日志数量
# 任务3：提取所有时间戳，计算测试总耗时
```

---

## 五、检验标准

### 自测题（完成后对照答案）

#### 题目1：列表操作
```python
# 有两个列表，找出同时存在于两个列表中的元素
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
# 期望输出: [4, 5]
```

#### 题目2：字典处理
```python
# 将以下列表转换为字典，key 是 name，value 是整个对象
users = [
    {"name": "张三", "age": 25},
    {"name": "李四", "age": 30},
]
# 期望输出: {"张三": {"name": "张三", "age": 25}, "李四": {"name": "李四", "age": 30}}
```

#### 题目3：函数编写
```python
# 编写函数 validate_email(email)
# 验证邮箱格式，返回 True/False
# 要求：包含@符号，@前后都有内容，域名包含点号
validate_email("test@example.com")  # True
validate_email("invalid")           # False
validate_email("@example.com")      # False
```

#### 题目4：综合应用
```python
# 给定测试用例列表，编写函数生成测试报告
cases = [
    {"name": "登录", "status": "pass", "time": 1.2},
    {"name": "搜索", "status": "fail", "time": 2.5},
    {"name": "支付", "status": "pass", "time": 3.0},
]

def generate_report(cases):
    """
    返回格式：
    {
        "total": 3,
        "passed": 2,
        "failed": 1,
        "pass_rate": "66.67%",
        "avg_time": 2.23,
        "failed_cases": ["搜索"]
    }
    """
    pass
```

### 答案

```python
# 题目1
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
result = [x for x in list1 if x in list2]
# 或者
result = list(set(list1) & set(list2))

# 题目2
users = [{"name": "张三", "age": 25}, {"name": "李四", "age": 30}]
result = {user["name"]: user for user in users}

# 题目3
import re

def validate_email(email):
    if not isinstance(email, str):
        return False
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return bool(re.match(pattern, email))

# 题目4
def generate_report(cases):
    total = len(cases)
    passed = sum(1 for c in cases if c["status"] == "pass")
    failed = sum(1 for c in cases if c["status"] == "fail")
    failed_cases = [c["name"] for c in cases if c["status"] == "fail"]
    total_time = sum(c["time"] for c in cases)

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": f"{passed/total*100:.2f}%",
        "avg_time": round(total_time/total, 2),
        "failed_cases": failed_cases
    }
```

---

## 六、本周小结

### 核心要点

1. **列表**：测试数据的主要载体，熟练掌握增删改查和推导式
2. **字典**：配置和结构化数据的最佳选择，善用 `.get()` 安全访问
3. **字符串**：掌握 f-string 和常用方法，正则表达式是进阶技能
4. **函数**：代码复用的基础，理解参数类型和作用域

### 下周预告

第2周将学习面向对象编程（OOP），这是理解测试框架源码和封装测试工具的基础。
