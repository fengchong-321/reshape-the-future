# 第10周:CI/CD与Jenkins

## 本周目标

掌握CI/CD基本概念,熟练使用Jenkins搭建自动化测试流水线,实现测试与持续集成的无缝对接。

---

## 一、知识点表格

| 主题 | 内容 | 重要性 |
|------|------|--------|
| CI/CD概念 | 持续集成、持续交付/部署 | ⭐⭐⭐⭐⭐ |
| Jenkins安装 | 环境搭建、插件管理 | ⭐⭐⭐⭐ |
| Job配置 | 自由风格项目、构建触发器 | ⭐⭐⭐⭐⭐ |
| Pipeline | 声明式、脚本式Pipeline | ⭐⭐⭐⭐⭐ |
| 参数化构建 | 构建参数、环境变量 | ⭐⭐⭐⭐ |
| 测试集成 | Pytest集成、报告展示 | ⭐⭐⭐⭐⭐ |
| 多环境部署 | Dev/Test/Prod环境管理 | ⭐⭐⭐⭐ |
| 通知机制 | 邮件、钉钉、企业微信 | ⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 CI/CD基础概念

```markdown
持续集成(CI):
- 开发人员频繁将代码集成到主干
- 每次集成都通过自动化构建和测试
- 目标:快速发现错误,防止分支大幅偏离

持续交付(CD):
- 将集成后的代码部署到生产环境
- 每次变更都可随时部署
- 部署过程自动化

持续部署(CD):
- 代码通过测试后自动部署到生产
- 完全自动化的发布流程

CI/CD流水线典型阶段:
1. 代码提交(Source)
2. 编译构建(Build)
3. 自动化测试(Test)
4. 部署到测试环境(Deploy to Staging)
5. 部署到生产环境(Deploy to Production)
```

---

### 2.2 Jenkins安装与配置

```bash
# ============================================
# 方式1:Docker安装(推荐)
# ============================================
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# 查看初始密码
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# ============================================
# 方式2:直接安装
# ============================================
# Ubuntu/Debian
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins

# macOS
brew install jenkins-lts

# 启动Jenkins
sudo systemctl start jenkins  # Linux
brew services start jenkins-lts  # macOS

# ============================================
# 初始化配置
# ============================================
# 1. 访问 http://localhost:8080
# 2. 输入初始密码
# 3. 安装推荐插件
# 4. 创建管理员账户
# 5. 配置Jenkins URL

# ============================================
# 推荐插件
# ============================================
# - Pipeline
# - Git
# - Credentials Binding
# - Email Extension
# - Allure
# - Docker
# - Blue Ocean
```

---

### 2.3 Jenkins Job配置

```groovy
# ============================================
# 自由风格项目配置
# ============================================
# 1. 新建任务 -> 自由风格项目
# 2. 源码管理 -> Git配置
# 3. 构建触发器 -> 定时构建/轮询SCM
# 4. 构建步骤 -> 执行shell/Invoke pytest
# 5. 构建后操作 -> 归档制品/发送邮件

# ============================================
# 定时构建配置
# ============================================
# H/15 * * * *  每15分钟执行一次
# H 2 * * *     每天凌晨2点执行
# H H(0-7) * * * 每天凌晨0-7点之间执行一次

# ============================================
# Git配置
# ============================================
Repository URL: https://github.com/user/repo.git
Credentials: 添加Git凭据
Branch: */main

# ============================================
# 构建步骤示例
# ============================================
# 执行Shell
#!/bin/bash
python -m pytest tests/ -v --alluredir=report

# Windows批处理
python -m pytest tests/ -v --alluredir=report
```

---

### 2.4 Pipeline语法

```groovy
// ============================================
// 声明式Pipeline(推荐)
// ============================================
pipeline {
    agent any  // 在任何可用agent上执行

    // 环境变量
    environment {
        PROJECT_NAME = 'api_test'
        REPORT_PATH = 'report'
    }

    // 构建参数
    parameters {
        string(name: 'ENV', defaultValue: 'test', description: '测试环境')
        booleanParam(name: 'SKIP_TEST', defaultValue: false, description: '跳过测试')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox', 'edge'], description: '浏览器类型')
    }

    // 工具配置
    tools {
        python 'Python3.9'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '拉取代码...'
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                echo '安装依赖...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            when {
                expression { params.SKIP_TEST == false }
            }
            steps {
                echo '执行测试...'
                sh 'pytest tests/ -v --alluredir=${REPORT_PATH}'
            }
        }

        stage('Report') {
            steps {
                echo '生成报告...'
                allure includeProperties: false, jdk: '', results: [[path: '${REPORT_PATH}']]
            }
        }
    }

    // 构建后操作
    post {
        always {
            echo '清理工作空间...'
            cleanWs()
        }
        success {
            echo '构建成功!'
            mail to: 'team@example.com',
                 subject: "构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "构建成功,请查看报告"
        }
        failure {
            echo '构建失败!'
            mail to: 'team@example.com',
                 subject: "构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "构建失败,请检查日志"
        }
    }
}

// ============================================
// 脚本式Pipeline
// ============================================
node {
    def projectPath = '/tmp/project'

    stage('Prepare') {
        dir(projectPath) {
            checkout scm
        }
    }

    stage('Build') {
        dir(projectPath) {
            sh 'pip install -r requirements.txt'
        }
    }

    stage('Test') {
        dir(projectPath) {
            try {
                sh 'pytest tests/ -v'
            } catch (Exception e) {
                currentBuild.result = 'FAILURE'
                throw e
            }
        }
    }
}

// ============================================
// 多分支Pipeline
// ============================================
// Jenkinsfile放在项目根目录
// 自动扫描所有分支并创建Pipeline
```

