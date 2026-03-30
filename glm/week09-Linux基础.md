# 第9周：Linux 基础

## 本周目标

掌握 Linux 基础命令，能在服务器上进行日常操作和问题排查。

---

## 一、学什么

| 主题 | 内容 | 重要性 |
|------|------|--------|
| 文件操作 | ls、cd、cp、mv、rm | ⭐⭐⭐⭐⭐ |
| 文件查看 | cat、less、head、tail | ⭐⭐⭐⭐⭐ |
| 权限管理 | chmod、chown | ⭐⭐⭐⭐ |
| 进程管理 | ps、top、kill | ⭐⭐⭐⭐⭐ |
| 日志查看 | grep、awk、sed | ⭐⭐⭐⭐⭐ |
| 网络命令 | curl、netstat、ssh | ⭐⭐⭐⭐ |
| Shell 脚本 | 基础语法 | ⭐⭐⭐ |

---

## 二、知识点详解

### 2.1 文件与目录操作

```bash
# ============================================
# 目录操作
# ============================================
# 查看当前目录
pwd

# 切换目录
cd /home/user      # 绝对路径
cd ./subdir        # 相对路径
cd ..              # 上级目录
cd ~               # 家目录
cd -               # 上一个目录

# 创建目录
mkdir dir1
mkdir -p dir1/dir2/dir3  # 创建多级目录

# 删除目录
rmdir dir1         # 删除空目录
rm -r dir1         # 删除目录及内容
rm -rf dir1        # 强制删除（不提示）

# ============================================
# 文件操作
# ============================================
# 列出文件
ls                 # 当前目录
ls -l              # 详细信息
ls -la             # 包含隐藏文件
ls -lh             # 人类可读大小
ls -lt             # 按时间排序

# 创建文件
touch file.txt
touch file{1..5}.txt  # 批量创建

# 复制文件
cp file1.txt file2.txt
cp -r dir1 dir2    # 复制目录
cp -p file1 file2  # 保留属性

# 移动/重命名
mv file1.txt file2.txt  # 重命名
mv file.txt /path/to/   # 移动
mv dir1 dir2            # 重命名目录

# 删除文件
rm file.txt
rm -i file.txt     # 交互式删除
rm -f file.txt     # 强制删除

# 查找文件
find /path -name "*.py"
find /path -type f -mtime -7  # 7天内修改的文件
find /path -size +100M        # 大于100M的文件

# ============================================
# 文件查看
# ============================================
# 显示全部
cat file.txt
cat -n file.txt    # 显示行号

# 分页查看
less file.txt
# 空格：下一页
# b：上一页
# /keyword：搜索
# q：退出

# 查看头部
head file.txt      # 前10行
head -n 20 file.txt  # 前20行

# 查看尾部
tail file.txt      # 后10行
tail -n 20 file.txt  # 后20行
tail -f log.txt    # 实时追踪（常用！）

# 查看文件信息
file file.txt
stat file.txt

# ============================================
# 文件编辑
# ============================================
# nano（简单编辑器）
nano file.txt

# vim（高级编辑器）
vim file.txt
# i：插入模式
# ESC：命令模式
# :w：保存
# :q：退出
# :wq：保存退出
# :q!：强制退出
# dd：删除一行
# /keyword：搜索
# :%s/old/new/g：替换
```

---

### 2.2 文件权限

```bash
# ============================================
# 权限说明
# ============================================
# ls -l 输出示例
# -rwxr-xr-x 1 user group 1234 Jan 1 10:00 file.txt
#  |        |  |    |     |
#  |        |  |    |     文件大小
#  |        |  |    所属组
#  |        |  所有者
#  |        链接数
#  权限

# 权限格式
# 第1位：-（文件）、d（目录）、l（链接）
# 后9位：3组权限（所有者、组、其他）
# r（读）= 4，w（写）= 2，x（执行）= 1

# ============================================
# 修改权限
# ============================================
# 数字方式
chmod 755 file.txt  # rwxr-xr-x
chmod 644 file.txt  # rw-r--r--
chmod 777 file.txt  # rwxrwxrwx（危险！）

# 符号方式
chmod u+x file.txt   # 所有者加执行权限
chmod g-w file.txt   # 组去掉写权限
chmod o+r file.txt   # 其他加读权限
chmod a+x file.txt   # 所有加执行权限

# 递归修改
chmod -R 755 /path/to/dir

# ============================================
# 修改所有者
# ============================================
# 修改所有者
chown user file.txt
chown user:group file.txt

# 递归修改
chown -R user:group /path/to/dir

# 修改组
chgrp group file.txt

# ============================================
# 特殊权限
# ============================================
# SUID（4）：以文件所有者身份执行
chmod u+s /usr/bin/passwd

# SGID（2）：以文件所属组身份执行
chmod g+s /path/to/dir

# Sticky bit（1）：只有所有者能删除
chmod +t /tmp
```

---

### 2.3 进程管理

```bash
# ============================================
# 查看进程
# ============================================
# ps 命令
ps                 # 当前终端进程
ps aux             # 所有进程
ps aux | grep python  # 过滤

# 输出说明
# USER  PID  %CPU %MEM VSZ  RSS  TTY  STAT START TIME COMMAND
# 用户  进程ID CPU 内存 虚拟 物理 终端 状态  开始  时间  命令

# top 命令（实时）
top
# P：按CPU排序
# M：按内存排序
# q：退出

# htop（更好用，需安装）
htop

# ============================================
# 后台运行
# ============================================
# 后台运行
python script.py &
nohup python script.py &  # 退出终端不停止

# 查看后台任务
jobs

# 调到前台
fg %1

# 调到后台
bg %1

# ============================================
# 杀进程
# ============================================
# 按 PID 杀
kill 1234
kill -9 1234       # 强制杀死

# 按名称杀
killall python
pkill -f "python script.py"

# ============================================
# 系统资源
# ============================================
# 内存
free -h

# 磁盘
df -h              # 文件系统
du -sh /path       # 目录大小
du -sh *           # 当前目录各文件大小

# CPU
lscpu
cat /proc/cpuinfo

# 系统信息
uname -a
cat /etc/os-release
```

---

### 2.4 文本处理

```bash
# ============================================
# grep - 文本搜索
# ============================================
# 基本搜索
grep "error" log.txt
grep -i "error" log.txt    # 忽略大小写
grep -r "error" /path/     # 递归搜索
grep -n "error" log.txt    # 显示行号
grep -c "error" log.txt    # 统计匹配行数
grep -v "error" log.txt    # 反向匹配
grep -E "error|warn" log.txt  # 正则

# 常用组合
grep -rn "TODO" ./         # 搜索代码中的 TODO
grep -r "error" --include="*.log" /path/  # 只搜索 .log 文件

# ============================================
# awk - 文本处理
# ============================================
# 基本用法
awk '{print $1}' file.txt      # 打印第1列
awk '{print $1, $3}' file.txt  # 打印第1和第3列
awk -F: '{print $1}' /etc/passwd  # 以:分隔

# 条件过滤
awk '$3 > 100 {print $0}' file.txt  # 第3列大于100

# 统计
awk '{sum += $1} END {print sum}' file.txt  # 求和
awk '{count++} END {print count}' file.txt  # 计数

# 实用示例
# 统计日志中各 IP 访问次数
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# ============================================
# sed - 流编辑器
# ============================================
# 替换
sed 's/old/new/' file.txt      # 替换每行第一个
sed 's/old/new/g' file.txt     # 替换所有
sed -i 's/old/new/g' file.txt  # 直接修改文件

# 删除
sed '/pattern/d' file.txt      # 删除匹配行
sed '1d' file.txt              # 删除第1行
sed '$d' file.txt              # 删除最后一行

# ============================================
# 其他常用
# ============================================
# 排序
sort file.txt
sort -r file.txt      # 倒序
sort -n file.txt      # 数字排序
sort -k2 file.txt     # 按第2列排序

# 去重
uniq file.txt         # 去除连续重复
sort file.txt | uniq  # 排序后去重
sort file.txt | uniq -c  # 统计出现次数

# 统计
wc file.txt           # 行数、单词数、字节数
wc -l file.txt        # 只统计行数

# 列操作
cut -d: -f1 /etc/passwd  # 以:分隔取第1列
cut -c1-5 file.txt       # 取每行1-5字符

# 合并
paste file1 file2     # 横向合并
cat file1 file2       # 纵向合并
```

---

### 2.5 网络命令

```bash
# ============================================
# 网络测试
# ============================================
# 测试连通性
ping google.com
ping -c 4 google.com  # 发送4个包

# 查看端口
netstat -tuln        # 监听的端口
netstat -an | grep 8080
ss -tuln             # 替代 netstat

# 测试端口
telnet localhost 8080
nc -zv localhost 8080

# DNS 查询
nslookup google.com
dig google.com
host google.com

# ============================================
# HTTP 请求
# ============================================
# curl 基本用法
curl http://example.com
curl -I http://example.com  # 只显示头部
curl -o file.html http://example.com  # 保存文件

# POST 请求
curl -X POST http://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'

# 带认证
curl -u user:pass http://example.com
curl -H "Authorization: Bearer token" http://example.com

# wget 下载
wget http://example.com/file.zip
wget -c http://example.com/file.zip  # 断点续传

# ============================================
# SSH
# ============================================
# 连接远程
ssh user@192.168.1.100
ssh -p 2222 user@host  # 指定端口

# 密钥登录
ssh-keygen -t rsa
ssh-copy-id user@host

# SCP 传输
scp file.txt user@host:/path/
scp -r dir/ user@host:/path/  # 目录

# SSH 隧道
ssh -L 8080:localhost:80 user@host  # 本地端口转发
```

---

### 2.6 日志查看

```bash
# ============================================
# 系统日志
# ============================================
# 系统日志位置
/var/log/messages    # 系统消息
/var/log/syslog      # 系统日志
/var/log/auth.log    # 认证日志
/var/log/nginx/      # Nginx 日志

# journalctl（systemd）
journalctl           # 所有日志
journalctl -u nginx  # 指定服务
journalctl -f        # 实时追踪
journalctl --since today  # 今天的日志
journalctl -p err    # 只看错误

# ============================================
# 日志分析技巧
# ============================================
# 实时查看
tail -f /var/log/nginx/access.log

# 搜索错误
grep -i error /var/log/nginx/error.log
grep -E "error|fail|critical" /var/log/app.log

# 统计状态码
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# 统计访问最多的 IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 统计某时间段的请求
awk '/2024-01-15 10:/' access.log | wc -l

# 查找慢请求
awk '$NF > 1 {print $0}' access.log  # 响应时间超过1秒
```

---

### 2.7 Shell 脚本基础

