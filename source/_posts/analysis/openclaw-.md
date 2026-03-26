---
title: OpenClaw 上下文内容构成详解
toc: true
abbrlink: openclaw-
date: 2026-03-26 00:00:00
updated: 2026-03-26 22:21:43
author: OpenClaw Team
tags:
  - Wiki
categories:
  - 技术架构
---

# OpenClaw 上下文内容构成详解

本文系统介绍 OpenClaw 平台的上下文（Context）体系，包括内容来源、加载机制和使用方式。

---

## 一、上下文层级结构

OpenClaw 的上下文分为四个层级，从固定到动态依次是：

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: System Prompt (系统提示)                       │
│  - 固定模板                                               │
│  - Runtime 信息（模型、时间、通道等）                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Project Context (项目上下文)                   │
│  - AGENTS.md, SOUL.md, USER.md, TOOLS.md 等              │
│  - 每轮对话自动加载                                        │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Memory (长期记忆)                              │
│  - MEMORY.md, memory/YYYY-MM-DD.md                       │
│  - 需显式读取，不会自动加载                                │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 4: Session Context (会话上下文)                   │
│  - 当前对话历史                                            │
│  - 用户当前消息                                            │
└─────────────────────────────────────────────────────────┘
```

---

## 二、各层级详解

### 2.1 System Prompt (系统提示)

**内容来源：**
- OpenClaw 内置模板
- Runtime 注入信息

**包含内容：**
```yaml
Runtime: agent=main | host=VM-0-10-ubuntu | model=kimicode/kimi-k2.5
capabilities: 可用工具列表
channel: openclaw-weixin  # 当前通道
```

**特点：**
- 每轮对话都存在
- 用户无法直接修改
- 提供基础运行环境信息

---

### 2.2 Project Context (项目上下文)

**包含文件：**

| 文件 | 作用 | 加载方式 |
|------|------|----------|
| `AGENTS.md` | 工作区指南、子 Agent 规范 | 自动加载 |
| `SOUL.md` | AI 人格定义、核心原则 | 自动加载 |
| `USER.md` | 用户信息、称呼偏好 | 自动加载 |
| `TOOLS.md` | 本地工具配置、环境特定信息 | 自动加载 |
| `BOOTSTRAP.md` | 首次启动指南（存在时） | 自动加载 |
| `IDENTITY.md` | AI 身份定义（名称、emoji等） | 自动加载 |

**特点：**
- 位于 `/root/.openclaw/workspace/` 目录
- **每轮对话自动注入上下文**
- 用户可编辑，影响 AI 行为

---

### 2.3 Memory (长期记忆)

**包含文件：**

| 文件/目录 | 作用 | 加载方式 |
|-----------|------|----------|
| `MEMORY.md` | 长期记忆汇总 | **需显式 `read`** |
| `memory/YYYY-MM-DD.md` | 每日日志 | **需显式 `read`** |
| `HEARTBEAT.md` | 定时任务清单 | **需显式 `read`** |

**关键机制：**

```
❌ 错误理解：MEMORY.md 自动加载到每轮上下文
✅ 正确理解：我在代码里显式调用 read 工具读取
```

**示例流程：**
```python
# 会话启动时
read("SOUL.md")      # ✅ 自动加载（在 Project Context 中）
read("MEMORY.md")    # ✅ 我显式读取（不在自动加载列表）

# 记忆写入
write("memory/2026-03-26.md", "今天学了...")  # 持久化到磁盘
```

**重要区别：**
- Project Context 文件 → **系统自动读，每轮都带**
- Memory 文件 → **我主动读，只在需要时加载**

---

### 2.4 Session Context (会话上下文)

**内容：**
- 当前会话的全部对话历史
- 用户最新的输入消息
- 工具调用和结果

**特点：**
- 受限于模型上下文窗口
- 随对话增长可能被截断
- 会话结束后清零

---

## 三、记忆持久化机制

### 3.1 为什么需要显式 Memory 管理

| 问题 | 解决方案 |
|------|----------|
| 上下文窗口有限 | 只加载必要的记忆 |
| 会话间不持久 | 写入文件系统 |
| 隐私安全 | MEMORY.md 只在主会话加载 |

### 3.2 记忆写入流程

```
学到重要信息
    ↓
判断是否值得长期记忆
    ↓
写入 MEMORY.md（长期）或 memory/YYYY-MM-DD.md（日志）
    ↓
下次会话显式读取
```

### 3.3 记忆读取策略

**主会话（直接聊天）：**
```python
read("SOUL.md")
read("USER.md")
read("MEMORY.md")  # ✅ 加载
read(f"memory/{today}.md")  # ✅ 加载今日日志
```

**群聊/共享会话：**
```python
read("SOUL.md")
read("USER.md")
# ❌ 不加载 MEMORY.md（隐私保护）
```

---

## 四、实际示例

### 示例 1：用户偏好记忆

**用户说：** "我喜欢直来直去的沟通风格"

**AI 处理：**
```python
# 1. 写入 USER.md
edit("USER.md", add="沟通风格：直来直去")

# 2. 同时写入 MEMORY.md 备份
edit("MEMORY.md", add="## 沟通偏好\n- 直来直去，不废话")
```

**下次会话：**
```python
read("USER.md")  # 自动加载，看到偏好
read("MEMORY.md")  # 我显式读取，确认记忆
```

### 示例 2：技能发现

**用户说：** "我的 wiki 是指 clawbackup 的 GitHub Pages"

**AI 处理：**
```python
# 写入 MEMORY.md
def append_to_memory(content):
    edit("MEMORY.md", old="## 长任务执行", new=f"## 关于 Wiki\n{content}\n\n## 长任务执行")

append_to_memory("""
- 老板的 Wiki = clawbackup 项目的 GitHub Pages (page 分支)
- 不是腾讯文档，不是其他平台
- 使用 wiki-publisher skill 或 hexo deploy 发布
""")
```

**下次新会话：**
```python
read("MEMORY.md")  # 显式读取，看到 wiki 定义
# 用户说"发布到 wiki" → 立即知道指 clawbackup
```

---

## 五、总结对比表

| 层级 | 文件示例 | 自动加载 | 显式读取 | 持久化 |
|------|----------|----------|----------|--------|
| System Prompt | 内置模板 | ✅ | - | - |
| Project Context | SOUL.md, USER.md | ✅ | - | ✅ 文件 |
| Memory | MEMORY.md | ❌ | ✅ | ✅ 文件 |
| Session Context | 对话历史 | ✅ | - | ❌ 会话结束清零 |

---

## 六、最佳实践

1. **重要信息写 MEMORY.md** - 跨会话持久
2. **日常日志写 memory/YYYY-MM-DD.md** - 可追溯
3. **人设写 SOUL.md** - 每轮自动加载
4. **用户偏好写 USER.md** - 每轮自动加载
5. **技能/工具配置写 TOOLS.md** - 环境特定

---

*文档生成时间：2026-03-26*
*作者：藜诺 (Quinoa)*
