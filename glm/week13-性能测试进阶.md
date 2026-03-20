# 第13周：RAG 测试与 Agent 测试

## 本周目标

掌握 RAG（检索增强生成）系统和 AI Agent 的测试方法。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| RAG 原理 | 检索增强生成流程 | ⭐⭐⭐⭐ |
| 向量数据库 | ChromaDB、FAISS | ⭐⭐⭐⭐ |
| RAG 测试 | 检索准确率、生成质量 | ⭐⭐⭐⭐⭐ |
| Agent 测试 | 工具调用、多轮对话 | ⭐⭐⭐⭐⭐ |
| 智能化测试 | AI 生成测试用例 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 RAG 系统原理

```
RAG（Retrieval-Augmented Generation）检索增强生成

流程：
1. 用户提问
2. 在知识库中检索相关文档
3. 将检索结果作为上下文
4. 大模型基于上下文生成回答

优势：
- 解决知识时效性问题
- 减少幻觉
- 可以使用企业私有数据

关键组件：
- 文档处理：分块、向量化
- 向量数据库：存储和检索
- Embedding 模型：文本转向量
- LLM：生成最终答案
```

```python
# ============================================
# 简单 RAG 系统实现
# ============================================
# 安装：pip install chromadb sentence-transformers

from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class SimpleRAG:
    """简单 RAG 系统"""

    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.chroma = Client(Settings())
        self.collection = None

    def index_documents(self, documents, collection_name="docs"):
        """索引文档"""
        self.collection = self.chroma.create_collection(collection_name)

        for i, doc in enumerate(documents):
            embedding = self.embedding_model.encode(doc["content"]).tolist()
            self.collection.add(
                ids=[str(i)],
                embeddings=[embedding],
                documents=[doc["content"]],
                metadatas=[doc.get("metadata", {})]
            )

    def search(self, query, top_k=3):
        """检索相关文档"""
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results

    def generate_answer(self, query, llm_client, top_k=3):
        """生成答案"""
        # 1. 检索
        search_results = self.search(query, top_k)
        contexts = search_results["documents"][0]

        # 2. 构建 Prompt
        context_text = "\n\n".join(contexts)
        prompt = f"""根据以下上下文回答问题：

上下文：
{context_text}

问题：{query}

请基于上下文回答，如果上下文中没有相关信息，请说"我不知道"。"""

        # 3. 生成答案
        answer = llm_client.chat(prompt)
        return {
            "query": query,
            "contexts": contexts,
            "answer": answer
        }

# 使用
documents = [
    {"content": "携程是一个在线旅行服务平台，成立于1999年。", "metadata": {"source": "about"}},
    {"content": "携程提供酒店预订、机票预订、火车票预订等服务。", "metadata": {"source": "services"}},
    {"content": "携程的客服热线是400-820-6666。", "metadata": {"source": "contact"}}
]

rag = SimpleRAG()
rag.index_documents(documents)
```

---

### 2.2 RAG 测试框架

