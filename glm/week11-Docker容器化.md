# 第11周：性能测试进阶

## 本周目标

掌握性能测试高级技巧，能进行性能分析和调优建议。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| 分布式压测 | Master-Worker 模式 | ⭐⭐⭐⭐ |
| 性能监控 | 服务器资源监控 | ⭐⭐⭐⭐⭐ |
| 瓶颈分析 | 定位性能瓶颈 | ⭐⭐⭐⭐⭐ |
| 测试报告 | 专业报告编写 | ⭐⭐⭐⭐ |
| 性能调优 | 常见优化策略 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 分布式压测

```bash
# 单机压测上限
# 单台机器通常只能模拟几百到几千用户
# 需要分布式压测模拟更大并发

# ============================================
# Master-Worker 模式
# ============================================
# Master 节点（协调）
locust -f locustfile.py --master

# Worker 节点（执行）
locust -f locustfile.py --worker --master-host=<master-ip>

# 多 Worker 示例
# 机器1（Master）：locust -f locustfile.py --master
# 机器2（Worker）：locust -f locustfile.py --worker --master-host=192.168.1.100
# 机器3（Worker）：locust -f locustfile.py --worker --master-host=192.168.1.100
# 机器4（Worker）：locust -f locustfile.py --worker --master-host=192.168.1.100
```

```python
# 分布式环境初始化
from locust import HttpUser, task, events
from locust.runners import MasterRunner

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """只在 Master 节点执行初始化"""
    if isinstance(environment.runner, MasterRunner):
        # 准备测试数据
        import requests
        requests.post("http://api.example.com/test/setup")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """只在 Master 节点执行清理"""
    if isinstance(environment.runner, MasterRunner):
        # 清理测试数据
        import requests
        requests.post("http://api.example.com/test/cleanup")
```

---

### 2.2 性能监控

```python
# ============================================
# 监控服务器资源
# ============================================
import psutil
import time

def monitor_resources(interval=1, duration=60):
    """监控 CPU 和内存使用"""
    results = []
    start_time = time.time()

    while time.time() - start_time < duration:
        cpu_percent = psutil.cpu_percent(interval=interval)
        memory = psutil.virtual_memory()

        results.append({
            "timestamp": time.time() - start_time,
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_used_gb": memory.used / (1024**3)
        })

    return results

# 使用
metrics = monitor_resources(interval=1, duration=60)
for m in metrics:
    print(f"CPU: {m['cpu_percent']}%, Memory: {m['memory_percent']}%")

# ============================================
# 监控数据库连接
# ============================================
import pymysql

def check_db_connections(host, user, password, database):
    """检查数据库连接数"""
    conn = pymysql.connect(
        host=host, user=user, password=password, database=database
    )
    cursor = conn.cursor()
    cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
    result = cursor.fetchone()
    cursor.execute("SHOW VARIABLES LIKE 'max_connections'")
    max_conn = cursor.fetchone()
    conn.close()

    current = int(result[1])
    max_allowed = int(max_conn[1])

    return {
        "current_connections": current,
        "max_connections": max_allowed,
        "usage_percent": current / max_allowed * 100
    }

# ============================================
# 监控 Redis
# ============================================
import redis

def check_redis_status(host="localhost", port=6379):
    """检查 Redis 状态"""
    r = redis.Redis(host=host, port=port)
    info = r.info()

    return {
        "connected_clients": info["connected_clients"],
        "used_memory_human": info["used_memory_human"],
        "total_commands_processed": info["total_commands_processed"],
        "instantaneous_ops_per_sec": info["instantaneous_ops_per_sec"]
    }
```

---

### 2.3 瓶颈分析

