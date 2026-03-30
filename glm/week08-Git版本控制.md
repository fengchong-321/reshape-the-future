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

---

#### 练习1：Git 初始化与配置

**场景说明**：作为新项目成员，你需要初始化 Git 仓库并进行基本配置。

**具体需求**：
1. 在本地创建一个名为 `git-practice` 的文件夹
2. 将其初始化为 Git 仓库
3. 配置用户名和邮箱（用于提交记录）
4. 配置常用别名：`st`（status）、`co`（checkout）、`br`（branch）、`ci`（commit）、`lg`（log --oneline --graph --all）
5. 验证配置是否生效

**使用示例**：
```bash
# 1. 创建项目文件夹
mkdir git-practice
cd git-practice

# 2. 初始化 Git 仓库
git init
# 输出: Initialized empty Git repository in /path/git-practice/.git/

# 3. 配置用户信息
git config user.name "张三"
git config user.email "zhangsan@example.com"

# 4. 配置常用别名
git config alias.st status
git config alias.co checkout
git config alias.br branch
git config alias.ci commit
git config alias.lg "log --oneline --graph --all"

# 5. 验证配置
git config --list
git config user.name
# 输出: 张三

# 6. 验证别名生效
git st
# 输出: On branch master
#       No commits yet
#       nothing to commit (create/copy files and use "git add" to track)
```

**验收标准**：
- [ ] Git 仓库初始化成功（存在 .git 目录）
- [ ] 用户名和邮箱配置正确
- [ ] 所有别名配置成功，可以使用简写命令
- [ ] `git st` 能正常显示仓库状态

---

---

#### 练习2：基本文件操作

**场景说明**：学习 Git 的基本文件操作流程：创建文件、添加到暂存区、提交更改。

**具体需求**：
1. 创建 `README.md` 文件，写入项目介绍内容
2. 创建 `src` 目录，在其中创建 `main.py` 文件
3. 使用 `git add` 将文件添加到暂存区
4. 使用 `git status` 查看状态
5. 使用 `git commit` 提交更改，提交信息符合规范格式（feat/fix/docs）

**使用示例**：
```bash
# 1. 创建项目文件
echo "# Git Practice Project" > README.md
echo "" >> README.md
echo "这是一个 Git 练习项目。" >> README.md

# 2. 创建源代码目录和文件
mkdir src
cat > src/main.py << 'EOF'
def main():
    print("Hello, Git!")

if __name__ == "__main__":
    main()
EOF

# 3. 查看当前状态
git status
# 输出: Untracked files: README.md, src/

# 4. 添加所有文件到暂存区
git add README.md src/

# 5. 再次查看状态
git status
# 输出: Changes to be committed:
#         new file:   README.md
#         new file:   src/main.py

# 6. 提交更改（符合规范格式）
git commit -m "feat: 初始化项目，添加 README 和主程序文件"

# 7. 验证提交
git log --oneline
# 输出: abc123 feat: 初始化项目，添加 README 和主程序文件

# 8. 确认工作区干净
git status
# 输出: nothing to commit, working tree clean
```

**验收标准**：
- [ ] 文件创建成功
- [ ] `git add` 正确添加文件到暂存区
- [ ] 提交信息符合规范格式（feat/fix/docs: 开头）
- [ ] `git log` 能看到提交记录
- [ ] 工作区状态干净

---

#### 练习3：.gitignore 配置

**场景说明**：配置 .gitignore 文件，避免将不必要的文件提交到版本控制。

**具体需求**：
1. 创建 .gitignore 文件
2. 配置忽略规则：
   - 忽略所有 `.pyc` 文件
   - 忽略 `__pycache__` 目录
   - 忽略 `.env` 文件
   - 忽略 `.idea` 和 `.vscode` 目录
   - 但保留 `important.pyc` 文件
3. 创建测试文件验证忽略规则生效

**使用示例**：
```bash
# 1. 创建 .gitignore 文件
cat > .gitignore << 'EOF'
# Python
*.pyc
__pycache__/
*.py[cod]

# 但保留 important.pyc
!important.pyc

# 环境配置
.env
*.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# 测试和构建
.pytest_cache/
.coverage
htmlcov/
dist/
build/
EOF

# 2. 创建测试文件验证忽略规则
mkdir -p __pycache__
touch test.pyc
touch important.pyc
touch .env
mkdir -p .idea

# 3. 查看状态，验证哪些文件被忽略
git status
# 应该只看到 important.pyc，其他文件被忽略

# 4. 验证 .gitignore 语法
git check-ignore -v test.pyc
# 输出: .gitignore:2:*.pyc    test.pyc

# 5. 验证 important.pyc 没有被忽略
git check-ignore -v important.pyc
# 应该没有输出（表示没有被忽略）
```

**验收标准**：
- [ ] .gitignore 文件创建成功
- [ ] `.pyc` 文件被正确忽略
- [ ] `important.pyc` 没有被忽略（例外规则生效）
- [ ] `.env` 文件被忽略
- [ ] IDE 配置目录被忽略

---

---

#### 练习4：分支基础操作

**场景说明**：学习 Git 分支的创建、切换、合并和删除操作。

**具体需求**：
1. 基于 main 分支创建 `feature-readme` 分支
2. 在新分支中修改 README.md 文件
3. 提交更改
4. 切换回 main 分支
5. 将 `feature-readme` 分支合并到 main
6. 删除已合并的分支

**使用示例**：
```bash
# 1. 查看当前分支
git branch
# 输出: * master（或 main）

# 2. 创建并切换到新分支
git checkout -b feature-readme
# 或使用新命令
git switch -c feature-readme

# 3. 验证分支切换成功
git branch
# 输出: * feature-readme
#       master

# 4. 修改 README.md
echo "" >> README.md
echo "## 功能特性" >> README.md
echo "- 基础功能实现" >> README.md

# 5. 提交更改
git add README.md
git commit -m "docs: 添加功能特性说明"

# 6. 切换回主分支
git checkout master
# 或
git switch master

# 7. 合并 feature-readme 分支
git merge feature-readme
# 输出: Updating abc123..def456
#       Fast-forward
#        README.md | 3 ++
#        1 file changed, 3 insertions(+)

# 8. 验证合并结果
cat README.md
# 应该包含新添加的内容

# 9. 删除已合并的分支
git branch -d feature-readme
# 输出: Deleted branch feature-readme (was def456).

# 10. 验证分支已删除
git branch
# feature-readme 不应该在列表中
```

**验收标准**：
- [ ] 能正确创建新分支
- [ ] 能正确切换分支
- [ ] 不同分支的修改互不影响
- [ ] 合并操作成功
- [ ] 能删除已合并的分支

---

---

#### 练习5：查看历史与差异

**场景说明**：学习如何查看 Git 提交历史和文件差异，这是代码审查和问题排查的基础技能。

