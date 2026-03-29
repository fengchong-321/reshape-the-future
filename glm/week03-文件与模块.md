# 第3周：文件操作与模块化

## 本周目标

掌握 Python 文件读写操作，能处理 JSON/YAML 配置文件和 CSV 测试数据；理解模块化开发，能组织规范的测试项目结构。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| 文件读写 | open()、with、编码 | ⭐⭐⭐⭐⭐ |
| JSON 处理 | json 模块、序列化/反序列化 | ⭐⭐⭐⭐⭐ |
| YAML 处理 | PyYAML、配置文件 | ⭐⭐⭐⭐⭐ |
| CSV 处理 | csv 模块、数据驱动测试 | ⭐⭐⭐⭐ |
| 路径处理 | os.path、pathlib | ⭐⭐⭐⭐ |
| 模块与包 | import、__init__.py、虚拟环境 | ⭐⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 文件读写基础

```python
# ============================================
# open() 函数基础
# ============================================
# open(file, mode, encoding)
# mode: r(读) w(写) a(追加) rb(二进制读) wb(二进制写)

# 读取整个文件
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 逐行读取（推荐，内存友好）
with open("test.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # strip() 去除换行符

# 读取所有行为列表
with open("test.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()  # ['第一行\n', '第二行\n', ...]

# 读取指定字节数
with open("test.txt", "r", encoding="utf-8") as f:
    chunk = f.read(100)  # 读取 100 个字符

# ============================================
# 写入文件
# ============================================
# 写入（覆盖）
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# 写入多行
lines = ["第一行", "第二行", "第三行"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines([line + "\n" for line in lines])

# 追加
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("追加内容\n")

# ============================================
# 二进制文件（图片、Excel等）
# ============================================
# 复制文件
with open("source.png", "rb") as src:
    content = src.read()
    with open("dest.png", "wb") as dst:
        dst.write(content)

# ============================================
# 文件指针
# ============================================
with open("test.txt", "r+") as f:
    content = f.read()      # 读取全部
    f.seek(0)               # 移动指针到开头
    f.write("新内容")        # 覆盖写入
    f.tell()                # 当前指针位置

# ============================================
# 为什么用 with？（上下文管理器）
# ============================================
# 不使用 with（需要手动关闭）
f = open("test.txt", "r")
try:
    content = f.read()
finally:
    f.close()  # 必须手动关闭

# 使用 with（自动关闭，即使发生异常）
with open("test.txt", "r") as f:
    content = f.read()
# 离开 with 块后自动关闭
```

---

### 2.2 JSON 处理

JSON 是接口测试中最常用的数据格式。

```python
import json

# ============================================
# Python 对象 → JSON 字符串（序列化）
# ============================================
data = {
    "username": "张三",
    "age": 28,
    "is_vip": True,
    "hobbies": ["reading", "gaming"],
    "address": None
}

# 转换为 JSON 字符串
json_str = json.dumps(data)
# '{"username": "\u5f20\u4e09", "age": 28, ...}'

# 格式化输出
json_str = json.dumps(data, indent=2, ensure_ascii=False)
# {
#   "username": "张三",
#   "age": 28,
#   ...
# }

# 排序键
json_str = json.dumps(data, sort_keys=True)

# ============================================
# JSON 字符串 → Python 对象（反序列化）
# ============================================
json_str = '{"name": "张三", "age": 28}'
data = json.loads(json_str)
# {'name': '张三', 'age': 28}

# ============================================
# 文件读写
# ============================================
# 写入 JSON 文件
data = {"name": "张三", "scores": [85, 90, 78]}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 读取 JSON 文件
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ============================================
# 处理复杂对象
# ============================================
from datetime import datetime

# 自定义编码器
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data = {"time": datetime.now()}
json_str = json.dumps(data, cls=DateTimeEncoder)

# 自定义解码器
def datetime_hook(obj):
    for key, value in obj.items():
        if key.endswith("_at") and isinstance(value, str):
            try:
                obj[key] = datetime.fromisoformat(value)
            except:
                pass
    return obj

data = json.loads('{"created_at": "2024-01-15T10:30:00"}', object_hook=datetime_hook)

# ============================================
# 测试场景：接口响应处理
# ============================================
import requests

def test_api():
    response = requests.post(
        "https://api.example.com/login",
        json={"username": "admin", "password": "123456"}
    )

    # 解析响应
    data = response.json()  # 等同于 json.loads(response.text)

    # 验证
    assert data["code"] == 200
    assert "token" in data["data"]

    return data

# ============================================
# 测试场景：测试数据存储
# ============================================
def save_test_result(result, filepath="results.json"):
    """保存测试结果"""
    # 读取现有数据
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        results = []

    # 添加新结果
    results.append(result)

    # 保存
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

# 使用
save_test_result({
    "case": "登录测试",
    "status": "pass",
    "duration": 1.5,
    "timestamp": "2024-01-15 10:30:00"
})
```

---

### 2.3 YAML 处理

YAML 是测试配置文件的首选格式，比 JSON 更易读。

```python
# 先安装：pip install pyyaml

import yaml

# ============================================
# YAML 语法示例
# ============================================
yaml_content = """
# 这是注释
name: 测试套件
version: 1.0

# 嵌套对象
database:
  host: localhost
  port: 3306
  name: test_db

# 列表
environments:
  - dev
  - test
  - prod

# 对象列表
test_cases:
  - name: 登录测试
    priority: P0
    data:
      username: admin
      password: "123456"  # 引号确保是字符串
  - name: 搜索测试
    priority: P1
    data:
      keyword: 酒店

# 多行字符串
description: |
  这是一个
  多行描述
  保留换行

# 多行字符串（不保留换行）
summary: >
  这是一个
  长描述
  会被合并成一行
"""

# ============================================
# 解析 YAML
# ============================================
data = yaml.safe_load(yaml_content)
# data 是 Python 字典

print(data["name"])           # "测试套件"
print(data["database"]["host"])  # "localhost"
print(data["test_cases"][0]["name"])  # "登录测试"

# ============================================
# 文件读写
# ============================================
# 读取 YAML 文件
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 写入 YAML 文件
data = {"name": "测试", "items": [1, 2, 3]}
with open("output.yaml", "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

# ============================================
# 测试配置示例
# ============================================
# config.yaml
"""
base_url: https://api.example.com
timeout: 30

auth:
  username: admin
  password: admin123

test_data:
  login:
    valid:
      - username: admin
        password: "123456"
      - username: user
        password: "abcdef"
    invalid:
      - username: ""
        password: "123456"
      - username: admin
        password: ""
"""

# 加载配置
class Config:
    _instance = None
    _config = None

    @classmethod
    def load(cls, filepath="config.yaml"):
        if cls._config is None:
            with open(filepath, "r", encoding="utf-8") as f:
                cls._config = yaml.safe_load(f)
        return cls._config

    @classmethod
    def get(cls, key, default=None):
        """支持点号访问嵌套配置"""
        keys = key.split(".")
        value = cls.load()
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

# 使用
Config.get("base_url")                    # "https://api.example.com"
Config.get("auth.username")               # "admin"
Config.get("test_data.login.valid")       # 返回列表
Config.get("not_exist", "default_value")  # "default_value"
```

---

### 2.4 CSV 处理

CSV 是数据驱动测试的常用格式。

```python
import csv

# ============================================
# 读取 CSV
# ============================================
# 假设 test_data.csv 内容：
# case_name,username,password,expected
# 登录成功,admin,123456,success
# 密码错误,admin,wrong,fail
# 用户名为空,,123456,fail

# 方式1：读取为字典列表（推荐）
with open("test_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    # [
    #   {"case_name": "登录成功", "username": "admin", ...},
    #   {"case_name": "密码错误", "username": "admin", ...},
    #   ...
    # ]

# 方式2：读取为列表
with open("test_data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # 第一行是表头
    rows = list(reader)
    # [["登录成功", "admin", "123456", "success"], ...]

# ============================================
# 写入 CSV
# ============================================
# 写入字典列表
data = [
    {"case_name": "登录成功", "status": "pass"},
    {"case_name": "登录失败", "status": "fail"},
]

with open("results.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = ["case_name", "status"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

# 写入列表
rows = [
    ["case_name", "status"],
    ["登录成功", "pass"],
    ["登录失败", "fail"],
]

with open("results.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# ============================================
# 数据驱动测试示例
# ============================================
# test_login.csv
# username,password,expected_code,expected_msg
# admin,123456,200,登录成功
# admin,wrong,401,密码错误
# "",123456,400,用户名不能为空

import pytest

def load_csv_data(filepath):
    """加载 CSV 测试数据"""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

@pytest.mark.parametrize("data", load_csv_data("test_login.csv"))
def test_login(data):
    """数据驱动登录测试"""
    response = requests.post(
        "https://api.example.com/login",
        json={
            "username": data["username"],
            "password": data["password"]
        }
    )

    assert response.json()["code"] == int(data["expected_code"])
    assert data["expected_msg"] in response.json()["message"]

# ============================================
# 处理大文件（流式读取）
# ============================================
def process_large_csv(filepath, batch_size=1000):
    """分批处理大 CSV 文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []

        for row in reader:
            batch.append(row)
            if len(batch) >= batch_size:
                yield batch
                batch = []

        if batch:  # 处理最后一批
            yield batch

# 使用
for batch in process_large_csv("large_file.csv"):
    print(f"处理 {len(batch)} 条记录")
```

