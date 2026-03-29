# 第15周：RAG 系统测试

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

**场景说明：**
在企业知识库系统中，需要将文档转换为向量并存储到向量数据库中，以支持语义检索功能。

**具体需求：**
1. 使用 ChromaDB 创建一个文档集合
2. 实现添加文档向量的方法
3. 实现基于相似度的文档检索方法
4. 支持元数据存储和过滤查询

**使用示例：**
```python
import chromadb
from chromadb.config import Settings

class VectorStore:
    """向量存储类"""

    def __init__(self, collection_name: str = "documents"):
        self.client = chromadb.Client(Settings())
        self.collection = self.client.create_collection(collection_name)

    def add_documents(self, documents: list, ids: list, metadatas: list = None):
        """添加文档"""
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def search(self, query: str, top_k: int = 5, where: dict = None) -> list:
        """检索相似文档"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where
        )
        return results

# 测试
store = VectorStore()
store.add_documents(
    ["携程是旅行平台", "携程成立于1999年"],
    ["id1", "id2"],
    [{"category": "about"}, {"category": "history"}]
)
results = store.search("携程是什么", top_k=3)
print(results["documents"])
```

**验收标准：**
- [ ] 成功创建 ChromaDB 集合
- [ ] 能添加至少10条文档记录
- [ ] 检索结果按相似度正确排序
- [ ] 支持基于元数据的过滤查询

#### 练习2：文档分块

**场景说明：**
在构建 RAG 系统时，长文档需要被切分成适当大小的块，以便更好地进行向量化和检索。

**具体需求：**
1. 实现按字符数分块的方法，支持重叠设置
2. 实现按句子分块的方法，保持语义完整性
3. 处理中英文混合文本的分块
4. 确保分块后每个块不超过最大 token 限制

**使用示例：**
```python
import re

def chunk_by_chars(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    按字符数分块

    Args:
        text: 待分块的文本
        chunk_size: 每个块的最大字符数
        overlap: 块之间的重叠字符数

    Returns:
        分块后的文本列表
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # 如果不是最后一块，尝试在句子边界切分
        if end < len(text):
            # 查找最近的句子结束符
            last_period = max(
                chunk.rfind('。'),
                chunk.rfind('！'),
                chunk.rfind('？'),
                chunk.rfind('.')
            )
            if last_period > chunk_size // 2:
                chunk = chunk[:last_period + 1]
                end = start + last_period + 1

        chunks.append(chunk.strip())
        start = end - overlap

    return [c for c in chunks if c]  # 过滤空块

def chunk_by_sentences(text: str, max_sentences: int = 5) -> list:
    """按句子分块"""
    # 按中英文句子分隔符分割
    sentences = re.split(r'(?<=[。！？.!?])\s*', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunk = ''.join(sentences[i:i + max_sentences])
        chunks.append(chunk)

    return chunks

# 测试
text = "这是第一句话。这是第二句话。这是第三句话。这是第四句话。这是第五句话。这是第六句话。" * 10
chunks = chunk_by_chars(text, chunk_size=200, overlap=20)
print(f"字符分块数量: {len(chunks)}")

chunks = chunk_by_sentences(text, max_sentences=3)
print(f"句子分块数量: {len(chunks)}")
```

**验收标准：**
- [ ] 字符分块功能正确，块大小不超过指定限制
- [ ] 重叠分块功能正确，相邻块有适当重叠
- [ ] 句子分块保持句子完整性，不在句子中间切分
- [ ] 能处理包含中英文标点的混合文本

#### 练习3：简单 RAG 系统实现

**场景说明：**
在客服机器人项目中，需要构建一个基础的 RAG 系统，将企业知识库文档索引化，并根据用户问题检索相关内容，为 LLM 提供上下文支持。

**具体需求：**
1. 实现文档索引功能，支持批量添加文档
2. 实现相似度检索方法，返回最相关的 top_k 个文档
3. 实现上下文构建方法，将检索结果拼接成格式化的上下文
4. 支持更新和删除文档

**使用示例：**
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

**验收标准：**
- [ ] 成功构建文档索引，支持至少100条文档
- [ ] 检索方法能返回按相似度排序的结果
- [ ] 上下文构建方法输出格式化的字符串
- [ ] 检索延迟在可接受范围内（<500ms）

#### 练习4：检索质量评估

**场景说明：**
在 RAG 系统上线后，需要定期评估检索模块的质量，通过计算 Precision、Recall、F1 等指标来监控检索效果，确保用户能获取到最相关的知识。

**具体需求：**
1. 实现 Precision@K 指标计算，衡量检索结果的精确度
2. 实现 Recall@K 指标计算，衡量相关文档的召回率
3. 实现 F1 分数计算，综合评估检索效果
4. 支持批量测试用例的评估和平均指标计算

