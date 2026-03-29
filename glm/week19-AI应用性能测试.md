# 第19周：AI 应用性能测试

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

**场景说明：**
你是一家电商公司的性能测试工程师，需要为即将到来的大促活动进行压力测试。由于单机压测无法模拟足够的并发用户，你需要搭建分布式压测环境来模拟真实的高并发场景。

**具体需求：**
1. 在两台机器（或两个终端）配置 Master-Worker 模式
2. 确保 Master 能正确分配任务给 Worker
3. 验证统计数据能在 Master 汇总显示
4. 测试 100 并发用户的基本压测能力

**使用示例：**
```bash
# 步骤1：机器1 启动 Master
locust -f locustfile.py --master

# 步骤2：机器2 启动 Worker
locust -f locustfile.py --worker --master-host=<master-ip>

# 步骤3：访问 Master 的 Web UI（http://<master-ip>:8089）
# 步骤4：启动 100 并发用户测试
# 步骤5：观察两个节点的状态
```

**验收标准：**
- [ ] Master 和 Worker 成功建立连接
- [ ] Master Web UI 显示 Worker 节点状态为在线
- [ ] 压测任务能正确分配给 Worker 执行
- [ ] 统计数据（RPS、响应时间等）在 Master 汇总显示
- [ ] 能完成 100 并发用户的基本压测

#### 练习2：多 Worker 负载均衡

**场景说明：**
在大规模压测场景中，需要多个 Worker 节点协同工作。你需要验证 Locust 的负载均衡能力，确保请求能均匀分配到各个 Worker，并且在 Worker 动态变化时能自动调整。

**具体需求：**
1. 配置 1 个 Master 和 3 个 Worker 节点
2. 验证请求能均匀分配到各 Worker
3. 测试动态添加/移除 Worker 的场景
4. 记录各节点的 RPS 贡献

**使用示例：**
```bash
# 步骤1：启动 Master
locust -f locustfile.py --master

# 步骤2：启动 3 个 Worker（在不同终端或机器）
locust -f locustfile.py --worker --master-host=<master-ip>  # Worker 1
locust -f locustfile.py --worker --master-host=<master-ip>  # Worker 2
locust -f locustfile.py --worker --master-host=<master-ip>  # Worker 3

# 步骤3：设置 300 并发用户并启动压测
# 步骤4：观察各 Worker 的请求分配情况
# 步骤5：动态停止一个 Worker，观察任务重分配
```

**验收标准：**
- [ ] 3 个 Worker 都成功连接到 Master
- [ ] 请求均匀分配到各 Worker（偏差不超过 20%）
- [ ] Worker 退出后，任务能自动重分配到剩余节点
- [ ] 能记录各节点的 RPS 贡献数据
- [ ] Master 汇总统计数据准确

#### 练习3：服务器资源监控

**场景说明：**
在进行性能测试时，需要同时监控服务器的资源使用情况，以便分析系统瓶颈。你需要编写一个资源监控脚本，能够在压测期间持续采集 CPU、内存、磁盘 I/O 等指标。

**具体需求：**
1. 监控 CPU 使用率（总体和各核心）
2. 监控内存使用率（使用量和百分比）
3. 监控磁盘 I/O（读写速率）
4. 每秒采样一次，持续监控
5. 输出到 CSV 文件，便于后续分析

**使用示例：**
```python
import psutil
import csv
import time

def monitor_resources(interval=1, duration=60, output_file='resources.csv'):
    """
    监控服务器资源

    Args:
        interval: 采样间隔（秒）
        duration: 监控时长（秒）
        output_file: 输出文件名
    """
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'cpu_percent', 'memory_percent',
                         'memory_used_gb', 'disk_read_mb', 'disk_write_mb'])

        start_time = time.time()
        while time.time() - start_time < duration:
            cpu = psutil.cpu_percent(interval=interval)
            mem = psutil.virtual_memory()
            disk = psutil.disk_io_counters()

            writer.writerow([
                time.strftime('%Y-%m-%d %H:%M:%S'),
                cpu,
                mem.percent,
                mem.used / (1024**3),
                disk.read_bytes / (1024**2),
                disk.write_bytes / (1024**2)
            ])

# 使用：监控 60 秒，每秒采样
monitor_resources(interval=1, duration=60)
```

**验收标准：**
- [ ] 能正确采集 CPU 使用率数据
- [ ] 能正确采集内存使用率数据
- [ ] 能正确采集磁盘 I/O 数据
- [ ] CSV 文件格式正确，包含表头
- [ ] 采样间隔和持续时间可配置

#### 练习4：数据库连接监控

**场景说明：**
在压测过程中，数据库连接数是一个关键指标。连接数过高可能导致连接池耗尽，影响系统稳定性。你需要编写监控脚本来实时跟踪数据库连接状态。

**具体需求：**
1. 连接到 MySQL 数据库
2. 查询当前连接数和最大连接数配置
3. 计算连接使用率
4. 每 5 秒输出一次状态
5. 当使用率超过 80% 时发出告警

**使用示例：**
```python
import pymysql
import time

def monitor_db_connections(host, user, password, database, interval=5, duration=300):
    """
    监控数据库连接数

    Args:
        host: 数据库主机
        user: 用户名
        password: 密码
        database: 数据库名
        interval: 采样间隔（秒）
        duration: 监控时长（秒）
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        # 查询当前连接数
        cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
        current = int(cursor.fetchone()[1])

        # 查询最大连接数
        cursor.execute("SHOW VARIABLES LIKE 'max_connections'")
        max_conn = int(cursor.fetchone()[1])

        # 计算使用率
        usage = current / max_conn * 100

        print(f"连接数: {current}/{max_conn}, 使用率: {usage:.1f}%")

        # 告警判断
        if usage > 80:
            print(f"[WARNING] 连接使用率超过 80%!")

        conn.close()
        time.sleep(interval)

# SQL 参考：
# SHOW STATUS LIKE 'Threads_connected'
# SHOW VARIABLES LIKE 'max_connections'
```

**验收标准：**
- [ ] 能成功连接到 MySQL 数据库
- [ ] 能正确查询当前连接数和最大连接数
- [ ] 能正确计算连接使用率
- [ ] 能按指定间隔持续监控
- [ ] 当使用率超过 80% 时能发出告警

#### 练习5：Redis 状态监控

**场景说明：**
Redis 是系统中的关键缓存组件，在压测期间需要监控其状态，确保缓存不会成为性能瓶颈。你需要编写脚本监控 Redis 的关键指标。

**具体需求：**
1. 监控连接客户端数
2. 监控内存使用量
3. 监控命令执行次数和每秒操作数
4. 监控键空间大小
5. 生成 Redis 状态报告并提示潜在瓶颈

**使用示例：**
```python
import redis
import time

def monitor_redis(host="localhost", port=6379, interval=5, duration=60):
    """
    监控 Redis 状态

    Args:
        host: Redis 主机
        port: Redis 端口
        interval: 采样间隔（秒）
        duration: 监控时长（秒）
    """
    r = redis.Redis(host=host, port=port)
    start_time = time.time()
    prev_commands = 0

    while time.time() - start_time < duration:
        info = r.info()

        current_time = time.strftime('%H:%M:%S')
        clients = info['connected_clients']
        memory = info['used_memory_human']
        commands = info['total_commands_processed']
        ops_per_sec = info['instantaneous_ops_per_sec']
        keys = info.get('db0', {}).get('keys', 0) if 'db0' in info else 0

        # 计算每秒操作数
        if prev_commands > 0:
            actual_ops = (commands - prev_commands) / interval
        else:
            actual_ops = 0
        prev_commands = commands

        print(f"[{current_time}] 客户端: {clients}, 内存: {memory}, "
              f"OPS: {ops_per_sec}, 键数: {keys}")

        # 瓶颈提示
        if info['used_memory'] > 1024**3:  # 超过 1GB
            print("[WARNING] Redis 内存使用超过 1GB")

        time.sleep(interval)

# 使用
monitor_redis(host="localhost", port=6379, interval=5, duration=60)
```

**验收标准：**
- [ ] 能成功连接到 Redis
- [ ] 能正确获取客户端连接数
- [ ] 能正确获取内存使用量
- [ ] 能正确计算每秒操作数
- [ ] 能识别并提示潜在的性能瓶颈

#### 练习6：性能指标采集

**场景说明：**
为了方便性能测试数据的统一管理，需要创建一个可复用的指标采集类，能够采集服务器资源指标和自定义业务指标，并支持多种输出格式。

**具体需求：**
1. 创建统一的 MetricsCollector 类
2. 采集 CPU、内存、磁盘、网络等基础指标
3. 支持添加自定义业务指标
4. 支持转换为字典和 JSON 格式
5. 每次采集记录时间戳

