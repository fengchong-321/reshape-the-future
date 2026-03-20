# 第 23 周 - Kubernetes 基础

## 学习目标
掌握 Kubernetes 核心概念，能够在 K8s 上部署应用。

---

## 知识点清单

### 1. 核心概念
**掌握程度**: Pod、Node、Cluster

**练习资源**:
- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Kubernetes 入门](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

**练习任务**:
- 理解 K8s 架构
- 理解 Pod 和容器的关系

---

### 2. 安装
**掌握程度**: minikube/kind、kubectl

**练习任务**:
- 安装 minikube 或 kind
- 安装 kubectl
- 启动本地集群

---

### 3. Pod
**掌握程度**: 定义、生命周期

**练习任务**:
- 编写 Pod 配置
- 部署 Pod
- 查看 Pod 状态

---

### 4. Deployment
**掌握程度**: 副本、滚动更新

**练习任务**:
- 编写 Deployment 配置
- 部署应用
- 执行滚动更新

---

### 5. Service
**掌握程度**: ClusterIP/NodePort/LoadBalancer

**练习任务**:
- 编写 Service 配置
- 暴露服务
- 理解服务类型

---

### 6. ConfigMap
**掌握程度**: 配置分离、环境变量

**练习任务**:
- 创建 ConfigMap
- 在 Pod 中使用 ConfigMap

---

### 7. Secret
**掌握程度**: 敏感信息、加密

**练习任务**:
- 创建 Secret
- 管理敏感信息

---

### 8. 调试
**掌握程度**: logs/exec/describe

**练习任务**:
- 查看日志
- 进入 Pod
- 查看详细信息

---

## 本周练习任务

### 必做任务

1. **部署 Web 应用**
```yaml
# 在 minikube 上部署一个 Web 应用
# 要求:
# - 使用 Deployment
# - 使用 Service 暴露
# - 配置健康检查
# - 能够访问
```

2. **水平扩缩容**
```yaml
# 配置 HPA（Horizontal Pod Autoscaler）
# 要求:
# - 基于 CPU 使用率
# - 最小 1 个副本
# - 最大 5 个副本
```

3. **滚动更新和回滚**
```bash
# 执行滚动更新
kubectl set image deployment/api api=myapp:2.0

# 查看更新状态
kubectl rollout status deployment/api

# 回滚
kubectl rollout undo deployment/api
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 应用能在 K8s 上运行
- [ ] 能执行扩容和回滚操作
- [ ] 博客：《Kubernetes 核心概念整理》
- [ ] 能解释 Pod 和 Deployment 的区别
- [ ] 能配置 ConfigMap 和 Secret

---

## Kubernetes 速查表

### kubectl 命令
```bash
# 集群信息
kubectl cluster-info
kubectl get nodes
kubectl version

# Pod 操作
kubectl get pods
kubectl get pods -n <namespace>
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- bash
kubectl delete pod <pod-name>

# Deployment 操作
kubectl get deployments
kubectl create deployment myapp --image=myapp:1.0
kubectl set image deployment/myapp myapp=myapp:2.0
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp

# Service 操作
kubectl get services
kubectl expose deployment/myapp --type=NodePort --port=80

# 配置
kubectl create configmap my-config --from-literal=key=value
kubectl create secret generic my-secret --from-literal=password=123

# 应用配置
kubectl apply -f config.yaml
kubectl delete -f config.yaml
```

### Pod 配置示例
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp
    image: myapp:1.0
    ports:
    - containerPort: 8000
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 30
      periodSeconds: 10
```

### Deployment 配置示例
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
        ports:
        - containerPort: 8000
```

### Service 配置示例
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
    nodePort: 30080
```

---

## 面试考点

### 高频面试题
1. K8s 的架构？
2. Pod 和容器的区别？
3. Deployment 的作用？
4. Service 的类型有哪些？
5. ConfigMap 和 Secret 的区别？
6. 滚动更新的原理？
7. HPA 的工作原理？

### 场景题
```yaml
# 1. 配置健康检查
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

# 2. 配置资源限制
resources:
  limits:
    memory: "512Mi"
    cpu: "1"
  requests:
    memory: "256Mi"
    cpu: "500m"
```

---

## 每日学习检查清单

### Day 1-2: 核心概念 + 安装
- [ ] 学习 K8s 架构
- [ ] 安装 minikube
- [ ] 安装 kubectl
- [ ] 启动集群
- [ ] GitHub 提交

### Day 3-4: Pod + Deployment
- [ ] 学习 Pod 配置
- [ ] 学习 Deployment
- [ ] 部署应用
- [ ] GitHub 提交

### Day 5-6: Service + ConfigMap + Secret
- [ ] 学习 Service
- [ ] 学习 ConfigMap
- [ ] 学习 Secret
- [ ] 配置 HPA
- [ ] 写博客

### Day 7: 复习
- [ ] 复习本周内容
- [ ] 完成部署
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 23 周总结

### 学习内容
- 掌握了 K8s 基础
- 能部署应用到 K8s
- 理解了核心概念

### 作品
- K8s 部署文档
- 博客文章

### 遇到的问题
- ...

### 下周改进
- ...
```
