# 第13周：Prompt 工程与测试

## 本周目标

掌握 Prompt 工程技术，能够设计、优化和测试 LLM 的提示词，建立 Prompt 测试体系。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Prompt 设计原则 | 清晰性、具体性、结构化 | ⭐⭐⭐⭐⭐ |
| Prompt 技术 | Few-shot、CoT、ReAct | ⭐⭐⭐⭐⭐ |
| Prompt 优化 | 迭代优化、A/B 测试 | ⭐⭐⭐⭐⭐ |
| Prompt 测试 | 边界测试、回归测试 | ⭐⭐⭐⭐⭐ |
| Prompt 管理 | 版本控制、模板管理 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 Prompt 设计原则

```python
# ============================================
# Prompt 设计核心原则
# ============================================
"""
1. 清晰性（Clarity）
   - 明确表达意图
   - 避免歧义

2. 具体性（Specificity）
   - 提供具体示例
   - 明确输出格式

3. 结构化（Structure）
   - 使用分隔符
   - 分步骤指导

4. 上下文（Context）
   - 提供必要背景
   - 设定角色和约束
"""

# ============================================
# 好的 Prompt 示例
# ============================================
GOOD_PROMPT = """
你是一个专业的软件测试工程师。

任务：为以下功能设计测试用例。

功能描述：
{feature_description}

要求：
1. 覆盖正常场景和边界场景
2. 每个测试用例包含：输入、预期输出、测试目的
3. 按优先级排序（P0-P3）
4. 使用 Markdown 表格格式输出

示例：
| 用例ID | 输入 | 预期输出 | 优先级 |
|--------|------|----------|--------|
| TC001 | 正常用户名 | 注册成功 | P0 |
"""

# ============================================
# 差的 Prompt 示例
# ============================================
BAD_PROMPT = "帮我写测试用例"
```

### 2.2 Prompt 技术

```python
# ============================================
# Zero-shot Prompting
# ============================================
ZERO_SHOT = """
将以下文本翻译成英文：
{text}
"""

# ============================================
# Few-shot Prompting
# ============================================
FEW_SHOT = """
以下是情感分析的示例：

文本：这个产品太棒了！
情感：正面

文本：服务很差，等了很久。
情感：负面

文本：{text}
情感：
"""

# ============================================
# Chain of Thought (CoT)
# ============================================
COT_PROMPT = """
请一步步思考解决以下问题：

问题：{question}

请按以下格式回答：
1. 理解问题：
2. 分析条件：
3. 推理过程：
4. 最终答案：
"""

# ============================================
# ReAct (Reasoning + Acting)
# ============================================
REACT_PROMPT = """
你是一个能够使用工具的智能助手。

可用工具：
- search(query): 搜索信息
- calculate(expression): 计算数学表达式
- get_weather(city): 获取天气

对于每个问题，请按以下格式思考和行动：

问题：{question}
思考：我需要...
行动：[工具名称]
行动输入：[工具参数]
观察：[工具返回结果]
思考：...
最终答案：...
"""
```

### 2.3 Prompt 模板管理

```python
# ============================================
# Prompt 模板类
# ============================================
from string import Template
from typing import Dict, Any
import json

class PromptTemplate:
    """Prompt 模板管理"""

    def __init__(self, template: str, variables: list = None):
        self.template = template
        self.variables = variables or self._extract_variables()

    def _extract_variables(self) -> list:
        """提取模板变量"""
        import re
        return re.findall(r'\{(\w+)\}', self.template)

    def format(self, **kwargs) -> str:
        """格式化模板"""
        return self.template.format(**kwargs)

    def validate(self, kwargs: dict) -> bool:
        """验证参数完整性"""
        return all(v in kwargs for v in self.variables)

# 使用
test_case_prompt = PromptTemplate("""
你是一个测试工程师，请为以下功能生成测试用例。

功能名称：{feature_name}
功能描述：{feature_description}
测试重点：{test_focus}

要求：
1. 生成至少 {min_cases} 个测试用例
2. 优先级分为 P0、P1、P2、P3
3. 使用表格格式输出
""")

prompt = test_case_prompt.format(
    feature_name="用户登录",
    feature_description="支持用户名密码和手机验证码登录",
    test_focus="安全性测试",
    min_cases=10
)
```

