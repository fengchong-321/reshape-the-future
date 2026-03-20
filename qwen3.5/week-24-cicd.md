# 第 24 周 - CI/CD

## 学习目标
掌握持续集成和持续部署的概念，能够配置自动化 pipeline。

---

## 知识点清单

### 1. CI 概念
**掌握程度**: 持续集成、自动化

**练习资源**:
- [CI/CD 概念](https://www.atlassian.com/continuous-delivery)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

**练习任务**:
- 理解 CI 的价值
- 理解 CI/CD 流程

---

### 2. GitHub Actions
**掌握程度**: workflow、job、step

**练习任务**:
- 编写 workflow 文件
- 理解 job 和 step

---

### 3. 触发器
**掌握程度**: push/pull_request/schedule

**练习任务**:
- 配置 push 触发
- 配置 PR 触发
- 配置定时触发

---

### 4. 缓存
**掌握程度**: 依赖缓存、加速

**练习任务**:
- 配置依赖缓存
- 优化构建速度

---

### 5. 制品
**掌握程度**: 上传、下载、保留

**练习任务**:
- 上传构建制品
- 下载制品

---

### 6. 部署
**掌握程度**: 自动部署、环境管理

**练习任务**:
- 配置自动部署
- 管理多环境

---

### 7. Jenkins
**掌握程度**: Pipeline、语法

**练习资源**:
- [Jenkins 文档](https://www.jenkins.io/doc/)

**练习任务**:
- 理解 Jenkins Pipeline
- 编写 Pipeline 脚本

---

### 8. 最佳实践
**掌握程度**: 安全、效率、维护

**练习任务**:
- 遵循 CI/CD 最佳实践
- 配置安全扫描

---

## 本周练习任务

### 必做任务

1. **GitHub Actions 配置**
```yaml
# 为测试项目配置 CI/CD pipeline
# 功能:
# - 提交后自动运行测试
# - 测试通过后构建镜像
# - 推送镜像到 Docker Hub
# - 部署到测试环境

# 要求:
# - 测试失败阻止部署
# - 有通知机制
```

2. **多环境部署**
```yaml
# 配置多环境部署
# 环境:
# - dev: 开发环境
# - staging: 预发环境
# - prod: 生产环境

# 要求:
# - 不同环境不同配置
# - prod 环境需要手动确认
```

3. **Jenkins Pipeline**
```groovy
// 编写一个 Jenkins Pipeline
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker build -t myapp .'
                sh 'docker push myapp'
            }
        }
    }
}
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] CI/CD pipeline 能自动运行
- [ ] 测试失败能阻止部署
- [ ] 阶段二总结：技术栈自评
- [ ] 能解释 CI 和 CD 的区别
- [ ] 能配置多环境部署

---

## GitHub Actions 速查表

### Workflow 示例
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          push: true
          tags: user/app:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
```

### 缓存配置
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### 制品上传
```yaml
- name: Upload artifact
  uses: actions/upload-artifact@v3
  with:
    name: build-artifact
    path: dist/
```

---

## 面试考点

### 高频面试题
1. CI/CD 的价值？
2. GitHub Actions 的工作原理？
3. 如何配置缓存加速？
4. 如何管理多环境？
5. 如何保证部署安全？
6. Jenkins Pipeline 语法？
7. 如何处理失败？

### 场景题
```yaml
# 1. 配置只有 main 分支才部署
if: github.ref == 'refs/heads/main'

# 2. 配置手动确认部署
environment:
  name: production
  url: https://example.com

# 3. 配置失败通知
- name: Notify on failure
  if: failure()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }}
```

---

## 每日学习检查清单

### Day 1-2: CI 概念 + GitHub Actions
- [ ] 学习 CI/CD 概念
- [ ] 学习 GitHub Actions
- [ ] 编写 workflow
- [ ] GitHub 提交

### Day 3-4: 缓存 + 制品 + 部署
- [ ] 配置缓存
- [ ] 配置制品
- [ ] 配置部署
- [ ] GitHub 提交

### Day 5-6: 多环境 + Jenkins
- [ ] 配置多环境
- [ ] 学习 Jenkins
- [ ] 编写 Pipeline
- [ ] 阶段二总结

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成 pipeline 配置
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 24 周总结

### 学习内容
- 掌握了 CI/CD
- 能配置 GitHub Actions
- 理解了自动化部署

### 作品
- CI/CD pipeline 配置
- Jenkins Pipeline

### 阶段二总结
- UI 自动化：✅ 已掌握
- 接口自动化：✅ 已掌握
- Web 开发：✅ 已掌握
- DevOps: ✅ 已掌握

### 遇到的问题
- ...

### 阶段三计划
- 测试平台开发
- 性能测试专项
- 开源贡献
```
