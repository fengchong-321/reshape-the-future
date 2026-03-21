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

logs = """
[2024-01-15 10:30:45] INFO  - 测试开始
[2024-01-15 10:30:47] ERROR - 登录失败
[2024-01-15 10:30:49] WARN  - 响应慢
[2024-01-15 10:30:51] INFO  - 测试结束
"""
import re
from sqlite3 import TimestampFromTicks

# 1. 提取所有 ERROR 级别的日志
error_lines = [line for line in logs.strip().split("\n") if "ERROR" in line]
print(error_lines)
# 2. 统计各级别日志数量
levels = ["INFO", "WARN", "ERROR"]
level_count = {level: 0 for level in levels}
for line in logs.strip().split("\n"):
    for level in levels:
        if level in line:
            level_count[level] += 1
            break
print(level_count)
# 3. 使用正则提取时间戳
timestamp_pattern = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]"
timestamps = re.findall(timestamp_pattern, logs)
print(timestamps)
for s in timestamps:
    print(s)
# 4. 计算测试总耗时
from datetime import datetime

if timestamps:
    start_time = datetime.strptime(timestamps[0], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(timestamps[-1], "%Y-%m-%d %H:%M:%S")
    duration = end_time - start_time
    print(duration)
else:
    print('没找到')
