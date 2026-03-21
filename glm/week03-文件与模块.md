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

**练习1：文件读写基础**
```python
# 1. 写入文本文件 "hello.txt"，内容为 "Hello, Python!"
# 2. 读取文件内容并打印
# 3. 追加一行 "Welcome to testing!"
# 4. 读取所有行到列表
# 5. 使用 with 语句确保文件关闭
```

**练习2：JSON 文件操作**
```python
data = {
    "users": [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 30}
    ],
    "settings": {"timeout": 30, "retry": 3}
}
# 1. 将 data 保存为 users.json
# 2. 读取 users.json 并打印
# 3. 添加一个用户并保存
# 4. 美化输出（indent=2）
# 5. 处理 JSONDecodeError 异常
```

**练习3：CSV 文件操作**
```python
# 1. 创建测试数据 CSV：username,password,expected
# 2. 读取 CSV 并打印每行
# 3. 使用 csv.DictReader 读取
# 4. 筛选出 expected=true 的行
# 5. 追加新行到 CSV
```

**练习4：YAML 配置文件**
```python
# config.yaml 内容：
# database:
#   host: localhost
#   port: 3306
#   name: test_db

# 1. 使用 PyYAML 读取配置
# 2. 访问 database.host
# 3. 修改 port 并保存
# 4. 处理 YAML 解析异常
# 5. 支持环境变量 ${DB_HOST}
```

**练习5：路径操作**
```python
from pathlib import Path
# 1. 获取当前脚本所在目录
# 2. 创建 output/reports 目录
# 3. 检查文件是否存在
# 4. 获取文件扩展名
# 5. 遍历目录下所有 .py 文件
```

**练习6：文件搜索与过滤**
```python
# 1. 列出当前目录所有文件
# 2. 只列出 .txt 文件
# 3. 递归列出所有子目录中的 .py 文件
# 4. 按修改时间排序文件
# 5. 查找大于 1MB 的文件
```

**练习7：模块导入**
```python
# 创建 my_utils.py 模块
# 1. 定义函数 add(a, b)
# 2. 在另一个文件中 import my_utils
# 3. 使用 from my_utils import add
# 4. 使用 import my_utils as utils
# 5. 理解 __name__ == "__main__"
```

**练习8：包结构**
```python
# 创建包结构：
# my_package/
# ├── __init__.py
# ├── utils.py
# └── subpackage/
#     └── __init__.py

# 1. 创建 __init__.py 导出公共接口
# 2. 使用相对导入
# 3. 从包导入模块
# 4. 设置 __all__
```

### 进阶练习（9-16）

**练习9：配置管理器**
```python
class ConfigManager:
    """配置管理器"""
    # 1. 支持 YAML 和 JSON 格式
    # 2. 支持环境变量覆盖
    # 3. 支持热重载 reload()
    # 4. 支持点号访问 get("db.host")
    # 5. 支持保存修改 save()
```

**练习10：数据驱动测试框架**
```python
class DataDriver:
    """数据驱动测试"""
    # 1. load_csv() 加载 CSV
    # 2. load_json() 加载 JSON
    # 3. load_yaml() 加载 YAML
    # 4. to_pytest_params() 转为 pytest 参数
    # 5. 支持 pytest.mark.parametrize
```

**练习11：测试报告生成器**
```python
class ReportGenerator:
    """测试报告生成器"""
    # 1. add_result() 添加结果
    # 2. summary() 统计信息
    # 3. save_json() 保存 JSON
    # 4. save_html() 保存 HTML
    # 5. compare_with_history() 历史对比
```

**练习12：日志系统**
```python
class Logger:
    """简易日志系统"""
    # 1. 支持 DEBUG/INFO/WARN/ERROR 级别
    # 2. 输出到文件和控制台
    # 3. 按日期分割日志文件
    # 4. 支持日志格式配置
    # 5. 使用 JSON 格式存储
```

