# 第17周：数据结构与算法（一）

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

## 四、本周练习清单

### 必刷题目

| 题号 | 题目 | 难度 |
|------|------|------|
| 1 | 两数之和 | 简单 |
| 3 | 无重复字符的最长子串 | 中等 |
| 15 | 三数之和 | 中等 |
| 20 | 有效的括号 | 简单 |
| 21 | 合并两个有序链表 | 简单 |
| 104 | 二叉树的最大深度 | 简单 |
| 141 | 环形链表 | 简单 |
| 146 | LRU 缓存 | 中等 |
| 206 | 反转链表 | 简单 |
| 236 | 二叉树的最近公共祖先 | 中等 |

---

## 五、本周小结

1. **双指针**：数组问题常用技巧
2. **链表**：画图理解指针变化
3. **哈希表**：空间换时间
4. **二叉树**：递归思维

### 下周预告

第18周继续算法，学习搜索和动态规划。
