# 第15周：RAG 与 Agent 测试

## 本周目标

掌握 RAG（检索增强生成）系统和 AI Agent 的测试方法，能够设计和实现智能化测试方案。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| RAG 原理 | 检索、生成、融合 | ⭐⭐⭐⭐⭐ |
| 向量数据库 | Chroma、Pinecone、Milvus | ⭐⭐⭐⭐ |
| Embedding | 文本嵌入、相似度计算 | ⭐⭐⭐⭐⭐ |
| RAG 评测 | 准确性、召回率、相关性 | ⭐⭐⭐⭐⭐ |
| Agent 测试 | 工具调用、规划、执行 | ⭐⭐⭐⭐⭐ |
| 智能化测试 | AI 驱动的测试生成 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 RAG 系统原理

```
RAG（Retrieval-Augmented Generation）= 检索 + 生成

核心流程：
1. 文档处理：分块 → 向量化 → 存储
2. 查询处理：问题 → 向量化 → 检索相关文档
3. 生成回答：问题 + 检索结果 → LLM → 回答

优势：
- 减少幻觉（基于真实文档）
- 支持私有知识
- 可追溯来源
- 易于更新知识

测试重点：
- 检索准确性：能否找到相关文档
- 生成质量：回答是否基于检索内容
- 端到端性能：响应时间
```

---

### 2.2 向量数据库

```python
# 使用 Chroma 向量数据库
import chromadb
from chromadb.config import Settings

class VectorStore:
    """向量存储"""

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = None

    def create_collection(self, name: str = "documents"):
        """创建集合"""
        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[dict]):
        """添加文档"""
        ids = [doc["id"] for doc in documents]
        texts = [doc["content"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]

        self.collection.add(
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )

    def search(self, query: str, n_results: int = 5) -> dict:
        """搜索相似文档"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def delete_collection(self, name: str):
        """删除集合"""
        self.client.delete_collection(name)
```

---

### 2.3 RAG 评测指标

```python
from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class EvaluationResult:
    """评测结果"""
    metric: str
    score: float
    details: dict = None

class RAGEvaluator:
    """RAG 系统评测器"""

    def __init__(self, rag_system):
        self.rag = rag_system

    def evaluate_retrieval(
        self,
        questions: List[str],
        relevant_doc_ids: List[List[str]],
        k_values: List[int] = [1, 3, 5, 10]
    ) -> dict:
        """评测检索质量"""
        results = {}

        for k in k_values:
            precision_scores = []
            recall_scores = []
            mrr_scores = []

            for question, relevant_ids in zip(questions, relevant_doc_ids):
                retrieved = self.rag.retrieve(question, top_k=k)
                retrieved_ids = [r.document.id for r in retrieved]

                # Precision@K
                hits = len(set(retrieved_ids) & set(relevant_ids))
                precision = hits / k
                precision_scores.append(precision)

                # Recall@K
                recall = hits / len(relevant_ids) if relevant_ids else 0
                recall_scores.append(recall)

                # MRR
                for rank, doc_id in enumerate(retrieved_ids, 1):
                    if doc_id in relevant_ids:
                        mrr_scores.append(1.0 / rank)
                        break
                else:
                    mrr_scores.append(0.0)

            results[f"precision@{k}"] = np.mean(precision_scores)
            results[f"recall@{k}"] = np.mean(recall_scores)
            results[f"mrr@{k}"] = np.mean(mrr_scores)

        return results

    def evaluate_generation(
        self,
        questions: List[str],
        ground_truths: List[str]
    ) -> dict:
        """评测生成质量"""
        results = {"relevance": [], "faithfulness": []}

        for question, ground_truth in zip(questions, ground_truths):
            response = self.rag.query(question)
            answer = response["answer"]

            # 相关性评分
            relevance = self._compute_relevance(answer, question)
            results["relevance"].append(relevance)

            # 忠实度评分
            context = [s["content"] for s in response["sources"]]
            faithfulness = self._compute_faithfulness(answer, context)
            results["faithfulness"].append(faithfulness)

        return {k: np.mean(v) for k, v in results.items()}

    def _compute_relevance(self, answer: str, question: str) -> float:
        """计算相关性"""
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        overlap = len(question_words & answer_words)
        return min(overlap / len(question_words), 1.0) if question_words else 0

    def _compute_faithfulness(self, answer: str, context: List[str]) -> float:
        """计算忠实度"""
        context_text = " ".join(context).lower()
        answer_words = answer.lower().split()
        supported = sum(1 for word in answer_words if word in context_text)
        return supported / len(answer_words) if answer_words else 0
```