```python
# ============================================
# Prompt 版本管理
# ============================================
class PromptRegistry:
    """Prompt 版本注册表"""

    def __init__(self):
        self.prompts = {}

    def register(self, name: str, version: str, prompt: str):
        """注册 Prompt 版本"""
        if name not in self.prompts:
            self.prompts[name] = {}
        self.prompts[name][version] = prompt

    def get(self, name: str, version: str = "latest") -> str:
        """获取 Prompt"""
        if name not in self.prompts:
            raise ValueError(f"Prompt '{name}' not found")
        if version == "latest":
            version = sorted(self.prompts[name].keys())[-1]
        return self.prompts[name][version]

    def list_versions(self, name: str) -> list:
        """列出所有版本"""
        return list(self.prompts.get(name, {}).keys())

# 使用
registry = PromptRegistry()
registry.register("sentiment", "v1", "分析情感：{text}")
registry.register("sentiment", "v2", "请分析以下文本的情感倾向（正面/负面/中性）：{text}")

prompt = registry.get("sentiment", "v2")
```

### 2.4 Prompt 测试框架

```python
# ============================================
# Prompt 测试用例
# ============================================
import pytest
from dataclasses import dataclass

@dataclass
class PromptTestCase:
    """Prompt 测试用例"""
    name: str
    input_data: dict
    expected_contains: list = None  # 输出应包含的关键词
    expected_not_contains: list = None  # 输出不应包含的关键词
    expected_format: str = None  # 期望的输出格式
    evaluator: callable = None  # 自定义评估函数

class PromptTester:
    """Prompt 测试器"""

    def __init__(self, llm_client, prompt_template: str):
        self.llm = llm_client
        self.prompt_template = prompt_template

    def run_test(self, test_case: PromptTestCase) -> dict:
        """运行单个测试"""
        # 生成 Prompt
        prompt = self.prompt_template.format(**test_case.input_data)

        # 调用 LLM
        response = self.llm.generate(prompt)

        # 验证结果
        result = {
            "name": test_case.name,
            "passed": True,
            "response": response,
            "errors": []
        }

        # 检查应包含的关键词
        if test_case.expected_contains:
            for keyword in test_case.expected_contains:
                if keyword not in response:
                    result["passed"] = False
                    result["errors"].append(f"缺少关键词: {keyword}")

        # 检查不应包含的关键词
        if test_case.expected_not_contains:
            for keyword in test_case.expected_not_contains:
                if keyword in response:
                    result["passed"] = False
                    result["errors"].append(f"不应包含: {keyword}")

        # 自定义评估
        if test_case.evaluator:
            eval_result = test_case.evaluator(response)
            if not eval_result.get("passed", True):
                result["passed"] = False
                result["errors"].extend(eval_result.get("errors", []))

        return result

# 使用
def test_sentiment_prompt():
    tester = PromptTester(llm_client, FEW_SHOT)

    test_cases = [
        PromptTestCase(
            name="positive_sentiment",
            input_data={"text": "今天天气真好！"},
            expected_contains=["正面", "积极"]
        ),
        PromptTestCase(
            name="negative_sentiment",
            input_data={"text": "这服务太差了"},
            expected_contains=["负面", "消极"]
        )
    ]

    for tc in test_cases:
        result = tester.run_test(tc)
        assert result["passed"], result["errors"]
```

### 2.5 Prompt A/B 测试

```python
# ============================================
# Prompt A/B 测试
# ============================================
import statistics
from typing import List, Callable

class PromptABTest:
    """Prompt A/B 测试"""

    def __init__(self, llm_client):
        self.llm = llm_client
        self.results = {"A": [], "B": []}

    def run_comparison(
        self,
        prompt_a: str,
        prompt_b: str,
        inputs: List[dict],
        evaluator: Callable,
        runs: int = 3
    ):
        """运行对比测试"""
        for input_data in inputs:
            for _ in range(runs):
                # 测试 Prompt A
                response_a = self.llm.generate(prompt_a.format(**input_data))
                score_a = evaluator(response_a, input_data)
                self.results["A"].append(score_a)

                # 测试 Prompt B
                response_b = self.llm.generate(prompt_b.format(**input_data))
                score_b = evaluator(response_b, input_data)
                self.results["B"].append(score_b)

    def analyze(self) -> dict:
        """分析测试结果"""
        return {
            "A": {
                "mean": statistics.mean(self.results["A"]),
                "std": statistics.stdev(self.results["A"]) if len(self.results["A"]) > 1 else 0,
                "count": len(self.results["A"])
            },
            "B": {
                "mean": statistics.mean(self.results["B"]),
                "std": statistics.stdev(self.results["B"]) if len(self.results["B"]) > 1 else 0,
                "count": len(self.results["B"])
            }
        }

# 使用
def evaluator(response, input_data):
    """评估函数：返回 0-1 分数"""
    # 简单示例：检查是否包含预期答案
    expected = input_data.get("expected", "")
    return 1.0 if expected in response else 0.0

ab_test = PromptABTest(llm_client)
ab_test.run_comparison(
    prompt_a="分析情感：{text}",
    prompt_b="请判断以下文本是正面、负面还是中性：{text}",
    inputs=[
        {"text": "这个产品很好用", "expected": "正面"},
        {"text": "服务太差了", "expected": "负面"}
    ],
    evaluator=evaluator
)
print(ab_test.analyze())
```

