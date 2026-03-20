# 第12周：AI 与大模型测试基础

## 本周目标

理解大语言模型（LLM）测试的独特挑战，掌握 LLM 测试的基本方法。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| LLM 基础 | 工作原理、主流模型 | ⭐⭐⭐⭐ |
| LLM 测试挑战 | 非确定性、幻觉、安全 | ⭐⭐⭐⭐⭐ |
| Prompt 测试 | 提示词设计与测试 | ⭐⭐⭐⭐⭐ |
| 语义相似度 | 相似度计算、阈值设定 | ⭐⭐⭐⭐ |
| LLM API 调用 | OpenAI、国内大模型 | ⭐⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 LLM 基础概念

```python
"""
大语言模型（LLM）基础

1. 什么是 LLM？
   - 基于深度学习的大规模语言模型
   - 通过海量文本训练，能理解和生成人类语言

2. 主流模型
   - OpenAI: GPT-4, GPT-3.5
   - Anthropic: Claude
   - Google: Gemini
   - 国产: 文心一言、通义千问、豆包

3. 核心概念
   - Token: 文本最小单位，约 1.5 个汉字
   - Temperature: 控制输出随机性（0-2）
   - Top-p: 核采样参数
   - Context Window: 上下文窗口大小

4. LLM 测试的挑战
   - 非确定性：相同输入可能得到不同输出
   - 语义理解：如何判断输出是否正确
   - 幻觉问题：模型可能编造不存在的信息
   - 安全性：可能产生有害内容
   - 偏见：模型可能存在训练数据偏见
"""
```

---

### 2.2 LLM API 调用

```python
# ============================================
# OpenAI API
# ============================================
# 安装：pip install openai

from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def call_gpt(prompt, model="gpt-4", temperature=0.7):
    """调用 GPT 模型"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=1000
    )
    return response.choices[0].message.content

# 使用
answer = call_gpt("什么是软件测试？")
print(answer)

# ============================================
# 国内大模型（以智谱 AI 为例）
# ============================================
# 安装：pip install zhipuai

from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your-api-key")

def call_glm(prompt, model="glm-4"):
    """调用智谱 GLM 模型"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ============================================
# 统一封装
# ============================================
class LLMClient:
    """大模型统一客户端"""

    def __init__(self, provider="openai", api_key=None, model=None):
        self.provider = provider
        self.api_key = api_key

        if provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = model or "gpt-3.5-turbo"
        elif provider == "zhipu":
            from zhipuai import ZhipuAI
            self.client = ZhipuAI(api_key=api_key)
            self.model = model or "glm-4"
        # 可以添加更多提供商

    def chat(self, prompt, system_prompt=None, temperature=0.7):
        """发送对话请求"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content

        elif self.provider == "zhipu":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content

# 使用
llm = LLMClient(provider="openai", api_key="xxx")
answer = llm.chat("你好", system_prompt="你是一个测试工程师")
```

---

### 2.3 Prompt 测试

```python
import pytest

# ============================================
# Prompt 模板
# ============================================
PROMPT_TEMPLATES = {
    "summarize": """请用{words}字以内总结以下内容：

{content}

要求：
1. 提取关键信息
2. 语言简洁
3. 保持客观""",

    "translate": """请将以下{source_lang}文本翻译成{target_lang}：

{content}

要求：
1. 保持原意
2. 语言流畅自然""",

    "qa": """根据以下上下文回答问题。如果上下文中没有相关信息，请回答"我不知道"。

上下文：
{context}

问题：{question}

请直接回答问题："""
}

# ============================================
# Prompt 测试框架
# ============================================
class PromptTester:
    """Prompt 测试框架"""

    def __init__(self, llm_client):
        self.llm = llm_client

    def test_prompt(self, prompt, validation_func, runs=3):
        """
        测试 Prompt

        Args:
            prompt: 提示词
            validation_func: 验证函数
            runs: 运行次数（应对非确定性）
        """
        results = []
        for i in range(runs):
            response = self.llm.chat(prompt)
            is_valid = validation_func(response)
            results.append({
                "run": i + 1,
                "response": response,
                "is_valid": is_valid
            })

        pass_rate = sum(r["is_valid"] for r in results) / runs
        return {
            "prompt": prompt,
            "results": results,
            "pass_rate": pass_rate,
            "passed": pass_rate >= 0.8  # 80% 通过率
        }

    def test_prompt_with_keywords(self, prompt, must_contain, must_not_contain=None):
        """测试 Prompt 是否包含关键词"""
        response = self.llm.chat(prompt)

        # 检查必须包含的关键词
        missing = [kw for kw in must_contain if kw not in response]

        # 检查不能包含的关键词
        forbidden = []
        if must_not_contain:
            forbidden = [kw for kw in must_not_contain if kw in response]

        return {
            "response": response,
            "passed": len(missing) == 0 and len(forbidden) == 0,
            "missing_keywords": missing,
            "forbidden_found": forbidden
        }

# ============================================
# 测试用例
# ============================================
def test_summarize_prompt():
    """测试摘要 Prompt"""
    llm = LLMClient(provider="openai", api_key="xxx")
    tester = PromptTester(llm)

    content = """
    软件测试是软件开发过程中的重要环节，目的是发现软件中的缺陷。
    测试可以分为单元测试、集成测试、系统测试和验收测试。
    好的测试能够提高软件质量，降低维护成本。
    """

    prompt = PROMPT_TEMPLATES["summarize"].format(
        words=50,
        content=content
    )

    result = tester.test_prompt_with_keywords(
        prompt,
        must_contain=["测试", "软件"],
        must_not_contain=["我不知道", "无法"]
    )

    assert result["passed"], f"缺少关键词: {result['missing_keywords']}"

def test_qa_prompt():
    """测试问答 Prompt"""
    llm = LLMClient(provider="openai", api_key="xxx")
    tester = PromptTester(llm)

    context = """
    携程是一个在线旅行服务平台，提供酒店预订、机票预订、旅游度假等服务。
    公司成立于1999年，总部位于上海。
    """

    # 测试：上下文中有答案的问题
    prompt1 = PROMPT_TEMPLATES["qa"].format(
        context=context,
        question="携程提供哪些服务？"
    )

    result1 = tester.test_prompt_with_keywords(
        prompt1,
        must_contain=["酒店", "机票"],
        must_not_contain=["我不知道"]
    )
    assert result1["passed"]

    # 测试：上下文中没有答案的问题
    prompt2 = PROMPT_TEMPLATES["qa"].format(
        context=context,
        question="携程的股票代码是什么？"
    )

    response = llm.chat(prompt2)
    assert "我不知道" in response or "没有" in response
```

