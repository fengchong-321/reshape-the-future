# 第16周：Agent 测试

## 本周目标

掌握 AI Agent 的测试方法，能够设计和实现 Agent 工具调用、多轮对话、状态管理的测试方案。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Agent 架构 | ReAct、Plan-Execute、多 Agent | ⭐⭐⭐⭐ |
| 工具调用测试 | 参数提取、执行验证 | ⭐⭐⭐⭐⭐ |
| 多轮对话测试 | 上下文理解、状态管理 | ⭐⭐⭐⭐⭐ |
| Agent 评测 | 任务完成率、效率评估 | ⭐⭐⭐⭐⭐ |
| 安全性测试 | 权限控制、输入验证 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 Agent 架构理解

```python
# ============================================
# Agent 基本概念
# ============================================
"""
Agent = LLM + Tools + Memory + Planning

核心组件：
1. LLM：大脑，负责推理和决策
2. Tools：工具集，执行具体操作
3. Memory：记忆，保存对话历史和状态
4. Planning：规划，分解复杂任务

常见架构：
- ReAct：Reasoning + Acting，交替思考和行动
- Plan-Execute：先规划再执行
- Multi-Agent：多个 Agent 协作
"""

# ============================================
# 简单 Agent 实现
# ============================================
import json
from typing import Callable, Dict, Any

class SimpleAgent:
    """简单 Agent 实现"""

    def __init__(self, llm_client, tools: Dict[str, Callable]):
        self.llm = llm_client
        self.tools = tools
        self.memory = []

    def think(self, user_input: str) -> Dict:
        """思考：决定是否使用工具"""
        # 构建工具描述
        tools_desc = "\n".join([
            f"- {name}: {func.__doc__}"
            for name, func in self.tools.items()
        ])

        prompt = f"""
你是一个智能助手，可以使用以下工具：
{tools_desc}

用户输入：{user_input}

请判断是否需要使用工具。如果需要，请返回 JSON：
{{"action": "use_tool", "tool": "工具名", "args": {{参数}}}}
如果不需要，请返回：
{{"action": "respond", "message": "回复内容"}}
"""
        response = self.llm.generate(prompt)
        return json.loads(response)

    def act(self, decision: Dict) -> Any:
        """执行：调用工具或返回回复"""
        if decision["action"] == "use_tool":
            tool_name = decision["tool"]
            tool_args = decision.get("args", {})
            if tool_name in self.tools:
                return self.tools[tool_name](**tool_args)
            else:
                return f"错误：未知工具 {tool_name}"
        else:
            return decision["message"]

    def run(self, user_input: str) -> str:
        """运行 Agent"""
        self.memory.append({"role": "user", "content": user_input})

        decision = self.think(user_input)
        result = self.act(decision)

        self.memory.append({"role": "assistant", "content": str(result)})
        return str(result)
```

### 2.2 工具定义与测试

```python
# ============================================
# 工具定义
# ============================================
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ToolParameter:
    """工具参数定义"""
    name: str
    type: str  # string, number, boolean, array, object
    description: str
    required: bool = True
    enum: Optional[List[str]] = None

@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    parameters: List[ToolParameter]

    def to_openai_format(self) -> dict:
        """转换为 OpenAI 工具格式"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        p.name: {
                            "type": p.type,
                            "description": p.description,
                            **({"enum": p.enum} if p.enum else {})
                        }
                        for p in self.parameters
                    },
                    "required": [p.name for p in self.parameters if p.required]
                }
            }
        }

# 定义工具
search_hotel_tool = Tool(
    name="search_hotel",
    description="搜索酒店",
    parameters=[
        ToolParameter("city", "string", "城市名称", required=True),
        ToolParameter("check_in", "string", "入住日期，格式 YYYY-MM-DD", required=True),
        ToolParameter("check_out", "string", "退房日期，格式 YYYY-MM-DD", required=True),
        ToolParameter("guests", "number", "入住人数", required=False)
    ]
)

book_hotel_tool = Tool(
    name="book_hotel",
    description="预订酒店",
    parameters=[
        ToolParameter("hotel_id", "string", "酒店ID", required=True),
        ToolParameter("guest_name", "string", "入住人姓名", required=True),
        ToolParameter("phone", "string", "联系电话", required=True)
    ]
)
```

