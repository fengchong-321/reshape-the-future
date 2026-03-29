# 第11周：Docker 容器化测试

## 本周目标

掌握 Docker 容器化技术，能够使用 Docker 构建测试环境、运行容器化测试。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Docker 基础 | 镜像、容器、仓库 | ⭐⭐⭐⭐⭐ |
| Dockerfile | 编写、优化、多阶段构建 | ⭐⭐⭐⭐⭐ |
| Docker Compose | 多容器编排、网络、 volumes | ⭐⭐⭐⭐ |
| 测试环境容器化 | 测试数据库、Mock 服务 | ⭐⭐⭐⭐⭐ |
| testcontainers | Python 测试容器库 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 Docker 基础概念

```bash
# ============================================
# Docker 核心概念
# ============================================
# 镜像（Image）：只读模板，包含运行应用所需的一切
# 容器（Container）：镜像的运行实例
# 仓库（Registry）：存储和分发镜像（Docker Hub、私有仓库）

# ============================================
# 常用命令
# ============================================
# 查看版本
docker --version
docker version

# 拉取镜像
docker pull python:3.11
docker pull mysql:8.0
docker pull redis:7

# 查看本地镜像
docker images

# 运行容器
docker run -d --name my-python python:3.11 sleep 1000
docker run -d --name my-mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0

# 查看运行中的容器
docker ps
docker ps -a  # 包括已停止的

# 进入容器
docker exec -it my-python bash

# 停止/启动/删除容器
docker stop my-python
docker start my-python
docker rm my-python

# 删除镜像
docker rmi python:3.11

# 查看容器日志
docker logs my-mysql
docker logs -f my-mysql  # 实时查看

# 查看容器资源使用
docker stats
```

### 2.2 Dockerfile 编写

```dockerfile
# ============================================
# 基础 Dockerfile 示例
# ============================================
# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 运行测试命令
CMD ["pytest", "-v"]
```

```dockerfile
# ============================================
# 多阶段构建（减小镜像体积）
# ============================================
# 第一阶段：构建
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# 第二阶段：运行
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/deps /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["pytest", "-v"]
```

```python
# ============================================
# Python 脚本构建镜像
# ============================================
import subprocess

def build_docker_image(tag: str, dockerfile_path: str = "."):
    """构建 Docker 镜像"""
    cmd = ["docker", "build", "-t", tag, dockerfile_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"构建失败: {result.stderr}")
    return tag

# 使用
build_docker_image("my-test:latest", "./tests")
```

### 2.3 Docker Compose

```yaml
# ============================================
# docker-compose.yml 示例
# ============================================
version: '3.8'

services:
  # 测试数据库
  test-db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: test123
      MYSQL_DATABASE: test_db
    ports:
      - "3307:3306"
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 5s
      retries: 10

  # Redis 缓存
  test-redis:
    image: redis:7
    ports:
      - "6380:6379"

  # Mock API 服务
  mock-api:
    image: wiremock/wiremock:latest
    ports:
      - "8080:8080"
    volumes:
      - ./mocks:/home/wiremock

  # 测试运行器
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    depends_on:
      test-db:
        condition: service_healthy
      test-redis:
        condition: service_started
    environment:
      DB_HOST: test-db
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: test123
      REDIS_HOST: test-redis
    volumes:
      - ./reports:/app/reports

volumes:
  db_data:
```

```python
# ============================================
# 使用 Docker Compose 管理测试环境
# ============================================
import subprocess
import time

class DockerComposeManager:
    """Docker Compose 环境管理器"""

    def __init__(self, compose_file: str = "docker-compose.yml"):
        self.compose_file = compose_file

    def up(self, services: list = None):
        """启动服务"""
        cmd = ["docker-compose", "-f", self.compose_file, "up", "-d"]
        if services:
            cmd.extend(services)
        subprocess.run(cmd, check=True)

    def down(self):
        """停止并清理"""
        cmd = ["docker-compose", "-f", self.compose_file, "down", "-v"]
        subprocess.run(cmd, check=True)

    def wait_for_service(self, service: str, port: int, timeout: int = 60):
        """等待服务就绪"""
        import socket
        start = time.time()
        while time.time() - start < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    return True
            except:
                pass
            time.sleep(1)
        raise TimeoutError(f"服务 {service} 启动超时")

# 使用
manager = DockerComposeManager()
manager.up(["test-db", "test-redis"])
manager.wait_for_service("test-db", 3307)
```

