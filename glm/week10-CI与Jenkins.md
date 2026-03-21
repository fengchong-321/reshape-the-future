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

### 基础练习（1-8）

#### 练习1：Locust 安装与基础脚本

```python
# 任务要求：
# 1. 安装 Locust：pip install locust
# 2. 创建 locustfile.py 文件
# 3. 编写一个简单的用户类，测试 https://jsonplaceholder.typicode.com/posts
# 4. 使用 Web UI 模式运行（locust -f locustfile.py）
# 5. 访问 http://localhost:8089，设置 10 用户，观察结果

# 预期输出：
# 能在 Web UI 中看到实时统计图表
# 能停止测试并查看汇总报告
```

#### 练习2：GET 请求性能测试

```python
# 任务要求：
# 编写 Locust 脚本，测试以下接口：
# 1. GET /posts - 获取文章列表
# 2. GET /posts/1 - 获取单篇文章
# 3. GET /users - 获取用户列表

# 要求：
# - 设置 wait_time = between(1, 3)
# - 使用 name 参数命名请求
# - 使用权重控制请求比例（5:3:2）

# 预期输出：
# 能看到各接口的响应时间统计
```

#### 练习3：POST 请求性能测试

```python
# 任务要求：
# 编写测试脚本，发送 POST 请求创建文章

# 要求：
# 1. POST /posts，请求体为 JSON 格式
# 2. 包含 title、body、userId 字段
# 3. 设置适当的 Content-Type 头
# 4. 使用 catch_response=True 验证响应

# 预期输出：
# POST 请求成功率统计
# 响应时间分布
```

#### 练习4：命令行模式运行

```bash
# 任务要求：
# 使用无头模式（headless）运行性能测试

# 要求：
# 1. 总用户数：50
# 2. 每秒启动用户数：5
# 3. 运行时间：60 秒
# 4. 生成 HTML 报告

# 命令示例：
# locust -f locustfile.py --headless -u 50 -r 5 -t 60s --html=report.html

# 预期输出：
# 命令行输出测试进度
# 生成 report.html 文件
```

#### 练习5：用户初始化与清理

```python
# 任务要求：
# 编写带有 on_start 和 on_stop 方法的用户类

# 功能要求：
# 1. on_start：模拟用户登录，获取 token
# 2. 将 token 添加到请求头
# 3. 执行业务请求
# 4. on_stop：模拟用户登出

# 预期输出：
# 每个虚拟用户都会先登录再执行任务
# 测试结束后正确登出
```

#### 练习6：权重与任务分配

```python
# 任务要求：
# 模拟电商网站的真实用户行为

# 任务权重设置：
# 1. 浏览商品列表 - 权重 10（最常见）
# 2. 查看商品详情 - 权重 8
# 3. 搜索商品 - 权重 5
# 4. 加入购物车 - 权重 3
# 5. 提交订单 - 权重 1（最少）

# 预期输出：
# 验证各任务的执行次数比例接近权重设置
```

#### 练习7：响应验证

```python
# 任务要求：
# 使用 catch_response=True 进行响应验证

# 验证内容：
# 1. 验证状态码是否为 200
# 2. 验证响应 JSON 中是否包含特定字段
# 3. 验证响应时间是否在可接受范围内
# 4. 根据验证结果标记成功或失败

# 预期输出：
# 自定义的失败原因显示在报告中
```

#### 练习8：性能指标解读

```
# 任务要求：
# 分析以下 Locust 测试报告数据

# 数据：
# 总请求数：10000
# 失败数：50
# 平均响应时间：150ms
# P50：100ms
# P95：300ms
# P99：800ms
# RPS：166.67

# 问题：
# 1. 计算失败率，判断是否可接受
# 2. 分析 P99 响应时间是否达标
# 3. 计算 RPS 是否满足预期
# 4. 给出整体评估和优化建议

# 预期输出：
# 完整的性能分析报告
```

### 进阶练习（9-16）

#### 练习9：数据驱动测试

```python
# 任务要求：
# 使用外部数据文件驱动性能测试

# 功能要求：
# 1. 创建 test_data.json，包含多个搜索关键词
# 2. 在 on_start 中加载测试数据
# 3. 每次请求随机选择一个关键词
# 4. 使用参数化方式发送请求

# 示例数据：
# {"keywords": ["python", "java", "golang", "rust", "javascript"]}
```

#### 练习10：完整业务流程测试

```python
# 任务要求：
# 模拟完整的购物流程

# 流程步骤：
# 1. 浏览商品列表
# 2. 选择一个商品
# 3. 查看商品详情
# 4. 加入购物车
# 5. 提交订单

# 要求：
# - 每个步骤依赖上一步骤的结果
# - 使用 catch_response=True 处理异常
# - 记录每个步骤的响应时间
```

#### 练习11：等待时间策略