**具体需求**：
1. 修改 main.py 文件，添加一个新函数
2. 使用 `git diff` 查看修改内容
3. 提交更改
4. 使用 `git log` 查看提交历史
5. 使用 `git show` 查看某次提交的详细内容

**使用示例**：
```bash
# 1. 修改 main.py 文件
cat > src/main.py << 'EOF'
def hello():
    print("Hello, World!")

def greet(name):
    """向指定用户问好"""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    hello()
    greet("Git Learner")
EOF

# 2. 查看修改内容（未暂存的修改）
git diff
# 输出示例：
# diff --git a/src/main.py b/src/main.py
# index abc1234..def5678 100644
# --- a/src/main.py
# +++ b/src/main.py
# @@ -1,3 +1,9 @@
# +def greet(name):
# +    """向指定用户问好"""
# +    print(f"Hello, {name}!")
# ...

# 3. 添加到暂存区
git add src/main.py

# 4. 查看暂存的修改
git diff --staged
# 或
git diff --cached

# 5. 提交更改
git commit -m "feat: 添加 greet 函数，向指定用户问好"

# 6. 查看提交历史
git log
# 输出:
# commit def5678...
# Author: Your Name <your@email.com>
# Date:   Mon Jan 1 10:00:00 2024 +0800
#     feat: 添加 greet 函数，向指定用户问好
# ...

# 7. 查看简洁的历史记录
git log --oneline
# 输出:
# def5678 feat: 添加 greet 函数，向指定用户问好
# abc1234 feat: 添加 hello 函数
# ...

# 8. 查看某次提交的详细内容
git show HEAD
# 显示最新提交的完整 diff

# 9. 查看特定提交
git show def5678

# 10. 查看文件修改历史
git log -p src/main.py
# 显示该文件的所有提交历史和修改内容

# 11. 比较两个提交
git diff HEAD~2 HEAD
# 比较当前提交和上上次提交的差异

# 12. 查看谁修改了文件的每一行
git blame src/main.py
# 输出:
# abc1234 (Your Name 2024-01-01 10:00:00 +0800 1) def hello():
# abc1234 (Your Name 2024-01-01 10:00:00 +0800 2)     print("Hello, World!")
# def5678 (Your Name 2024-01-01 11:00:00 +0800 3)
# ...
```

**验收标准**：
- [ ] 能理解 `git diff` 输出的格式和含义
- [ ] 能使用 `git log` 查看历史记录
- [ ] 能使用 `git show` 查看提交详情
- [ ] 能使用 `git blame` 追踪代码来源

---

---

#### 练习6：撤销操作

**场景说明**：学习 Git 的撤销操作，理解工作区、暂存区和提交区的关系。

**具体需求**：
1. 修改 main.py 文件但不提交
2. 使用 `git restore` 撤销工作区修改
3. 再次修改并 `add` 到暂存区
4. 使用 `git restore --staged` 撤销暂存
5. 提交后使用 `git commit --amend` 修改提交信息

**使用示例**：
```bash
# 场景1：撤销工作区修改（未 add）

# 1. 修改文件
echo "# 错误的修改" >> src/main.py

# 2. 查看状态
git status
# 输出: modified: src/main.py

# 3. 撤销修改（恢复到暂存区或最新提交的状态）
git restore src/main.py
# 或使用旧命令
git checkout -- src/main.py

# 4. 验证撤销成功
git status
# 输出: nothing to commit, working tree clean


# 场景2：撤销暂存（已 add，未 commit）

# 1. 修改并添加到暂存区
echo "# 新功能" >> src/main.py
git add src/main.py

# 2. 查看状态
git status
# 输出: Changes to be committed:
#         modified:   src/main.py

# 3. 撤销暂存（保留工作区修改）
git restore --staged src/main.py
# 或使用旧命令
git reset HEAD src/main.py

# 4. 验证暂存已撤销
git status
# 输出: Changes not staged for commit:
#         modified:   src/main.py


# 场景3：修改提交信息（已 commit）

# 1. 提交代码
git add src/main.py
git commit -m "feat: 添加新功能"

# 2. 发现提交信息有误，修改
git commit --amend -m "feat: 添加新功能（修正后的信息）"

# 3. 验证修改
git log -1
# 应该显示修正后的提交信息


# 场景4：撤销最近一次提交（保留修改）

# 1. 撤销提交，保留修改在暂存区
git reset --soft HEAD~1

# 2. 撤销提交，保留修改在工作区
git reset --mixed HEAD~1
# 或简写
git reset HEAD~1

# 3. 撤销提交，丢弃所有修改（危险！）
git reset --hard HEAD~1


# 场景5：撤销某次提交（创建新提交）

# 使用 revert 会创建一个新的提交来撤销指定提交
git revert <commit-id>
```

**验收标准**：
- [ ] 能区分工作区、暂存区、提交区
- [ ] 能正确使用 `git restore` 撤销工作区修改
- [ ] 能正确使用 `git restore --staged` 撤销暂存
- [ ] 能使用 `git commit --amend` 修改提交信息
- [ ] 理解 `reset` 和 `revert` 的区别

---

---

#### 练习7：标签管理

**场景说明**：使用标签标记重要的版本节点，便于版本发布和回溯。

**具体需求**：
1. 为当前提交打轻量标签 `v0.1.0`
2. 为当前提交打附注标签 `v0.2.0`，添加说明信息
3. 查看所有标签
4. 查看 `v0.2.0` 标签的详细信息
5. 删除 `v0.1.0` 标签

**使用示例**：
```bash
# 1. 创建轻量标签
git tag v0.1.0

# 2. 创建附注标签（推荐，包含更多信息）
git tag -a v0.2.0 -m "版本 0.2.0 - 添加基础功能"

# 3. 为历史提交打标签
# 先查看提交历史
git log --oneline
# 找到目标提交ID，例如 abc1234
git tag -a v0.0.1 abc1234 -m "初始版本"

# 4. 查看所有标签
git tag
# 输出:
# v0.0.1
# v0.1.0
# v0.2.0

# 5. 按模式筛选标签
git tag -l "v0.1.*"
# 输出: v0.1.0

# 6. 查看标签详细信息
git show v0.2.0
# 输出:
# tag v0.2.0
# Tagger: Your Name <your@email.com>
# Date:   Mon Jan 1 10:00:00 2024 +0800
#
# 版本 0.2.0 - 添加基础功能
# ...

# 7. 推送标签到远程
git push origin v0.2.0

# 推送所有标签
git push origin --tags

# 8. 删除本地标签
git tag -d v0.1.0
# 输出: Deleted tag 'v0.1.0' (was abc1234)

# 9. 删除远程标签
git push origin --delete v0.1.0

# 10. 检出标签（创建分支）
git checkout -b version-0.2 v0.2.0
```

**验收标准**：
- [ ] 能正确创建轻量标签和附注标签
- [ ] 理解两种标签的区别
- [ ] 能查看标签列表和详细信息
- [ ] 能删除本地和远程标签
- [ ] 能基于标签创建分支

---

---