```python
# ============================================
# 性能瓶颈分析框架
# ============================================

class PerformanceAnalyzer:
    """性能分析器"""

    def __init__(self, locust_stats, server_metrics):
        self.stats = locust_stats
        self.metrics = server_metrics

    def analyze(self):
        """综合分析"""
        report = {
            "summary": self._get_summary(),
            "bottlenecks": [],
            "recommendations": []
        }

        # 1. 检查错误率
        if self.stats.total.fail_ratio > 0.01:
            report["bottlenecks"].append({
                "type": "high_error_rate",
                "severity": "high",
                "value": f"{self.stats.total.fail_ratio * 100:.2f}%",
                "threshold": "<1%"
            })
            report["recommendations"].append("检查错误日志，定位失败原因")

        # 2. 检查响应时间
        p99 = self.stats.total.get_response_time_percentile(0.99)
        if p99 > 2000:
            report["bottlenecks"].append({
                "type": "slow_response",
                "severity": "high",
                "value": f"P99: {p99:.0f}ms",
                "threshold": "<2000ms"
            })
            report["recommendations"].append("检查慢查询日志，优化数据库")

        # 3. 检查 CPU 使用率
        avg_cpu = sum(m["cpu_percent"] for m in self.metrics) / len(self.metrics)
        if avg_cpu > 80:
            report["bottlenecks"].append({
                "type": "high_cpu",
                "severity": "medium",
                "value": f"平均 CPU: {avg_cpu:.1f}%",
                "threshold": "<80%"
            })
            report["recommendations"].append("考虑增加服务器资源或优化代码")

        # 4. 检查内存使用
        avg_memory = sum(m["memory_percent"] for m in self.metrics) / len(self.metrics)
        if avg_memory > 85:
            report["bottlenecks"].append({
                "type": "high_memory",
                "severity": "high",
                "value": f"平均内存: {avg_memory:.1f}%",
                "threshold": "<85%"
            })
            report["recommendations"].append("检查内存泄漏，增加内存或优化")

        return report

    def _get_summary(self):
        """获取摘要"""
        return {
            "total_requests": self.stats.total.num_requests,
            "total_failures": self.stats.total.num_failures,
            "failure_rate": f"{self.stats.total.fail_ratio * 100:.2f}%",
            "avg_response_time": f"{self.stats.total.avg_response_time:.2f}ms",
            "rps": f"{self.stats.total.total_rps:.2f}"
        }

# ============================================
# 常见瓶颈类型
# ============================================
"""
1. 数据库瓶颈
   - 症状：响应时间随并发增加而急剧上升
   - 原因：慢查询、缺少索引、连接池不足
   - 解决：优化 SQL、添加索引、增加连接池

2. CPU 瓶颈
   - 症状：CPU 使用率接近 100%，响应变慢
   - 原因：计算密集型操作、死循环
   - 解决：优化算法、增加服务器、使用缓存

3. 内存瓶颈
   - 症状：内存使用率高，频繁 GC
   - 原因：内存泄漏、大对象
   - 解决：修复泄漏、调整 JVM 参数

4. 网络 I/O 瓶颈
   - 症状：响应时间长，但 CPU/内存正常
   - 原因：带宽不足、网络延迟
   - 解决：压缩传输、CDN、优化网络

5. 连接池瓶颈
   - 症状：请求等待，错误率上升
   - 原因：连接池太小
   - 解决：增加连接池大小
"""
```

---

### 2.4 性能测试报告

```python
# ============================================
# 性能测试报告模板
# ============================================

def generate_performance_report(test_config, locust_stats, server_metrics, analysis):
    """生成性能测试报告"""

    report = f"""
# 性能测试报告

## 1. 测试概要

| 项目 | 内容 |
|------|------|
| 测试日期 | {test_config['date']} |
| 测试环境 | {test_config['environment']} |
| 测试时长 | {test_config['duration']} |
| 并发用户数 | {test_config['users']} |
| 测试接口 | {test_config['endpoints']} |

## 2. 测试结果

### 2.1 总体指标

| 指标 | 数值 | 目标 | 结果 |
|------|------|------|------|
| 总请求数 | {locust_stats.total.num_requests} | - | - |
| 错误率 | {locust_stats.total.fail_ratio * 100:.2f}% | <1% | {'✅' if locust_stats.total.fail_ratio < 0.01 else '❌'} |
| 平均响应时间 | {locust_stats.total.avg_response_time:.2f}ms | <300ms | {'✅' if locust_stats.total.avg_response_time < 300 else '❌'} |
| P99 响应时间 | {locust_stats.total.get_response_time_percentile(0.99):.2f}ms | <1000ms | {'✅' if locust_stats.total.get_response_time_percentile(0.99) < 1000 else '❌'} |
| TPS | {locust_stats.total.total_rps:.2f} | >100 | {'✅' if locust_stats.total.total_rps > 100 else '❌'} |

### 2.2 资源使用

| 资源 | 平均使用率 | 峰值使用率 | 目标 |
|------|-----------|-----------|------|
| CPU | {sum(m['cpu_percent'] for m in server_metrics)/len(server_metrics):.1f}% | {max(m['cpu_percent'] for m in server_metrics):.1f}% | <80% |
| 内存 | {sum(m['memory_percent'] for m in server_metrics)/len(server_metrics):.1f}% | {max(m['memory_percent'] for m in server_metrics):.1f}% | <85% |

## 3. 瓶颈分析

"""
    for bottleneck in analysis["bottlenecks"]:
        report += f"""
### {bottleneck['type']}
- 严重程度：{bottleneck['severity']}
- 实际值：{bottleneck['value']}
- 阈值：{bottleneck['threshold']}
"""

    report += """
## 4. 优化建议

"""
    for i, rec in enumerate(analysis["recommendations"], 1):
        report += f"{i}. {rec}\n"

    report += """
## 5. 结论

本次性能测试{'通过' if locust_stats.total.fail_ratio < 0.01 and locust_stats.total.get_response_time_percentile(0.99) < 1000 else '未通过'}。

## 6. 附录

- 详细数据：[附件]
- 监控图表：[附件]
"""

    return report
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 能运行分布式压测
- [ ] 能监控服务器资源
- [ ] 能分析性能瓶颈
- [ ] 能编写性能测试报告

### 应该了解

- [ ] 容量规划
- [ ] 性能调优策略

---

## 四、练习内容

### 基础练习（1-8）

#### 练习1：分布式压测环境搭建

```bash
# 任务要求：
# 在两台机器（或两个终端）配置 Master-Worker 模式

