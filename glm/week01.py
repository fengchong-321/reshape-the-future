# numbers = [3, 1, 4, 1, 5, 9, 2, 6]
# numbers.sort()
# print(numbers)
# print("原地排序")           # 原地排序 [1, 1, 2, 3, 4, 5, 6, 9]
# numbers.sort(reverse=True)
# print(numbers)
# print("降序")    # 降序
# numbers.reverse()
# print(numbers)
# print("反转")    # 反转

# names = ["登录", "搜索"]
# priorities = ["P0", "P1"]
# for name, priority in zip(names, priorities):
#     print(f"{name}: {priority}")

# print("=" * 100)

# import itertools

# for name, priority in itertools.product(names, priorities):
#     print(f"{name}:{priority}")


# # 给定测试结果数据
# test_results = [
#     {"name": "登录测试", "status": "pass", "duration": 1.2},
#     {"name": "搜索测试", "status": "fail", "duration": 2.5},
#     {"name": "支付测试", "status": "pass", "duration": 3.1},
#     {"name": "订单测试", "status": "fail", "duration": 1.8},
#     {"name": "退出测试", "status": "pass", "duration": 0.5},
#     {"name": "注册测试", "status": "pass", "duration": 2.0},
#     {"name": "收藏测试", "status": "skip", "duration": 0.0},
# ]

# # 任务1：统计各状态的用例数量
# # 期望输出: {"pass": 4, "fail": 2, "skip": 1}
# status_count = {}
# for item in test_results:
#     status = item["status"]
#     status_count[status] = status_count.get(status, 0) + 1

# print(status_count)

# # 任务2：找出所有失败的用例名
# # 期望输出: ["搜索测试", "订单测试"]
# print([item["name"] for item in test_results if item["status"] == "fail"])

# # 任务3：计算通过用例的平均耗时
# # 期望输出: 1.7
# pass_durations = [item["duration"] for item in test_results if item["status"] == "pass"]
# avg_duration = sum(pass_durations) / len(pass_durations)
# print(avg_duration)

# # 任务4：按耗时降序排列
# # 期望输出: [{"name": "支付测试", ...}, {"name": "搜索测试", ...}, ...]
# test_results.sort(key=lambda x: x["duration"], reverse=True)
# print(test_results)


# print("=" * 100)

# # 给定配置字典
# config = {
#     "base_url": "https://api.ctrip.com",
#     "timeout": 30,
#     "retry": 3,
#     "headers": {"Content-Type": "application/json", "Authorization": "Bearer xxx"},
#     "environments": {
#         "dev": "https://dev.ctrip.com",
#         "test": "https://test.ctrip.com",
#         "prod": "https://api.ctrip.com",
#     },
# }


# # 任务1：编写函数 get_config(key, default=None)
# # 支持点号访问嵌套配置
# # get_config("headers.Content-Type") 返回 "application/json"
# # get_config("timeout") 返回 30
# # get_config("not_exist", "default") 返回 "default"
# def get_config(key: str, default=None):
#     if not isinstance(key, str) or not key:
#         return default
#     keys = key.split(".")
#     current = config
#     for k in keys:
#         if isinstance(current, dict) and k in current:
#             current = current[k]
#         else:
#             return default
#     return current


# # 任务2：编写函数 switch_env(env_name)
# # 将 base_url 切换到指定环境
# def switch_env(env_name: str):
#     new_url = get_config(f"environments.{env_name}")
#     if new_url is not None:
#         config["base_url"] = new_url


# # 测试 get_config
# print(get_config("timeout"))  # 30
# print(get_config("headers.Content-Type"))  # application/json
# print(get_config("not_exist", "default"))  # default

# # 测试 switch_env
# print(config["base_url"])  # https://api.ctrip.com
# switch_env("test")
# print(config["base_url"])  # https://test.ctrip.com
# switch_env("dev")
# print(config["base_url"])  # https://dev.ctrip.com
# switch_env("prod")
# print(config["base_url"])  # https://api.ctrip.com


# # 创建一个包含 10 个测试用例名的列表
# # 完成以下操作：
# # 1. 添加一个新用例到末尾
# # 2. 在第 3 个位置插入一个用例
# # 3. 删除第一个用例
# # 4. 获取列表长度
# # 5. 判断"登录测试"是否在列表中

# testcase = ['1','2','3','4','5','6','7','8','9','10']
# testcase.append('11')
# testcase.insert(2,'33')
# print(testcase)
# print(len(testcase))
# print('登录测试' in testcase)