```bash
#!/bin/bash
# ============================================
# 基本语法
# ============================================

# 变量
NAME="张三"
echo "Hello, $NAME"
echo "Hello, ${NAME}"

# 特殊变量
$0    # 脚本名
$1    # 第1个参数
$#    # 参数个数
$@    # 所有参数
$?    # 上个命令退出码
$$    # 当前进程PID

# ============================================
# 条件判断
# ============================================
# if 语句
if [ -f "file.txt" ]; then
    echo "文件存在"
elif [ -d "dir" ]; then
    echo "目录存在"
else
    echo "不存在"
fi

# 文件测试
[ -f file ]    # 是否是文件
[ -d dir ]     # 是否是目录
[ -e path ]    # 是否存在
[ -r file ]    # 是否可读
[ -w file ]    # 是否可写
[ -x file ]    # 是否可执行
[ -s file ]    # 是否非空

# 字符串测试
[ -z "$str" ]  # 是否为空
[ -n "$str" ]  # 是否非空
[ "$a" = "$b" ]  # 是否相等

# 数字比较
[ $a -eq $b ]  # 相等
[ $a -ne $b ]  # 不等
[ $a -gt $b ]  # 大于
[ $a -lt $b ]  # 小于
[ $a -ge $b ]  # 大于等于
[ $a -le $b ]  # 小于等于

# ============================================
# 循环
# ============================================
# for 循环
for i in 1 2 3 4 5; do
    echo $i
done

for file in *.txt; do
    echo $file
done

for i in {1..10}; do
    echo $i
done

# while 循环
count=0
while [ $count -lt 5 ]; do
    echo $count
    count=$((count + 1))
done

# ============================================
# 函数
# ============================================
greet() {
    echo "Hello, $1"
}
greet "张三"

# ============================================
# 实用脚本示例
# ============================================
#!/bin/bash
# 日志分析脚本

LOG_FILE="/var/log/nginx/access.log"

echo "=== 访问统计 ==="
echo "总请求数：$(wc -l < $LOG_FILE)"
echo ""
echo "Top 10 IP："
awk '{print $1}' $LOG_FILE | sort | uniq -c | sort -rn | head -10
echo ""
echo "状态码统计："
awk '{print $9}' $LOG_FILE | sort | uniq -c | sort -rn
```

---

## 三、练习内容

### 基础练习（1-8）

---

#### 练习1：文件与目录基本操作

**场景说明**：你是一名测试工程师，需要在 Linux 服务器上创建测试环境目录结构，并进行基本的文件操作。

**具体需求**：
1. 在家目录下创建目录结构：`~/practice/linux/{dir1,dir2,dir3}`
2. 在 `dir1` 中创建文件 `file1.txt`，写入内容 `"Hello Linux"`
3. 将 `file1.txt` 复制到 `dir2` 目录
4. 将 `dir1/file1.txt` 移动到 `dir3` 并重命名为 `file3.txt`
5. 删除 `dir2` 目录及其内容

**使用示例**：
```bash
# 1. 创建目录结构
mkdir -p ~/practice/linux/{dir1,dir2,dir3}

# 2. 创建文件并写入内容
echo "Hello Linux" > ~/practice/linux/dir1/file1.txt

# 3. 复制文件到 dir2
cp ~/practice/linux/dir1/file1.txt ~/practice/linux/dir2/

# 4. 移动并重命名文件
mv ~/practice/linux/dir1/file1.txt ~/practice/linux/dir3/file3.txt

# 5. 删除 dir2 目录
rm -rf ~/practice/linux/dir2

# 6. 验证结果
ls -R ~/practice/linux/
# 输出应显示：
# /home/user/practice/linux/:
# dir1  dir3
#
# /home/user/practice/linux/dir1:
# (空)
#
# /home/user/practice/linux/dir3:
# file3.txt

cat ~/practice/linux/dir3/file3.txt
# 输出: Hello Linux
```

**验收标准**：
- [ ] 目录结构创建正确（使用 `ls -R` 验证）
- [ ] 文件内容正确（使用 `cat` 验证显示 `"Hello Linux"`）
- [ ] `dir2` 目录已删除
- [ ] `dir1` 目录为空
- [ ] `dir3` 目录包含 `file3.txt`

---

#### 练习2：文件查看与搜索

**场景说明**：你需要分析一个包含测试日志的文件，快速查看文件开头、结尾以及统计文件基本信息。

**具体需求**：
1. 创建一个包含 50 行内容的文件 `data.txt`，每行格式为 `"Line 1: 测试数据"` 到 `"Line 50: 测试数据"`
2. 使用 `head` 查看前 10 行
3. 使用 `tail` 查看后 10 行
4. 使用 `less` 分页浏览文件（熟悉快捷键）
5. 使用 `wc` 统计文件行数、单词数、字节数

**使用示例**：
```bash
# 1. 创建 50 行测试文件
for i in {1..50}; do echo "Line $i: 测试数据" >> data.txt; done

# 2. 查看前 10 行
head -n 10 data.txt
# 输出:
# Line 1: 测试数据
# Line 2: 测试数据
# ...
# Line 10: 测试数据

# 3. 查看后 10 行
tail -n 10 data.txt
# 输出:
# Line 41: 测试数据
# Line 42: 测试数据
# ...
# Line 50: 测试数据

# 4. 使用 less 分页浏览（按空格翻页，按 q 退出）
less data.txt

# 5. 统计文件信息
wc data.txt
# 输出: 50  150  650 data.txt
# 解释: 50行, 150个单词, 650字节

# 6. 只统计行数
wc -l data.txt
# 输出: 50 data.txt
```

**验收标准**：
- [ ] 文件创建成功，包含 50 行内容
- [ ] `head -n 10` 正确显示前 10 行
- [ ] `tail -n 10` 正确显示后 10 行
- [ ] 熟悉 `less` 基本快捷键（空格翻页、/搜索、q退出）
- [ ] 理解 `wc` 输出的三个数字含义

---

#### 练习3：文件权限管理

**场景说明**：你创建了一个 Shell 脚本用于自动化测试，需要设置正确的权限使其可执行，并理解 Linux 文件权限系统。

**具体需求**：
1. 创建文件 `script.sh`，内容为 `#!/bin/bash\necho "Hello World"`
2. 使用 `ls -l` 查看文件默认权限
3. 使用数字方式设置权限为 `755`（rwxr-xr-x）
4. 使用符号方式给其他用户添加读权限（`o+r`）
5. 修改文件所有者为当前用户

**使用示例**：
```bash
# 1. 创建脚本文件
echo '#!/bin/bash
echo "Hello World"' > script.sh

# 2. 查看默认权限
ls -l script.sh
# 输出示例: -rw-r--r-- 1 user group 0 Jan 1 10:00 script.sh

# 3. 使用数字方式设置权限为 755
chmod 755 script.sh
ls -l script.sh
# 输出: -rwxr-xr-x 1 user group 0 Jan 1 10:00 script.sh
# 解释: 所有者=rwx(7), 组=r-x(5), 其他=r-x(5)

# 4. 使用符号方式添加权限
chmod o+r script.sh  # 其他用户添加读权限
# 注意: 755 已经包含 o+r，这里演示语法

# 5. 执行脚本验证权限
./script.sh
# 输出: Hello World

# 权限说明:
# r = 4 (读)  w = 2 (写)  x = 1 (执行)
# 755 = 4+2+1, 4+1, 4+1 = rwxr-xr-x
```

**验收标准**：
- [ ] 文件创建成功，内容正确
- [ ] 能解释 `rwxr-xr-x` 每一位的含义
- [ ] 能将 `755` 转换为 `rwxr-xr-x`
- [ ] 文件可以被执行（`./script.sh` 运行成功）
- [ ] 理解符号方式 `u+x`、`g-w`、`o+r` 的含义

---

#### 练习4：进程管理基础

**场景说明**：作为测试工程师，你需要监控系统进程状态，并在必要时终止无响应的进程。

**具体需求**：
1. 使用 `ps aux` 查看所有进程
2. 使用 `ps aux | grep python` 筛选出包含 python 的进程
3. 使用 `top` 查看实时进程（按 CPU 排序，按 P 键）
4. 启动一个后台任务 `sleep 100 &`
5. 使用 `jobs` 查看后台任务
6. 使用 `kill` 终止后台任务

**使用示例**：
```bash
# 1. 查看所有进程
ps aux
# 输出示例:
# USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
# root         1  0.0  0.1 169424 11200 ?        Ss   10:00   0:01 /sbin/init
# user      1234  0.5  2.1 123456 78900 ?        S    10:05   0:03 python app.py

# 2. 筛选 Python 进程
ps aux | grep python
# 输出: user  1234  0.5  2.1 ... python app.py

# 3. 实时监控（按 q 退出）
top
# 按 P: 按 CPU 排序
# 按 M: 按内存排序
# 按 k: 输入 PID 杀进程

# 4. 启动后台任务
sleep 100 &
# 输出: [1] 5678  (5678 是进程 PID)

# 5. 查看后台任务
jobs
# 输出: [1]+  Running   sleep 100 &

# 6. 终止后台任务
kill %1
# 或者使用 PID: kill 5678
# 强制终止: kill -9 5678

# 7. 验证任务已终止
jobs
# 输出: [1]+  Terminated  sleep 100
```

**验收标准**：
- [ ] 能理解 `ps aux` 输出的各列含义（PID、%CPU、%MEM、COMMAND）
- [ ] 能使用管道配合 `grep` 筛选进程
- [ ] 能在 `top` 中按 CPU/内存排序
- [ ] 能正确启动后台任务（使用 `&`）
- [ ] 能使用 `jobs` 查看后台任务
- [ ] 能使用 `kill` 或 `kill -9` 终止进程

---

#### 练习5：grep 文本搜索

**场景说明**：你需要从应用日志中快速定位错误信息，这是测试工程师日常排查问题的必备技能。

**具体需求**：
1. 创建日志文件 `app.log`，包含多种级别的日志（error、warning、info）
2. 使用 `grep` 搜索所有包含 `"error"` 的行
3. 使用 `grep -i` 忽略大小写搜索 `"ERROR"`
4. 使用 `grep -c` 统计 error 出现的次数
5. 使用 `grep -v` 搜索不包含 `"info"` 的行
6. 使用 `grep -n` 显示行号

**使用示例**：
```bash
# 1. 创建测试日志文件
cat > app.log << 'EOF'
2024-01-15 10:00:01 [INFO] Application started
2024-01-15 10:00:02 [INFO] Loading configuration
2024-01-15 10:00:03 [WARNING] Config file not found, using defaults
2024-01-15 10:00:04 [INFO] Connecting to database
2024-01-15 10:00:05 [ERROR] Database connection failed
2024-01-15 10:00:06 [INFO] Retrying connection
2024-01-15 10:00:07 [ERROR] Max retries exceeded
2024-01-15 10:00:08 [info] Application shutdown
EOF

# 2. 搜索包含 "error" 的行（区分大小写）
grep "error" app.log
# 输出: 无匹配（因为日志中是 ERROR）

# 3. 忽略大小写搜索
grep -i "error" app.log
# 输出:
# 2024-01-15 10:00:05 [ERROR] Database connection failed
# 2024-01-15 10:00:07 [ERROR] Max retries exceeded

# 4. 统计匹配行数
grep -c -i "error" app.log
# 输出: 2

# 5. 搜索不包含 "info" 的行
grep -v -i "info" app.log
# 输出:
# 2024-01-15 10:00:03 [WARNING] Config file not found...
# 2024-01-15 10:00:05 [ERROR] Database connection failed
# 2024-01-15 10:00:07 [ERROR] Max retries exceeded

# 6. 显示行号
grep -n -i "error" app.log
# 输出:
# 5:2024-01-15 10:00:05 [ERROR] Database connection failed
# 7:2024-01-15 10:00:07 [ERROR] Max retries exceeded

# 7. 使用正则表达式
grep -E "ERROR|WARNING" app.log
# 输出所有包含 ERROR 或 WARNING 的行
```