# 步骤：
# 1. 机器1 启动 Master：
#    locust -f locustfile.py --master
# 2. 机器2 启动 Worker：
#    locust -f locustfile.py --worker --master-host=<master-ip>
# 3. 访问 Master 的 Web UI
# 4. 启动 100 并发用户测试
# 5. 观察两个节点的状态

# 预期输出：
# Master 能正确分配任务给 Worker
# 统计数据在 Master 汇总显示
```

#### 练习2：多 Worker 负载均衡

```bash
# 任务要求：
# 配置 3 个 Worker 节点，验证负载均衡

# 步骤：
# 1. 启动 1 个 Master 和 3 个 Worker
# 2. 设置 300 并发用户
# 3. 观察各 Worker 的请求分配情况
# 4. 动态添加/移除 Worker
# 5. 记录各节点的 RPS 贡献

# 预期输出：
# 请求均匀分配到各 Worker
# Worker 退出后任务自动重分配
```

#### 练习3：服务器资源监控

```python
# 任务要求：
# 编写资源监控脚本，与性能测试同步运行

# 功能要求：
# 1. 监控 CPU 使用率
# 2. 监控内存使用率
# 3. 监控磁盘 I/O
# 4. 每秒采样一次
# 5. 输出到 CSV 文件

# 使用 psutil 库：
import psutil
import csv
import time

# 预期输出：
# resources.csv 包含完整的监控数据
```

#### 练习4：数据库连接监控

```python
# 任务要求：
# 监控 MySQL 数据库连接数变化

# 功能要求：
# 1. 连接到 MySQL 数据库
# 2. 查询当前连接数
# 3. 查询最大连接数配置
# 4. 计算连接使用率
# 5. 每 5 秒输出一次状态

# SQL 参考：
# SHOW STATUS LIKE 'Threads_connected'
# SHOW VARIABLES LIKE 'max_connections'

# 预期输出：
# 连接数变化曲线
# 连接使用率告警（>80%）
```

#### 练习5：Redis 状态监控

```python
# 任务要求：
# 监控 Redis 在性能测试期间的状态

# 监控指标：
# 1. 连接客户端数
# 2. 内存使用量
# 3. 命令执行次数
# 4. 每秒操作数
# 5. 键空间大小

# 使用 redis-py：
import redis

# 预期输出：
# Redis 状态报告
# 性能瓶颈提示
```

#### 练习6：性能指标采集

```python
# 任务要求：
# 创建统一的指标采集类

# 功能要求：
class MetricsCollector:
    def __init__(self):
        # 初始化
        pass

    def collect(self):
        # 采集所有指标
        pass

    def to_dict(self):
        # 转换为字典格式
        pass

    def to_json(self):
        # 转换为 JSON 格式
        pass

