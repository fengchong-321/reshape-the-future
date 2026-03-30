# 第14周：向量数据库与 Embedding 测试

## 本周目标

掌握向量数据库和 Embedding 技术，能够设计和实现向量检索的测试方案。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Embedding 基础 | 文本向量化、相似度计算 | ⭐⭐⭐⭐⭐ |
| ChromaDB | 本地向量数据库 | ⭐⭐⭐⭐⭐ |
| FAISS | 高效向量检索 | ⭐⭐⭐⭐ |
| Pinecone | 云端向量数据库 | ⭐⭐⭐ |
| 向量检索测试 | 准确率、召回率评估 | ⭐⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 Embedding 基础

```python
# ============================================
# 文本 Embedding 基础
# ============================================
"""
Embedding：将文本转换为高维向量表示

常用模型：
- OpenAI: text-embedding-3-small, text-embedding-3-large
- 开源: all-MiniLM-L6-v2, bge-large-zh

维度：通常 384-1536 维
"""

# ============================================
# 使用 sentence-transformers
# ============================================
# 安装：pip install sentence-transformers

from sentence_transformers import SentenceTransformer

# 加载模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 单文本编码
text = "这是一个测试文本"
embedding = model.encode(text)
print(f"向量维度: {embedding.shape}")  # (384,)

# 批量编码
texts = ["文本1", "文本2", "文本3"]
embeddings = model.encode(texts)
print(f"批量向量形状: {embeddings.shape}")  # (3, 384)
```

```python
# ============================================
# 相似度计算
# ============================================
import numpy as np
from numpy.linalg import norm

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """计算余弦相似度"""
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """计算欧几里得距离"""
    return norm(vec1 - vec2)

# 使用
vec1 = model.encode("我喜欢吃苹果")
vec2 = model.encode("我爱吃水果")
vec3 = model.encode("今天天气很好")

print(f"相似文本相似度: {cosine_similarity(vec1, vec2):.4f}")  # ~0.8
print(f"不同文本相似度: {cosine_similarity(vec1, vec3):.4f}")  # ~0.3
```

```python
# ============================================
# 使用 OpenAI Embedding
# ============================================
from openai import OpenAI

client = OpenAI()

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    """获取 OpenAI Embedding"""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

# 使用
embedding = get_embedding("测试文本")
print(f"OpenAI Embedding 维度: {len(embedding)}")  # 1536
```

### 2.2 ChromaDB

```python
# ============================================
# ChromaDB 基础使用
# ============================================
# 安装：pip install chromadb

import chromadb
from chromadb.config import Settings

# 创建客户端
client = chromadb.Client(Settings())

# 或持久化存储
# client = chromadb.PersistentClient(path="./chroma_db")

# 创建集合
collection = client.create_collection(
    name="documents",
    metadata={"description": "文档集合"}
)

# 添加文档
collection.add(
    documents=["文档1内容", "文档2内容", "文档3内容"],
    metadatas=[{"source": "web"}, {"source": "file"}, {"source": "api"}],
    ids=["doc1", "doc2", "doc3"]
)

# 查询
results = collection.query(
    query_texts=["搜索查询"],
    n_results=2
)
print(results)
```

```python
# ============================================
# ChromaDB 使用自定义 Embedding
# ============================================
from chromadb.utils import embedding_functions

# 使用 sentence-transformers
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=embedding_function
)

# 添加文档（会自动生成 embedding）
collection.add(
    documents=["Python 是一种编程语言", "Java 也是一种编程语言"],
    ids=["py", "java"]
)

# 查询
results = collection.query(
    query_texts=["编程语言有哪些"],
    n_results=2
)
```

```python
# ============================================
# ChromaDB 增删改查
# ============================================
# 更新文档
collection.update(
    ids=["doc1"],
    documents=["更新后的文档1内容"],
    metadatas=[{"source": "updated"}]
)

# 删除文档
collection.delete(ids=["doc2"])

# 获取文档
result = collection.get(ids=["doc1"])
print(result)

# 获取所有文档
all_docs = collection.get()
print(f"总文档数: {len(all_docs['ids'])}")
```

