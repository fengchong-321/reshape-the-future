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

### 基础练习（1-8）

#### 练习1：向量数据库基础操作

```python
# 使用 ChromaDB 实现向量存储
# 要求：
# 1. 创建集合（Collection）
# 2. 添加文档向量
# 3. 实现相似度检索

import chromadb
from chromadb.config import Settings

class VectorStore:
    """向量存储类"""

    def __init__(self, collection_name: str = "documents"):
        self.client = chromadb.Client(Settings())
        self.collection = self.client.create_collection(collection_name)

    def add_documents(self, documents: list, ids: list):
        """添加文档"""
        # TODO: 实现代码
        pass

    def search(self, query: str, top_k: int = 5) -> list:
        """检索相似文档"""
        # TODO: 实现代码
        pass

# 测试
store = VectorStore()
store.add_documents(["文档1内容", "文档2内容"], ["id1", "id2"])
results = store.search("查询内容", top_k=3)
```

#### 练习2：文档分块

```python
# 实现文档分块功能
# 要求：
# 1. 支持按字符数分块
# 2. 支持按句子分块
# 3. 支持重叠分块

def chunk_by_chars(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """按字符数分块"""
    # TODO: 实现代码
    pass

def chunk_by_sentences(text: str, max_sentences: int = 5) -> list:
    """按句子分块"""
    # TODO: 实现代码
    pass

# 测试
text = "这是一段很长的文本..." * 100
chunks = chunk_by_chars(text, chunk_size=200, overlap=20)
print(f"分块数量: {len(chunks)}")
```

#### 练习3：简单 RAG 系统实现

```python
# 实现简单的 RAG 系统
# 要求：
# 1. 文档索引功能
# 2. 相似度检索
# 3. 上下文拼接

class SimpleRAG:
    def __init__(self, documents: list):
        self.documents = documents
        self.index = None

    def build_index(self):
        """构建索引"""
        # TODO: 实现代码
        pass

    def retrieve(self, query: str, top_k: int = 3) -> list:
        """检索相关文档"""
        # TODO: 实现代码
        pass

    def build_context(self, query: str) -> str:
        """构建上下文"""
        # TODO: 实现代码
        pass

# 测试
documents = ["文档1", "文档2", "文档3"]
rag = SimpleRAG(documents)
rag.build_index()
context = rag.build_context("查询问题")
```

#### 练习4：检索质量评估

```python
# 评估检索质量
# 要求：
# 1. 计算 Precision@K
# 2. 计算 Recall@K
# 3. 计算 F1 分数

def evaluate_retrieval(retrieved_ids: list, relevant_ids: list, k: int = 5) -> dict:
    """
    评估检索质量

    返回：
    {
        "precision": float,
        "recall": float,
        "f1": float
    }
    """
    # TODO: 实现代码
    pass

# 测试
result = evaluate_retrieval(
    retrieved_ids=["1", "2", "3", "4", "5"],
    relevant_ids=["2", "3", "7"],
    k=5
)
print(f"Precision@5: {result['precision']}")
```

#### 练习5：Agent 工具调用测试

```python
# 测试 Agent 的工具调用能力
# 要求：
# 1. 定义工具函数
# 2. 模拟工具调用
# 3. 验证调用结果

TOOLS = [
    {
        "name": "search_hotel",
        "description": "搜索酒店",
        "parameters": {
            "city": "城市名称",
            "check_in": "入住日期",
            "check_out": "退房日期"
        }
    },
    {
        "name": "book_hotel",
        "description": "预订酒店",
        "parameters": {
            "hotel_id": "酒店ID",
            "user_name": "用户名"
        }
    }
]

def test_tool_calling(user_input: str, expected_tool: str) -> bool:
    """测试工具调用是否正确"""
    # TODO: 实现代码
    pass

# 测试
assert test_tool_calling("帮我搜索北京的酒店", "search_hotel")
assert test_tool_calling("预订酒店ID为123的房间", "book_hotel")
```

#### 练习6：参数提取测试

```python
# 测试 Agent 的参数提取能力
# 要求：
# 1. 从用户输入中提取参数
# 2. 验证参数完整性
# 3. 处理缺失参数

def extract_parameters(user_input: str, tool_schema: dict) -> dict:
    """
    从用户输入中提取参数

    返回：
    {
        "extracted": dict,  # 提取的参数
        "missing": list,  # 缺失的必填参数
        "confidence": float  # 提取置信度
    }
    """
    # TODO: 实现代码
    pass

# 测试
result = extract_parameters(
    "搜索北京朝阳区3月15日入住的酒店",
    TOOLS[0]
)
assert result["extracted"]["city"] == "北京"
```

#### 练习7：多轮对话测试

