# 第 6 周 - Linux 进阶 + Shell 脚本

## 学习目标
掌握 Linux 进程管理、网络命令、系统监控，能够编写复杂的 Shell 脚本实现自动化任务。

---

## 知识点清单

### 1. 进程管理
**掌握程度**: ps/top/kill/pkill/jobs/bg/fg

**练习资源**:
- [Linux 进程管理文档](https://man7.org/linux/man-pages/man1/ps.1.html)

**练习任务**:
- 查看系统所有进程
- 按 CPU/内存排序
- 杀死指定进程
- 后台运行任务

---

### 2. 网络命令
**掌握程度**: netstat/ss/curl/wget/ping

**练习任务**:
- 查看端口占用
- 测试 API 接口
- 下载文件
- 诊断网络连通性

---

### 3. 系统监控
**掌握程度**: df/du/free/uptime

**练习任务**:
- 查看磁盘使用率
- 查看内存使用
- 查看系统负载

---

### 4. 日志分析
**掌握程度**: /var/log、journalctl

**练习任务**:
- 查看系统日志
- 查看应用日志
- 使用 journalctl 查询

---

### 5. Shell 变量
**掌握程度**: 定义、引用、环境变量

**练习任务**:
- 定义和使用变量
- 使用环境变量
- 理解 $0, $1, $2... 的含义

---

### 6. 条件判断
**掌握程度**: if/case、test 命令

**练习任务**:
- 编写条件判断脚本
- 使用 case 语句
- 理解 test 命令的各种操作符

---

### 7. 循环
**掌握程度**: for/while、break/continue

**练习任务**:
- 遍历文件列表
- 批量处理文件
- 理解 break 和 continue 的区别

---

### 8. 函数
**掌握程度**: 定义、参数、返回值

**练习任务**:
- 定义函数
- 传递参数
- 返回值处理

---

## 本周练习任务

### 必做任务

1. **系统监控脚本**
```bash
#!/bin/bash
# 实现一个系统监控脚本
# 功能:
# - 显示 CPU 使用率
# - 显示内存使用率
# - 显示磁盘使用率
# - 超过阈值时告警
```

2. **日志分析脚本**
```bash
#!/bin/bash
# 实现一个日志分析脚本
# 功能:
# - 统计访问频率
# - 统计错误率
# - 找出 Top 10 IP
# - 生成分析报告
```

3. **自动化部署脚本**
```bash
#!/bin/bash
# 实现一个自动化部署脚本
# 功能:
# - 拉取代码
# - 安装依赖
# - 重启服务
# - 健康检查
```

4. **进程管理练习**
```bash
# 1. 找出 CPU 占用最高的进程
# 2. 找出占用内存最多的进程
# 3. 后台运行一个长时间任务
# 4. 将前台任务放到后台
```

---

## 验收标准

完成本周学习后，你应该能够：

- [ ] 3 个脚本都能正常运行并输出正确结果
- [ ] 能解释 `set -e` 的作用
- [ ] 能查看和管理进程
- [ ] 能诊断网络问题
- [ ] 博客：《Linux 运维常用命令整理》

---

## Shell 脚本编程要点

### 变量
```bash
# 定义变量
name="value"

# 引用变量
echo $name
echo ${name}

# 特殊变量
$0      # 脚本名
$1-$9   # 参数
$#      # 参数个数
$?      # 上个命令的退出状态
$$      # 当前进程 ID
```

### 条件判断
```bash
# if 语句
if [ condition ]; then
    ...
elif [ condition ]; then
    ...
else
    ...
fi

# test 命令操作符
-eq     # 等于
-ne     # 不等于
-gt     # 大于
-lt     # 小于
-f      # 文件存在
-d      # 目录存在
```

### 循环
```bash
# for 循环
for i in {1..10}; do
    echo $i
done

# while 循环
while [ condition ]; do
    ...
done

# 遍历文件
for file in *.txt; do
    echo $file
done
```

### 函数
```bash
# 定义函数
function_name() {
    local var=$1
    echo "Hello $var"
    return 0
}

# 调用函数
function_name "World"
```

### 最佳实践
```bash
#!/bin/bash
# 脚本开头
set -e          # 出错退出
set -u          # 未定义变量报错
set -o pipefail # 管道失败时报错

# 使用函数
main() {
    ...
}

main "$@"
```

---

## 面试考点

### 高频面试题
1. Shell 脚本中$?的含义？
2. 如何查看端口占用？
3. 如何杀死占用端口的进程？
4. Shell 中数组如何定义？
5. for 和 while 循环的区别？
6. 如何实现 Shell 函数？
7. set -e 的作用？

### 场景题
```bash
# 1. 批量杀死包含特定关键词的进程
ps aux | grep "keyword" | grep -v grep | awk '{print $2}' | xargs kill -9

# 2. 监控 CPU 使用率，超过 80% 时告警
while true; do
    cpu=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
    if (( $(echo "$cpu > 80" | bc -l) )); then
        echo "CPU 告警！"
    fi
    sleep 60
done

# 3. 统计当前目录下每种文件类型的数量
find . -type f | awk -F. '{print $NF}' | sort | uniq -c
```

---

## 每日学习检查清单

### Day 1-2: 进程管理 + 网络命令
- [ ] 学习进程管理命令
- [ ] 学习网络命令
- [ ] 完成练习任务
- [ ] GitHub 提交

### Day 3-4: 系统监控 + 日志分析
- [ ] 学习系统监控命令
- [ ] 学习日志分析
- [ ] 编写监控脚本
- [ ] GitHub 提交

### Day 5-7: Shell 脚本编程
- [ ] 学习变量和条件
- [ ] 学习循环和函数
- [ ] 编写 3 个综合脚本
- [ ] 写博客
- [ ] 周总结

---

## 周总结模板

```markdown
## 第 6 周总结

### 学习内容
- 掌握了进程管理
- 学会了系统监控
- 能编写 Shell 脚本

### 作品
- 系统监控脚本
- 日志分析脚本
- 自动化部署脚本

### 遇到的问题
- ...

### 下周改进
- ...
```