```python
# 任务要求：
# 实现不同的等待时间策略

# 策略实现：
# 1. 固定等待：between(2, 2)
# 2. 随机等待：between(1, 5)
# 3. 指数等待：自定义 wait_time 函数
# 4. 思考时间：模拟真实用户阅读时间

# 测试对比：
# 比较不同策略下的性能指标差异
```

#### 练习12：事件监听与自定义报告

```python
# 任务要求：
# 使用 Locust 事件系统生成自定义报告

# 功能要求：
# 1. test_start：测试开始时记录时间
# 2. test_stop：测试结束时生成报告
# 3. 导出 CSV 格式的详细数据
# 4. 计算并输出自定义指标
# 5. 生成简单的文本报告

# 预期输出：
# custom_report.csv
# summary.txt
```

#### 练习13：多用户类型模拟

```python
# 任务要求：
# 模拟不同类型的用户行为

# 用户类型：
# 1. 普通用户：浏览、搜索、查看详情
# 2. 注册用户：登录、浏览、下单
# 3. 管理员：登录、查看报表、管理操作

# 要求：
# - 创建 3 个不同的用户类
# - 设置不同的权重
# - 验证各类用户的请求分布
```

#### 练习14：性能测试场景设计

```python
# 任务要求：
# 设计并实现阶梯式负载测试

# 场景描述：
# 阶段1：10 用户，持续 1 分钟（预热）
# 阶段2：50 用户，持续 3 分钟（正常负载）
# 阶段3：100 用户，持续 2 分钟（高负载）
# 阶段4：200 用户，持续 1 分钟（压力测试）

# 要求：
# - 使用 Locust 的阶跃功能
# - 记录各阶段的性能指标
# - 分析性能拐点
```

#### 练习15：接口依赖处理

```python
# 任务要求：
# 处理有依赖关系的接口测试

# 场景：
# 1. 登录获取 token
# 2. 使用 token 获取用户信息
# 3. 使用用户 ID 查询订单
# 4. 创建新订单

# 要求：
# - 正确传递各步骤的数据
# - 处理 token 过期的情况
# - 验证数据一致性
```

#### 练习16：异常处理与重试

```python
# 任务要求：
# 实现健壮的异常处理机制

# 功能要求：
# 1. 捕获网络超时异常
# 2. 捕获服务器错误（5xx）
# 3. 实现简单的重试机制
# 4. 记录异常详情
# 5. 设置最大重试次数

# 预期输出：
# 异常情况不影响整体测试
# 详细的错误日志
```

### 综合练习（17-20）

#### 练习17：API 性能测试套件

```python
# 任务要求：
# 为 REST API 设计完整的性能测试套件

# 测试内容：
# 1. 用户模块：注册、登录、信息修改
# 2. 商品模块：列表、详情、搜索
# 3. 订单模块：创建、查询、取消
# 4. 支付模块：支付、回调

# 要求：
# - 使用真实 API（或 Mock 服务）
# - 设计合理的测试场景
# - 生成完整的测试报告
# - 包含性能基线对比
```

#### 练习18：性能瓶颈定位

```
# 场景描述：
# 某系统性能测试结果如下：
# - 100 并发：平均 RT 200ms，错误率 0.1%
# - 200 并发：平均 RT 500ms，错误率 1%
# - 500 并发：平均 RT 2000ms，错误率 15%
# - 1000 并发：平均 RT 5000ms，错误率 40%

# 任务要求：
# 1. 绘制性能曲线（并发数 vs 响应时间）
# 2. 分析性能拐点
# 3. 推测可能的瓶颈（数据库/应用/网络）
# 4. 提出优化建议
# 5. 设计验证方案

# 预期输出：
# 完整的性能分析报告
# 优化建议清单
```

#### 练习19：持续集成中的性能测试

```python
# 任务要求：
# 将 Locust 集成到 CI/CD 流程

# 功能要求：
# 1. 编写可在 CI 中运行的脚本
# 2. 设置性能阈值（断言）
# 3. 生成 JUnit 格式的报告
# 4. 测试失败时发送通知
# 5. 支持不同环境的配置

# 示例配置：
# - 平均响应时间 < 500ms
# - P99 响应时间 < 2000ms
# - 错误率 < 1%
```

#### 练习20：性能测试报告生成

```python
# 任务要求：
# 编写自动化报告生成脚本

# 报告内容：
# 1. 测试概要（时间、环境、配置）
# 2. 性能指标汇总表
# 3. 各接口详细数据
# 4. 性能评估（与基线对比）
# 5. 瓶颈分析
# 6. 优化建议
# 7. 附录（图表、原始数据）

# 输出格式：
# - Markdown 格式
# - HTML 格式（可选）

# 预期输出：
# 专业的性能测试报告文档
```

---

## 五、本周小结

1. **性能测试**：验证系统承载能力
2. **Locust**：Python 原生性能测试工具
3. **指标分析**：定位性能瓶颈

### 下周预告

第11周继续性能测试进阶。