### 2.4 testcontainers 库

```python
# ============================================
# testcontainers-python 使用
# ============================================
# 安装：pip install testcontainers

import pytest
from testcontainers.mysql import MySqlContainer
from testcontainers.redis import RedisContainer
import pymysql
import redis

class TestWithContainers:

    @pytest.fixture(scope="class")
    def mysql_container(self):
        """MySQL 容器 fixture"""
        with MySqlContainer("mysql:8.0") as mysql:
            yield mysql

    @pytest.fixture(scope="class")
    def redis_container(self):
        """Redis 容器 fixture"""
        with RedisContainer("redis:7") as redis_container:
            yield redis_container

    def test_mysql_connection(self, mysql_container):
        """测试 MySQL 连接"""
        conn = pymysql.connect(
            host=mysql_container.get_container_host_ip(),
            port=mysql_container.get_exposed_port(3306),
            user="root",
            password="test",
            database="test"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result == (1,)
        conn.close()

    def test_redis_connection(self, redis_container):
        """测试 Redis 连接"""
        client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379)
        )
        client.set("test_key", "test_value")
        assert client.get("test_key") == b"test_value"
```

```python
# ============================================
# 自定义容器
# ============================================
from testcontainers.core.generic import GenericContainer

class MockApiContainer(GenericContainer):
    """Mock API 容器"""

    def __init__(self, image: str = "wiremock/wiremock:latest"):
        super().__init__(image)
        self.with_exposed_ports(8080)

    def get_url(self):
        return f"http://{self.get_container_host_ip()}:{self.get_exposed_port(8080)}"

# 使用
def test_with_mock_api():
    with MockApiContainer() as mock:
        url = mock.get_url()
        # 配置 mock 响应...
        # 进行测试...
```

### 2.5 CI/CD 中使用 Docker

```yaml
# ============================================
# GitLab CI 示例
# ============================================
test:
  image: python:3.11
  services:
    - mysql:8.0
    - redis:7
  variables:
    MYSQL_ROOT_PASSWORD: test123
    MYSQL_DATABASE: test_db
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml
```

```yaml
# ============================================
# GitHub Actions 示例
# ============================================
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: test123
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

---

## 三、学到什么程度

### 必须掌握
- [ ] Docker 基本概念和常用命令
- [ ] 编写 Dockerfile 构建测试镜像
- [ ] 使用 Docker Compose 编排多容器
- [ ] 使用 testcontainers 进行容器化测试
- [ ] CI/CD 中集成 Docker 测试

### 应该了解
- [ ] 多阶段构建优化镜像体积
- [ ] Docker 网络和数据卷
- [ ] 私有镜像仓库使用
- [ ] 容器安全最佳实践

---

## 四、练习内容

### 基础练习（1-8）

#### 练习1：Docker 基础操作

**场景说明：**
作为测试工程师，需要在本地快速搭建测试环境，使用 Docker 可以避免手动安装各种依赖。

**具体需求：**
1. 拉取 Python 3.11 镜像
2. 运行一个交互式容器
3. 在容器内执行 Python 代码
4. 查看容器日志和状态

**使用示例：**
```bash
# 拉取镜像
docker pull python:3.11-slim

# 运行交互式容器
docker run -it --name my-python python:3.11-slim bash

# 在容器内执行
python -c "print('Hello Docker')"

# 查看容器状态
docker ps -a
docker inspect my-python
```

**验收标准：**
- [ ] 成功拉取 Python 3.11 镜像
- [ ] 能运行交互式容器
- [ ] 能在容器内执行 Python 代码
- [ ] 能查看容器详细信息和日志

---

#### 练习2：编写 Dockerfile

**场景说明：**
团队需要将测试环境标准化，使用 Dockerfile 可以确保所有开发者在相同的环境中运行测试。

**具体需求：**
1. 创建一个基于 Python 3.11 的测试镜像
2. 安装 pytest 和 requests 库
3. 复制测试代码到镜像
4. 设置默认运行 pytest

**使用示例：**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tests/ ./tests/
CMD ["pytest", "tests/", "-v"]
```