```python
# ============================================
# 工具调用测试
# ============================================
import pytest

class ToolCallTester:
    """工具调用测试器"""

    def __init__(self, agent):
        self.agent = agent

    def test_tool_selection(
        self,
        user_input: str,
        expected_tool: str,
        expected_args: dict = None
    ) -> dict:
        """测试工具选择是否正确"""
        decision = self.agent.think(user_input)

        result = {
            "passed": True,
            "errors": [],
            "decision": decision
        }

        # 检查是否选择了正确的工具
        if decision.get("action") != "use_tool":
            result["passed"] = False
            result["errors"].append("应该调用工具但未调用")
            return result

        if decision.get("tool") != expected_tool:
            result["passed"] = False
            result["errors"].append(f"工具选择错误：期望 {expected_tool}，实际 {decision.get('tool')}")

        # 检查参数
        if expected_args:
            actual_args = decision.get("args", {})
            for key, expected_value in expected_args.items():
                if key not in actual_args:
                    result["passed"] = False
                    result["errors"].append(f"缺少参数: {key}")
                elif actual_args[key] != expected_value:
                    result["passed"] = False
                    result["errors"].append(f"参数 {key} 错误：期望 {expected_value}，实际 {actual_args[key]}")

        return result

# 使用
def test_tool_selection():
    tester = ToolCallTester(agent)

    # 测试1：搜索酒店
    result = tester.test_tool_selection(
        "帮我搜索北京3月15日入住的酒店",
        expected_tool="search_hotel",
        expected_args={"city": "北京"}
    )
    assert result["passed"], result["errors"]

    # 测试2：预订酒店
    result = tester.test_tool_selection(
        "预订酒店ID为12345的房间，我名字叫张三",
        expected_tool="book_hotel",
        expected_args={"hotel_id": "12345", "guest_name": "张三"}
    )
    assert result["passed"], result["errors"]
```

### 2.3 参数提取测试

```python
# ============================================
# 参数提取测试
# ============================================
from datetime import datetime

class ParameterExtractor:
    """参数提取器"""

    def __init__(self, tool: Tool):
        self.tool = tool

    def extract(self, user_input: str) -> dict:
        """从用户输入中提取参数"""
        # 构建提取 prompt
        params_desc = "\n".join([
            f"- {p.name} ({p.type}): {p.description}"
            for p in self.tool.parameters
        ])

        prompt = f"""
从用户输入中提取以下参数：
{params_desc}

用户输入：{user_input}

请返回 JSON 格式：
{{"extracted": {{参数名: 值}}, "missing": ["缺失的必填参数"]}}
"""
        response = self.llm.generate(prompt)
        return json.loads(response)

class ParameterExtractionTester:
    """参数提取测试器"""

    def __init__(self, extractor: ParameterExtractor):
        self.extractor = extractor

    def test_extraction(
        self,
        user_input: str,
        expected_extracted: dict,
        expected_missing: list = None
    ) -> dict:
        """测试参数提取"""
        result = self.extractor.extract(user_input)

        test_result = {
            "passed": True,
            "errors": [],
            "extracted": result.get("extracted", {}),
            "missing": result.get("missing", [])
        }

        # 检查提取的参数
        for key, expected_value in expected_extracted.items():
            actual = result.get("extracted", {}).get(key)
            if actual != expected_value:
                test_result["passed"] = False
                test_result["errors"].append(f"参数 {key}: 期望 {expected_value}，实际 {actual}")

        # 检查缺失参数
        if expected_missing:
            actual_missing = set(result.get("missing", []))
            expected_set = set(expected_missing)
            if actual_missing != expected_set:
                test_result["passed"] = False
                test_result["errors"].append(f"缺失参数: 期望 {expected_set}，实际 {actual_missing}")

        return test_result

# 使用
def test_parameter_extraction():
    extractor = ParameterExtractor(search_hotel_tool)
    tester = ParameterExtractionTester(extractor)

    result = tester.test_extraction(
        "帮我搜索北京3月15日到3月17日的酒店",
        expected_extracted={
            "city": "北京",
            "check_in": "2024-03-15",
            "check_out": "2024-03-17"
        }
    )
    assert result["passed"], result["errors"]
```

### 2.4 多轮对话测试