---

### 2.5 参数化构建

```groovy
// ============================================
// 参数类型
// ============================================
pipeline {
    agent any

    parameters {
        // 字符串参数
        string(name: 'USERNAME', defaultValue: 'admin', description: '用户名')

        // 文本参数
        text(name: 'DESCRIPTION', defaultValue: '', description: '描述信息')

        // 布尔参数
        booleanParam(name: 'DEBUG_MODE', defaultValue: false, description: '调试模式')

        // 选择参数
        choice(name: 'ENVIRONMENT', choices: ['dev', 'test', 'staging', 'prod'], description: '环境')

        // 文件参数
        file(name: 'CONFIG_FILE', description: '配置文件')

        // 密码参数
        password(name: 'API_KEY', defaultValue: '', description: 'API密钥')

        // 运行时参数
        runParam(name: 'UPSTREAM_BUILD', description: '上游构建')
    }

    stages {
        stage('Example') {
            steps {
                echo "用户名: ${params.USERNAME}"
                echo "环境: ${params.ENVIRONMENT}"
                echo "调试模式: ${params.DEBUG_MODE}"
            }
        }
    }
}

// ============================================
// 动态参数(使用Active Choices插件)
// ============================================
// 需要安装 Active Choices Plugin
// 可以根据其他参数的值动态生成选项
```

---

### 2.6 测试集成

```groovy
// ============================================
// Pytest集成
// ============================================
pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh '''
                    virtualenv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v \
                        --junitxml=report/junit.xml \
                        --alluredir=report/allure-results \
                        --html=report/report.html
                '''
            }
        }

        stage('Publish Report') {
            steps {
                // 发布JUnit报告
                junit 'report/junit.xml'

                // 发布Allure报告
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'report/allure-results']]

                // 发布HTML报告
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'report',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
}

// ============================================
// 并行测试执行
// ============================================
pipeline {
    agent any

    stages {
        stage('Parallel Tests') {
            parallel {
                stage('API Tests') {
                    steps {
                        sh 'pytest tests/api/ -v'
                    }
                }
                stage('UI Tests') {
                    steps {
                        sh 'pytest tests/ui/ -v'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'pytest tests/integration/ -v'
                    }
                }
            }
        }
    }
}
```

---

### 2.7 通知机制

```groovy
// ============================================
// 邮件通知
// ============================================
pipeline {
    agent any

    post {
        success {
            emailext(
                subject: "构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>构建成功</h2>
                    <p>项目: ${env.JOB_NAME}</p>
                    <p>构建号: ${env.BUILD_NUMBER}</p>
                    <p>构建地址: ${env.BUILD_URL}</p>
                """,
                to: 'team@example.com',
                mimeType: 'text/html'
            )
        }
        failure {
            emailext(
                subject: "构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>构建失败</h2>
                    <p>项目: ${env.JOB_NAME}</p>
                    <p>构建号: ${env.BUILD_NUMBER}</p>
                    <p>请检查: ${env.BUILD_URL}console</p>
                """,
                to: 'team@example.com',
                mimeType: 'text/html'
            )
        }
    }
}

// ============================================
// 钉钉通知
// ============================================
// 需要安装 DingTalk 插件
dingtalk(
    robot: 'dingtalk-robot',
    type: 'MARKDOWN',
    title: '构建通知',
    text: [
        "# 构建通知",
        "- 项目: ${env.JOB_NAME}",
        "- 构建号: ${env.BUILD_NUMBER}",
        "- 状态: ${currentBuild.result}",
        "- [查看详情](${env.BUILD_URL})"
    ]
)

// ============================================
// 企业微信通知
// ============================================
// 使用webhook发送消息
def sendWeworkNotification(String status) {
    def webhookUrl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY'

    def payload = """
    {
        "msgtype": "markdown",
        "markdown": {
            "content": "### 构建通知\\n
                        > 项目: ${env.JOB_NAME}\\n
                        > 构建号: ${env.BUILD_NUMBER}\\n
                        > 状态: ${status}\\n
                        > [查看详情](${env.BUILD_URL})"
        }
    }
    """

    httpRequest(
        url: webhookUrl,
        httpMode: 'POST',
        contentType: 'APPLICATION_JSON',
        requestBody: payload
    )
}
```

---

### 2.8 多环境管理