# cases = ["登录", "搜索", "支付", "订单", "退款", "评价", "收藏", "分享", "注销", "退出"]
# # 1. 获取前 5 个用例
# # 2. 获取后 3 个用例
# # 3. 获取索引 2-6 的用例（不含 6）
# # 4. 每隔 2 个取一个用例
# # 5. 反转列表
# print(cases[:5])
# print(cases[-3:])
# print(cases[2:6])
# print(cases[::2])
# cases.reverse()
# print(cases)

# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# # 使用列表推导式：
# # 1. 生成所有数字的平方
# # 2. 筛选出偶数
# # 3. 筛选出大于 5 的奇数
# # 4. 将每个数字转为字符串
# # 5. 生成 (数字, 平方) 元组列表

# print([x**2 for x in numbers])
# print([x for x in numbers if x % 2 == 0])
# print([x for x in numbers if x % 2 == 1 and x > 5])
# print([str(x) for x in numbers])
# print(([(x, x**2) for x in numbers]))

# 创建用户字典，包含 username, password, age, is_vip 四个字段
# 1. 添加 email 字段
# 2. 修改 age 为 30
# 3. 安全获取 phone（不存在返回"未设置"）
# 4. 删除 is_vip 字段
# 5. 遍历打印所有键值对


# keys = ["sername", "password", "age", "is_vip"]
# values = ["", "", "", ""]
# d = dict(zip(keys, values))
# print(d)
# d["email"] = ""
# d["age"] = 30
# d.get("phone", 0)
# d.pop("is_vip")
# for key, value in d.items():
#     print(f"{key}:{value}")

# test_data = {
#     "login": {"valid": ["admin", "user"], "invalid": ["", "guest"]},
#     "search": {"keywords": ["酒店", "机票"]},
#     "order": {"status": ["pending", "paid", "cancelled"]}
# }
# # 1. 获取 login 下的 valid 用户列表
# # 2. 添加一个新的搜索关键词
# # 3. 统计 order 下有多少种状态
# # 4. 判断 search 下是否有 "火车票" 关键词
# print(test_data['login']['valid'])
# test_data['search']['keywords'].append('门票')
# print(test_data['search']['keywords'])
# print(len(test_data['order']['status']))
# print('火车票' in test_data['search']['keywords'])

# name, age, score = "张三", 28, 85.55
# # 使用 f-string 输出：
# # 1. "姓名：张三，年龄：28"
# # 2. "张三的成绩是 95.5 分"
# # 3. "明年张三 29 岁"
# # 4. "成绩等级：A"（90以上为A）
# # 5. 格式化成绩保留 1 位小数

# print(f'姓名：{name},年龄：{age}')
# print(f'{name}的成绩是{score}')
# print(f'明年{name}{age+1}岁')
# print(f'成绩等级{'为A' if score > 90 else '不为A'}')
# print(f'{score:.1f}')

# text = "  Hello, Python WOrld!  "
# # 1. 去除首尾空格
# # 2. 转为小写
# # 3. 替换 "Python" 为 "Java"
# # 4. 按 ", " 分割
# # 5. 统计 "o" 出现次数
# print(text.strip())
# print(text.lower())
# print(text.replace('Python','Java'))
# print(text)
# print(text.split(','))
# print(text.count('o'))

# 1. 使用 for 循环打印 1-10
# 2. 使用 while 循环计算 1+2+...+100
# 3. 使用 for + enumerate 打印带索引的用例名
# 4. 使用 zip 同时遍历两个列表
# 5. 使用 break 找到第一个大于 50 的数

# for i in range(1, 10):
#     print(i)
# total = 0
# i = 1
# while i <= 100:
#     total += i
#     i += 1
# print(total)
# cases = ["登录", "搜索", "支付", "订单", "退款", "评价", "收藏", "分享", "注销", "退出"]
# for index, name in enumerate(cases):
#     print(index + 1, name)

# test_results = [
#     {"name": "登录测试", "status": "pass", "duration": 1.2},
#     {"name": "搜索测试", "status": "fail", "duration": 2.5},
#     {"name": "支付测试", "status": "pass", "duration": 3.1},
#     {"name": "订单测试", "status": "fail", "duration": 1.8},
#     {"name": "退出测试", "status": "pass", "duration": 0.5},
# ]

# # 1. 统计各状态的用例数量
# # 2. 找出所有失败的用例名
# # 3. 计算通过用例的平均耗时
# # 4. 按耗时降序排列
# # 5. 找出耗时最长的用例