#### 练习8：Git Stash 使用

**场景说明**：当你正在开发一个功能，突然需要切换到其他分支处理紧急任务，但当前修改还未完成不能提交时，可以使用 stash 暂存。

**具体需求**：
1. 在 main.py 文件中添加未完成的修改
2. 需要紧急切换分支处理其他任务
3. 使用 `git stash` 暂存当前修改
4. 切换分支完成其他任务并提交
5. 回到原分支，使用 `git stash pop` 恢复修改

**使用示例**：
```bash
# 1. 在当前分支进行未完成的修改
echo "# 未完成的功能" >> src/main.py
echo "def new_feature():" >> src/main.py
echo "    pass  # TODO" >> src/main.py

# 2. 查看状态
git status
# 输出: modified: src/main.py

# 3. 尝试切换分支（会失败）
git checkout hotfix-branch
# 输出: error: Your local changes would be overwritten by checkout

# 4. 暂存当前修改
git stash
# 或带描述信息
git stash save "正在开发新功能，临时保存"

# 5. 验证工作区干净
git status
# 输出: nothing to commit, working tree clean

# 6. 查看 stash 列表
git stash list
# 输出: stash@{0}: On master: 正在开发新功能，临时保存

# 7. 现在可以安全切换分支
git checkout hotfix-branch

# 8. 在 hotfix 分支完成紧急任务
echo "hotfix" > hotfix.txt
git add hotfix.txt
git commit -m "fix: 紧急修复"

# 9. 切换回原分支
git checkout master

# 10. 恢复暂存的修改
git stash pop
# 或指定恢复特定的 stash
git stash apply stash@{0}

# 11. 验证修改已恢复
git status
# 输出: modified: src/main.py

# 12. 查看 stash 内容（不恢复）
git stash show
git stash show -p  # 显示详细差异

# 13. 删除 stash
git stash drop stash@{0}
# 清空所有 stash
git stash clear

# 14. 从 stash 创建新分支
git stash branch feature-continue
```

**验收标准**：
- [ ] 能正确使用 stash 暂存修改
- [ ] 暂存后能正常切换分支
- [ ] 能正确恢复暂存的修改
- [ ] 理解 stash 的工作流程
- [ ] 能管理多个 stash

---

### 进阶练习（9-16）

---

#### 练习9：合并冲突解决

**场景说明**：当两个分支修改了同一文件的同一位置时，合并会产生冲突，需要手动解决。

**具体需求**：
1. 创建分支 `feature-a`，修改 README.md 的第一行
2. 提交后切换回 master，同样修改 README.md 的第一行（不同内容）
3. 尝试合并 `feature-a`，观察冲突
4. 手动编辑冲突文件，保留两边的修改
5. 完成合并

**使用示例**：
```bash
# 1. 创建并切换到 feature-a 分支
git checkout -b feature-a

# 2. 修改 README.md 第一行
echo "# 项目名称 - 功能A版本" > README.md.tmp
tail -n +2 README.md >> README.md.tmp
mv README.md.tmp README.md

# 或者直接编辑第一行
sed -i '' '1s/.*/# 项目名称 - 功能A版本/' README.md

# 3. 提交修改
git add README.md
git commit -m "feat: 修改项目标题为功能A版本"

# 4. 切换回 master 分支
git checkout master

# 5. 修改 README.md 第一行（不同内容）
sed -i '' '1s/.*/# 项目名称 - 主版本/' README.md

# 6. 提交修改
git add README.md
git commit -m "feat: 修改项目标题为主版本"

# 7. 尝试合并 feature-a（会产生冲突）
git merge feature-a
# 输出: CONFLICT (content): Merge conflict in README.md
#       Automatic merge failed; fix conflicts and then commit the result.

# 8. 查看冲突文件
cat README.md
# 输出:
# <<<<<<< HEAD
# # 项目名称 - 主版本
# =======
# # 项目名称 - 功能A版本
# >>>>>>> feature-a

# 9. 查看冲突状态
git status
# 输出: Unmerged paths:
#         both modified:   README.md

# 10. 手动解决冲突（编辑文件）
# 选择保留的内容，删除冲突标记
echo "# 项目名称 - 整合版本（包含主版本和功能A）" > README.md

# 11. 添加解决冲突后的文件
git add README.md

# 12. 完成合并
git commit -m "merge: 合并 feature-a，解决标题冲突"

# 13. 验证合并完成
git log --oneline -3

# 其他解决方案：

# 使用某一方的版本
git checkout --ours README.md      # 使用当前分支（master）的版本
git checkout --theirs README.md    # 使用合并分支（feature-a）的版本

# 使用合并工具
git mergetool

# 中止合并
git merge --abort
```

**验收标准**：
- [ ] 能识别冲突发生的原因
- [ ] 理解冲突标记的含义（`<<<<<<<`, `=======`, `>>>>>>>`）
- [ ] 能手动解决冲突
- [ ] 能使用 `--ours` 或 `--theirs` 选择版本
- [ ] 能中止合并操作

---

---

#### 练习10：Rebase 操作

**场景说明**：变基（rebase）可以将分支的提交移动到另一个基础提交之上，保持线性历史。

**具体需求**：
1. 创建分支 `feature-b`，添加 3 次提交
2. main 分支也有新的提交
3. 使用 rebase 将 `feature-b` 的提交变基到最新的 main
4. 查看提交历史，确认线性历史

**使用示例**：
```bash
# 1. 创建 feature-b 分支
git checkout -b feature-b

# 2. 在 feature-b 上创建 3 次提交
echo "Feature B step 1" >> README.md
git add README.md
git commit -m "feat: feature-b 步骤1"

echo "Feature B step 2" >> README.md
git add README.md
git commit -m "feat: feature-b 步骤2"

echo "Feature B step 3" >> README.md
git add README.md
git commit -m "feat: feature-b 步骤3"

# 3. 切换到 main 并添加新提交
git checkout master
echo "Main branch update" >> README.md
git add README.md
git commit -m "feat: main 分支更新"

# 4. 查看当前历史
git log --oneline --graph --all
# 输出:
# * def4567 feat: feature-b 步骤3
# * cde4567 feat: feature-b 步骤2
# * bcd4567 feat: feature-b 步骤1
# | * abc4567 feat: main 分支更新
# |/
# * 1234567 初始提交

# 5. 切换到 feature-b 并变基
git checkout feature-b
git rebase master

# 6. 查看变基后的历史
git log --oneline --graph --all
# 输出:
# * abc1234 feat: feature-b 步骤3
# * def4567 feat: feature-b 步骤2
# * cde4567 feat: feature-b 步骤1
# * abc4567 feat: main 分支更新
# * 1234567 初始提交

# 7. 处理 rebase 冲突
# 如果有冲突，Git 会暂停
# 1. 手动解决冲突
# 2. git add 冲突文件
# 3. git rebase --continue

# 跳过当前提交
git rebase --skip

# 中止变基
git rebase --abort

# 8. 交互式变基（修改历史）
git rebase -i HEAD~3
# 编辑器中显示：
# pick cde4567 feat: feature-b 步骤1
# pick def4567 feat: feature-b 步骤2
# pick abc1234 feat: feature-b 步骤3
# 可以修改为：
# squash cde4567 feat: feature-b 步骤1
# pick def4567 feat: feature-b 步骤2
# reword abc1234 feat: feature-b 步骤3
# 保存并完成编辑
```

