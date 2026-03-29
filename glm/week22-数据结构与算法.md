# 第22周：数据结构与算法

## 本周目标

掌握面试中最常见的数据结构和算法，能解决 LeetCode 简单/中等难度题目。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| 数组与字符串 | 双指针、滑动窗口 | ⭐⭐⭐⭐⭐ |
| 链表 | 单链表、快慢指针 | ⭐⭐⭐⭐⭐ |
| 哈希表 | HashMap、HashSet | ⭐⭐⭐⭐⭐ |
| 栈与队列 | 单调栈、优先队列 | ⭐⭐⭐⭐ |
| 二叉树 | 遍历、常见问题 | ⭐⭐⭐⭐⭐ |
| 排序算法 | 快排、归并、堆排 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 数组与字符串

```python
# ============================================
# 双指针技巧
# ============================================

# 1. 两数之和（有序数组）
def two_sum(numbers, target):
    """LeetCode 167 - 有序数组的两数之和"""
    left, right = 0, len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return [-1, -1]

# 2. 三数之和
def three_sum(nums):
    """LeetCode 15 - 三数之和为0"""
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # 跳过重复

        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result

# ============================================
# 滑动窗口
# ============================================

# 1. 最长子串（无重复字符）
def length_of_longest_substring(s):
    """LeetCode 3 - 无重复字符的最长子串"""
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)

    return max_length

# 2. 最小覆盖子串
def min_window(s, t):
    """LeetCode 76 - 最小覆盖子串"""
    from collections import Counter

    if not s or not t:
        return ""

    # 统计 t 中字符频率
    t_count = Counter(t)
    required = len(t_count)

    # 滑动窗口
    left = 0
    formed = 0
    window_count = {}
    ans = (float('inf'), 0, 0)  # (length, left, right)

    for right in range(len(s)):
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1

        if char in t_count and window_count[char] == t_count[char]:
            formed += 1

        while left <= right and formed == required:
            char = s[left]

            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)

            window_count[char] -= 1
            if char in t_count and window_count[char] < t_count[char]:
                formed -= 1

            left += 1

    return "" if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]
```

---

### 2.2 链表

```python
# ============================================
# 链表定义
# ============================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# ============================================
# 常见链表问题
# ============================================

# 1. 反转链表
def reverse_list(head):
    """LeetCode 206 - 反转链表"""
    prev = None
    current = head

    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp

    return prev

# 2. 检测环形链表
def has_cycle(head):
    """LeetCode 141 - 环形链表"""
    if not head or not head.next:
        return False

    slow = head
    fast = head.next

    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next

    return True

# 3. 找到环的入口
def detect_cycle(head):
    """LeetCode 142 - 环形链表 II"""
    if not head:
        return None

    # 第一阶段：检测是否有环
    slow = fast = head
    has_cycle = False

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            has_cycle = True
            break

    if not has_cycle:
        return None

    # 第二阶段：找入口
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow

# 4. 合并两个有序链表
def merge_two_lists(l1, l2):
    """LeetCode 21 - 合并两个有序链表"""
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2

    return dummy.next

# 5. 删除链表倒数第 N 个节点
def remove_nth_from_end(head, n):
    """LeetCode 19 - 删除链表的倒数第N个节点"""
    dummy = ListNode(0)
    dummy.next = head

    fast = slow = dummy

    # fast 先走 n 步
    for _ in range(n + 1):
        fast = fast.next

    # 同时移动
    while fast:
        fast = fast.next
        slow = slow.next

    # 删除节点
    slow.next = slow.next.next

    return dummy.next

# 6. 链表的中间节点
def middle_node(head):
    """LeetCode 876 - 链表的中间结点"""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

---

### 2.3 哈希表

```python
# ============================================
# 哈希表应用
# ============================================

# 1. 两数之和（无序）
def two_sum(nums, target):
    """LeetCode 1 - 两数之和"""
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []

# 2. 字母异位词分组
def group_anagrams(strs):
    """LeetCode 49 - 字母异位词分组"""
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # 排序后的字符串作为 key
        key = ''.join(sorted(s))
        groups[key].append(s)

    return list(groups.values())

# 3. 最长连续序列
def longest_consecutive(nums):
    """LeetCode 128 - 最长连续序列"""
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # 只从序列起点开始
        if num - 1 not in num_set:
            current_num = num
            current_length = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            max_length = max(max_length, current_length)

    return max_length