**使用示例：**
```python
import psutil
import json
import time

class MetricsCollector:
    """统一的性能指标采集类"""

    def __init__(self):
        self.metrics = {}
        self.custom_metrics = {}

    def collect(self):
        """采集所有指标"""
        self.metrics = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_gb": psutil.virtual_memory().used / (1024**3),
            "disk_percent": psutil.disk_usage('/').percent,
            "network_bytes_sent": psutil.net_io_counters().bytes_sent,
            "network_bytes_recv": psutil.net_io_counters().bytes_recv,
        }
        # 合并自定义指标
        self.metrics.update(self.custom_metrics)
        return self.metrics

    def add_custom_metric(self, name, value):
        """添加自定义业务指标"""
        self.custom_metrics[name] = value

    def to_dict(self):
        """转换为字典格式"""
        return self.metrics

    def to_json(self):
        """转换为 JSON 格式"""
        return json.dumps(self.metrics, indent=2, ensure_ascii=False)

# 使用示例
collector = MetricsCollector()
collector.add_custom_metric("active_users", 100)
collector.add_custom_metric("requests_per_second", 500)

metrics = collector.collect()
print(collector.to_json())
```

**验收标准：**
- [ ] MetricsCollector 类能正确初始化
- [ ] collect() 方法能采集 CPU、内存、磁盘、网络指标
- [ ] 支持添加自定义业务指标
- [ ] to_dict() 返回正确的字典格式
- [ ] to_json() 返回正确的 JSON 格式
- [ ] 每次采集都包含时间戳

#### 练习7：Locust 统计数据导出

**场景说明：**
性能测试结束后，需要将 Locust 的统计数据导出为文件，便于后续分析和报告编写。你需要编写事件监听器来自动导出测试数据。

**具体需求：**
1. 在 test_stop 事件中触发导出
2. 导出每个接口的统计数据（请求数、失败数、响应时间、RPS）
3. 输出为 CSV 和 JSON 两种格式
4. 生成汇总报告

5. 支持自定义输出路径

**使用示例：**
```python
from locust import events
import csv
import json

@events.test_stop.add_listener
def export_stats(environment, **kwargs):
    """导出 Locust 统计数据"""
    stats = environment.stats

    # 导出 CSV
    with open('locust_stats.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'num_requests', 'num_failures',
                         'avg_response_time', 'min_response_time', 'max_response_time', 'total_rps'])

        for name, stats_entry in stats.entries.items():
            writer.writerow([
                name,
                stats_entry.num_requests,
                stats_entry.num_failures,
                stats_entry.avg_response_time,
                stats_entry.min_response_time,
                stats_entry.max_response_time,
                stats_entry.total_rps
            ])

    # 导出 JSON
    json_stats = {}
    for name, stats_entry in stats.entries.items():
        json_stats[name] = {
            'num_requests': stats_entry.num_requests,
            'num_failures': stats_entry.num_failures,
            'avg_response_time': stats_entry.avg_response_time,
            'rps': stats_entry.total_rps
        }

    with open('locust_stats.json', 'w') as f:
        json.dump(json_stats, f, indent=2)

    # 生成汇总报告
    total = stats.total
    summary = f"""
性能测试汇总报告
====================
总请求数: {total.num_requests}
总失败数: {total.num_failures}
失败率: {total.fail_ratio * 100:.2f}%
平均响应时间: {total.avg_response_time:.2f}ms
RPS: {total.total_rps:.2f}
"""
    with open('summary.txt', 'w') as f:
        f.write(summary)

    print("统计数据已导出到 locust_stats.csv, locust_stats.json 和 summary.txt")
```

**验收标准：**
- [ ] 事件监听器能正确注册到 test_stop 事件
- [ ] 能导出 CSV 格式文件，包含表头
- [ ] 能导出 JSON 格式文件，结构正确
- [ ] 能生成汇总报告文件
- [ ] 统计数据准确完整（包含所有接口）

#### 练习8：基础瓶颈识别

**场景说明：**
性能测试完成后，你收到了一份测试数据，需要根据这些数据分析系统的性能瓶颈，并提出优化建议。

**具体需求：**
根据以下测试数据分析性能瓶颈：
- 总请求数：50000
- 错误率：5.2%
- 平均响应时间：800ms
- P99 响应时间：3500ms
- CPU 使用率：95%
- 内存使用率：45%
- 数据库连接数：150/200

**使用示例：**
```
分析步骤：
1. 识别主要瓶颈
   - 错误率 5.2% > 1%（阈值），存在高错误率问题
   - P99 响应时间 3500ms > 2000ms（阈值），响应时间过长
   - CPU 使用率 95% > 80%（阈值），CPU 是主要瓶颈
   - 数据库连接使用率 75%（150/200），接近警戒线

2. 分析可能的原因
   - CPU 使用率高：可能是计算密集型操作、算法效率低
   - 响应时间长：可能受 CPU 瓶颈影响，或存在慢查询
   - 错误率高：可能是超时或资源不足导致

3. 初步优化建议
   - 优化 CPU 密集型代码，使用缓存减少计算
   - 检查数据库慢查询日志，添加必要索引
   - 考虑增加服务器资源或水平扩展

4. 验证方案
   - 优化后重新压测，对比 CPU 使用率变化
   - 验证响应时间和错误率是否改善
```

**验收标准：**
- [ ] 能正确识别 CPU 为主要瓶颈
- [ ] 能分析出至少 2 个可能的原因
- [ ] 能提出至少 3 条优化建议
- [ ] 能设计验证方案来确认优化效果
- [ ] 产出完整的瓶颈分析报告

### 进阶练习(9-16)

#### 练习9：性能分析器实现

**场景说明：**
你是一个性能测试团队的核心开发人员，需要构建一个可复用的性能分析器类，能够自动分析压测数据，识别性能瓶颈并给出优化建议。

**具体需求:**
1. 实现完整的 PerformanceAnalyzer 类
2. 支持错误率检查（可配置阈值）
3. 支持响应时间检查（P99 阈值可配置）
4. 支持资源使用检查（CPU、内存阈值可配置）
5. 自动生成优化建议

**使用示例:**
```python
class PerformanceAnalyzer:
    """性能分析器"""

    def __init__(self, locust_stats, server_metrics):
        self.stats = locust_stats
        self.metrics = server_metrics
        self.bottlenecks = []
        self.recommendations = []

    def analyze(self):
        """综合分析方法"""
        self.check_error_rate()
        self.check_response_time()
        self.check_resource_usage()
        self.generate_recommendations()
        return {
            "bottlenecks": self.bottlenecks,
            "recommendations": self.recommendations
        }

    def check_error_rate(self, threshold=0.01):
        """检查错误率"""
        fail_ratio = self.stats.total.fail_ratio
        if fail_ratio > threshold:
            self.bottlenecks.append({
                "type": "high_error_rate",
                "value": f"{fail_ratio * 100:.2f}%",
                "threshold": f"<{threshold * 100:.0f}%"
            })

    def check_response_time(self, p99_threshold=2000):
        """检查响应时间"""
        p99 = self.stats.total.get_response_time_percentile(0.99)
        if p99 > p99_threshold:
            self.bottlenecks.append({
                "type": "slow_response",
                "value": f"{p99:.0f}ms",
                "threshold": f"<{p99_threshold}ms"
            })

    def check_resource_usage(self, cpu_threshold=80, mem_threshold=85):
        """检查资源使用"""
        avg_cpu = sum(m["cpu_percent"] for m in self.metrics) / len(self.metrics)
        avg_mem = sum(m["memory_percent"] for m in self.metrics) / len(self.metrics)

        if avg_cpu > cpu_threshold:
            self.bottlenecks.append({
                "type": "high_cpu",
                "value": f"{avg_cpu:.1f}%",
                "threshold": f"<{cpu_threshold}%"
            })

        if avg_mem > mem_threshold:
            self.bottlenecks.append({
                "type": "high_memory",
                "value": f"{avg_mem:.1f}%",
                "threshold": f"<{mem_threshold}%"
            })

    def generate_recommendations(self):
        """生成优化建议"""
        for bottleneck in self.bottlenecks:
            if bottleneck["type"] == "high_error_rate":
                self.recommendations.append("检查错误日志，定位失败原因")
            elif bottleneck["type"] == "slow_response":
                self.recommendations.append("检查慢查询日志,优化数据库")
            elif bottleneck["type"] == "high_cpu":
                self.recommendations.append("优化算法或增加服务器资源")
            elif bottleneck["type"] == "high_memory":
                self.recommendations.append("检查内存泄漏,增加内存")

# 使用示例
analyzer = PerformanceAnalyzer(locust_stats, server_metrics)
result = analyzer.analyze()
print(f"发现 {len(result['bottlenecks'])} 个瓶颈")
for rec in result['recommendations']:
    print(f"建议: {rec}")
```
**验收标准:**
- [ ] PerformanceAnalyzer 类能正确初始化
- [ ] analyze() 方法返回结构化结果
- [ ] check_error_rate() 能正确识别高错误率
- [ ] check_response_time() 能正确识别慢响应
- [ ] check_resource_usage() 能正确识别高资源使用
- [ ] generate_recommendations() 能生成针对性建议