---

### 2.5 路径处理

```python
import os
from pathlib import Path

# ============================================
# os.path（传统方式）
# ============================================
# 获取当前工作目录
os.getcwd()

# 拼接路径（跨平台）
path = os.path.join("tests", "data", "config.json")
# Windows: "tests\\data\\config.json"
# Linux/Mac: "tests/data/config.json"

# 获取文件名
os.path.basename("/path/to/file.txt")    # "file.txt"

# 获取目录名
os.path.dirname("/path/to/file.txt")     # "/path/to"

# 分割扩展名
os.path.splitext("file.txt")             # ("file", ".txt")

# 判断路径是否存在
os.path.exists("/path/to/file")
os.path.isfile("/path/to/file")
os.path.isdir("/path/to/dir")

# 创建目录
os.makedirs("path/to/dir", exist_ok=True)

# 列出目录内容
os.listdir("path/to/dir")

# ============================================
# pathlib（推荐，Python 3.4+）
# ============================================
# Path 对象
p = Path("tests/data/config.json")

# 属性
p.name        # "config.json"
p.stem        # "config"
p.suffix      # ".json"
p.parent      # Path("tests/data")
p.parents[0]  # Path("tests/data")
p.parents[1]  # Path("tests")

# 路径操作
p.exists()    # 是否存在
p.is_file()   # 是否是文件
p.is_dir()    # 是否是目录

# 创建目录
Path("output/logs").mkdir(parents=True, exist_ok=True)

# 读写文件（Path 对象自带方法）
p = Path("test.txt")
content = p.read_text(encoding="utf-8")
p.write_text("新内容", encoding="utf-8")

# 拼接路径
base = Path("/home/user")
config = base / "config" / "settings.yaml"

# 遍历目录
for file in Path("tests").glob("*.py"):
    print(file)

for file in Path("tests").rglob("*.py"):  # 递归
    print(file)

# ============================================
# 测试项目中的路径处理
# ============================================
# 项目结构
# project/
# ├── config/
# │   └── settings.yaml
# ├── tests/
# │   ├── test_api.py
# │   └── data/
# │       └── users.csv
# └── utils/
#     └── helpers.py

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 配置文件路径
CONFIG_FILE = PROJECT_ROOT / "config" / "settings.yaml"

# 测试数据目录
TEST_DATA_DIR = PROJECT_ROOT / "tests" / "data"

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def get_test_data(filename):
    """获取测试数据文件路径"""
    return TEST_DATA_DIR / filename

# 使用
data_path = get_test_data("users.csv")
```

---

### 2.6 模块与包

```python
# ============================================
# import 语法
# ============================================
# 导入整个模块
import os
os.path.join("a", "b")

# 导入并起别名
import numpy as np
import pandas as pd

# 从模块导入特定内容
from os.path import join, exists
join("a", "b")

# 导入所有（不推荐）
from os.path import *

# ============================================
# 模块搜索路径
# ============================================
import sys
print(sys.path)  # 模块搜索路径列表

# 添加搜索路径
sys.path.append("/path/to/module")

# ============================================
# __name__ == "__main__"
# ============================================
# my_module.py

def main():
    print("主程序")

def helper():
    print("辅助函数")

# 只有直接运行时才执行
if __name__ == "__main__":
    main()

# 当被 import 时，__name__ 是模块名
# 当直接运行时，__name__ 是 "__main__"

# ============================================
# 包（Package）
# ============================================
# 包是包含 __init__.py 的目录

# 项目结构
# my_package/
# ├── __init__.py
# ├── module1.py
# ├── module2.py
# └── subpackage/
#     ├── __init__.py
#     └── module3.py

# __init__.py 可以是空文件，也可以初始化代码
# my_package/__init__.py
"""
from .module1 import func1
from .module2 import func2

__version__ = "1.0.0"
"""

# 使用
from my_package import func1, func2
from my_package.subpackage import module3

# ============================================
# 相对导入 vs 绝对导入
# ============================================
# 在 my_package/subpackage/module3.py 中

# 绝对导入（推荐）
from my_package.module1 import func1

# 相对导入
from ..module1 import func1      # 上一级
from ..subpackage import module3 # 跨子包
from . import another_module     # 当前目录
```

---

### 2.7 虚拟环境与依赖管理

```bash
# ============================================
# venv（Python 内置）
# ============================================
# 创建虚拟环境
python -m venv venv

# 激活
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 退出
deactivate

# ============================================
# pip 包管理
# ============================================
# 安装包
pip install requests

# 安装指定版本
pip install requests==2.28.0
pip install requests>=2.28.0

# 卸载
pip uninstall requests

# 查看已安装
pip list
pip freeze

# 导出依赖
pip freeze > requirements.txt

# 从文件安装
pip install -r requirements.txt

# ============================================
# requirements.txt 示例
# ============================================
# requirements.txt
"""
requests==2.31.0
pytest==7.4.0
pyyaml==6.0.1
allure-pytest==2.13.2
"""

# ============================================
# pip.conf 配置（国内镜像加速）
# ============================================
# ~/.pip/pip.conf (Linux/Mac)
# %APPDATA%\pip\pip.ini (Windows)
"""
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
"""
```

---

### 2.8 测试项目结构

```
my_test_project/
├── README.md
├── requirements.txt
├── pytest.ini              # Pytest 配置
├── config/
│   ├── __init__.py
│   ├── settings.yaml       # 主配置
│   └── settings.prod.yaml  # 环境配置
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Pytest 共享 fixture
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_login.py
│   │   └── test_user.py
│   ├── test_ui/
│   │   ├── __init__.py
│   │   └── test_home.py
│   └── data/
│       ├── users.csv
│       └── orders.json
├── utils/
│   ├── __init__.py
│   ├── http_client.py      # HTTP 客户端封装
│   ├── db_helper.py        # 数据库工具
│   └── logger.py           # 日志工具
├── reports/
│   └── .gitkeep
└── scripts/
    ├── run_tests.sh
    └── generate_report.py
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 能熟练读写文本文件和 JSON 文件
- [ ] 能使用 YAML 管理测试配置
- [ ] 能使用 CSV 实现数据驱动测试
- [ ] 能使用 pathlib 处理路径
- [ ] 能创建规范的测试项目结构
- [ ] 能使用虚拟环境和 requirements.txt

### 应该了解

- [ ] JSON 序列化自定义对象
- [ ] CSV 大文件处理
- [ ] 模块搜索机制

---

## 四、练习内容（20 题）

### 基础练习（1-8）

---

**练习1：文件读写基础**

**场景说明**：在测试过程中，经常需要将测试结果写入日志文件，或者读取配置文件。

**具体需求**：
1. 使用 `with` 语句写入文本文件 `hello.txt`，内容为 `"Hello, Python!"`
2. 读取 `hello.txt` 内容并打印
3. 追加一行 `"Welcome to testing!"` 到文件末尾
4. 读取所有行到列表，去除换行符
5. 统计文件行数和字符数

**使用示例**：
```python
# 写入文件
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!")