**验收标准：**
- [ ] Dockerfile 语法正确
- [ ] 构建成功无报错
- [ ] 镜像能正常运行测试
- [ ] 镜像大小合理（< 500MB）

---

#### 练习3：Dockerfile 多阶段构建

**场景说明：**
生产环境需要最小化镜像体积以提高部署效率，多阶段构建可以只保留运行时必需的文件。

**具体需求：**
1. 第一阶段安装构建依赖
2. 第二阶段只复制运行时文件
3. 最终镜像体积减少 50% 以上

**使用示例：**
```dockerfile
# 阶段1：构建
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# 阶段2：运行
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/deps /usr/local/lib/python3.11/site-packages
COPY . .
CMD ["pytest"]
```

**验收标准：**
- [ ] 使用多阶段构建语法
- [ ] 最终镜像体积明显减小
- [ ] 测试仍能正常运行
- [ ] 构建时间在可接受范围内

---

#### 练习4：Docker Compose 基础

**场景说明：**
测试需要依赖多个服务（数据库、缓存等），使用 Docker Compose 可以一键启动所有依赖。

**具体需求：**
1. 编写 docker-compose.yml 文件
2. 定义 MySQL 和 Redis 服务
3. 配置端口映射和环境变量
4. 使用命令启动和停止服务

**使用示例：**
```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: test123
      MYSQL_DATABASE: testdb
    ports:
      - "3307:3306"

  redis:
    image: redis:7
    ports:
      - "6380:6379"
```

**验收标准：**
- [ ] docker-compose.yml 语法正确
- [ ] docker-compose up 成功启动所有服务
- [ ] 能通过映射端口访问服务
- [ ] docker-compose down 正确清理资源

---

#### 练习5：Docker Compose 服务依赖

**场景说明：**
测试需要等待数据库完全启动后才能运行，需要配置服务依赖和健康检查。

**具体需求：**
1. 配置数据库健康检查
2. 设置测试服务依赖数据库
3. 测试服务在数据库就绪后启动

**使用示例：**
```yaml
services:
  db:
    image: mysql:8.0
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 5s
      retries: 10

  test:
    build: .
    depends_on:
      db:
        condition: service_healthy
```

**验收标准：**
- [ ] 健康检查配置正确
- [ ] depends_on 使用 condition
- [ ] 测试在数据库就绪后执行
- [ ] 启动顺序符合预期

---

#### 练习6：testcontainers MySQL

**场景说明：**
集成测试需要真实的数据库环境，使用 testcontainers 可以在测试时自动启动临时数据库。

**具体需求：**
1. 使用 testcontainers 启动 MySQL 容器
2. 获取容器连接信息
3. 执行数据库操作
4. 测试结束后自动清理

**使用示例：**
```python
from testcontainers.mysql import MySqlContainer
import pymysql

def test_with_mysql():
    with MySqlContainer("mysql:8.0") as mysql:
        conn = pymysql.connect(
            host=mysql.get_container_host_ip(),
            port=mysql.get_exposed_port(3306),
            user="root",
            password="test"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        assert cursor.fetchone() is not None
```

**验收标准：**
- [ ] 容器成功启动
- [ ] 能获取正确的连接信息
- [ ] 数据库操作正常
- [ ] 测试后容器自动清理

---

#### 练习7：testcontainers Redis

**场景说明：**
测试缓存功能需要 Redis 环境，使用 testcontainers 可以快速创建隔离的 Redis 实例。

**具体需求：**
1. 启动 Redis 容器
2. 执行缓存读写操作
3. 验证数据正确性

**使用示例：**
```python
from testcontainers.redis import RedisContainer
import redis

def test_with_redis():
    with RedisContainer("redis:7") as redis_container:
        client = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379)
        )
        client.set("key", "value")
        assert client.get("key") == b"value"
```

**验收标准：**
- [ ] Redis 容器成功启动
- [ ] 能执行 set/get 操作
- [ ] 数据读写正确
- [ ] 连接配置正确

---

#### 练习8：testcontainers pytest fixture

**场景说明：**
多个测试用例需要共享同一个数据库容器，使用 pytest fixture 可以提高效率。