#### 练习10：瓶颈类型分类

**场景说明：**
在性能测试中，不同类型的瓶颈有不同的症状和解决方案。你需要实现一个自动识别系统，能够根据监控数据自动判断瓶颈类型。

**具体需求：**
1. 定义常见瓶颈类型及其症状
2. 实现自动识别逻辑
3. 支持多种检查方法的组合判断
4. 输出瓶颈类型和置信度

**使用示例：**
```python
# 瓶颈类型定义
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

class BottleneckClassifier:
    """瓶颈类型分类器"""

    def __init__(self):
        self.bottleneck_types = BOTTLENECK_TYPES

    def classify(self, metrics: dict) -> dict:
        """
        自动识别瓶颈类型

        Args:
            metrics: 包含各项指标的字典

        Returns:
            {"bottleneck_type": str, "confidence": float, "evidence": list}
        """
        results = []

        # 检查数据库瓶颈
        if self._check_database(metrics):
            results.append(("database", 0.8))

        # 检查 CPU 瓶颈
        if self._check_cpu(metrics):
            results.append(("cpu", 0.9))

        # 检查内存瓶颈
        if self._check_memory(metrics):
            results.append(("memory", 0.85))

        # 检查网络瓶颈
        if self._check_network(metrics):
            results.append(("network", 0.7))

        if results:
            # 按置信度排序
            results.sort(key=lambda x: x[1], reverse=True)
            return {
                "bottleneck_type": results[0][0],
                "confidence": results[0][1],
                "all_detected": results
            }

        return {"bottleneck_type": "unknown", "confidence": 0.0}

    def _check_database(self, metrics):
        return (metrics.get("db_connection_usage", 0) > 0.7 or
                metrics.get("slow_query_count", 0) > 10)

    def _check_cpu(self, metrics):
        return metrics.get("cpu_percent", 0) > 80

    def _check_memory(self, metrics):
        return metrics.get("memory_percent", 0) > 85

    def _check_network(self, metrics):
        return (metrics.get("cpu_percent", 0) < 60 and
                metrics.get("memory_percent", 0) < 60 and
                metrics.get("avg_response_time", 0) > 1000)

# 使用示例
classifier = BottleneckClassifier()
result = classifier.classify({
    "cpu_percent": 95,
    "memory_percent": 45,
    "db_connection_usage": 0.5,
    "avg_response_time": 800
})
print(f"识别结果: {result['bottleneck_type']}, 置信度: {result['confidence']}")
```

**验收标准：**
- [ ] 瓶颈类型定义完整（至少 4 种类型）
- [ ] classify() 方法能正确识别 CPU 瓶颈
- [ ] classify() 方法能正确识别内存瓶颈
- [ ] classify() 方法能正确识别数据库瓶颈
- [ ] 返回结果包含置信度
- [ ] 支持多种瓶颈同时存在的场景

#### 练习11：性能基线管理

**场景说明：**
为了跟踪系统性能的变化趋势，需要建立性能基线管理机制。每次性能测试后，与基线对比以检测是否存在性能退化。

**具体需求：**
1. 实现性能基线的存储和加载
2. 支持当前结果与基线的对比
3. 检测性能退化并告警
4. 支持更新基线

**使用示例：**
```python
import json
from datetime import datetime

class BaselineManager:
    """性能基线管理器"""

    def __init__(self, baseline_file='baseline.json'):
        self.baseline_file = baseline_file
        self.baseline = None

    def save_baseline(self, stats):
        """保存当前结果为基线"""
        self.baseline = {
            "timestamp": datetime.now().isoformat(),
            "avg_response_time": stats.total.avg_response_time,
            "p99_response_time": stats.total.get_response_time_percentile(0.99),
            "rps": stats.total.total_rps,
            "error_rate": stats.total.fail_ratio
        }
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)
        print(f"基线已保存到 {self.baseline_file}")

    def load_baseline(self):
        """加载基线数据"""
        try:
            with open(self.baseline_file, 'r') as f:
                self.baseline = json.load(f)
            return self.baseline
        except FileNotFoundError:
            print("未找到基线文件")
            return None

    def compare(self, current_stats):
        """对比当前结果与基线"""
        if not self.baseline:
            return {"error": "未加载基线数据"}

        current = {
            "avg_response_time": current_stats.total.avg_response_time,
            "p99_response_time": current_stats.total.get_response_time_percentile(0.99),
            "rps": current_stats.total.total_rps,
            "error_rate": current_stats.total.fail_ratio
        }

        diff = {}
        for key in current:
            if self.baseline[key] != 0:
                change = (current[key] - self.baseline[key]) / self.baseline[key] * 100
                diff[key] = {
                    "baseline": self.baseline[key],
                    "current": current[key],
                    "change_percent": change
                }

        return diff

    def check_regression(self, current_stats, thresholds):
        """检查是否有性能退化"""
        diff = self.compare(current_stats)
        regressions = []

        # 检查响应时间退化
        if diff.get("avg_response_time", {}).get("change_percent", 0) > thresholds.get("response_time", 20):
            regressions.append("平均响应时间退化超过阈值")

        # 检查 RPS 退化
        if diff.get("rps", {}).get("change_percent", 0) < -thresholds.get("rps", 10):
            regressions.append("RPS 下降超过阈值")

        # 检查错误率上升
        if diff.get("error_rate", {}).get("change_percent", 0) > thresholds.get("error_rate", 50):
            regressions.append("错误率上升超过阈值")

        return {
            "has_regression": len(regressions) > 0,
            "regressions": regressions
        }

# 使用示例
manager = BaselineManager()
manager.load_baseline()

# 对比当前结果
diff = manager.compare(current_stats)
for key, value in diff.items():
    print(f"{key}: 基线={value['baseline']:.2f}, 当前={value['current']:.2f}, 变化={value['change_percent']:.1f}%")

# 检查退化
result = manager.check_regression(current_stats, {"response_time": 20, "rps": 10, "error_rate": 50})
if result["has_regression"]:
    print(f"发现性能退化: {result['regressions']}")
```

**验收标准：**
- [ ] save_baseline() 能正确保存基线到文件
- [ ] load_baseline() 能正确加载基线数据
- [ ] compare() 能计算各指标的变化百分比
- [ ] check_regression() 能检测性能退化
- [ ] 支持自定义退化阈值

#### 练习12：实时监控仪表板

**场景说明：**
在性能测试执行过程中，测试人员需要实时查看系统状态。你需要创建一个实时监控仪表板，可视化展示关键性能指标。

**具体需求：**
1. 实时显示 RPS 曲线
2. 实时显示响应时间曲线
3. 实时显示错误率
4. 显示服务器资源使用率（CPU、内存）
5. 当指标超过阈值时显示告警

**使用示例：**
```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import time

class RealtimeDashboard:
    """实时性能监控仪表板"""

    def __init__(self, max_points=100):
        self.max_points = max_points
        self.rps_data = deque(maxlen=max_points)
        self.response_time_data = deque(maxlen=max_points)
        self.error_rate_data = deque(maxlen=max_points)
        self.timestamps = deque(maxlen=max_points)

        # 设置图表
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('Performance Test Dashboard')

    def update(self, frame):
        """更新图表数据"""
        # 模拟获取实时数据
        current_time = time.time()

        # 这里应该从 Locust 或监控系统获取实际数据
        # 示例使用模拟数据
        self.timestamps.append(current_time)
        self.rps_data.append(self._get_current_rps())
        self.response_time_data.append(self._get_avg_response_time())
        self.error_rate_data.append(self._get_error_rate())

        # 清空并重绘
        for ax in self.axes.flat:
            ax.clear()

        # RPS 图
        self.axes[0, 0].plot(list(self.rps_data), 'b-')
        self.axes[0, 0].set_title('RPS')
        self.axes[0, 0].set_ylabel('Requests/sec')

        # 响应时间图
        self.axes[0, 1].plot(list(self.response_time_data), 'g-')
        self.axes[0, 1].set_title('Response Time')
        self.axes[0, 1].set_ylabel('ms')
        self.axes[0, 1].axhline(y=500, color='r', linestyle='--', label='Threshold')
        self.axes[0, 1].legend()

        # 错误率图
        self.axes[1, 0].plot(list(self.error_rate_data), 'r-')
        self.axes[1, 0].set_title('Error Rate')
        self.axes[1, 0].set_ylabel('%')
        self.axes[1, 0].axhline(y=1, color='r', linestyle='--', label='Threshold')

        # 资源使用图
        cpu, memory = self._get_resource_usage()
        self.axes[1, 1].bar(['CPU', 'Memory'], [cpu, memory])
        self.axes[1, 1].set_title('Resource Usage')
        self.axes[1, 1].set_ylabel('%')
        self.axes[1, 1].set_ylim(0, 100)

        # 告警检查
        if self.error_rate_data[-1] > 1:
            self.fig.suptitle('Performance Test Dashboard - WARNING: High Error Rate!',
                             color='red', fontsize=14)

        return self.axes.flat

    def _get_current_rps(self):
        """获取当前 RPS（应从实际数据源获取）"""
        return 100 + (time.time() % 50)  # 模拟数据

    def _get_avg_response_time(self):
        """获取平均响应时间"""
        return 200 + (time.time() % 100)

    def _get_error_rate(self):
        """获取错误率"""
        return 0.5 + (time.time() % 2)

    def _get_resource_usage(self):
        """获取资源使用率"""
        import psutil
        return psutil.cpu_percent(), psutil.virtual_memory().percent

    def start(self):
        """启动仪表板"""
        ani = FuncAnimation(self.fig, self.update, interval=1000)
        plt.tight_layout()
        plt.show()

# 使用示例
dashboard = RealtimeDashboard()
dashboard.start()
```