# 4. LRU 缓存
class LRUCache:
    """LeetCode 146 - LRU 缓存"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = []  # 简化实现，实际用双向链表

    def get(self, key):
        if key in self.cache:
            # 移到最前面
            self.order.remove(key)
            self.order.insert(0, key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # 删除最久未使用
            old_key = self.order.pop()
            del self.cache[old_key]

        self.cache[key] = value
        self.order.insert(0, key)
```

---

### 2.4 栈与队列

```python
# ============================================
# 栈的应用
# ============================================

# 1. 有效的括号
def is_valid(s):
    """LeetCode 20 - 有效的括号"""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)

    return not stack

# 2. 最小栈
class MinStack:
    """LeetCode 155 - 最小栈"""
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]

# 3. 每日温度（单调栈）
def daily_temperatures(temperatures):
    """LeetCode 739 - 每日温度"""
    n = len(temperatures)
    result = [0] * n
    stack = []  # 存索引

    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_index = stack.pop()
            result[prev_index] = i - prev_index
        stack.append(i)

    return result

# ============================================
# 队列的应用
# ============================================

# 1. 用队列实现栈
class MyStack:
    """LeetCode 225 - 用队列实现栈"""
    def __init__(self):
        from collections import deque
        self.queue = deque()

    def push(self, x):
        self.queue.append(x)
        # 将前面的元素移到后面
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self):
        return self.queue.popleft()

    def top(self):
        return self.queue[0]

    def empty(self):
        return len(self.queue) == 0
```

---

### 2.5 二叉树

```python
# ============================================
# 二叉树定义
# ============================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ============================================
# 遍历
# ============================================

# 1. 前序遍历（递归）
def preorder_traversal(root):
    result = []

    def dfs(node):
        if not node:
            return
        result.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result

# 2. 前序遍历（迭代）
def preorder_iterative(root):
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result

# 3. 中序遍历
def inorder_traversal(root):
    result = []
    stack = []
    current = root

    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right

    return result

# 4. 层序遍历
def level_order(root):
    """LeetCode 102 - 二叉树的层序遍历"""
    from collections import deque

    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)

    return result

# ============================================
# 常见问题
# ============================================

# 1. 最大深度
def max_depth(root):
    """LeetCode 104 - 二叉树的最大深度"""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# 2. 翻转二叉树
def invert_tree(root):
    """LeetCode 226 - 翻转二叉树"""
    if not root:
        return None

    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)

    return root

# 3. 对称二叉树
def is_symmetric(root):
    """LeetCode 101 - 对称二叉树"""
    def is_mirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return (left.val == right.val and
                is_mirror(left.left, right.right) and
                is_mirror(left.right, right.left))

    return is_mirror(root, root)

# 4. 路径总和
def has_path_sum(root, target_sum):
    """LeetCode 112 - 路径总和"""
    if not root:
        return False

    if not root.left and not root.right:
        return root.val == target_sum

    return (has_path_sum(root.left, target_sum - root.val) or
            has_path_sum(root.right, target_sum - root.val))

# 5. 最近公共祖先
def lowest_common_ancestor(root, p, q):
    """LeetCode 236 - 二叉树的最近公共祖先"""
    if not root or root == p or root == q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root
    return left or right
```

---

### 2.6 排序算法

```python
# ============================================
# 常见排序算法
# ============================================

# 1. 快速排序
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

# 2. 归并排序
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 3. 堆排序
def heap_sort(arr):
    import heapq
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]

# ============================================
# 排序算法复杂度
# ============================================
"""
算法      平均      最坏      最好      空间      稳定
快速排序  O(nlogn) O(n²)    O(nlogn) O(logn)  不稳定
归并排序  O(nlogn) O(nlogn) O(nlogn) O(n)     稳定
堆排序    O(nlogn) O(nlogn) O(nlogn) O(1)     不稳定
冒泡排序  O(n²)    O(n²)    O(n)     O(1)     稳定
插入排序  O(n²)    O(n²)    O(n)     O(1)     稳定
选择排序  O(n²)    O(n²)    O(n²)    O(1)     不稳定
"""
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 双指针、滑动窗口
- [ ] 链表常见操作
- [ ] 哈希表应用
- [ ] 栈和队列
- [ ] 二叉树遍历
- [ ] 排序算法复杂度

### 练习目标

- [ ] 完成 50+ LeetCode 题目
- [ ] 简单题 30 分钟内
- [ ] 中等题 45 分钟内

---

## 四、练习内容

### 基础练习（1-8）

---

**练习1：两数之和（LeetCode 1）**

**场景说明**：两数之和是面试中最常见的题目之一，考察哈希表的使用和空间换时间的思想。

**具体需求**：
1. 给定一个整数数组 nums 和一个目标值 target
2. 在数组中找出和为目标值的那两个整数
3. 返回它们的数组下标
4. 要求时间复杂度低于 O(n^2)

**使用示例**：
```python
def two_sum(nums, target):
    """
    两数之和

    示例：
    输入：nums = [2, 7, 11, 15], target = 9
    输出：[0, 1]
    解释：nums[0] + nums[1] = 2 + 7 = 9
    """
    seen = {}  # 值 -> 索引

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []

# 测试
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]
```

**验收标准**：
- [ ] 能正确实现算法
- [ ] 时间复杂度为 O(n)
- [ ] 能处理找不到解的情况
- [ ] 能解释哈希表优化的原理

---

**练习2：反转链表（LeetCode 206）**

**场景说明**：链表反转是链表操作的基础，考察对指针操作的理解。

**具体需求**：
1. 给定单链表的头节点 head
2. 反转链表并返回反转后的链表头节点
3. 分别使用迭代和递归两种方式实现

**使用示例**：
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    """
    反转链表（迭代法）

    输入：1 -> 2 -> 3 -> 4 -> 5
    输出：5 -> 4 -> 3 -> 2 -> 1
    """
    prev = None
    current = head

    while current:
        next_temp = current.next  # 保存下一个节点
        current.next = prev       # 反转指针
        prev = current            # 移动 prev
        current = next_temp       # 移动 current

    return prev

def reverse_list_recursive(head):
    """反转链表（递归法）"""
    if not head or not head.next:
        return head

    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None

    return new_head

# 辅助函数：创建链表
def create_list(values):
    dummy = ListNode()
    current = dummy
    for val in values:
        current.next = ListNode(val)
        current = current.next
    return dummy.next

# 辅助函数：打印链表
def print_list(head):
    values = []
    while head:
        values.append(str(head.val))
        head = head.next
    print(" -> ".join(values))

# 测试
head = create_list([1, 2, 3, 4, 5])
print("原链表：", end="")
print_list(head)

reversed_head = reverse_list(head)
print("反转后：", end="")
print_list(reversed_head)  # 5 -> 4 -> 3 -> 2 -> 1
```

**验收标准**：
- [ ] 能正确实现迭代版本
- [ ] 能正确实现递归版本
- [ ] 能画图解释指针变化过程
- [ ] 能分析时间复杂度 O(n) 和空间复杂度

---

**练习3：有效的括号（LeetCode 20）**

**场景说明**：括号匹配是栈的典型应用，考察对栈数据结构的理解。

**具体需求**：
1. 给定一个只包括括号字符的字符串
2. 判断字符串是否有效（括号是否正确匹配和闭合）
3. 使用栈数据结构实现

**使用示例**：
```python
def is_valid(s):
    """
    有效的括号

    示例：
    输入：s = "()[]{}"
    输出：True
    输入：s = "([)]"
    输出：False
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:  # 右括号
            if not stack or stack.pop() != mapping[char]:
                return False
        else:  # 左括号
            stack.append(char)

    return not stack  # 栈为空才有效