```groovy
// ============================================
// 环境配置
// ============================================
pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'test', 'staging', 'prod'], description: '部署环境')
    }

    environment {
        // 根据环境设置不同的配置
        CONFIG_FILE = "config/${params.DEPLOY_ENV}.yaml"
    }

    stages {
        stage('Load Config') {
            steps {
                script {
                    // 加载环境配置
                    def config = readYaml file: env.CONFIG_FILE
                    env.DB_HOST = config.database.host
                    env.API_URL = config.api.url
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "部署到 ${params.DEPLOY_ENV} 环境"
                echo "数据库: ${env.DB_HOST}"
                echo "API: ${env.API_URL}"
                // 部署逻辑
            }
        }
    }
}

// ============================================
// 使用Credentials管理敏感信息
// ============================================
pipeline {
    agent any

    environment {
        // 从Jenkins Credentials中获取
        DB_PASSWORD = credentials('db-password')
        API_KEY = credentials('api-key')
    }

    stages {
        stage('Use Credentials') {
            steps {
                sh 'echo $DB_PASSWORD | docker login -u admin --password-stdin'
            }
        }
    }
}

// ============================================
// 审批流程(生产环境)
// ============================================
pipeline {
    agent any

    stages {
        stage('Deploy to Staging') {
            steps {
                echo '部署到测试环境'
            }
        }

        stage('Approval') {
            when {
                expression { params.DEPLOY_ENV == 'prod' }
            }
            steps {
                input message: '确认部署到生产环境?',
                      ok: '确认部署',
                      submitter: 'admin,release-team'
            }
        }

        stage('Deploy to Production') {
            when {
                expression { params.DEPLOY_ENV == 'prod' }
            }
            steps {
                echo '部署到生产环境'
            }
        }
    }
}
```

---

## 三、学到什么程度

### 必须掌握

- [ ] CI/CD基本概念
- [ ] Jenkins安装和基础配置
- [ ] Pipeline基本语法
- [ ] 测试集成与报告

### 应该了解

- [ ] 参数化构建
- [ ] 多环境管理
- [ ] 通知机制配置
- [ ] 分布式构建

---

## 四、练习内容

### 基础练习(1-8)

#### 练习1:Jenkins环境搭建

**场景说明:**
你刚入职一家公司,团队需要搭建CI/CD环境来自动化测试流程。作为测试开发工程师,你需要负责Jenkins的安装和基础配置。

**具体需求:**
1. 使用Docker方式安装Jenkins
2. 完成Jenkins初始化配置
3. 安装必要插件(Pipeline、Git、Allure)
4. 创建第一个管理员账户
5. 验证Jenkins正常运行

**使用示例:**
```bash
# 1. 启动Jenkins容器
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# 2. 获取初始密码
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# 3. 访问 http://localhost:8080
# 4. 输入密码完成初始化
# 5. 安装推荐插件
# 6. 创建管理员账户
```

**验收标准:**
- [ ] Jenkins容器正常运行
- [ ] 能够通过浏览器访问Jenkins
- [ ] 成功登录管理员账户
- [ ] 已安装Pipeline、Git、Allure插件
- [ ] 系统信息页面显示Jenkins版本

---

#### 练习2:创建第一个自由风格Job

**场景说明:**
Jenkins环境搭建完成后,你需要创建第一个测试任务来自动运行项目的单元测试。

**具体需求:**
1. 创建一个自由风格项目
2. 配置Git仓库地址
3. 配置构建触发器(每15分钟轮询一次)
4. 添加构建步骤执行pytest
5. 配置构建后归档测试报告

**使用示例:**
```groovy
# Job配置步骤:
1. 新建任务 -> 输入名称 "unit_test" -> 自由风格项目
2. 源码管理 -> Git -> Repository URL: https://github.com/your/repo.git
3. 构建触发器 -> 轮询SCM -> H/15 * * * *
4. 构建 -> 执行shell:
   #!/bin/bash
   pip install -r requirements.txt
   pytest tests/ -v --junitxml=report/junit.xml
5. 构建后操作 -> 发布JUnit测试结果报告 -> report/junit.xml
```

**验收标准:**
- [ ] Job创建成功
- [ ] Git仓库配置正确
- [ ] 构建触发器配置正确
- [ ] 能够成功执行一次构建
- [ ] 测试报告正确显示

---

#### 练习3:编写第一个Pipeline

**场景说明:**
团队决定采用Pipeline as Code的方式来管理CI/CD流程,你需要将之前的自由风格Job改写为Pipeline。

**具体需求:**
1. 创建Pipeline项目
2. 编写包含Checkout、Setup、Test三个stage的Pipeline
3. 使用声明式语法
4. 配置Git作为代码源
5. 在Pipeline中执行pytest

**使用示例:**
```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest tests/ -v'
            }
        }
    }
}
```

**验收标准:**
- [ ] Pipeline项目创建成功
- [ ] 包含至少3个stage
- [ ] 使用声明式语法
- [ ] Pipeline能够成功执行
- [ ] 各stage日志输出正确

---

#### 练习4:配置构建参数

**场景说明:**
测试团队需要针对不同环境进行测试,需要能够灵活选择测试环境和测试范围。

**具体需求:**
1. 添加环境选择参数(dev/test/prod)
2. 添加测试类型选择参数(api/ui/all)
3. 添加是否发送通知的布尔参数
4. 在Pipeline中使用这些参数
5. 根据参数执行不同的测试