---

### 2.4 语义相似度测试

```python
# 安装：pip install sentence-transformers

from sentence_transformers import SentenceTransformer
import numpy as np

# ============================================
# 语义相似度计算
# ============================================
class SemanticComparator:
    """语义相似度比较器"""

    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        # 使用多语言模型，支持中文
        self.model = SentenceTransformer(model_name)

    def similarity(self, text1, text2):
        """计算两段文本的语义相似度"""
        embeddings = self.model.encode([text1, text2])
        # 余弦相似度
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return similarity

    def batch_similarity(self, text, candidates):
        """计算文本与多个候选的相似度"""
        all_texts = [text] + candidates
        embeddings = self.model.encode(all_texts)

        similarities = []
        for i in range(1, len(all_texts)):
            sim = np.dot(embeddings[0], embeddings[i]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[i])
            )
            similarities.append(sim)

        return similarities

# ============================================
# LLM 输出验证
# ============================================
class LLMOutputValidator:
    """LLM 输出验证器"""

    def __init__(self, llm_client, similarity_threshold=0.7):
        self.llm = llm_client
        self.comparator = SemanticComparator()
        self.similarity_threshold = similarity_threshold

    def validate_semantic_equivalence(self, response, expected_meaning):
        """验证语义等价"""
        similarity = self.comparator.similarity(response, expected_meaning)
        return {
            "response": response,
            "expected": expected_meaning,
            "similarity": similarity,
            "passed": similarity >= self.similarity_threshold
        }

    def validate_best_match(self, response, expected_options):
        """验证输出是否匹配预期选项之一"""
        similarities = self.comparator.batch_similarity(response, expected_options)
        best_idx = np.argmax(similarities)
        best_similarity = similarities[best_idx]

        return {
            "response": response,
            "best_match": expected_options[best_idx],
            "similarity": best_similarity,
            "passed": best_similarity >= self.similarity_threshold
        }

# ============================================
# 测试用例
# ============================================
def test_semantic_equivalence():
    """测试语义等价"""
    validator = LLMOutputValidator(None)

    # 测试语义相似
    result1 = validator.validate_semantic_equivalence(
        "测试是验证软件功能是否正常的过程",
        "软件测试是用来检查程序是否按预期工作的"
    )
    assert result1["passed"]  # 相似度应该很高

    # 测试语义不同
    result2 = validator.validate_semantic_equivalence(
        "今天天气很好",
        "软件测试是用来检查程序是否按预期工作的"
    )
    assert not result2["passed"]  # 相似度应该很低
```

---

## 三、学到什么程度

### 必须掌握

- [ ] 理解 LLM 的基本概念和挑战
- [ ] 能调用主流 LLM API
- [ ] 能编写 Prompt 测试用例
- [ ] 能使用语义相似度验证输出

### 应该了解

- [ ] 不同模型的 API 差异
- [ ] Temperature 参数的影响

---

## 四、练习内容

### 练习1：Prompt 模板测试

```python
# 编写 5 个 Prompt 模板
# 测试不同温度下的输出稳定性
```

### 练习2：语义验证

```python
# 实现语义相似度验证
# 测试 LLM 的问答准确性
```

### 练习3：安全性测试

```python
# 测试 LLM 是否会拒绝有害请求
# 验证安全过滤效果
```

---

## 五、本周小结

1. **LLM 基础**：理解非确定性输出的挑战
2. **Prompt 测试**：大模型测试的核心
3. **语义验证**：比关键词匹配更准确

### 下周预告

第13周继续学习 RAG 测试和 Agent 测试。
