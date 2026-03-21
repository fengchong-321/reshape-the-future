# 第8周：Git 版本控制

## 本周目标

掌握 Git 版本控制，能进行团队协作和代码管理。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| Git 基础 | 安装、配置、基本命令 | ⭐⭐⭐⭐⭐ |
| 分支管理 | 创建、切换、合并、删除 | ⭐⭐⭐⭐⭐ |
| 远程仓库 | clone、push、pull、fetch | ⭐⭐⭐⭐⭐ |
| 冲突解决 | 合并冲突、变基 | ⭐⭐⭐⭐ |
| 回退操作 | reset、revert、cherry-pick | ⭐⭐⭐⭐ |
| Git Flow | 分支策略、工作流 | ⭐⭐⭐⭐ |
| .gitignore | 忽略规则 | ⭐⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 Git 基础配置

```bash
# ============================================
# 安装与配置
# ============================================
# 安装（Mac）
brew install git

# 配置用户信息
git config --global user.name "你的名字"
git config --global user.email "your@email.com"

# 配置编辑器
git config --global core.editor vim

# 配置别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --all"

# 查看配置
git config --list
git config user.name

# ============================================
# 初始化仓库
# ============================================
# 创建新仓库
mkdir my-project
cd my-project
git init

# 克隆远程仓库
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git  # SSH 方式
git clone https://github.com/user/repo.git my-folder  # 指定目录
```

---

### 2.2 基本操作

```bash
# ============================================
# 文件状态
# ============================================
# 查看状态
git status
git status -s  # 简洁模式

# 文件状态说明
# ?? - 未跟踪
# A  - 已暂存（新文件）
# M  - 已修改
# MM - 暂存后又有修改

# ============================================
# 添加到暂存区
# ============================================
# 添加单个文件
git add filename

# 添加多个文件
git add file1 file2 file3

# 添加所有修改
git add .
git add --all

# 添加某个目录
git add src/

# 交互式添加
git add -p

# ============================================
# 提交
# ============================================
# 提交暂存区
git commit -m "提交说明"

# 添加并提交（已跟踪的文件）
git commit -am "提交说明"

# 修改上次提交
git commit --amend -m "新的提交说明"

# 提交消息规范
"""
<type>(<scope>): <subject>

<body>

<footer>

type 类型：
- feat: 新功能
- fix: 修复 bug
- docs: 文档
- style: 格式（不影响代码运行）
- refactor: 重构
- test: 测试
- chore: 构建过程或辅助工具

示例：
feat(auth): 添加用户登录功能

- 实现 JWT 认证
- 添加登录接口测试
- 更新文档

Closes #123
"""

# ============================================
# 查看历史
# ============================================
# 查看提交历史
git log
git log --oneline  # 单行显示
git log -n 5       # 最近5次
git log --graph    # 图形化显示
git log --all      # 所有分支

# 查看文件修改历史
git log -p filename
git log --oneline filename

# 查看某次提交
git show commit_id
git show HEAD      # 最新提交
git show HEAD~1    # 上一次提交
git show HEAD~2    # 上上次提交

# 查看差异
git diff                    # 工作区 vs 暂存区
git diff --staged          # 暂存区 vs 最新提交
git diff HEAD              # 工作区 vs 最新提交
git diff branch1 branch2   # 分支比较
git diff commit1 commit2   # 提交比较

# ============================================
# 撤销操作
# ============================================
# 撤销工作区修改（未 add）
git checkout -- filename
git restore filename  # Git 2.23+

# 撤销暂存（已 add，未 commit）
git reset HEAD filename
git restore --staged filename  # Git 2.23+

# 撤销提交（已 commit）
# 保留修改
git reset --soft HEAD~1   # 回退到暂存状态
git reset --mixed HEAD~1  # 回退到工作区（默认）

# 丢弃修改
git reset --hard HEAD~1   # 完全丢弃（危险！）

# 撤销某次提交（创建新提交）
git revert commit_id

# ============================================
# 删除文件
# ============================================
# 删除文件并提交
git rm filename

# 删除已修改但未提交的文件
git rm -f filename

# 只删除暂存，保留工作区
git rm --cached filename

# 删除目录
git rm -r directory/
```

