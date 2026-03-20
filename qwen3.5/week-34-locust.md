# 第 34 周 - Locust

## 学习目标
掌握 Locust 压测工具，能够编写负载测试脚本。

---

## 知识点清单

### 1. 安装运行
**掌握程度**: locust 命令、Web UI

**练习资源**:
- [Locust 官方文档](https://locust.io/)

---

### 2. 脚本编写
**掌握程度**: HttpUser、task

**练习任务**:
- 编写压测脚本

---

### 3. 用户行为
**掌握程度**: 模拟、等待、权重

**练习任务**:
- 模拟真实用户行为

---

### 4. 分布式
**掌握程度**: Master/Worker 模式

**练习任务**:
- 分布式执行

---

### 5. 自定义指标
**掌握程度**: events、自定义统计

**练习任务**:
- 扩展指标

---

### 6. API 测试
**掌握程度**: 负载测试、压力测试

**练习任务**:
- 执行压测

---

### 7. 结果分析
**掌握程度**: 图表、导出

**练习任务**:
- 分析结果

---

### 8. 集成 CI
**掌握程度**: 自动执行、阈值检查

**练习任务**:
- 集成 CI

---

## 本周练习任务

### 必做任务

1. **电商网站负载测试**
```python
from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def browse_products(self):
        self.client.get("/products")

    @task(1)
    def add_to_cart(self):
        self.client.post("/cart/add", json={"product_id": 1})

# 执行:
# locust -f locustfile.py --headless -u 1000 -r 100 -t 5m
```

2. **分布式压测**
```bash
# Master 节点
locust -f locustfile.py --master

# Worker 节点
locust -f locustfile.py --worker
```

3. **性能分析报告**
```markdown
# 包含:
# - 测试场景
# - 并发用户数
# - 测试结果
# - 瓶颈分析
# - 优化建议
```

---

## 验收标准

- [ ] 能模拟 1000+ 并发用户
- [ ] 报告包含瓶颈分析
- [ ] 能提出优化建议

---

## 周总结模板

```markdown
## 第 34 周总结

### 学习内容
- 掌握了 Locust
- 能编写压测脚本
- 能分析结果

### 作品
- 负载测试脚本
- 性能分析报告

### 遇到的问题
- ...

### 下周改进
- ...
```
