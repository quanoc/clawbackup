# AGENTS.md - 子 Agent 任务执行规范

> 本文档聚焦子 Agent 任务执行，其他通用规范见 SOUL.md

---

## 快速开始

派生子 Agent 时，任务描述必须包含：
1. 任务目标（做什么）
2. 输出要求（交付什么）
3. 进度文件路径（写哪里）

示例：
```
调研代码理解 AI 工具

任务目标：...
输出要求：...

完成后将结果写入：memory/tasks/task_xxx.md
进度更新写入：memory/tasks/task_xxx-progress.json
```

---

## 子 Agent 执行规范（必读）

### 核心原则

**每执行一个工具调用，立即写进度文件。**

子 Agent 通过写文件汇报进度，不是通过消息。

**记忆锚点：**
> 每完成一个工具调用（搜索、读取、抓取等）后，**立即**更新进度文件。
> 问自己：「刚做了什么？有什么结果？」→ 写下来。
> 
> **双文件写入：**
> 1. JSON 状态文件（`{TASK_ID}-progress.json`）→ 覆盖写入，供主 Agent 快速读取
> 2. 日志文件（`{TASK_ID}.log`）→ **追加写入**，保留完整执行历史

### 环境变量

启动时自动注入：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `TASK_FILE_PATH` | 任务文件完整路径 | `memory/tasks/task_xxx.md` |
| `TASK_ID` | 任务 ID | `task_xxx` |

**进度文件路径推导：**
- JSON 状态文件：`memory/tasks/{TASK_ID}-progress.json`（覆盖写入，只保留最新状态）
- 日志文件：`memory/tasks/{TASK_ID}.log`（**追加写入**，保留完整历史）

### 执行流程（强制！！写进度文件时机）

```
启动 → 读取 TASK_FILE_PATH
  ↓
写进度文件（5%）- "已启动"
  ↓
拆步骤计划 → 写进度文件（10%）- "计划：1.XXX 2.XXX 3.XXX"
  ↓
【每个工具调用后立即写进度】
  ↓
整理阶段 → 写进度（80%）- "正在整理报告"
  ↓
完成 → 写进度文件（100%）- "任务完成，结果在xxx"
      → 更新任务文件 status: completed
```

### 进度文件规范

**两个文件，两种用途：**

| 文件 | 路径 | 写入方式 | 用途 |
|------|------|---------|------|
| JSON 状态 | `memory/tasks/{taskId}-progress.json` | **覆盖** | 主 Agent 快速查看最新状态 |
| 日志文件 | `memory/tasks/{taskId}.log` | **追加** | 保留完整执行历史，便于追溯 |

**JSON 状态文件格式（覆盖写入）：**
```json
{
  "progress": 50,
  "message": "正在搜索工具信息 3/5",
  "timestamp": "2026-03-28T01:30:00Z",
  "step": 3,
  "stepName": "搜索工具信息",
  "stepTotal": 5,
  "details": "已完成GitHub Copilot、Cursor，正在处理Tabnine"
}
```

**日志文件格式（追加写入）：**
```
[2026-03-28T01:30:00Z] [Step 3/5] 正在搜索工具信息
[2026-03-28T01:31:00Z] [Step 3/5] ✓ 完成 GitHub Copilot
[2026-03-28T01:32:00Z] [Step 3/5] ✓ 完成 Cursor
[2026-03-28T01:33:00Z] [Step 3/5] 正在处理 Tabnine...
```

**字段说明（JSON）：**
- `progress`: 0-100 整数（必须）
- `message`: 人类可读状态（必须，**包含具体动作和结果**）
- `timestamp`: ISO 8601 时间戳（必须）
- `step`: 当前步骤序号（推荐）
- `stepName`: 当前步骤名称（推荐）
- `stepTotal`: 总步骤数（推荐）
- `details`: 详细进度（可选，**用于记录具体成果**，如"已找到：GraphCodeBERT、CodeReviewer、Devin"）

### 任务文件规范

**格式：**
```yaml
---
taskId: task_xxx
status: running|completed|failed
title: 任务标题
progress: 45
startTime: 2026-03-28T01:00:00Z
updateTime: 2026-03-28T01:30:00Z
error: "失败原因（如果有）"
---

### 归档

完成后：
1. 任务文件移动到 `memory/tasks/completed/{taskId}.md`
2. 进度 JSON 文件保留（可选）
3. 日志文件保留（**推荐保留**，便于追溯历史）