**使用示例:**
```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'test', 'prod'], description: '测试环境')
        choice(name: 'TEST_TYPE', choices: ['api', 'ui', 'all'], description: '测试类型')
        booleanParam(name: 'SEND_NOTIFICATION', defaultValue: true, description: '发送通知')
    }

    stages {
        stage('Test') {
            steps {
                script {
                    if (params.TEST_TYPE == 'api' || params.TEST_TYPE == 'all') {
                        sh "pytest tests/api/ -v --env=${params.ENV}"
                    }
                    if (params.TEST_TYPE == 'ui' || params.TEST_TYPE == 'all') {
                        sh "pytest tests/ui/ -v --env=${params.ENV}"
                    }
                }
            }
        }
    }
}
```

**验收标准:**
- [ ] 参数配置正确
- [ ] 能够在构建时选择参数
- [ ] 参数在Pipeline中正确使用
- [ ] 不同参数组合执行结果正确
- [ ] 参数显示在构建历史中

---

#### 练习5:集成Allure测试报告

**场景说明:**
团队需要更专业的测试报告来展示测试结果,包括趋势图和历史记录。

**具体需求:**
1. 安装Allure插件
2. 在Pipeline中生成Allure报告
3. 配置Allure报告发布
4. 验证报告正确显示
5. 查看历史趋势

**使用示例:**
```groovy
pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh 'pytest tests/ -v --alluredir=report/allure-results'
            }
        }

        stage('Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'report/allure-results']]
            }
        }
    }
}
```

**验收标准:**
- [ ] Allure插件安装成功
- [ ] 测试执行后生成Allure数据
- [ ] 报告在Jenkins中正确显示
- [ ] 报告包含测试用例详情
- [ ] 能够查看历史趋势

---

#### 练习6:配置邮件通知

**场景说明:**
测试完成后需要自动发送邮件通知团队成员,让相关人及时了解构建状态。

**具体需求:**
1. 配置Jenkins邮件服务器
2. 安装Email Extension插件
3. 配置构建成功/失败时发送邮件
4. 邮件包含构建信息和报告链接
5. 测试邮件通知功能

**使用示例:**
```groovy
pipeline {
    agent any

    post {
        success {
            emailext(
                subject: "构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>构建成功</h2>
                    <p>项目: ${env.JOB_NAME}</p>
                    <p>构建号: ${env.BUILD_NUMBER}</p>
                    <p>查看详情: ${env.BUILD_URL}</p>
                """,
                to: 'team@example.com',
                mimeType: 'text/html'
            )
        }
        failure {
            emailext(
                subject: "构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>构建失败</h2>
                    <p>请检查构建日志</p>
                    <p>日志地址: ${env.BUILD_URL}console</p>
                """,
                to: 'team@example.com',
                mimeType: 'text/html'
            )
        }
    }
}
```

**验收标准:**
- [ ] 邮件服务器配置正确
- [ ] Email Extension插件安装
- [ ] 构建成功时收到邮件
- [ ] 构建失败时收到邮件
- [ ] 邮件内容包含关键信息

---

#### 练习7:定时构建配置

**场景说明:**
团队需要每天晚上自动运行回归测试,并在第二天早上查看结果。

**具体需求:**
1. 配置每日凌晨2点自动构建
2. 配置每15分钟轮询SCM变更
3. 配置仅在有代码变更时构建
4. 验证定时任务执行
5. 查看构建历史

**使用示例:**
```groovy
pipeline {
    agent any

    triggers {
        // 每天凌晨2点执行
        cron('H 2 * * *')
        // 每15分钟检查一次代码变更
        pollSCM('H/15 * * * *')
    }

    stages {
        stage('Test') {
            steps {
                sh 'pytest tests/ -v'
            }
        }
    }
}
```

**验收标准:**
- [ ] 定时任务配置正确
- [ ] 能够在指定时间自动执行
- [ ] 轮询SCM配置正确
- [ ] 代码变更触发构建
- [ ] 构建历史记录完整

---

#### 练习8:Git集成与多分支

**场景说明:**
项目有多个分支需要分别进行CI,需要配置多分支Pipeline来自动管理。

**具体需求:**
1. 配置多分支Pipeline项目
2. 为不同分支创建Jenkinsfile
3. 配置分支发现策略
4. 验证分支扫描功能
5. 测试不同分支的构建

**使用示例:**
```groovy
// 项目根目录创建 Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Test') {
            steps {
                sh 'pytest tests/ -v'
            }
        }
    }
}

// 多分支Pipeline配置:
// 1. 新建任务 -> 多分支Pipeline
// 2. 配置Git仓库
// 3. 配置分支发现策略
// 4. 扫描分支
```

**验收标准:**
- [ ] 多分支Pipeline创建成功
- [ ] 能够自动发现所有分支
- [ ] 各分支有独立的构建历史
- [ ] 新分支自动创建Pipeline
- [ ] 删除分支后Pipeline自动清理

---

### 进阶练习(9-16)

#### 练习9:并行测试执行

**场景说明:**
测试套件越来越多,串行执行耗时太长,需要实现并行执行来缩短构建时间。

