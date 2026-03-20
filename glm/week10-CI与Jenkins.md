# 第10周：性能测试基础 - Locust

## 本周目标

掌握性能测试基础概念，能使用 Locust 进行接口性能测试。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| 性能测试概念 | 负载测试、压力测试、并发 | ⭐⭐⭐⭐ |
| Locust 基础 | 安装、编写测试脚本 | ⭐⭐⭐⭐⭐ |
| Locust 进阶 | 自定义用户行为、权重 | ⭐⭐⭐⭐ |
| 性能指标 | TPS、RT、错误率 | ⭐⭐⭐⭐⭐ |
| 结果分析 | 报告解读、瓶颈定位 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 性能测试概念

```
性能测试类型：

1. 负载测试（Load Testing）
   - 验证系统在预期负载下的表现
   - 目的：确保系统能承受预期用户数

2. 压力测试（Stress Testing）
   - 逐步增加负载直到系统崩溃
   - 目的：找到系统的极限

3. 并发测试（Concurrency Testing）
   - 同时大量用户访问
   - 目的：验证并发处理能力

4. 持久测试（Soak Testing）
   - 长时间持续负载
   - 目的：发现内存泄漏等问题

核心指标：

- TPS/QPS：每秒事务数/查询数
- RT：响应时间（平均、P95、P99）
- 并发数：同时在线用户数
- 错误率：失败请求占比
- 资源使用率：CPU、内存、IO
```

---

### 2.2 Locust 基础

```bash
# 安装
pip install locust

# 验证
locust --version
```

```python
# locustfile.py
from locust import HttpUser, task, between

class MyUser(HttpUser):
    """模拟用户行为"""

    # 用户操作间隔时间（秒）
    wait_time = between(1, 3)

    # 基础 URL
    host = "https://jsonplaceholder.typicode.com"

    @task
    def get_posts(self):
        """获取文章列表"""
        self.client.get("/posts", name="获取文章列表")

    @task(3)  # 权重为 3，执行概率更高
    def get_post_detail(self):
        """获取文章详情"""
        post_id = 1  # 可以随机生成
        self.client.get(f"/posts/{post_id}", name="获取文章详情")

    @task
    def create_post(self):
        """创建文章"""
        self.client.post("/posts", json={
            "title": "测试标题",
            "body": "测试内容",
            "userId": 1
        }, name="创建文章")
```

```bash
# Web UI 模式运行
locust -f locustfile.py

# 访问 http://localhost:8089
# 设置用户数和每秒启动用户数

# 无头模式（命令行）
locust -f locustfile.py --headless -u 100 -r 10 -t 60s
# -u: 总用户数
# -r: 每秒启动用户数
# -t: 运行时间

# 生成 HTML 报告
locust -f locustfile.py --headless -u 100 -r 10 -t 60s --html=report.html
```

---

### 2.3 Locust 进阶