# 测试
print(is_valid("()"))       # True
print(is_valid("()[]{}"))   # True
print(is_valid("(]"))       # False
print(is_valid("([)]"))     # False
print(is_valid("{[]}"))     # True
```

**验收标准**：
- [ ] 能正确实现算法
- [ ] 能解释栈的使用原理
- [ ] 能处理边界情况（空字符串、奇数长度）
- [ ] 时间复杂度 O(n)

---

**练习4：无重复字符的最长子串（LeetCode 3）**

**场景说明**：滑动窗口是解决子串/子数组问题的常用技巧，本题是经典的滑动窗口应用。

**具体需求**：
1. 给定一个字符串 s
2. 找出其中不含有重复字符的最长子串的长度
3. 使用滑动窗口算法实现

**使用示例**：
```python
def length_of_longest_substring(s):
    """
    无重复字符的最长子串

    示例：
    输入：s = "abcabcbb"
    输出：3（"abc"）
    """
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        # 当遇到重复字符时，收缩左边界
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)

    return max_length

# 测试
print(length_of_longest_substring("abcabcbb"))  # 3
print(length_of_longest_substring("bbbbb"))     # 1
print(length_of_longest_substring("pwwkew"))    # 3
```

**验收标准**：
- [ ] 能正确实现滑动窗口算法
- [ ] 能解释窗口收缩的时机
- [ ] 时间复杂度 O(n)
- [ ] 能优化为使用字典记录位置

---

**练习5：二叉树的最大深度（LeetCode 104）**

**场景说明**：二叉树的深度计算是树的基础操作，考察递归思维和 BFS 遍历。

**具体需求**：
1. 给定二叉树的根节点
2. 计算二叉树的最大深度
3. 分别使用递归（DFS）和迭代（BFS）两种方式实现

**使用示例**：
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root):
    """
    二叉树的最大深度（递归/DFS）

    示例：
        3
       / \
      9  20
        /  \
       15   7
    输出：3
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def max_depth_bfs(root):
    """二叉树的最大深度（迭代/BFS）"""
    from collections import deque

    if not root:
        return 0

    queue = deque([root])
    depth = 0

    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return depth

# 测试
# 构建树
#       3
#      / \
#     9  20
#       /  \
#      15   7
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

print(max_depth(root))     # 3
print(max_depth_bfs(root)) # 3
```