**验收标准**：
- [ ] 理解 rebase 与 merge 的区别
- [ ] 能正确执行变基操作
- [ ] 能处理变基过程中的冲突
- [ ] 理解交互式变基的用法
- [ ] 知道不要对已推送的分支执行 rebase

---

#### 练习11：交互式 Rebase

**场景说明**：当你需要整理提交历史，比如合并多个小提交、修改提交信息、删除某些提交时，可以使用交互式变基（interactive rebase）。

**具体需求**：
1. 在分支上创建 3 次提交
2. 使用 `git rebase -i HEAD~3` 进入交互模式
3. 将第二次提交的 `pick` 改为 `squash`，合并到第一次提交
4. 将第三次提交的 `pick` 改为 `reword`，修改提交信息
5. 保存并完成变基

**使用示例**：
```bash
# 1. 创建测试分支和 3 次提交
git checkout -b feature-interactive
echo "功能1" >> README.md && git add . && git commit -m "feat: 添加功能1"
echo "功能2" >> README.md && git add . && git commit -m "feat: 添加功能2"
echo "功能3" >> README.md && git add . && git commit -m "feat: 添加功能3"

# 2. 查看当前提交历史
git log --oneline -3
# 输出:
# abc1234 feat: 添加功能3
# def5678 feat: 添加功能2
# ghi9012 feat: 添加功能1

# 3. 启动交互式变基
git rebase -i HEAD~3

# 编辑器会显示：
# pick ghi9012 feat: 添加功能1
# pick def5678 feat: 添加功能2
# pick abc1234 feat: 添加功能3

# 4. 修改为（将第二个改为 squash，第三个改为 reword）：
# pick ghi9012 feat: 添加功能1
# squash def5678 feat: 添加功能2
# reword abc1234 feat: 添加功能3

# 5. 保存后，编辑合并提交信息
# 将两个提交合并为一个，编写新的提交信息

# 6. 修改第三个提交的信息
# 将 "feat: 添加功能3" 改为更详细的描述

# 7. 查看变基后的历史
git log --oneline -5
# 现在只有 2 个提交（功能1+2合并，功能3单独）

# 常用交互式命令说明：
# pick (p)   = 使用提交
# reword (r) = 使用提交，但修改提交信息
# edit (e)   = 使用提交，但停下来修改
# squash (s) = 使用提交，合并到前一个提交
# drop (d)   = 删除提交
```

**验收标准**：
- [ ] 能正确启动交互式变基
- [ ] 理解 pick、squash、reword、drop 等命令的作用
- [ ] 能将多个提交合并为一个
- [ ] 能修改历史提交的提交信息
- [ ] 理解交互式变基的风险（不要对已推送的提交使用）

**练习12：Cherry-pick 选择性合并**

**场景说明**：当你只需要从其他分支合并特定的某个提交，而不是整个分支时，可以使用 cherry-pick 命令。这在热修复场景中特别有用。

**具体需求**：
1. 在 `feature-c` 分支上创建 3 次提交（提交 A、提交 B、提交 C）
2. 切换到 main 分支
3. 使用 cherry-pick 只将提交 B 应用到 main
4. 验证 main 分支只有提交 B 的修改
5. 处理 cherry-pick 可能产生的冲突

**使用示例**：
```bash
# 1. 创建 feature-c 分支并添加 3 次提交
git checkout -b feature-c

echo "功能A：用户登录" > feature_a.txt
git add feature_a.txt
git commit -m "feat: 添加用户登录功能"
COMMIT_A=$(git rev-parse HEAD)

echo "功能B：密码重置" > feature_b.txt
git add feature_b.txt
git commit -m "feat: 添加密码重置功能"
COMMIT_B=$(git rev-parse HEAD)

echo "功能C：用户注销" > feature_c.txt
git add feature_c.txt
git commit -m "feat: 添加用户注销功能"

# 2. 查看提交历史，记录提交 B 的 ID
git log --oneline -3
# 输出:
# abc1234 feat: 添加用户注销功能
# def5678 feat: 添加密码重置功能  <- 这是我们需要的
# ghi9012 feat: 添加用户登录功能

# 3. 切换到 main 分支
git checkout main

# 4. 使用 cherry-pick 只应用提交 B
git cherry-pick def5678
# 或使用完整的 commit hash
# git cherry-pick $COMMIT_B

# 5. 验证结果
git log --oneline -1
# 输出: def5678 feat: 添加密码重置功能

ls -la
# 应该只有 feature_b.txt，没有 feature_a.txt 和 feature_c.txt

# 6. 处理 cherry-pick 冲突
# 如果有冲突：
# 1. 手动解决冲突
# 2. git add 冲突文件
# 3. git cherry-pick --continue
# 或放弃：git cherry-pick --abort

# 7. cherry-pick 多个提交
git cherry-pick commit1..commit2  # 范围（不包含 commit1）
git cherry-pick commit1^..commit2  # 范围（包含 commit1）

# 8. cherry-pick 但不自动提交（先审查）
git cherry-pick -n def5678
# 审查修改后再手动 commit
```

**验收标准**：
- [ ] 能正确使用 cherry-pick 选择性合并提交
- [ ] 理解 cherry-pick 与 merge 的区别
- [ ] 能处理 cherry-pick 产生的冲突
- [ ] 理解 cherry-pick 的使用场景（热修复、选择性功能合并）
- [ ] 能使用 `-n` 参数进行审查后再提交

**练习13：Git Reset 三种模式**

**场景说明**：理解 Git reset 三种模式的区别是版本控制的核心技能，不同的模式决定了是否保留工作区和暂存区的修改。

**具体需求**：
1. 创建 3 次提交（提交1、提交2、提交3）
2. 使用 `git reset --soft HEAD~1` 回退一次，观察工作区和暂存区状态
3. 再次提交，恢复到 3 次提交状态
4. 使用 `git reset --mixed HEAD~1` 回退一次，观察状态变化
5. 使用 `git reset --hard HEAD~1` 回退一次，观察状态变化
6. 总结三种模式的区别