**验收标准：**
- [ ] 仪表板能正常启动并显示图表
- [ ] RPS 曲线能实时更新
- [ ] 响应时间曲线能实时更新
- [ ] 错误率能实时显示
- [ ] 资源使用率能正确显示
- [ ] 指标超过阈值时能显示告警

#### 练习13：性能测试配置管理

**场景说明：**
为了支持不同类型的性能测试（冒烟测试、负载测试、压力测试），需要实现测试场景的配置化管理，方便快速切换和复用测试配置。

**具体需求：**
1. 支持 YAML 格式的配置文件
2. 支持多种测试场景（冒烟、负载、压力）
3. 每个场景可配置用户数、启动速率、持续时间、阈值
4. 实现配置加载和验证功能

**使用示例：**
```yaml
# config.yaml 配置文件示例
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
    thresholds:
      error_rate: 0.05
      avg_rt: 1000
      p99_rt: 3000
```

```python
import yaml
from dataclasses import dataclass

@dataclass
class TestScenario:
    """测试场景配置"""
    name: str
    users: int
    spawn_rate: int
    duration: int
    thresholds: dict

class ConfigManager:
    """性能测试配置管理器"""

    def __init__(self, config_file='config.yaml'):
        self.config_file = config_file
        self.scenarios = {}

    def load_config(self):
        """加载配置文件"""
        with open(self.config_file, 'r') as f:
            config = yaml.safe_load(f)

        for name, scenario_config in config.get('scenarios', {}).items():
            self.scenarios[name] = TestScenario(
                name=name,
                users=scenario_config.get('users', 10),
                spawn_rate=scenario_config.get('spawn_rate', 5),
                duration=scenario_config.get('duration', 60),
                thresholds=scenario_config.get('thresholds', {})
            )

        return self.scenarios

    def validate_scenario(self, scenario_name):
        """验证场景配置"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"场景 '{scenario_name}' 不存在")

        scenario = self.scenarios[scenario_name]
        errors = []

        if scenario.users <= 0:
            errors.append("用户数必须大于 0")
        if scenario.spawn_rate <= 0:
            errors.append("启动速率必须大于 0")
        if scenario.duration <= 0:
            errors.append("持续时间必须大于 0")

        thresholds = scenario.thresholds
        if thresholds.get('error_rate', 0) > 1:
            errors.append("错误率阈值不能超过 100%")

        return len(errors) == 0, errors

    def get_scenario(self, scenario_name):
        """获取指定场景配置"""
        if scenario_name not in self.scenarios:
            self.load_config()
        return self.scenarios.get(scenario_name)

# 使用示例
manager = ConfigManager('config.yaml')
manager.load_config()

# 获取并验证冒烟测试配置
scenario = manager.get_scenario('smoke_test')
is_valid, errors = manager.validate_scenario('smoke_test')

if is_valid:
    print(f"场景: {scenario.name}")
    print(f"用户数: {scenario.users}")
    print(f"持续时间: {scenario.duration}s")
else:
    print(f"配置错误: {errors}")
```

**验收标准：**
- [ ] 能正确加载 YAML 配置文件
- [ ] 能解析多种测试场景
- [ ] validate_scenario() 能检测无效配置
- [ ] get_scenario() 能返回正确的场景配置
- [ ] 配置文件格式清晰，易于维护

#### 练习14：分布式测试数据准备

**场景说明：**
在分布式压测中，需要在 Master 节点统一准备测试数据，测试结束后清理数据，避免数据污染。需要实现分布式环境下的测试数据管理机制。

**具体需求：**
1. Master 节点统一初始化测试数据
2. Worker 节点能获取测试数据
3. 测试结束后 Master 清理数据
4. 支持数据隔离（多次测试不互相影响）

**使用示例：**
```python
from locust import events, HttpUser, task
from locust.runners import MasterRunner
import requests
import json

class DistributedDataManager:
    """分布式测试数据管理器"""

    def __init__(self, api_base_url):
        self.api_base_url = api_base_url
        self.test_data_id = None

    def setup_test_data(self):
        """初始化测试数据"""
        # 创建测试用户
        users = []
        for i in range(100):
            user = {
                "username": f"test_user_{i}",
                "password": "test123",
                "email": f"test{i}@example.com"
            }
            response = requests.post(
                f"{self.api_base_url}/api/test/users",
                json=user
            )
            users.append(response.json()["id"])

        # 创建测试订单
        orders = []
        for user_id in users[:50]:
            order = {
                "user_id": user_id,
                "product_id": 1,
                "quantity": 1
            }
            response = requests.post(
                f"{self.api_base_url}/api/test/orders",
                json=order
            )
            orders.append(response.json()["id"])

        self.test_data_id = {
            "users": users,
            "orders": orders
        }

        # 保存数据 ID 到文件供 Worker 使用
        with open("test_data_id.json", "w") as f:
            json.dump(self.test_data_id, f)

        print(f"测试数据已创建: {len(users)} 用户, {len(orders)} 订单")
        return self.test_data_id

    def cleanup_test_data(self):
        """清理测试数据"""
        if not self.test_data_id:
            return

        # 删除测试用户（会级联删除订单）
        for user_id in self.test_data_id["users"]:
            requests.delete(f"{self.api_base_url}/api/test/users/{user_id}")

        print(f"测试数据已清理: {len(self.test_data_id['users'])} 用户")

        # 删除 ID 文件
        import os
        if os.path.exists("test_data_id.json"):
            os.remove("test_data_id.json")

# 全局数据管理器
data_manager = DistributedDataManager("http://localhost:8000")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """只在 Master 节点执行初始化"""
    if isinstance(environment.runner, MasterRunner):
        print("Master 节点: 开始准备测试数据...")
        data_manager.setup_test_data()

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """只在 Master 节点执行清理"""
    if isinstance(environment.runner, MasterRunner):
        print("Master 节点: 开始清理测试数据...")
        data_manager.cleanup_test_data()

class TestUser(HttpUser):
    """测试用户类"""

    def on_start(self):
        """Worker 节点获取测试数据"""
        # 从文件加载测试数据 ID
        try:
            with open("test_data_id.json", "r") as f:
                self.test_data = json.load(f)
        except FileNotFoundError:
            self.test_data = None

    @task
    def test_api(self):
        """测试任务"""
        if self.test_data and self.test_data["users"]:
            user_id = self.test_data["users"][0]
            self.client.get(f"/api/users/{user_id}")
```

**验收标准：**
- [ ] Master 节点能成功初始化测试数据
- [ ] 测试数据 ID 能保存到文件
- [ ] Worker 节点能读取测试数据
- [ ] 测试结束后数据能正确清理
- [ ] 支持多次测试的数据隔离

#### 练习15：性能测试报告模板

**场景说明：**
性能测试完成后，需要生成专业的测试报告给项目组和管理层。你需要创建一个可复用的报告生成器，支持多种输出格式。

**具体需求：**
1. 创建专业的性能测试报告生成器
2. 支持 Markdown 和 HTML 两种输出格式
3. 包含测试配置、结果、资源指标、瓶颈分析、优化建议
4. 报告格式清晰专业