**验收标准**：
- [ ] 能正确实现递归版本
- [ ] 能正确实现迭代版本
- [ ] 能解释递归的终止条件
- [ ] 能分析时间复杂度 O(n)

---

**练习6：合并两个有序链表（LeetCode 21）**

**场景说明**：合并有序链表是链表操作的经典题目，考察指针操作和递归思维。

**具体需求**：
1. 将两个升序链表合并为一个新的升序链表
2. 分别使用迭代和递归两种方式实现
3. 返回合并后的链表头节点

**使用示例**：
```python
def merge_two_lists(l1, l2):
    """
    合并两个有序链表（迭代法）

    输入：1 -> 2 -> 4, 1 -> 3 -> 4
    输出：1 -> 1 -> 2 -> 3 -> 4 -> 4
    """
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # 连接剩余部分
    current.next = l1 if l1 else l2

    return dummy.next

def merge_two_lists_recursive(l1, l2):
    """合并两个有序链表（递归法）"""
    if not l1:
        return l2
    if not l2:
        return l1

    if l1.val <= l2.val:
        l1.next = merge_two_lists_recursive(l1.next, l2)
        return l1
    else:
        l2.next = merge_two_lists_recursive(l1, l2.next)
        return l2
```

**验收标准**：
- [ ] 能正确实现迭代版本
- [ ] 能正确实现递归版本
- [ ] 能使用哑节点简化代码
- [ ] 时间复杂度 O(n+m)

---

**练习7：环形链表（LeetCode 141）**

**场景说明**：环形链表检测是快慢指针的经典应用，考察对双指针技巧的理解。

**具体需求**：
1. 给定链表头节点
2. 判断链表中是否有环
3. 使用快慢指针实现，空间复杂度 O(1)

**使用示例**：
```python
def has_cycle(head):
    """
    环形链表检测（快慢指针）

    原理：如果有环，快指针最终会追上慢指针
    """
    if not head or not head.next:
        return False

    slow = head
    fast = head.next

    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next

    return True

# 测试
# 创建有环链表：1 -> 2 -> 3 -> 4 -> 2（环）
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = head.next  # 形成环

print(has_cycle(head))  # True
```

**验收标准**：
- [ ] 能正确实现快慢指针
- [ ] 能解释为什么快慢指针能检测环
- [ ] 空间复杂度 O(1)
- [ ] 能计算环的起点（进阶）

---

**练习8：三数之和（LeetCode 15）**

**场景说明**：三数之和是双指针技巧的典型应用，考察排序后使用双指针优化查找。

**具体需求**：
1. 找出数组中和为 0 的三元组
2. 结果中不能有重复的三元组
3. 使用双指针优化到 O(n^2)

**使用示例**：
```python
def three_sum(nums):
    """
    三数之和

    示例：
    输入：nums = [-1, 0, 1, 2, -1, -4]
    输出：[[-1, -1, 2], [-1, 0, 1]]
    """
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        # 跳过重复元素
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # 跳过重复元素
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result

# 测试
print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0, 0]))           # [[0, 0, 0]]
```

**验收标准**：
- [ ] 能正确实现双指针算法
- [ ] 能正确处理重复元素
- [ ] 时间复杂度 O(n^2)
- [ ] 能解释排序的作用

---

### 进阶练习（9-16）

---

**练习9：LRU 缓存机制（LeetCode 146）**

**场景说明**：LRU 是常用的缓存淘汰策略，本题综合考察哈希表和双向链表的使用。

**具体需求**：
1. 实现 LRUCache 类，支持 get 和 put 操作
2. get(key)：存在则返回值并移到最前，不存在返回 -1
3. put(key, value)：存在则更新，不存在则插入
4. 容量满时删除最久未使用的元素
5. get 和 put 时间复杂度要求 O(1)