# status_count = {}
# for item in test_results:
#     status = item["status"]
#     status_count[status] = status_count.get(status, 0) + 1
# print(status_count)
# print([item["name"] for item in test_results if item["status"] == "fail"])
# list_duration = [item["duration"] for item in test_results if item["status"] == "pass"]
# print(list_duration)
# avg_duration = round(sum(list_duration) / len(list_duration), 1)
# print(avg_duration)
# test_results.sort(key=lambda x: x["duration"], reverse=True)
# print(test_results)
# longgest = max(test_results, key=lambda x: x["duration"])
# print(longgest)

# config = {
#     "base_url": "https://api.ctrip.com",
#     "timeout": 30,
#     "headers": {
#         "Content-Type": "application/json",
#         "Authorization": "Bearer xxx"
#     }
# }

# # 编写函数 get_config(key, default=None)
# # 支持点号访问嵌套配置
# # get_config("headers.Content-Type") → "application/json"
# # get_config("timeout") → 30
# # get_config("not_exist", "default") → "default"

# def get_config(key:str, default=None):
#     if not isinstance(key,str) or not key:
#         return default

#     keys = key.split('.')
#     current = config

#     for k in keys:
#         if isinstance(current,dict) and k in current:
#             current = current[k]
#         else:
#             return default
#     return current
# import re
# from datetime import datetime

# logs = """
# [2024-01-15 10:30:45] INFO  - 测试开始
# [2024-01-15 10:30:47] ERROR - 登录失败
# [2024-01-15 10:30:49] WARN  - 响应慢
# [2024-01-15 10:30:51] INFO  - 测试结束
# """
# # 1. 提取所有 ERROR 级别的日志
# error_lines = [line for line in logs.strip().split("\n") if "ERROR" in line]
# print(error_lines)
# # 2. 统计各级别日志数量
# levels = ["INFO", "WARN", "ERROR"]
# level_count = {level: 0 for level in levels}
# for line in logs.strip().split("\n"):
#     for level in levels:
#         if level in line:
#             level_count[level] += 1
#             break
# print(level_count)
# # 3. 使用正则提取时间戳
# timestamp_pattern = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]"
# timestamps = re.findall(timestamp_pattern, logs)
# print(timestamps)
# for s in timestamps:
#     print(s)
# # 4. 计算测试总耗时
# if timestamps:
#     start_time = datetime.strptime(timestamps[0], "%Y-%m-%d %H:%M:%S")
#     end_time = datetime.strptime(timestamps[-1], "%Y-%m-%d %H:%M:%S")
#     duration = end_time - start_time
#     print(duration)
# else:
#     print("没找到")


# 编写函数 create_test_case(name, priority="P2", *tags, **options)
# 要求：
# 1. name 是必填参数
# 2. priority 默认 "P2"
# 3. tags 接收任意数量的标签
# 4. options 接收任意关键字参数
# 调用示例：
# create_test_case("登录测试", "P0", "smoke", "regression", timeout=30, retry=3)
# def create_test_case(name, priority="P2", *tags, **options):
#     test_case = {"name": name, "priority": priority, "tags": tags, "options": options}
#     return test_case

# users = [
#     {"name": "张三", "age": 25},
#     {"name": "李四", "age": 30},
#     {"name": "王五", "age": 28},
# ]

# # 1. 转为字典：{"张三": {"name": "张三", "age": 25}, ...}
# users_dict = {user["name"]: user for user in users}
# print(users_dict)
# # 2. 提取所有用户名列表
# user_name = [user['name'] for user in users]
# print(user_name)
# # 3. 提取所有年龄列表
# user_age = [user['age'] for user in users]
# print(user_age)
# # 4. 按年龄升序排列
# users.sort(key=lambda x: x["age"])
# print(users)
# # 5. 筛选年龄大于 26 的用户
# print([user["name"] for user in users if user["age"] > 26])

# import re

# text = "订单号：12345，金额：678.90元，手机：13812345678"

# # 1. 提取订单号（纯数字）
# orderid = re.search(r"订单号：(\d{5})", text)
# print(orderid.group(1) if orderid else None)
# # 2. 提取金额（浮点数）
# orderamount = re.search(r"金额：(\d+(?:\.\d+)?)元", text)
# print(orderamount.group(1) if orderamount else None)
# # 3. 提取手机号（11位数字）
# phone = re.search(r"(1[3-9]\d{9})", text)
# print(phone.group(1) if phone else None)
# # 4. 验证邮箱格式
# re.search(r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", text)
# # 5. 将所有数字替换为 ***
# new_text = re.sub(r"\d+(?:\.\d+)?", "***", text)
# print(new_text)