**使用示例：**
```python
from datetime import datetime

class PerformanceReport:
    """专业的性能测试报告生成器"""

    def __init__(self):
        self.test_config = {}       # 测试配置
        self.results = {}           # 测试结果
        self.resource_metrics = {}  # 资源指标
        self.analysis = {}          # 瓶颈分析
        self.recommendations = []   # 优化建议

    def set_test_config(self, config: dict):
        """设置测试配置"""
        self.test_config = config

    def set_results(self, results: dict):
        """设置测试结果"""
        self.results = results

    def set_resource_metrics(self, metrics: dict):
        """设置资源指标"""
        self.resource_metrics = metrics

    def set_analysis(self, analysis: dict):
        """设置瓶颈分析"""
        self.analysis = analysis

    def set_recommendations(self, recommendations: list):
        """设置优化建议"""
        self.recommendations = recommendations

    def to_markdown(self) -> str:
        """生成 Markdown 格式报告"""
        report = f"""# 性能测试报告

## 1. 测试概要

| 项目 | 内容 |
|------|------|
| 测试日期 | {self.test_config.get('date', 'N/A')} |
| 测试环境 | {self.test_config.get('environment', 'N/A')} |
| 测试时长 | {self.test_config.get('duration', 'N/A')} |
| 并发用户数 | {self.test_config.get('users', 'N/A')} |

## 2. 测试结果

### 2.1 总体指标

| 指标 | 数值 | 目标 | 结果 |
|------|------|------|------|
| 总请求数 | {self.results.get('total_requests', 0)} | - | - |
| 错误率 | {self.results.get('error_rate', 0):.2%} | <1% | {'通过' if self.results.get('error_rate', 1) < 0.01 else '未通过'} |
| 平均响应时间 | {self.results.get('avg_response_time', 0):.0f}ms | <300ms | {'通过' if self.results.get('avg_response_time', 999) < 300 else '未通过'} |
| P99 响应时间 | {self.results.get('p99_response_time', 0):.0f}ms | <1000ms | {'通过' if self.results.get('p99_response_time', 9999) < 1000 else '未通过'} |
| TPS | {self.results.get('tps', 0):.2f} | >100 | {'通过' if self.results.get('tps', 0) > 100 else '未通过'} |

### 2.2 资源使用

| 资源 | 平均使用率 | 峰值使用率 | 目标 |
|------|-----------|-----------|------|
| CPU | {self.resource_metrics.get('avg_cpu', 0):.1f}% | {self.resource_metrics.get('max_cpu', 0):.1f}% | <80% |
| 内存 | {self.resource_metrics.get('avg_memory', 0):.1f}% | {self.resource_metrics.get('max_memory', 0):.1f}% | <85% |

## 3. 瓶颈分析

"""
        for bottleneck in self.analysis.get("bottlenecks", []):
            report += f"- **{bottleneck['type']}**: {bottleneck['value']} (阈值: {bottleneck['threshold']})\n"

        report += "\n## 4. 优化建议\n\n"
        for i, rec in enumerate(self.recommendations, 1):
            report += f"{i}. {rec}\n"

        report += f"""
## 5. 结论

本次性能测试{'通过' if self.results.get('error_rate', 1) < 0.01 and self.results.get('p99_response_time', 9999) < 1000 else '未通过'}。

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return report

    def to_html(self) -> str:
        """生成 HTML 格式报告"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>性能测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
    </style>
</head>
<body>
    <h1>性能测试报告</h1>
    <h2>1. 测试概要</h2>
    <table>
        <tr><th>项目</th><th>内容</th></tr>
        <tr><td>测试日期</td><td>{self.test_config.get('date', 'N/A')}</td></tr>
        <tr><td>测试环境</td><td>{self.test_config.get('environment', 'N/A')}</td></tr>
        <tr><td>并发用户数</td><td>{self.test_config.get('users', 'N/A')}</td></tr>
    </table>

    <h2>2. 测试结果</h2>
    <table>
        <tr><th>指标</th><th>数值</th><th>目标</th><th>结果</th></tr>
        <tr>
            <td>错误率</td>
            <td>{self.results.get('error_rate', 0):.2%}</td>
            <td>&lt;1%</td>
            <td class="{'pass' if self.results.get('error_rate', 1) < 0.01 else 'fail'}">
                {'通过' if self.results.get('error_rate', 1) < 0.01 else '未通过'}
            </td>
        </tr>
        <tr>
            <td>平均响应时间</td>
            <td>{self.results.get('avg_response_time', 0):.0f}ms</td>
            <td>&lt;300ms</td>
            <td class="{'pass' if self.results.get('avg_response_time', 999) < 300 else 'fail'}">
                {'通过' if self.results.get('avg_response_time', 999) < 300 else '未通过'}
            </td>
        </tr>
    </table>

    <h2>5. 结论</h2>
    <p>本次性能测试{'通过' if self.results.get('error_rate', 1) < 0.01 else '未通过'}。</p>
</body>
</html>
"""
        return html

# 使用示例
report = PerformanceReport()
report.set_test_config({
    "date": "2024-01-15",
    "environment": "Staging",
    "duration": "5分钟",
    "users": 100
})
report.set_results({
    "total_requests": 50000,
    "error_rate": 0.005,
    "avg_response_time": 150,
    "p99_response_time": 450,
    "tps": 166.5
})
report.set_resource_metrics({
    "avg_cpu": 65,
    "max_cpu": 78,
    "avg_memory": 55,
    "max_memory": 62
})
report.set_analysis({"bottlenecks": []})
report.set_recommendations(["建议添加 Redis 缓存减少数据库压力"])

# 保存报告
with open("performance_report.md", "w") as f:
    f.write(report.to_markdown())

with open("performance_report.html", "w") as f:
    f.write(report.to_html())

print("报告已生成: performance_report.md, performance_report.html")
```

**验收标准：**
- [ ] to_markdown() 能生成完整的 Markdown 报告
- [ ] to_html() 能生成完整的 HTML 报告
- [ ] 报告包含测试概要、结果、资源使用、瓶颈分析、建议
- [ ] Markdown 格式正确，易于阅读
- [ ] HTML 报告有基本样式，显示美观

#### 练习16：容量规划分析

**场景说明：**
性能测试的最终目的是为系统容量规划提供依据。你需要基于性能测试结果，分析系统当前容量，预测性能拐点，并给出扩容建议。

**具体需求：**
1. 分析当前系统容量（最大并发、TPS）
2. 绘制资源使用曲线
3. 预测性能拐点
4. 给出扩容建议

**使用示例：**
```python
from dataclasses import dataclass
from typing import List

@dataclass
class CapacityData:
    """容量测试数据"""
    concurrent_users: int
    tps: float
    avg_response_time: float
    cpu_percent: float
    memory_percent: float
    error_rate: float

class CapacityPlanner:
    """容量规划分析器"""

    def __init__(self, test_data: List[CapacityData]):
        self.test_data = test_data

    def analyze_current_capacity(self):
        """分析当前系统容量"""
        # 找到错误率 < 1% 且响应时间 < 500ms 的最大并发
        valid_data = [
            d for d in self.test_data
            if d.error_rate < 0.01 and d.avg_response_time < 500
        ]

        if valid_data:
            max_capacity = max(valid_data, key=lambda x: x.concurrent_users)
            return {
                "max_concurrent_users": max_capacity.concurrent_users,
                "max_tps": max_capacity.tps,
                "cpu_at_max": max_capacity.cpu_percent,
                "memory_at_max": max_capacity.memory_percent
            }
        return None

    def predict_bottleneck(self):
        """预测性能拐点"""
        # 使用线性回归预测 CPU 达到 80% 时的并发数
        from statistics import linear_regression

        users = [d.concurrent_users for d in self.test_data]
        cpu = [d.cpu_percent for d in self.test_data]

        # 简单线性预测
        slope = (cpu[-1] - cpu[0]) / (users[-1] - users[0])
        intercept = cpu[0] - slope * users[0]

        # 预测 CPU = 80% 时的并发数
        predicted_users = (80 - intercept) / slope if slope > 0 else float('inf')

        return {
            "predicted_bottleneck_users": int(predicted_users),
            "warning": "接近性能拐点" if predicted_users < max(users) * 1.2 else "容量充足"
        }

    def calculate_scaling_recommendation(self, target_tps: float):
        """计算扩容建议"""
        current_capacity = self.analyze_current_capacity()
        if not current_capacity:
            return {"error": "无法分析当前容量"}

        current_tps = current_capacity["max_tps"]
        scaling_factor = target_tps / current_tps

        return {
            "current_max_tps": current_tps,
            "target_tps": target_tps,
            "scaling_factor": scaling_factor,
            "recommended_servers": int(scaling_factor + 0.5),  # 向上取整
            "estimated_cost_increase": f"{(scaling_factor - 1) * 100:.0f}%"
        }

    def generate_capacity_report(self):
        """生成容量规划报告"""
        current = self.analyze_current_capacity()
        bottleneck = self.predict_bottleneck()

        report = f"""
容量规划分析报告
================

1. 当前系统容量
   - 最大并发用户: {current['max_concurrent_users']}
   - 最大 TPS: {current['max_tps']:.2f}
   - 此时 CPU 使用率: {current['cpu_at_max']:.1f}%
   - 此时内存使用率: {current['memory_at_max']:.1f}%

2. 性能拐点预测
   - 预计 CPU 瓶颈出现在: {bottleneck['predicted_bottleneck_users']} 并发用户
   - 状态: {bottleneck['warning']}

3. 扩容建议
   - 如果需要支持更多用户，建议先优化代码或增加缓存
   - 如需扩容，建议按当前容量的 1.5 倍预留资源
"""
        return report

# 使用示例
test_data = [
    CapacityData(50, 100, 100, 30, 40, 0.001),
    CapacityData(100, 180, 150, 45, 48, 0.002),
    CapacityData(200, 320, 220, 62, 55, 0.005),
    CapacityData(300, 420, 350, 75, 62, 0.008),
    CapacityData(400, 480, 520, 88, 70, 0.015),  # 开始出现瓶颈
]

planner = CapacityPlanner(test_data)
print(planner.generate_capacity_report())

# 计算扩容建议
scaling = planner.calculate_scaling_recommendation(target_tps=1000)
print(f"建议增加 {scaling['recommended_servers']} 台服务器以达到目标 TPS")
```