**使用示例：**
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

**验收标准：**
- [ ] Precision@K 计算正确，值在 0-1 范围内
- [ ] Recall@K 计算正确，能正确处理空集合情况
- [ ] F1 分数计算正确，能处理 Precision 或 Recall 为 0 的情况
- [ ] 函数返回字典包含 precision、recall、f1 三个键

#### 练习5：Agent 工具调用测试

**场景说明：**
在旅行助手 Agent 开发中，需要验证 Agent 能否根据用户意图正确选择调用哪个工具，例如用户说"搜索酒店"时应调用 search_hotel 工具。

**具体需求：**
1. 定义工具列表，包含工具名称、描述和参数说明
2. 实现工具调用测试函数，验证 Agent 是否调用了正确的工具
3. 支持多种用户表达方式的测试（如"帮我找酒店"、"查一下酒店"）
4. 返回详细的测试结果，包括调用状态和错误信息

**使用示例：**
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

**验收标准：**
- [ ] 工具定义完整，包含名称、描述、参数三个字段
- [ ] 测试函数能正确判断工具调用是否匹配预期
- [ ] 支持至少5种不同的用户表达方式测试
- [ ] 测试通过率达到90%以上

#### 练习6：参数提取测试

**场景说明：**
在智能客服 Agent 中，用户输入往往是自然语言，需要从中准确提取工具所需的结构化参数，如从"预订明天北京飞上海的机票"中提取出发地、目的地、日期等信息。

**具体需求：**
1. 实现从自然语言中提取结构化参数的函数
2. 识别必填参数和可选参数的缺失情况
3. 返回提取置信度，用于判断是否需要用户确认
4. 处理日期、时间、地点等特殊类型的参数解析

**使用示例：**
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

**验收标准：**
- [ ] 能正确提取城市、日期等基本参数
- [ ] 能识别缺失的必填参数并返回 missing 列表
- [ ] 置信度计算合理，范围在 0-1 之间
- [ ] 参数提取准确率达到85%以上

#### 练习7：多轮对话测试

**场景说明：**
在酒店预订场景中，用户往往需要多轮交互才能完成任务，例如先搜索酒店、再查看详情、最后预订。Agent 需要正确理解上下文中的指代（如"第一个"、"这个"）。

**具体需求：**
1. 实现多轮对话测试函数，支持连续对话场景
2. 正确处理代词指代，将"这个"、"第一个"映射到上下文中的具体对象
3. 维护对话状态，记录每轮的输入、输出和预期结果
4. 计算整体通过率，支持部分通过的评分

**使用示例：**
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

**验收标准：**
- [ ] 能正确处理至少3轮的连续对话
- [ ] 代词指代解析准确率达到80%以上
- [ ] 返回结果包含每轮对话的详细状态
- [ ] 整体通过率计算正确

#### 练习8：RAG 上下文构建

**场景说明：**
在 RAG 系统中，检索到的多个文档片段需要被组织成结构化的上下文，供 LLM 理解和生成答案。同时需要控制总长度，避免超出模型的 token 限制。

**具体需求：**
1. 实现上下文构建函数，将检索结果格式化为结构化文本
2. 支持按相关性排序组织文档片段
3. 实现 token 估算功能，控制上下文总长度不超过限制
4. 当超出长度限制时，智能截断低相关性内容

**使用示例：**
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

**验收标准：**
- [ ] 上下文输出格式清晰，包含来源标识
- [ ] Token 估算功能准确，误差在10%以内
- [ ] 超长内容能被正确截断，不破坏语义完整性
- [ ] 支持自定义上下文模板格式

---

### 进阶练习（9-16）

#### 练习9：RAG 系统完整评估

**场景说明：**
在 RAG 系统上线前，需要进行全面的质量评估，包括检索是否准确、生成答案是否优质、是否存在幻觉等问题，以确保系统达到生产标准。

**具体需求：**
1. 实现检索质量评估方法，计算 Precision、Recall、MRR 等指标
2. 实现生成质量评估方法，使用语义相似度评估答案质量
3. 实现忠实度评估方法，检测答案是否基于上下文生成（幻觉检测）
4. 实现综合评估方法，汇总所有指标生成评估报告

**使用示例：**
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

**验收标准：**
- [ ] 检索评估返回 precision、recall、mrr 三个核心指标
- [ ] 生成评估使用语义相似度计算，阈值可配置
- [ ] 忠实度评估能识别明显的幻觉内容
- [ ] 综合评估输出包含所有指标的汇总报告

#### 练习10：混合检索实现