**使用示例**：
```python
class LRUCache:
    """
    LRU 缓存机制

    使用哈希表 + 双向链表实现 O(1) 操作
    """

    class Node:
        def __init__(self, key=0, value=0):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node

        # 使用伪头尾节点简化边界处理
        self.head = self.Node()
        self.tail = self.Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node):
        """将节点添加到头部"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        """移除节点"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node):
        """将节点移到头部"""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self):
        """移除尾部节点"""
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = self.Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

            if len(self.cache) > self.capacity:
                tail = self._remove_tail()
                del self.cache[tail.key]

# 测试
lru = LRUCache(2)
lru.put(1, 1)
lru.put(2, 2)
print(lru.get(1))  # 1
lru.put(3, 3)      # 淘汰 key=2
print(lru.get(2))  # -1
```

**验收标准**：
- [ ] 能正确实现双向链表操作
- [ ] get 和 put 时间复杂度 O(1)
- [ ] 能处理容量满时的淘汰
- [ ] 能使用伪节点简化边界处理

---

**练习10：二叉树的最近公共祖先（LeetCode 236）**

**场景说明**：最近公共祖先是二叉树的重要操作，考察递归思维。

**具体需求**：
1. 给定二叉树和两个节点 p、q
2. 找到 p 和 q 的最近公共祖先
3. 使用递归实现

**使用示例**：
```python
def lowest_common_ancestor(root, p, q):
    """
    二叉树的最近公共祖先

    示例：
        3
       / \
      5   1
     / \ / \
    6  2 0  8
      / \
     7   4
    p = 5, q = 1，输出：3
    """
    # 终止条件
    if not root or root == p or root == q:
        return root

    # 在左右子树中查找
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    # 如果左右都找到，当前节点就是 LCA
    if left and right:
        return root

    # 返回找到的那一边
    return left if left else right
```

**验收标准**：
- [ ] 能正确实现递归算法
- [ ] 能解释递归的逻辑
- [ ] 时间复杂度 O(n)
- [ ] 能处理各种边界情况

---

**练习11：最长连续序列（LeetCode 128）**

**场景说明**：本题考察哈希表的使用，要求 O(n) 时间复杂度。

**具体需求**：
1. 找出数组中数字连续的最长序列长度
2. 时间复杂度要求 O(n)
3. 使用哈希集合实现

**使用示例**：
```python
def longest_consecutive(nums):
    """
    最长连续序列

    示例：
    输入：nums = [100, 4, 200, 1, 3, 2]
    输出：4（最长连续序列是 [1, 2, 3, 4]）
    """
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # 只从序列的起点开始（优化关键）
        if num - 1 not in num_set:
            current_num = num
            current_length = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            max_length = max(max_length, current_length)

    return max_length

# 测试
print(longest_consecutive([100, 4, 200, 1, 3, 2]))  # 4
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # 9
```

**验收标准**：
- [ ] 能正确实现算法
- [ ] 时间复杂度 O(n)
- [ ] 能解释为什么只从起点开始
- [ ] 能处理空数组的情况

---

**练习12：字母异位词分组（LeetCode 49）**

**场景说明**：本题考察哈希表的使用和字符串处理技巧。

**具体需求**：
1. 将字母异位词（字母相同但顺序不同）分组
2. 使用哈希表实现
3. 考虑不同的 key 生成方式

**使用示例**：
```python
def group_anagrams(strs):
    """
    字母异位词分组

    示例：
    输入：strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    输出：[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    """
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # 方法1：排序后的字符串作为 key
        key = ''.join(sorted(s))
        groups[key].append(s)

    return list(groups.values())

def group_anagrams_count(strs):
    """使用字符计数作为 key"""
    from collections import defaultdict

    groups = defaultdict(list)

    for s in strs:
        # 方法2：字符计数作为 key
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)
        groups[key].append(s)

    return list(groups.values())

# 测试
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
```

**验收标准**：
- [ ] 能正确实现排序方法
- [ ] 能实现字符计数方法
- [ ] 能比较两种方法的优劣
- [ ] 时间复杂度分析正确

---

**练习13：每日温度（LeetCode 739）**

**场景说明**：单调栈是解决"下一个更大元素"类问题的经典方法。

**具体需求**：
1. 给定每日温度数组
2. 返回数组，表示多少天后会有更高温度
3. 使用单调栈实现

**使用示例**：
```python
def daily_temperatures(temperatures):
    """
    每日温度（单调栈）

    示例：
    输入：temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
    输出：[1, 1, 4, 2, 1, 1, 0, 0]
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # 存储索引，单调递减栈

    for i in range(n):
        # 当前温度比栈顶高，弹出并计算
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_index = stack.pop()
            result[prev_index] = i - prev_index
        stack.append(i)

    return result

# 测试
print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))
# [1, 1, 4, 2, 1, 1, 0, 0]
```

