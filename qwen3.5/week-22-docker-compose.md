# 第 22 周 - Docker Compose

## 学习目标
掌握 Docker Compose，能够编排多容器应用。

---

## 知识点清单

### 1. Compose 文件
**掌握程度**: 版本、服务、配置

**练习资源**:
- [Docker Compose 文档](https://docs.docker.com/compose/)

**练习任务**:
- 编写 compose.yml
- 理解服务定义

---

### 2. 服务编排
**掌握程度**: 依赖、启动顺序

**练习任务**:
- 配置服务依赖
- 理解启动顺序

---

### 3. 网络
**掌握程度**: 服务发现、内部通信

**练习任务**:
- 配置网络
- 理解服务发现

---

### 4. 数据卷
**掌握程度**: 共享数据、持久化

**练习任务**:
- 配置数据卷
- 实现数据持久化

---

### 5. 环境变量
**掌握程度**: .env、变量替换

**练习任务**:
- 使用.env 文件
- 管理配置

---

### 6. 健康检查
**掌握程度**: healthcheck、依赖

**练习任务**:
- 配置健康检查
- 配置自动重启

---

### 7. 日志
**掌握程度**: 收集、查看、轮转

**练习任务**:
- 查看日志
- 配置日志驱动

---

### 8. 生产实践
**掌握程度**: 分离配置、资源限制

**练习任务**:
- 分离 dev/prod 配置
- 配置资源限制

---

## 本周练习任务

### 必做任务

1. **完整应用栈编排**
```yaml
# 编排一个完整应用栈
# 包括:
# - Web 前端（React）
# - API 后端（FastAPI）
# - 数据库（MySQL）
# - 缓存（Redis）

# 要求:
# - 一键启动
# - 服务间能通信
# - 数据持久化
```

2. **环境变量管理**
```bash
# 创建.env 文件
# .env:
#   MYSQL_ROOT_PASSWORD=root
#   API_HOST=0.0.0.0
#   API_PORT=8000

# 要求:
# - 敏感信息不提交到 Git
# - 提供.env.example 模板
```

3. **健康检查配置**
```yaml
# 为每个服务配置健康检查
# 要求:
# - 能检测服务是否正常
# - 失败时自动重启
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] `docker compose up` 能启动完整应用
- [ ] 服务之间能正常通信
- [ ] 能解释服务发现的原理
- [ ] 能配置健康检查
- [ ] 能管理环境变量

---

## Docker Compose 速查表

### 基础命令
```bash
# 启动
docker compose up
docker compose up -d  # 后台运行

# 停止
docker compose down
docker compose down -v  # 删除数据卷

# 查看
docker compose ps
docker compose logs
docker compose logs -f api  # 查看特定服务

# 其他
docker compose build
docker compose restart
docker compose exec api bash
```

### compose.yml 示例
```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - api

  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql://root:${MYSQL_ROOT_PASSWORD}@db:3306/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: app
    volumes:
      - db-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    volumes:
      - redis-data:/data

volumes:
  db-data:
  redis-data:
```

### 环境变量
```bash
# .env 文件
MYSQL_ROOT_PASSWORD=root
API_HOST=0.0.0.0
API_PORT=8000

# .env.example（提交到 Git）
MYSQL_ROOT_PASSWORD=
API_HOST=0.0.0.0
API_PORT=8000
```

### 资源限制
```yaml
services:
  api:
    build: ./backend
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## 面试考点

### 高频面试题
1. Docker Compose 的作用？
2. 服务间如何通信？
3. 如何配置服务依赖？
4. 健康检查的作用？
5. 如何管理环境变量？
6. 数据卷的作用？
7. 如何限制容器资源？

### 场景题
```yaml
# 1. 配置服务等待数据库启动后再启动
depends_on:
  db:
    condition: service_healthy

# 2. 配置多环境
# docker-compose.dev.yml
# docker-compose.prod.yml
```

---

## 每日学习检查清单

### Day 1-2: Compose 文件 + 编排
- [ ] 学习 Compose 语法
- [ ] 编写 compose.yml
- [ ] 配置服务依赖
- [ ] GitHub 提交

### Day 3-4: 网络 + 数据卷
- [ ] 学习网络配置
- [ ] 学习数据卷
- [ ] 实现服务通信
- [ ] GitHub 提交

### Day 5-6: 环境变量 + 健康检查
- [ ] 学习环境变量
- [ ] 配置健康检查
- [ ] 配置资源限制
- [ ] 完成完整应用栈

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成部署文档
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 22 周总结

### 学习内容
- 掌握了 Docker Compose
- 能编排多容器应用
- 理解了服务发现

### 作品
- 完整应用栈编排
- 部署文档

### 遇到的问题
- ...

### 下周改进
- ...
```