```python
import pytest
from typing import List, Dict

# ============================================
# RAG 测试指标
# ============================================
class RAGEvaluator:
    """RAG 系统评估器"""

    def __init__(self, rag_system, llm_client):
        self.rag = rag_system
        self.llm = llm_client
        self.comparator = SemanticComparator()

    def evaluate_retrieval(self, test_cases: List[Dict]):
        """
        评估检索质量

        测试用例格式：
        {
            "query": "携程提供哪些服务",
            "relevant_doc_ids": ["1", "2"]  # 相关文档 ID
        }
        """
        results = []

        for case in test_cases:
            search_results = self.rag.search(case["query"], top_k=5)
            retrieved_ids = search_results["ids"][0]
            relevant_ids = case["relevant_doc_ids"]

            # 计算指标
            retrieved_set = set(retrieved_ids)
            relevant_set = set(relevant_ids)

            hits = retrieved_set & relevant_set

            precision = len(hits) / len(retrieved_set) if retrieved_set else 0
            recall = len(hits) / len(relevant_set) if relevant_set else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

            results.append({
                "query": case["query"],
                "precision": precision,
                "recall": recall,
                "f1": f1
            })

        # 平均指标
        avg_precision = sum(r["precision"] for r in results) / len(results)
        avg_recall = sum(r["recall"] for r in results) / len(results)
        avg_f1 = sum(r["f1"] for r in results) / len(results)

        return {
            "cases": results,
            "avg_precision": avg_precision,
            "avg_recall": avg_recall,
            "avg_f1": avg_f1
        }

    def evaluate_answer_quality(self, test_cases: List[Dict]):
        """
        评估答案质量

        测试用例格式：
        {
            "query": "携程什么时候成立的",
            "expected_answer": "1999年"
        }
        """
        results = []

        for case in test_cases:
            rag_result = self.rag.generate_answer(case["query"], self.llm)

            # 语义相似度
            similarity = self.comparator.similarity(
                rag_result["answer"],
                case["expected_answer"]
            )

            results.append({
                "query": case["query"],
                "answer": rag_result["answer"],
                "expected": case["expected_answer"],
                "similarity": similarity,
                "passed": similarity >= 0.7
            })

        pass_rate = sum(r["passed"] for r in results) / len(results)
        return {
            "cases": results,
            "pass_rate": pass_rate
        }

    def evaluate_faithfulness(self, test_cases: List[Dict]):
        """
        评估忠实度（是否产生幻觉）

        检查答案是否基于检索到的上下文
        """
        results = []

        for case in test_cases:
            rag_result = self.rag.generate_answer(case["query"], self.llm)
            answer = rag_result["answer"]
            contexts = rag_result["contexts"]

            # 如果回答包含"我不知道"，检查是否确实没有相关信息
            if "我不知道" in answer:
                # 检查上下文是否确实没有答案
                # 这里简化处理
                results.append({
                    "query": case["query"],
                    "answer": answer,
                    "faithful": True  # 诚实回答不知道
                })
            else:
                # 检查答案内容是否来自上下文
                context_text = " ".join(contexts)
                # 简化：检查答案中的关键信息是否在上下文中
                # 实际可以使用 NLI 模型
                faithful = True  # 需要更复杂的验证

                results.append({
                    "query": case["query"],
                    "answer": answer,
                    "contexts": contexts,
                    "faithful": faithful
                })

        faithfulness_rate = sum(r["faithful"] for r in results) / len(results)
        return {
            "cases": results,
            "faithfulness_rate": faithfulness_rate
        }

# ============================================
# 测试用例
# ============================================
class TestRAG:

    @pytest.fixture
    def rag_system(self):
        """RAG 系统 fixture"""
        rag = SimpleRAG()
        rag.index_documents([
            {"content": "携程成立于1999年，总部位于上海。"},
            {"content": "携程提供酒店、机票、火车票预订服务。"},
            {"content": "携程客服电话：400-820-6666。"}
        ])
        return rag

    def test_retrieval_quality(self, rag_system):
        """测试检索质量"""
        evaluator = RAGEvaluator(rag_system, None)

        test_cases = [
            {"query": "携程什么时候成立的", "relevant_doc_ids": ["0"]},
            {"query": "携程有哪些服务", "relevant_doc_ids": ["1"]},
            {"query": "携程客服电话", "relevant_doc_ids": ["2"]}
        ]

        results = evaluator.evaluate_retrieval(test_cases)
        assert results["avg_recall"] >= 0.8

    def test_answer_quality(self, rag_system):
        """测试答案质量"""
        llm = LLMClient(provider="openai", api_key="xxx")
        evaluator = RAGEvaluator(rag_system, llm)

        test_cases = [
            {"query": "携程什么时候成立的", "expected_answer": "1999年"},
            {"query": "携程总部在哪", "expected_answer": "上海"}
        ]

        results = evaluator.evaluate_answer_quality(test_cases)
        assert results["pass_rate"] >= 0.7
```

---

### 2.3 Agent 测试