**验收标准**：
- [ ] 能正确实现单调栈
- [ ] 能解释单调栈的原理
- [ ] 时间复杂度 O(n)
- [ ] 能解决类似的"下一个更大元素"问题

---

**练习14：删除链表的倒数第 N 个节点（LeetCode 19）**

**场景说明**：快慢指针是处理链表倒数问题的常用技巧。

**具体需求**：
1. 删除链表的倒数第 n 个节点
2. 使用快慢指针实现一次遍历
3. 处理边界情况（删除头节点）

**使用示例**：
```python
def remove_nth_from_end(head, n):
    """
    删除链表的倒数第 N 个节点

    示例：
    输入：head = [1, 2, 3, 4, 5], n = 2
    输出：[1, 2, 3, 5]
    """
    dummy = ListNode(0)
    dummy.next = head

    fast = slow = dummy

    # 快指针先走 n+1 步
    for _ in range(n + 1):
        fast = fast.next

    # 同时移动
    while fast:
        fast = fast.next
        slow = slow.next

    # 删除节点
    slow.next = slow.next.next

    return dummy.next
```

**验收标准**：
- [ ] 能正确实现快慢指针
- [ ] 能处理删除头节点的情况
- [ ] 时间复杂度 O(n)
- [ ] 能解释为什么用哑节点

---

**练习15：快速排序实现**

**场景说明**：快速排序是最重要的排序算法之一，面试经常要求手写实现。

**具体需求**：
1. 实现快速排序算法
2. 分析时间复杂度和空间复杂度
3. 实现原地排序版本

**使用示例**：
```python
def quick_sort(arr):
    """
    快速排序（简单版本）

    示例：
    输入：[3, 6, 8, 10, 1, 2, 1]
    输出：[1, 1, 2, 3, 6, 8, 10]
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

def quick_sort_inplace(arr, low=0, high=None):
    """快速排序（原地版本）"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        # 分区
        pivot_index = partition(arr, low, high)
        # 递归排序
        quick_sort_inplace(arr, low, pivot_index - 1)
        quick_sort_inplace(arr, pivot_index + 1, high)

    return arr

def partition(arr, low, high):
    """分区函数"""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# 测试
print(quick_sort([3, 6, 8, 10, 1, 2, 1]))
# [1, 1, 2, 3, 6, 8, 10]

arr = [3, 6, 8, 10, 1, 2, 1]
quick_sort_inplace(arr)
print(arr)  # [1, 1, 2, 3, 6, 8, 10]
```

**验收标准**：
- [ ] 能正确实现快速排序
- [ ] 能实现原地排序版本
- [ ] 能分析时间复杂度（平均 O(nlogn)，最坏 O(n^2)）
- [ ] 能说明优化方法（随机选 pivot、三数取中）

---

**练习16：二叉树的层序遍历（LeetCode 102）**

**场景说明**：层序遍历是 BFS 的典型应用，考察队列的使用。

**具体需求**：
1. 返回二叉树的层序遍历结果
2. 每层节点值放在一个列表中
3. 使用 BFS 实现

**使用示例**：
```python
def level_order(root):
    """
    二叉树的层序遍历

    示例：
        3
       / \
      9  20
        /  \
       15   7
    输出：[[3], [9, 20], [15, 7]]
    """
    from collections import deque

    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)

    return result
```

**验收标准**：
- [ ] 能正确实现 BFS 层序遍历
- [ ] 能正确分层输出
- [ ] 时间复杂度 O(n)
- [ ] 能实现 DFS 递归版本

---

### 综合练习（17-20）

---

**练习17：实现一个最小栈（LeetCode 155）**

**场景说明**：最小栈考察如何在 O(1) 时间内获取最小值，是栈的扩展应用。

**具体需求**：
1. 实现支持 push、pop、top 操作的栈
2. 在常数时间内获取栈中最小元素
3. 使用辅助栈实现

**使用示例**：
```python
class MinStack:
    """
    最小栈

    使用辅助栈存储每个位置的最小值
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # 辅助栈存储当前最小值
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

# 测试
minStack = MinStack()
minStack.push(-2)
minStack.push(0)
minStack.push(-3)
print(minStack.getMin())  # -3
minStack.pop()
print(minStack.top())     # 0
print(minStack.getMin())  # -2
```

**验收标准**：
- [ ] 所有操作时间复杂度 O(1)
- [ ] 能正确维护最小值
- [ ] 能处理空栈情况
- [ ] 能解释辅助栈的原理

---