**具体需求：**
1. 创建 session 级别的 fixture
2. 多个测试共享容器
3. 每个测试使用独立的数据

**使用示例：**
```python
import pytest
from testcontainers.mysql import MySqlContainer

@pytest.fixture(scope="session")
def mysql_container():
    with MySqlContainer("mysql:8.0") as mysql:
        yield mysql

@pytest.fixture
def db_connection(mysql_container):
    # 每个测试获取新连接
    conn = create_connection(mysql_container)
    yield conn
    conn.close()

def test_case1(db_connection):
    # 使用数据库连接
    pass

def test_case2(db_connection):
    # 使用数据库连接
    pass
```

**验收标准：**
- [ ] fixture 作用域正确
- [ ] 容器只启动一次
- [ ] 每个测试获取独立连接
- [ ] 测试后资源正确清理

---

### 进阶练习（9-16）

#### 练习9：自定义 testcontainers 容器

**场景说明：**
需要测试的项目依赖特定的服务（如 Elasticsearch、Kafka），需要自定义容器配置。

**具体需求：**
1. 继承 GenericContainer 创建自定义容器
2. 配置环境变量和端口
3. 添加等待策略

**使用示例：**
```python
from testcontainers.core.generic import GenericContainer
from testcontainers.core.waiting_utils import wait_for

class ElasticsearchContainer(GenericContainer):
    def __init__(self):
        super().__init__("elasticsearch:8.0")
        self.with_exposed_ports(9200)
        self.with_env("discovery.type", "single-node")

    def get_url(self):
        return f"http://{self.get_container_host_ip()}:{self.get_exposed_port(9200)}"
```

**验收标准：**
- [ ] 自定义容器类正确实现
- [ ] 环境变量配置生效
- [ ] 端口映射正确
- [ ] 服务可正常访问

---

#### 练习10：Docker 网络配置

**场景说明：**
多个容器需要相互通信，需要配置 Docker 网络。

**具体需求：**
1. 创建自定义网络
2. 容器加入同一网络
3. 通过容器名互相访问

**使用示例：**
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - frontend

  api:
    image: python:3.11
    networks:
      - frontend
      - backend

  db:
    image: mysql:8.0
    networks:
      - backend

networks:
  frontend:
  backend:
```

**验收标准：**
- [ ] 自定义网络创建成功
- [ ] 容器正确加入网络
- [ ] 容器间可以通过名称访问
- [ ] 网络隔离符合预期

---

#### 练习11：Docker 数据卷

**场景说明：**
需要持久化测试数据和共享文件，使用数据卷可以管理容器数据。

**具体需求：**
1. 创建命名卷
2. 挂载到容器指定路径
3. 数据在容器删除后保留

**使用示例：**
```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    volumes:
      - db_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  db_data:
```

**验收标准：**
- [ ] 命名卷创建成功
- [ ] 数据正确持久化
- [ ] 容器删除后数据保留
- [ ] 文件挂载正确

---

#### 练习12：容器化测试环境完整配置

**场景说明：**
为一个完整的测试项目配置容器化环境，包括数据库、缓存、Mock 服务。

**具体需求：**
1. 配置 MySQL + Redis + Mock API
2. 编写测试运行容器
3. 配置依赖和启动顺序

**使用示例：**
```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: test123
    healthcheck:
      test: ["CMD", "mysqladmin", "ping"]
      interval: 5s
      retries: 10

  redis:
    image: redis:7

  mock:
    image: wiremock/wiremock
    ports:
      - "8080:8080"

  test:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      REDIS_HOST: redis
      MOCK_URL: http://mock:8080
```

**验收标准：**
- [ ] 所有服务正确配置
- [ ] 健康检查生效
- [ ] 环境变量传递正确
- [ ] 测试成功运行

---

#### 练习13：Docker 镜像优化

**场景说明：**
镜像体积过大影响构建和部署速度，需要优化 Dockerfile。

**具体需求：**
1. 使用 slim 基础镜像
2. 合并 RUN 指令减少层数
3. 清理缓存文件
4. 使用 .dockerignore

**使用示例：**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 合并安装和清理
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 使用缓存挂载
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .
```

**验收标准：**
- [ ] 镜像体积减少 30%+
- [ ] 构建时间合理
- [ ] 测试正常运行
- [ ] 使用了 .dockerignore