### 2.6 Prompt 回归测试

```python
# ============================================
# Prompt 回归测试
# ============================================
import json
from pathlib import Path

class PromptRegressionTest:
    """Prompt 回归测试"""

    def __init__(self, baseline_dir: str = "./prompt_baselines"):
        self.baseline_dir = Path(baseline_dir)
        self.baseline_dir.mkdir(exist_ok=True)

    def save_baseline(self, name: str, prompt: str, inputs: list, outputs: list):
        """保存基线"""
        baseline = {
            "prompt": prompt,
            "inputs": inputs,
            "expected_outputs": outputs,
            "created_at": datetime.now().isoformat()
        }
        path = self.baseline_dir / f"{name}.json"
        with open(path, "w") as f:
            json.dump(baseline, f, ensure_ascii=False, indent=2)

    def load_baseline(self, name: str) -> dict:
        """加载基线"""
        path = self.baseline_dir / f"{name}.json"
        with open(path) as f:
            return json.load(f)

    def run_regression(self, name: str, llm_client, similarity_threshold: float = 0.8):
        """运行回归测试"""
        baseline = self.load_baseline(name)
        results = []

        for i, (input_data, expected) in enumerate(zip(
            baseline["inputs"],
            baseline["expected_outputs"]
        )):
            prompt = baseline["prompt"].format(**input_data)
            actual = llm_client.generate(prompt)

            # 计算相似度
            similarity = self._calculate_similarity(actual, expected)
            passed = similarity >= similarity_threshold

            results.append({
                "index": i,
                "passed": passed,
                "similarity": similarity,
                "expected": expected,
                "actual": actual
            })

        return results

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        # 使用简单的 Jaccard 相似度
        words1 = set(text1.split())
        words2 = set(text2.split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union)
```

---

## 三、学到什么程度

### 必须掌握
- [ ] Prompt 设计的四大原则
- [ ] Few-shot、CoT、ReAct 技术
- [ ] Prompt 模板管理
- [ ] Prompt 测试框架搭建
- [ ] A/B 测试和回归测试

### 应该了解
- [ ] Prompt 注入攻击防护
- [ ] 多模态 Prompt 设计
- [ ] Prompt 缓存策略
- [ ] 企业级 Prompt 管理平台

---

## 四、练习内容

### 基础练习（1-8）

#### 练习1：Prompt 设计原则实践

**场景说明：**
作为 AI 测试工程师，需要为团队的 Prompt 编写制定规范。

**具体需求：**
1. 对比好坏 Prompt 的差异
2. 编写符合设计原则的 Prompt
3. 验证 Prompt 的清晰性和具体性

**使用示例：**
```python
# 差的 Prompt
bad_prompt = "写测试用例"

# 好的 Prompt
good_prompt = """
你是一个资深测试工程师。
任务：为以下 API 接口设计测试用例。

接口信息：
- 名称：用户登录
- 方法：POST
- 路径：/api/login
- 参数：username, password

要求：
1. 覆盖正常场景和异常场景
2. 每个用例包含：用例名、输入、预期输出
3. 按优先级 P0-P3 分类
4. 使用 Markdown 表格格式
"""
```

**验收标准：**
- [ ] 识别至少 3 个差 Prompt 的问题
- [ ] 编写符合原则的 Prompt
- [ ] Prompt 输出结果符合预期

---

#### 练习2：Few-shot Prompting

**场景说明：**
需要让 LLM 学习特定的输出格式，使用 Few-shot 提供示例。

**具体需求：**
1. 设计 2-3 个示例
2. 构造 Few-shot Prompt
3. 测试新输入的输出格式

**使用示例：**
```python
few_shot_prompt = """
以下是测试用例生成的示例：

需求：用户登录功能
测试用例：
| ID | 步骤 | 预期结果 |
| TC001 | 输入正确的用户名和密码 | 登录成功 |
| TC002 | 输入错误的密码 | 提示密码错误 |
| TC003 | 不输入用户名 | 提示用户名必填 |

需求：用户注册功能
测试用例：
| ID | 步骤 | 预期结果 |
| TC001 | 输入有效信息 | 注册成功 |
| TC002 | 输入已存在的用户名 | 提示用户名已存在 |

需求：{requirement}
测试用例：
"""
```