```python
# 测试多轮对话能力
# 要求：
# 1. 保持对话上下文
# 2. 正确理解代词指代
# 3. 维护对话状态

def test_multi_turn_conversation(conversation_flow: list) -> dict:
    """
    测试多轮对话

    conversation_flow 格式：
    [
        {"user": "搜索北京的酒店", "expected_tool": "search_hotel"},
        {"user": "第一个多少钱", "expected_tool": "get_price"},
        {"user": "预订这个", "expected_tool": "book_hotel"}
    ]
    """
    # TODO: 实现代码
    pass

# 测试
flow = [
    {"user": "搜索北京的酒店", "expected_tool": "search_hotel"},
    {"user": "预订第一个", "expected_tool": "book_hotel"}
]
result = test_multi_turn_conversation(flow)
print(f"通过率: {result['pass_rate']}")
```

#### 练习8：RAG 上下文构建

```python
# 实现 RAG 上下文构建
# 要求：
# 1. 检索相关文档
# 2. 格式化上下文
# 3. 控制上下文长度

def build_rag_context(query: str, documents: list, max_tokens: int = 2000) -> str:
    """
    构建 RAG 上下文

    返回格式化的上下文字符串
    """
    # TODO: 实现代码
    pass

# 测试
context = build_rag_context(
    "携程是什么？",
    ["携程是旅行平台", "携程成立于1999年", "携程总部在上海"],
    max_tokens=500
)
print(context)
```

---

### 进阶练习（9-16）

#### 练习9：RAG 系统完整评估

```python
# 实现 RAG 系统的完整评估
# 要求：
# 1. 检索质量评估
# 2. 生成质量评估
# 3. 忠实度评估

class RAGEvaluator:
    def __init__(self, rag_system, llm_client):
        self.rag = rag_system
        self.llm = llm_client

    def evaluate_retrieval(self, test_cases: list) -> dict:
        """评估检索质量"""
        # TODO: 实现代码
        pass

    def evaluate_generation(self, test_cases: list) -> dict:
        """评估生成质量"""
        # TODO: 实现代码
        pass

    def evaluate_faithfulness(self, test_cases: list) -> dict:
        """评估忠实度（幻觉检测）"""
        # TODO: 实现代码
        pass

    def comprehensive_evaluation(self, test_cases: list) -> dict:
        """综合评估"""
        # TODO: 实现代码
        pass
```

#### 练习10：混合检索实现

```python
# 实现混合检索（向量+关键词）
# 要求：
# 1. 向量相似度检索
# 2. BM25 关键词检索
# 3. 结果融合排序

def hybrid_search(query: str, documents: list, top_k: int = 5) -> list:
    """
    混合检索

    返回融合排序后的结果
    """
    # TODO: 实现代码
    pass

# 测试
documents = ["Python编程语言", "Java编程语言", "机器学习入门", "深度学习实践"]
results = hybrid_search("Python 入门", documents)
print(results)
```

#### 练习11：重排序实现

```python
# 实现检索结果重排序
# 要求：
# 1. 使用交叉编码器重排序
# 2. 提高检索精度
# 3. 评估重排序效果

def rerank_results(query: str, candidates: list, top_k: int = 5) -> list:
    """
    重排序检索结果

    返回重排序后的结果
    """
    # TODO: 实现代码
    pass

# 测试
candidates = ["相关文档1", "不太相关的文档", "非常相关的文档"]
reranked = rerank_results("查询问题", candidates, top_k=3)
```

#### 练习12：Agent 状态管理

```python
# 实现 Agent 状态管理
# 要求：
# 1. 维护对话状态
# 2. 管理工具调用历史
# 3. 支持状态恢复

class AgentStateManager:
    def __init__(self):
        self.conversation_history = []
        self.tool_call_history = []
        self.current_state = {}

    def update_state(self, user_input: str, agent_response: str):
        """更新状态"""
        # TODO: 实现代码
        pass

    def get_context(self) -> dict:
        """获取当前上下文"""
        # TODO: 实现代码
        pass

    def reset(self):
        """重置状态"""
        # TODO: 实现代码
        pass
```

#### 练习13：工具执行测试

```python
# 测试工具执行正确性
# 要求：
# 1. 模拟工具执行
# 2. 验证执行结果
# 3. 处理执行异常

class ToolExecutor:
    def __init__(self, tools: list):
        self.tools = {t["name"]: t for t in tools}

    def execute(self, tool_name: str, parameters: dict) -> dict:
        """
        执行工具

        返回：
        {
            "success": bool,
            "result": any,
            "error": str or None
        }
        """
        # TODO: 实现代码
        pass

    def validate_parameters(self, tool_name: str, parameters: dict) -> bool:
        """验证参数"""
        # TODO: 实现代码
        pass
```

#### 练习14：AI 生成测试用例

```python
# 使用 AI 生成测试用例
# 要求：
# 1. 根据需求生成测试用例
# 2. 生成边界值用例
# 3. 生成异常场景用例

class AITestCaseGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client

    def generate_functional_cases(self, requirement: str, count: int = 10) -> list:
        """生成功能测试用例"""
        # TODO: 实现代码
        pass

    def generate_edge_cases(self, function_spec: str) -> list:
        """生成边界值测试用例"""
        # TODO: 实现代码
        pass

    def generate_error_cases(self, function_spec: str) -> list:
        """生成异常测试用例"""
        # TODO: 实现代码
        pass
```

#### 练习15：幻觉检测与缓解

