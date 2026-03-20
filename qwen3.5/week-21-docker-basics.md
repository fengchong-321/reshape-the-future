# 第 21 周 - Docker 基础

## 学习目标
掌握 Docker 核心概念，能够将应用容器化。

---

## 知识点清单

### 1. 核心概念
**掌握程度**: 镜像、容器、仓库

**练习资源**:
- [Docker 官方文档](https://docs.docker.com/)
- [Docker 入门教程](https://docs.docker.com/get-started/)

**练习任务**:
- 理解镜像和容器的区别
- 理解仓库的作用

---

### 2. 安装配置
**掌握程度**: Docker Desktop、镜像加速

**练习任务**:
- 安装 Docker Desktop
- 配置镜像加速器

---

### 3. 镜像操作
**掌握程度**: pull/push/build/tag

**练习任务**:
- 拉取镜像
- 构建镜像
- 推送镜像
- 打标签

---

### 4. Dockerfile
**掌握程度**: 指令、最佳实践

**练习任务**:
- 编写 Dockerfile
- 理解每层的作用
- 优化镜像大小

---

### 5. 容器操作
**掌握程度**: run/exec/logs/cp

**练习任务**:
- 运行容器
- 执行命令
- 查看日志
- 复制文件

---

### 6. 数据卷
**掌握程度**: volume、bind mount

**练习任务**:
- 创建数据卷
- 挂载数据卷
- 持久化数据

---

### 7. 网络
**掌握程度**: bridge/host/none

**练习任务**:
- 创建网络
- 连接容器
- 理解网络模式

---

### 8. 多阶段构建
**掌握程度**: 减小镜像大小

**练习任务**:
- 实现多阶段构建
- 优化镜像大小到 200MB 以下

---

## 本周练习任务

### 必做任务

1. **Docker 化 3 个项目**
```
项目:
1. Python 应用（FastAPI）
2. React 前端
3. MySQL 数据库

要求:
- 每个项目都能 Docker 化运行
- 编写 Dockerfile
- 编写启动脚本
```

2. **优化 Python 镜像**
```dockerfile
# 要求:
# - 使用多阶段构建
# - 镜像大小 < 200MB
# - 包含完整功能
```

3. **数据持久化**
```bash
# 实现 MySQL 数据持久化
# 要求:
# - 容器删除后数据不丢失
# - 使用 volume 或 bind mount
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 3 个项目都能 Docker 化运行
- [ ] 镜像大小符合标准
- [ ] 能解释 Docker 分层原理
- [ ] 能使用数据卷持久化数据
- [ ] 能配置容器网络

---

## Docker 速查表

### 基础命令
```bash
# 镜像操作
docker pull python:3.9
docker images
docker rmi <image_id>
docker build -t myapp:1.0 .
docker tag myapp:1.0 username/myapp:1.0
docker push username/myapp:1.0

# 容器操作
docker run -d -p 8000:8000 myapp:1.0
docker ps
docker stop <container_id>
docker rm <container_id>
docker logs <container_id>
docker exec -it <container_id> bash
docker cp file.txt container:/app/

# 数据卷
docker volume create mydata
docker volume ls
docker run -v mydata:/data myapp:1.0

# 网络
docker network create mynet
docker network ls
docker run --network=mynet myapp:1.0
```

### Dockerfile 示例
```dockerfile
# 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 多阶段构建
```dockerfile
# 构建阶段
FROM node:16 as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: ./frontend
    ports:
      - "3000:80"
  api:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
```

---

## 面试考点

### 高频面试题
1. 镜像和容器的区别？
2. Dockerfile 常见指令？
3. 数据卷和 bind mount 的区别？
4. 如何减小镜像大小？
5. Docker 网络模式有哪些？
6. 什么是多阶段构建？
7. Docker 和虚拟机的区别？

### 场景题
```bash
# 1. 容器启动失败，如何排查？
docker logs <container_id>
docker inspect <container_id>

# 2. 如何进入运行中的容器？
docker exec -it <container_id> bash

# 3. 如何查看容器资源占用？
docker stats
```

---

## 每日学习检查清单

### Day 1-2: 基础 + 安装
- [ ] 学习 Docker 概念
- [ ] 安装 Docker Desktop
- [ ] 运行第一个容器
- [ ] GitHub 提交

### Day 3-4: Dockerfile + 镜像
- [ ] 学习 Dockerfile 指令
- [ ] 编写 Dockerfile
- [ ] 构建镜像
- [ ] GitHub 提交

### Day 5-6: 数据卷 + 网络
- [ ] 学习数据卷
- [ ] 学习网络
- [ ] 实现数据持久化
- [ ] 多阶段构建

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成 3 个项目 Docker 化
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 21 周总结

### 学习内容
- 掌握了 Docker 基础
- 能编写 Dockerfile
- 能容器化应用

### 作品
- 3 个 Docker 化项目
- Dockerfile 集合

### 遇到的问题
- ...

### 下周改进
- ...
```