---

### 2.3 分支管理

```bash
# ============================================
# 分支操作
# ============================================
# 查看分支
git branch          # 本地分支
git branch -r       # 远程分支
git branch -a       # 所有分支
git branch -v       # 显示最后一次提交

# 创建分支
git branch feature-login    # 基于当前分支创建
git branch feature-login commit_id  # 基于某次提交创建

# 切换分支
git checkout feature-login
git switch feature-login    # Git 2.23+

# 创建并切换
git checkout -b feature-login
git switch -c feature-login

# 删除分支
git branch -d feature-login      # 已合并的分支
git branch -D feature-login      # 强制删除

# 重命名分支
git branch -m old-name new-name
git branch -m new-name  # 重命名当前分支

# ============================================
# 合并分支
# ============================================
# 合并指定分支到当前分支
git checkout main
git merge feature-login

# 快进合并（默认）
# A - B - C (main)
#            \
#             D - E (feature)
# 合并后：A - B - C - D - E (main)

# 普通合并（保留分支历史）
git merge --no-ff feature-login
# A - B - C ------ M (main)
#            \    /
#             D - E (feature)

# 压缩合并（squash）
git merge --squash feature-login
git commit -m "合并 feature-login"

# ============================================
# 冲突解决
# ============================================
# 发生冲突时
"""
<<<<<<< HEAD
当前分支内容
=======
合并分支内容
>>>>>>> feature-login
"""

# 解决步骤
# 1. 手动编辑冲突文件，选择保留的内容
# 2. 删除冲突标记
# 3. git add 冲突文件
# 4. git commit

# 查看冲突文件
git status

# 使用某一方的版本
git checkout --ours filename     # 使用当前分支
git checkout --theirs filename   # 使用合并分支

# 中止合并
git merge --abort

# ============================================
# 变基（Rebase）
# ============================================
# 变基 vs 合并
# Merge：保留分支历史，产生合并提交
# Rebase：线性历史，无合并提交

# 变基操作
git checkout feature-login
git rebase main

# 解决变基冲突
# 1. 手动解决冲突
# 2. git add 冲突文件
# 3. git rebase --continue

# 跳过当前提交
git rebase --skip

# 中止变基
git rebase --abort

# 交互式变基（修改历史）
git rebase -i HEAD~3
# 可以：squash(合并)、reword(修改消息)、drop(删除)等

# 注意：已推送到远程的分支不要 rebase！
```

---

### 2.4 远程仓库

```bash
# ============================================
# 远程仓库管理
# ============================================
# 查看远程仓库
git remote
git remote -v

# 添加远程仓库
git remote add origin https://github.com/user/repo.git
git remote add upstream https://github.com/original/repo.git

# 修改远程仓库
git remote set-url origin https://new-url.git

# 删除远程仓库
git remote remove origin

# ============================================
# 推送
# ============================================
# 推送到远程
git push origin main

# 首次推送（设置上游）
git push -u origin main
git push --set-upstream origin main

# 推送所有分支
git push --all origin

# 推送标签
git push origin tagname
git push --tags

# 强制推送（危险！）
git push -f origin main
git push --force-with-lease origin main  # 更安全

# ============================================
# 拉取
# ============================================
# 拉取并合并
git pull origin main

# 拉取并变基
git pull --rebase origin main

# 仅拉取（不合并）
git fetch origin
git fetch --all

# 查看拉取的更新
git log origin/main

# 合并拉取的更新
git merge origin/main

# ============================================
# 跟踪分支
# ============================================
# 查看跟踪关系
git branch -vv

# 设置跟踪
git branch -u origin/main
git branch --set-upstream-to=origin/main

# ============================================
# 删除远程分支
# ============================================
git push origin --delete feature-login
```

---

### 2.5 标签管理

