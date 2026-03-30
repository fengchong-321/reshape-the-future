# AI 测试开发工程师 · 24周脱产学习计划

## 项目背景

针对 36 岁携程前端测试工程师转型 **AI 测试开发工程师** 的学习路线，面向上海地区 AI 测试开发岗位。

**项目驱动**：围绕 **Dify**（开源 AI 应用平台）展开学习和测试实践。

---

## 技术栈

### P0（核心必学）
- Python（含 pytest）
- Git
- Linux 常用命令
- HTTP/HTTPS
- SQL（MySQL/PostgreSQL）
- Docker
- 大模型原理（Transformer/Prompt 工程）
- LangChain
- DeepEval
- 对抗性测试（提示注入/越狱）

### P1（强烈推荐）
- CI/CD（GitHub Actions）
- Locust（性能测试）
- 向量数据库（Chroma/Milvus）
- Redis
- LangSmith

### P2（可选加分）
- Java/Go
- Kubernetes
- 前端基础（React/Vue）
- 知识图谱（Neo4j）
- 数据漂移检测（EvidentlyAI）

---

## 24 周学习计划概览

### 第一阶段：编程与工程基础（第1-6周）
| 周次 | 主题 | 核心内容 |
|------|------|---------|
| week01 | Python 基础 | 变量、数据结构、控制流、函数 |
| week02 | Python 进阶 | 面向对象、异常处理、模块化 |
| week03 | pytest 测试框架 | fixture、参数化、标记、断言 |
| week04 | Git 与 Linux | Git 工作流、Linux 常用命令 |
| week05 | HTTP 与 SQL | HTTP 协议、MySQL/PostgreSQL 操作 |
| week06 | Docker 基础 | Dockerfile、Docker Compose、容器化测试 |

### 第二阶段：大模型与 AI 测试基础（第7-11周）⭐
| 周次 | 主题 | 核心内容 |
|------|------|---------|
| week07 | 大模型原理 | Transformer 架构、Token、模型类型 |
| week08 | Prompt 工程 | Prompt 设计、优化技巧、评估方法 |
| week09 | LLM API 测试 | OpenAI/Anthropic API 调用、非确定性测试 |
| week10 | LangChain 基础 | Chain、Agent、Memory、回调机制 |
| week11 | LangChain 测试 | LangChain 应用测试、Mock LLM |

### 第三阶段：AI 测试框架与评估（第12-15周）⭐
| 周次 | 主题 | 核心内容 |
|------|------|---------|
| week12 | DeepEval 框架 | 评测指标、测试用例设计、报告生成 |
| week13 | RAGAS 评估 | RAG 评估指标、检索质量、生成质量 |
| week14 | 向量数据库测试 | Chroma/Milvus、Embedding 测试、相似度验证 |
| week15 | 对抗性测试 | 提示注入、越狱测试、安全边界 |

### 第四阶段：工程化与性能（第16-19周）
| 周次 | 主题 | 核心内容 |
|------|------|---------|
| week16 | CI/CD | GitHub Actions 自动化测试流水线 |
| week17 | Locust 性能测试 | LLM 接口压测、延迟测试、吞吐量 |
| week18 | Redis 与缓存 | 缓存测试、会话管理、数据一致性 |
| week19 | LangSmith 追踪 | 链路追踪、调试、性能分析 |

### 第五阶段：项目实战（第20-23周）
| 周次 | 主题 | 核心内容 |
|------|------|---------|
| week20 | Dify 部署与理解 | 部署 Dify、理解架构、API 分析 |
| week21 | Dify 接口测试 | 完整接口测试套件、数据驱动 |
| week22 | Dify AI 功能测试 | RAG 测试、Agent 测试、对话质量评估 |
| week23 | Dify 端到端测试 | 完整测试框架、CI 集成、报告 |

### 第六阶段：面试准备（第24周）
| 周次 | 主题 | 核心内容 |
|------|------|---------|
| week24 | 面试准备 | 知识复习、模拟面试、项目展示 |

---

## 如何使用本计划

### 交互命令

| 命令 | 作用 |
|------|------|
| `/week N` | 生成第 N 周周概要（目标 + 步骤 + 知识点清单） |
| `/day N` | 生成当周第 N 天详细计划（含知识点段落详解） |
| `/练习` | 获取当周练习题和代码框架 |
| `/review` | 提交代码让我 review，给出改进建议 |
| `/提问 xxx` | 结合当前周上下文回答问题 |
| `/总结` | 生成当周总结 |
| `/检验` | 提供 20 道面试题 |
| `/debug` | 帮助调试报错 |
| `/下一周` | 生成下周周概要 |

### 学习流程建议

```
周初：/week N       → 获取本周概要
每日：/day N        → 获取当日详细计划
      /练习         → 获取练习题，动手写代码
      /debug        → 遇到报错，帮我调试
      /提问 xxx     → 遇到疑问，结合上下文解答
      /review       → 写完代码，让我 review
周末：/检验         → 完成周检验
```

### 技术更新说明

> 由于无法实时联网，每周周概要基于 2026-03-29 之前的主流技术栈。
> 建议你在执行前自行检索最新动态，或告诉我确认是否有新工具出现。

---

## 开始学习

输入 `/week 1` 开始第一周学习。