# 采集内容：
# - CPU、内存、磁盘、网络
# - 自定义业务指标
# - 时间戳
```

#### 练习7：Locust 统计数据导出

```python
# 任务要求：
# 编写事件监听器，导出 Locust 统计数据

# 功能要求：
# 1. 在 test_stop 事件中触发
# 2. 导出每个接口的统计数据
# 3. 包含：请求数、失败数、响应时间、RPS
# 4. 输出为 CSV 和 JSON 两种格式
# 5. 生成汇总报告

# 预期输出：
# locust_stats.csv
# locust_stats.json
# summary.txt
```

#### 练习8：基础瓶颈识别

```
# 任务要求：
# 根据以下测试数据分析性能瓶颈

# 测试数据：
# - 总请求数：50000
# - 错误率：5.2%
# - 平均响应时间：800ms
# - P99 响应时间：3500ms
# - CPU 使用率：95%
# - 内存使用率：45%
# - 数据库连接数：150/200

# 问题：
# 1. 识别主要瓶颈
# 2. 分析可能的原因
# 3. 提出初步优化建议
# 4. 设计验证方案

# 预期输出：
# 瓶颈分析报告
```

### 进阶练习（9-16）

#### 练习9：性能分析器实现

```python
# 任务要求：
# 实现完整的性能分析器类

class PerformanceAnalyzer:
    def __init__(self, locust_stats, server_metrics):
        self.stats = locust_stats
        self.metrics = server_metrics

    def analyze(self):
        # 综合分析方法
        pass

    def check_error_rate(self, threshold=0.01):
        # 检查错误率
        pass

    def check_response_time(self, p99_threshold=2000):
        # 检查响应时间
        pass

    def check_resource_usage(self, cpu_threshold=80, mem_threshold=85):
        # 检查资源使用
        pass

    def generate_recommendations(self):
        # 生成优化建议
        pass

# 预期输出：
# 结构化的分析结果
```

#### 练习10：瓶颈类型分类

```python
# 任务要求：
# 实现瓶颈类型自动识别

# 瓶颈类型：
BOTTLENECK_TYPES = {
    'database': {
        'symptoms': ['响应时间随并发增加', '数据库连接数高'],
        'checks': ['check_db_connections', 'check_slow_queries']
    },
    'cpu': {
        'symptoms': ['CPU 使用率高', '响应变慢'],
        'checks': ['check_cpu_usage']
    },
    'memory': {
        'symptoms': ['内存使用高', '频繁 GC'],
        'checks': ['check_memory_usage', 'check_gc_stats']
    },
    'network': {
        'symptoms': ['响应时间长', 'CPU/内存正常'],
        'checks': ['check_network_io']
    }
}

# 实现自动识别逻辑
```

#### 练习11：性能基线管理

```python
# 任务要求：
# 实现性能基线的存储和对比

# 功能要求：
class BaselineManager:
    def __init__(self, baseline_file='baseline.json'):
        pass

    def save_baseline(self, stats):
        # 保存当前结果为基线
        pass

    def load_baseline(self):
        # 加载基线数据
        pass

    def compare(self, current_stats):
        # 对比当前结果与基线
        # 返回差异报告
        pass

    def check_regression(self, current_stats, thresholds):
        # 检查是否有性能退化
        pass

# 预期输出：
# 基线对比报告
# 性能退化告警
```

#### 练习12：实时监控仪表板

```python
# 任务要求：
# 创建实时性能监控仪表板

# 功能要求：
# 1. 实时显示 RPS 曲线
# 2. 实时显示响应时间曲线
# 3. 实时显示错误率
# 4. 显示服务器资源使用率
# 5. 告警提示

# 可选方案：
# - 使用 matplotlib 绘图
# - 使用 Flask 提供 Web 界面
# - 使用 WebSocket 实时推送

# 预期输出：
# 实时更新的监控界面
```

#### 练习13：性能测试配置管理

```python
# 任务要求：
# 实现测试场景的配置化管理

# 配置文件示例 (config.yaml)：
scenarios:
  smoke_test:
    users: 10
    spawn_rate: 5
    duration: 60
    thresholds:
      error_rate: 0.01
      avg_rt: 500
      p99_rt: 2000

  load_test:
    users: 100
    spawn_rate: 10
    duration: 300
    thresholds:
      error_rate: 0.01
      avg_rt: 300
      p99_rt: 1000

  stress_test:
    users: 500
    spawn_rate: 20
    duration: 600