---

#### 练习14：Docker in CI/CD

**场景说明：**
在 CI/CD 流水线中使用 Docker 运行测试。

**具体需求：**
1. 配置 GitHub Actions 或 GitLab CI
2. 使用服务容器
3. 缓存 Docker 层

**使用示例：**
```yaml
# GitHub Actions
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: test123
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t test-image .
      - run: docker run test-image pytest
```

**验收标准：**
- [ ] CI 配置正确
- [ ] 服务容器正常启动
- [ ] 测试成功运行
- [ ] 构建日志清晰

---

#### 练习15：容器日志和调试

**场景说明：**
测试失败时需要查看容器日志进行调试。

**具体需求：**
1. 配置日志驱动
2. 查看容器标准输出
3. 进入容器调试

**使用示例：**
```bash
# 查看日志
docker logs container-name
docker logs -f --tail 100 container-name

# 进入容器
docker exec -it container-name bash

# 查看进程
docker top container-name

# 查看资源使用
docker stats container-name
```

**验收标准：**
- [ ] 能查看实时日志
- [ ] 能进入容器调试
- [ ] 能查看资源使用情况
- [ ] 能导出容器日志

---

#### 练习16：Docker 安全最佳实践

**场景说明：**
生产环境需要注意容器安全，避免安全漏洞。

**具体需求：**
1. 使用非 root 用户运行
2. 只读文件系统
3. 限制资源使用

**使用示例：**
```dockerfile
FROM python:3.11-slim

# 创建非 root 用户
RUN useradd -m appuser
USER appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

CMD ["pytest"]
```

```yaml
services:
  app:
    build: .
    read_only: true
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

**验收标准：**
- [ ] 使用非 root 用户
- [ ] 文件系统只读配置
- [ ] 资源限制生效
- [ ] 安全扫描无高危漏洞

---

### 综合练习（17-20）

#### 练习17：完整的容器化测试项目

**场景说明：**
为一个 API 项目创建完整的容器化测试环境。

**具体需求：**
1. 编写 Dockerfile 构建测试镜像
2. 编写 docker-compose.yml 配置所有依赖
3. 配置 testcontainers 进行集成测试
4. 编写 CI 配置文件

**验收标准：**
- [ ] Dockerfile 优化合理
- [ ] 所有依赖服务正确配置
- [ ] 集成测试通过
- [ ] CI 流水线成功

---

#### 练习18：测试数据库迁移

**场景说明：**
测试数据库 schema 迁移脚本，需要干净的数据库环境。

**具体需求：**
1. 启动临时数据库容器
2. 执行迁移脚本
3. 验证迁移结果
4. 清理容器

**验收标准：**
- [ ] 迁移脚本执行成功
- [ ] 数据库结构正确
- [ ] 测试数据验证通过
- [ ] 资源正确清理

---

#### 练习19：并行测试容器隔离

**场景说明：**
并行运行测试需要为每个进程创建独立的容器实例。

**具体需求：**
1. 使用 pytest-xdist 并行测试
2. 每个进程独立的数据库容器
3. 避免数据冲突

**验收标准：**
- [ ] 并行测试成功
- [ ] 容器隔离正确
- [ ] 无数据冲突
- [ ] 测试结果正确

---

#### 练习20：容器化测试报告

**场景说明：**
将测试报告从容器导出到主机。

**具体需求：**
1. 配置卷挂载导出报告
2. 生成 Allure 报告
3. 配置报告目录权限

**验收标准：**
- [ ] 报告正确导出
- [ ] Allure 报告生成成功
- [ ] 文件权限正确
- [ ] 报告内容完整

---

## 五、检验标准

### 自测题

1. Docker 镜像和容器有什么区别？
2. 如何编写一个优化的 Dockerfile？
3. testcontainers 相比手动启动容器有什么优势？
4. 如何在 CI/CD 中使用 Docker 运行测试？

### 参考答案

1. 镜像是只读模板，容器是镜像的运行实例
2. 使用 slim 基础镜像、多阶段构建、合并层数、清理缓存
3. 自动管理生命周期、测试隔离、无需手动清理
4. 使用 services 配置依赖容器，或 docker-compose action