### 2.3 FAISS

```python
# ============================================
# FAISS 基础使用
# ============================================
# 安装：pip install faiss-cpu (或 faiss-gpu)

import faiss
import numpy as np

# 创建向量（假设 128 维）
dimension = 128
n_vectors = 1000

# 随机生成测试向量
vectors = np.random.random((n_vectors, dimension)).astype('float32')

# 创建索引
index = faiss.IndexFlatL2(dimension)

# 添加向量
index.add(vectors)
print(f"索引中向量数: {index.ntotal}")

# 搜索
k = 5  # 返回最近 5 个
query = np.random.random((1, dimension)).astype('float32')
distances, indices = index.search(query, k)

print(f"最近邻索引: {indices}")
print(f"距离: {distances}")
```

```python
# ============================================
# FAISS 与文本检索
# ============================================
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class FAISSRetriever:
    """FAISS 文本检索器"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384
        self.index = None
        self.documents = []

    def index_documents(self, documents: list):
        """索引文档"""
        self.documents = documents
        embeddings = self.model.encode(documents)

        # 创建索引
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype('float32'))

    def search(self, query: str, k: int = 5) -> list:
        """搜索相似文档"""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding.astype('float32'), k)

        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "document": self.documents[idx],
                "distance": float(distances[0][i]),
                "index": int(idx)
            })
        return results

# 使用
retriever = FAISSRetriever()
retriever.index_documents([
    "Python 是一种高级编程语言",
    "Java 是面向对象的编程语言",
    "JavaScript 用于网页开发",
    "Go 语言由 Google 开发",
    "Rust 注重安全和性能"
])

results = retriever.search("网页开发语言", k=2)
for r in results:
    print(f"文档: {r['document']}, 距离: {r['distance']:.4f}")
```

### 2.4 向量检索测试

```python
# ============================================
# 检索质量评估
# ============================================
from typing import List, Set
from dataclasses import dataclass

@dataclass
class RetrievalTestCase:
    """检索测试用例"""
    query: str
    relevant_doc_ids: Set[int]  # 相关文档 ID 集合

class RetrievalEvaluator:
    """检索评估器"""

    def __init__(self, retriever):
        self.retriever = retriever

    def evaluate(self, test_cases: List[RetrievalTestCase], k: int = 5):
        """评估检索质量"""
        results = []

        for tc in test_cases:
            # 执行检索
            search_results = self.retriever.search(tc.query, k)
            retrieved_ids = {r["index"] for r in search_results}

            # 计算 Precision@K
            relevant_retrieved = len(retrieved_ids & tc.relevant_doc_ids)
            precision = relevant_retrieved / k if k > 0 else 0

            # 计算 Recall@K
            recall = relevant_retrieved / len(tc.relevant_doc_ids) if tc.relevant_doc_ids else 0

            # 计算 F1
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

            results.append({
                "query": tc.query,
                "precision": precision,
                "recall": recall,
                "f1": f1
            })

        # 计算平均指标
        avg_precision = sum(r["precision"] for r in results) / len(results)
        avg_recall = sum(r["recall"] for r in results) / len(results)
        avg_f1 = sum(r["f1"] for r in results) / len(results)

        return {
            "cases": results,
            "avg_precision": avg_precision,
            "avg_recall": avg_recall,
            "avg_f1": avg_f1
        }

# 使用
test_cases = [
    RetrievalTestCase("编程语言", {0, 1}),  # Python, Java
    RetrievalTestCase("网页开发", {2}),      # JavaScript
    RetrievalTestCase("Google", {3})         # Go
]

evaluator = RetrievalEvaluator(retriever)
metrics = evaluator.evaluate(test_cases, k=3)
print(f"平均 Precision@3: {metrics['avg_precision']:.4f}")
print(f"平均 Recall@3: {metrics['avg_recall']:.4f}")
```