# 实现配置加载和验证
```

#### 练习14：分布式测试数据准备

```python
# 任务要求：
# 在分布式环境下管理测试数据

# 功能要求：
# 1. Master 节点初始化测试数据
# 2. Worker 节点获取测试数据
# 3. 测试结束后清理数据
# 4. 支持数据隔离

# 使用 Locust 事件：
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        # Master 初始化
        pass

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        # Master 清理
        pass
```

#### 练习15：性能测试报告模板

```python
# 任务要求：
# 创建专业的性能测试报告生成器

# 报告结构：
class PerformanceReport:
    def __init__(self):
        self.test_config = {}      # 测试配置
        self.results = {}          # 测试结果
        self.resource_metrics = {} # 资源指标
        self.analysis = {}         # 瓶颈分析
        self.recommendations = []  # 优化建议

    def to_markdown(self):
        # 生成 Markdown 格式报告
        pass

    def to_html(self):
        # 生成 HTML 格式报告
        pass

    def to_pdf(self):
        # 生成 PDF 格式报告（可选）
        pass

# 预期输出：
# 完整的专业测试报告
```

#### 练习16：容量规划分析

```python
# 任务要求：
# 基于性能测试结果进行容量规划

# 分析内容：
# 1. 当前系统容量（最大并发、TPS）
# 2. 资源使用曲线
# 3. 性能拐点预测
# 4. 扩容建议

# 输入数据：
# - 不同并发下的性能数据
# - 资源使用数据
# - 业务增长预期

# 输出：
# - 当前容量评估
# - 扩容时机建议
# - 资源配置建议
```

### 综合练习（17-20）

#### 练习17：完整性能测试流程

```python
# 任务要求：
# 实现端到端的性能测试流程

# 流程步骤：
# 1. 环境检查（服务可用性、依赖服务）
# 2. 测试数据准备
# 3. 启动监控
# 4. 执行性能测试
# 5. 收集测试数据
# 6. 停止监控
# 7. 数据分析
# 8. 生成报告
# 9. 清理测试数据
# 10. 发送通知

# 实现要求：
# - 使用 Python 脚本编排
# - 支持配置化
# - 完善的错误处理
# - 详细的日志记录
```

#### 练习18：性能问题诊断案例

```
# 场景描述：
# 某电商系统在大促期间出现性能问题

# 症状：
# - 首页加载时间从 500ms 上升到 5000ms
# - 数据库 CPU 使用率 95%
# - 应用服务器 CPU 使用率 60%
# - 错误率从 0.1% 上升到 10%

# 任务要求：
# 1. 分析可能的瓶颈原因
# 2. 设计排查步骤
# 3. 提出优化方案
# 4. 制定验证计划

# 输出：
# - 问题诊断报告
# - 优化方案清单
# - 预期效果评估
```

#### 练习19：性能测试平台设计

```python
# 任务要求：
# 设计性能测试平台的核心模块

# 模块设计：
class PerformanceTestPlatform:
    """性能测试平台"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.test_executor = TestExecutor()
        self.monitor = ResourceMonitor()
        self.analyzer = PerformanceAnalyzer()
        self.reporter = ReportGenerator()

    def run_test(self, test_config):
        """执行测试"""
        pass

    def schedule_test(self, test_config, schedule):
        """定时测试"""
        pass

    def compare_results(self, test_id1, test_id2):
        """结果对比"""
        pass

# 实现各模块的核心功能
```

#### 练习20：性能优化实践

```python
# 任务要求：
# 基于性能测试结果实施优化并验证

# 优化场景（选择一个）：
# 场景 A：数据库优化
# - 添加缺失索引
# - 优化慢查询
# - 调整连接池配置

# 场景 B：缓存优化
# - 添加 Redis 缓存
# - 优化缓存策略
# - 实现缓存预热

# 场景 C：代码优化
# - 优化热点代码
# - 减少数据库查询
# - 异步处理

# 验证要求：
# 1. 优化前性能基线
# 2. 实施优化
# 3. 优化后性能测试
# 4. 对比分析报告
# 5. 效果量化（性能提升百分比）
```

---

## 五、本周小结

1. **分布式压测**：突破单机限制
2. **监控**：性能分析的基础
3. **瓶颈分析**：定位问题根源
4. **报告**：专业输出能力

### 下周预告

第12-13周学习 AI 与大模型测试。