```python
# ============================================
# 多轮对话测试
# ============================================
from typing import List, Dict

@dataclass
class ConversationTurn:
    """对话轮次"""
    user_input: str
    expected_tool: str = None
    expected_response_contains: List[str] = None
    expected_state: dict = None

class ConversationTester:
    """多轮对话测试器"""

    def __init__(self, agent):
        self.agent = agent
        self.conversation_history = []

    def run_conversation(
        self,
        turns: List[ConversationTurn]
    ) -> dict:
        """运行多轮对话测试"""
        results = []

        for i, turn in enumerate(turns):
            turn_result = {
                "turn": i + 1,
                "user_input": turn.user_input,
                "passed": True,
                "errors": []
            }

            # 执行对话
            response = self.agent.run(turn.user_input)
            turn_result["response"] = response

            # 检查工具调用
            if turn.expected_tool:
                last_decision = self.agent.memory[-1]
                if turn.expected_tool not in str(last_decision):
                    turn_result["passed"] = False
                    turn_result["errors"].append(f"期望调用工具 {turn.expected_tool}")

            # 检查响应内容
            if turn.expected_response_contains:
                for keyword in turn.expected_response_contains:
                    if keyword not in response:
                        turn_result["passed"] = False
                        turn_result["errors"].append(f"响应缺少关键词: {keyword}")

            # 检查状态
            if turn.expected_state:
                for key, value in turn.expected_state.items():
                    if self.agent.state.get(key) != value:
                        turn_result["passed"] = False
                        turn_result["errors"].append(f"状态 {key} 错误")

            results.append(turn_result)

        return {
            "turns": results,
            "all_passed": all(r["passed"] for r in results)
        }

# 使用
def test_hotel_booking_conversation():
    tester = ConversationTester(agent)

    conversation = [
        ConversationTurn(
            user_input="帮我搜索北京的酒店",
            expected_tool="search_hotel"
        ),
        ConversationTurn(
            user_input="第一个多少钱",
            expected_response_contains=["元", "价格"]
        ),
        ConversationTurn(
            user_input="就订这个吧",
            expected_tool="book_hotel"
        )
    ]

    result = tester.run_conversation(conversation)
    assert result["all_passed"], [r["errors"] for r in result["turns"] if not r["passed"]]
```

### 2.5 Agent 评测框架

```python
# ============================================
# Agent 任务评测
# ============================================
from dataclasses import dataclass
from typing import Any
import time

@dataclass
class AgentTask:
    """Agent 任务"""
    name: str
    description: str
    initial_input: str
    success_criteria: callable  # 判断任务是否成功的函数
    max_turns: int = 10
    timeout: int = 60

@dataclass
class TaskResult:
    """任务结果"""
    task_name: str
    success: bool
    turns: int
    duration: float
    final_state: dict
    errors: list

class AgentEvaluator:
    """Agent 评测器"""

    def __init__(self, agent):
        self.agent = agent

    def evaluate_task(self, task: AgentTask) -> TaskResult:
        """评估单个任务"""
        start_time = time.time()
        turns = 0
        errors = []

        try:
            # 执行任务
            response = self.agent.run(task.initial_input)
            turns = 1

            # 检查是否成功
            success = task.success_criteria(self.agent, response)

            # 如果不成功，尝试继续
            while not success and turns < task.max_turns:
                # 可以添加额外的交互逻辑
                turns += 1
                time.sleep(0.1)

        except Exception as e:
            errors.append(str(e))
            success = False

        duration = time.time() - start_time

        return TaskResult(
            task_name=task.name,
            success=success,
            turns=turns,
            duration=duration,
            final_state=getattr(self.agent, 'state', {}),
            errors=errors
        )

    def evaluate_batch(self, tasks: List[AgentTask]) -> dict:
        """批量评估"""
        results = [self.evaluate_task(task) for task in tasks]

        return {
            "total": len(results),
            "success": sum(1 for r in results if r.success),
            "success_rate": sum(1 for r in results if r.success) / len(results),
            "avg_turns": sum(r.turns for r in results) / len(results),
            "avg_duration": sum(r.duration for r in results) / len(results),
            "results": results
        }

# 使用
def test_agent_tasks():
    evaluator = AgentEvaluator(agent)

    tasks = [
        AgentTask(
            name="搜索酒店",
            description="搜索指定城市的酒店",
            initial_input="搜索北京3月15日的酒店",
            success_criteria=lambda agent, resp: "酒店" in resp and len(resp) > 0
        ),
        AgentTask(
            name="预订流程",
            description="完成酒店预订",
            initial_input="预订北京酒店",
            success_criteria=lambda agent, resp: "预订成功" in resp
        )
    ]

    results = evaluator.evaluate_batch(tasks)
    print(f"成功率: {results['success_rate']:.2%}")
```

