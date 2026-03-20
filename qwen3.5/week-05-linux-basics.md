# 第 5 周 - Linux 基础

## 学习目标
掌握 Linux 系统的基本操作，能够熟练使用命令行完成文件管理、文本处理、权限管理等任务。

---

## 知识点清单

### 1. 文件系统
**掌握程度**: 目录结构、cd/pwd/ls/mkdir/rm/cp/mv

**练习资源**:
- [Linux 命令大全](https://man.linuxde.net/)
- [Linux 教程 - 菜鸟教程](https://www.runoob.com/linux/linux-tutorial.html)

**练习任务**:
- 在终端完成文件创建、复制、移动、删除
- 熟悉 Linux 目录结构（/etc, /var, /home, /usr 等）

---

### 2. 文件查看
**掌握程度**: cat/tac/head/tail/less/more

**练习任务**:
- 查看大文件的指定行（如：查看日志的最后 100 行）
- 分页查看文件内容

---

### 3. 权限管理
**掌握程度**: chmod/chown、rwx 含义、数字表示法

**练习任务**:
- 设置文件权限（如：755, 644）
- 修改文件所有者
- 理解 rwxr-xr-x 的含义

---

### 4. 文本处理
**掌握程度**: grep/cut/sort/uniq/wc

**练习任务**:
- 从日志中搜索特定关键词
- 统计文件中不重复的行数
- 提取文件的指定列

---

### 5. 管道重定向
**掌握程度**: `|`、`>`、`>>`、`2>&1`

**练习任务**:
- 组合多个命令完成任务
- 将输出重定向到文件
- 理解标准输出和标准错误

---

### 6. 查找
**掌握程度**: find/locate、按名称/大小/时间

**练习任务**:
- 按文件名查找
- 按文件大小查找
- 按修改时间查找

---

### 7. 压缩
**掌握程度**: tar/gzip/zip/unzip

**练习任务**:
- 打包目录
- 解压 tar.gz 文件
- 压缩文件

---

### 8. 编辑器
**掌握程度**: vim 基础（插入/保存/退出/搜索）

**练习资源**:
- [Vim 教程](https://github.com/wsdjeg/vim-galore-zh_cn)

**练习任务**:
- 用 vim 编辑文件
- 掌握基本操作（插入、保存、退出、搜索、替换）

---

## 本周练习任务

### 必做任务

1. **环境搭建**
```bash
# 选项 1: 购买云服务器（阿里云/腾讯云）
# 选项 2: 使用虚拟机（VirtualBox + Ubuntu）
# 选项 3: 使用 WSL（Windows Subsystem for Linux）
```

2. **文件操作练习（20 题）**
```bash
# 1. 创建目录结构
mkdir -p project/{src,dist,tests}

# 2. 创建文件
touch file{1..10}.txt

# 3. 复制、移动、删除练习
# ...
```

3. **日志分析任务**
```bash
# 给定一个 10MB 的 Nginx 日志文件
# 1. 找出访问最多的 IP（前 10）
# 2. 找出错误最多的 URL（前 10）
# 3. 统计每小时的请求数
```

4. **Shell 脚本（5 个）**
```bash
# 1. 批量重命名脚本（给所有.txt 文件加日期前缀）
# 2. 日志清理脚本（删除 7 天前的日志）
# 3. 文件备份脚本
# 4. 系统信息收集脚本
# 5. 用户管理脚本
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 20 道 Linux 命令练习题全对
- [ ] 能从日志文件中提取指定信息
- [ ] 5 个 shell 脚本都能正常运行
- [ ] 能用 vim 编辑文件
- [ ] 能解释管道和重定向的工作原理
- [ ] 能设置正确的文件权限

---

## Linux 命令速查表

### 文件操作
```bash
pwd                     # 显示当前目录
ls -la                  # 列出文件（含隐藏）
cd /path                # 切换目录
mkdir -p path/to/dir    # 创建目录
rm -rf dir              # 删除目录（谨慎！）
cp -r src dest          # 复制
mv src dest             # 移动/重命名
touch file              # 创建文件
```

### 文件查看
```bash
cat file                # 查看文件
head -n 10 file         # 查看前 10 行
tail -n 10 file         # 查看后 10 行
tail -f file            # 实时查看文件
less file               # 分页查看
```

### 权限管理
```bash
chmod 755 file          # 设置权限
chmod +x script.sh      # 添加执行权限
chown user:group file   # 修改所有者
ls -l                   # 查看权限
```

### 文本处理
```bash
grep "pattern" file     # 搜索
cut -d',' -f1 file      # 提取列
sort file               # 排序
uniq file               # 去重
wc -l file              # 统计行数
```

### 管道和重定向
```bash
cmd1 | cmd2             # 管道
cmd > file              # 覆盖重定向
cmd >> file             # 追加重定向
cmd 2>&1                # 错误重定向到输出
```

### 查找
```bash
find /path -name "*.py" # 按名称查找
find /path -size +10M   # 按大小查找
find /path -mtime -7    # 按时间查找
locate filename         # 快速查找
```

### 压缩
```bash
tar -czvf archive.tar.gz dir    # 压缩
tar -xzvf archive.tar.gz        # 解压
gzip file                       # gzip 压缩
zip -r archive.zip dir          # zip 压缩
unzip archive.zip               # 解压 zip
```

### Vim 基本操作
```vim
i          # 进入插入模式
Esc        # 退出插入模式
:w         # 保存
:q         # 退出
:q!        # 强制退出不保存
:wq        # 保存并退出
/pattern   # 搜索
:n         # 下一处匹配
dd         # 删除行
yy         # 复制行
p          # 粘贴
```

---

## 面试考点

### 高频面试题
1. Linux 目录结构是怎样的？
2. 如何查看文件后 100 行？
3. 如何查找占用磁盘最大的文件？
4. 如何查看进程并杀死？
5. chmod 755 代表什么含义？
6. 如何实时查看日志文件？
7. 管道和重定向的区别？

### 场景题
```bash
# 1. 从日志中找出访问最多的 10 个 IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 2. 查找大于 100M 的文件并删除
find /path -size +100M -delete

# 3. 统计当前目录下每个文件类型的数量
find . -type f | awk -F. '{print $NF}' | sort | uniq -c
```

---

## 每日学习检查清单

### Day 1-2: 文件操作
- [ ] 学习文件系统
- [ ] 完成 10 道文件操作题
- [ ] GitHub 提交（记录练习）

### Day 3-4: 权限 + 文本处理
- [ ] 学习权限管理
- [ ] 学习文本处理命令
- [ ] 完成日志分析
- [ ] GitHub 提交

### Day 5-6: 管道 + 查找 + 压缩
- [ ] 学习管道和重定向
- [ ] 学习查找命令
- [ ] 学习压缩命令
- [ ] 编写 5 个 shell 脚本
- [ ] GitHub 提交

### Day 7: 复习 + vim
- [ ] 学习 vim 基础
- [ ] 复习本周内容
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 5 周总结

### 学习内容
- 掌握了 Linux 基础命令
- 学会了文本处理
- 能编写 shell 脚本

### 遇到的问题
- vim 操作不熟练（已解决）
- 正则表达式理解困难（已解决）

### 脚本仓库
- GitHub 链接：...

### 下周改进
- ...
```
