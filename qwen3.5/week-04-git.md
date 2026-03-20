# 第 4 周 - Git 版本控制

## 学习目标
掌握 Git 版本控制的核心命令和工作流，能够熟练使用 Git 进行代码管理和协作。

---

## 知识点清单

### 1. 基础命令
**掌握程度**: init/add/commit/status/log/diff

**练习资源**:
- [Git 官方文档](https://git-scm.com/doc)
- [Git 教程 - 廖雪峰](https://www.liaoxuefeng.com/wiki/896043488029600)

**练习任务**:
- 初始化一个 Git 仓库
- 完成首次提交
- 查看提交历史和差异

---

### 2. 分支
**掌握程度**: branch/checkout/merge

**练习任务**:
- 创建新分支
- 在分支上开发
- 合并到主分支

---

### 3. 冲突解决
**掌握程度**: 识别冲突、手动解决

**练习任务**:
- 制造一个合并冲突
- 手动解决冲突
- 理解冲突产生的原因

---

### 4. 远程操作
**掌握程度**: remote/push/pull/fetch

**练习资源**:
- [GitHub 教程](https://docs.github.com/en/get-started)

**练习任务**:
- 创建 GitHub 账号
- 创建远程仓库
- 推送本地代码
- 拉取远程更新

---

### 5. 变基
**掌握程度**: rebase vs merge、交互式 rebase

**练习任务**:
- 用 rebase 整理提交历史
- 理解 rebase 和 merge 的区别
- 交互式 rebase 压缩提交

---

### 6. 回退
**掌握程度**: reset/revert、HEAD 用法

**练习任务**:
- 回退到指定提交
- 撤销一次错误提交
- 理解 reset --soft/mixed/hard 的区别

---

### 7. 标签
**掌握程度**: tag 创建推送

**练习任务**:
- 给版本打 tag
- 推送 tag 到远程

---

### 8. 最佳实践
**掌握程度**: 提交信息规范、分支策略

**练习资源**:
- [Conventional Commits](https://www.conventionalcommits.org/)

**练习任务**:
- 遵循 conventional commits 规范
- 保持提交历史整洁

---

## 本周练习任务

### 必做任务

1. **GitHub 仓库建立**
```bash
# 创建 GitHub 账号
# 创建 python-practice 仓库
# 配置 SSH 密钥
# 推送代码
```

2. **分支练习**
```bash
# 每天练习:
# 1. 创建特性分支
# 2. 修改代码
# 3. 提交
# 4. 合并到 main
# 5. 推送到远程
```

3. **冲突解决练习**
```bash
# 1. 创建两个分支
# 2. 在两个分支上修改同一文件
# 3. 尝试合并，制造冲突
# 4. 手动解决冲突
```

4. **提交历史整理**
```bash
# 1. 用 interactive rebase 压缩提交
# 2. 修改提交信息
# 3. 保持历史整洁
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] GitHub 有 1 个仓库，提交记录 30+
- [ ] 至少有 2 个分支合并记录
- [ ] 能解决一次手动制造的合并冲突
- [ ] 提交信息符合 conventional commits 规范
- [ ] 能用 rebase 整理历史
- [ ] 能回退错误提交

---

## Git 命令速查表

### 基础命令
```bash
git init                    # 初始化仓库
git clone <url>            # 克隆仓库
git status                 # 查看状态
git add <file>             # 添加文件
git commit -m "msg"        # 提交
git log                    # 查看历史
git diff                   # 查看差异
```

### 分支命令
```bash
git branch                 # 查看分支
git branch <name>          # 创建分支
git checkout <name>        # 切换分支
git checkout -b <name>     # 创建并切换
git merge <branch>         # 合并分支
git branch -d <name>       # 删除分支
```

### 远程命令
```bash
git remote -v              # 查看远程
git remote add <name> <url> # 添加远程
git push <remote> <branch> # 推送
git pull <remote> <branch> # 拉取
git fetch <remote>         # 获取
```

### 回退命令
```bash
git reset --soft HEAD~1    # 回退，保留更改
git reset --mixed HEAD~1   # 回退，保留文件
git reset --hard HEAD~1    # 回退，丢弃更改
git revert <commit>        # 撤销提交
```

### 变基命令
```bash
git rebase <branch>        # 变基
git rebase -i HEAD~n       # 交互式变基
```

---

## 面试考点

### 高频面试题
1. git merge 和 git rebase 的区别？
2. git reset 和 git revert 的区别？
3. 什么是 HEAD？
4. 如何解决合并冲突？
5. 什么是 fast-forward 合并？
6. 什么是 detached HEAD 状态？
7. git fetch 和 git pull 的区别？

### 场景题
```bash
# 1. 提交错了文件，如何撤销？
# 2. 提交信息写错了，如何修改？
# 3. 想把多个提交压缩成一个？
# 4. 想回退到某个历史版本？
# 5. 合并时产生冲突，如何解决？
```

---

## 每日学习检查清单

### Day 1-2: 基础命令
- [ ] 学习 Git 基础概念
- [ ] 初始化仓库
- [ ] 完成首次提交
- [ ] GitHub 提交

### Day 3-4: 分支 + 合并
- [ ] 学习分支操作
- [ ] 创建合并分支
- [ ] GitHub 提交

### Day 5: 冲突解决
- [ ] 制造合并冲突
- [ ] 手动解决冲突
- [ ] GitHub 提交

### Day 6-7: 远程 + 变基 + 回退
- [ ] 学习远程操作
- [ ] 学习 rebase
- [ ] 学习回退
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 4 周总结

### 学习内容
- 掌握了 Git 基础命令
- 学会了分支管理
- 能解决合并冲突

### 遇到的问题
- rebase 理解困难（已解决）
- 冲突解决不熟练（已解决）

### GitHub 仓库
- 仓库链接：...
- 提交次数：XX 次

### 下周改进
- ...
```