**验收标准：**
- [ ] 示例设计合理
- [ ] 输出格式一致
- [ ] 新输入能正确泛化

---

#### 练习3：Chain of Thought

**场景说明：**
需要 LLM 进行复杂推理，使用 CoT 提高准确性。

**具体需求：**
1. 设计 CoT Prompt
2. 对比有无 CoT 的效果
3. 验证推理步骤的合理性

**使用示例：**
```python
cot_prompt = """
请一步步分析以下测试场景：

场景：一个电商网站的购物车功能

请按以下步骤分析：
1. 理解功能需求：
   - 购物车能做什么？
   - 有哪些边界情况？

2. 设计测试点：
   - 正常流程测试
   - 异常流程测试
   - 性能测试点

3. 列出测试用例：
   - 用表格形式输出
"""
```

**验收标准：**
- [ ] 推理步骤清晰
- [ ] 分析过程完整
- [ ] 结论合理

---

#### 练习4：Prompt 模板类实现

**场景说明：**
团队需要管理多个 Prompt 模板，实现模板管理类。

**具体需求：**
1. 实现 PromptTemplate 类
2. 支持变量提取和验证
3. 支持模板格式化

**使用示例：**
```python
template = PromptTemplate("""
角色：{role}
任务：{task}
要求：{requirements}
""")

# 验证变量
assert template.variables == ["role", "task", "requirements"]

# 格式化
prompt = template.format(
    role="测试工程师",
    task="设计登录测试用例",
    requirements="覆盖安全测试"
)
```

**验收标准：**
- [ ] 变量提取正确
- [ ] 格式化无错误
- [ ] 参数验证有效

---

#### 练习5：Prompt 版本管理

**场景说明：**
Prompt 需要不断迭代优化，建立版本管理机制。

**具体需求：**
1. 实现 PromptRegistry 类
2. 支持版本注册和获取
3. 支持 latest 版本

**使用示例：**
```python
registry = PromptRegistry()
registry.register("test_gen", "v1", "生成测试用例：{feature}")
registry.register("test_gen", "v2", "作为测试工程师，为{feature}生成测试用例")

# 获取最新版本
latest = registry.get("test_gen", "latest")
assert "测试工程师" in latest
```

**验收标准：**
- [ ] 版本注册成功
- [ ] latest 获取最新版本
- [ ] 版本列表正确

---

#### 练习6：Prompt 测试用例设计

**场景说明：**
为 Prompt 编写测试用例，确保输出符合预期。

**具体需求：**
1. 设计 PromptTestCase 数据类
2. 支持关键词检查
3. 支持自定义评估

**使用示例：**
```python
test_case = PromptTestCase(
    name="login_test_generation",
    input_data={"feature": "用户登录"},
    expected_contains=["TC001", "P0", "登录成功"],
    expected_not_contains=["我不知道", "无法回答"]
)
```

**验收标准：**
- [ ] 测试用例结构完整
- [ ] 关键词检查有效
- [ ] 支持多种验证方式

---

#### 练习7：Prompt 测试器实现

**场景说明：**
实现 PromptTester 类，自动化测试 Prompt 效果。

**具体需求：**
1. 实现 PromptTester 类
2. 支持批量测试
3. 生成测试报告

**使用示例：**
```python
tester = PromptTester(llm_client, prompt_template)
results = tester.run_tests([
    PromptTestCase(name="case1", input_data={"text": "..."}),
    PromptTestCase(name="case2", input_data={"text": "..."})
])

assert all(r["passed"] for r in results)
```

**验收标准：**
- [ ] 测试器实现完整
- [ ] 测试结果准确
- [ ] 错误信息清晰

---

#### 练习8：关键词验证测试

**场景说明：**
验证 LLM 输出是否包含期望的关键词。

**具体需求：**
1. 实现关键词包含检查
2. 实现关键词排除检查
3. 处理中英文混合情况

**使用示例：**
```python
def validate_output(response: str, expected: list, not_expected: list) -> dict:
    errors = []
    for kw in expected:
        if kw not in response:
            errors.append(f"缺少关键词: {kw}")
    for kw in not_expected:
        if kw in response:
            errors.append(f"不应包含: {kw}")
    return {"passed": len(errors) == 0, "errors": errors}
```

**验收标准：**
- [ ] 关键词检查准确
- [ ] 错误信息明确
- [ ] 支持中英文

---

### 进阶练习（9-16）

#### 练习9：A/B 测试实现

**场景说明：**
对比两个 Prompt 版本的效果，选择最优版本。

**具体需求：**
1. 实现 PromptABTest 类
2. 支持多次运行取平均
3. 生成对比报告