**验收标准**：
- [ ] 能使用 `grep` 进行基本搜索
- [ ] 理解 `-i`（忽略大小写）的作用
- [ ] 能使用 `-c` 统计匹配次数
- [ ] 能使用 `-v` 反向匹配
- [ ] 能使用 `-n` 显示行号
- [ ] 能使用 `-E` 进行正则表达式搜索

---

#### 练习6：查找文件

**场景说明**：你需要快速定位服务器上的特定文件，例如查找测试报告、日志文件或大文件。

**具体需求**：
1. 在当前目录下查找所有 `.txt` 文件
2. 查找 7 天内修改过的文件
3. 查找大于 1M 的文件
4. 查找属于当前用户的文件
5. 查找并删除所有 `.tmp` 文件

**使用示例**：
```bash
# 准备测试文件
mkdir -p test_dir && cd test_dir
touch file1.txt file2.txt file3.log temp1.tmp temp2.tmp
dd if=/dev/zero of=large_file.bin bs=1M count=5  # 创建5MB文件

# 1. 查找所有 .txt 文件
find . -name "*.txt"
# 输出:
# ./file1.txt
# ./file2.txt

# 2. 查找 7 天内修改过的文件
find . -mtime -7
# 输出所有7天内修改的文件

# 3. 查找大于 1M 的文件
find . -size +1M
# 输出:
# ./large_file.bin

# 4. 查找属于当前用户的文件
find . -user $USER
# 输出当前用户的所有文件

# 5. 查找并删除所有 .tmp 文件
find . -name "*.tmp" -type f
# 先查看要删除的文件:
# ./temp1.tmp
# ./temp2.tmp

find . -name "*.tmp" -type f -delete
# 删除所有 .tmp 文件

ls *.tmp 2>/dev/null
# 输出: 无（已删除）

# 常用 find 组合:
# 查找并执行命令
find . -name "*.log" -exec ls -lh {} \;

# 查找空文件
find . -empty

# 查找目录
find . -type d
```

**验收标准**：
- [ ] 能使用 `-name` 按文件名查找
- [ ] 能使用 `-mtime` 按修改时间查找
- [ ] 能使用 `-size` 按文件大小查找
- [ ] 能使用 `-type` 按文件类型查找
- [ ] 能使用 `-delete` 或 `-exec` 对查找结果执行操作

---

#### 练习7：网络基础命令

**场景说明**：你需要诊断网络连接问题，并通过命令行测试 API 接口的连通性。

**具体需求**：
1. 使用 `ping` 测试与 `google.com` 的连通性（发送 4 个包）
2. 使用 `curl` 获取 `http://httpbin.org/get` 的响应
3. 发送 POST 请求到 `http://httpbin.org/post`，携带 JSON 数据
4. 使用 `netstat` 或 `ss` 查看当前监听的端口
5. 查看本机 DNS 配置（`/etc/resolv.conf`）

**使用示例**：
```bash
# 1. 测试网络连通性
ping -c 4 google.com
# 输出示例:
# PING google.com (142.250.185.78): 56 data bytes
# 64 bytes from 142.250.185.78: icmp_seq=0 ttl=117 time=15.2 ms
# ...
# --- google.com ping statistics ---
# 4 packets transmitted, 4 packets received, 0.0% packet loss

# 2. 发送 GET 请求
curl http://httpbin.org/get
# 输出 JSON 响应

# 3. 发送 POST 请求（携带 JSON 数据）
curl -X POST http://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 123}'
# 输出:
# {
#   "args": {},
#   "data": "{\"name\": \"test\", \"value\": 123}",
#   "json": {"name": "test", "value": 123},
#   ...
# }

# 4. 查看监听端口
netstat -tuln
# 或使用 ss
ss -tuln
# 输出示例:
# Proto Recv-Q Send-Q Local Address  Foreign Address  State
# tcp   0      0      0.0.0.0:22     0.0.0.0:*        LISTEN
# tcp   0      0      127.0.0.1:3306 0.0.0.0:*        LISTEN

# 5. 查看 DNS 配置
cat /etc/resolv.conf
# 输出示例:
# nameserver 8.8.8.8
# nameserver 8.8.4.4

# 6. 只显示 HTTP 响应头
curl -I http://httpbin.org/get
# 输出:
# HTTP/1.1 200 OK
# Content-Type: application/json
# ...
```

**验收标准**：
- [ ] 能使用 `ping -c` 测试网络连通性
- [ ] 能使用 `curl` 发送 GET 请求
- [ ] 能使用 `curl -X POST -H -d` 发送带 JSON 的 POST 请求
- [ ] 能使用 `netstat -tuln` 或 `ss -tuln` 查看监听端口
- [ ] 理解 `/etc/resolv.conf` 的作用

---

#### 练习8：系统资源监控

**场景说明**：作为测试工程师，你需要监控系统资源使用情况，以便在性能测试时分析系统瓶颈。

**具体需求**：
1. 使用 `free` 查看内存使用情况
2. 使用 `df` 查看磁盘使用情况
3. 使用 `du` 查看当前目录大小
4. 使用 `top` 观察系统负载
5. 查看系统版本信息

**使用示例**：
```bash
# 1. 查看内存使用情况
free -h
# 输出示例:
#               total        used        free      shared  buff/cache   available
# Mem:           7.7G        2.1G        3.2G        256M        2.4G        5.1G
# Swap:          2.0G          0B        2.0G
# 解释: -h 以人类可读格式显示

# 2. 查看磁盘使用情况
df -h
# 输出示例:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1       100G   30G   70G  30% /
# /dev/sda2       500G  150G  350G  30% /home

# 3. 查看目录大小
du -sh .
# 输出: 150M    .

du -sh *
# 输出各子目录大小:
# 50M     dir1
# 30M     dir2
# 70M     dir3

# 4. 实时监控系统
top
# 常用快捷键:
# P - 按 CPU 使用率排序
# M - 按内存使用率排序
# q - 退出

# 或者使用 htop（更友好，需安装）
htop

# 5. 查看系统版本
cat /etc/os-release
# 输出示例:
# NAME="Ubuntu"
# VERSION="20.04.3 LTS (Focal Fossa)"
# ID=ubuntu
# ID_LIKE=debian

# 查看内核版本
uname -a
# 输出: Linux hostname 5.4.0-90-generic #101-Ubuntu SMP x86_64 GNU/Linux
```

**验收标准**：
- [ ] 能使用 `free -h` 查看内存信息
- [ ] 能使用 `df -h` 查看磁盘使用情况
- [ ] 能使用 `du -sh` 查看目录大小
- [ ] 熟悉 `top` 的基本操作（排序、退出）
- [ ] 能查看系统版本和内核信息

---

### 进阶练习（9-16）

---

#### 练习9：awk 文本处理

**场景说明**：你需要从 CSV 格式的测试数据文件中提取和统计数据，用于分析测试结果。

**具体需求**：
创建 CSV 文件 `users.csv`，内容如下：
```
name,age,salary
Alice,25,5000
Bob,30,6000
Charlie,28,5500
```

1. 打印所有姓名（第一列，跳过标题行）
2. 打印年龄大于 26 的行
3. 计算平均工资
4. 格式化输出：`姓名: xxx, 年龄: xxx`
5. 统计记录数量

**使用示例**：
```bash
# 创建测试文件
cat > users.csv << 'EOF'
name,age,salary
Alice,25,5000
Bob,30,6000
Charlie,28,5500
EOF

# 1. 打印所有姓名（跳过第一行标题）
awk 'NR>1 {print $1}' users.csv
# 输出:
# Alice
# Bob
# Charlie

# 2. 打印年龄大于 26 的行
awk -F',' 'NR>1 && $2 > 26 {print $0}' users.csv
# 输出:
# Bob,30,6000
# Charlie,28,5500

# 3. 计算平均工资
awk -F',' 'NR>1 {sum+=$3; count++} END {print "平均工资:", sum/count}' users.csv
# 输出: 平均工资: 5500

# 4. 格式化输出
awk -F',' 'NR>1 {printf "姓名: %s, 年龄: %s\n", $1, $2}' users.csv
# 输出:
# 姓名: Alice, 年龄: 25
# 姓名: Bob, 年龄: 30
# 姓名: Charlie, 年龄: 28

# 5. 统计记录数量
awk -F',' 'NR>1 {count++} END {print "记录数:", count}' users.csv
# 输出: 记录数: 3

# 6. 使用默认分隔符处理空格分隔的文件
echo "hello world test" | awk '{print $2}'
# 输出: world
```

**验收标准**：
- [ ] 能使用 `-F` 指定分隔符
- [ ] 能使用 `$1`、`$2` 访问列
- [ ] 能使用 `NR>1` 跳过标题行
- [ ] 能使用 `END` 块进行统计
- [ ] 能使用 `printf` 格式化输出

---

#### 练习10：sed 流编辑器

**场景说明**：你需要批量修改配置文件，例如将测试环境的配置替换为生产环境配置。

**具体需求**：
创建配置文件 `config.txt`：
1. 将所有 `"localhost"` 替换为 `"127.0.0.1"`
2. 删除空行
3. 删除包含 `"#"` 注释的行
4. 在文件开头添加一行 `"# Configuration"`
5. 只打印修改后的第 5 到 10 行

**使用示例**：
```bash
# 创建测试配置文件
cat > config.txt << 'EOF'
# Database Configuration
db_host=localhost
db_port=3306

# API Configuration
api_host=localhost
api_port=8080

# Cache Configuration
cache_host=localhost
cache_port=6379
EOF

# 1. 替换 localhost 为 127.0.0.1（只打印，不修改文件）
sed 's/localhost/127.0.0.1/g' config.txt

# 2. 直接修改文件（-i 选项）
sed -i 's/localhost/127.0.0.1/g' config.txt
# macOS 需要指定备份后缀或空字符串:
# sed -i '' 's/localhost/127.0.0.1/g' config.txt

# 3. 删除空行
sed '/^$/d' config.txt
# 解释:
# /^$/  匹配空行（行首和行尾之间没有字符）
# d     删除匹配的行

# 4. 删除注释行
sed '/#/d' config.txt
# 删除以 # 开头的行
sed '/^[[:space:]]*#/d' config.txt

# 5. 在文件开头添加一行
sed '1i # Configuration' config.txt
# 1i 表示在第一行之前插入

# 6. 只打印第 5 到 10 行
sed -n '5,10p' config.txt
# -n 抑制默认输出
# 5,10p 打印第 5 到 10 行

# 7. 组合多个操作
sed -e 's/localhost/127.0.0.1/g' -e '/^$/d' -e '/#/d' config.txt

# 8. 替换每行第一个匹配
sed 's/o/X/' config.txt
# 只替换每行的第一个 o

# 替换所有匹配
sed 's/o/X/g' config.txt
# 替换每行的所有 o
```