**场景说明：**
在实际的 RAG 系统中，单纯的向量检索可能无法满足所有场景。需要结合向量语义检索和 BM25 关键词检索，通过融合排序提高检索的准确性和覆盖率。

**具体需求：**
1. 实现向量相似度检索，使用 Embedding 模型计算语义相似度
2. 实现 BM25 关键词检索，处理精确匹配场景
3. 实现 Reciprocal Rank Fusion (RRF) 或加权融合算法
4. 支持自定义两种检索方式的权重比例

**使用示例：**
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

**验收标准：**
- [ ] 向量检索和关键词检索分别实现并可独立调用
- [ ] 融合排序结果合理，兼顾语义相关性和关键词匹配
- [ ] 支持配置向量检索和关键词检索的权重
- [ ] 混合检索效果优于单一检索方式（通过评估验证）

#### 练习11：重排序实现

**场景说明：**
在 RAG 系统的检索流程中，初步检索可能返回大量结果，需要通过重排序（Rerank）模型对候选结果进行精细化排序，将最相关的文档排在前面，提高检索精度。

**具体需求：**
1. 实现基于交叉编码器（Cross-Encoder）的重排序方法
2. 支持批量处理候选文档，提高排序效率
3. 返回重排序后的文档列表及相关性分数
4. 提供重排序前后的效果对比评估

**使用示例：**
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

**验收标准：**
- [ ] 重排序函数能正确处理 query 和候选文档列表
- [ ] 返回结果按相关性分数降序排列
- [ ] 支持 top_k 参数控制返回数量
- [ ] 重排序后检索准确率有明显提升

#### 练习12：Agent 状态管理

**场景说明：**
在复杂的 Agent 对话场景中，需要管理用户的对话历史、工具调用记录和当前状态，以支持多轮对话的上下文理解和状态恢复功能。

**具体需求：**
1. 维护对话历史记录，支持查询和限制历史长度
2. 管理工具调用历史，记录每次调用的参数和结果
3. 实现状态保存和恢复功能，支持会话持久化
4. 提供上下文摘要功能，避免历史过长影响性能

**使用示例：**
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

**验收标准：**
- [ ] 对话历史正确记录每轮的用户输入和 Agent 响应
- [ ] 工具调用历史包含工具名、参数、执行结果和时间戳
- [ ] reset 方法能完全清空当前会话状态
- [ ] 支持导出和导入状态（JSON 格式）

#### 练习13：工具执行测试

**场景说明：**
在 Agent 系统中，工具的执行结果直接影响用户体验。需要实现工具执行器来统一管理工具调用，包括参数验证、执行监控和异常处理。

**具体需求：**
1. 实现工具执行器，统一管理工具的注册和调用
2. 实现参数验证功能，检查必填参数和参数类型
3. 实现执行结果封装，包含成功状态、结果和错误信息
4. 处理执行异常，支持超时控制和重试机制

**使用示例：**
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

**验收标准：**
- [ ] execute 方法返回统一格式的结果字典
- [ ] 参数验证能检测缺失的必填参数和类型错误
- [ ] 能捕获并记录工具执行过程中的异常
- [ ] 支持设置执行超时时间

#### 练习14：AI 生成测试用例

**场景说明：**
在测试工作中，手动编写测试用例耗时耗力。利用 LLM 可以根据需求文档自动生成测试用例，覆盖功能、边界和异常场景，提高测试效率。

**具体需求：**
1. 实现根据需求描述生成功能测试用例的方法
2. 实现根据函数规格生成边界值测试用例的方法
3. 实现生成异常场景测试用例的方法
4. 输出格式化的测试用例，包含步骤和预期结果

**使用示例：**
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

**验收标准：**
- [ ] 功能测试用例覆盖主要业务场景
- [ ] 边界值用例包含空值、最大值、最小值等边界情况
- [ ] 异常用例包含参数错误、权限不足等异常场景
- [ ] 生成的测试用例格式统一，包含用例ID、步骤、预期结果

#### 练习15：幻觉检测与缓解

**场景说明：**
在 RAG 系统中，LLM 可能会生成与上下文不符的内容（幻觉），影响答案的可靠性。需要实现幻觉检测机制，识别不可信的内容并提供缓解策略。

**具体需求：**
1. 实现幻觉检测函数，判断答案是否基于提供的上下文
2. 标记答案中可能产生幻觉的具体内容片段
3. 返回检测置信度，用于判断是否需要人工审核
4. 实现幻觉缓解函数，尝试修正或标注不可信内容

**使用示例：**
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

**验收标准：**
- [ ] 幻觉检测能识别明显与上下文矛盾的内容
- [ ] 返回的 hallucinated_parts 列表包含可疑片段
- [ ] 置信度合理反映检测的可信程度
- [ ] 缓解函数能标注或移除幻觉内容