```python
# ============================================
# Agent 基础概念
# ============================================
"""
AI Agent 是能够：
1. 理解用户意图
2. 决定调用哪些工具
3. 执行工具并处理结果
4. 生成最终回答

测试重点：
1. 工具调用正确性
2. 参数提取准确性
3. 多轮对话一致性
4. 错误处理能力
"""

# ============================================
# Agent 测试框架
# ============================================
class AgentTester:
    """Agent 测试框架"""

    def __init__(self, agent):
        self.agent = agent
        self.conversation_history = []

    def test_tool_calling(self, user_input: str, expected_tool: str):
        """测试工具调用"""
        result = self.agent.run(user_input)

        # 检查是否调用了正确的工具
        tool_calls = result.get("tool_calls", [])
        called_tools = [tc["name"] for tc in tool_calls]

        return {
            "input": user_input,
            "expected_tool": expected_tool,
            "called_tools": called_tools,
            "passed": expected_tool in called_tools
        }

    def test_tool_parameters(self, user_input: str, expected_params: dict):
        """测试工具参数提取"""
        result = self.agent.run(user_input)

        tool_calls = result.get("tool_calls", [])
        if not tool_calls:
            return {"passed": False, "reason": "没有调用工具"}

        actual_params = tool_calls[0].get("args", {})

        # 检查关键参数
        missing = []
        wrong = []
        for key, expected_value in expected_params.items():
            if key not in actual_params:
                missing.append(key)
            elif expected_value is not None and actual_params[key] != expected_value:
                wrong.append((key, expected_value, actual_params[key]))

        return {
            "passed": len(missing) == 0 and len(wrong) == 0,
            "missing_params": missing,
            "wrong_params": wrong,
            "actual_params": actual_params
        }

    def test_multi_turn(self, conversation_flow: List[Dict]):
        """
        测试多轮对话

        conversation_flow 格式：
        [
            {"user": "搜索北京酒店", "expected_tool": "search_hotel"},
            {"user": "价格最低的那个", "expected_tool": "get_hotel_detail"},
            {"user": "预订这个", "expected_tool": "book_hotel"}
        ]
        """
        results = []

        for turn in conversation_flow:
            result = self.agent.run(turn["user"])
            self.conversation_history.append({
                "user": turn["user"],
                "agent": result
            })

            tool_calls = result.get("tool_calls", [])
            called_tools = [tc["name"] for tc in tool_calls]

            results.append({
                "turn": len(results) + 1,
                "user": turn["user"],
                "expected": turn["expected_tool"],
                "called": called_tools,
                "passed": turn["expected_tool"] in called_tools
            })

        pass_rate = sum(r["passed"] for r in results) / len(results)
        return {
            "turns": results,
            "pass_rate": pass_rate
        }

    def test_safety(self, harmful_inputs: List[str]):
        """测试安全性（拒绝有害请求）"""
        results = []

        for input_text in harmful_inputs:
            result = self.agent.run(input_text)
            response = result.get("response", "")

            # 检查是否拒绝
            refused = any(
                keyword in response
                for keyword in ["不能", "无法", "抱歉", "不提供"]
            )

            results.append({
                "input": input_text,
                "refused": refused,
                "response": response
            })

        refusal_rate = sum(r["refused"] for r in results) / len(results)
        return {
            "cases": results,
            "refusal_rate": refusal_rate
        }

# ============================================
# 测试用例
# ============================================
class TestTravelAgent:

    @pytest.fixture
    def agent(self):
        """旅行助手 Agent"""
        # 这里返回实际的 Agent 实例
        pass

    def test_search_hotel(self, agent):
        """测试酒店搜索"""
        tester = AgentTester(agent)

        result = tester.test_tool_calling(
            "帮我搜索北京朝阳区附近的酒店",
            expected_tool="search_hotel"
        )
        assert result["passed"]

    def test_tool_parameters(self, agent):
        """测试参数提取"""
        tester = AgentTester(agent)

        result = tester.test_tool_parameters(
            "搜索上海浦东的酒店，价格在500-1000元",
            expected_params={"city": "上海", "district": "浦东"}
        )
        assert result["passed"]

    def test_multi_turn_booking(self, agent):
        """测试多轮预订对话"""
        tester = AgentTester(agent)

        flow = [
            {"user": "搜索北京的酒店", "expected_tool": "search_hotel"},
            {"user": "第一个多少钱", "expected_tool": "get_price"},
            {"user": "帮我预订", "expected_tool": "book_hotel"}
        ]

        result = tester.test_multi_turn(flow)
        assert result["pass_rate"] >= 0.8
```