```python
# ============================================
# MRR (Mean Reciprocal Rank) 计算
# ============================================
def calculate_mrr(test_cases: List[RetrievalTestCase], retriever, k: int = 10):
    """计算 MRR"""
    reciprocal_ranks = []

    for tc in test_cases:
        results = retriever.search(tc.query, k)
        for rank, r in enumerate(results, 1):
            if r["index"] in tc.relevant_doc_ids:
                reciprocal_ranks.append(1.0 / rank)
                break
        else:
            reciprocal_ranks.append(0.0)

    return sum(reciprocal_ranks) / len(reciprocal_ranks)
```

### 2.5 Embedding 质量测试

```python
# ============================================
# Embedding 语义一致性测试
# ============================================
class EmbeddingQualityTester:
    """Embedding 质量测试器"""

    def __init__(self, model):
        self.model = model

    def test_semantic_similarity(self, test_pairs: list):
        """测试语义相似度"""
        results = []

        for pair in test_pairs:
            text1, text2, expected_similar = pair
            emb1 = self.model.encode(text1)
            emb2 = self.model.encode(text2)
            similarity = cosine_similarity(emb1, emb2)

            # 判断是否符合预期
            threshold = 0.7
            actual_similar = similarity > threshold
            passed = actual_similar == expected_similar

            results.append({
                "text1": text1,
                "text2": text2,
                "similarity": similarity,
                "expected": expected_similar,
                "actual": actual_similar,
                "passed": passed
            })

        return results

# 使用
tester = EmbeddingQualityTester(model)
test_pairs = [
    ("我喜欢苹果", "我爱吃苹果", True),
    ("我喜欢苹果", "今天下雨了", False),
    ("Python是编程语言", "Java是编程语言", True),
    ("北京是首都", "上海是大城市", False)
]

results = tester.test_semantic_similarity(test_pairs)
for r in results:
    print(f"'{r['text1']}' vs '{r['text2']}'")
    print(f"  相似度: {r['similarity']:.4f}, 通过: {r['passed']}")
```

---

## 三、学到什么程度

### 必须掌握
- [ ] Embedding 原理和常用模型
- [ ] 余弦相似度计算
- [ ] ChromaDB 基本操作
- [ ] FAISS 索引创建和搜索
- [ ] 检索质量评估（Precision、Recall、F1）

### 应该了解
- [ ] Pinecone 等云端向量数据库
- [ ] IVF、HNSW 等索引类型
- [ ] Embedding 模型微调
- [ ] 多模态 Embedding

---

## 四、练习内容

### 基础练习（1-8）

#### 练习1：Embedding 基础操作

**场景说明：**
作为 AI 测试工程师，需要理解 Embedding 的基本概念和操作。

**具体需求：**
1. 使用 sentence-transformers 编码文本
2. 查看 Embedding 向量维度
3. 比较不同文本的 Embedding

**使用示例：**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
texts = ["测试文本1", "测试文本2"]
embeddings = model.encode(texts)
print(f"向量形状: {embeddings.shape}")
```

**验收标准：**
- [ ] 成功加载模型
- [ ] 编码输出正确维度
- [ ] 能批量编码文本

---

#### 练习2：余弦相似度计算

**场景说明：**
需要量化文本之间的语义相似度。

**具体需求：**
1. 实现余弦相似度函数
2. 测试相似文本和不同文本
3. 设定相似度阈值

**使用示例：**
```python
import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# 测试
sim = cosine_similarity(emb1, emb2)
print(f"相似度: {sim:.4f}")
```

**验收标准：**
- [ ] 相似度计算正确
- [ ] 相似文本得分高
- [ ] 不同文本得分低

---

#### 练习3：ChromaDB 创建集合

**场景说明：**
需要在项目中使用向量数据库存储文档。

**具体需求：**
1. 创建 ChromaDB 客户端
2. 创建文档集合
3. 添加测试文档

**使用示例：**
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("test_docs")
collection.add(
    documents=["文档1", "文档2"],
    ids=["id1", "id2"]
)
```