---

## 三、学到什么程度

### 必须掌握
- [ ] Agent 架构和核心组件
- [ ] 工具定义和调用测试
- [ ] 参数提取测试
- [ ] 多轮对话测试
- [ ] Agent 任务评测

### 应该了解
- [ ] Multi-Agent 协作测试
- [ ] Agent 记忆系统测试
- [ ] Agent 规划能力测试
- [ ] Agent 安全性测试

---

## 四、练习内容

### 基础练习（1-8）

#### 练习1：简单 Agent 实现

**场景说明：**
理解 Agent 的基本架构，实现一个简单的 Agent。

**具体需求：**
1. 实现 SimpleAgent 类
2. 支持 think 和 act 方法
3. 支持基本的记忆功能

**使用示例：**
```python
agent = SimpleAgent(llm_client, tools={
    "search": search_function,
    "calculate": calculate_function
})
response = agent.run("搜索北京天气")
```

**验收标准：**
- [ ] Agent 类实现完整
- [ ] think 方法返回正确格式
- [ ] act 方法能调用工具
- [ ] 记忆功能正常

---

#### 练习2：工具定义

**场景说明：**
为 Agent 定义可调用的工具。

**具体需求：**
1. 实现 Tool 和 ToolParameter 类
2. 支持 OpenAI 格式转换
3. 定义 3 个以上工具

**使用示例：**
```python
weather_tool = Tool(
    name="get_weather",
    description="获取城市天气",
    parameters=[
        ToolParameter("city", "string", "城市名称", required=True)
    ]
)
```

**验收标准：**
- [ ] 工具定义完整
- [ ] 参数类型支持完整
- [ ] 格式转换正确

---

#### 练习3：工具调用测试

**场景说明：**
测试 Agent 是否正确选择和调用工具。

**具体需求：**
1. 实现 ToolCallTester 类
2. 验证工具选择
3. 验证参数传递

**使用示例：**
```python
tester = ToolCallTester(agent)
result = tester.test_tool_selection(
    "搜索北京酒店",
    expected_tool="search_hotel"
)
assert result["passed"]
```

**验收标准：**
- [ ] 测试器实现完整
- [ ] 工具选择验证正确
- [ ] 参数验证正确

---

#### 练习4：参数提取测试

**场景说明：**
测试从用户输入中提取参数的能力。

**具体需求：**
1. 实现 ParameterExtractor 类
2. 支持必填/选填参数
3. 检测缺失参数

**使用示例：**
```python
extractor = ParameterExtractor(tool)
result = extractor.extract("搜索北京3月15日的酒店")
assert result["extracted"]["city"] == "北京"
```

**验收标准：**
- [ ] 参数提取准确
- [ ] 缺失参数检测
- [ ] 支持多种格式

---

#### 练习5：单轮对话测试

**场景说明：**
测试单轮对话的响应质量。

**具体需求：**
1. 测试直接回复场景
2. 测试工具调用场景
3. 验证响应格式

**验收标准：**
- [ ] 回复内容正确
- [ ] 工具调用正确
- [ ] 格式符合预期

---

#### 练习6：多轮对话测试

**场景说明：**
测试多轮对话的上下文理解能力。

**具体需求：**
1. 实现 ConversationTester 类
2. 支持多轮对话验证
3. 验证上下文传递

**使用示例：**
```python
tester = ConversationTester(agent)
result = tester.run_conversation([
    ConversationTurn("搜索酒店", expected_tool="search"),
    ConversationTurn("第一个", expected_tool="book")
])
```

**验收标准：**
- [ ] 多轮测试通过
- [ ] 上下文正确
- [ ] 状态管理正常

---

#### 练习7：代词指代测试

**场景说明：**
测试 Agent 对代词的理解能力。

**具体需求：**
1. 设计代词测试用例
2. 验证代词解析
3. 验证上下文关联

**验收标准：**
- [ ] 代词解析正确
- [ ] 指代关系明确
- [ ] 测试用例覆盖

---

#### 练习8：Agent 状态管理

**场景说明：**
测试 Agent 的状态管理能力。

**具体需求：**
1. 实现状态存储
2. 验证状态更新
3. 验证状态持久化

**验收标准：**
- [ ] 状态存储正确
- [ ] 更新及时
- [ ] 持久化可靠

---