**使用示例**：
```bash
# 1. 准备测试环境：创建 3 次提交
mkdir reset-test && cd reset-test && git init
echo "版本1" > file.txt && git add . && git commit -m "提交1：版本1"
echo "版本2" >> file.txt && git add . && git commit -m "提交2：版本2"
echo "版本3" >> file.txt && git add . && git commit -m "提交3：版本3"

# 2. 查看当前状态
git log --oneline
# 输出:
# abc1234 提交3：版本3
# def5678 提交2：版本2
# ghi9012 提交1：版本1

# ============================================
# 模式1：--soft（软重置）
# ============================================
# 回退到提交2，保留修改在暂存区
git reset --soft HEAD~1

# 查看状态
git status
# 输出: Changes to be committed:
#         modified:   file.txt  <- 修改在暂存区

git log --oneline
# 输出:
# def5678 提交2：版本2
# ghi9012 提交1：版本1

# 文件内容仍然包含 "版本3"
cat file.txt  # 版本1\n版本2\n版本3

# 可以直接重新提交
git commit -m "提交3：版本3（重新提交）"

# ============================================
# 模式2：--mixed（混合重置，默认）
# ============================================
# 先恢复 3 次提交
echo "版本3" >> file.txt && git add . && git commit -m "提交3：版本3"

# 使用 --mixed 回退（或不写参数，默认就是 --mixed）
git reset --mixed HEAD~1
# 或简写
git reset HEAD~1

# 查看状态
git status
# 输出: Changes not staged for commit:
#         modified:   file.txt  <- 修改在工作区，未暂存

git log --oneline
# 只有 2 次提交

# 文件内容仍然保留
cat file.txt  # 版本1\n版本2\n版本3

# 需要重新 add 才能 commit
git add . && git commit -m "提交3：版本3"

# ============================================
# 模式3：--hard（硬重置，危险！）
# ============================================
# 恢复 3 次提交
echo "版本3" >> file.txt && git add . && git commit -m "提交3：版本3"

# 使用 --hard 回退（会丢失修改！）
git reset --hard HEAD~1

# 查看状态
git status
# 输出: nothing to commit, working tree clean

# 文件内容也回退了！
cat file.txt  # 只有 版本1\n版本2

# ============================================
# 三种模式对比总结
# ============================================
# --soft:   回退提交，保留修改在暂存区（staged）
# --mixed:  回退提交，保留修改在工作区（unstaged）
# --hard:   回退提交，丢弃所有修改（危险！）

# 使用场景：
# --soft:   想重新组织提交，但不丢失修改
# --mixed:  想重新审视修改，重新 add
# --hard:   确定要丢弃所有修改（慎用！）
```

**验收标准**：
- [ ] 能清晰区分 soft、mixed、hard 三种模式
- [ ] 理解三种模式对工作区、暂存区、提交区的不同影响
- [ ] 能根据实际场景选择合适的 reset 模式
- [ ] 理解 --hard 的危险性，谨慎使用
- [ ] 能使用 `git log` 和 `git status` 验证 reset 结果

**练习14：Git Reflog 恢复**

**场景说明**：Git reflog 是 Git 的"后悔药"，记录了所有 HEAD 的变化历史，即使使用 `reset --hard` 丢失了提交，也可以通过 reflog 找回。

**具体需求**：
1. 创建几次提交
2. 使用 `git reset --hard` 回退到之前的状态（模拟误操作）
3. 使用 `git reflog` 查看操作历史
4. 使用 reflog 找回被丢弃的提交
5. 恢复到之前的状态

**使用示例**：
```bash
# 1. 创建几次提交
echo "版本1" > file.txt && git add . && git commit -m "提交1"
echo "版本2" >> file.txt && git add . && git commit -m "提交2"
echo "版本3" >> file.txt && git add . && git commit -m "提交3"
echo "版本4" >> file.txt && git add . && git commit -m "提交4"
echo "版本5" >> file.txt && git add . && git commit -m "提交5"

# 2. 查看当前提交历史
git log --oneline
# 输出:
# abc1234 提交5
# def5678 提交4
# ghi9012 提交3
# jkl3456 提交2
# mno7890 提交1

# 3. 模拟误操作：使用 --hard 回退，丢弃后 3 次提交
git reset --hard HEAD~3
# 现在只剩下提交1和提交2

git log --oneline
# 输出:
# jkl3456 提交2
# mno7890 提交1
# 提交3、4、5 "丢失"了！

# 4. 使用 reflog 查看操作历史
git reflog
# 输出:
# jkl3456 HEAD@{0}: reset: moving to HEAD~3
# abc1234 HEAD@{1}: commit: 提交5        <- 这是我们想恢复的状态
# def5678 HEAD@{2}: commit: 提交4
# ghi9012 HEAD@{3}: commit: 提交3
# jkl3456 HEAD@{4}: commit: 提交2
# mno7890 HEAD@{5}: commit: 提交1

# 5. 使用 reflog 恢复到之前的状态
# 方法1：使用 reflog 编号
git reset --hard HEAD@{1}
# 或使用 commit hash
git reset --hard abc1234

# 6. 验证恢复成功
git log --oneline
# 输出:
# abc1234 提交5
# def5678 提交4
# ghi9012 提交3
# jkl3456 提交2
# mno7890 提交1
# 所有提交都回来了！

# 7. 其他 reflog 用法
# 查看最近 10 条记录
git reflog -10

# 查看某个分支的 reflog
git reflog show feature-branch

# 查看指定时间范围
git reflog --since="2 hours ago"

# 8. 恢复单个文件
# 如果你只想恢复某个文件到之前的状态
git checkout HEAD@{1} -- path/to/file.txt
```

**验收标准**：
- [ ] 能使用 `git reflog` 查看操作历史
- [ ] 理解 reflog 记录的是 HEAD 的变化
- [ ] 能通过 reflog 恢复误删的提交
- [ ] 能使用 `HEAD@{n}` 或 commit hash 恢复
- [ ] 理解 reflog 有过期时间（默认 90 天）

**练习15：Git Flow 工作流实践**

**场景说明**：Git Flow 是一种广泛使用的分支策略，定义了 main、develop、feature、release、hotfix 五种分支类型，规范了团队协作流程。

**具体需求**：
1. 初始化 Git Flow 结构（创建 main 和 develop 分支）
2. 从 develop 创建 `feature/user-auth` 分支开发新功能
3. 完成功能开发后合并回 develop
4. 从 develop 创建 `release/1.0.0` 分支准备发布
5. 发布到 main 并打标签