# cases = [
#     {"name": "登录", "status": "pass", "time": 1.2},
#     {"name": "搜索", "status": "fail", "time": 2.5},
#     {"name": "支付", "status": "pass", "time": 3.0},
# ]

# 编写函数 generate_report(cases) 返回：
# {
#     "total": 3,
#     "passed": 2,
#     "failed": 1,
#     "pass_rate": "66.67%",
#     "avg_time": 2.23,
#     "failed_cases": ["搜索"]
# }


# def generate_report(cases):
#     total = len(cases)
#     passed = sum(1 for case in cases if case["status"] == "pass")
#     failed = sum(1 for case in cases if case["status"] == "failed")
#     # 避免除以0，加上if-else
#     pass_rate = f"{passed / total:.2%}" if total > 0 else "0.00%"
#     avg_time = (
#         round(sum(case["time"] for case in cases) / total, 2) if total > 0 else 0.0
#     )
#     failed_cases = [case["name"] for case in cases if case["status"] == "fail"]
#     return {
#         "total": total,
#         "passed": passed,
#         "failed": failed,
#         "pass_rate": pass_rate,
#         "avg_time": avg_time,
#         "failed_cases": failed_cases,
#     }
# print(generate_report(cases))

# list1 = [1, 2, 3, 4, 5]
# list2 = [4, 5, 6, 7, 8]

# # 1. 找出两个列表的交集
# print([x for x in list1 if x in list2])
# # 2. 找出两个列表的并集
# print(list1 + [x for x in list2 if x not in list1])
# # 3. 找出只在 list1 中的元素
# print([x for x in list1 if x not in list2])
# # 4. 合并两个列表并去重
# print(list1 + [x for x in list2 if x not in list1])
# # 5. 找出两个列表中重复的元素
# print([x for x in list1 if x in list2])

# 编写函数 execute_tests(test_cases)
# test_cases 是用例列表，每个用例包含 name 和 steps
# 模拟执行每个步骤，随机返回 pass/fail
# 返回执行结果列表，包含用例名、状态、耗时


# test_cases = [
#     {"name": "登录", "steps": ["打开页面", "输入用户名", "输入密码", "点击登录"]},
#     {"name": "搜索", "steps": ["输入关键词", "点击搜索", "验证结果"]},
# ]
# import random
# import time
# def execute_tests(test_cases):
#     result = ['pass','fail']
#     cases_result = []
#     for case in test_cases:
#         start_time = time.time()
#         for step in case['steps']:
#             print(step)
#         end_time = time.time()
#         case_dict = {
#             'name':case['name'],
#             'status':random.choice(result),
#             'duration':f'{end_time-start_time:.6f}'
#         }
#         cases_result.append(case_dict)
#     return cases_result

# print(execute_tests(test_cases))

# 编写 ConfigManager 类（用字典模拟）
# 实现以下方法：
# 1. load(config_dict) - 加载配置
# 2. get(key, default=None) - 获取配置（支持点号访问嵌套）
# 3. set(key, value) - 设置配置
# 4. get_env(env_name) - 获取环境配置
# 5. to_dict() - 导出为字典


# class ConfigManager:
#     def __init__(self):
#         self.config = {}

#     def load(self, config_dict):
#         if isinstance(config_dict, dict):
#             self.config = config_dict
#         else:
#             raise TypeError("config_dict must be a dict")

#     def get(self, key, default=None):
#         if not isinstance(key, str) or not key:
#             return default
#         keys = key.split(".")
#         current = self.config

#         for k in keys:
#             if isinstance(current, dict) and k in current:
#                 current = current[k]
#             else:
#                 return default
#         return current

#     def set(self, key, value):
#         if not isinstance(key, str) or not key:
#             raise ValueError("key must be a non-empty string")

#         keys = key.split(".")
#         current = self.config

#         for k in keys[:-1]:
#             if k not in current:
#                 current[k] = {}
#             elif not isinstance(current, dict):
#                 current[k] = {}
#             current = current[k]
#         current[keys[-1]] = value

#     def get_env(self, env_name):
#         envs = self.get("environments", {})
#         return envs.get(env_name, {})

#     def to_dict(self):
#         return self.config.copy()


# if __name__ == "__main__":
#     cm = ConfigManager()

#     config = {
#         "base_url": "https://api.ctrip.com",
#         "timeout": 30,
#         "retry": 3,
#         "headers": {"Content-Type": "application/json", "Authorization": "Bearer xxx"},
#         "environments": {
#             "dev": "https://dev.ctrip.com",
#             "test": "https://test.ctrip.com",
#             "prod": "https://api.ctrip.com",
#         },
#     }