**具体需求:**
1. 将测试分为API、UI、Unit三组
2. 使用parallel阶段并行执行
3. 收集所有测试结果
4. 汇总测试报告
5. 比较并行前后的执行时间

**使用示例:**
```groovy
pipeline {
    agent any

    stages {
        stage('Parallel Tests') {
            parallel {
                stage('API Tests') {
                    steps {
                        sh 'pytest tests/api/ -v --junitxml=report/api.xml'
                    }
                }
                stage('UI Tests') {
                    steps {
                        sh 'pytest tests/ui/ -v --junitxml=report/ui.xml'
                    }
                }
                stage('Unit Tests') {
                    steps {
                        sh 'pytest tests/unit/ -v --junitxml=report/unit.xml'
                    }
                }
            }
        }

        stage('Publish Results') {
            steps {
                junit 'report/*.xml'
            }
        }
    }
}
```

**验收标准:**
- [ ] 三个测试组并行执行
- [ ] 所有测试结果正确收集
- [ ] 并行执行时间明显缩短
- [ ] 测试报告包含所有结果
- [ ] 构建日志清晰显示并行执行

---

#### 练习10:条件化Stage执行

**场景说明:**
不同分支需要执行不同的测试策略,main分支执行全量测试,其他分支执行快速测试。

**具体需求:**
1. 根据分支名称执行不同测试
2. main分支执行所有测试
3. feature分支执行快速测试
4. 使用when指令控制stage执行
5. 添加自定义条件判断

**使用示例:**
```groovy
pipeline {
    agent any

    stages {
        stage('Fast Tests') {
            steps {
                sh 'pytest tests/unit/ tests/api/ -v'
            }
        }

        stage('Full Tests') {
            when {
                branch 'main'
            }
            steps {
                sh 'pytest tests/ -v'
            }
        }

        stage('Integration Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                sh 'pytest tests/integration/ -v'
            }
        }

        stage('Performance Tests') {
            when {
                expression {
                    return params.RUN_PERFORMANCE == true
                }
            }
            steps {
                sh 'pytest tests/performance/ -v'
            }
        }
    }
}
```

**验收标准:**
- [ ] when指令使用正确
- [ ] 分支条件判断正确
- [ ] main分支执行全量测试
- [ ] 其他分支执行快速测试
- [ ] 自定义条件正常工作

---

#### 练习11:使用共享库

**场景说明:**
多个项目有相似的Pipeline逻辑,需要抽取公共代码到共享库中复用。

**具体需求:**
1. 创建Jenkins共享库
2. 定义公共Pipeline步骤
3. 在项目中引用共享库
4. 实现测试执行的公共方法
5. 验证共享库调用

**使用示例:**
```groovy
// 共享库文件: vars/runTests.groovy
def call(String testType, String env) {
    sh "pytest tests/${testType}/ -v --env=${env} --alluredir=report/allure-results"
    allure includeProperties: false, results: [[path: 'report/allure-results']]
}

// 共享库文件: vars/notify.groovy
def call(String status) {
    emailext(
        subject: "${status}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
        body: "构建状态: ${status}",
        to: 'team@example.com'
    )
}

// Pipeline中使用
@Library('my-shared-library') _

pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                runTests 'api', 'test'
            }
        }
    }

    post {
        always {
            notify currentBuild.result ?: 'SUCCESS'
        }
    }
}
```

**验收标准:**
- [ ] 共享库创建成功
- [ ] 公共方法定义正确
- [ ] Pipeline正确引用共享库
- [ ] 共享库方法正常调用
- [ ] 代码复用效果明显

---

#### 练习12:Docker Agent配置

**场景说明:**
需要在Docker容器中执行测试,以保证测试环境的一致性。

**具体需求:**
1. 配置Docker agent
2. 使用自定义Docker镜像
3. 挂载工作目录
4. 在容器中执行测试
5. 收集测试结果

**使用示例:**
```groovy
pipeline {
    agent {
        docker {
            image 'python:3.9'
            args '-v $HOME/.cache:/root/.cache'
        }
    }

    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest tests/ -v'
            }
        }
    }
}

// 或使用自定义镜像
pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile.test'
            dir 'docker'
            additionalBuildArgs '--build-arg PYTHON_VERSION=3.9'
        }
    }

    stages {
        stage('Test') {
            steps {
                sh 'pytest tests/ -v'
            }
        }
    }
}
```

**验收标准:**
- [ ] Docker agent配置正确
- [ ] 容器成功启动
- [ ] 测试在容器中执行
- [ ] 测试结果正确收集
- [ ] 容器执行后自动清理

---

#### 练习13:凭据管理

**场景说明:**
测试需要访问数据库和API,需要安全地管理密码和密钥等敏感信息。

**具体需求:**
1. 在Jenkins中添加凭据
2. 在Pipeline中使用凭据
3. 环境变量方式使用
4. 文件类型凭据使用
5. 验证凭据安全性