```python
# 实现 RAG 幻觉检测与缓解
# 要求：
# 1. 检测答案是否基于上下文
# 2. 标记可疑内容
# 3. 提供缓解策略

def detect_hallucination(answer: str, contexts: list) -> dict:
    """
    检测幻觉

    返回：
    {
        "has_hallucination": bool,
        "hallucinated_parts": list,
        "confidence": float
    }
    """
    # TODO: 实现代码
    pass

def mitigate_hallucination(answer: str, contexts: list) -> str:
    """
    缓解幻觉

    返回修正后的答案
    """
    # TODO: 实现代码
    pass
```

#### 练习16：Agent 安全性测试

```python
# 测试 Agent 安全性
# 要求：
# 1. 测试有害请求拒绝
# 2. 测试权限控制
# 3. 测试数据保护

class AgentSecurityTester:
    def __init__(self, agent):
        self.agent = agent

    def test_harmful_requests(self) -> dict:
        """测试有害请求拒绝"""
        # TODO: 实现代码
        pass

    def test_unauthorized_access(self) -> dict:
        """测试未授权访问"""
        # TODO: 实现代码
        pass

    def test_data_protection(self) -> dict:
        """测试数据保护"""
        # TODO: 实现代码
        pass
```

---

### 综合练习（17-20）

#### 练习17：完整 RAG 测试系统

```python
# 实现完整的 RAG 测试系统
# 要求：
# 1. 集成检索、生成、评估
# 2. 支持多种测试场景
# 3. 生成测试报告

class RAGTestSystem:
    def __init__(self, rag_system, llm_client):
        self.rag = rag_system
        self.llm = llm_client
        self.evaluator = RAGEvaluator(rag_system, llm_client)

    def run_retrieval_tests(self, test_cases: list) -> dict:
        """运行检索测试"""
        # TODO: 实现代码
        pass

    def run_generation_tests(self, test_cases: list) -> dict:
        """运行生成测试"""
        # TODO: 实现代码
        pass

    def run_end_to_end_tests(self, test_cases: list) -> dict:
        """运行端到端测试"""
        # TODO: 实现代码
        pass

    def generate_report(self) -> str:
        """生成测试报告"""
        # TODO: 实现代码
        pass
```

#### 练习18：完整 Agent 测试系统

```python
# 实现完整的 Agent 测试系统
# 要求：
# 1. 工具调用测试
# 2. 多轮对话测试
# 3. 安全性测试
# 4. 性能测试

class AgentTestSystem:
    def __init__(self, agent):
        self.agent = agent
        self.results = {}

    def test_tool_calling(self, test_cases: list) -> dict:
        """测试工具调用"""
        # TODO: 实现代码
        pass

    def test_multi_turn(self, conversations: list) -> dict:
        """测试多轮对话"""
        # TODO: 实现代码
        pass

    def test_safety(self, harmful_inputs: list) -> dict:
        """测试安全性"""
        # TODO: 实现代码
        pass

    def test_performance(self, test_cases: list) -> dict:
        """测试性能"""
        # TODO: 实现代码
        pass

    def run_all_tests(self) -> dict:
        """运行所有测试"""
        # TODO: 实现代码
        pass
```

#### 练习19：智能测试报告生成

```python
# 实现智能测试报告生成
# 要求：
# 1. 分析测试结果
# 2. 识别问题模式
# 3. 提供改进建议
# 4. 生成可视化报告

class TestReportGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client

    def analyze_results(self, test_results: dict) -> dict:
        """分析测试结果"""
        # TODO: 实现代码
        pass

    def identify_patterns(self, failures: list) -> list:
        """识别失败模式"""
        # TODO: 实现代码
        pass

    def generate_recommendations(self, analysis: dict) -> list:
        """生成改进建议"""
        # TODO: 实现代码
        pass

    def generate_report(self, test_results: dict, output_format: str = "markdown") -> str:
        """生成测试报告"""
        # TODO: 实现代码
        pass
```

#### 练习20：持续评估流水线

```python
# 实现持续评估流水线
# 要求：
# 1. 定期运行评估
# 2. 跟踪指标变化
# 3. 自动告警
# 4. 生成趋势报告

class ContinuousEvaluationPipeline:
    def __init__(self, config: dict):
        self.config = config
        self.history = []

    def run_evaluation(self) -> dict:
        """运行评估"""
        # TODO: 实现代码
        pass

    def track_metrics(self, results: dict):
        """跟踪指标"""
        # TODO: 实现代码
        pass

    def check_alerts(self, current_results: dict) -> list:
        """检查告警"""
        # TODO: 实现代码
        pass

    def generate_trend_report(self, days: int = 30) -> str:
        """生成趋势报告"""
        # TODO: 实现代码
        pass

    def schedule_evaluation(self, cron_expression: str):
        """定时调度评估"""
        # TODO: 实现代码
        pass
```

---

## 五、本周小结

1. **RAG 测试**：检索准确率 + 生成质量
2. **Agent 测试**：工具调用 + 多轮对话
3. **智能化测试**：AI 辅助测试

### 下周预告

第14周学习 LLM 评测和安全测试。