**使用示例**：
```bash
# 1. 初始化仓库
mkdir gitflow-demo && cd gitflow-demo
git init
echo "# Git Flow Demo" > README.md
git add . && git commit -m "feat: 初始化项目"

# 2. 创建 develop 分支
git checkout -b develop
git checkout main  # 切回 main

# ============================================
# 功能开发流程
# ============================================
# 3. 从 develop 创建功能分支
git checkout develop
git checkout -b feature/user-auth

# 4. 在功能分支上开发
echo "用户认证模块" > auth.py
git add auth.py && git commit -m "feat: 添加用户认证模块"

echo "登录功能" >> auth.py
git add . && git commit -m "feat: 实现登录功能"

echo "登出功能" >> auth.py
git add . && git commit -m "feat: 实现登出功能"

# 5. 功能开发完成，合并回 develop
git checkout develop
git merge --no-ff feature/user-auth -m "merge: 合并用户认证功能"
git branch -d feature/user-auth

# ============================================
# 发布流程
# ============================================
# 6. 从 develop 创建 release 分支
git checkout -b release/1.0.0

# 7. 在 release 分支上修复 bug、更新版本号
echo "修复发布前的 bug" >> auth.py
git add . && git commit -m "fix: 修复发布前的 bug"

# 更新版本号
echo "version: 1.0.0" > VERSION
git add VERSION && git commit -m "chore: 更新版本号到 1.0.0"

# 8. 发布：合并到 main
git checkout main
git merge --no-ff release/1.0.0 -m "release: 发布 1.0.0"

# 9. 打标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 10. 也要合并回 develop（保持 develop 同步）
git checkout develop
git merge --no-ff release/1.0.0

# 11. 删除 release 分支
git branch -d release/1.0.0

# ============================================
# 紧急修复流程
# ============================================
# 12. 从 main 创建 hotfix 分支
git checkout main
git checkout -b hotfix/1.0.1

# 13. 修复紧急 bug
echo "修复紧急 bug" >> auth.py
git add . && git commit -m "fix: 修复紧急安全问题"

# 14. 合并到 main 和 develop
git checkout main
git merge --no-ff hotfix/1.0.1
git tag -a v1.0.1 -m "Hotfix version 1.0.1"

git checkout develop
git merge --no-ff hotfix/1.0.1

# 15. 删除 hotfix 分支
git branch -d hotfix/1.0.1

# ============================================
# 查看分支结构
# ============================================
git log --oneline --graph --all
```

**验收标准**：
- [ ] 理解 Git Flow 的五种分支类型和作用
- [ ] 能正确执行功能开发流程
- [ ] 能正确执行发布流程
- [ ] 能正确执行紧急修复流程
- [ ] 理解为什么 release 和 hotfix 要同时合并到 main 和 develop

**练习16：远程仓库协作**

**场景说明**：在实际团队开发中，需要与远程仓库进行协作，掌握 clone、push、pull、fetch 等操作是必备技能。

**具体需求**：
1. 在 GitHub/GitLab 上创建远程仓库（或使用已有仓库）
2. 添加远程仓库地址到本地仓库
3. 推送本地分支到远程
4. 模拟协作场景：克隆仓库、做修改并推送
5. 原仓库拉取更新，解决可能的冲突

**使用示例**：
```bash
# ============================================
# 初始化远程仓库连接
# ============================================
# 1. 添加远程仓库
git remote add origin https://github.com/username/repo.git
# 或使用 SSH
git remote add origin git@github.com:username/repo.git

# 2. 查看远程仓库
git remote -v
# 输出:
# origin  https://github.com/username/repo.git (fetch)
# origin  https://github.com/username/repo.git (push)

# 3. 修改远程仓库地址
git remote set-url origin https://new-url.git

# ============================================
# 推送本地分支
# ============================================
# 4. 首次推送（设置上游分支）
git push -u origin main
# -u 等同于 --set-upstream

# 5. 后续推送
git push origin main
# 或简写（已设置上游）
git push

# 6. 推送所有分支
git push --all origin

# 7. 推送标签
git push origin v1.0.0
git push --tags  # 推送所有标签

# 8. 强制推送（危险！仅在确定必要时使用）
git push -f origin main
# 更安全的强制推送
git push --force-with-lease origin main

# ============================================
# 拉取远程更新
# ============================================
# 9. fetch：只拉取，不合并
git fetch origin
git fetch --all  # 拉取所有远程

# 10. 查看远程分支
git branch -r
git branch -a  # 所有分支

# 11. 查看远程更新
git log origin/main

# 12. pull：拉取并合并
git pull origin main
# 使用 rebase 方式
git pull --rebase origin main

# 13. 合并远程更新
git fetch origin
git merge origin/main

# ============================================
# 模拟团队协作
# ============================================
# 14. 克隆仓库（模拟另一开发者）
cd /tmp
git clone https://github.com/username/repo.git repo-clone
cd repo-clone

# 15. 创建分支并修改
git checkout -b feature-by-other
echo "其他开发者的修改" >> README.md
git add . && git commit -m "feat: 其他开发者的修改"

# 16. 推送到远程
git push origin feature-by-other

# 17. 回到原仓库，拉取更新
cd /path/to/original/repo
git fetch origin
git branch -a  # 可以看到 origin/feature-by-other

# 18. 检出远程分支
git checkout -b feature-by-other origin/feature-by-other
# 或
git checkout --track origin/feature-by-other

# 19. 查看跟踪关系
git branch -vv
# 输出:
# * main                abc1234 [origin/main] 最新提交
#   feature-by-other    def5678 [origin/feature-by-other] 其他开发者的修改

# ============================================
# 处理远程冲突
# ============================================
# 20. 如果 pull 时有冲突
git pull origin main
# 冲突时解决：
# 1. 手动解决冲突文件
# 2. git add 冲突文件
# 3. git commit
# 或中止：git merge --abort

# 21. 删除远程分支
git push origin --delete feature-by-other

# ============================================
# 同步 fork 的仓库
# ============================================
# 22. 添加上游仓库
git remote add upstream https://github.com/original/repo.git

# 23. 同步上游更新
git fetch upstream
git checkout main
git merge upstream/main
```

**验收标准**：
- [ ] 能正确添加和管理远程仓库
- [ ] 能使用 push 推送本地分支到远程
- [ ] 能使用 fetch 和 pull 拉取远程更新
- [ ] 理解本地分支与远程分支的跟踪关系
- [ ] 能处理 pull 时的冲突
- [ ] 理解 clone、push、pull、fetch 的区别

### 综合练习（17-20）

---

**练习17：完整项目版本控制**

**场景说明**：模拟一个完整的项目开发流程，从初始化到发布，体验完整的 Git 工作流。

**具体需求**：
1. 初始化项目，创建 .gitignore
2. 创建 develop 分支
3. 开发功能 A（feature/feature-a）
4. 开发功能 B（feature/feature-b）
5. 合并到 develop，测试
6. 创建 release 分支，修复 bug
7. 发布到 main，打版本标签