---

### 2.4 智能化测试

```python
# ============================================
# AI 生成测试用例
# ============================================
class AITestCaseGenerator:
    """AI 测试用例生成器"""

    def __init__(self, llm_client):
        self.llm = llm_client

    def generate_test_cases(self, requirement: str, count: int = 10):
        """根据需求生成测试用例"""
        prompt = f"""根据以下需求，生成 {count} 个测试用例：

需求：
{requirement}

请以 JSON 格式输出，每个测试用例包含：
- case_id: 用例ID
- title: 用例标题
- preconditions: 前置条件
- steps: 测试步骤列表
- expected_result: 预期结果
- priority: 优先级（P0/P1/P2）
- type: 测试类型（功能/边界/异常）

```json
[
  {{
    "case_id": "TC001",
    "title": "..."
  }}
]
```"""

        response = self.llm.chat(prompt)

        # 提取 JSON
        import json
        import re
        json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        return json.loads(response)

    def generate_edge_cases(self, function_spec: str):
        """生成边界值测试用例"""
        prompt = f"""根据以下函数规格，生成边界值测试用例：

{function_spec}

请考虑以下边界情况：
1. 空值/null
2. 最大值/最小值
3. 特殊字符
4. 超长输入
5. 负数/零

以 JSON 格式输出测试用例。"""

        response = self.llm.chat(prompt)
        return response

    def generate_api_test_cases(self, api_spec: str):
        """根据 API 规格生成测试用例"""
        prompt = f"""根据以下 API 规格，生成测试用例：

{api_spec}

请生成以下类型的测试：
1. 正常场景
2. 参数缺失
3. 参数类型错误
4. 权限验证
5. 边界值

以 JSON 格式输出。"""

        response = self.llm.chat(prompt)
        return response

# ============================================
# AI 辅助 Bug 分析
# ============================================
class AIBugAnalyzer:
    """AI Bug 分析器"""

    def __init__(self, llm_client):
        self.llm = llm_client

    def analyze_test_failure(self, test_name: str, error_log: str, code_snippet: str = None):
        """分析测试失败原因"""
        prompt = f"""测试用例 "{test_name}" 失败了。

错误日志：
{error_log}
"""

        if code_snippet:
            prompt += f"""
相关代码：
{code_snippet}
"""

        prompt += """
请分析：
1. 失败的根本原因是什么？
2. 可能的修复方案是什么？
3. 如何避免类似问题？

请给出详细分析。"""

        return self.llm.chat(prompt)

    def suggest_fix(self, bug_description: str, code_context: str):
        """建议修复方案"""
        prompt = f"""发现以下 Bug：

{bug_description}

相关代码：
{code_context}

请提供：
1. 问题根因分析
2. 修复代码建议
3. 需要添加的测试用例"""

        return self.llm.chat(prompt)
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 理解 RAG 系统原理
- [ ] 能评估 RAG 检索和生成质量
- [ ] 能测试 Agent 的工具调用
- [ ] 能测试多轮对话
- [ ] 能使用 AI 生成测试用例

### 应该了解

- [ ] 向量数据库
- [ ] Agent 架构

---

## 四、练习内容

### 练习1：RAG 评估

```python
# 构建简单 RAG 系统
# 实现检索和生成评估
```

### 练习2：Agent 测试

```python
# 测试旅行助手 Agent
# 覆盖工具调用和多轮对话
```

### 练习3：AI 生成用例

```python
# 使用 AI 生成测试用例
# 评估生成质量
```

---

## 五、本周小结

1. **RAG 测试**：检索准确率 + 生成质量
2. **Agent 测试**：工具调用 + 多轮对话
3. **智能化测试**：AI 辅助测试

### 下周预告

第14周学习 LLM 评测和安全测试。
