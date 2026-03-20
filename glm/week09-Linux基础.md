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

## 三、学到什么程度

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

## 四、本周小结

1. **文件操作**：日常必备
2. **进程管理**：问题排查
3. **日志分析**：定位问题关键
4. **Shell 脚本**：自动化基础

### 下周预告

第10周学习性能测试。