```python
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner, WorkerRunner
import json
import random

class APIUser(HttpUser):
    """API 性能测试用户"""

    wait_time = between(1, 2)
    host = "https://api.example.com"

    # ============================================
    # 初始化（每个用户执行一次）
    # ============================================
    def on_start(self):
        """用户开始前执行"""
        # 登录获取 Token
        response = self.client.post("/login", json={
            "username": "test",
            "password": "test123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.client.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
        else:
            self.token = None

    def on_stop(self):
        """用户结束后执行"""
        if self.token:
            self.client.post("/logout")

    # ============================================
    # 任务定义
    # ============================================
    @task(10)
    def browse_products(self):
        """浏览商品（高频操作）"""
        page = random.randint(1, 10)
        self.client.get(
            f"/products?page={page}",
            name="浏览商品"
        )

    @task(5)
    def view_product(self):
        """查看商品详情"""
        product_id = random.randint(1, 100)
        self.client.get(
            f"/products/{product_id}",
            name="查看商品详情"
        )

    @task(2)
    def add_to_cart(self):
        """加入购物车"""
        self.client.post("/cart/items", json={
            "product_id": random.randint(1, 100),
            "quantity": random.randint(1, 3)
        }, name="加入购物车")

    @task(1)
    def checkout(self):
        """下单（低频操作）"""
        self.client.post("/orders", json={
            "address_id": 1,
            "payment_method": "alipay"
        }, name="下单")

    # ============================================
    # 条件执行
    # ============================================
    @task
    def view_orders(self):
        """查看订单（需要登录）"""
        if not self.token:
            return  # 未登录跳过

        self.client.get("/orders", name="查看订单")


# ============================================
# 测试数据
# ============================================
class DataDrivenUser(HttpUser):
    """数据驱动性能测试"""

    wait_time = between(1, 3)
    host = "https://api.example.com"

    def on_start(self):
        # 加载测试数据
        with open("test_data.json") as f:
            self.test_data = json.load(f)

    @task
    def search(self):
        keyword = random.choice(self.test_data["keywords"])
        self.client.get(f"/search?q={keyword}", name="搜索")


# ============================================
# 分步测试
# ============================================
class WorkflowUser(HttpUser):
    """完整业务流程测试"""

    wait_time = between(2, 5)

    @task
    def purchase_flow(self):
        """完整购买流程"""
        # 1. 浏览商品
        with self.client.get("/products", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("获取商品失败")
                return
            products = response.json()

        # 2. 选择商品
        product_id = products[0]["id"]

        # 3. 加入购物车
        with self.client.post("/cart/items",
                             json={"product_id": product_id},
                             catch_response=True) as response:
            if response.status_code != 201:
                response.failure("加入购物车失败")
                return

        # 4. 下单
        self.client.post("/orders", name="下单")


# ============================================
# 事件监听
# ============================================
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """测试开始时执行"""
    print("性能测试开始...")

    # 只在 Master 节点执行
    if isinstance(environment.runner, MasterRunner):
        # 初始化测试数据
        pass

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """测试结束时执行"""
    print("性能测试结束...")

    # 输出统计信息
    stats = environment.stats
    print(f"总请求数: {stats.total.num_requests}")
    print(f"失败率: {stats.total.fail_ratio * 100:.2f}%")
    print(f"平均响应时间: {stats.total.avg_response_time:.2f}ms")
```

---

### 2.4 性能指标分析

```python
# 性能报告分析要点

"""
Locust 统计报告解读：

1. Requests（请求数）
   - Total Requests: 总请求数
   - Fails: 失败数
   - Failure rate: 失败率（应 < 1%）

2. Response Time（响应时间）
   - Average: 平均响应时间
   - Min/Max: 最小/最大响应时间
   - Median (50%): 中位数
   - 95%: 95% 的请求响应时间低于此值
   - 99%: 99% 的请求响应时间低于此值

3. RPS（每秒请求数）
   - Current: 当前 RPS
   - Average: 平均 RPS

性能评估标准：

| 指标 | 优秀 | 良好 | 一般 | 差 |
|------|------|------|------|-----|
| 平均 RT | <100ms | <300ms | <500ms | >500ms |
| P99 RT | <500ms | <1s | <2s | >2s |
| 错误率 | <0.1% | <1% | <5% | >5% |
| TPS | >1000 | >500 | >100 | <100 |
"""

# 自定义报告导出
@events.test_stop.add_listener
def export_custom_report(environment, **kwargs):
    """导出自定义报告"""
    import csv

    stats = environment.stats

    with open("performance_report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["接口", "请求数", "失败数", "错误率",
                        "平均RT", "P50", "P95", "P99", "RPS"])

        for name, entry in stats.entries.items():
            writer.writerow([
                name,
                entry.num_requests,
                entry.num_failures,
                f"{entry.fail_ratio * 100:.2f}%",
                f"{entry.avg_response_time:.2f}",
                f"{entry.get_response_time_percentile(0.5):.2f}",
                f"{entry.get_response_time_percentile(0.95):.2f}",
                f"{entry.get_response_time_percentile(0.99):.2f}",
                f"{entry.total_rps:.2f}"
            ])
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 理解性能测试核心概念
- [ ] 能编写 Locust 测试脚本
- [ ] 能运行性能测试并获取报告
- [ ] 能解读性能测试报告

### 应该了解

- [ ] 分布式运行
- [ ] 自定义报告

---

## 四、练习内容

### 练习1：登录接口压测

```python
# 编写 Locust 脚本
# 测试登录接口性能
# 要求：100 并发，持续 5 分钟
```

### 练习2：电商流程压测

```python
# 模拟完整购物流程
# 浏览 -> 加购 -> 下单
# 权重：10:5:1
```

### 练习3：报告分析

```
# 给定性能测试报告
# 分析瓶颈并给出优化建议
```

---

## 五、本周小结

1. **性能测试**：验证系统承载能力
2. **Locust**：Python 原生性能测试工具
3. **指标分析**：定位性能瓶颈

### 下周预告

第11周继续性能测试进阶。
