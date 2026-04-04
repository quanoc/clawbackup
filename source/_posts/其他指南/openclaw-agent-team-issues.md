---
title: OpenClaw Agent 团队协作问题记录
tags:
  - openclaw
  - agent
  - 团队协作
abbrlink: 23793
date: 2026-03-28 22:10:00
categories:
  - 其他指南
---

# OpenClaw Agent 团队协作问题记录

> 记录时间：2026-03-28
> 记录人：藜诺

## 问题概述

在配置藜诺（主 Agent）与码哥（持久化 Agent）的协作过程中，遇到了一系列关于 Agent 通信、消息路由和任务管理的问题。本文档记录核心问题及解决方案。

---

## 1. Agent 间通信问题

### 问题描述
藜诺无法直接给码哥发消息，报错：
```
Session send visibility is restricted. Set tools.sessions.visibility=all to allow cross-agent access.
```

### 根本原因
- 默认 `tools.sessions.visibility: "tree"`，只能访问当前 session 及其子 session
- 码哥是独立 Agent，不是藜诺派生的子 Agent
- 跨 Agent 通信需要 `visibility: "all"` + `agentToAgent.enabled: true`

### 解决方案
修改 `~/.openclaw/openclaw.json`：
```json
"tools": {
  "sessions": {
    "visibility": "all"
  },
  "agentToAgent": {
    "enabled": true
  }
}
```
然后重启 gateway。

---

## 2. 持久化 Agent Session 问题

### 问题描述
无法启动码哥的持久化 session，报错：
```
thread=true is unavailable because no channel plugin registered subagent_spawning hooks.
```

### 根本原因
- `mode: "session"` 需要 `thread=true` 才能保持长期绑定
- 微信 channel 不支持 `thread` 模式
- 只有支持 thread 的 channel（如 Discord）才能启动持久化 session

### 解决方案
**方案 A：独立 Channel（推荐）**
- 给码哥配置独立的 QQ 或微信账号
- 码哥有自己的消息入口，session 长期存在

**方案 B：按需启动**
- 派任务时启动子 Agent，任务完结束
- 当前使用的模式

---

## 3. 消息路由机制

### 问题描述
微信消息如何路由到码哥（而不是藜诺）？

### 调研结论
通过查看 `~/.openclaw/extensions/openclaw-weixin/` 源码：

| 路由方式 | 支持情况 | 说明 |
|---------|---------|------|
| @提及路由 | ❌ 不支持 | 微信插件无相关逻辑 |
| 命令前缀路由 | ✅ 支持 | `/echo`、`/toggle-debug` 等 `/` 开头命令 |
| 自动路由 | ❓ 未确认 | 依赖 OpenClaw 核心 SDK |

### 关键发现
- 路由逻辑在 `channelRuntime.routing.resolveAgentRoute()`
- 具体规则在 OpenClaw 核心，不在微信插件内
- 可能支持 `/mage xxx` 命令触发码哥

---

## 4. 子 Agent 任务管理问题

### 问题描述
- 任务设计太宽泛，子 Agent 卡住 20 分钟无结果
- 进度文件更新不及时，无法监督
- 任务频繁失败或超时

### 解决方案
1. **任务要具体** — "查本地文件 X，找不到再上网搜"
2. **强制进度更新** — "每 2 分钟必须写进度文件"
3. **先本地后远程** — 优先查本地文档
4. **设置超时阈值** — 超过 5 分钟没进度就 kill

---

## 5. Claude Code 环境配置

### 安装状态
| 组件 | 状态 | 版本 |
|-----|------|------|
| Claude Code CLI | ✅ 已安装 | v2.1.86 |
| everything-claude-code | ✅ 已配置 | 28 agents, 60 commands, 125 skills |

### 待解决问题
- 需要 Anthropic API key 才能正常使用

---

## 关键配置总结

### Agent 间通信配置
```json
"tools": {
  "sessions": {
    "visibility": "all"
  },
  "agentToAgent": {
    "enabled": true
  }
}
```

### Git 全局配置
```bash
git config --global user.name "quanoc"
git config --global user.email "waisec@sina.com"
```

---

## 待办事项

- [ ] 给码哥配置独立 QQ channel
- [ ] 配置 Anthropic API key
- [ ] 测试命令前缀路由（`/mage`）
- [ ] 优化子 Agent 任务设计规范