#     cm.load(config)

#     print(cm.get("base_url"))
#     print(cm.get("headers.Content-Type"))
#     print(cm.get("no_exist", "default"))

#     cm.set("headers.Authorization", "Bearer token")
#     print(cm.get("headers.Authorization"))

#     cm.set("database.host", "localhost")
#     cm.set("database.port", 5432)
#     print(cm.get("database"))

#     print(cm.get_env("dev"))
#     print(cm.get_env("staging"))

#     print(cm.to_dict())


# 编写函数生成测试数据
# 1. generate_users(n) - 生成 n 个随机用户数据
# 2. generate_phone() - 生成随机手机号
# 3. generate_email(name) - 根据名字生成邮箱
# 4. generate_test_cases(module, count) - 生成测试用例数据
# 5. save_to_json(data, filename) - 保存为 JSON 文件
# import random

# def generate_users(n):
#     users= []
#     for i in range(n):
#         user = {
#             "name":f"xxx{n}"
#         }
#         users.append(user)
#     return users

# def generate_phone():
#     return f'13{random.randint(100000000,999999999)}'

# def generate_email(name):
#     return f'{name}@gmail.com'

# 编写简易断言函数
# 1. assert_equal(actual, expected, msg="")
# 2. assert_not_equal(actual, expected, msg="")
# 3. assert_in(item, container, msg="")
# 4. assert_true(condition, msg="")
# 5. assert_raises(func, exception_type, msg="")

# 要求：断言失败时抛出 AssertionError，包含错误信息和期望值


# def assert_equal(actual, expected, msg=""):
#     if actual != expected:
#         error_msg = f"{msg}" if msg else ""
#         error_msg += f"Assertion failed: expected {expected}, got {actual}"
#         raise AssertionError(error_msg)


# def assert_not_equal(actual, expected, msg=""):
#     if actual == expected:
#         error_msg = f"{msg}" if msg else ""
#         error_msg += f"Assertion failed: expected {expected}, got {actual}"
#         raise AssertionError(error_msg)


# def assert_in(item, container, msg=""):
#     if item not in container:
#         error_msg = f"{msg}" if msg else ""
#         error_msg += f"Assertion failed: {container} not contain {item}"
#         raise AssertionError(error_msg)


# def assert_true(condition, msg=""):
#     if not condition:
#         error_msg = f"{msg}" if msg else ""
#         error_msg += f"Assertion failed: {condition} not true"
#         raise AssertionError(error_msg)


# # assert_equal(1, 1)

# # try:
# #     assert_equal(2, 1, "值不匹配")
# # except AssertionError as e:
# #     print(e)

# try:
#     assert_in(4, [1, 2, 3])
# except AssertionError as e:
#     print(e)

# # 有两个列表，找出同时存在于两个列表中的元素
# list1 = [1, 2, 3, 4, 5]
# list2 = [4, 5, 6, 7, 8]
# # 期望输出: [4, 5]
# print([i for i in list1 if i in list2])

# # 将以下列表转换为字典，key 是 name，value 是整个对象
# users = [
#     {"name": "张三", "age": 25},
#     {"name": "李四", "age": 30},
# ]
# # 期望输出: {"张三": {"name": "张三", "age": 25}, "李四": {"name": "李四", "age": 30}}

# print({user["name"]: user for user in users})

# # 编写函数 validate_email(email)
# # 验证邮箱格式，返回 True/False
# # 要求：包含@符号，@前后都有内容，域名包含点号
# def validate_email(email: str):
#     if email.count("@") != 1:
#         return False

#     local, domain = email.split("@")

#     if not local:
#         return False

#     if "." not in domain:
#         return False

#     if domain.startswith(".") or domain.endswith("."):
#         return False
#     return True


# print(validate_email("test@example.com"))  # True
# print(validate_email("invalid"))  # False
# print(validate_email("@example.com"))  # False

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
    total = len(cases)
    passed = sum([1 for case in cases if case["status"] == "pass"])
    failed = sum([1 for case in cases if case["status"] == "fail"])
    pass_rate = f"{passed / total:.2%}"
    avg_time = round(sum([case["time"] for case in cases]) / total, 2)
    failed_cases = [case["name"] for case in cases if case["status"] == "fail"]

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "avg_time": avg_time,
        "failed_cases": failed_cases,
    }


if __name__ == "__main__":
    print(generate_report(cases))