**验收标准：**
- [ ] 集合创建成功
- [ ] 文档添加成功
- [ ] 能查询文档数量

---

#### 练习4：ChromaDB 向量检索

**场景说明：**
需要实现基于语义的文档检索。

**具体需求：**
1. 添加多个文档到集合
2. 执行语义查询
3. 分析检索结果

**使用示例：**
```python
results = collection.query(
    query_texts=["搜索查询"],
    n_results=3
)
print(results['documents'])
```

**验收标准：**
- [ ] 查询返回结果
- [ ] 结果按相似度排序
- [ ] 包含距离信息

---

#### 练习5：ChromaDB 元数据过滤

**场景说明：**
需要根据元数据条件过滤检索结果。

**具体需求：**
1. 添加带元数据的文档
2. 使用 where 条件过滤
3. 验证过滤结果

**使用示例：**
```python
collection.add(
    documents=["技术文档", "业务文档"],
    metadatas=[{"type": "tech"}, {"type": "business"}],
    ids=["1", "2"]
)

results = collection.query(
    query_texts=["文档"],
    where={"type": "tech"}
)
```

**验收标准：**
- [ ] 元数据添加成功
- [ ] 过滤条件生效
- [ ] 结果符合预期

---

#### 练习6：FAISS 索引创建

**场景说明：**
需要高效处理大规模向量检索。

**具体需求：**
1. 创建 FAISS 索引
2. 添加向量
3. 执行搜索

**使用示例：**
```python
import faiss
import numpy as np

dimension = 128
index = faiss.IndexFlatL2(dimension)
vectors = np.random.random((100, dimension)).astype('float32')
index.add(vectors)
```

**验收标准：**
- [ ] 索引创建成功
- [ ] 向量添加正确
- [ ] 搜索返回结果

---

#### 练习7：FAISS 文本检索器

**场景说明：**
需要将 FAISS 与文本检索结合使用。

**具体需求：**
1. 封装 FAISSRetriever 类
2. 支持文档索引和搜索
3. 返回原始文档

**使用示例：**
```python
retriever = FAISSRetriever()
retriever.index_documents(["文档1", "文档2", "文档3"])
results = retriever.search("查询", k=2)
```

**验收标准：**
- [ ] 封装类实现完整
- [ ] 搜索返回文档
- [ ] 距离计算正确

---

#### 练习8：检索质量评估

**场景说明：**
需要评估向量检索的质量。

**具体需求：**
1. 实现 Precision@K 计算
2. 实现 Recall@K 计算
3. 计算 F1 分数

**使用示例：**
```python
def evaluate_retrieval(retrieved, relevant, k):
    retrieved_set = set(retrieved[:k])
    relevant_set = set(relevant)
    precision = len(retrieved_set & relevant_set) / k
    recall = len(retrieved_set & relevant_set) / len(relevant_set)
    return precision, recall
```

**验收标准：**
- [ ] Precision 计算正确
- [ ] Recall 计算正确
- [ ] F1 计算正确

---

### 进阶练习（9-16）

#### 练习9：Embedding 语义一致性测试

**场景说明：**
验证 Embedding 模型的语义理解能力。

**具体需求：**
1. 设计语义相似/不同的文本对
2. 计算相似度
3. 验证是否符合预期

**验收标准：**
- [ ] 测试用例覆盖全面
- [ ] 相似度计算准确
- [ ] 通过率达标

---

#### 练习10：批量 Embedding 性能测试

**场景说明：**
测试 Embedding 编码的性能。

**具体需求：**
1. 测试不同批量大小的性能
2. 测量编码时间
3. 优化建议

**验收标准：**
- [ ] 性能数据准确
- [ ] 批量优化有效
- [ ] 报告清晰

---