**验收标准**：
- [ ] 能使用 `s/old/new/g` 进行替换
- [ ] 能使用 `-i` 直接修改文件
- [ ] 能使用 `/pattern/d` 删除匹配行
- [ ] 能使用 `-n '5,10p'` 打印指定行
- [ ] 能使用 `-e` 组合多个操作

---

#### 练习11：管道与重定向

**场景说明**：你需要组合多个命令来处理复杂的任务，并将结果保存到文件或过滤输出。

**具体需求**：
1. 将 `ls -la` 的输出重定向到文件 `list.txt`
2. 将错误输出重定向到 `/dev/null`
3. 使用管道组合命令：查找所有 `.py` 文件并统计行数
4. 使用管道：`ps aux | grep python | awk '{print $2}'`
5. 将命令输出同时显示和保存到文件

**使用示例**：
```bash
# 1. 输出重定向到文件（覆盖）
ls -la > list.txt
# > 会覆盖已有文件

# 追加到文件
ls -la >> list.txt
# >> 在文件末尾追加

# 2. 错误输出重定向
ls /nonexistent 2>/dev/null
# 2> 重定向标准错误
# /dev/null 是一个特殊文件，丢弃所有输入

# 同时重定向标准输出和错误
ls /nonexistent > output.txt 2>&1
# 2>&1 将标准错误重定向到标准输出

# 或使用更简洁的语法（bash）
ls /nonexistent &> output.txt

# 3. 管道组合命令
# 查找所有 .py 文件并统计总行数
find . -name "*.py" -exec cat {} \; | wc -l

# 或者使用 xargs
find . -name "*.py" | xargs cat | wc -l

# 4. 多级管道
# 查找 python 进程并提取 PID
ps aux | grep python | grep -v grep | awk '{print $2}'
# grep -v grep 排除 grep 自身的进程

# 统计当前目录下各类型文件数量
ls -l | awk '{print $NF}' | grep -o '\.[^.]*$' | sort | uniq -c

# 5. 同时输出到屏幕和文件（tee）
ls -la | tee list.txt
# tee 会将输入同时输出到屏幕和文件

# 追加模式
ls -la | tee -a list.txt

# 6. 输入重定向
# 从文件读取输入
wc -l < list.txt

# Here Document（多行输入）
cat << 'EOF'
这是一个
多行
文本
EOF

# 7. 组合示例：分析访问日志
# 统计访问最多的 10 个 IP
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

**验收标准**：
- [ ] 理解 `>`（覆盖）和 `>>`（追加）的区别
- [ ] 能使用 `2>/dev/null` 丢弃错误输出
- [ ] 能使用 `|` 组合多个命令
- [ ] 能使用 `tee` 同时输出到屏幕和文件
- [ ] 能使用 Here Document 输入多行文本

---

#### 练习12：Shell 脚本基础

**场景说明**：你需要编写一个备份脚本，用于定期备份测试报告目录。

**具体需求**：
编写脚本 `backup.sh`，实现以下功能：
1. 接收一个目录参数
2. 检查目录是否存在
3. 创建备份文件（添加时间戳）
4. 输出备份结果
5. 处理错误情况（如参数缺失、目录不存在等）

**使用示例**：
```bash
#!/bin/bash
# backup.sh - 目录备份脚本