**练习18：设计一个支持增删改查的数据结构**

**场景说明**：设计一个支持 O(1) 插入、删除、随机访问的数据结构，综合考察哈希表和数组。

**具体需求**：
1. insert(val)：元素不存在时插入，O(1)
2. remove(val)：元素存在时删除，O(1)
3. getRandom：随机返回一个元素，O(1)

**使用示例**：
```python
import random

class RandomizedSet:
    """
    支持随机访问的集合

    使用数组 + 哈希表实现
    """

    def __init__(self):
        self.nums = []          # 存储元素
        self.pos = {}           # 元素 -> 索引

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False

        self.nums.append(val)
        self.pos[val] = len(self.nums) - 1
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False

        # 将要删除的元素与最后一个元素交换
        index = self.pos[val]
        last = self.nums[-1]

        self.nums[index] = last
        self.pos[last] = index

        self.nums.pop()
        del self.pos[val]

        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)

# 测试
rs = RandomizedSet()
print(rs.insert(1))  # True
print(rs.remove(2))  # False
print(rs.insert(2))  # True
print(rs.getRandom())  # 1 或 2
print(rs.remove(1))  # True
print(rs.insert(2))  # False
print(rs.getRandom())  # 2
```

**验收标准**：
- [ ] 所有操作时间复杂度 O(1)
- [ ] 能正确实现删除操作（交换技巧）
- [ ] 能正确处理边界情况
- [ ] 能解释设计思路

---

**练习19：综合链表操作**

**场景说明**：设计一个支持多种操作的链表，综合考察链表操作。

**具体需求**：
1. addAtHead(val)：头部添加节点
2. addAtTail(val)：尾部添加节点
3. addAtIndex(index, val)：指定位置添加
4. deleteAtIndex(index)：删除指定位置
5. get(index)：获取指定位置的值

**使用示例**：
```python
class MyLinkedList:
    """设计链表"""

    class Node:
        def __init__(self, val=0):
            self.val = val
            self.next = None

    def __init__(self):
        self.dummy = self.Node()  # 哑节点
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1

        current = self.dummy.next
        for _ in range(index):
            current = current.next
        return current.val

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return

        prev = self.dummy
        for _ in range(index):
            prev = prev.next

        new_node = self.Node(val)
        new_node.next = prev.next
        prev.next = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        prev = self.dummy
        for _ in range(index):
            prev = prev.next

        prev.next = prev.next.next
        self.size -= 1
```

**验收标准**：
- [ ] 所有操作正确实现
- [ ] 使用哑节点简化边界处理
- [ ] 能正确处理索引越界
- [ ] 能分析时间复杂度

---

**练习20：算法复杂度分析练习**

**场景说明**：复杂度分析是算法面试的基础能力，需要能够快速分析代码的复杂度。

**具体需求**：
1. 分析以下代码的时间复杂度和空间复杂度
2. 说明分析的理由

**使用示例**：
```python
# 代码1
def func1(n):
    result = 0
    for i in range(n):
        for j in range(n):
            result += i * j
    return result

# 代码2
def func2(n):
    if n <= 1:
        return n
    return func2(n - 1) + func2(n - 2)

# 代码3
def func3(n):
    result = []
    for i in range(n):
        result = result + [i]  # 注意：列表拼接
    return result

# 代码4
def func4(n):
    while n > 1:
        n = n // 2
    return n
```

**完整答案**：
```
代码1：
- 时间复杂度：O(n^2)
- 空间复杂度：O(1)
- 理由：双重循环，外层 n 次，内层 n 次

代码2：
- 时间复杂度：O(2^n)
- 空间复杂度：O(n)
- 理由：递归树高度 n，每层分裂为 2 个子问题

代码3：
- 时间复杂度：O(n^2)
- 空间复杂度：O(n)
- 理由：列表拼接 result + [i] 是 O(n) 操作，循环 n 次

代码4：
- 时间复杂度：O(log n)
- 空间复杂度：O(1)
- 理由：每次 n 减半，需要 log n 次迭代
```

**验收标准**：
- [ ] 能正确分析每段代码的时间复杂度
- [ ] 能正确分析每段代码的空间复杂度
- [ ] 能解释分析的理由
- [ ] 能识别隐藏的复杂度（如列表拼接）

---

## 五、检验标准

### 验证题1：数组与双指针

**场景描述**：验证对双指针技巧的掌握程度。

**详细需求**：
1. 实现 `move_zeroes` 函数：将数组中的 0 移到末尾
2. 实现 `remove_duplicates` 函数：删除排序数组中的重复元素
3. 要求原地操作，时间复杂度 O(n)

