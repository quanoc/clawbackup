---
taskId: task_backup_workspace
status: running
title: 工作空间备份到 clawbackup 仓库 main 分支
progress: 0
startTime: 2026-03-28T10:34:00+08:00
updateTime: 2026-03-28T10:34:00+08:00
---

## 任务目标
将 `/home/admin/.openclaw/workspace` 工作空间备份到 clawbackup 仓库的 main 分支，实现远程备份。

## 执行步骤
1. 进入 clawbackup 仓库目录
2. `git checkout main` 切换到 main 分支
3. 清理工作区（防止旧文件残留）
4. 复制工作空间文件到仓库，排除隐私数据
5. `git add` 添加文件
6. `git commit` 提交（带时间戳消息）
7. `git push` 推送到远程

## 隐私排除项
- `.env*`、`*.key`、`*.pem`、`*.secret`
- 含 token/api_key/password 的配置文件
- `IDENTITY.md`、`USER.md`（含个人信息）

## 输出要求
- 提交成功后汇报：提交 hash、文件数量、推送状态
- 如有失败，汇报具体错误信息

## 进度文件
- JSON 状态：`memory/tasks/task_backup_workspace-progress.json`
- 日志文件：`memory/tasks/task_backup_workspace.log`