```bash
# ============================================
# 创建标签
# ============================================
# 轻量标签
git tag v1.0.0

# 附注标签（推荐）
git tag -a v1.0.0 -m "版本 1.0.0"

# 给某次提交打标签
git tag -a v0.9.0 commit_id -m "版本 0.9.0"

# ============================================
# 查看标签
# ============================================
git tag
git tag -l "v1.*"
git show v1.0.0

# ============================================
# 推送标签
# ============================================
git push origin v1.0.0
git push origin --tags

# ============================================
# 删除标签
# ============================================
git tag -d v1.0.0
git push origin --delete v1.0.0

# ============================================
# 检出标签
# ============================================
git checkout v1.0.0
git checkout -b version1 v1.0.0  # 创建分支
```

---

### 2.6 暂存工作

```bash
# ============================================
# git stash
# ============================================
# 暂存当前修改
git stash
git stash save "描述信息"

# 查看 stash 列表
git stash list

# 查看 stash 内容
git stash show
git stash show -p

# 恢复 stash
git stash apply          # 恢复最近的
git stash apply stash@{2}  # 恢复指定的

# 恢复并删除
git stash pop

# 删除 stash
git stash drop stash@{0}
git stash clear  # 清空所有

# 从 stash 创建分支
git stash branch feature-stash
```

---

### 2.7 Git Flow 工作流

```bash
# ============================================
# 分支策略
# ============================================
"""
主要分支：
- main/master: 生产环境代码
- develop: 开发分支

辅助分支：
- feature/*: 功能分支
- release/*: 发布分支
- hotfix/*: 紧急修复分支

工作流程：
1. 从 develop 创建 feature 分支
2. 完成功能后合并回 develop
3. 从 develop 创建 release 分支
4. 测试完成后合并到 main 和 develop
5. main 打 tag
6. 紧急修复从 main 创建 hotfix
"""

# 功能开发
git checkout develop
git checkout -b feature/login

# 开发完成
git checkout develop
git merge --no-ff feature/login
git branch -d feature/login

# 准备发布
git checkout -b release/1.0.0 develop
# 修复 bug、更新版本号

# 发布
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"

git checkout develop
git merge --no-ff release/1.0.0

git branch -d release/1.0.0

# 紧急修复
git checkout -b hotfix/bug-123 main
# 修复 bug
git checkout main
git merge --no-ff hotfix/bug-123
git tag -a v1.0.1 -m "Hotfix 1.0.1"

git checkout develop
git merge --no-ff hotfix/bug-123

git branch -d hotfix/bug-123
```

---

### 2.8 .gitignore

```bash
# ============================================
# .gitignore 规则
# ============================================
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# 测试
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# 构建输出
dist/
build/
*.egg-info/

# 日志
*.log
logs/

# 配置文件（含敏感信息）
.env
*.local
config.local.*

# 系统文件
.DS_Store
Thumbs.db

# ============================================
# 语法
# ============================================
# 注释
# 这是注释

# 忽略所有 .log 文件
*.log

# 但保留 important.log
!important.log

# 忽略目录
build/

# 忽略目录下所有文件
build/**

# 只忽略当前目录的 TODO
/TODO

# 忽略 doc 目录下的 .txt 文件
doc/**/*.txt
```

---

### 2.9 Git 常见问题

```bash
# ============================================
# 撤销操作
# ============================================
# 撤销最近一次 commit（保留修改）
git reset --soft HEAD~1

# 撤销最近一次 commit（丢弃修改）
git reset --hard HEAD~1

# 修改最近一次 commit 消息
git commit --amend -m "新消息"

# 撤销某次 commit（创建新 commit）
git revert <commit-id>

# ============================================
# 恢复误删
# ============================================
# 查看操作历史
git reflog

# 恢复到某个状态
git reset --hard <reflog-id>

# ============================================
# 清理
# ============================================
# 删除未跟踪的文件
git clean -n  # 预览
git clean -f  # 删除文件
git clean -fd # 删除文件和目录

# ============================================
# Cherry-pick
# ============================================
# 选择某次提交应用到当前分支
git cherry-pick <commit-id>
git cherry-pick <commit1>..<commit2>
```

