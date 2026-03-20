# 第 20 周 - 前后端联调

## 学习目标
掌握前后端联调的核心技能，能够部署完整的全栈应用。

---

## 知识点清单

### 1. CORS
**掌握程度**: 跨域原理、配置

**练习资源**:
- [MDN CORS 文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS)

**练习任务**:
- 理解跨域原理
- 配置 CORS

---

### 2. 代理
**掌握程度**: Nginx 反向代理

**练习任务**:
- 配置 Nginx 反向代理
- 理解代理的作用

---

### 3. 认证流程
**掌握程度**: Token、刷新、过期

**练习任务**:
- 实现完整认证流程
- 处理 token 刷新
- 处理过期

---

### 4. 错误处理
**掌握程度**: 统一错误、前端展示

**练习任务**:
- 统一后端错误格式
- 前端友好展示错误

---

### 5. 加载状态
**掌握程度**: loading、骨架屏

**练习任务**:
- 实现 loading 状态
- 实现骨架屏

---

### 6. 表单验证
**掌握程度**: 前后端双重验证

**练习任务**:
- 前端验证
- 后端验证
- 验证一致

---

### 7. 文件上传
**掌握程度**: 前端表单、后端接收

**练习任务**:
- 实现文件上传
- 实现文件下载

---

### 8. 部署
**掌握程度**: 前端 build、后端服务

**练习任务**:
- 前端部署到 Vercel
- 后端部署到 Railway
- 能演示完整流程

---

## 本周练习任务

### 必做任务

1. **完整的博客系统**
```
功能:
- 用户注册/登录
- 文章 CRUD
- 评论功能
- 标签管理

要求:
- 前后端完全联调
- 部署到云端
- 可公开访问
```

2. **部署文档**
```markdown
# 部署指南

## 前端部署
1. 构建命令
2. Vercel 配置
3. 环境变量

## 后端部署
1. Railway 配置
2. 数据库配置
3. 环境变量

## 域名配置
1. 域名购买
2. DNS 配置
3. HTTPS 配置
```

3. **README 文档**
```markdown
# 博客系统

## 功能特性
- ...

## 技术栈
- 前端：React
- 后端：FastAPI
- 数据库：SQLite/PostgreSQL

## 快速开始
# 安装依赖
npm install
pip install -r requirements.txt

# 运行
npm run dev
uvicorn main:app --reload

## 在线 Demo
- 前端链接
- 后端 API 文档
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 博客系统能正常访问
- [ ] 有完整的 README 和部署文档
- [ ] 能演示完整流程
- [ ] 能解释 CORS 的工作原理
- [ ] 能处理认证过期场景

---

## CORS 配置

### FastAPI CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Nginx 配置

### 反向代理
```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 部署指南

### 前端部署到 Vercel
```bash
# 安装 Vercel CLI
npm install -g vercel

# 部署
cd frontend
vercel

# 按照提示完成配置
```

### 后端部署到 Railway
```bash
# 1. 创建 Railway 项目
# 2. 连接 GitHub 仓库
# 3. 配置环境变量
# 4. 自动部署
```

---

## 面试考点

### 高频面试题
1. 什么是 CORS？如何解决？
2. 什么是反向代理？
3. Token 过期的处理流程？
4. 前后端验证的区别？
5. 如何优化大文件上传？
6. 什么是 CDN？如何使用？
7. 如何部署全栈应用？

### 场景题
```
题目：用户反映上传图片很慢，如何优化？

思路:
1. 前端压缩图片
2. 后端分片上传
3. 使用 CDN 加速
4. 异步处理
```

---

## 每日学习检查清单

### Day 1-2: CORS + 代理
- [ ] 学习 CORS 原理
- [ ] 配置 CORS
- [ ] 学习 Nginx 代理
- [ ] GitHub 提交

### Day 3-4: 认证 + 错误处理
- [ ] 实现完整认证流程
- [ ] 统一错误处理
- [ ] 实现加载状态
- [ ] GitHub 提交

### Day 5-6: 文件上传 + 部署
- [ ] 实现文件上传
- [ ] 部署前端到 Vercel
- [ ] 部署后端到 Railway
- [ ] 编写文档

### Day 7: 复习 + 总结
- [ ] 复习本周内容
- [ ] 阶段二总结
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 20 周总结

### 学习内容
- 掌握了前后端联调
- 学会了部署全栈应用
- 理解了 CORS 和代理

### 作品
- 完整的博客系统（在线可访问）
- 部署文档

### 遇到的问题
- ...

### 阶段二总结
- UI 自动化：已掌握
- 接口自动化：已掌握
- Web 开发：已掌握
- DevOps: 待学习

### 下周改进
- ...
```