**使用示例:**
```groovy
pipeline {
    agent any

    environment {
        // 使用Secret Text
        API_KEY = credentials('api-key')

        // 使用Username/Password
        DB_CREDS = credentials('db-credentials')
    }

    stages {
        stage('Use Credentials') {
            steps {
                // 使用环境变量
                sh 'echo $API_KEY'

                // Username/Password分别访问
                sh "mysql -u $DB_CREDS_USR -p$DB_CREDS_PSW"

                // 使用withCredentials
                withCredentials([usernamePassword(
                    credentialsId: 'aws-credentials',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    sh 'aws s3 ls'
                }
            }
        }

        stage('Use File Credential') {
            steps {
                withCredentials([file(
                    credentialsId: 'ssh-key',
                    variable: 'SSH_KEY'
                )]) {
                    sh 'ssh -i $SSH_KEY user@server'
                }
            }
        }
    }
}
```

**验收标准:**
- [ ] 凭据成功添加到Jenkins
- [ ] Pipeline正确引用凭据
- [ ] 环境变量方式正常工作
- [ ] 文件凭据正确使用
- [ ] 日志中不显示敏感信息

---

#### 练习14:矩阵构建

**场景说明:**
需要在多个Python版本和多个环境下同时运行测试,验证兼容性。

**具体需求:**
1. 配置多Python版本(3.8, 3.9, 3.10)
2. 配置多环境(dev, test)
3. 使用矩阵构建实现组合
4. 收集所有组合的测试结果
5. 生成汇总报告

**使用示例:**
```groovy
pipeline {
    agent any

    parameters {
        // 手动选择时使用
        choice(name: 'PYTHON_VERSION', choices: ['3.8', '3.9', '3.10'], description: 'Python版本')
    }

    stages {
        stage('Matrix Test') {
            matrix {
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '3.8', '3.9', '3.10'
                    }
                    axis {
                        name 'ENVIRONMENT'
                        values 'dev', 'test'
                    }
                }

                stages {
                    stage('Setup') {
                        steps {
                            sh "docker run --rm -v $(pwd):/app -w /app python:${PYTHON_VERSION} pip install -r requirements.txt"
                        }
                    }

                    stage('Test') {
                        steps {
                            sh "docker run --rm -v $(pwd):/app -w /app python:${PYTHON_VERSION} pytest tests/ -v --env=${ENVIRONMENT}"
                        }
                    }
                }
            }
        }
    }
}
```

**验收标准:**
- [ ] 矩阵配置正确
- [ ] 所有组合都执行测试
- [ ] 测试结果按组合区分
- [ ] 汇总报告正确生成
- [ ] 失败组合正确标记

---

#### 练习15:集成SonarQube代码扫描

**场景说明:**
除了测试,还需要对代码进行静态分析,检查代码质量。

**具体需求:**
1. 安装SonarQube插件
2. 配置SonarQube服务器
3. 在Pipeline中集成代码扫描
4. 配置质量门限
5. 根据扫描结果决定是否继续

**使用示例:**
```groovy
pipeline {
    agent any

    environment {
        SONAR_SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                            -Dsonar.projectKey=my-project \
                            -Dsonar.sources=. \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '代码质量检查通过,开始部署'
            }
        }
    }
}
```

**验收标准:**
- [ ] SonarQube插件安装成功
- [ ] 服务器连接配置正确
- [ ] 代码扫描成功执行
- [ ] 扫描结果在Jenkins中显示
- [ ] 质量门限正常工作

---

#### 练习16:流水线可视化

**场景说明:**
需要更直观地展示Pipeline执行过程和状态,方便团队成员理解CI/CD流程。

**具体需求:**
1. 安装Blue Ocean插件
2. 使用Blue Ocean查看Pipeline
3. 添加阶段描述信息
4. 配置Pipeline图标和颜色
5. 生成Pipeline可视化图表

**使用示例:**
```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checkout code from repository'
                checkout scm
            }
            post {
                success {
                    echo 'Code checkout successful'
                }
            }
        }

        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'python setup.py build'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'pytest tests/ -v'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh 'python deploy.py'
            }
        }
    }
}

// 访问Blue Ocean:
// http://localhost:8080/blue
// 可以看到可视化的Pipeline执行过程
```

**验收标准:**
- [ ] Blue Ocean插件安装成功
- [ ] 能够用Blue Ocean查看Pipeline
- [ ] Pipeline阶段清晰可见
- [ ] 执行状态实时更新
- [ ] 日志查看方便

---

### 综合练习(17-20)

#### 练习17:完整CI/CD流水线

**场景说明:**
为公司的API测试项目设计一套完整的CI/CD流水线,从代码提交到报告发布。

**具体需求:**
1. 代码提交触发构建
2. 安装依赖和设置环境
3. 执行单元测试和集成测试
4. 生成测试报告
5. 发送通知邮件