# 读取文件
with open("hello.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)  # Hello, Python!

# 追加内容
with open("hello.txt", "a", encoding="utf-8") as f:
    f.write("\nWelcome to testing!")

# 读取所有行
with open("hello.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f]
    print(lines)  # ['Hello, Python!', 'Welcome to testing!']

# 统计
print(f"行数: {len(lines)}")      # 行数: 2
print(f"字符数: {len(content)}")  # 字符数: 15
```

**验收标准**：
- [ ] 正确使用 `with` 语句管理文件
- [ ] 写入、读取、追加操作正确
- [ ] 行列表和统计结果正确
- [ ] 文件编码使用 `utf-8`

---

**练习2：JSON 文件操作**

**场景说明**：JSON 是接口测试中最常用的数据格式，需要熟练掌握读写操作。

**具体需求**：
1. 创建字典 `data`，包含用户列表和设置
2. 将 `data` 保存为 `users.json`，格式化输出（indent=2）
3. 读取 `users.json` 并打印
4. 添加一个用户 `{"name": "王五", "age": 28}` 并保存
5. 处理 `JSONDecodeError` 异常（读取非法 JSON 时）

**使用示例**：
```python
import json

# 原始数据
data = {
    "users": [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 30}
    ],
    "settings": {"timeout": 30, "retry": 3}
}

# 保存 JSON 文件（格式化）
with open("users.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 读取 JSON 文件
with open("users.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded["users"][0]["name"])  # 张三

# 添加用户并保存
loaded["users"].append({"name": "王五", "age": 28})
with open("users.json", "w", encoding="utf-8") as f:
    json.dump(loaded, f, indent=2, ensure_ascii=False)

# 异常处理
try:
    with open("invalid.json", "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"JSON 格式错误: {e}")
except FileNotFoundError:
    print("文件不存在")
```

**验收标准**：
- [ ] JSON 文件正确保存和读取
- [ ] `ensure_ascii=False` 保留中文
- [ ] `indent=2` 格式化输出
- [ ] 异常处理正确

---

**练习3：CSV 文件操作**

**场景说明**：CSV 是数据驱动测试的常用格式，需要掌握读写操作。

**具体需求**：
1. 创建测试数据 CSV 文件 `test_data.csv`，包含列：`case_name,username,password,expected`
2. 写入 3 行测试数据
3. 使用 `csv.DictReader` 读取并打印每行
4. 筛选出 `expected=success` 的行
5. 追加新的测试用例到 CSV

**使用示例**：
```python
import csv

# 写入 CSV 文件
test_data = [
    {"case_name": "登录成功", "username": "admin", "password": "123456", "expected": "success"},
    {"case_name": "密码错误", "username": "admin", "password": "wrong", "expected": "fail"},
    {"case_name": "用户为空", "username": "", "password": "123456", "expected": "fail"}
]

with open("test_data.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = ["case_name", "username", "password", "expected"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(test_data)

# 读取 CSV 文件
with open("test_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"用例: {row['case_name']}, 预期: {row['expected']}")

# 筛选成功的用例
with open("test_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    success_cases = [row for row in reader if row["expected"] == "success"]
    print(f"成功用例数: {len(success_cases)}")  # 成功用例数: 1

# 追加新用例
new_case = {"case_name": "正常登录", "username": "user", "password": "pass", "expected": "success"}
with open("test_data.csv", "a", encoding="utf-8", newline="") as f:
    fieldnames = ["case_name", "username", "password", "expected"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerow(new_case)
```

**验收标准**：
- [ ] CSV 文件正确写入和读取
- [ ] 使用 `DictReader` 和 `DictWriter`
- [ ] `newline=""` 参数正确设置
- [ ] 筛选和追加功能正确

---

**练习4：YAML 配置文件**

**场景说明**：YAML 是测试框架中最常用的配置文件格式，需要掌握读写操作。

**具体需求**：
1. 创建 YAML 配置文件 `config.yaml`，包含数据库配置
2. 使用 PyYAML 读取配置
3. 访问嵌套配置 `database.host` 和 `database.port`
4. 修改 `port` 为 `3307` 并保存
5. 处理 YAML 解析异常

**使用示例**：
```python
import yaml

# 创建配置内容
config_content = """
database:
  host: localhost
  port: 3306
  name: test_db
  user: root
api:
  base_url: https://api.example.com
  timeout: 30
"""

# 写入 YAML 文件
with open("config.yaml", "w", encoding="utf-8") as f:
    f.write(config_content)

# 读取 YAML 文件
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 访问配置
print(config["database"]["host"])  # localhost
print(config["database"]["port"])  # 3306
print(config["api"]["base_url"])   # https://api.example.com

# 修改配置
config["database"]["port"] = 3307

# 保存修改
with open("config.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

# 异常处理
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
except yaml.YAMLError as e:
    print(f"YAML 解析错误: {e}")
except FileNotFoundError:
    print("配置文件不存在")
```

**验收标准**：
- [ ] YAML 文件正确读写
- [ ] 使用 `safe_load` 安全加载
- [ ] 嵌套配置访问正确
- [ ] `allow_unicode=True` 保留中文

---

**练习5：路径操作**

**场景说明**：测试项目中需要处理各种文件路径，pathlib 是现代 Python 的首选方式。

**具体需求**：
1. 使用 `pathlib.Path` 获取当前脚本所在目录
2. 创建 `output/reports` 目录（包括父目录）
3. 检查 `config.yaml` 文件是否存在
4. 获取文件的扩展名和文件名（不含扩展名）
5. 遍历目录下所有 `.py` 文件

**使用示例**：
```python
from pathlib import Path

# 获取当前脚本目录
current_dir = Path(__file__).parent
print(f"当前目录: {current_dir}")

# 创建多级目录
output_dir = Path("output/reports")
output_dir.mkdir(parents=True, exist_ok=True)
print(f"目录已创建: {output_dir.exists()}")  # 目录已创建: True

# 检查文件是否存在
config_file = Path("config.yaml")
if config_file.exists():
    print(f"配置文件存在: {config_file.resolve()}")
else:
    print("配置文件不存在")

# 获取文件属性
test_file = Path("tests/test_api.py")
print(f"文件名: {test_file.name}")      # test_api.py
print(f"文件名(无后缀): {test_file.stem}")  # test_api
print(f"扩展名: {test_file.suffix}")    # .py
print(f"父目录: {test_file.parent}")    # tests

# 遍历目录下所有 .py 文件
tests_dir = Path("tests")
if tests_dir.exists():
    for py_file in tests_dir.glob("*.py"):
        print(f"发现文件: {py_file}")

# 递归遍历所有子目录中的 .py 文件
for py_file in tests_dir.rglob("*.py"):
    print(f"Python 文件: {py_file}")
```

**验收标准**：
- [ ] 正确使用 `pathlib.Path`
- [ ] `mkdir(parents=True, exist_ok=True)` 正确使用
- [ ] 文件属性获取正确
- [ ] `glob` 和 `rglob` 使用正确

---

**练习6：文件搜索与过滤**

**场景说明**：在测试项目中，经常需要查找特定类型的文件或按条件过滤文件。

**具体需求**：
1. 列出当前目录所有文件和目录
2. 只列出 `.txt` 文件
3. 递归列出所有子目录中的 `.py` 文件
4. 按修改时间排序文件（最新的在前）
5. 查找大于 1MB 的文件

**使用示例**：
```python
from pathlib import Path
import os

base_dir = Path(".")

# 列出当前目录所有文件和目录
all_items = list(base_dir.iterdir())
print(f"共 {len(all_items)} 个项目")

# 只列出 .txt 文件
txt_files = [f for f in base_dir.glob("*.txt") if f.is_file()]
print(f"TXT 文件: {[f.name for f in txt_files]}")

# 递归列出所有 .py 文件
py_files = list(base_dir.rglob("*.py"))
print(f"共找到 {len(py_files)} 个 Python 文件")

# 按修改时间排序
files_with_time = [(f, f.stat().st_mtime) for f in base_dir.iterdir() if f.is_file()]
sorted_files = sorted(files_with_time, key=lambda x: x[1], reverse=True)
for f, mtime in sorted_files[:5]:
    print(f"文件: {f.name}, 修改时间: {mtime}")

# 查找大于 1MB 的文件
large_files = []
for f in base_dir.rglob("*"):
    if f.is_file() and f.stat().st_size > 1024 * 1024:
        size_mb = f.stat().st_size / (1024 * 1024)
        large_files.append((f, size_mb))
        print(f"大文件: {f}, 大小: {size_mb:.2f}MB")
```

**验收标准**：
- [ ] 正确使用 `iterdir()`、`glob()`、`rglob()`
- [ ] 文件大小和修改时间获取正确
- [ ] 排序逻辑正确
- [ ] 大小单位换算正确（1MB = 1024*1024 bytes）

---

**练习7：模块导入**

**场景说明**：理解模块导入机制是组织测试代码的基础。

**具体需求**：
1. 创建 `my_utils.py` 模块，定义函数 `add(a, b)` 和 `multiply(a, b)`
2. 在另一个文件中使用 `import my_utils` 导入
3. 使用 `from my_utils import add` 导入特定函数
4. 使用 `import my_utils as utils` 起别名
5. 理解 `if __name__ == "__main__":` 的作用

**使用示例**：

```python
# my_utils.py
"""工具模块"""

def add(a, b):
    """加法运算"""
    return a + b

def multiply(a, b):
    """乘法运算"""
    return a * b

def main():
    """模块测试"""
    print(f"add(1, 2) = {add(1, 2)}")
    print(f"multiply(3, 4) = {multiply(3, 4)}")

if __name__ == "__main__":
    # 只有直接运行此文件时才执行
    main()
```

```python
# test_module.py
"""测试模块导入"""

# 方式1：导入整个模块
import my_utils
result1 = my_utils.add(1, 2)
print(f"方式1: {result1}")  # 方式1: 3

# 方式2：导入特定函数
from my_utils import multiply
result2 = multiply(3, 4)
print(f"方式2: {result2}")  # 方式2: 12

# 方式3：使用别名
import my_utils as utils
result3 = utils.add(5, 6)
print(f"方式3: {result3}")  # 方式3: 11

# 方式4：导入所有（不推荐）
from my_utils import *
result4 = add(7, 8)
print(f"方式4: {result4}")  # 方式4: 15
```

**验收标准**：
- [ ] 模块文件正确创建
- [ ] 四种导入方式都能正确使用
- [ ] 理解 `__name__` 的作用
- [ ] 模块文档字符串正确添加

---

**练习8：包结构**

**场景说明**：规范的包结构是组织测试项目的基础。

**具体需求**：
1. 创建包结构 `my_test_utils/`，包含 `__init__.py`、`validators.py`、`helpers.py`
2. 在 `__init__.py` 中导出公共接口
3. 使用相对导入在模块间引用
4. 从包导入模块和函数
5. 设置 `__all__` 控制导出内容

**使用示例**：

```
# 项目结构
my_test_utils/
├── __init__.py
├── validators.py
└── helpers.py
```

```python
# my_test_utils/validators.py
"""验证器模块"""

def is_valid_email(email):
    """验证邮箱格式"""
    return "@" in email and "." in email

def is_valid_phone(phone):
    """验证手机号格式"""
    return phone.isdigit() and len(phone) == 11
```

```python
# my_test_utils/helpers.py
"""辅助函数模块"""

def format_date(date_obj):
    """格式化日期"""
    return date_obj.strftime("%Y-%m-%d")

def get_timestamp():
    """获取时间戳"""
    import time
    return int(time.time())
```

```python
# my_test_utils/__init__.py
"""测试工具包"""

from .validators import is_valid_email, is_valid_phone
from .helpers import format_date, get_timestamp

# 控制 from my_test_utils import * 导入的内容
__all__ = ["is_valid_email", "is_valid_phone", "format_date", "get_timestamp"]

__version__ = "1.0.0"
```

```python
# 使用包
# 方式1：导入整个包
import my_test_utils
print(my_test_utils.is_valid_email("test@example.com"))  # True

# 方式2：从包导入函数
from my_test_utils import is_valid_phone, format_date
print(is_valid_phone("13800138000"))  # True

# 方式3：导入子模块
from my_test_utils.validators import is_valid_email
print(is_valid_email("invalid"))  # False

# 查看版本
print(my_test_utils.__version__)  # 1.0.0
```

**验收标准**：
- [ ] 包结构正确创建
- [ ] `__init__.py` 正确导出接口
- [ ] 相对导入正确使用
- [ ] `__all__` 正确设置

---

### 进阶练习（9-16）

---

**练习9：配置管理器**

**场景说明**：测试框架需要统一的配置管理，支持多种格式和环境变量覆盖。

**具体需求**：
1. 支持 YAML 和 JSON 格式自动识别
2. 支持环境变量覆盖配置（如 `${DB_HOST}`）
3. 支持热重载 `reload()` 方法
4. 支持点号访问 `get("db.host")`
5. 支持保存修改 `save()` 方法

**使用示例**：
```python
# config.yaml
"""
database:
  host: ${DB_HOST:localhost}
  port: 3306
  name: test_db
api:
  base_url: https://api.example.com
  timeout: 30
"""

# 使用配置管理器
config = ConfigManager("config.yaml")

# 点号访问嵌套配置
print(config.get("database.host"))  # localhost（或环境变量值）
print(config.get("database.port"))  # 3306
print(config.get("api.timeout"))    # 30

# 不存在的键返回默认值
print(config.get("database.user", "root"))  # root

# 修改配置
config.set("database.port", 3307)
config.save()  # 保存到文件

# 热重载
config.reload()

# 设置环境变量后重新加载
import os
os.environ["DB_HOST"] = "192.168.1.100"
config.reload()
print(config.get("database.host"))  # 192.168.1.100
```

**验收标准**：
- [ ] 自动识别 YAML/JSON 格式
- [ ] 环境变量覆盖正确
- [ ] 点号访问正确
- [ ] 保存和重载功能正常

---

**练习10：数据驱动测试框架**

**场景说明**：数据驱动测试需要从多种数据源加载测试数据。

**具体需求**：
1. `load_csv(filepath)` 加载 CSV 文件返回字典列表
2. `load_json(filepath)` 加载 JSON 文件
3. `load_yaml(filepath)` 加载 YAML 文件
4. `to_pytest_params(data)` 转为 pytest 参数化格式
5. 支持 `pytest.mark.parametrize` 装饰器

**使用示例**：
```python
# test_data.csv
"""
case_name,username,password,expected
登录成功,admin,123456,success
密码错误,admin,wrong,fail
"""

# 使用数据驱动
driver = DataDriver()

# 加载 CSV
csv_data = driver.load_csv("test_data.csv")
print(f"加载 {len(csv_data)} 条数据")

# 加载 JSON
json_data = driver.load_json("test_data.json")

# 加载 YAML
yaml_data = driver.load_yaml("test_data.yaml")

# 转为 pytest 参数
params = driver.to_pytest_params(csv_data, id_key="case_name")
# 返回 [("admin", "123456", "success"), ("admin", "wrong", "fail")]

# 配合 pytest 使用
import pytest

@pytest.mark.parametrize("username,password,expected", params)
def test_login(username, password, expected):
    # 测试逻辑
    pass
```

**验收标准**：
- [ ] 三种格式都能正确加载
- [ ] CSV 使用 DictReader
- [ ] 转换为 pytest 参数格式正确
- [ ] 异常处理完善

---

**练习11：测试报告生成器**

**场景说明**：测试执行后需要生成报告，支持多种格式输出。

**具体需求**：
1. `add_result(case_name, status, duration, message="")` 添加测试结果
2. `summary()` 返回统计信息字典
3. `save_json(filepath)` 保存 JSON 格式报告
4. `save_html(filepath)` 保存简单 HTML 报告
5. `compare_with_history(filepath)` 与历史报告对比

**使用示例**：
```python
# 创建报告生成器
report = ReportGenerator("测试报告")

# 添加测试结果
report.add_result("登录测试", "pass", 1.5)
report.add_result("搜索测试", "pass", 2.3)
report.add_result("下单测试", "fail", 3.0, "库存不足")
report.add_result("支付测试", "skip", 0, "依赖服务不可用")

# 获取统计
stats = report.summary()
print(stats)
# {'total': 4, 'passed': 2, 'failed': 1, 'skipped': 1, 'pass_rate': '50.0%'}

# 保存 JSON 报告
report.save_json("reports/test_report.json")

# 保存 HTML 报告
report.save_html("reports/test_report.html")

# 与历史报告对比
history_file = "reports/last_report.json"
if Path(history_file).exists():
    diff = report.compare_with_history(history_file)
    print(f"通过率变化: {diff['pass_rate_change']}")
```

**验收标准**：
- [ ] 结果添加和统计正确
- [ ] JSON 保存格式正确
- [ ] HTML 报告可读性好
- [ ] 历史对比功能正常

---

**练习12：日志系统**

**场景说明**：测试执行需要完善的日志记录系统。

**具体需求**：
1. 支持 `DEBUG/INFO/WARN/ERROR` 级别
2. 同时输出到文件和控制台
3. 按日期分割日志文件（如 `app_2024-01-15.log`）
4. 支持日志格式配置
5. 支持结构化 JSON 格式存储

**使用示例**：
```python
# 创建日志器
logger = Logger(
    name="test_logger",
    level="DEBUG",
    log_dir="logs",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 记录日志
logger.debug("调试信息：变量 x = 10")
logger.info("测试开始执行")
logger.warn("配置文件使用默认值")
logger.error("连接数据库失败")

# 设置级别
logger.set_level("INFO")
logger.debug("这条不会输出")  # 级别不够

# 输出到文件
logger.set_file("logs/test.log")

# 按 JSON 格式输出
logger.enable_json_format()
logger.info("测试完成", extra={"duration": 1.5, "status": "pass"})
# {"level": "INFO", "message": "测试完成", "duration": 1.5, "status": "pass", "timestamp": "..."}
```

**验收标准**：
- [ ] 四个级别正确实现
- [ ] 文件和控制台同时输出
- [ ] 日期分割功能正常
- [ ] JSON 格式正确

---

**练习13：缓存管理**

**场景说明**：接口测试中需要缓存响应数据，减少重复请求。

**具体需求**：
1. `cache_get(key)` 获取缓存，不存在返回 `None`
2. `cache_set(key, value, ttl=300)` 设置缓存和过期时间
3. `cache_delete(key)` 删除指定缓存
4. `cache_clear()` 清空所有缓存
5. 自动过期清理（惰性删除）

**使用示例**：
```python
# 创建文件缓存
cache = FileCache(cache_dir=".cache")

# 设置缓存
cache.cache_set("user:1001", {"name": "张三", "age": 25}, ttl=60)
cache.cache_set("api:config", {"timeout": 30}, ttl=300)

# 获取缓存
user = cache.cache_get("user:1001")
print(user)  # {'name': '张三', 'age': 25}

# 缓存不存在
data = cache.cache_get("not_exist")
print(data)  # None

# 删除缓存
cache.cache_delete("user:1001")
print(cache.cache_get("user:1001"))  # None

# 清空缓存
cache.cache_clear()

# TTL 过期测试
cache.cache_set("temp", "value", ttl=1)
time.sleep(2)
print(cache.cache_get("temp"))  # None（已过期）
```

**验收标准**：
- [ ] 缓存存取正确
- [ ] TTL 过期机制正常
- [ ] 删除和清空功能正常
- [ ] 文件存储格式正确

---

**练习14：文件监控**

**场景说明**：测试过程中需要监控配置文件或日志文件的变化。

**具体需求**：
1. `watch(path, callback)` 监控指定路径
2. `on_modified(callback)` 文件修改回调
3. `on_created(callback)` 文件创建回调
4. `on_deleted(callback)` 文件删除回调
5. `stop()` 停止监控

**使用示例**：
```python
# 创建文件监控器
watcher = FileWatcher()

# 定义回调函数
def on_modified(event):
    print(f"文件被修改: {event.path}")

def on_created(event):
    print(f"文件被创建: {event.path}")

def on_deleted(event):
    print(f"文件被删除: {event.path}")

# 注册回调
watcher.on_modified(on_modified)
watcher.on_created(on_created)
watcher.on_deleted(on_deleted)

# 开始监控
watcher.watch("config.yaml")
watcher.watch("logs/")

# 运行一段时间后停止
time.sleep(60)
watcher.stop()
```

**验收标准**：
- [ ] 监控启动和停止正常
- [ ] 三种事件回调正确触发
- [ ] 支持监控目录
- [ ] 资源正确释放

---

**练习15：批量文件处理**

**场景说明**：测试数据文件需要批量处理和转换。

**具体需求**：
1. `process_all(directory, processor)` 处理目录下所有文件
2. `rename_files(directory, pattern, replacement)` 批量重命名
3. `copy_with_structure(src, dst)` 复制并保持目录结构
4. `find_and_replace(directory, old_text, new_text)` 查找替换内容
5. `generate_manifest(directory)` 生成文件清单（JSON 格式）

**使用示例**：
```python
# 创建批量处理器
processor = BatchFileProcessor()

# 处理所有文件
def to_uppercase(content):
    return content.upper()

processor.process_all("data/", to_uppercase)

# 批量重命名（test_*.py -> test_*_new.py）
processor.rename_files("tests/", r"test_(.*).py", r"test_\1_new.py")

# 复制保持结构
processor.copy_with_structure("source/", "backup/")

# 查找替换
processor.find_and_replace("config/", "localhost", "127.0.0.1")

# 生成文件清单
manifest = processor.generate_manifest("project/")
print(json.dumps(manifest, indent=2))
# {
#   "files": [
#     {"path": "main.py", "size": 1024, "modified": "2024-01-15"},
#     ...
#   ],
#   "total_size": 10240,
#   "file_count": 10
# }
```

**验收标准**：
- [ ] 批量处理功能正常
- [ ] 重命名正则正确
- [ ] 目录结构保持完整
- [ ] 清单格式正确

---

**练习16：测试数据生成器**

**场景说明**：测试需要大量模拟数据，需要数据生成工具。

**具体需求**：
1. `generate_users(n)` 生成 n 个用户数据
2. `generate_orders(n)` 生成 n 个订单数据
3. `save_to_csv(data, path)` 保存为 CSV
4. `save_to_json(data, path)` 保存为 JSON
5. `load_template(template_path)` 加载模板生成数据

**使用示例**：
```python
# 创建数据生成器
generator = TestDataGenerator()

# 生成用户数据
users = generator.generate_users(10)
print(f"生成 {len(users)} 个用户")
print(users[0])
# {'id': 1, 'username': 'user_001', 'email': 'user_001@test.com', 'age': 25}

# 生成订单数据
orders = generator.generate_orders(5)
print(orders[0])
# {'order_id': 'ORD001', 'user_id': 1, 'amount': 99.9, 'status': 'pending'}

# 保存为 CSV
generator.save_to_csv(users, "data/users.csv")

# 保存为 JSON
generator.save_to_json(orders, "data/orders.json")

# 使用模板生成
template = {
    "name": "{prefix}_{index}",
    "value": "{random_int}"
}
data = generator.load_template("template.json", count=3, prefix="test")
```

**验收标准**：
- [ ] 用户和订单数据格式正确
- [ ] CSV 和 JSON 保存正确
- [ ] ID 自动递增
- [ ] 模板功能正常

---

### 综合练习（17-20）

---

**练习17：搭建测试项目**

**场景说明**：从零搭建一个规范的测试项目结构。

**具体需求**：
1. 创建标准项目目录结构
2. 编写 `requirements.txt` 依赖文件
3. 编写 `pytest.ini` 配置文件
4. 创建 `conftest.py` 共享 fixtures
5. 创建示例测试文件

**使用示例**：

```
# 项目结构
my_test_project/
├── README.md
├── requirements.txt
├── pytest.ini
├── config/
│   ├── __init__.py
│   ├── settings.yaml
│   └── settings.local.yaml
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   │   ├── __init__.py
│   │   └── test_login.py
│   └── data/
│       ├── users.csv
│       └── orders.json
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   └── http_client.py
└── reports/
    └── .gitkeep
```

```python
# requirements.txt
"""
requests==2.31.0
pytest==7.4.0
pyyaml==6.0.1
"""

# pytest.ini
"""
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
"""

# tests/conftest.py
import pytest
from utils.config import Config

@pytest.fixture(scope="session")
def config():
    """加载配置"""
    return Config.load("config/settings.yaml")

@pytest.fixture
def api_client(config):
    """API 客户端"""
    from utils.http_client import HttpClient
    client = HttpClient(config.get("api.base_url"))
    yield client
    client.close()
```

**验收标准**：
- [ ] 目录结构完整规范
- [ ] 配置文件正确
- [ ] fixtures 可正常使用
- [ ] pytest 可正常运行

---

**练习18：多环境配置管理**

**场景说明**：测试需要在 dev/test/staging/prod 等多环境运行。

**具体需求**：
1. 支持 dev/test/staging/prod 四种环境
2. 根据环境变量 `ENV` 切换配置
3. 配置继承（base -> env -> local）
4. 敏感信息从环境变量读取
5. 配置验证和默认值

**使用示例**：
```python
# 配置文件结构
# config/
# ├── base.yaml        # 基础配置
# ├── dev.yaml         # 开发环境
# ├── test.yaml        # 测试环境
# ├── staging.yaml     # 预发布环境
# └── prod.yaml        # 生产环境

# 使用
import os
os.environ["ENV"] = "test"
os.environ["DB_PASSWORD"] = "secret123"

config = EnvironmentConfig()
config.load()

print(config.get("database.host"))     # test.db.example.com
print(config.get("database.password")) # secret123（从环境变量）

# 切换环境
config.switch_env("dev")
print(config.get("database.host"))     # localhost

# 配置继承
# base.yaml: database.timeout: 30
# dev.yaml: database.host: localhost
# 最终: database.host=localhost, database.timeout=30
```

**验收标准**：
- [ ] 环境切换正确
- [ ] 配置继承正常
- [ ] 环境变量覆盖正确
- [ ] 默认值机制正常

---

**练习19：测试数据版本管理**

**场景说明**：测试数据需要版本控制，支持回滚和对比。

**具体需求**：
1. `snapshot(data_dir)` 创建数据快照
2. `restore(version)` 恢复到指定版本
3. `diff(v1, v2)` 对比两个版本差异
4. `list_versions()` 列出所有版本
5. `auto_cleanup(keep=10)` 自动清理旧版本

**使用示例**：
```python
# 创建版本管理器
manager = DataVersionManager("test_data/")

# 创建快照
v1 = manager.snapshot()
print(f"创建版本: {v1}")  # v1.0_20240115_103000

# 修改数据后创建新快照
# ... 修改文件 ...
v2 = manager.snapshot()
print(f"创建版本: {v2}")  # v1.1_20240115_110000

# 列出所有版本
versions = manager.list_versions()
print(versions)  # ['v1.0_20240115_103000', 'v1.1_20240115_110000']

# 对比版本差异
diff = manager.diff(v1, v2)
print(diff)
# {'added': ['new_file.csv'], 'modified': ['users.csv'], 'deleted': []}

# 恢复到旧版本
manager.restore(v1)

# 自动清理（保留最近 10 个版本）
manager.auto_cleanup(keep=10)
```

**验收标准**：
- [ ] 快照创建正确
- [ ] 版本恢复正常
- [ ] 差异对比准确
- [ ] 清理功能正常

---

**练习20：插件化配置加载器**

**场景说明**：支持多种配置格式，可扩展新格式。

**具体需求**：
1. `register_loader(ext, loader)` 注册格式加载器
2. `load(path)` 根据扩展名自动选择加载器
3. 内置支持 `.yaml/.json/.toml/.ini`
4. 支持远程配置（HTTP URL）
5. 支持配置合并策略

**使用示例**：
```python
# 创建配置加载器
loader = ConfigLoader()

# 加载本地文件（自动识别格式）
yaml_config = loader.load("config/settings.yaml")
json_config = loader.load("config/settings.json")
ini_config = loader.load("config/settings.ini")

# 加载远程配置
remote_config = loader.load("https://example.com/config.json")

# 注册自定义加载器
def load_xml(filepath):
    import xml.etree.ElementTree as ET
    tree = ET.parse(filepath)
    return {elem.tag: elem.text for elem in tree.getroot()}

loader.register_loader(".xml", load_xml)
xml_config = loader.load("config/settings.xml")

# 配置合并
merged = loader.merge([
    "config/base.yaml",
    "config/env.yaml",
    "config/local.yaml"
], strategy="deep")  # 深度合并
```

**验收标准**：
- [ ] 四种格式正确加载
- [ ] 远程配置正常
- [ ] 自定义加载器正常
- [ ] 合并策略正确

## 五、检验标准

### 自测题

---

#### 题目1：JSON 文件合并与处理（综合考察：JSON 读写、异常处理、文件操作）

**场景描述**：在接口测试中，经常需要将多个测试数据 JSON 文件合并成一个文件，并进行去重和排序。

**详细需求**：
1. 实现 `merge_json_files(filepaths, output)` 函数
2. 支持合并多个 JSON 文件（列表格式或对象格式）
3. 如果是列表，合并后去重（根据 `id` 字段）
4. 如果是对象，深度合并（嵌套字典）
5. 处理文件不存在和 JSON 格式错误异常
6. 输出格式化的 JSON 文件

**测试用例**：
```python
import json
import os
import tempfile

def test_merge_json_files():
    """测试 JSON 文件合并"""
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()

    # 创建测试文件1
    file1 = os.path.join(temp_dir, "users1.json")
    with open(file1, "w", encoding="utf-8") as f:
        json.dump([
            {"id": 1, "name": "张三", "age": 25},
            {"id": 2, "name": "李四", "age": 30}
        ], f)

    # 创建测试文件2
    file2 = os.path.join(temp_dir, "users2.json")
    with open(file2, "w", encoding="utf-8") as f:
        json.dump([
            {"id": 2, "name": "李四", "age": 30},  # 重复
            {"id": 3, "name": "王五", "age": 28}
        ], f)

    # 合并文件
    output = os.path.join(temp_dir, "merged.json")
    merge_json_files([file1, file2], output)

    # 验证结果
    with open(output, "r", encoding="utf-8") as f:
        merged = json.load(f)

    assert len(merged) == 3  # 去重后应为3条
    assert merged[0]["id"] == 1
    assert merged[1]["id"] == 2
    assert merged[2]["id"] == 3

    # 测试异常处理
    try:
        merge_json_files(["not_exist.json"], output)
    except FileNotFoundError:
        print("正确抛出 FileNotFoundError")

    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print("测试通过!")

if __name__ == "__main__":
    test_merge_json_files()
```

---

#### 题目2：CSV 数据处理与转换（综合考察：CSV 读写、数据过滤、文件操作）

**场景描述**：数据驱动测试需要从 CSV 文件中筛选特定条件的数据，并转换为其他格式。

**详细需求**：
1. 实现 `filter_csv(input_file, output_file, column, value)` 函数
2. 实现 `csv_to_json(csv_file, json_file)` 转换函数
3. 实现按多列筛选 `filter_csv_multi(input_file, output_file, filters)`
4. 处理 CSV 文件不存在的情况
5. 支持自定义分隔符

**测试用例**：
```python
import csv
import json
import os
import tempfile

def test_csv_operations():
    """测试 CSV 操作"""
    temp_dir = tempfile.mkdtemp()

    # 创建测试 CSV 文件
    csv_file = os.path.join(temp_dir, "test_data.csv")
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["case_name", "status", "priority", "duration"])
        writer.writeheader()
        writer.writerow({"case_name": "登录测试", "status": "pass", "priority": "P0", "duration": "1.5"})
        writer.writerow({"case_name": "搜索测试", "status": "fail", "priority": "P1", "duration": "2.0"})
        writer.writerow({"case_name": "下单测试", "status": "pass", "priority": "P0", "duration": "3.0"})
        writer.writerow({"case_name": "支付测试", "status": "skip", "priority": "P2", "duration": "0"})

    # 测试单列筛选
    output1 = os.path.join(temp_dir, "filtered.csv")
    filter_csv(csv_file, output1, "status", "pass")

    with open(output1, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2
    print(f"单列筛选: {len(rows)} 条记录")

    # 测试多列筛选
    output2 = os.path.join(temp_dir, "filtered_multi.csv")
    filter_csv_multi(csv_file, output2, {"status": "pass", "priority": "P0"})

    with open(output2, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2
    print(f"多列筛选: {len(rows)} 条记录")

    # 测试 CSV 转 JSON
    json_file = os.path.join(temp_dir, "test_data.json")
    csv_to_json(csv_file, json_file)

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 4
    assert data[0]["case_name"] == "登录测试"
    print(f"CSV 转 JSON: {len(data)} 条记录")

    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print("测试通过!")

if __name__ == "__main__":
    test_csv_operations()
```

---

#### 题目3：路径处理与文件搜索（综合考察：pathlib、文件操作、异常处理）

**场景描述**：测试项目需要查找和管理各种测试文件。

**详细需求**：
1. 实现 `find_files(directory, pattern)` 递归查找文件
2. 实现 `get_file_info(filepath)` 获取文件详细信息
3. 实现 `organize_files(src_dir, dst_dir, by="ext")` 按扩展名分类整理文件
4. 实现 `find_duplicates(directory)` 查找重复文件（按内容 hash）
5. 处理路径不存在和权限不足异常

**测试用例**：
```python
import os
import tempfile
from pathlib import Path
import hashlib

def test_file_operations():
    """测试文件操作"""
    temp_dir = tempfile.mkdtemp()

    # 创建测试文件结构
    Path(temp_dir, "test1.py").write_text("print('test1')")
    Path(temp_dir, "test2.py").write_text("print('test2')")
    Path(temp_dir, "data.json").write_text('{"key": "value"}')
    Path(temp_dir, "config.yaml").write_text("name: test")

    subdir = Path(temp_dir, "subdir")
    subdir.mkdir()
    Path(subdir, "test3.py").write_text("print('test3')")

    # 测试递归查找
    py_files = find_files(temp_dir, "*.py")
    assert len(py_files) == 3
    print(f"找到 {len(py_files)} 个 Python 文件")

    # 测试获取文件信息
    info = get_file_info(Path(temp_dir, "test1.py"))
    assert info["name"] == "test1.py"
    assert info["size"] > 0
    assert info["extension"] == ".py"
    print(f"文件信息: {info}")

    # 测试按扩展名整理
    organize_dir = os.path.join(temp_dir, "organized")
    organize_files(temp_dir, organize_dir, by="ext")

    assert Path(organize_dir, ".py").exists()
    assert Path(organize_dir, ".json").exists()
    print("文件整理完成")

    # 测试查找重复文件
    # 创建重复文件
    Path(temp_dir, "test1_copy.py").write_text("print('test1')")

    duplicates = find_duplicates(temp_dir)
    assert len(duplicates) >= 1  # 至少有一组重复
    print(f"找到 {len(duplicates)} 组重复文件")

    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print("测试通过!")

if __name__ == "__main__":
    test_file_operations()
```

---

#### 题目4：配置管理系统（综合考察：YAML/JSON、模块化、异常处理）

**场景描述**：测试框架需要统一的配置管理，支持多环境、热重载和验证。

**详细需求**：

**ConfigManager 类**：
1. `__init__(self, config_path)` 初始化配置
2. `load()` 加载配置文件（自动识别 YAML/JSON）
3. `get(key, default=None)` 点号访问嵌套配置
4. `set(key, value)` 设置配置值
5. `save()` 保存配置到文件
6. `reload()` 重新加载配置
7. `validate(schema)` 验证配置是否符合 schema

**环境变量支持**：
1. 支持 `${ENV_VAR}` 格式引用环境变量
2. 支持 `${ENV_VAR:default}` 格式设置默认值

**测试用例**：
```python
import os
import json
import tempfile
import yaml

def test_config_manager():
    """测试配置管理器"""
    temp_dir = tempfile.mkdtemp()
    config_file = os.path.join(temp_dir, "config.yaml")

    # 创建测试配置
    config_data = {
        "database": {
            "host": "${DB_HOST:localhost}",
            "port": 3306,
            "name": "test_db"
        },
        "api": {
            "base_url": "https://api.example.com",
            "timeout": 30
        }
    }

    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    # 测试基本加载
    config = ConfigManager(config_file)
    config.load()

    # 测试点号访问
    assert config.get("database.port") == 3306
    assert config.get("api.base_url") == "https://api.example.com"
    print("点号访问测试通过")

    # 测试默认值
    assert config.get("not.exist", "default") == "default"
    assert config.get("database.user", "root") == "root"
    print("默认值测试通过")

    # 测试环境变量
    os.environ["DB_HOST"] = "192.168.1.100"
    config.reload()
    assert config.get("database.host") == "192.168.1.100"
    print("环境变量测试通过")

    # 测试设置和保存
    config.set("database.port", 3307)
    config.save()

    # 重新加载验证
    config.reload()
    assert config.get("database.port") == 3307
    print("设置和保存测试通过")

    # 测试配置验证
    schema = {
        "database.host": {"type": str, "required": True},
        "database.port": {"type": int, "required": True, "range": [1, 65535]}
    }
    assert config.validate(schema) == True
    print("配置验证测试通过")

    # 清理
    del os.environ["DB_HOST"]
    import shutil
    shutil.rmtree(temp_dir)
    print("所有测试通过!")

if __name__ == "__main__":
    test_config_manager()
```

---

### 答案

#### 题目1 答案

```python
import json
from pathlib import Path
from typing import List, Union

def merge_json_files(filepaths: List[str], output: str) -> None:
    """
    合并多个 JSON 文件到一个文件

    Args:
        filepaths: JSON 文件路径列表
        output: 输出文件路径

    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON 格式错误
    """
    merged_data = []
    seen_ids = set()  # 用于去重

    for filepath in filepaths:
        # 检查文件是否存在
        if not Path(filepath).exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")

        # 读取 JSON 文件
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"文件 {filepath} JSON 格式错误: {e}", e.doc, e.pos)

        # 处理不同格式的数据
        if isinstance(data, list):
            # 列表格式：合并并去重
            for item in data:
                if isinstance(item, dict) and 'id' in item:
                    item_id = item['id']
                    if item_id not in seen_ids:
                        seen_ids.add(item_id)
                        merged_data.append(item)
                else:
                    # 没有 id 字段，直接添加
                    merged_data.append(item)
        elif isinstance(data, dict):
            # 对象格式：深度合并
            if not merged_data or not isinstance(merged_data, dict):
                if merged_data:
                    # 如果已有列表数据，将对象转为列表元素
                    merged_data = {}
            merged_data = _deep_merge(merged_data, data)
        else:
            # 其他类型（字符串、数字等）
            merged_data.append(data)

    # 如果是列表数据，按 id 排序
    if isinstance(merged_data, list) and merged_data and 'id' in merged_data[0]:
        merged_data.sort(key=lambda x: x.get('id', 0))

    # 写入输出文件
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)


def _deep_merge(dict1: dict, dict2: dict) -> dict:
    """深度合并两个字典"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


# 使用示例
if __name__ == "__main__":
    # 合并多个 JSON 文件
    merge_json_files(
        ["data/users1.json", "data/users2.json"],
        "data/merged_users.json"
    )
    print("合并完成!")
```

---

#### 题目2 答案

```python
import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

def filter_csv(input_file: str, output_file: str, column: str, value: str) -> int:
    """
    过滤 CSV 文件中指定列等于指定值的行

    Args:
        input_file: 输入 CSV 文件路径
        output_file: 输出 CSV 文件路径
        column: 列名
        value: 过滤值

    Returns:
        过滤后的行数

    Raises:
        FileNotFoundError: 文件不存在
        KeyError: 列名不存在
    """
    if not Path(input_file).exists():
        raise FileNotFoundError(f"文件不存在: {input_file}")

    filtered_rows = []
    fieldnames = None

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        # 检查列名是否存在
        if column not in fieldnames:
            raise KeyError(f"列名 '{column}' 不存在，可用列: {fieldnames}")

        # 过滤数据
        for row in reader:
            if row.get(column) == value:
                filtered_rows.append(row)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    return len(filtered_rows)


def filter_csv_multi(input_file: str, output_file: str, filters: Dict[str, str]) -> int:
    """
    按多列条件过滤 CSV 文件

    Args:
        input_file: 输入 CSV 文件路径
        output_file: 输出 CSV 文件路径
        filters: 过滤条件字典 {列名: 值}

    Returns:
        过滤后的行数
    """
    if not Path(input_file).exists():
        raise FileNotFoundError(f"文件不存在: {input_file}")

    filtered_rows = []
    fieldnames = None

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        # 检查列名
        for col in filters.keys():
            if col not in fieldnames:
                raise KeyError(f"列名 '{col}' 不存在")

        # 过滤数据（所有条件都满足）
        for row in reader:
            if all(row.get(col) == val for col, val in filters.items()):
                filtered_rows.append(row)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    return len(filtered_rows)


def csv_to_json(csv_file: str, json_file: str, encoding: str = 'utf-8') -> int:
    """
    将 CSV 文件转换为 JSON 文件

    Args:
        csv_file: CSV 文件路径
        json_file: JSON 文件路径
        encoding: 文件编码

    Returns:
        转换的记录数
    """
    if not Path(csv_file).exists():
        raise FileNotFoundError(f"文件不存在: {csv_file}")

    data = []

    with open(csv_file, 'r', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(dict(row))

    with open(json_file, 'w', encoding=encoding) as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return len(data)


# 使用示例
if __name__ == "__main__":
    # 单列筛选
    count = filter_csv("test_data.csv", "filtered.csv", "status", "pass")
    print(f"筛选出 {count} 条记录")

    # 多列筛选
    count = filter_csv_multi("test_data.csv", "filtered_multi.csv",
                              {"status": "pass", "priority": "P0"})
    print(f"多列筛选出 {count} 条记录")

    # CSV 转 JSON
    count = csv_to_json("test_data.csv", "test_data.json")
    print(f"转换 {count} 条记录到 JSON")
```

---

#### 题目3 答案

```python
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

def find_files(directory: str, pattern: str) -> List[Path]:
    """
    递归查找目录下所有匹配模式的文件

    Args:
        directory: 搜索目录
        pattern: 文件模式（如 *.py）

    Returns:
        匹配的文件路径列表
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")

    return list(dir_path.rglob(pattern))


def get_file_info(filepath: str) -> Dict[str, Any]:
    """
    获取文件详细信息

    Args:
        filepath: 文件路径

    Returns:
        文件信息字典
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    stat = path.stat()

    return {
        "name": path.name,
        "stem": path.stem,
        "extension": path.suffix,
        "size": stat.st_size,
        "size_human": _format_size(stat.st_size),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "parent": str(path.parent)
    }


def _format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def organize_files(src_dir: str, dst_dir: str, by: str = "ext") -> Dict[str, int]:
    """
    按扩展名分类整理文件

    Args:
        src_dir: 源目录
        dst_dir: 目标目录
        by: 分类方式（ext/date/size）

    Returns:
        各类别文件数量
    """
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)

    if not src_path.exists():
        raise FileNotFoundError(f"源目录不存在: {src_dir}")

    dst_path.mkdir(parents=True, exist_ok=True)
    counts = {}

    for file in src_path.rglob("*"):
        if not file.is_file():
            continue

        # 确定分类
        if by == "ext":
            category = file.suffix.lower() or "no_extension"
        elif by == "date":
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            category = mtime.strftime("%Y-%m")
        elif by == "size":
            size = file.stat().st_size
            if size < 1024:
                category = "small"
            elif size < 1024 * 1024:
                category = "medium"
            else:
                category = "large"
        else:
            category = "other"

        # 创建目标目录
        category_dir = dst_path / category
        category_dir.mkdir(exist_ok=True)

        # 复制文件
        import shutil
        dst_file = category_dir / file.name
        shutil.copy2(file, dst_file)

        counts[category] = counts.get(category, 0) + 1

    return counts


def find_duplicates(directory: str) -> List[List[str]]:
    """
    查找重复文件（按内容 hash）

    Args:
        directory: 搜索目录

    Returns:
        重复文件组列表
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")

    # 计算所有文件的 hash
    hash_map: Dict[str, List[str]] = {}

    for file in dir_path.rglob("*"):
        if not file.is_file():
            continue

        file_hash = _calculate_hash(file)
        if file_hash not in hash_map:
            hash_map[file_hash] = []
        hash_map[file_hash].append(str(file))

    # 找出重复的文件组
    duplicates = [files for files in hash_map.values() if len(files) > 1]
    return duplicates


def _calculate_hash(filepath: Path, chunk_size: int = 8192) -> str:
    """计算文件 MD5 hash"""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


# 使用示例
if __name__ == "__main__":
    # 查找文件
    py_files = find_files("tests", "*.py")
    print(f"找到 {len(py_files)} 个 Python 文件")

    # 获取文件信息
    info = get_file_info("config.yaml")
    print(f"文件信息: {info}")

    # 整理文件
    counts = organize_files("downloads", "organized", by="ext")
    print(f"整理结果: {counts}")

    # 查找重复文件
    duplicates = find_duplicates("data")
    for group in duplicates:
        print(f"重复文件组: {group}")
```

---

#### 题目4 答案

```python
import os
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, List

class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._raw_config: Dict[str, Any] = {}

    def load(self) -> None:
        """加载配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        # 根据扩展名选择加载方式
        suffix = self.config_path.suffix.lower()

        with open(self.config_path, 'r', encoding='utf-8') as f:
            if suffix in ['.yaml', '.yml']:
                try:
                    import yaml
                    self._raw_config = yaml.safe_load(f) or {}
                except ImportError:
                    raise ImportError("需要安装 PyYAML: pip install pyyaml")
            elif suffix == '.json':
                self._raw_config = json.load(f)
            else:
                raise ValueError(f"不支持的配置格式: {suffix}")

        # 处理环境变量
        self._config = self._process_env_vars(self._raw_config)

    def _process_env_vars(self, data: Any) -> Any:
        """处理配置中的环境变量"""
        if isinstance(data, dict):
            return {k: self._process_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._process_env_vars(item) for item in data]
        elif isinstance(data, str):
            return self._replace_env_var(data)
        return data

    def _replace_env_var(self, value: str) -> str:
        """替换环境变量 ${VAR} 或 ${VAR:default}"""
        pattern = r'\$\{([^}]+)\}'

        def replacer(match):
            expr = match.group(1)
            if ':' in expr:
                var_name, default = expr.split(':', 1)
                return os.environ.get(var_name, default)
            else:
                return os.environ.get(expr, match.group(0))

        return re.sub(pattern, replacer, value)

    def get(self, key: str, default: Any = None) -> Any:
        """
        点号访问嵌套配置

        Args:
            key: 配置键，支持点号分隔（如 "database.host"）
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split('.')
        data = self._raw_config

        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]

        data[keys[-1]] = value

        # 重新处理环境变量
        self._config = self._process_env_vars(self._raw_config)

    def save(self) -> None:
        """保存配置到文件"""
        suffix = self.config_path.suffix.lower()

        with open(self.config_path, 'w', encoding='utf-8') as f:
            if suffix in ['.yaml', '.yml']:
                try:
                    import yaml
                    yaml.dump(self._raw_config, f, allow_unicode=True, default_flow_style=False)
                except ImportError:
                    raise ImportError("需要安装 PyYAML")
            elif suffix == '.json':
                json.dump(self._raw_config, f, indent=2, ensure_ascii=False)

    def reload(self) -> None:
        """重新加载配置"""
        self.load()

    def validate(self, schema: Dict[str, Dict]) -> bool:
        """
        验证配置是否符合 schema

        Args:
            schema: 验证规则
                {
                    "key": {"type": type, "required": bool, "range": [min, max]}
                }

        Returns:
            验证是否通过

        Raises:
            ValueError: 验证失败
        """
        for key, rules in schema.items():
            value = self.get(key)
            required = rules.get('required', False)

            # 检查必填
            if required and value is None:
                raise ValueError(f"缺少必填配置: {key}")

            if value is None:
                continue

            # 检查类型
            expected_type = rules.get('type')
            if expected_type and not isinstance(value, expected_type):
                raise ValueError(f"配置 {key} 类型错误: 期望 {expected_type}, 实际 {type(value)}")

            # 检查范围
            if 'range' in rules and isinstance(value, (int, float)):
                min_val, max_val = rules['range']
                if not (min_val <= value <= max_val):
                    raise ValueError(f"配置 {key} 超出范围: {min_val} - {max_val}")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """导出为字典"""
        return self._config.copy()


# 使用示例
if __name__ == "__main__":
    # 创建配置管理器
    config = ConfigManager("config/settings.yaml")
    config.load()

    # 获取配置
    print(config.get("database.host"))
    print(config.get("api.timeout", 30))

    # 设置配置
    config.set("database.port", 3307)
    config.save()

    # 验证配置
    schema = {
        "database.host": {"type": str, "required": True},
        "database.port": {"type": int, "required": True, "range": [1, 65535]}
    }
    config.validate(schema)
```

---

### 自测检查清单

完成以上练习后，请对照以下清单进行自我检查：

#### 文件操作
- [ ] 能熟练使用 `with` 语句管理文件资源
- [ ] 理解 `r/w/a/rb/wb` 等文件模式
- [ ] 能正确处理文件编码（utf-8）
- [ ] 能使用 `read()/readline()/readlines()` 读取文件
- [ ] 能使用 `write()/writelines()` 写入文件

#### JSON 处理
- [ ] 理解 `json.dumps()/json.loads()` 的区别
- [ ] 理解 `json.dump()/json.load()` 的区别
- [ ] 能使用 `indent` 和 `ensure_ascii` 格式化输出
- [ ] 能处理 `JSONDecodeError` 异常

#### YAML 处理
- [ ] 能安装和使用 PyYAML
- [ ] 理解 `yaml.safe_load()` 的安全性
- [ ] 能使用 `yaml.dump()` 保存配置
- [ ] 能处理 `YAMLError` 异常

#### CSV 处理
- [ ] 能使用 `csv.DictReader` 读取 CSV
- [ ] 能使用 `csv.DictWriter` 写入 CSV
- [ ] 理解 `newline=""` 参数的作用
- [ ] 能处理 CSV 数据过滤和转换

#### 路径处理
- [ ] 能使用 `pathlib.Path` 处理路径
- [ ] 能使用 `glob()/rglob()` 搜索文件
- [ ] 能使用 `mkdir(parents=True, exist_ok=True)` 创建目录
- [ ] 能获取文件属性（大小、修改时间等）

#### 模块与包
- [ ] 理解 `import` 的几种方式
- [ ] 理解 `__init__.py` 的作用
- [ ] 理解 `__name__ == "__main__"` 的作用
- [ ] 能创建规范的包结构

---

## 六、本周小结

### 核心要点

1. **文件操作**：with 语句自动管理资源
2. **JSON**：接口测试必备，dumps/loads 和 dump/load
3. **YAML**：配置文件首选，比 JSON 更易读
4. **CSV**：数据驱动测试常用格式
5. **pathlib**：现代路径处理方式
6. **模块化**：规范的项目结构是专业测试的基础

### 下周预告

第4周开始进入 Pytest 测试框架，这是 Python 测试的核心技能。