#### 练习11：向量维度影响测试

**场景说明：**
测试不同 Embedding 维度对检索效果的影响。

**具体需求：**
1. 使用不同维度的模型
2. 对比检索效果
3. 分析权衡

**验收标准：**
- [ ] 对比测试完整
- [ ] 效果差异明显
- [ ] 分析合理

---

#### 练习12：ChromaDB 持久化存储

**场景说明：**
需要持久化向量数据库。

**具体需求：**
1. 配置持久化路径
2. 测试重启后数据保留
3. 测试数据迁移

**验收标准：**
- [ ] 数据持久化成功
- [ ] 重启后数据完整
- [ ] 迁移无丢失

---

#### 练习13：FAISS IVF 索引

**场景说明：**
需要使用更高效的索引结构。

**具体需求：**
1. 创建 IVF 索引
2. 训练和添加向量
3. 对比搜索效果

**验收标准：**
- [ ] IVF 索引创建成功
- [ ] 搜索结果正确
- [ ] 性能提升明显

---

#### 练习14：混合检索实现

**场景说明：**
结合向量检索和关键词检索。

**具体需求：**
1. 实现关键词检索
2. 实现向量检索
3. 融合排序

**验收标准：**
- [ ] 两种检索实现
- [ ] 融合算法合理
- [ ] 效果提升

---

#### 练习15：检索结果重排序

**场景说明：**
对检索结果进行二次排序优化。

**具体需求：**
1. 实现重排序逻辑
2. 使用交叉编码器
3. 评估效果提升

**验收标准：**
- [ ] 重排序实现
- [ ] 效果提升明显
- [ ] 延迟可接受

---

#### 练习16：大规模向量测试

**场景说明：**
测试大规模向量检索的性能。

**具体需求：**
1. 生成 10 万+ 向量
2. 测试索引时间
3. 测试查询延迟

**验收标准：**
- [ ] 大规模测试成功
- [ ] 性能指标完整
- [ ] 瓶颈分析准确

---

### 综合练习（17-20）

#### 练习17：完整向量检索测试框架

**场景说明：**
搭建完整的向量检索测试框架。

**具体需求：**
1. 整合 Embedding、索引、检索
2. 支持多种评估指标
3. 生成测试报告

**验收标准：**
- [ ] 框架功能完整
- [ ] 评估指标全面
- [ ] 报告清晰

---

#### 练习18：RAG 检索组件测试

**场景说明：**
为 RAG 系统测试检索组件。

**具体需求：**
1. 测试文档切分
2. 测试向量索引
3. 测试检索召回率

**验收标准：**
- [ ] 组件测试覆盖
- [ ] 召回率达标
- [ ] 集成测试通过

---

#### 练习19：Embedding 模型对比测试

**场景说明：**
对比不同 Embedding 模型的效果。

**具体需求：**
1. 选择 3+ 模型
2. 设计统一测试集
3. 对比分析报告

**验收标准：**
- [ ] 对比测试完整
- [ ] 数据分析准确
- [ ] 推荐结论合理

---

#### 练习20：向量数据库压力测试

**场景说明：**
对向量数据库进行压力测试。

**具体需求：**
1. 并发写入测试
2. 并发查询测试
3. 资源消耗监控

**验收标准：**
- [ ] 压力测试完成
- [ ] 瓶颈识别准确
- [ ] 优化建议可行

---

## 五、检验标准

### 自测题

1. 什么是 Embedding？它有什么作用？
2. 余弦相似度的计算公式是什么？
3. ChromaDB 和 FAISS 有什么区别？
4. 如何评估向量检索的质量？

### 参考答案

1. Embedding 是将文本转换为高维向量表示，使语义相似的文本在向量空间中距离更近
2. cos(A,B) = (A·B) / (||A|| × ||B||)
3. ChromaDB 是功能完整的向量数据库，FAISS 是高效的向量检索库
4. 使用 Precision@K、Recall@K、MRR 等指标评估