**使用示例:**
```groovy
pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    parameters {
        choice(name: 'ENV', choices: ['dev', 'test', 'staging'], description: '测试环境')
        booleanParam(name: 'SEND_REPORT', defaultValue: true, description: '发送测试报告')
    }

    environment {
        PROJECT_NAME = 'api_test'
        REPORT_DIR = 'report'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '========== 拉取代码 =========='
                checkout scm
                sh 'git log -1'
            }
        }

        stage('Setup') {
            steps {
                echo '========== 安装依赖 =========='
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo '========== 代码检查 =========='
                sh '''
                    . venv/bin/activate
                    flake8 api/ tests/
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo '========== 单元测试 =========='
                sh '''
                    . venv/bin/activate
                    pytest tests/unit/ -v \
                        --junitxml=${REPORT_DIR}/junit-unit.xml \
                        --cov=api --cov-report=xml:${REPORT_DIR}/coverage.xml
                '''
            }
        }

        stage('Integration Tests') {
            steps {
                echo '========== 集成测试 =========='
                sh """
                    . venv/bin/activate
                    pytest tests/integration/ -v \\
                        --env=\${params.ENV} \\
                        --junitxml=\${REPORT_DIR}/junit-integration.xml \\
                        --alluredir=\${REPORT_DIR}/allure-results
                """
            }
        }

        stage('Report') {
            steps {
                echo '========== 发布报告 =========='
                junit "${REPORT_DIR}/junit-*.xml"
                allure includeProperties: false, results: [[path: "${REPORT_DIR}/allure-results"]]
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            script {
                if (params.SEND_REPORT) {
                    emailext(
                        subject: "【成功】${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """
                            <h2>构建成功</h2>
                            <p>项目: ${env.JOB_NAME}</p>
                            <p>构建号: ${env.BUILD_NUMBER}</p>
                            <p>环境: ${params.ENV}</p>
                            <p><a href="${env.BUILD_URL}allure/">查看Allure报告</a></p>
                        """,
                        to: 'team@example.com',
                        mimeType: 'text/html'
                    )
                }
            }
        }
        failure {
            emailext(
                subject: "【失败】${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>构建失败</h2>
                    <p>请检查: <a href="${env.BUILD_URL}console">构建日志</a></p>
                """,
                to: 'team@example.com',
                mimeType: 'text/html'
            )
        }
    }
}
```

**验收标准:**
- [ ] Pipeline包含完整的CI/CD流程
- [ ] 代码提交自动触发构建
- [ ] 所有测试正确执行
- [ ] 测试报告正确生成
- [ ] 通知邮件正确发送

---

#### 练习18:多环境部署流水线

**场景说明:**
设计一套支持开发、测试、生产三套环境的部署流水线,包含审批流程。

**具体需求:**
1. 支持选择部署环境
2. 不同环境使用不同配置
3. 生产环境需要人工审批
4. 部署后执行冒烟测试
5. 失败时自动回滚

**使用示例:**
```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'test', 'prod'], description: '部署环境')
        booleanParam(name: 'SKIP_SMOKE', defaultValue: false, description: '跳过冒烟测试')
    }

    environment {
        CONFIG_FILE = "config/${params.DEPLOY_ENV}.yaml"
    }

    stages {
        stage('Load Config') {
            steps {
                script {
                    def config = readYaml file: env.CONFIG_FILE
                    env.SERVER_HOST = config.server.host
                    env.SERVER_PORT = config.server.port
                }
            }
        }

        stage('Build') {
            steps {
                sh 'python setup.py build'
            }
        }

        stage('Test') {
            steps {
                sh "pytest tests/ -v --env=${params.DEPLOY_ENV}"
            }
        }

        stage('Approval') {
            when {
                expression { params.DEPLOY_ENV == 'prod' }
            }
            steps {
                input message: '确认部署到生产环境?',
                      ok: '确认',
                      submitter: 'admin,release-team'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def currentVersion = sh(script: 'cat version.txt', returnStdout: true).trim()
                    env.BACKUP_VERSION = currentVersion
                }
                sh """
                    echo "部署到 ${params.DEPLOY_ENV} 环境"
                    echo "服务器: ${env.SERVER_HOST}:${env.SERVER_PORT}"
                    python deploy.py --env=${params.DEPLOY_ENV}
                """
            }
        }

        stage('Smoke Test') {
            when {
                expression { params.SKIP_SMOKE == false }
            }
            steps {
                sh "pytest tests/smoke/ -v --env=${params.DEPLOY_ENV}"
            }
        }
    }

    post {
        failure {
            script {
                if (env.BACKUP_VERSION) {
                    echo "回滚到版本: ${env.BACKUP_VERSION}"
                    sh "python rollback.py --version=${env.BACKUP_VERSION}"
                }
            }
        }
    }
}
```

**验收标准:**
- [ ] 支持三套环境部署
- [ ] 环境配置正确加载
- [ ] 生产环境需要审批
- [ ] 冒烟测试正确执行
- [ ] 失败时自动回滚

---

#### 练习19:性能测试集成

**场景说明:**
将性能测试集成到CI/CD流程中,每次构建都执行基准性能测试。

**具体需求:**
1. 集成Locust性能测试
2. 配置性能基准线
3. 性能结果与基准对比
4. 性能下降超过阈值时标记失败
5. 生成性能趋势报告