**练习13：缓存管理**
```python
class FileCache:
    """文件缓存"""
    # 1. cache_get(key) 获取缓存
    # 2. cache_set(key, value, ttl) 设置缓存
    # 3. cache_delete(key) 删除缓存
    # 4. cache_clear() 清空缓存
    # 5. 自动过期清理
```

**练习14：文件监控**
```python
class FileWatcher:
    """文件变化监控"""
    # 1. watch(path, callback) 监控文件
    # 2. on_modified() 修改回调
    # 3. on_created() 创建回调
    # 4. on_deleted() 删除回调
    # 5. stop() 停止监控
```

**练习15：批量文件处理**
```python
class BatchFileProcessor:
    """批量文件处理器"""
    # 1. process_all() 处理所有文件
    # 2. rename_files() 批量重命名
    # 3. copy_with_structure() 复制保持结构
    # 4. find_and_replace() 查找替换内容
    # 5. generate_manifest() 生成文件清单
```

**练习16：测试数据生成器**
```python
class TestDataGenerator:
    """测试数据生成"""
    # 1. generate_users(n) 生成用户数据
    # 2. generate_orders(n) 生成订单数据
    # 3. save_to_csv(data, path) 保存 CSV
    # 4. save_to_json(data, path) 保存 JSON
    # 5. load_template(template_path) 加载模板
```

### 综合练习（17-20）

**练习17：搭建测试项目**
```bash
# 创建完整项目结构
my_test_project/
├── config/
│   ├── settings.yaml
│   └── settings.local.yaml
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── data/
│       ├── users.csv
│       └── orders.json
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   └── http_client.py
├── reports/
├── requirements.txt
└── pytest.ini
```

**练习18：多环境配置管理**
```python
class EnvironmentConfig:
    """多环境配置"""
    # 1. 支持 dev/test/staging/prod 环境
    # 2. 根据环境变量切换配置
    # 3. 配置继承（local 覆盖 base）
    # 4. 敏感信息加密存储
    # 5. 配置验证和默认值
```

**练习19：测试数据版本管理**
```python
class DataVersionManager:
    """测试数据版本管理"""
    # 1. snapshot() 创建数据快照
    # 2. restore(version) 恢复到指定版本
    # 3. diff(v1, v2) 对比版本差异
    # 4. list_versions() 列出所有版本
    # 5. auto_cleanup() 自动清理旧版本
```

**练习20：插件化配置加载器**
```python
class ConfigLoader:
    """插件化配置加载"""
    # 1. register_loader(ext, loader) 注册加载器
    # 2. load(path) 自动选择加载器
    # 3. 支持 .yaml/.json/.toml/.ini
    # 4. 支持远程配置 (HTTP)
    # 5. 支持配置合并策略
```

## 五、检验标准

### 自测题

#### 题目1：JSON 处理
实现函数 `merge_json_files(filepaths, output)`，合并多个 JSON 文件到一个文件。

#### 题目2：CSV 处理
实现函数 `filter_csv(input_file, output_file, column, value)`，过滤 CSV 文件中指定列等于指定值的行。

#### 题目3：路径处理
实现函数 `find_files(directory, pattern)`，递归查找目录下所有匹配模式的文件。

### 答案

```python
# 题目1
import json
from pathlib import Path

def merge_json_files(filepaths, output):
    """合并多个 JSON 文件"""
    merged = []
    for filepath in filepaths:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                merged.extend(data)
            else:
                merged.append(data)

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)


# 题目2
import csv

def filter_csv(input_file, output_file, column, value):
    """过滤 CSV 文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        filtered = [row for row in reader if row.get(column) == value]

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered)


# 题目3
from pathlib import Path

def find_files(directory, pattern):
    """递归查找文件"""
    return list(Path(directory).rglob(pattern))

# 使用
find_files("tests", "*.py")  # 查找所有 Python 文件
```

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