---

### 2.4 Agent 测试

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class ToolType(Enum):
    SEARCH = "search"
    CALCULATOR = "calculator"
    DATABASE = "database"
    API = "api"

@dataclass
class ToolCall:
    """工具调用记录"""
    tool_name: str
    arguments: dict
    result: Any
    timestamp: float

@dataclass
class AgentTrace:
    """Agent 执行轨迹"""
    task: str
    plan: List[str]
    tool_calls: List[ToolCall]
    final_answer: str
    success: bool
    error: Optional[str] = None

class AgentTester:
    """Agent 测试器"""

    def __init__(self, agent):
        self.agent = agent
        self.traces: List[AgentTrace] = []

    def run_task(self, task: str) -> AgentTrace:
        """运行任务并记录轨迹"""
        result = self.agent.run(task)

        trace = AgentTrace(
            task=task,
            plan=result.get("plan", []),
            tool_calls=result.get("tool_calls", []),
            final_answer=result.get("answer", ""),
            success=result.get("success", False),
            error=result.get("error")
        )
        self.traces.append(trace)
        return trace

    def test_tool_selection(self, test_cases: List[dict]) -> dict:
        """测试工具选择正确性"""
        correct = 0
        total = len(test_cases)

        for tc in test_cases:
            trace = self.run_task(tc["task"])
            expected_tools = set(tc["expected_tools"])
            actual_tools = set(tc.tool_name for tc in trace.tool_calls)

            if expected_tools.issubset(actual_tools):
                correct += 1

        return {
            "tool_selection_accuracy": correct / total if total > 0 else 0,
            "correct": correct,
            "total": total
        }

    def test_task_completion(self, test_cases: List[dict]) -> dict:
        """测试任务完成率"""
        completed = 0
        total = len(test_cases)

        for tc in test_cases:
            trace = self.run_task(tc["task"])
            if trace.success:
                if self._verify_answer(trace.final_answer, tc.get("expected_answer")):
                    completed += 1

        return {
            "task_completion_rate": completed / total if total > 0 else 0,
            "completed": completed,
            "total": total
        }

    def _verify_answer(self, actual: str, expected: str = None) -> bool:
        """验证答案"""
        if not expected:
            return len(actual) > 10
        actual_words = set(actual.lower().split())
        expected_words = set(expected.lower().split())
        overlap = len(actual_words & expected_words)
        return overlap / len(expected_words) > 0.5 if expected_words else True

    def analyze_traces(self) -> dict:
        """分析执行轨迹"""
        if not self.traces:
            return {"error": "没有执行轨迹"}

        total = len(self.traces)
        successful = sum(1 for t in self.traces if t.success)

        tool_usage = {}
        for trace in self.traces:
            for tc in trace.tool_calls:
                tool_usage[tc.tool_name] = tool_usage.get(tc.tool_name, 0) + 1

        avg_steps = np.mean([len(t.plan) for t in self.traces])

        return {
            "total_tasks": total,
            "success_rate": successful / total,
            "tool_usage": tool_usage,
            "avg_planning_steps": avg_steps
        }
```

---

### 2.5 智能化测试

```python
from typing import List, Dict, Any
import json

class AITestGenerator:
    """AI 驱动的测试生成器"""

    def __init__(self, llm):
        self.llm = llm

    def generate_test_cases(self, api_spec: dict, count: int = 10) -> List[dict]:
        """根据 API 规范生成测试用例"""
        prompt = f"""
        根据以下 API 规范生成 {count} 个测试用例：

        API 规范：
        {json.dumps(api_spec, indent=2, ensure_ascii=False)}

        请生成包含以下类型的测试用例：
        1. 正常场景测试
        2. 边界值测试
        3. 异常场景测试
        4. 安全测试

        输出 JSON 格式的测试用例列表。
        """

        response = self.llm.generate(prompt)
        return json.loads(response)

    def generate_edge_cases(self, field_type: str) -> List[Any]:
        """生成边界测试值"""
        edge_cases = {
            "string": ["", " ", "a" * 1000, "<script>alert(1)</script>"],
            "integer": [0, -1, 1, 2**31 - 1, -2**31],
            "float": [0.0, -0.0, 0.1, 1e10, float('inf')],
            "email": ["test@test.com", "invalid", "@test.com", ""]
        }
        return edge_cases.get(field_type, [])

    def generate_assertions(self, response: dict) -> List[str]:
        """根据响应生成断言"""
        assertions = ["assert response.status_code == 200"]

        if "data" in response:
            assertions.append("assert 'data' in response.json()")

            for key, value in response.get("data", {}).items():
                if isinstance(value, str):
                    assertions.append(f"assert isinstance(response.json()['data']['{key}'], str)")

        return assertions


