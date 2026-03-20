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

## 四、学到什么程度

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

## 五、本周小结

1. **Git 基础**：版本控制必备技能
2. **分支策略**：团队协作的基础
3. **冲突解决**：合并代码的关键

### 下周预告

第9周学习 Linux 基础。