**验收标准：**
- [ ] analyze_current_capacity() 能正确计算最大容量
- [ ] predict_bottleneck() 能预测性能拐点
- [ ] calculate_scaling_recommendation() 能给出扩容建议
- [ ] generate_capacity_report() 能生成完整报告
- [ ] 分析结果合理，有实际参考价值

### 综合练习（17-20）

#### 练习17：完整性能测试流程

**场景说明：**
你需要实现一个端到端的自动化性能测试流程，从环境检查到报告生成，覆盖完整的性能测试生命周期。

**具体需求：**
1. 环境检查（服务可用性、依赖服务）
2. 测试数据准备
3. 启动资源监控
4. 执行性能测试
5. 收集测试数据
6. 停止监控
7. 数据分析
8. 生成报告
9. 清理测试数据
10. 发送通知

**使用示例：**
```python
import subprocess
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class PerformanceTestPipeline:
    """完整性能测试流程"""

    def __init__(self, config: dict):
        self.config = config
        self.results = {}
        self.log_file = open("perf_test.log", "w")

    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        self.log_file.write(log_line + "\n")

    def check_environment(self):
        """步骤1: 环境检查"""
        self.log("步骤1: 检查环境...")

        # 检查目标服务可用性
        try:
            response = requests.get(self.config["target_url"], timeout=10)
            if response.status_code != 200:
                raise Exception(f"目标服务返回 {response.status_code}")
            self.log("目标服务可用")
        except Exception as e:
            self.log(f"错误: 目标服务不可用 - {e}")
            return False

        # 检查依赖服务
        for service in self.config.get("dependencies", []):
            try:
                requests.get(service["url"], timeout=5)
                self.log(f"依赖服务 {service['name']} 可用")
            except:
                self.log(f"警告: 依赖服务 {service['name']} 不可用")

        return True

    def prepare_test_data(self):
        """步骤2: 准备测试数据"""
        self.log("步骤2: 准备测试数据...")
        # 调用数据准备脚本或 API
        # ...
        self.log("测试数据准备完成")
        return True

    def start_monitoring(self):
        """步骤3: 启动监控"""
        self.log("步骤3: 启动资源监控...")
        # 启动监控进程
        self.monitor_process = subprocess.Popen(
            ["python", "monitor.py"],
            stdout=subprocess.PIPE
        )
        self.log("监控已启动")
        return True

    def run_performance_test(self):
        """步骤4: 执行性能测试"""
        self.log("步骤4: 执行性能测试...")
        # 运行 Locust 压测
        cmd = [
            "locust", "-f", self.config["locust_file"],
            "--headless", "-u", str(self.config["users"]),
            "-r", str(self.config["spawn_rate"]),
            "-t", self.config["duration"],
            "--host", self.config["target_url"]
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.results["locust_output"] = result.stdout
        self.log("性能测试执行完成")
        return True

    def collect_results(self):
        """步骤5: 收集测试数据"""
        self.log("步骤5: 收集测试数据...")
        # 收集 Locust 统计数据
        # 收集监控数据
        # ...
        self.log("测试数据收集完成")
        return True

    def stop_monitoring(self):
        """步骤6: 停止监控"""
        self.log("步骤6: 停止监控...")
        if hasattr(self, 'monitor_process'):
            self.monitor_process.terminate()
        self.log("监控已停止")
        return True

    def analyze_results(self):
        """步骤7: 数据分析"""
        self.log("步骤7: 分析测试数据...")
        # 使用 PerformanceAnalyzer 分析数据
        # ...
        self.results["analysis"] = {"status": "completed"}
        self.log("数据分析完成")
        return True

    def generate_report(self):
        """步骤8: 生成报告"""
        self.log("步骤8: 生成测试报告...")
        # 使用 PerformanceReport 生成报告
        # ...
        self.log("报告已生成: performance_report.md")
        return True

    def cleanup(self):
        """步骤9: 清理测试数据"""
        self.log("步骤9: 清理测试数据...")
        # 清理测试产生的临时数据
        # ...
        self.log("测试数据清理完成")
        return True

    def send_notification(self):
        """步骤10: 发送通知"""
        self.log("步骤10: 发送通知...")

        if not self.config.get("notification"):
            return True

        # 发送邮件通知
        msg = MIMEText(f"""
性能测试已完成。

测试结果: {'通过' if self.results.get('passed') else '未通过'}
详细报告请查看: performance_report.md
        """)

        msg['Subject'] = '性能测试报告'
        msg['From'] = self.config["notification"]["from"]
        msg['To'] = self.config["notification"]["to"]

        # smtp = smtplib.SMTP('smtp.example.com')
        # smtp.send_message(msg)
        self.log("通知已发送")
        return True

    def run(self):
        """执行完整流程"""
        self.log("=" * 50)
        self.log("开始执行性能测试流程")
        self.log("=" * 50)

        steps = [
            ("环境检查", self.check_environment),
            ("准备测试数据", self.prepare_test_data),
            ("启动监控", self.start_monitoring),
            ("执行性能测试", self.run_performance_test),
            ("收集测试数据", self.collect_results),
            ("停止监控", self.stop_monitoring),
            ("数据分析", self.analyze_results),
            ("生成报告", self.generate_report),
            ("清理数据", self.cleanup),
            ("发送通知", self.send_notification),
        ]

        for step_name, step_func in steps:
            try:
                if not step_func():
                    self.log(f"流程在 '{step_name}' 步骤失败")
                    return False
            except Exception as e:
                self.log(f"步骤 '{step_name}' 执行出错: {e}")
                return False

        self.log("=" * 50)
        self.log("性能测试流程执行完成")
        self.log("=" * 50)
        self.log_file.close()
        return True

# 使用示例
config = {
    "target_url": "http://localhost:8000",
    "locust_file": "locustfile.py",
    "users": 100,
    "spawn_rate": 10,
    "duration": "5m",
    "dependencies": [
        {"name": "MySQL", "url": "http://localhost:3306"},
        {"name": "Redis", "url": "http://localhost:6379"}
    ],
    "notification": {
        "from": "test@example.com",
        "to": "team@example.com"
    }
}

pipeline = PerformanceTestPipeline(config)
pipeline.run()
```

**验收标准：**
- [ ] 10 个步骤都能正确执行
- [ ] 环境检查能检测服务可用性
- [ ] 能启动和停止监控
- [ ] 能执行 Locust 压测
- [ ] 能生成测试报告
- [ ] 有完善的错误处理和日志记录

#### 练习18：性能问题诊断案例

**场景说明：**
某电商系统在大促期间出现性能问题。你需要根据症状分析问题原因，设计排查方案，并提出优化建议。

**具体需求：**
1. 分析可能的瓶颈原因
2. 设计排查步骤
3. 提出优化方案
4. 制定验证计划

**使用示例：**
```
问题描述：
某电商系统在大促期间出现性能问题

症状：
- 首页加载时间从 500ms 上升到 5000ms
- 数据库 CPU 使用率 95%
- 应用服务器 CPU 使用率 60%
- 错误率从 0.1% 上升到 10%
- 缓存命中率从 85% 下降到 30%
```