class SelfHealingTestRunner:
    """带自愈能力的测试运行器"""

    def __init__(self, llm):
        self.generator = AITestGenerator(llm)
        self.results = []

    def run_with_healing(self, test_func, *args, **kwargs):
        """运行测试，失败时尝试自愈"""
        try:
            test_func(*args, **kwargs)
            return {"status": "passed", "test": test_func.__name__}
        except AssertionError as e:
            fix_result = self._try_fix_test(test_func, str(e))
            if fix_result:
                return {"status": "fixed", "test": test_func.__name__, "fix": fix_result}
            return {"status": "failed", "test": test_func.__name__, "error": str(e)}

    def _try_fix_test(self, test_func, error: str) -> str:
        """尝试修复失败的测试"""
        if "status_code" in error:
            return "更新期望状态码"
        elif "timeout" in error:
            return "增加超时时间"
        return None
```

---

## 三、学到什么程度

### 必须掌握

- [ ] RAG 系统的工作原理
- [ ] 向量相似度计算
- [ ] 检索评测指标（Precision、Recall、MRR）
- [ ] Agent 测试的基本方法

### 应该了解

- [ ] 向量数据库的使用
- [ ] 生成质量评测
- [ ] 智能化测试生成
- [ ] Agent 执行轨迹分析

---

## 四、练习内容

### 基础练习（1-8）

#### 练习1：向量相似度计算

```python
# tests/test_similarity.py
# 要求：
# 1. 实现余弦相似度计算
# 2. 实现欧几里得距离
# 3. 测试不同相似度度量

import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """计算欧几里得距离"""
    return np.linalg.norm(a - b)

def test_cosine_similarity():
    a = np.array([1, 0, 0])
    b = np.array([1, 0, 0])
    assert cosine_similarity(a, b) == 1.0

    c = np.array([0, 1, 0])
    assert cosine_similarity(a, c) == 0.0

    d = np.array([1, 1, 0])
    assert 0 < cosine_similarity(a, d) < 1
```

#### 练习2：文档分块

```python
# tests/test_chunking.py
# 要求：
# 1. 实现固定大小分块
# 2. 实现按句子分块
# 3. 实现重叠分块

import re

def chunk_by_size(text: str, chunk_size: int = 500) -> list:
    """按固定大小分块"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def chunk_by_sentence(text: str) -> list:
    """按句子分块"""
    sentences = re.split(r'[。！？.!?]', text)
    return [s.strip() for s in sentences if s.strip()]

def chunk_with_overlap(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """带重叠的分块"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def test_chunking():
    text = "这是一个测试文本。" * 100

    chunks = chunk_by_size(text, 50)
    assert all(len(c) <= 50 for c in chunks)

    sentences = chunk_by_sentence(text)
    assert len(sentences) > 0
```

#### 练习3：简单 RAG 检索

```python
# tests/test_rag_retrieval.py
# 要求：
# 1. 实现文档索引
# 2. 实现相似度检索
# 3. 返回 top-k 结果

import numpy as np
from typing import List, Tuple