# ============================================
# 参数检查
# ============================================
if [ $# -eq 0 ]; then
    echo "错误: 缺少目录参数"
    echo "用法: $0 <目录路径>"
    exit 1
fi

SOURCE_DIR="$1"

# ============================================
# 目录检查
# ============================================
if [ ! -d "$SOURCE_DIR" ]; then
    echo "错误: 目录不存在: $SOURCE_DIR"
    exit 1
fi

# ============================================
# 创建备份
# ============================================
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.tar.gz"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 创建备份
echo "开始备份: $SOURCE_DIR"
tar -czf "$BACKUP_FILE" "$SOURCE_DIR" 2>/dev/null

# ============================================
# 结果检查
# ============================================
if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "备份成功!"
    echo "备份文件: $BACKUP_FILE"
    echo "文件大小: $BACKUP_SIZE"
else
    echo "错误: 备份失败"
    exit 1
fi
```

**测试运行**：
```bash
# 1. 添加执行权限
chmod +x backup.sh

# 2. 创建测试目录
mkdir -p test_reports
echo "测试报告1" > test_reports/report1.txt
echo "测试报告2" > test_reports/report2.txt

# 3. 运行备份脚本
./backup.sh test_reports
# 输出:
# 开始备份: test_reports
# 备份成功!
# 备份文件: ./backups/backup_20240115_103045.tar.gz
# 文件大小: 1K

# 4. 测试错误情况
./backup.sh
# 输出: 错误: 缺少目录参数

./backup.sh /nonexistent
# 输出: 错误: 目录不存在: /nonexistent

# 5. 验证备份
tar -tzf ./backups/backup_*.tar.gz
# 列出备份内容
```

**验收标准**：
- [ ] 脚本正确处理参数缺失情况
- [ ] 脚本正确处理目录不存在情况
- [ ] 备份文件名包含时间戳
- [ ] 备份成功后显示文件大小
- [ ] 错误时返回非零退出码

---

#### 练习13：Shell 条件判断

**场景说明**：你需要编写一个文件检查脚本，用于验证测试环境中的文件状态。

**具体需求**：
编写脚本 `check_file.sh`：
1. 接收一个文件路径参数
2. 判断文件是否存在
3. 判断是文件还是目录
4. 判断是否可读、可写、可执行
5. 输出详细信息

**使用示例**：
```bash
#!/bin/bash
# check_file.sh - 文件检查脚本

FILE="$1"

# 参数检查
if [ -z "$FILE" ]; then
    echo "用法: $0 <文件路径>"
    exit 1
fi

echo "检查: $FILE"
echo "===================="

# 存在性检查
if [ -e "$FILE" ]; then
    echo "✓ 文件存在"
else
    echo "✗ 文件不存在"
    exit 1
fi

# 类型检查
if [ -f "$FILE" ]; then
    echo "✓ 类型: 普通文件"
elif [ -d "$FILE" ]; then
    echo "✓ 类型: 目录"
elif [ -L "$FILE" ]; then
    echo "✓ 类型: 符号链接"
else
    echo "? 类型: 其他"
fi

# 权限检查
if [ -r "$FILE" ]; then
    echo "✓ 可读"
else
    echo "✗ 不可读"
fi

if [ -w "$FILE" ]; then
    echo "✓ 可写"
else
    echo "✗ 不可写"
fi

if [ -x "$FILE" ]; then
    echo "✓ 可执行"
else
    echo "✗ 不可执行"
fi

# 文件大小
if [ -f "$FILE" ]; then
    SIZE=$(du -h "$FILE" | cut -f1)
    echo "大小: $SIZE"
fi

# 修改时间
MOD_TIME=$(stat -c %y "$FILE" 2>/dev/null || stat -f "%Sm" "$FILE")
echo "修改时间: $MOD_TIME"
```

**测试运行**：
```bash
# 添加执行权限
chmod +x check_file.sh

# 测试普通文件
touch test.txt
./check_file.sh test.txt
# 输出:
# 检查: test.txt
# ====================
# ✓ 文件存在
# ✓ 类型: 普通文件
# ✓ 可读
# ✓ 可写
# ✗ 不可执行
# 大小: 0B
# 修改时间: ...

# 测试目录
mkdir test_dir
./check_file.sh test_dir
# 输出:
# ✓ 类型: 目录
# ✓ 可执行

# 测试不存在的文件
./check_file.sh /nonexistent
# 输出: ✗ 文件不存在
```

**验收标准**：
- [ ] 正确判断文件/目录类型
- [ ] 正确判断读/写/执行权限
- [ ] 显示文件大小和修改时间
- [ ] 处理文件不存在的情况

---

#### 练习14：Shell 循环

**场景说明**：在自动化测试和运维工作中，经常需要批量处理文件，如压缩日志、批量重命名等。掌握 Shell 循环是必备技能。

**具体需求**：
编写脚本 `batch_process.sh`，实现以下功能：
1. 遍历当前目录下所有 `.log` 文件
2. 对每个文件进行 gzip 压缩
3. 统计处理的文件数量
4. 输出处理结果
5. 将结果写入日志文件

**使用示例**：
```bash
#!/bin/bash
# batch_process.sh - 批量处理日志文件

# ============================================
# 参数配置
# ============================================
LOG_DIR="${1:-.}"  # 默认当前目录
OUTPUT_LOG="process.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# ============================================
# 初始化
# ============================================
echo "[$TIMESTAMP] 开始批量处理日志文件..." | tee -a "$OUTPUT_LOG"
echo "目标目录: $LOG_DIR" | tee -a "$OUTPUT_LOG"

# ============================================
# 方法1：for 循环遍历文件
# ============================================
count=0
failed=0

for logfile in "$LOG_DIR"/*.log; do
    # 检查文件是否存在（没有匹配时 *.log 不会展开）
    if [ ! -f "$logfile" ]; then
        echo "没有找到 .log 文件"
        exit 0
    fi

    filename=$(basename "$logfile")
    echo "处理文件: $filename"

    # 压缩文件
    if gzip "$logfile"; then
        echo "  ✅ 压缩成功: ${filename}.gz"
        ((count++))
    else
        echo "  ❌ 压缩失败: $filename"
        ((failed++))
    fi
done

# ============================================
# 方法2：while 循环读取列表
# ============================================
# find . -name "*.log" | while read file; do
#     echo "处理: $file"
#     gzip "$file"
# done

# ============================================
# 方法3：for 循环使用命令替换
# ============================================
# for file in $(find . -name "*.log"); do
#     gzip "$file"
# done

# ============================================
# 输出统计结果
# ============================================
echo "" | tee -a "$OUTPUT_LOG"
echo "========== 处理完成 ==========" | tee -a "$OUTPUT_LOG"
echo "成功: $count 个文件" | tee -a "$OUTPUT_LOG"
echo "失败: $failed 个文件" | tee -a "$OUTPUT_LOG"
echo "详情请查看: $OUTPUT_LOG"

# ============================================
# 更多循环示例
# ============================================
# for 循环：数字范围
for i in {1..5}; do
    echo "数字: $i"
done

# for 循环：列表
for item in apple banana cherry; do
    echo "水果: $item"
done

# while 循环：计数器
counter=0
while [ $counter -lt 5 ]; do
    echo "计数: $counter"
    ((counter++))
done

# while 循环：读取文件
while IFS= read -r line; do
    echo "行: $line"
done < data.txt

# until 循环：直到条件成立
count=0
until [ $count -ge 5 ]; do
    echo "until 循环: $count"
    ((count++))
done

# 嵌套循环
for i in 1 2 3; do
    for j in a b c; do
        echo "$i$j"
    done
done

# 循环控制
for i in {1..10}; do
    if [ $i -eq 3 ]; then
        continue  # 跳过 3
    fi
    if [ $i -eq 7 ]; then
        break  # 在 7 时退出
    fi
    echo "i = $i"
done
```

**验收标准**：
- [ ] 能正确使用 for 循环遍历文件
- [ ] 能正确使用 while 循环读取文件
- [ ] 能在循环中进行条件判断
- [ ] 能统计循环处理的数量
- [ ] 理解 continue 和 break 的作用

#### 练习15：日志分析实战

**场景说明**：日志分析是测试工程师和运维人员的日常工作，通过分析访问日志可以了解系统运行状况、发现异常、优化性能。

**具体需求**：
创建模拟 Nginx 访问日志 `access.log`，然后进行以下分析：
1. 统计总请求数
2. 统计各状态码数量（200、404、500 等）
3. 找出访问最多的前 10 个 IP
4. 找出响应时间最慢的 10 个请求
5. 统计某时间段的请求数

**使用示例**：
```bash
# ============================================
# 1. 创建模拟日志文件
# ============================================
cat > access.log << 'EOF'
192.168.1.1 - - [15/Jan/2024:10:00:01 +0800] "GET /index.html HTTP/1.1" 200 1234 0.050
192.168.1.2 - - [15/Jan/2024:10:00:02 +0800] "GET /api/users HTTP/1.1" 200 5678 0.120
192.168.1.1 - - [15/Jan/2024:10:00:03 +0800] "POST /api/login HTTP/1.1" 200 234 0.200
192.168.1.3 - - [15/Jan/2024:10:00:04 +0800] "GET /api/products HTTP/1.1" 404 0 0.010
192.168.1.2 - - [15/Jan/2024:10:00:05 +0800] "GET /index.html HTTP/1.1" 200 1234 0.060
192.168.1.4 - - [15/Jan/2024:10:00:06 +0800] "GET /api/orders HTTP/1.1" 500 0 1.500
192.168.1.1 - - [15/Jan/2024:10:00:07 +0800] "DELETE /api/user/1 HTTP/1.1" 403 0 0.030
192.168.1.5 - - [15/Jan/2024:10:00:08 +0800] "GET /api/users HTTP/1.1" 200 5678 0.150
192.168.1.2 - - [15/Jan/2024:10:00:09 +0800] "GET /api/products HTTP/1.1" 200 8900 0.080
192.168.1.3 - - [15/Jan/2024:10:00:10 +0800] "POST /api/orders HTTP/1.1" 201 456 2.000
EOF

# 日志格式说明：
# IP - - [时间] "请求方法 路径 协议" 状态码 响应大小 响应时间

# ============================================
# 2. 统计总请求数
# ============================================
echo "=== 总请求数 ==="
wc -l access.log
# 或
awk 'END {print NR " 次请求"}' access.log

# ============================================
# 3. 统计各状态码数量
# ============================================
echo ""
echo "=== 状态码统计 ==="
awk '{print $9}' access.log | sort | uniq -c | sort -rn
# 输出:
#       5 200
#       1 201
#       1 403
#       1 404
#       1 500

# 解释：
# $9 是第9列（状态码）
# sort 排序
# uniq -c 统计出现次数
# sort -rn 按数字倒序

# ============================================
# 4. 找出访问最多的前 10 个 IP
# ============================================
echo ""
echo "=== Top 10 IP ==="
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
# 输出:
#       3 192.168.1.1
#       3 192.168.1.2
#       2 192.168.1.3
#       1 192.168.1.4
#       1 192.168.1.5

# ============================================
# 5. 找出响应时间最慢的 10 个请求
# ============================================
echo ""
echo "=== 响应最慢的 10 个请求 ==="
# 假设响应时间在最后一列（$NF）
awk '{print $NF, $7}' access.log | sort -rn | head -10
# 输出:
# 2.000 /api/orders
# 1.500 /api/orders
# 0.200 /api/login
# 0.150 /api/users
# ...

# ============================================
# 6. 统计某时间段的请求数
# ============================================
echo ""
echo "=== 10:00:05 到 10:00:10 之间的请求 ==="
awk '/10:00:0[5-9]/ || /10:00:10/' access.log | wc -l

# 或者更精确的时间范围
awk '$4 >= "[15/Jan/2024:10:00:05" && $4 <= "[15/Jan/2024:10:00:10"' access.log | wc -l

# ============================================
# 7. 统计访问最多的 URL
# ============================================
echo ""
echo "=== Top 10 URL ==="
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -10
# 输出:
#       2 /api/users
#       2 /api/products
#       ...

# ============================================
# 8. 分析错误请求（状态码 >= 400）
# ============================================
echo ""
echo "=== 错误请求分析 ==="
awk '$9 >= 400 {print $1, $7, $9}' access.log
# 输出:
# 192.168.1.3 /api/products 404
# 192.168.1.4 /api/orders 500
# 192.168.1.1 /api/user/1 403

# ============================================
# 9. 计算平均响应时间
# ============================================
echo ""
echo "=== 平均响应时间 ==="
awk '{sum+=$NF; count++} END {print "平均响应时间:", sum/count, "秒"}' access.log

# ============================================
# 10. 综合分析脚本
# ============================================
cat > analyze_log.sh << 'SCRIPT'
#!/bin/bash
LOG_FILE="${1:-access.log}"

echo "========== 日志分析报告 =========="
echo "日志文件: $LOG_FILE"
echo "分析时间: $(date)"
echo ""

echo "1. 总体统计"
echo "   总请求数: $(wc -l < $LOG_FILE)"
echo "   唯一IP数: $(awk '{print $1}' $LOG_FILE | sort -u | wc -l)"
echo ""

echo "2. 状态码分布"
awk '{count[$9]++} END {for (code in count) print "   " code ": " count[code]}' $LOG_FILE | sort
echo ""

echo "3. Top 5 访问IP"
awk '{print $1}' $LOG_FILE | sort | uniq -c | sort -rn | head -5 | awk '{print "   " $2 ": " $1 " 次"}'
echo ""

echo "4. 错误请求 (4xx/5xx)"
awk '$9 >= 400 {print "   " $1 " -> " $7 " (" $9 ")"}' $LOG_FILE
echo ""

echo "5. 响应时间统计"
awk '{sum+=$NF; if($NF>max)max=$NF} END {print "   平均: " sum/NR "秒, 最大: " max "秒"}' $LOG_FILE

echo ""
echo "========== 分析完成 =========="
SCRIPT

chmod +x analyze_log.sh
./analyze_log.sh access.log
```

**验收标准**：
- [ ] 能使用 awk 提取日志中的特定字段
- [ ] 能使用 sort、uniq、head 组合进行统计分析
- [ ] 能统计状态码分布
- [ ] 能找出访问最多的 IP 和 URL
- [ ] 能分析响应时间和错误请求

#### 练习16：SSH 远程操作

**场景说明**：作为测试工程师，经常需要连接远程服务器进行测试环境部署、日志查看、问题排查等操作。掌握 SSH 是必备技能。

**具体需求**：
1. 生成 SSH 密钥对（公钥和私钥）
2. 将公钥复制到远程服务器（或本地模拟测试）
3. 使用 SSH 执行远程命令
4. 使用 SCP 传输文件
5. 配置 SSH 别名简化连接

**使用示例**：
```bash
# ============================================
# 1. 生成 SSH 密钥对
# ============================================
# 生成 RSA 密钥（默认 2048 位）
ssh-keygen -t rsa

# 生成更安全的 ED25519 密钥（推荐）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 交互过程：
# Enter file to save the key: 按 Enter 使用默认路径
# Enter passphrase: 可以设置密码保护私钥（可选）
# Enter same passphrase again: 再次确认

# 查看生成的密钥
ls -la ~/.ssh/
# id_rsa      - 私钥（保密！）
# id_rsa.pub  - 公钥（需要复制到服务器）
# known_hosts - 已知主机列表

# ============================================
# 2. 将公钥复制到远程服务器
# ============================================
# 方法1：使用 ssh-copy-id（推荐）
ssh-copy-id user@192.168.1.100

# 指定端口
ssh-copy-id -p 2222 user@192.168.1.100

# 方法2：手动复制
cat ~/.ssh/id_rsa.pub | ssh user@192.168.1.100 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# 方法3：手动复制（分步）
# 1. 在本地查看公钥
cat ~/.ssh/id_rsa.pub
# 2. 登录远程服务器
ssh user@192.168.1.100
# 3. 添加公钥
mkdir -p ~/.ssh
echo "ssh-rsa AAAA... user@host" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# ============================================
# 3. SSH 基本连接
# ============================================
# 基本连接
ssh user@192.168.1.100

# 指定端口
ssh -p 2222 user@192.168.1.100

# 使用特定私钥
ssh -i ~/.ssh/my_key user@192.168.1.100

# ============================================
# 4. 执行远程命令（不登录）
# ============================================
# 在远程服务器执行单个命令
ssh user@192.168.1.100 "ls -la"

# 执行多个命令
ssh user@192.168.1.100 "cd /var/log && ls -la && tail nginx.log"

# 使用 here document 执行多行命令
ssh user@192.168.1.100 << 'EOF'
    cd /var/log
    echo "当前目录: $(pwd)"
    ls -la
    tail -20 nginx/access.log
EOF

# 执行脚本
ssh user@192.168.1.100 'bash -s' < local_script.sh

# ============================================
# 5. SCP 文件传输
# ============================================
# 上传文件到远程
scp local_file.txt user@192.168.1.100:/remote/path/

# 上传目录（-r 递归）
scp -r local_dir/ user@192.168.1.100:/remote/path/

# 从远程下载文件
scp user@192.168.1.100:/remote/path/file.txt ./local/

# 从远程下载目录
scp -r user@192.168.1.100:/remote/path/ ./local/

# 指定端口
scp -P 2222 file.txt user@192.168.1.100:/path/

# 显示传输进度
scp -v file.txt user@192.168.1.100:/path/

# ============================================
# 6. 配置 SSH 别名
# ============================================
# 编辑配置文件
vim ~/.ssh/config

# 添加主机配置
Host dev
    HostName 192.168.1.100
    User developer
    Port 22
    IdentityFile ~/.ssh/id_rsa

Host prod
    HostName 192.168.1.200
    User admin
    Port 2222
    IdentityFile ~/.ssh/prod_key

Host jump
    HostName jump.example.com
    User jumpuser
    ProxyJump dev  # 通过 dev 跳转

# 使用别名连接
ssh dev
ssh prod
ssh jump

# 使用别名传输文件
scp file.txt dev:/path/
scp -r dev:/var/log/ ./logs/

# ============================================
# 7. SSH 隧道
# ============================================
# 本地端口转发
# 将本地 8080 端口转发到远程的 80 端口
ssh -L 8080:localhost:80 user@192.168.1.100

# 访问远程内网服务
# 将本地 3306 转发到远程内网的数据库服务器
ssh -L 3306:10.0.0.5:3306 user@192.168.1.100

# 远程端口转发
ssh -R 8080:localhost:80 user@192.168.1.100

# 动态端口转发（SOCKS 代理）
ssh -D 1080 user@192.168.1.100

# ============================================
# 8. SSH 高级用法
# ============================================
# 保持连接（防止断开）
ssh -o ServerAliveInterval=60 user@192.168.1.100

# 后台运行
ssh -f user@192.168.1.100 "sleep 100"

# 压缩传输
ssh -C user@192.168.1.100

# X11 转发（图形界面）
ssh -X user@192.168.1.100

# 使用 rsync 同步文件（比 scp 更高效）
rsync -avz local_dir/ user@192.168.1.100:/remote/path/
```

**验收标准**：
- [ ] 能生成 SSH 密钥对
- [ ] 能将公钥复制到远程服务器实现免密登录
- [ ] 能使用 SSH 执行远程命令
- [ ] 能使用 SCP 传输文件和目录
- [ ] 能配置 SSH 别名简化连接

### 综合练习（17-20）

---

#### 练习17：系统巡检脚本

**场景说明**：作为测试工程师或运维人员，需要定期检查系统运行状态，及时发现潜在问题。

**具体需求**：
编写系统巡检脚本 `system_check.sh`，检查以下项目：
1. CPU 使用率（警告阈值 80%）
2. 内存使用率（警告阈值 85%）
3. 磁盘使用率（警告阈值 90%）
4. 检查关键服务是否运行（nginx、mysql）
5. 检查系统负载
6. 输出格式化的巡检报告

**使用示例**：
```bash
#!/bin/bash
# system_check.sh - 系统巡检脚本

# ============================================
# 配置
# ============================================
CPU_THRESHOLD=80
MEM_THRESHOLD=85
DISK_THRESHOLD=90
SERVICES=("nginx" "mysql" "redis")
REPORT_FILE="system_report_$(date +%Y%m%d_%H%M%S).txt"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================
# 函数：输出带颜色的状态
# ============================================
print_ok() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================
# 函数：检查 CPU 使用率
# ============================================
check_cpu() {
    # 获取 CPU 使用率（不同系统可能需要调整）
    if command -v top &> /dev/null; then
        CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print int($2)}')
        if [ -z "$CPU_USAGE" ]; then
            # macOS 兼容
            CPU_USAGE=$(top -l 1 | grep "CPU usage" | awk '{print int($3)}')
        fi
    else
        CPU_USAGE=$(awk '/cpu /{print 100-$NF}' /proc/stat 2>/dev/null || echo "0")
    fi

    echo ""
    echo "=== CPU 使用率 ==="
    echo "当前 CPU 使用率: ${CPU_USAGE}%"

    if [ "$CPU_USAGE" -gt "$CPU_THRESHOLD" ]; then
        print_warn "CPU 使用率超过阈值 ${CPU_THRESHOLD}%"
        return 1
    else
        print_ok "CPU 使用率正常"
        return 0
    fi
}

# ============================================
# 函数：检查内存使用率
# ============================================
check_memory() {
    echo ""
    echo "=== 内存使用率 ==="

    if command -v free &> /dev/null; then
        # Linux
        MEM_INFO=$(free -m | grep "Mem:")
        TOTAL=$(echo $MEM_INFO | awk '{print $2}')
        USED=$(echo $MEM_INFO | awk '{print $3}')
        MEM_USAGE=$((USED * 100 / TOTAL))
        echo "总内存: ${TOTAL}MB, 已用: ${USED}MB"
    else
        # macOS
        MEM_INFO=$(vm_stat)
        FREE_PAGES=$(echo "$MEM_INFO" | grep "free" | awk '{print $3}' | tr -d '.')
        TOTAL_MEM=$(sysctl -n hw.memsize)
        TOTAL_MEM_MB=$((TOTAL_MEM / 1024 / 1024))
        # 简化处理
        MEM_USAGE=50
        echo "总内存: ${TOTAL_MEM_MB}MB"
    fi

    echo "当前内存使用率: ${MEM_USAGE}%"

    if [ "$MEM_USAGE" -gt "$MEM_THRESHOLD" ]; then
        print_warn "内存使用率超过阈值 ${MEM_THRESHOLD}%"
        return 1
    else
        print_ok "内存使用率正常"
        return 0
    fi
}

# ============================================
# 函数：检查磁盘使用率
# ============================================
check_disk() {
    echo ""
    echo "=== 磁盘使用率 ==="

    df -h | grep -v "tmpfs" | grep -v "Filesystem" | while read line; do
        USAGE=$(echo $line | awk '{print $5}' | tr -d '%')
        MOUNT=$(echo $line | awk '{print $6}')
        SIZE=$(echo $line | awk '{print $2}')
        USED=$(echo $line | awk '{print $3}')
        AVAIL=$(echo $line | awk '{print $4}')

        echo "挂载点: $MOUNT (总: $SIZE, 已用: $USED, 可用: $AVAIL)"

        if [ "$USAGE" -gt "$DISK_THRESHOLD" ]; then
            print_warn "磁盘使用率 ${USAGE}% 超过阈值 ${DISK_THRESHOLD}%"
        else
            print_ok "磁盘使用率 ${USAGE}% 正常"
        fi
    done
}

# ============================================
# 函数：检查系统负载
# ============================================
check_load() {
    echo ""
    echo "=== 系统负载 ==="

    # 获取负载
    if [ -f /proc/loadavg ]; then
        LOAD=$(cat /proc/loadavg | awk '{print $1, $2, $3}')
    else
        LOAD=$(uptime | awk -F'load averages:' '{print $2}')
    fi

    CPU_CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 1)

    echo "系统负载 (1/5/15分钟): $LOAD"
    echo "CPU 核心数: $CPU_CORES"

    # 简单判断：负载是否超过核心数
    LOAD_1=$(echo $LOAD | awk '{print $1}')
    if [ $(echo "$LOAD_1 > $CPU_CORES" | bc 2>/dev/null || echo 0) -eq 1 ]; then
        print_warn "系统负载较高"
    else
        print_ok "系统负载正常"
    fi
}

# ============================================
# 函数：检查服务状态
# ============================================
check_services() {
    echo ""
    echo "=== 服务状态 ==="

    for service in "${SERVICES[@]}"; do
        if command -v systemctl &> /dev/null; then
            # systemd 系统
            if systemctl is-active --quiet "$service"; then
                print_ok "$service 服务运行中"
            else
                print_error "$service 服务未运行"
            fi
        elif command -v service &> /dev/null; then
            # SysV 系统
            if service "$service" status &> /dev/null; then
                print_ok "$service 服务运行中"
            else
                print_error "$service 服务未运行"
            fi
        else
            # 使用 pgrep 检查进程
            if pgrep -x "$service" &> /dev/null; then
                print_ok "$service 进程存在"
            else
                print_warn "$service 进程不存在"
            fi
        fi
    done
}

# ============================================
# 函数：检查网络连接
# ============================================
check_network() {
    echo ""
    echo "=== 网络连接 ==="

    # 检查外网连接
    if ping -c 1 -W 2 8.8.8.8 &> /dev/null; then
        print_ok "外网连接正常"
    else
        print_error "外网连接异常"
    fi

    # 检查 DNS
    if nslookup google.com &> /dev/null; then
        print_ok "DNS 解析正常"
    else
        print_warn "DNS 解析异常"
    fi
}

# ============================================
# 主程序
# ============================================
main() {
    echo "=========================================="
    echo "        系统巡检报告"
    echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "  主机: $(hostname)"
    echo "=========================================="

    check_cpu
    check_memory
    check_disk
    check_load
    check_services
    check_network

    echo ""
    echo "=========================================="
    echo "        巡检完成"
    echo "=========================================="
}

# 执行并保存报告
main | tee "$REPORT_FILE"
echo ""
echo "报告已保存到: $REPORT_FILE"
```

**验收标准**：
- [ ] 脚本能正确检测 CPU 使用率
- [ ] 脚本能正确检测内存使用率
- [ ] 脚本能正确检测磁盘使用率
- [ ] 脚本能检测指定服务的运行状态
- [ ] 超过阈值时有警告提示
- [ ] 生成格式化的巡检报告

#### 练习18：日志监控脚本

**场景说明**：在生产环境中，需要实时监控日志文件，及时发现错误和异常，以便快速响应。

**具体需求**：
编写日志监控脚本 `log_monitor.sh`，实现以下功能：
1. 监控指定的日志文件
2. 实时检测 ERROR 和 WARNING 关键字
3. 发现关键字时发送通知（写入告警文件）
4. 记录告警时间和内容
5. 支持多个日志文件同时监控

**使用示例**：
```bash
#!/bin/bash
# log_monitor.sh - 日志监控脚本

# ============================================
# 配置
# ============================================
ALERT_FILE="alerts.log"
KEYWORDS="ERROR|WARN|CRITICAL|Exception|Failed"
LOG_FILES=("${@:-app.log}")  # 默认监控 app.log，可传参数指定多个
CHECK_INTERVAL=5

# 颜色定义
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# ============================================
# 初始化
# ============================================
init() {
    echo "=========================================="
    echo "         日志监控启动"
    echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "  监控文件: ${LOG_FILES[*]}"
    echo "  关键字: $KEYWORDS"
    echo "=========================================="

    # 创建告警文件
    touch "$ALERT_FILE"
}

# ============================================
# 函数：发送告警
# ============================================
send_alert() {
    local log_file=$1
    local line=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # 写入告警文件
    echo "[$timestamp] [$log_file] $line" >> "$ALERT_FILE"

    # 控制台输出
    if echo "$line" | grep -qiE "error|critical|exception"; then
        echo -e "${RED}[ERROR]${NC} [$log_file] $line"
    else
        echo -e "${YELLOW}[WARN]${NC} [$log_file] $line"
    fi

    # 可选：发送邮件或钉钉通知
    # send_dingtalk "$line"
    # send_email "Log Alert" "$line"
}

# ============================================
# 函数：监控单个日志文件
# ============================================
monitor_file() {
    local log_file=$1

    if [ ! -f "$log_file" ]; then
        echo -e "${RED}文件不存在: $log_file${NC}"
        return 1
    fi

    echo -e "${GREEN}开始监控: $log_file${NC}"

    # 使用 tail -f 实时监控
    # 方法1：使用 grep 过滤
    tail -f "$log_file" 2>/dev/null | while read -r line; do
        if echo "$line" | grep -qiE "$KEYWORDS"; then
            send_alert "$log_file" "$line"
        fi
    done
}

# ============================================
# 函数：后台监控模式
# ============================================
background_monitor() {
    local log_file=$1
    local last_size=0
    local current_size

    echo -e "${GREEN}后台监控: $log_file${NC}"

    while true; do
        if [ -f "$log_file" ]; then
            current_size=$(wc -c < "$log_file")

            if [ "$current_size" -gt "$last_size" ]; then
                # 读取新增内容
                tail -c +$((last_size + 1)) "$log_file" | while read -r line; do
                    if echo "$line" | grep -qiE "$KEYWORDS"; then
                        send_alert "$log_file" "$line"
                    fi
                done
            elif [ "$current_size" -lt "$last_size" ]; then
                # 文件被截断（如日志轮转）
                echo -e "${YELLOW}日志文件已重置: $log_file${NC}"
            fi

            last_size=$current_size
        fi

        sleep $CHECK_INTERVAL
    done
}

# ============================================
# 函数：发送钉钉通知（示例）
# ============================================
send_dingtalk() {
    local message=$1
    local webhook="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"

    curl -s -X POST "$webhook" \
        -H "Content-Type: application/json" \
        -d "{\"msgtype\": \"text\", \"text\": {\"content\": \"日志告警: $message\"}}" \
        > /dev/null
}

# ============================================
# 函数：发送邮件通知（示例）
# ============================================
send_email() {
    local subject=$1
    local body=$2
    local recipients="admin@example.com"

    echo "$body" | mail -s "$subject" "$recipients"
}

# ============================================
# 函数：生成测试日志
# ============================================
generate_test_log() {
    local log_file="test_app.log"

    echo "生成测试日志文件: $log_file"

    cat > "$log_file" << 'EOF'
2024-01-15 10:00:01 [INFO] Application started
2024-01-15 10:00:02 [INFO] Loading configuration
2024-01-15 10:00:03 [WARN] Config file not found, using defaults
2024-01-15 10:00:04 [INFO] Connecting to database
2024-01-15 10:00:05 [ERROR] Database connection failed
2024-01-15 10:00:06 [INFO] Retrying connection
2024-01-15 10:00:07 [ERROR] Max retries exceeded
EOF

    echo "测试日志已生成"
}

# ============================================
# 函数：实时添加测试日志
# ============================================
add_test_entries() {
    local log_file=$1

    echo "向 $log_file 添加测试条目..."

    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] 正常日志条目" >> "$log_file"
    sleep 1
    echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] 警告：磁盘空间不足" >> "$log_file"
    sleep 1
    echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] 错误：服务连接超时" >> "$log_file"
    sleep 1
    echo "$(date '+%Y-%m-%d %H:%M:%S') [CRITICAL] 严重：内存溢出" >> "$log_file"

    echo "测试条目已添加"
}

# ============================================
# 主程序
# ============================================
main() {
    # 解析参数
    while getopts "f:k:gh" opt; do
        case $opt in
            f) LOG_FILES+=("$OPTARG") ;;
            k) KEYWORDS="$OPTARG" ;;
            g) generate_test_log; exit 0 ;;
            h)
                echo "用法: $0 [选项] [日志文件...]"
                echo "选项:"
                echo "  -f FILE   指定监控的日志文件"
                echo "  -k WORDS  指定关键字（正则表达式）"
                echo "  -g        生成测试日志文件"
                echo "  -h        显示帮助信息"
                exit 0
                ;;
        esac
    done

    init

    # 为每个日志文件启动监控进程
    for log_file in "${LOG_FILES[@]}"; do
        # 使用后台模式监控
        background_monitor "$log_file" &
        echo "监控进程 PID: $!"
    done

    # 等待所有后台进程
    wait
}

# 如果带参数运行，执行主程序
if [ $# -gt 0 ]; then
    main "$@"
else
    # 交互式演示
    init
    generate_test_log
    echo ""
    echo "启动监控（5秒后添加测试条目）..."
    monitor_file "test_app.log" &
    MONITOR_PID=$!

    sleep 2
    add_test_entries "test_app.log"

    sleep 3
    kill $MONITOR_PID 2>/dev/null

    echo ""
    echo "=== 告警记录 ==="
    cat "$ALERT_FILE" 2>/dev/null || echo "无告警"
fi
```

**验收标准**：
- [ ] 脚本能实时监控日志文件
- [ ] 能检测指定的关键字
- [ ] 发现关键字时正确记录告警
- [ ] 告警包含时间戳和来源文件
- [ ] 支持同时监控多个日志文件

#### 练习19：自动化部署脚本

**场景说明**：在持续集成/持续部署（CI/CD）流程中，需要自动化部署脚本来完成代码更新、依赖安装、服务重启等操作。

**具体需求**：
编写应用部署脚本 `deploy.sh`，实现以下功能：
1. 拉取最新代码
2. 安装/更新依赖
3. 执行数据库迁移
4. 重启服务
5. 健康检查
6. 回滚机制（失败时恢复）

**使用示例**：
```bash
#!/bin/bash
# deploy.sh - 自动化部署脚本

# ============================================
# 配置
# ============================================
APP_NAME="myapp"
APP_DIR="/var/www/$APP_NAME"
BACKUP_DIR="/var/backups/$APP_NAME"
GIT_REPO="https://github.com/user/repo.git"
BRANCH="main"
LOG_FILE="deploy_$(date +%Y%m%d_%H%M%S).log"
HEALTH_URL="http://localhost:8080/health"
HEALTH_TIMEOUT=30

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ============================================
# 函数：日志记录
# ============================================
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$1"; }
log_warn() { log "WARN" "$1"; }
log_error() { log "ERROR" "$1"; }
log_success() { log "SUCCESS" "$1"; }

# ============================================
# 函数：错误处理
# ============================================
handle_error() {
    local message=$1
    log_error "$message"
    rollback
    exit 1
}

# ============================================
# 函数：备份当前版本
# ============================================
backup() {
    log_info "开始备份当前版本..."

    BACKUP_NAME="${APP_NAME}_$(date +%Y%m%d_%H%M%S).tar.gz"

    if [ -d "$APP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$(dirname $APP_DIR)" "$(basename $APP_DIR)"
        log_success "备份完成: $BACKUP_DIR/$BACKUP_NAME"

        # 记录备份路径供回滚使用
        echo "$BACKUP_DIR/$BACKUP_NAME" > .latest_backup
    else
        log_warn "应用目录不存在，跳过备份"
    fi
}

# ============================================
# 函数：回滚
# ============================================
rollback() {
    log_warn "开始回滚..."

    if [ -f .latest_backup ]; then
        LATEST_BACKUP=$(cat .latest_backup)
        if [ -f "$LATEST_BACKUP" ]; then
            # 停止服务
            stop_service

            # 恢复备份
            rm -rf "$APP_DIR"
            tar -xzf "$LATEST_BACKUP" -C "$(dirname $APP_DIR)"

            # 重启服务
            start_service

            log_success "回滚完成"
        else
            log_error "备份文件不存在: $LATEST_BACKUP"
        fi
    else
        log_warn "没有可用的备份"
    fi
}

# ============================================
# 函数：拉取代码
# ============================================
pull_code() {
    log_info "开始拉取最新代码..."

    if [ -d "$APP_DIR/.git" ]; then
        cd "$APP_DIR"
        git fetch origin
        git checkout "$BRANCH"
        git pull origin "$BRANCH" || handle_error "代码拉取失败"
    else
        git clone -b "$BRANCH" "$GIT_REPO" "$APP_DIR" || handle_error "代码克隆失败"
        cd "$APP_DIR"
    fi

    CURRENT_COMMIT=$(git rev-parse HEAD)
    log_success "代码更新完成，当前提交: ${CURRENT_COMMIT:0:8}"
}

# ============================================
# 函数：安装依赖
# ============================================
install_dependencies() {
    log_info "开始安装依赖..."
    cd "$APP_DIR"

    # Python 项目
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt || handle_error "Python 依赖安装失败"
    fi

    # Node.js 项目
    if [ -f "package.json" ]; then
        npm install || handle_error "Node.js 依赖安装失败"
    fi

    # Java 项目
    if [ -f "pom.xml" ]; then
        mvn clean package -DskipTests || handle_error "Maven 构建失败"
    fi

    if [ -f "build.gradle" ]; then
        ./gradlew build -x test || handle_error "Gradle 构建失败"
    fi

    log_success "依赖安装完成"
}

# ============================================
# 函数：数据库迁移
# ============================================
run_migrations() {
    log_info "执行数据库迁移..."
    cd "$APP_DIR"

    # Django 迁移
    if [ -f "manage.py" ]; then
        python manage.py migrate || handle_error "数据库迁移失败"
    fi

    # Flask-Migrate
    if [ -f "migrations" ]; then
        flask db upgrade || handle_error "数据库迁移失败"
    fi

    # 自定义迁移脚本
    if [ -f "scripts/migrate.sh" ]; then
        bash scripts/migrate.sh || handle_error "数据库迁移失败"
    fi

    log_success "数据库迁移完成"
}

# ============================================
# 函数：停止服务
# ============================================
stop_service() {
    log_info "停止服务..."

    if command -v systemctl &> /dev/null; then
        systemctl stop "$APP_NAME" || true
    elif [ -f "scripts/stop.sh" ]; then
        bash scripts/stop.sh
    else
        pkill -f "$APP_NAME" || true
    fi

    log_success "服务已停止"
}

# ============================================
# 函数：启动服务
# ============================================
start_service() {
    log_info "启动服务..."
    cd "$APP_DIR"

    if command -v systemctl &> /dev/null; then
        systemctl start "$APP_NAME" || handle_error "服务启动失败"
    elif [ -f "scripts/start.sh" ]; then
        bash scripts/start.sh || handle_error "服务启动失败"
    else
        # 简单的后台启动
        nohup python app.py > logs/app.log 2>&1 &
    fi

    log_success "服务已启动"
}

# ============================================
# 函数：健康检查
# ============================================
health_check() {
    log_info "执行健康检查..."

    local count=0
    while [ $count -lt $HEALTH_TIMEOUT ]; do
        if curl -sf "$HEALTH_URL" > /dev/null; then
            log_success "健康检查通过"
            return 0
        fi

        sleep 1
        ((count++))
        echo -n "."
    done

    echo ""
    handle_error "健康检查失败，服务未能正常启动"
}

# ============================================
# 函数：部署后通知
# ============================================
notify() {
    local status=$1
    local message=$2

    # 钉钉通知
    # curl -X POST "webhook_url" -d "{\"text\": {\"content\": \"[$status] $message\"}}"

    # 邮件通知
    # echo "$message" | mail -s "Deploy $status" admin@example.com

    log_info "通知: [$status] $message"
}

# ============================================
# 函数：清理旧备份
# ============================================
cleanup_old_backups() {
    log_info "清理旧备份..."

    # 保留最近 5 个备份
    cd "$BACKUP_DIR"
    ls -t *.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null

    log_success "旧备份清理完成"
}

# ============================================
# 主程序
# ============================================
main() {
    echo "=========================================="
    echo "    自动化部署脚本"
    echo "    应用: $APP_NAME"
    echo "    时间: $(date)"
    echo "=========================================="

    # 1. 备份
    backup

    # 2. 拉取代码
    pull_code

    # 3. 安装依赖
    install_dependencies

    # 4. 数据库迁移
    run_migrations

    # 5. 停止服务
    stop_service

    # 6. 启动服务
    start_service

    # 7. 健康检查
    health_check

    # 8. 清理旧备份
    cleanup_old_backups

    # 9. 发送成功通知
    notify "SUCCESS" "部署成功: $APP_NAME @ $(date)"

    echo ""
    echo "=========================================="
    log_success "部署完成！"
    echo "=========================================="
}

# 解析命令行参数
case "$1" in
    rollback)
        rollback
        ;;
    backup)
        backup
        ;;
    *)
        main
        ;;
esac
```

**验收标准**：
- [ ] 脚本能正确备份当前版本
- [ ] 脚本能正确拉取最新代码
- [ ] 脚本能正确安装依赖
- [ ] 脚本能正确执行数据库迁移
- [ ] 脚本能正确重启服务
- [ ] 健康检查失败时能自动回滚
- [ ] 部署失败时能自动回滚

#### 练习20：性能分析报告

**场景说明**：在性能测试或问题排查时，需要收集系统性能数据并生成报告，帮助分析系统瓶颈。

**具体需求**：
编写性能分析脚本，完成以下任务：
1. 收集 1 分钟内的系统指标（每 5 秒采样）
   - CPU 使用率
   - 内存使用率
   - 磁盘 I/O
   - 网络流量
2. 分析进程资源占用 Top 10
3. 检查系统日志中的错误
4. 生成 Markdown 格式的报告
5. 给出优化建议

**使用示例**：
```bash
#!/bin/bash
# performance_analysis.sh - 系统性能分析脚本

# ============================================
# 配置
# ============================================
REPORT_FILE="performance_report_$(date +%Y%m%d_%H%M%S).md"
DURATION=60        # 采样时长（秒）
INTERVAL=5         # 采样间隔（秒）
SAMPLES=$((DURATION / INTERVAL))

# 数据文件
CPU_DATA=$(mktemp)
MEM_DATA=$(mktemp)
DISK_DATA=$(mktemp)
NET_DATA=$(mktemp)

# ============================================
# 函数：收集 CPU 数据
# ============================================
collect_cpu() {
    echo "收集 CPU 数据..."

    for ((i=0; i<SAMPLES; i++)); do
        if [ -f /proc/stat ]; then
            # Linux
            CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print 100-$8}')
        else
            # macOS
            CPU_USAGE=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | tr -d '%')
        fi

        echo "$(date +%H:%M:%S),${CPU_USAGE:-0}" >> "$CPU_DATA"
        sleep $INTERVAL
    done
}

# ============================================
# 函数：收集内存数据
# ============================================
collect_memory() {
    echo "收集内存数据..."

    for ((i=0; i<SAMPLES; i++)); do
        if command -v free &> /dev/null; then
            # Linux
            MEM_INFO=$(free -m | grep "Mem:")
            TOTAL=$(echo $MEM_INFO | awk '{print $2}')
            USED=$(echo $MEM_INFO | awk '{print $3}')
            MEM_USAGE=$((USED * 100 / TOTAL))
        else
            # macOS
            MEM_USAGE=$(vm_stat | head -5 | awk '/free/ {print 100-$3*100}')
        fi

        echo "$(date +%H:%M:%S),${MEM_USAGE:-0}" >> "$MEM_DATA"
        sleep $INTERVAL
    done
}

# ============================================
# 函数：收集磁盘 I/O 数据
# ============================================
collect_disk() {
    echo "收集磁盘 I/O 数据..."

    for ((i=0; i<SAMPLES; i++)); do
        if command -v iostat &> /dev/null; then
            IO_UTIL=$(iostat -c 1 -x 2>/dev/null | tail -1 | awk '{print $NF}')
        else
            IO_UTIL="0"
        fi

        echo "$(date +%H:%M:%S),${IO_UTIL:-0}" >> "$DISK_DATA"
        sleep $INTERVAL
    done
}

# ============================================
# 函数：收集网络数据
# ============================================
collect_network() {
    echo "收集网络数据..."

    for ((i=0; i<SAMPLES; i++)); do
        # 简化处理，记录网络连接数
        NET_CONN=$(netstat -an 2>/dev/null | grep ESTABLISHED | wc -l)
        echo "$(date +%H:%M:%S),${NET_CONN:-0}" >> "$NET_DATA"
        sleep $INTERVAL
    done
}

# ============================================
# 函数：获取进程 Top 10
# ============================================
get_top_processes() {
    echo "获取资源占用 Top 10 进程..."

    # CPU Top 10
    echo "### CPU 占用 Top 10"
    ps aux --sort=-%cpu 2>/dev/null | head -11 || ps aux -r | head -11

    echo ""
    echo "### 内存占用 Top 10"
    ps aux --sort=-%mem 2>/dev/null | head -11 || ps aux -m | head -11
}

# ============================================
# 函数：检查系统日志错误
# ============================================
check_log_errors() {
    echo "检查系统日志中的错误..."

    echo "### 最近 24 小时的错误日志"

    if [ -d /var/log ]; then
        # 检查 syslog
        if [ -f /var/log/syslog ]; then
            grep -i "error\|critical\|fatal" /var/log/syslog | tail -20
        fi

        # 检查 messages
        if [ -f /var/log/messages ]; then
            grep -i "error\|critical\|fatal" /var/log/messages | tail -20
        fi
    elif command -v journalctl &> /dev/null; then
        journalctl --since "1 day ago" -p err | tail -20
    else
        echo "无法访问系统日志"
    fi
}

# ============================================
# 函数：计算统计数据
# ============================================
calculate_stats() {
    local data_file=$1
    local name=$2

    if [ ! -s "$data_file" ]; then
        echo "无数据"
        return
    fi

    # 提取数值列
    values=$(cut -d',' -f2 "$data_file")

    # 计算平均值
    avg=$(echo "$values" | awk '{sum+=$1; count++} END {printf "%.2f", sum/count}')

    # 计算最大值
    max=$(echo "$values" | sort -n | tail -1)

    # 计算最小值
    min=$(echo "$values" | sort -n | head -1)

    echo "| 指标 | 值 |"
    echo "|------|------|"
    echo "| 平均值 | ${avg}% |"
    echo "| 最大值 | ${max}% |"
    echo "| 最小值 | ${min}% |"
}

# ============================================
# 函数：生成优化建议
# ============================================
generate_recommendations() {
    local cpu_avg=$1
    local mem_avg=$2

    echo "### 优化建议"

    if [ $(echo "$cpu_avg > 80" | bc 2>/dev/null || echo 0) -eq 1 ]; then
        echo "- CPU 使用率较高，建议检查 CPU 密集型进程或考虑扩容"
    fi

    if [ $(echo "$mem_avg > 85" | bc 2>/dev/null || echo 0) -eq 1 ]; then
        echo "- 内存使用率较高，建议检查内存泄漏或增加物理内存"
    fi

    echo "- 定期检查和清理系统日志"
    echo "- 配置监控告警，及时发现异常"
    echo "- 考虑使用缓存减少数据库压力"
    echo "- 优化慢查询 SQL"
}

# ============================================
# 函数：生成 Markdown 报告
# ============================================
generate_report() {
    echo "生成报告..."

    # 计算 CPU 平均值
    CPU_AVG=$(awk -F',' '{sum+=$2; count++} END {printf "%.2f", sum/count}' "$CPU_DATA")
    MEM_AVG=$(awk -F',' '{sum+=$2; count++} END {printf "%.2f", sum/count}' "$MEM_DATA")

    cat > "$REPORT_FILE" << EOF
# 系统性能分析报告

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')
**主机名**: $(hostname)
**系统**: $(uname -a)

---

## 1. 概要

| 指标 | 平均值 | 状态 |
|------|--------|------|
| CPU 使用率 | ${CPU_AVG}% | $([ $(echo "$CPU_AVG > 80" | bc 2>/dev/null || echo 0) -eq 1 ] && echo "⚠️ 较高" || echo "✅ 正常") |
| 内存使用率 | ${MEM_AVG}% | $([ $(echo "$MEM_AVG > 85" | bc 2>/dev/null || echo 0) -eq 1 ] && echo "⚠️ 较高" || echo "✅ 正常") |

---

## 2. 详细数据

### 2.1 CPU 使用率

$(calculate_stats "$CPU_DATA" "CPU")

**采样数据**:
\`\`\`
$(cat "$CPU_DATA")
\`\`\`

### 2.2 内存使用率

$(calculate_stats "$MEM_DATA" "内存")

**采样数据**:
\`\`\`
$(cat "$MEM_DATA")
\`\`\`

### 2.3 网络连接数

**采样数据**:
\`\`\`
$(cat "$NET_DATA")
\`\`\`

---

## 3. 进程分析

\`\`\`
$(get_top_processes)
\`\`\`

---

## 4. 日志错误

\`\`\`
$(check_log_errors)
\`\`\`

---

## 5. 优化建议

$(generate_recommendations "$CPU_AVG" "$MEM_AVG")

---

*报告由自动化脚本生成*
EOF

    echo "报告已生成: $REPORT_FILE"
}

# ============================================
# 主程序
# ============================================
main() {
    echo "=========================================="
    echo "    系统性能分析"
    echo "    采样时长: ${DURATION}秒"
    echo "    采样间隔: ${INTERVAL}秒"
    echo "=========================================="

    # 并行收集数据
    collect_cpu &
    collect_memory &
    collect_disk &
    collect_network &

    # 等待数据收集完成
    wait

    # 生成报告
    generate_report

    # 清理临时文件
    rm -f "$CPU_DATA" "$MEM_DATA" "$DISK_DATA" "$NET_DATA"

    echo ""
    echo "=========================================="
    echo "    分析完成"
    echo "=========================================="
}

main
```

**验收标准**：
- [ ] 脚本能正确收集 CPU 使用率数据
- [ ] 脚本能正确收集内存使用率数据
- [ ] 脚本能正确获取进程资源占用排名
- [ ] 能检查系统日志中的错误
- [ ] 生成格式正确的 Markdown 报告
- [ ] 报告包含优化建议

---

## 四、学到什么程度

### 必须掌握

- [ ] 文件操作命令
- [ ] 文件查看命令
- [ ] 进程管理
- [ ] grep 搜索
- [ ] 日志查看

### 应该了解

- [ ] Shell 脚本基础
- [ ] 网络命令
- [ ] 权限管理

---

## 五、本周小结

1. **文件操作**：日常必备
2. **进程管理**：问题排查
3. **日志分析**：定位问题关键
4. **Shell 脚本**：自动化基础

### 下周预告

第10周学习性能测试。