```python
class PerformanceDiagnosis:
    """性能问题诊断"""

    def __init__(self, symptoms: dict):
        self.symptoms = symptoms
        self.diagnosis = []

    def analyze_bottleneck(self):
        """分析瓶颈原因"""
        analysis = []

        # 分析数据库 CPU 高
        if self.symptoms.get("db_cpu", 0) > 90:
            analysis.append({
                "type": "数据库瓶颈",
                "evidence": f"数据库 CPU 使用率 {self.symptoms['db_cpu']}%",
                "possible_causes": [
                    "慢查询导致 CPU 飙升",
                    "缺少索引导致全表扫描",
                    "连接池不足导致等待"
                ]
            })

        # 分析响应时间
        if self.symptoms.get("response_time", 0) > 1000:
            analysis.append({
                "type": "响应时间过长",
                "evidence": f"响应时间 {self.symptoms['response_time']}ms",
                "possible_causes": [
                    "数据库查询慢",
                    "缓存失效导致直接查库",
                    "网络延迟"
                ]
            })

        # 分析错误率
        if self.symptoms.get("error_rate", 0) > 0.01:
            analysis.append({
                "type": "高错误率",
                "evidence": f"错误率 {self.symptoms['error_rate'] * 100:.1f}%",
                "possible_causes": [
                    "服务超时",
                    "数据库连接耗尽",
                    "内存溢出"
                ]
            })

        # 分析缓存命中率
        if self.symptoms.get("cache_hit_rate", 100) < 50:
            analysis.append({
                "type": "缓存效率低",
                "evidence": f"缓存命中率 {self.symptoms['cache_hit_rate']}%",
                "possible_causes": [
                    "缓存过期策略不当",
                    "缓存容量不足",
                    "热点数据未缓存"
                ]
            })

        self.diagnosis = analysis
        return analysis

    def design_investigation_steps(self):
        """设计排查步骤"""
        steps = [
            {
                "step": 1,
                "action": "检查数据库慢查询日志",
                "command": "SHOW FULL PROCESSLIST; SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;",
                "expected": "找到执行时间长的 SQL 语句"
            },
            {
                "step": 2,
                "action": "检查数据库连接数",
                "command": "SHOW STATUS LIKE 'Threads_connected'; SHOW VARIABLES LIKE 'max_connections';",
                "expected": "确认是否连接池耗尽"
            },
            {
                "step": 3,
                "action": "检查 Redis 缓存状态",
                "command": "redis-cli info stats | grep keyspace",
                "expected": "确认缓存容量和命中率"
            },
            {
                "step": 4,
                "action": "分析应用日志",
                "command": "grep -i 'error\\|exception\\|timeout' /var/log/app.log | tail -100",
                "expected": "找到错误和异常信息"
            },
            {
                "step": 5,
                "action": "检查 JVM 状态（如果是 Java 应用）",
                "command": "jstat -gc <pid> 1000 10",
                "expected": "确认是否有频繁 GC"
            }
        ]
        return steps

    def propose_optimization(self):
        """提出优化方案"""
        optimizations = []

        for issue in self.diagnosis:
            if issue["type"] == "数据库瓶颈":
                optimizations.extend([
                    {
                        "priority": "P0",
                        "action": "添加缺失索引",
                        "detail": "分析慢查询日志，为高频查询添加索引",
                        "expected_improvement": "查询性能提升 50%-80%"
                    },
                    {
                        "priority": "P0",
                        "action": "优化热点 SQL",
                        "detail": "重写复杂查询，拆分大查询",
                        "expected_improvement": "数据库 CPU 降低 30%"
                    },
                    {
                        "priority": "P1",
                        "action": "增加数据库连接池",
                        "detail": "将连接池从 50 增加到 100",
                        "expected_improvement": "减少连接等待时间"
                    }
                ])

            if issue["type"] == "缓存效率低":
                optimizations.extend([
                    {
                        "priority": "P0",
                        "action": "增加缓存容量",
                        "detail": "将 Redis 内存从 2GB 增加到 8GB",
                        "expected_improvement": "缓存命中率提升到 80%"
                    },
                    {
                        "priority": "P1",
                        "action": "优化缓存策略",
                        "detail": "对热点数据设置更长的过期时间",
                        "expected_improvement": "减少缓存穿透"
                    }
                ])

        return optimizations

    def create_verification_plan(self):
        """制定验证计划"""
        return {
            "steps": [
                "1. 在测试环境复现问题",
                "2. 实施优化方案",
                "3. 使用相同压测参数重新测试",
                "4. 对比优化前后的指标"
            ],
            "success_criteria": [
                "响应时间 < 500ms",
                "错误率 < 0.1%",
                "数据库 CPU < 70%",
                "缓存命中率 > 80%"
            ]
        }

# 使用示例
symptoms = {
    "response_time": 5000,  # ms
    "db_cpu": 95,           # %
    "app_cpu": 60,          # %
    "error_rate": 0.10,     # 10%
    "cache_hit_rate": 30    # %
}

diagnosis = PerformanceDiagnosis(symptoms)
print("=== 瓶颈分析 ===")
for issue in diagnosis.analyze_bottleneck():
    print(f"- {issue['type']}: {issue['evidence']}")

print("\n=== 排查步骤 ===")
for step in diagnosis.design_investigation_steps():
    print(f"{step['step']}. {step['action']}")

print("\n=== 优化方案 ===")
for opt in diagnosis.propose_optimization():
    print(f"[{opt['priority']}] {opt['action']}: {opt['expected_improvement']}")
```

**验收标准：**
- [ ] 能正确识别数据库为主要瓶颈
- [ ] 能分析出至少 3 个可能原因
- [ ] 排查步骤具体可执行
- [ ] 优化方案有优先级和预期效果
- [ ] 验证计划包含成功标准

#### 练习19：性能测试平台设计

**场景说明：**
你需要设计一个企业级性能测试平台的核心架构，支持测试配置管理、执行、监控、分析和报告生成等功能。
**具体需求:**
1. 设计性能测试平台的核心模块
2. 实现配置管理、测试执行、监控、分析、报告等核心功能
3. 支持测试调度和结果对比
4. 模块间解耦，便于扩展
**使用示例:**
```python
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime
import json

@dataclass
class TestConfig:
    """测试配置"""
    name: str
    target_url: str
    users: int
    spawn_rate: int
    duration: str
    thresholds: Dict[str, float]

class ConfigManager:
    """配置管理器"""

    def __init__(self):
        self.configs: Dict[str, TestConfig] = {}

    def load_config(self, file_path: str) -> TestConfig:
        """从文件加载配置"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        config = TestConfig(**data)
        self.configs[config.name] = config
        return config

    def save_config(self, config: TestConfig, file_path: str):
        """保存配置到文件"""
        with open(file_path, 'w') as f:
            json.dump(config.__dict__, f, indent=2)

    def get_config(self, name: str) -> Optional[TestConfig]:
        """获取配置"""
        return self.configs.get(name)

class TestExecutor:
    """测试执行器"""

    def __init__(self):
        self.current_test = None
        self.test_history: list = []

    def execute(self, config: TestConfig) -> Dict[str, Any]:
        """执行测试"""
        self.current_test = {
            "config": config,
            "start_time": datetime.now(),
            "status": "running"
        }

        # 模拟执行测试
        # 实际应调用 Locust API
        results = {
            "total_requests": 10000,
            "total_failures": 50,
            "avg_response_time": 250,
            "rps": 150.5
        }

        self.current_test["end_time"] = datetime.now()
        self.current_test["results"] = results
        self.current_test["status"] = "completed"

        self.test_history.append(self.current_test)
        return results

    def stop_current_test(self):
        """停止当前测试"""
        if self.current_test:
            self.current_test["status"] = "stopped"

class ResourceMonitor:
    """资源监控器"""

    def __init__(self):
        self.metrics: list = []
        self.monitoring = False

    def start(self, interval: int = 1):
        """开始监控"""
        self.monitoring = True
        # 启动监控线程

    def stop(self):
        """停止监控"""
        self.monitoring = False

    def get_metrics(self) -> list:
        """获取监控数据"""
        return self.metrics

class PerformanceAnalyzer:
    """性能分析器"""

    def analyze(self, test_results: Dict, metrics: list) -> Dict[str, Any]:
        """分析测试结果"""
        return {
            "passed": test_results["total_failures"] / test_results["total_requests"] < 0.01,
            "bottlenecks": ["CPU 使用率偏高"] if sum(m["cpu"] for m in metrics) / len(metrics) > 80 else [],
            "recommendations": ["考虑增加服务器资源"] if sum(m["cpu"] for m in metrics) / len(metrics) > 80 else []
        }

class ReportGenerator:
    """报告生成器"""

    def generate(self, test_config: TestConfig, results: Dict, analysis: Dict) -> str:
        """生成测试报告"""
        report = f"""
# 性能测试报告

## 测试配置
- 测试名称: {test_config.name}
- 目标地址: {test_config.target_url}
- 并发用户: {test_config.users}
- 测试时长: {test_config.duration}

## 测试结果
- 总请求数: {results['total_requests']}
- 失败数: {results['total_failures']}
- 平均响应时间: {results['avg_response_time']}ms
- RPS: {results['rps']}

## 分析结论
- 测试{'通过' if analysis['passed'] else '未通过'}
- 瓶颈: {', '.join(analysis['bottlenecks']) if analysis['bottlenecks'] else '无'}
- 建议: {', '.join(analysis['recommendations']) if analysis['recommendations'] else '无'}
"""
        return report

class PerformanceTestPlatform:
    """性能测试平台"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.test_executor = TestExecutor()
        self.monitor = ResourceMonitor()
        self.analyzer = PerformanceAnalyzer()
        self.reporter = ReportGenerator()

    def run_test(self, config: TestConfig) -> str:
        """执行测试"""
        # 开始监控
        self.monitor.start()

        # 执行测试
        results = self.test_executor.execute(config)

        # 停止监控
        self.monitor.stop()

        # 获取监控数据
        metrics = self.monitor.get_metrics()

        # 分析结果
        analysis = self.analyzer.analyze(results, metrics)

        # 生成报告
        report = self.reporter.generate(config, results, analysis)

        return report

    def schedule_test(self, config: TestConfig, schedule: str):
        """定时测试"""
        # 使用 APScheduler 或类似库实现定时调度
        pass

    def compare_results(self, test_id1: str, test_id2: str) -> Dict:
        """结果对比"""
        # 获取两次测试结果并对比
        pass

# 使用示例
platform = PerformanceTestPlatform()

config = TestConfig(
    name="API冒烟测试",
    target_url="http://localhost:8000",
    users=10,
    spawn_rate=5,
    duration="1m",
    thresholds={"error_rate": 0.01, "response_time": 500}
)

report = platform.run_test(config)
print(report)
```
**验收标准:**
- [ ] 平台架构设计合理，模块职责清晰
- [ ] ConfigManager 能加载和保存配置
- [ ] TestExecutor 能执行测试并记录历史
- [ ] ResourceMonitor 能启动和停止监控
- [ ] PerformanceAnalyzer 能分析结果
- [ ] ReportGenerator 能生成格式化报告
- [ ] 各模块能协同工作完成完整测试流程