class SimpleRetriever:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    def index(self, documents: List[str], embedding_func):
        """索引文档"""
        self.documents = documents
        self.embeddings = [embedding_func(doc) for doc in documents]

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[int, float]]:
        """搜索相似文档"""
        similarities = []
        for i, emb in enumerate(self.embeddings):
            sim = cosine_similarity(query_embedding, emb)
            similarities.append((i, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:k]

def test_retrieval():
    retriever = SimpleRetriever()
    # 测试代码
    pass
```

#### 练习4：RAG 评测指标

```python
# tests/test_rag_metrics.py
# 要求：
# 1. 实现 Precision@K
# 2. 实现 Recall@K
# 3. 实现 MRR

def precision_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    """计算 Precision@K"""
    retrieved_k = set(retrieved[:k])
    relevant_set = set(relevant)
    return len(retrieved_k & relevant_set) / k

def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    """计算 Recall@K"""
    retrieved_k = set(retrieved[:k])
    relevant_set = set(relevant)
    return len(retrieved_k & relevant_set) / len(relevant_set) if relevant_set else 0

def mean_reciprocal_rank(ranking_lists: List[List[str]], relevant_lists: List[List[str]]) -> float:
    """计算 MRR"""
    rr_sum = 0
    for ranking, relevant in zip(ranking_lists, relevant_lists):
        relevant_set = set(relevant)
        for rank, doc in enumerate(ranking, 1):
            if doc in relevant_set:
                rr_sum += 1.0 / rank
                break
    return rr_sum / len(ranking_lists) if ranking_lists else 0

def test_metrics():
    retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
    relevant = ["doc1", "doc3", "doc6"]

    p5 = precision_at_k(retrieved, relevant, 5)
    assert p5 == 2 / 5

    r5 = recall_at_k(retrieved, relevant, 5)
    assert r5 == 2 / 3
```

#### 练习5：向量数据库使用

```python
# tests/test_vector_db.py
# 要求：
# 1. 创建向量集合
# 2. 添加文档
# 3. 执行搜索
# 4. 删除文档

import pytest

def test_vector_db_operations():
    """测试向量数据库操作"""
    # 使用内存数据库进行测试
    import chromadb

    client = chromadb.Client()
    collection = client.create_collection("test_docs")

    # 添加文档
    collection.add(
        documents=["文档1", "文档2", "文档3"],
        ids=["1", "2", "3"]
    )

    # 搜索
    results = collection.query(
        query_texts=["文档"],
        n_results=2
    )

    assert len(results["ids"][0]) == 2

    # 删除
    collection.delete(ids=["1"])
    assert collection.count() == 2
```

#### 练习6：Agent 工具调用测试

```python
# tests/test_agent_tools.py
# 要求：
# 1. 定义工具
# 2. 测试工具调用
# 3. 验证返回结果

from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Tool:
    name: str
    description: str
    func: Callable

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def call(self, name: str, **kwargs) -> Any:
        return self.tools[name].func(**kwargs)

def calculator(expression: str) -> float:
    """简单计算器"""
    return eval(expression)

def test_tool_registry():
    registry = ToolRegistry()
    registry.register(Tool(
        name="calculator",
        description="执行数学计算",
        func=calculator
    ))

    result = registry.call("calculator", expression="2 + 2")
    assert result == 4
```

#### 练习7：Agent 执行轨迹

```python
# tests/test_agent_trace.py
# 要求：
# 1. 记录工具调用
# 2. 记录执行步骤
# 3. 分析轨迹

from typing import List, Any
from dataclasses import dataclass, field

@dataclass
class ToolCall:
    tool_name: str
    arguments: dict
    result: Any
    timestamp: float

class AgentTracer:
    def __init__(self):
        self.traces: List[ToolCall] = []

    def trace_tool_call(self, tool_name: str, args: dict, result: Any):
        """记录工具调用"""
        import time
        self.traces.append(ToolCall(
            tool_name=tool_name,
            arguments=args,
            result=result,
            timestamp=time.time()
        ))

    def get_trace_summary(self) -> dict:
        """获取轨迹摘要"""
        tool_usage = {}
        for trace in self.traces:
            tool_usage[trace.tool_name] = tool_usage.get(trace.tool_name, 0) + 1

        return {
            "total_calls": len(self.traces),
            "tool_usage": tool_usage
        }

def test_tracing():
    tracer = AgentTracer()
    tracer.trace_tool_call("search", {"query": "Python"}, ["result1"])
    tracer.trace_tool_call("calculator", {"expr": "1+1"}, 2)

    summary = tracer.get_trace_summary()
    assert summary["total_calls"] == 2
    assert "search" in summary["tool_usage"]
```

#### 练习8：测试数据生成

```python
# tests/test_data_generation.py
# 要求：
# 1. 生成边界值测试数据
# 2. 生成随机测试数据
# 3. 生成负面测试数据

import random
import string

def generate_edge_values(field_type: str) -> List[Any]:
    """生成边界值"""
    edge_cases = {
        "int": [0, -1, 1, 2**31-1, -2**31],
        "string": ["", " ", "a" * 1000],
        "email": ["test@test.com", "invalid", ""]
    }
    return edge_cases.get(field_type, [])

def generate_random_user() -> dict:
    """生成随机用户数据"""
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    return {
        "username": username,
        "email": f"{username}@test.com",
        "age": random.randint(18, 80)
    }

def test_data_generation():
    int_edges = generate_edge_values("int")
    assert 0 in int_edges

    user = generate_random_user()
    assert "username" in user
    assert "email" in user
```

---

### 进阶练习（9-16）

#### 练习9：完整 RAG 系统测试

```python
# tests/test_rag_complete.py
# 要求：
# 1. 测试文档索引
# 2. 测试检索质量
# 3. 测试生成质量
# 4. 端到端测试

import pytest

class TestRAGSystem:
    @pytest.fixture
    def rag_system(self):
        """初始化 RAG 系统"""
        pass

    def test_document_indexing(self, rag_system):
        """测试文档索引"""
        docs = ["文档1内容", "文档2内容"]
        rag_system.add_documents(docs)
        assert rag_system.document_count() == 2

    def test_retrieval_quality(self, rag_system):
        """测试检索质量"""
        results = rag_system.retrieve("查询", k=5)
        assert len(results) <= 5
```

#### 练习10：RAG 性能测试

```python
# tests/test_rag_performance.py
# 要求：
# 1. 测试索引性能
# 2. 测试查询性能
# 3. 测试并发性能

import time
from concurrent.futures import ThreadPoolExecutor

def test_query_performance(rag_system):
    """测试查询性能"""
    start = time.time()
    for _ in range(100):
        rag_system.query("测试查询")
    elapsed = time.time() - start
    assert elapsed / 100 < 1  # 平均每次查询 < 1s
```

#### 练习11：Agent 规划测试

```python
# tests/test_agent_planning.py
# 要求：
# 1. 测试任务分解
# 2. 测试步骤排序
# 3. 测试依赖处理

def test_task_planning():
    planner = AgentPlanner()
    plan = planner.plan("搜索天气并计算平均温度")
    assert "search" in " ".join(plan).lower()
    assert "calculate" in " ".join(plan).lower()
```

#### 练习12：Agent 错误处理测试

```python
# tests/test_agent_errors.py
# 要求：
# 1. 测试工具不存在
# 2. 测试参数错误
# 3. 测试超时处理

def test_tool_not_found(agent):
    with pytest.raises(ValueError):
        agent.call_tool("nonexistent_tool")

def test_timeout_handling(agent):
    with pytest.raises(TimeoutError):
        agent.run_with_timeout("long_task", timeout=0.1)
```

#### 练习13：智能测试生成

```python
# tests/test_ai_generation.py
# 要求：
# 1. 根据 API 规范生成测试
# 2. 生成边界测试用例
# 3. 生成安全测试用例

class TestGenerator:
    def generate_from_spec(self, api_spec: dict) -> List[dict]:
        """根据 API 规范生成测试"""
        tests = []
        # 正常场景
        tests.append({
            "name": "正常创建",
            "endpoint": api_spec["endpoint"],
            "expected_status": 201
        })
        # 异常场景
        tests.append({
            "name": "缺少必填字段",
            "body": {},
            "expected_status": 400
        })
        return tests
```

#### 练习14：测试自愈系统

```python
# tests/test_self_healing.py
# 要求：
# 1. 检测测试失败
# 2. 分析失败原因
# 3. 尝试自动修复

class SelfHealingTestRunner:
    def run_with_healing(self, test_func):
        try:
            test_func()
            return {"status": "passed"}
        except AssertionError as e:
            error_type = self._analyze_error(str(e))
            return {"status": "failed", "error_type": error_type}
```

#### 练习15：RAG 评测报告

```python
# tests/test_rag_report.py
# 要求：
# 1. 收集评测数据
# 2. 计算综合指标
# 3. 生成报告

class EvaluationReport:
    def __init__(self):
        self.metrics = {}
        self.test_cases = []

    def add_result(self, metric: str, value: float):
        self.metrics[metric] = value

    def generate_summary(self) -> dict:
        return {
            "total_tests": len(self.test_cases),
            "metrics": self.metrics
        }
```

#### 练习16：多模态 RAG 测试

```python
# tests/test_multimodal_rag.py
# 要求：
# 1. 测试文本检索
# 2. 测试图像检索
# 3. 测试混合检索

def test_text_retrieval(multimodal_rag):
    multimodal_rag.add_text("测试文本")
    results = multimodal_rag.search_text("测试")
    assert len(results) > 0

def test_mixed_retrieval(multimodal_rag):
    results = multimodal_rag.search_mixed(
        text_query="测试",
        text_weight=0.6
    )
    assert len(results) > 0
```

---

### 综合练习（17-20）

#### 练习17：企业级 RAG 测试框架

```python
# 综合练习：构建企业级 RAG 测试框架
# 要求：
# 1. 模块化设计
# 2. 支持多种评测指标
# 3. 支持自定义测试用例
# 4. 生成详细报告

class RAGTestFramework:
    def __init__(self, config: dict):
        self.config = config
        self.evaluators = []

    def register_evaluator(self, evaluator):
        self.evaluators.append(evaluator)

    def run_all(self) -> dict:
        results = {}
        for evaluator in self.evaluators:
            results.update(evaluator.evaluate())
        return results

    def generate_report(self) -> str:
        return "# RAG 评测报告"
```

#### 练习18：Agent 集成测试

```python
# 综合练习：Agent 集成测试
# 要求：
# 1. 测试多工具协作
# 2. 测试复杂任务链
# 3. 测试状态管理

class TestAgentIntegration:
    def test_multi_tool_task(self, agent):
        """测试多工具任务"""
        result = agent.run("搜索天气，计算平均温度，发送邮件")
        assert result["success"]
        assert len(result["tool_calls"]) >= 2

    def test_state_management(self, agent):
        """测试状态管理"""
        agent.run("记住用户名是张三")
        result = agent.run("用户名是什么？")
        assert "张三" in result["answer"]
```

#### 练习19：AI 测试平台

```python
# 综合练习：构建 AI 测试平台
# 要求：
# 1. 测试用例管理
# 2. 执行引擎
# 3. 结果分析
# 4. 持续集成

class AITestPlatform:
    def __init__(self):
        self.test_cases = []
        self.results = []

    def upload_test_cases(self, cases: List[dict]):
        self.test_cases.extend(cases)

    def execute_tests(self, parallel: bool = True):
        for case in self.test_cases:
            result = self._run_case(case)
            self.results.append(result)

    def analyze_results(self) -> dict:
        passed = sum(1 for r in self.results if r["passed"])
        return {
            "total": len(self.results),
            "passed": passed,
            "pass_rate": passed / len(self.results)
        }
```

#### 练习20：综合实战项目

```python
# 综合实战：构建完整的 RAG 测试系统
# 要求：
# 1. 支持多种文档格式（PDF、Word、Markdown）
# 2. 支持多种检索策略（向量、关键词、混合）
# 3. 完整的评测指标体系
# 4. 可视化评测报告
# 5. CI/CD 集成

# 项目结构：
# rag_test_system/
# ├── config/
# │   └── settings.yaml
# ├── loaders/
# │   ├── pdf_loader.py
# │   └── markdown_loader.py
# ├── retrievers/
# │   ├── vector_retriever.py
# │   └── hybrid_retriever.py
# ├── evaluators/
# │   ├── retrieval_evaluator.py
# │   └── generation_evaluator.py
# ├── reporters/
# │   └── html_reporter.py
# └── main.py

class RAGTestSystem:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.retriever = None
        self.evaluator = None

    def setup(self):
        """初始化系统"""
        pass

    def run_evaluation(self, test_data_path: str):
        """运行评测"""
        pass

    def generate_report(self, output_path: str):
        """生成报告"""
        pass
```

---

## 五、本周小结

1. **RAG 原理**：检索增强生成的核心流程
2. **向量检索**：Embedding 和相似度计算
3. **评测指标**：Precision、Recall、MRR 等
4. **Agent 测试**：工具调用、规划、执行轨迹
5. **智能化测试**：AI 驱动的测试生成

### 下周预告

第16周学习 LLM 评测与安全测试。