---

## 三、Python 调用 Git

```python
# 安装：pip install GitPython

from git import Repo
from pathlib import Path

# ============================================
# 基本操作
# ============================================
# 克隆仓库
repo = Repo.clone_from(
    'https://github.com/user/repo.git',
    '/path/to/local'
)

# 打开本地仓库
repo = Repo('/path/to/repo')

# 查看状态
print(repo.is_dirty())  # 是否有修改
print(repo.untracked_files)  # 未跟踪文件

# 添加文件
repo.index.add(['file1.txt', 'file2.txt'])

# 提交
repo.index.commit('提交说明')

# ============================================
# 分支操作
# ============================================
# 查看分支
print(repo.heads)  # 本地分支
print(repo.references)  # 所有引用

# 当前分支
print(repo.active_branch)

# 创建分支
new_branch = repo.create_head('feature-new')

# 切换分支
new_branch.checkout()
# 或
repo.heads.feature_new.checkout()

# 删除分支
repo.delete_head('feature-old')

# ============================================
# 远程操作
# ============================================
# 查看远程
print(repo.remotes)
print(repo.remotes.origin.url)

# 拉取
repo.remotes.origin.pull()

# 推送
repo.remotes.origin.push()

# ============================================
# 日志
# ============================================
# 提交历史
for commit in repo.iter_commits('main'):
    print(commit.hexsha)
    print(commit.message)
    print(commit.author)
    print(commit.committed_date)

# ============================================
# 测试场景
# ============================================
def test_git_operations():
    """测试 Git 操作"""
    repo = Repo('/path/to/test/repo')
    
    # 测试仓库状态
    assert not repo.is_dirty() or repo.untracked_files == []
    
    # 测试分支存在
    assert 'main' in [h.name for h in repo.heads]
    
    # 测试最新提交
    latest = repo.heads.main.commit
    assert latest.message.startswith('feat') or latest.message.startswith('fix')
```

---

## 四、练习内容

### 基础练习（1-8）

#### 练习1：Git 初始化与配置

```bash
# 任务要求：
# 1. 在本地创建一个名为 "git-practice" 的文件夹
# 2. 将其初始化为 Git 仓库
# 3. 配置用户名和邮箱
# 4. 配置常用别名（st、co、br、ci、lg）

# 预期输出：
# 能够使用 git status 查看仓库状态
# 能够使用 git lg 查看提交历史
```

#### 练习2：基本文件操作

```bash
# 任务要求：
# 1. 创建 README.md 文件，写入项目介绍
# 2. 创建 src 目录，在其中创建 main.py 文件
# 3. 将文件添加到暂存区
# 4. 提交更改，提交信息符合规范格式

# 预期输出：
# 使用 git log 能看到提交记录
# 使用 git status 确认工作区干净
```

#### 练习3：.gitignore 配置

```bash
# 任务要求：
# 创建 .gitignore 文件，配置以下忽略规则：
# 1. 忽略所有 .pyc 文件
# 2. 忽略 __pycache__ 目录
# 3. 忽略 .env 文件
# 4. 忽略 .idea 和 .vscode 目录
# 5. 但保留 important.pyc 文件

# 预期输出：
# 创建测试文件验证忽略规则生效
```

#### 练习4：分支基础操作

```bash
# 任务要求：
# 1. 基于 main 分支创建 feature-readme 分支
# 2. 在新分支中修改 README.md 文件
# 3. 提交更改
# 4. 切换回 main 分支
# 5. 将 feature-readme 分支合并到 main

# 预期输出：
# main 分支包含 feature-readme 的修改
# 使用 git branch -d 删除已合并的分支
```

#### 练习5：查看历史与差异

