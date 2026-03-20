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

### 练习1：分布式压测

```bash
# 在两台机器上配置 Master-Worker
# 模拟 1000 并发用户
```

### 练习2：瓶颈分析

```python
# 给定性能测试数据和监控指标
# 分析瓶颈并给出优化建议
```

### 练习3：报告编写

```python
# 编写完整的性能测试报告
# 包含：概要、结果、分析、建议
```

---

## 五、本周小结

1. **分布式压测**：突破单机限制
2. **监控**：性能分析的基础
3. **瓶颈分析**：定位问题根源
4. **报告**：专业输出能力

### 下周预告

第12-13周学习 AI 与大模型测试。