### 进阶练习（9-16）

#### 练习9：任务完成率评测

**场景说明：**
评估 Agent 完成任务的能力。

**具体需求：**
1. 定义任务和成功标准
2. 实现评测逻辑
3. 统计完成率

**验收标准：**
- [ ] 任务定义清晰
- [ ] 评测逻辑正确
- [ ] 统计准确

---

#### 练习10：Agent 效率测试

**场景说明：**
评估 Agent 完成任务的效率。

**具体需求：**
1. 测量执行时间
2. 统计对话轮次
3. 分析效率瓶颈

**验收标准：**
- [ ] 时间测量准确
- [ ] 轮次统计正确
- [ ] 瓶颈分析合理

---

#### 练习11：工具执行测试

**场景说明：**
测试工具执行的正确性。

**具体需求：**
1. 模拟工具执行
2. 验证执行结果
3. 处理执行异常

**验收标准：**
- [ ] 执行模拟真实
- [ ] 结果验证完整
- [ ] 异常处理正确

---

#### 练习12：错误恢复测试

**场景说明：**
测试 Agent 的错误恢复能力。

**具体需求：**
1. 注入错误场景
2. 测试恢复策略
3. 验证最终结果

**验收标准：**
- [ ] 错误注入有效
- [ ] 恢复策略合理
- [ ] 结果符合预期

---

#### 练习13：Agent 安全测试

**场景说明：**
测试 Agent 的安全性。

**具体需求：**
1. 测试权限控制
2. 测试输入验证
3. 测试敏感信息保护

**验收标准：**
- [ ] 权限控制有效
- [ ] 输入验证完整
- [ ] 信息保护到位

---

#### 练习14：多工具协调测试

**场景说明：**
测试 Agent 协调多个工具的能力。

**具体需求：**
1. 设计多工具场景
2. 测试工具选择
3. 测试结果整合

**验收标准：**
- [ ] 工具选择正确
- [ ] 调用顺序合理
- [ ] 结果整合正确

---

#### 练习15：Agent 记忆测试

**场景说明：**
测试 Agent 的记忆能力。

**具体需求：**
1. 测试短期记忆
2. 测试长期记忆
3. 测试记忆检索

**验收标准：**
- [ ] 记忆存储正确
- [ ] 检索准确
- [ ] 记忆影响决策

---

#### 练习16：Agent 规划测试

**场景说明：**
测试 Agent 的规划能力。

**具体需求：**
1. 设计复杂任务
2. 测试任务分解
3. 验证执行顺序

**验收标准：**
- [ ] 任务分解合理
- [ ] 顺序正确
- [ ] 执行完整

---

### 综合练习（17-20）

#### 练习17：完整 Agent 测试框架

**场景说明：**
搭建完整的 Agent 测试框架。

**具体需求：**
1. 整合所有测试组件
2. 支持 pytest 集成
3. 生成测试报告

**验收标准：**
- [ ] 框架功能完整
- [ ] pytest 集成成功
- [ ] 报告清晰

---

#### 练习18：酒店预订 Agent 测试

**场景说明：**
为酒店预订 Agent 设计完整测试。

**具体需求：**
1. 设计测试场景
2. 覆盖完整流程
3. 边界场景测试

**验收标准：**
- [ ] 场景覆盖完整
- [ ] 流程测试通过
- [ ] 边界处理正确

---

#### 练习19：客服 Agent 测试

**场景说明：**
为智能客服 Agent 设计测试。

**具体需求：**
1. 测试问答能力
2. 测试工单创建
3. 测试转人工

**验收标准：**
- [ ] 问答准确
- [ ] 工单正确
- [ ] 转接流畅

---

#### 练习20：Agent 压力测试

**场景说明：**
对 Agent 进行压力测试。

**具体需求：**
1. 并发请求测试
2. 长时间运行测试
3. 资源消耗监控

**验收标准：**
- [ ] 并发处理正常
- [ ] 长期运行稳定
- [ ] 资源消耗合理

---

## 五、检验标准

### 自测题

1. Agent 的核心组件有哪些？
2. 如何测试工具调用的正确性？
3. 多轮对话测试需要注意什么？
4. 如何评估 Agent 的任务完成能力？

### 参考答案

1. LLM、Tools、Memory、Planning
2. 验证工具选择、参数提取、执行结果
3. 上下文理解、状态管理、代词指代
4. 定义任务、设定成功标准、统计完成率和效率