**使用示例**：
```bash
# ============================================
# 1. 初始化项目
# ============================================
mkdir my-project && cd my-project
git init
git config user.name "开发者"
git config user.email "dev@example.com"

# 创建 .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.env
.idea/
.vscode/
*.log
EOF

# 初始提交
echo "# My Project" > README.md
git add . && git commit -m "feat: 初始化项目"

# ============================================
# 2. 创建 develop 分支
# ============================================
git checkout -b develop

# ============================================
# 3. 开发功能 A
# ============================================
git checkout -b feature/feature-a

# 创建功能 A 文件
mkdir -p src
cat > src/feature_a.py << 'EOF'
def feature_a():
    """功能 A 实现"""
    return "Feature A"
EOF

git add . && git commit -m "feat: 实现功能 A"

# ============================================
# 4. 开发功能 B
# ============================================
git checkout develop
git checkout -b feature/feature-b

cat > src/feature_b.py << 'EOF'
def feature_b():
    """功能 B 实现"""
    return "Feature B"
EOF

git add . && git commit -m "feat: 实现功能 B"

# ============================================
# 5. 合并到 develop
# ============================================
git checkout develop
git merge --no-ff feature/feature-a -m "merge: 合并功能 A"
git merge --no-ff feature/feature-b -m "merge: 合并功能 B"

# 删除功能分支
git branch -d feature/feature-a
git branch -d feature/feature-b

# ============================================
# 6. 创建 release 分支
# ============================================
git checkout -b release/1.0.0

# 修复发布前发现的 bug
echo "# 修复后的功能" >> src/feature_a.py
git add . && git commit -m "fix: 修复发布前的问题"

# 更新版本号
echo "1.0.0" > VERSION
git add . && git commit -m "chore: 更新版本号到 1.0.0"

# ============================================
# 7. 发布到 main
# ============================================
git checkout main
git merge --no-ff release/1.0.0 -m "release: 发布 1.0.0"
git tag -a v1.0.0 -m "Release version 1.0.0"

# 同步回 develop
git checkout develop
git merge --no-ff release/1.0.0

# 删除 release 分支
git branch -d release/1.0.0

# ============================================
# 8. 查看最终历史
# ============================================
git log --oneline --graph --all
```

**验收标准**：
- [ ] 项目结构清晰，包含 .gitignore
- [ ] 功能分支正确合并到 develop
- [ ] release 分支处理正确
- [ ] main 分支有版本标签
- [ ] 提交历史清晰，分支结构合理

**练习18：代码回滚与恢复**

**场景说明**：项目发布了 v1.0.0，发现了一个严重 bug，需要紧急修复并发布 v1.0.1。同时需要撤销某次有问题的提交。

**具体需求**：
1. 检出 v1.0.0 标签
2. 创建 hotfix/v1.0.1 分支
3. 修复 bug 并提交
4. 使用 `git revert` 撤销某次有问题的提交
5. 合并到 main 和 develop，打 v1.0.1 标签

**使用示例**：
```bash
# ============================================
# 场景：v1.0.0 发布后发现严重 bug
# ============================================

# 1. 查看当前状态
git log --oneline -5
git tag -l

# 2. 基于 v1.0.0 创建 hotfix 分支
git checkout -b hotfix/v1.0.1 v1.0.0
# 或者从 main 创建
git checkout main
git checkout -b hotfix/v1.0.1

# 3. 修复紧急 bug
cat > hotfix.py << 'EOF'
# 修复安全漏洞
def fix_security_issue():
    return "安全漏洞已修复"
EOF

git add . && git commit -m "fix: 修复安全漏洞 CVE-2024-001"

# 4. 假设发现之前的某次提交有问题，需要撤销
# 先查看提交历史
git log --oneline main
# 假设 def5678 是有问题的提交

# 使用 revert 撤销（创建新提交，不修改历史）
git revert def5678 --no-edit
# 会创建一个新的提交来撤销 def5678 的修改

# 5. 更新版本号
echo "1.0.1" > VERSION
git add . && git commit -m "chore: 更新版本号到 1.0.1"

# ============================================
# 发布 hotfix
# ============================================
# 6. 合并到 main
git checkout main
git merge --no-ff hotfix/v1.0.1 -m "hotfix: 紧急修复 v1.0.1"
git tag -a v1.0.1 -m "Hotfix version 1.0.1"

# 7. 同步到 develop（确保 develop 也有修复）
git checkout develop
git merge --no-ff hotfix/v1.0.1

# 8. 删除 hotfix 分支
git branch -d hotfix/v1.0.1

# ============================================
# 验证结果
# ============================================
# 查看标签
git tag -l "v1.0.*"
# 输出: v1.0.0, v1.0.1

# 查看 main 分支历史
git checkout main
git log --oneline -5

# ============================================
# revert vs reset 对比
# ============================================
# git revert <commit>:
#   - 创建新提交来撤销修改
#   - 保留历史记录
#   - 适合已推送的提交
#   - 安全，不会丢失数据

# git reset --hard <commit>:
#   - 直接回退到指定提交
#   - 删除历史记录
#   - 只适合未推送的提交
#   - 危险，可能丢失数据

# 如果需要撤销多个提交
git revert def5678..abc1234  # 撤销范围（不包含 def5678）
git revert def5678^..abc1234  # 撤销范围（包含 def5678）
```

**验收标准**：
- [ ] 能正确创建 hotfix 分支
- [ ] 能使用 revert 撤销指定提交
- [ ] 理解 revert 和 reset 的区别及使用场景
- [ ] hotfix 正确合并到 main 和 develop
- [ ] 正确打版本标签

**练习19：Git 钩子配置**

**场景说明**：Git 钩子（hooks）可以在特定事件发生时自动执行脚本，常用于代码检查、提交信息验证、自动化测试等场景。

**具体需求**：
1. 进入 `.git/hooks` 目录，了解现有的钩子模板
2. 创建 `pre-commit` 钩子：检查代码中是否有 console.log 和 TODO 标记
3. 创建 `commit-msg` 钩子：验证提交信息格式（feat|fix|docs: 开头）
4. 测试钩子是否生效
5. 理解客户端钩子和服务端钩子的区别