#### 练习20：性能优化实践

**场景说明:**
在性能测试中发现系统瓶颈后，需要实施具体的优化措施并验证效果。选择一个优化场景进行实践。
**具体需求:**
选择以下场景之一进行优化实践：
- 场景 A：数据库优化（添加索引、优化慢查询、调整连接池）
- 场景 B：缓存优化（添加 Redis 缓存、优化缓存策略、实现缓存预热）
- 场景 C：代码优化（优化热点代码、减少数据库查询、异步处理)

验证要求：
1. 记录优化前性能基线
2. 实施优化措施
3. 进行优化后性能测试
4. 生成对比分析报告
5. 量化性能提升百分比

**使用示例:**
```python
import time
from dataclasses import dataclass

@dataclass
class PerformanceBaseline:
    """性能基线"""
    avg_response_time: float
    p99_response_time: float
    rps: float
    error_rate: float
    cpu_usage: float
    memory_usage: float

class DatabaseOptimizer:
    """数据库优化器 - 场景 A"""

    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.baseline: PerformanceBaseline = None
        self.optimized: PerformanceBaseline = None

    def record_baseline(self, test_results: dict) -> PerformanceBaseline:
        """记录优化前基线"""
        self.baseline = PerformanceBaseline(
            avg_response_time=test_results["avg_response_time"],
            p99_response_time=test_results["p99_response_time"],
            rps=test_results["rps"],
            error_rate=test_results["error_rate"],
            cpu_usage=test_results["cpu_usage"],
            memory_usage=test_results["memory_usage"]
        )
        return self.baseline

    def add_index(self, table: str, columns: list, index_name: str):
        """添加索引"""
        import pymysql
        conn = pymysql.connect(**self.db_config)
        cursor = conn.cursor()

        index_sql = f"CREATE INDEX {index_name} ON {table}({', '.join(columns)})"
        cursor.execute(index_sql)
        conn.commit()
        conn.close()
        print(f"索引 {index_name} 已创建")

    def optimize_query(self, slow_query: str, optimized_query: str):
        """优化慢查询"""
        # 记录优化前后的查询
        print(f"优化前: {slow_query}")
        print(f"优化后: {optimized_query}")

    def adjust_connection_pool(self, new_pool_size: int):
        """调整连接池配置"""
        # 修改应用配置或数据库配置
        print(f"连接池大小已调整为 {new_pool_size}")

    def record_optimized(self, test_results: dict) -> PerformanceBaseline:
        """记录优化后结果"""
        self.optimized = PerformanceBaseline(
            avg_response_time=test_results["avg_response_time"],
            p99_response_time=test_results["p99_response_time"],
            rps=test_results["rps"],
            error_rate=test_results["error_rate"],
            cpu_usage=test_results["cpu_usage"],
            memory_usage=test_results["memory_usage"]
        )
        return self.optimized

    def generate_comparison_report(self) -> str:
        """生成对比报告"""
        if not self.baseline or not self.optimized:
            return "缺少基线或优化后数据"

        def calc_improvement(baseline_val, optimized_val, lower_is_better=True):
            if lower_is_better:
                return (baseline_val - optimized_val) / baseline_val * 100
            return (optimized_val - baseline_val) / baseline_val * 100

        report = f"""
# 数据库优化对比报告

## 基线数据
- 平均响应时间: {self.baseline.avg_response_time:.2f}ms
- P99 响应时间: {self.baseline.p99_response_time:.2f}ms
- RPS: {self.baseline.rps:.2f}
- 错误率: {self.baseline.error_rate * 100:.2f}%
- CPU 使用率: {self.baseline.cpu_usage:.1f}%
- 内存使用率: {self.baseline.memory_usage:.1f}%

## 优化后数据
- 平均响应时间: {self.optimized.avg_response_time:.2f}ms
- P99 响应时间: {self.optimized.p99_response_time:.2f}ms
- RPS: {self.optimized.rps:.2f}
- 错误率: {self.optimized.error_rate * 100:.2f}%
- CPU 使用率: {self.optimized.cpu_usage:.1f}%
- 内存使用率: {self.optimized.memory_usage:.1f}%

## 性能提升
- 响应时间改善: {calc_improvement(self.baseline.avg_response_time, self.optimized.avg_response_time):.1f}%
- RPS 提升: {calc_improvement(self.baseline.rps, self.optimized.rps, lower_is_better=False):.1f}%
- 错误率降低: {calc_improvement(self.baseline.error_rate, self.optimized.error_rate):.1f}%
- CPU 使用率降低: {calc_improvement(self.baseline.cpu_usage, self.optimized.cpu_usage):.1f}%

## 结论
优化{'成功' if self.optimized.avg_response_time < self.baseline.avg_response_time else '失败'}，响应时间提升了 {calc_improvement(self.baseline.avg_response_time, self.optimized.avg_response_time):.1f}%
"""
        return report

# 使用示例 - 数据库优化场景
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "test_db"
}

optimizer = DatabaseOptimizer(db_config)

# 1. 记录基线
baseline = optimizer.record_baseline({
    "avg_response_time": 850,
    "p99_response_time": 2500,
    "rps": 120,
    "error_rate": 0.02,
    "cpu_usage": 85,
    "memory_usage": 60
})

# 2. 实施优化
optimizer.add_index("orders", ["user_id", "created_at"], "idx_orders_user_date")
optimizer.optimize_query(
    "SELECT * FROM orders WHERE user_id = ?",
    "SELECT * FROM orders USE INDEX (idx_orders_user_date) WHERE user_id = ? LIMIT 100"
)
optimizer.adjust_connection_pool(100)

# 3. 记录优化后结果
optimized = optimizer.record_optimized({
    "avg_response_time": 320,
    "p99_response_time": 800,
    "rps": 280,
    "error_rate": 0.005,
    "cpu_usage": 55,
    "memory_usage": 58
})

# 4. 生成对比报告
print(optimizer.generate_comparison_report())
```
**验收标准:**
- [ ] 能记录优化前性能基线
- [ ] 能实施具体的优化措施（至少 2 项）
- [ ] 能记录优化后性能数据
- [ ] 能生成对比分析报告
- [ ] 能量化性能提升百分比
- [ ] 报告包含基线、优化后、提升百分比三部分

---

## 五、本周小结

1. **分布式压测**：突破单机限制
2. **监控**：性能分析的基础
3. **瓶颈分析**：定位问题根源
4. **报告**：专业输出能力

### 下周预告

第12-13周学习 AI 与大模型测试。