**验收标准：**
- [ ] A/B 测试逻辑正确
- [ ] 统计分析合理
- [ ] 报告清晰易读

---

#### 练习10：评估函数设计

**场景说明：**
设计 Prompt 输出的评估函数，量化评估质量。

**具体需求：**
1. 实现准确性评估
2. 实现格式评估
3. 实现完整性评估

**验收标准：**
- [ ] 评估维度全面
- [ ] 评分标准清晰
- [ ] 结果可量化

---

#### 练习11：回归测试基线

**场景说明：**
建立 Prompt 回归测试基线，确保修改后不影响效果。

**具体需求：**
1. 保存基线输出
2. 加载基线对比
3. 计算相似度

**验收标准：**
- [ ] 基线保存成功
- [ ] 相似度计算正确
- [ ] 回归报告清晰

---

#### 练习12：Prompt 注入测试

**场景说明：**
测试 Prompt 的安全性，防止注入攻击。

**具体需求：**
1. 设计注入攻击测试用例
2. 验证防护措施
3. 记录漏洞

**验收标准：**
- [ ] 覆盖常见注入模式
- [ ] 防护措施有效
- [ ] 安全报告完整

---

#### 练习13：多语言 Prompt 测试

**场景说明：**
测试 Prompt 在不同语言下的效果。

**具体需求：**
1. 设计中英文测试用例
2. 对比不同语言效果
3. 优化多语言支持

**验收标准：**
- [ ] 多语言测试通过
- [ ] 效果差异分析
- [ ] 优化建议合理

---

#### 练习14：长文本 Prompt 处理

**场景说明：**
测试长文本输入下的 Prompt 效果。

**具体需求：**
1. 测试 Token 限制
2. 测试长文本摘要
3. 测试分段处理

**验收标准：**
- [ ] Token 计算正确
- [ ] 长文本处理策略有效
- [ ] 输出质量稳定

---

#### 练习15：温度参数测试

**场景说明：**
测试不同温度参数对 Prompt 输出的影响。

**具体需求：**
1. 测试温度 0-1 范围
2. 分析稳定性 vs 创造性
3. 确定最佳参数

**验收标准：**
- [ ] 温度测试覆盖全面
- [ ] 影响分析准确
- [ ] 参数建议合理

---

#### 练习16：Prompt 性能测试

**场景说明：**
测试 Prompt 的响应时间和 Token 消耗。

**具体需求：**
1. 测量响应延迟
2. 统计 Token 消耗
3. 优化建议

**验收标准：**
- [ ] 性能指标完整
- [ ] 统计数据准确
- [ ] 优化方案可行

---

### 综合练习（17-20）

#### 练习17：完整 Prompt 测试框架

**场景说明：**
搭建完整的 Prompt 测试框架，支持多种测试场景。

**具体需求：**
1. 整合模板管理、测试执行、报告生成
2. 支持 pytest 集成
3. 生成 HTML 报告

**验收标准：**
- [ ] 框架功能完整
- [ ] pytest 集成成功
- [ ] 报告美观实用

---

#### 练习18：Prompt 持续监控

**场景说明：**
建立 Prompt 效果持续监控机制。

**具体需求：**
1. 定期运行回归测试
2. 效果下降告警
3. 趋势分析

**验收标准：**
- [ ] 监控机制有效
- [ ] 告警及时
- [ ] 趋势可视化

---

#### 练习19：Prompt 优化闭环

**场景说明：**
建立 Prompt 优化-测试-上线的完整流程。

**具体需求：**
1. 收集失败案例
2. 自动生成优化建议
3. A/B 验证后上线

**验收标准：**
- [ ] 闭环流程完整
- [ ] 自动化程度高
- [ ] 效果持续提升

---

#### 练习20：企业级 Prompt 管理平台

**场景说明：**
设计企业级 Prompt 管理平台的测试方案。

**具体需求：**
1. 测试 Prompt CRUD 功能
2. 测试版本管理
3. 测试权限控制

**验收标准：**
- [ ] 功能测试覆盖
- [ ] 边界场景测试
- [ ] 安全测试通过

---

## 五、检验标准

### 自测题

1. Prompt 设计的四大原则是什么？
2. Few-shot 和 Zero-shot 的区别？
3. 如何进行 Prompt A/B 测试？
4. Prompt 回归测试的目的是什么？

### 参考答案

1. 清晰性、具体性、结构化、上下文
2. Few-shot 提供示例，Zero-shot 不提供示例
3. 使用相同的输入对比两个 Prompt 的效果，统计分析结果
4. 确保 Prompt 修改后不影响已有功能的效果