**使用示例**：
```bash
# ============================================
# 1. 查看钩子目录
# ============================================
ls -la .git/hooks/
# 输出各种 .sample 文件（示例模板）

# ============================================
# 2. 创建 pre-commit 钩子
# ============================================
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# pre-commit 钩子：提交前检查

echo "执行 pre-commit 检查..."

# 获取暂存的文件
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|ts)$')

if [ -z "$STAGED_FILES" ]; then
    echo "没有需要检查的文件"
    exit 0
fi

# 检查 console.log
CONSOLE_LOG=$(git diff --cached -U0 $STAGED_FILES | grep -E '^\+.*console\.log' || true)
if [ ! -z "$CONSOLE_LOG" ]; then
    echo "❌ 错误：发现 console.log 语句"
    echo "$CONSOLE_LOG"
    exit 1
fi

# 检查 print 语句（Python）
PRINT_STMT=$(git diff --cached -U0 $STAGED_FILES | grep -E '^\+.*print\(' | grep -v 'print(' || true)
if [ ! -z "$PRINT_STMT" ]; then
    echo "⚠️  警告：发现 print 语句（建议使用 logging）"
fi

# 检查 TODO 标记
TODO_FOUND=$(git diff --cached -U0 $STAGED_FILES | grep -E '^\+.*TODO' || true)
if [ ! -z "$TODO_FOUND" ]; then
    echo "⚠️  警告：发现 TODO 标记"
    echo "$TODO_FOUND"
fi

echo "✅ pre-commit 检查通过"
exit 0
EOF

# 添加执行权限
chmod +x .git/hooks/pre-commit

# ============================================
# 3. 创建 commit-msg 钩子
# ============================================
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# commit-msg 钩子：验证提交信息格式

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# 提交信息格式：type(scope): subject
# type: feat|fix|docs|style|refactor|test|chore
# 示例：feat(auth): 添加用户登录功能

PATTERN="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,}$"

if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
    echo "❌ 提交信息格式不正确！"
    echo ""
    echo "正确格式：type(scope): subject"
    echo ""
    echo "type 类型："
    echo "  feat     - 新功能"
    echo "  fix      - 修复 bug"
    echo "  docs     - 文档更新"
    echo "  style    - 代码格式（不影响功能）"
    echo "  refactor - 重构"
    echo "  test     - 测试相关"
    echo "  chore    - 构建/工具相关"
    echo ""
    echo "示例："
    echo "  feat(auth): 添加用户登录功能"
    echo "  fix: 修复登录页面样式问题"
    echo "  docs: 更新 README"
    exit 1
fi

echo "✅ 提交信息格式正确"
exit 0
EOF

chmod +x .git/hooks/commit-msg

# ============================================
# 4. 测试钩子
# ============================================
# 测试 pre-commit
echo "console.log('test');" > test.js
git add test.js
git commit -m "test"
# 输出：❌ 错误：发现 console.log 语句

# 修复后重新提交
echo "const x = 1;" > test.js
git add test.js

# 测试 commit-msg（格式错误）
git commit -m "错误的提交信息"
# 输出：❌ 提交信息格式不正确！

# 测试 commit-msg（格式正确）
git commit -m "feat: 添加测试文件"
# 输出：✅ 提交信息格式正确

# ============================================
# 5. 跳过钩子（紧急情况）
# ============================================
# 使用 --no-verify 跳过钩子
git commit --no-verify -m "紧急修复"

# ============================================
# 6. 其他常用钩子
# ============================================
# pre-push：推送前检查（如运行测试）
# post-merge：合并后执行（如安装依赖）
# post-checkout：切换分支后执行

# pre-push 示例
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# 推送前运行测试
echo "运行测试..."
pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "❌ 测试失败，禁止推送"
    exit 1
fi
exit 0
EOF
chmod +x .git/hooks/pre-push
```

**验收标准**：
- [ ] 能正确创建 pre-commit 钩子
- [ ] 能正确创建 commit-msg 钩子
- [ ] 钩子在对应事件时正确执行
- [ ] 不符合规范的提交被拒绝
- [ ] 理解 `--no-verify` 跳过钩子的用法

**练习20：团队协作冲突处理**

**场景说明**：在团队协作中，多个开发者可能同时修改同一文件，导致冲突。学会正确处理冲突是团队协作的关键技能。

**具体需求**：
1. 创建两个本地仓库模拟两个开发者
2. 开发者 A 修改文件并推送到远程
3. 开发者 B 修改同一文件的同一位置
4. 开发者 B 尝试推送，发现冲突
5. 开发者 B 拉取、解决冲突、重新推送

**使用示例**：
```bash
# ============================================
# 1. 创建模拟环境
# ============================================
# 创建远程仓库（模拟服务器）
mkdir -p /tmp/git-remote && cd /tmp/git-remote
git init --bare project.git

# 开发者 A 克隆
mkdir -p /tmp/dev-a && cd /tmp/dev-a
git clone /tmp/git-remote/project.git
cd project
git config user.name "开发者A"
git config user.email "dev-a@example.com"

# 开发者 B 克隆
mkdir -p /tmp/dev-b && cd /tmp/dev-b
git clone /tmp/git-remote/project.git
cd project
git config user.name "开发者B"
git config user.email "dev-b@example.com"

# ============================================
# 2. 开发者 A：创建初始文件并推送
# ============================================
cd /tmp/dev-a/project
cat > README.md << 'EOF'
# 项目说明

## 功能列表
- 功能1
- 功能2
EOF

git add . && git commit -m "feat: 初始化 README"
git push origin main

# ============================================
# 3. 开发者 B：拉取更新，然后修改同一位置
# ============================================
cd /tmp/dev-b/project
git pull origin main

# 修改 README（同一位置）
cat > README.md << 'EOF'
# 项目说明

## 功能列表
- 功能1
- 功能2
- 功能3 (开发者B添加)
EOF

git add . && git commit -m "feat: 添加功能3"

# ============================================
# 4. 开发者 A：同时修改同一位置
# ============================================
cd /tmp/dev-a/project
cat > README.md << 'EOF'
# 项目说明

## 功能列表
- 功能1
- 功能2
- 功能4 (开发者A添加)
EOF

git add . && git commit -m "feat: 添加功能4"

# ============================================
# 5. 开发者 A 先推送（成功）
# ============================================
git push origin main

# ============================================
# 6. 开发者 B 尝试推送（失败）
# ============================================
cd /tmp/dev-b/project
git push origin main
# 输出：! [rejected] main -> main (fetch first)
#       error: failed to push some refs

# ============================================
# 7. 开发者 B 拉取并解决冲突
# ============================================
git pull origin main
# 输出：CONFLICT (content): Merge conflict in README.md
#       Automatic merge failed; fix conflicts and then commit the result.

# 查看冲突文件
cat README.md
# 输出：
# # 项目说明
#
# ## 功能列表
# - 功能1
# - 功能2
# <<<<<<< HEAD
# - 功能3 (开发者B添加)
# =======
# - 功能4 (开发者A添加)
# >>>>>>> abc1234...

# 手动解决冲突
cat > README.md << 'EOF'
# 项目说明

## 功能列表
- 功能1
- 功能2
- 功能3 (开发者B添加)
- 功能4 (开发者A添加)
EOF

# 标记冲突已解决
git add README.md
git commit -m "merge: 合并开发者A的修改，解决冲突"

# ============================================
# 8. 开发者 B 重新推送（成功）
# ============================================
git push origin main

# ============================================
# 9. 开发者 A 拉取最新代码
# ============================================
cd /tmp/dev-a/project
git pull origin main

# 验证
cat README.md
# 现在两个开发者的代码都包含了

# ============================================
# 最佳实践总结
# ============================================
# 1. 提交前先 pull，保持本地最新
# 2. 小步提交，避免大范围修改
# 3. 避免修改同一文件的同一位置
# 4. 冲突时与相关开发者沟通
# 5. 解决冲突后仔细检查代码

# ============================================
# 使用 rebase 保持线性历史（可选）
# ============================================
# 开发者 B 也可以使用 rebase
git pull --rebase origin main
# 这样会把你的提交放在远程提交之后
# 如果有冲突，解决后：
git add README.md
git rebase --continue
```

**验收标准**：
- [ ] 能模拟多人协作场景
- [ ] 能识别推送冲突
- [ ] 能正确拉取并解决冲突
- [ ] 理解冲突标记的含义
- [ ] 掌握冲突解决的最佳实践

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