```bash
# 任务要求：
# 1. 修改 main.py 文件，添加一个函数
# 2. 使用 git diff 查看修改内容
# 3. 提交更改
# 4. 使用 git log 查看历史
# 5. 使用 git show 查看某次提交的详细内容

# 预期输出：
# 能理解 diff 输出的含义
# 能追踪文件修改历史
```

#### 练习6：撤销操作

```bash
# 任务要求：
# 1. 修改 main.py 文件但不提交
# 2. 使用 git restore 撤销工作区修改
# 3. 再次修改并 add 到暂存区
# 4. 使用 git restore --staged 撤销暂存
# 5. 提交后使用 git commit --amend 修改提交信息

# 预期输出：
# 理解工作区、暂存区、提交区的关系
# 掌握各种撤销操作
```

#### 练习7：标签管理

```bash
# 任务要求：
# 1. 为当前提交打轻量标签 v0.1.0
# 2. 为当前提交打附注标签 v0.2.0，添加说明信息
# 3. 查看所有标签
# 4. 查看 v0.2.0 标签的详细信息
# 5. 删除 v0.1.0 标签

# 预期输出：
# 使用 git tag 列出标签
# 使用 git show v0.2.0 查看标签信息
```

#### 练习8：Git Stash 使用

```bash
# 任务要求：
# 1. 修改 main.py 文件但不提交
# 2. 需要紧急切换分支处理其他任务
# 3. 使用 git stash 暂存修改
# 4. 切换分支完成其他任务
# 5. 回到原分支，使用 git stash pop 恢复修改

# 预期输出：
# 理解 stash 的使用场景
# 掌握 stash 的基本操作
```

### 进阶练习（9-16）

#### 练习9：合并冲突解决

```bash
# 任务要求：
# 1. 创建分支 feature-a，修改 README.md 的第一行
# 2. 提交后切换回 main，同样修改 README.md 的第一行（不同内容）
# 3. 尝试合并 feature-a，解决冲突
# 4. 手动编辑冲突文件，保留两边的修改
# 5. 完成合并

# 预期输出：
# 理解冲突标记 <<<<<<< ======= >>>>>>> 的含义
# 能够手动解决合并冲突
```

#### 练习10：Rebase 操作

```bash
# 任务要求：
# 1. 创建分支 feature-b，添加 3 次提交
# 2. main 分支也有新的提交
# 3. 使用 rebase 将 feature-b 的提交变基到最新的 main
# 4. 查看提交历史，确认线性历史

# 预期输出：
# 理解 merge 和 rebase 的区别
# 掌握 rebase 的基本操作
```

#### 练习11：交互式 Rebase

```bash
# 任务要求：
# 1. 在分支上创建 3 次提交
# 2. 使用 git rebase -i HEAD~3 进入交互模式
# 3. 将第二次提交的 pick 改为 squash，合并到第一次提交
# 4. 将第三次提交的 pick 改为 reword，修改提交信息

# 预期输出：
# 理解交互式 rebase 的各种操作
# 能够压缩和修改历史提交
```

#### 练习12：Cherry-pick 选择性合并

```bash
# 任务要求：
# 1. 在 feature-c 分支上创建 3 次提交（A、B、C）
# 2. 切换到 main 分支
# 3. 只使用 cherry-pick 将提交 B 应用到 main
# 4. 验证 main 只有 B 的修改

# 预期输出：
# 理解 cherry-pick 的使用场景
# 能够选择性合并特定提交
```

#### 练习13：Git Reset 三种模式

```bash
# 任务要求：
# 1. 创建 3 次提交（提交1、提交2、提交3）
# 2. 使用 git reset --soft HEAD~1 回退一次，观察状态
# 3. 再次提交，恢复到 3 次提交
# 4. 使用 git reset --mixed HEAD~1 回退一次，观察状态
# 5. 使用 git reset --hard HEAD~1 回退一次，观察状态

# 预期输出：
# 理解 soft、mixed、hard 三种模式的区别
# 知道何时使用哪种模式
```

#### 练习14：Git Reflog 恢复