**测试用例**：
```python
def move_zeroes(nums):
    """将 0 移到末尾"""
    # TODO: 实现
    pass

def remove_duplicates(nums):
    """删除排序数组中的重复元素，返回新长度"""
    # TODO: 实现
    pass

# 测试
nums1 = [0, 1, 0, 3, 12]
move_zeroes(nums1)
print(nums1)  # [1, 3, 12, 0, 0]

nums2 = [1, 1, 2]
length = remove_duplicates(nums2)
print(length, nums2[:length])  # 2, [1, 2]
```

**完整答案**：
```python
def move_zeroes(nums):
    """将 0 移到末尾"""
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1

def remove_duplicates(nums):
    """删除排序数组中的重复元素"""
    if not nums:
        return 0

    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    return slow + 1
```

**自测检查清单**：
- [ ] move_zeroes 正确实现
- [ ] remove_duplicates 正确实现
- [ ] 两个函数都是原地操作
- [ ] 时间复杂度都是 O(n)

---

### 验证题2：链表操作

**场景描述**：验证对链表操作的掌握程度。

**详细需求**：
1. 实现链表的中间节点查找
2. 实现链表是否为回文链表的判断
3. 使用快慢指针

**测试用例**：
```python
def middle_node(head):
    """返回链表的中间节点"""
    # TODO: 实现
    pass

def is_palindrome(head):
    """判断链表是否为回文"""
    # TODO: 实现
    pass
```

**完整答案**：
```python
def middle_node(head):
    """返回链表的中间节点"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def is_palindrome(head):
    """判断链表是否为回文"""
    # 1. 找中点
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2. 反转后半部分
    prev = None
    while slow:
        next_temp = slow.next
        slow.next = prev
        prev = slow
        slow = next_temp

    # 3. 比较前后两部分
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next

    return True
```

**自测检查清单**：
- [ ] middle_node 正确实现
- [ ] is_palindrome 正确实现
- [ ] 使用了快慢指针
- [ ] 能处理边界情况

---

### 验证题3：二叉树操作

**场景描述**：验证对二叉树遍历的掌握程度。

**详细需求**：
1. 实现二叉树的前序、中序、后序遍历（迭代）
2. 实现判断两棵树是否相同

**测试用例**：
```python
def preorder_traversal(root):
    """前序遍历（迭代）"""
    pass

def inorder_traversal(root):
    """中序遍历（迭代）"""
    pass

def is_same_tree(p, q):
    """判断两棵树是否相同"""
    pass
```

**完整答案**：
```python
def preorder_traversal(root):
    """前序遍历（迭代）"""
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result

def inorder_traversal(root):
    """中序遍历（迭代）"""
    result = []
    stack = []
    current = root

    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right

    return result

def is_same_tree(p, q):
    """判断两棵树是否相同"""
    if not p and not q:
        return True
    if not p or not q:
        return False
    if p.val != q.val:
        return False

    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
```

**自测检查清单**：
- [ ] 前序遍历迭代版本正确
- [ ] 中序遍历迭代版本正确
- [ ] is_same_tree 正确实现
- [ ] 能解释遍历的顺序

---

### 验证题4：哈希表应用

**场景描述**：验证对哈希表应用的掌握程度。

**详细需求**：
1. 实现两数之和（返回所有不重复的组合）
2. 实现判断两个字符串是否为字母异位词

**测试用例**：
```python
def two_sum_all(nums, target):
    """返回所有不重复的两数之和组合"""
    pass

def is_anagram(s, t):
    """判断两个字符串是否为字母异位词"""
    pass
```

**完整答案**：
```python
def two_sum_all(nums, target):
    """返回所有不重复的两数之和组合"""
    seen = set()
    result = set()

    for num in nums:
        complement = target - num
        if complement in seen:
            pair = tuple(sorted([num, complement]))
            result.add(pair)
        seen.add(num)

    return [list(pair) for pair in result]

def is_anagram(s, t):
    """判断两个字符串是否为字母异位词"""
    if len(s) != len(t):
        return False

    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1

    for c in t:
        if c not in count:
            return False
        count[c] -= 1
        if count[c] == 0:
            del count[c]

    return len(count) == 0
```

**自测检查清单**：
- [ ] two_sum_all 正确去重
- [ ] is_anagram 正确实现
- [ ] 时间复杂度合理
- [ ] 能处理边界情况

---

## 六、本周小结

1. **双指针**：数组问题常用技巧
2. **链表**：画图理解指针变化
3. **哈希表**：空间换时间
4. **二叉树**：递归思维

### 下周预告

第18周继续算法，学习搜索和动态规划。