#### 练习16：Agent 安全性测试

**场景说明：**
Agent 系统直接面向用户，可能面临各种恶意输入和攻击尝试。需要全面测试 Agent 的安全性，确保其能拒绝有害请求、正确处理权限控制和保护敏感数据。

**具体需求：**
1. 实现有害请求拒绝测试，验证 Agent 能识别并拒绝危险指令
2. 实现未授权访问测试，验证权限控制机制的有效性
3. 实现数据保护测试，验证敏感信息不会被泄露
4. 汇总测试结果，生成安全性评估报告

**使用示例：**
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

**验收标准：**
- [ ] 有害请求拒绝率达到95%以上
- [ ] 未授权访问能被正确拦截并返回权限错误
- [ ] 敏感数据（如密码、身份证号）不会被返回给用户
- [ ] 测试报告包含各类安全测试的详细结果

---

### 综合练习（17-20）

#### 练习17：完整 RAG 测试系统

**场景说明：**
在企业级 RAG 系统开发中，需要一套完整的测试系统来覆盖检索、生成、端到端等各个环节，并能自动生成测试报告，支持持续集成和质量监控。

**具体需求：**
1. 集成检索测试、生成测试和端到端测试功能
2. 支持多种测试场景，包括单轮问答、多轮对话、边界情况等
3. 实现测试报告生成功能，包含指标汇总和问题分析
4. 支持测试配置管理，可自定义测试用例和阈值

**使用示例：**
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

**验收标准：**
- [ ] 三种测试类型（检索、生成、端到端）均能正确执行
- [ ] 测试结果包含详细的指标数据和通过率
- [ ] 测试报告格式清晰，支持 Markdown 或 HTML 输出
- [ ] 支持从配置文件加载测试用例

#### 练习18：完整 Agent 测试系统

**场景说明：**
在 Agent 产品发布前，需要进行全面的功能和非功能测试，包括工具调用准确性、多轮对话一致性、安全性和性能表现，确保 Agent 在各种场景下都能正常工作。

**具体需求：**
1. 实现工具调用测试模块，验证工具选择和参数提取的准确性
2. 实现多轮对话测试模块，验证上下文理解和状态管理
3. 实现安全性测试模块，验证有害请求拒绝和权限控制
4. 实现性能测试模块，测试响应时间和资源消耗
5. 提供 run_all_tests 方法一键运行所有测试

**使用示例：**
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

**验收标准：**
- [ ] 四种测试模块均能独立运行并返回结果
- [ ] run_all_tests 方法汇总所有测试结果
- [ ] 性能测试包含响应时间、吞吐量等指标
- [ ] 测试结果支持导出为 JSON 格式

#### 练习19：智能测试报告生成

**场景说明：**
测试执行后会产生大量数据，需要通过智能分析自动识别问题模式、生成改进建议，并输出易读的测试报告，帮助开发团队快速定位和解决问题。

**具体需求：**
1. 实现测试结果分析功能，统计通过率、失败原因分布等
2. 实现问题模式识别，自动归类相似的失败案例
3. 利用 LLM 生成改进建议，提供具体的修复方向
4. 支持生成 Markdown 或 HTML 格式的可视化报告

**使用示例：**
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

**验收标准：**
- [ ] 分析结果包含通过率、失败分布等关键统计
- [ ] 能识别至少3种常见的失败模式
- [ ] 改进建议具体可行，与失败原因相关
- [ ] 报告格式清晰，包含图表或表格展示

#### 练习20：持续评估流水线

**场景说明：**
在生产环境中，RAG 系统和 Agent 的效果会随着数据更新、模型变化而波动。需要建立持续评估流水线，定期运行评估、跟踪指标变化、及时发现异常。

**具体需求：**
1. 实现定期评估调度功能，支持 cron 表达式配置
2. 实现指标跟踪功能，记录历史评估结果
3. 实现告警检查功能，当指标下降超过阈值时触发告警
4. 实现趋势报告生成，展示指标变化趋势和异常点

**使用示例：**
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

**验收标准：**
- [ ] 支持 cron 表达式配置定时评估
- [ ] 历史记录持久化存储，支持查询指定时间范围
- [ ] 告警阈值可配置，支持多级告警
- [ ] 趋势报告包含指标变化曲线和异常标注

---

## 五、本周小结

1. **RAG 测试**：检索准确率 + 生成质量
2. **Agent 测试**：工具调用 + 多轮对话
3. **智能化测试**：AI 辅助测试

### 下周预告

第14周学习 LLM 评测和安全测试。
