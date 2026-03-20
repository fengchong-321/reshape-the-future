# 第 12 周 - 阶段一验收项目

## 学习目标
综合运用阶段一所学知识，为一个开源 Python 库编写完整的测试套件，验证学习成果。

---

## 项目任务

### 选择一个开源项目

**要求**:
- GitHub 上 100-500 star 的 Python 库
- 有一定用户量但测试覆盖不足
- 项目活跃（最近有更新）
- 有贡献指南（CONTRIBUTING.md）

**寻找途径**:
- GitHub Explore: https://github.com/explore
- Good First Issue: https://goodfirstissues.com/
- First Timers Only: https://www.firsttimersonly.com/

---

## 项目实施步骤

### Step 1: 分析现有测试覆盖情况
```bash
# 1. Fork 项目
# 2. 克隆到本地
git clone https://github.com/yourname/project.git
cd project

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行现有测试
pytest --cov=src

# 5. 分析覆盖率报告
# 找出未覆盖的模块和函数
```

---

### Step 2: 制定测试计划
```markdown
# 测试计划

## 目标模块
- 模块 A: 覆盖率从 50% 提升到 80%
- 模块 B: 添加缺失的边界测试
- 模块 C: 添加异常场景测试

## 时间安排
- Day 1-2: 阅读源码，理解功能
- Day 3-5: 编写测试用例
- Day 6: 运行测试，修复问题
- Day 7: 提交 PR

## 验收标准
- 新增测试用例 50+
- 总体覆盖率提升 10%+
- PR 被合并
```

---

### Step 3: 编写测试用例
```python
# 示例：为一个工具函数编写测试
import pytest
from module import utility_function

class TestUtilityFunction:
    """utility_function 的测试类"""

    def test_normal_case(self):
        """测试正常情况"""
        result = utility_function('input')
        assert result == 'expected'

    def test_empty_input(self):
        """测试空输入"""
        result = utility_function('')
        assert result == ''

    def test_invalid_input(self):
        """测试无效输入"""
        with pytest.raises(ValueError):
            utility_function(None)

    @pytest.mark.parametrize('input,expected', [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    ])
    def test_multiple_cases(self, input, expected):
        """参数化测试"""
        result = utility_function(input)
        assert result == expected
```

---

### Step 4: 提交 PR
```markdown
# PR 模板

## Description
添加 XX 模块的测试用例，提升覆盖率从 X% 到 Y%

## Changes
- 新增测试文件：tests/test_module.py
- 新增测试用例：50 个
- 覆盖率提升：10%

## Checklist
- [ ] 测试全部通过
- [ ] 代码符合项目规范
- [ ] 已运行 lint 检查
- [ ] 已更新文档（如有需要）

## Related Issue
Fixes #123
```

---

## 知识点回顾

### 阶段一核心知识点

#### Python 基础（第 1-3 周）
- [ ] 数据类型和流程控制
- [ ] 函数和模块
- [ ] 面向对象编程
- [ ] 装饰器、生成器、上下文管理器

#### Git（第 4 周）
- [ ] 基础命令
- [ ] 分支管理
- [ ] 冲突解决
- [ ] 远程协作

#### Linux（第 5-6 周）
- [ ] 文件操作
- [ ] 文本处理
- [ ] Shell 脚本
- [ ] 系统监控

#### MySQL（第 7-8 周）
- [ ] SQL 基础
- [ ] 连接查询
- [ ] 索引和事务
- [ ] Python 连接数据库

#### 测试理论和 pytest（第 9-11 周）
- [ ] 测试用例设计
- [ ] pytest 基础
- [ ] pytest 进阶
- [ ] mock 测试
- [ ] 覆盖率

---

## 验收标准

完成本周学习后，你应该：

- [ ] PR 被合并（或至少有 maintainer review）
- [ ] 写一篇博客记录整个过程
- [ ] 阶段一总结：技术栈掌握程度自评
- [ ] GitHub 有完整的提交历史
- [ ] 能独立为项目编写测试

---

## 博客写作指南

### 文章结构
```markdown
# 标题：我为开源项目 XX 贡献了测试代码

## 背景
- 为什么选择这个项目
- 项目的测试覆盖情况

## 过程
- 环境搭建
- 源码阅读
- 测试编写
- 遇到的问题

## 结果
- PR 链接
- 覆盖率提升
- 学到的东西

## 总结
- 经验教训
- 给新手的建议
```

---

## 阶段一自评表

### 技能掌握程度（1-5 分）

| 技能 | 自评 | 证明 |
|------|------|------|
| Python 基础 | /5 | 能独立完成练习 |
| Python 进阶 | /5 | 理解装饰器、生成器 |
| Git | /5 | 能解决冲突、提交 PR |
| Linux | /5 | 能编写 Shell 脚本 |
| MySQL | /5 | 能编写复杂 SQL |
| pytest | /5 | 能编写完整测试套件 |
| 测试理论 | /5 | 能设计测试用例 |

### 作品清单
- [ ] GitHub 仓库（python-practice）
- [ ] 技术博客（至少 5 篇）
- [ ] 开源贡献 PR
- [ ] Shell 脚本集
- [ ] SQL 练习记录

---

## 每日学习检查清单

### Day 1-2: 寻找项目 + 环境搭建
- [ ] 寻找目标项目
- [ ] Fork 项目
- [ ] 搭建开发环境
- [ ] 阅读源码

### Day 3-5: 编写测试
- [ ] 制定测试计划
- [ ] 编写测试用例（50+）
- [ ] 运行测试
- [ ] 修复问题

### Day 6: 提交 PR
- [ ] 检查代码规范
- [ ] 撰写 PR 描述
- [ ] 提交 PR
- [ ] 跟进反馈

### Day 7: 总结
- [ ] 写博客
- [ ] 阶段一总结
- [ ] 制定阶段二计划

---

## 阶段一总结模板

```markdown
# 阶段一学习总结

## 学习概况
- 学习时间：12 周
- 每日投入：8 小时
- 完成项目：X 个
- 代码提交：X 次

## 技能提升
### Python
- 从零基础到能...
- 掌握了...

### Git
- 能熟练使用...

### Linux
- 能编写...

### MySQL
- 能编写...

### 测试
- 能独立...

## 作品展示
1. [GitHub 仓库](链接)
2. [技术博客](链接)
3. [开源 PR](链接)

## 遇到的挑战
- 挑战 1：... 解决方案：...
- 挑战 2：... 解决方案：...

## 阶段二计划
- 学习目标：...
- 重点关注：...
```

---

## 下一步

阶段一完成后，进入**阶段二：技术深化**（第 13-24 周）

学习内容包括：
- UI 自动化测试（Playwright）
- 接口自动化测试
- Web 开发基础（React + FastAPI）
- DevOps（Docker + K8s + CI/CD）

准备好继续前进吗？
