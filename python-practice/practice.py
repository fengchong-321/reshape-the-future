# 1. 统计字符频率
# 描述：编写函数 count_chars(s: str) -> dict，统计字符串中每个字符（包括空格、标点）出现的次数，返回字典。
# 示例：
# 输入 "hello world" → {'h':1, 'e':1, 'l':3, 'o':2, ' ':1, 'w':1, 'r':1, 'd':1}


def count_chars(s: str) -> dict:
    s_count = {}
    for ch in s:
        s_count[ch] = s_count.get(ch, 0) + 1
    return s_count

print(count_chars("hello world"))


# 2. 手动反转字符串
# 描述：编写函数 reverse_string(s: str) -> str，不使用切片 [::-1] 或内置 reversed，手动实现字符串反转。
# 示例：
# 输入 "Python" → "nohtyP"