**使用示例:**
```groovy
pipeline {
    agent any

    environment {
        PERFORMANCE_THRESHOLD = 100  // 平均响应时间阈值(ms)
        THROUGHPUT_THRESHOLD = 50    // 吞吐量阈值(RPS)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt locust'
            }
        }

        stage('Functional Tests') {
            steps {
                sh 'pytest tests/ -v'
            }
        }

        stage('Performance Tests') {
            steps {
                sh '''
                    locust -f performance/locustfile.py \
                        --headless \
                        --users 100 \
                        --spawn-rate 10 \
                        --run-time 5m \
                        --host http://test-server:8080 \
                        --html report/performance.html \
                        --csv report/performance
                '''
            }
        }

        stage('Performance Analysis') {
            steps {
                script {
                    def stats = readCSV file: 'report/performance_stats.csv'
                    def avgResponseTime = stats[1]['Average Response Time'].toInteger()
                    def throughput = stats[1]['Requests/s'].toDouble()

                    echo "平均响应时间: ${avgResponseTime}ms"
                    echo "吞吐量: ${throughput} RPS"

                    if (avgResponseTime > env.PERFORMANCE_THRESHOLD.toInteger()) {
                        error "性能测试失败: 平均响应时间 ${avgResponseTime}ms 超过阈值 ${env.PERFORMANCE_THRESHOLD}ms"
                    }

                    if (throughput < env.THROUGHPUT_THRESHOLD.toDouble()) {
                        error "性能测试失败: 吞吐量 ${throughput} RPS 低于阈值 ${env.THROUGHPUT_THRESHOLD} RPS"
                    }
                }
            }
        }

        stage('Publish Performance Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'report',
                    reportFiles: 'performance.html',
                    reportName: 'Performance Report'
                ])
            }
        }
    }
}
```

**验收标准:**
- [ ] Locust性能测试正确执行
- [ ] 性能指标正确收集
- [ ] 与基准阈值正确对比
- [ ] 超过阈值时构建失败
- [ ] 性能报告正确生成

---

#### 练习20:完整DevOps流水线

**场景说明:**
设计一套完整的DevOps流水线,包含代码扫描、测试、构建镜像、部署的全流程。

**具体需求:**
1. 代码静态扫描(SonarQube)
2. 单元测试和覆盖率
3. 构建Docker镜像
4. 推送镜像到仓库
5. 部署到Kubernetes

**使用示例:**
```groovy
pipeline {
    agent any

    environment {
        REGISTRY = 'registry.example.com'
        IMAGE_NAME = "${REGISTRY}/myapp"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        SONARQUBE_ENV = 'SonarQube'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(env.SONARQUBE_ENV) {
                    sh """
                        sonar-scanner \
                            -Dsonar.projectKey=myapp \
                            -Dsonar.sources=. \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Test') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pytest tests/ -v \
                        --junitxml=report/junit.xml \
                        --cov=app --cov-report=xml:coverage.xml \
                        --alluredir=report/allure-results
                '''
            }
            post {
                always {
                    junit 'report/junit.xml'
                    allure includeProperties: false, results: [[path: 'report/allure-results']]
                }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    docker.withRegistry("https://${REGISTRY}", 'registry-credentials') {
                        def customImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                        customImage.push()
                        customImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy to Dev') {
            steps {
                sh """
                    kubectl set image deployment/myapp \
                        myapp=${IMAGE_NAME}:${IMAGE_TAG} \
                        --namespace=dev
                """
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'pytest tests/smoke/ -v --env=dev'
            }
        }

        stage('Approval for Production') {
            steps {
                input message: '部署到生产环境?',
                      ok: '确认部署',
                      submitter: 'admin,release-team'
            }
        }

        stage('Deploy to Prod') {
            steps {
                sh """
                    kubectl set image deployment/myapp \
                        myapp=${IMAGE_NAME}:${IMAGE_TAG} \
                        --namespace=prod
                """
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            dingtalk(
                robot: 'dingtalk-robot',
                type: 'MARKDOWN',
                title: '部署成功',
                text: [
                    "### 部署成功",
                    "- 项目: ${env.JOB_NAME}",
                    "- 版本: ${IMAGE_TAG}",
                    "- [查看详情](${env.BUILD_URL})"
                ]
            )
        }
        failure {
            dingtalk(
                robot: 'dingtalk-robot',
                type: 'MARKDOWN',
                title: '部署失败',
                text: [
                    "### 部署失败",
                    "- 项目: ${env.JOB_NAME}",
                    "- [查看日志](${env.BUILD_URL}console)"
                ]
            )
        }
    }
}
```

**验收标准:**
- [ ] 代码扫描正确执行
- [ ] 质量门限正常工作
- [ ] 测试正确执行并生成报告
- [ ] Docker镜像成功构建和推送
- [ ] Kubernetes部署成功

---

## 五、本周小结

本周学习了CI/CD的核心概念和Jenkins的完整使用流程。从基础的安装配置到高级的Pipeline编写,从简单的测试集成到完整的DevOps流水线。掌握这些内容后,你应该能够:

1. 搭建和维护Jenkins环境
2. 编写各种类型的Pipeline
3. 集成测试框架和报告工具
4. 配置多环境部署流程
5. 实现完整的CI/CD流水线

继续练习和探索,将CI/CD应用到实际项目中,提升团队的开发和测试效率!