```bash
# 任务要求：
# 1. 创建几次提交
# 2. 使用 git reset --hard 回退到之前的状态
# 3. 使用 git reflog 查看操作历史
# 4. 使用 reflog 找回被丢弃的提交
# 5. 恢复到之前的状态

# 预期输出：
# 理解 reflog 是 Git 的"后悔药"
# 能够恢复误操作丢失的提交
```

#### 练习15：Git Flow 工作流实践

```bash
# 任务要求：
# 1. 初始化 Git Flow 结构（main、develop 分支）
# 2. 从 develop 创建 feature/user-auth 分支
# 3. 完成功能开发后合并回 develop
# 4. 从 develop 创建 release/1.0.0 分支
# 5. 发布到 main 并打标签

# 预期输出：
# 理解 Git Flow 的分支策略
# 能够按照工作流进行团队协作
```

#### 练习16：远程仓库协作

```bash
# 任务要求：
# 1. 在 GitHub/GitLab 上创建远程仓库
# 2. 添加远程仓库地址
# 3. 推送本地分支到远程
# 4. 模拟另一开发者：克隆仓库，做修改并推送
# 5. 原仓库拉取更新，解决可能的冲突

# 预期输出：
# 掌握 clone、push、pull、fetch 操作
# 理解本地分支与远程分支的跟踪关系
```

### 综合练习（17-20）

#### 练习17：完整项目版本控制

```bash
# 任务要求：
# 模拟一个完整的项目开发流程：
# 1. 初始化项目，创建 .gitignore
# 2. 创建 develop 分支
# 3. 开发功能 A（feature/feature-a）
# 4. 开发功能 B（feature/feature-b）
# 5. 合并到 develop，测试
# 6. 创建 release 分支，修复 bug
# 7. 发布到 main，打版本标签

# 预期输出：
# 完整的项目提交历史
# 规范的分支结构
```

#### 练习18：代码回滚与恢复

```bash
# 场景描述：
# 项目发布了 v1.0.0，发现了一个严重 bug

# 任务要求：
# 1. 检出 v1.0.0 标签
# 2. 创建 hotfix/v1.0.1 分支
# 3. 修复 bug 并提交
# 4. 使用 git revert 撤销某次有问题的提交
# 5. 合并到 main 和 develop，打 v1.0.1 标签

# 预期输出：
# 理解 reset 和 revert 的区别
# 掌握紧急修复的工作流程
```

#### 练习19：Git 钩子配置

```bash
# 任务要求：
# 1. 进入 .git/hooks 目录
# 2. 创建 pre-commit 钩子：
#    - 检查代码中是否有 console.log
#    - 检查是否有 TODO 标记
# 3. 创建 commit-msg 钩子：
#    - 验证提交信息格式（feat|fix|docs: 开头）
# 4. 测试钩子是否生效

# 预期输出：
# 提交时自动执行检查
# 不符合规范的提交被拒绝
```

#### 练习20：团队协作冲突处理

```bash
# 场景描述：
# 两个开发者同时修改同一文件

# 任务要求：
# 1. 创建两个本地仓库模拟两个开发者
# 2. 开发者 A 修改文件并推送
# 3. 开发者 B 修改同一文件的同一位置
# 4. 开发者 B 尝试推送，发现冲突
# 5. 开发者 B 拉取、解决冲突、重新推送

# 预期输出：
# 理解团队协作中的常见问题
# 掌握冲突解决的最佳实践
```

---

## 五、学到什么程度

### 必须掌握

- [ ] Git 基本操作（add、commit、push、pull）
- [ ] 分支管理（创建、切换、合并）
- [ ] 冲突解决
- [ ] .gitignore 配置

### 应该了解

- [ ] Git Flow 工作流
- [ ] rebase vs merge
- [ ] Git 钩子

---

## 六、本周小结

1. **Git 基础**：版本控制必备技能
2. **分支策略**：团队协作的基础
3. **冲突解决**：合并代码的关键

### 下周预告

第9周学习 Linux 基础。
