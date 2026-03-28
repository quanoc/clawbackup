---
title: OpenClaw 核心问题汇总
date: 2026-03-28 22:20:00
tags:
  - openclaw
  - agent
  - 问题汇总
  - 团队协作
categories:
  - 技术问题
abbrlink: 23794
---

# OpenClaw 核心问题汇总

> 整理时间：2026-03-28  
> 整理人：藜诺  
> 来源：历史任务执行记录与博客文档

---

## 📋 目录

1. [Agent 间通信问题](#1-agent-间通信问题)
2. [消息路由机制问题](#2-消息路由机制问题)
3. [持久化 Agent Session 问题](#3-持久化-agent-session-问题)
4. [子 Agent 任务管理问题](#4-子-agent-任务管理问题)
5. [Claude Code 环境配置问题](#5-claude-code-环境配置问题)
6. [待办事项清单](#6-待办事项清单)

---

## 1. Agent 间通信问题

### 1.1 跨 Agent 消息发送失败

**问题描述**  
藜诺（主 Agent）无法直接给码哥（持久化 Agent）发送消息，报错：
```
Session send visibility is restricted. 
Set tools.sessions.visibility=all to allow cross-agent access.
```

**根本原因**  
- 默认配置 `tools.sessions.visibility: "tree"`，只允许访问当前 session 及其子 session
- 码哥是独立 Agent，不是藜诺派生的子 Agent
- 跨 Agent 通信需要同时满足两个条件：
  1. `visibility: "all"` 
  2. `agentToAgent.enabled: true`

**解决方案**  
修改 `~/.openclaw/openclaw.json` 配置文件：
```json
{
  "tools": {
    "sessions": {
      "visibility": "all"
    },
    "agentToAgent": {
      "enabled": true
    }
  }
}
```
修改后需重启 gateway 生效。

---

## 2. 消息路由机制问题

### 2.1 微信 Channel 不支持 @提及路由

**问题描述**  
希望通过 `@码哥` 的方式将消息路由给码哥，而不是默认路由到藜诺。

**调研结论**  
通过查看 `~/.openclaw/extensions/openclaw-weixin/` 源码发现：

| 路由方式 | 支持情况 | 说明 |
|---------|---------|------|
| @提及路由 | ❌ 不支持 | 微信插件无相关逻辑 |
| 命令前缀路由 | ✅ 支持 | `/echo`、`/toggle-debug` 等 `/` 开头命令 |
| 自动路由 | ❓ 未确认 | 依赖 OpenClaw 核心 SDK |

**关键发现**  
- 路由逻辑在 `channelRuntime.routing.resolveAgentRoute()` 中实现
- 具体规则在 OpenClaw 核心，不在微信插件内
- 可能支持 `/mage xxx` 命令触发码哥

**待验证**  
- [ ] 测试 `/mage` 命令是否能路由到码哥
- [ ] 查看 OpenClaw 核心源码确认路由规则

---

## 3. 持久化 Agent Session 问题

### 3.1 无法启动持久化 Session

**问题描述**  
启动码哥的持久化 session 时失败，报错：
```
thread=true is unavailable because no channel plugin 
registered subagent_spawning hooks.
```

**根本原因**  
- `mode: "session"` 需要 `thread=true` 才能保持长期绑定
- 微信 channel 不支持 `thread` 模式
- 只有支持 thread 的 channel（如 Discord）才能启动持久化 session

**解决方案**  

**方案 A：独立 Channel（推荐）**
- 给码哥配置独立的 QQ 或微信账号
- 码哥有自己的消息入口，session 长期存在
- 优点：完全独立，不受主 Agent 影响
- 缺点：需要额外配置一个微信号/QQ号

**方案 B：按需启动（当前使用）**
- 派任务时启动子 Agent，任务完结束
- 每次任务都是新的 session
- 优点：简单，无需额外账号
- 缺点：无法保持长期上下文

**技术细节**  
根据 OpenClaw 源码分析：

| 维度 | run 模式 | session 模式 |
|------|---------|-------------|
| 设计目标 | 一次性任务执行 | 持久化线程内协作 |
| thread 绑定 | 不需要 | 必须 (thread=true) |
| 生命周期 | 短暂 (默认 60 分钟归档) | 持久 (无归档时间) |
| 清理策略 | 可配置 | 固定 keep |
| 后续交互 | ❌ 不支持 | ✅ 支持 follow-up |
| 适用场景 | 独立任务、批处理 | 持续对话、复杂工作流 |

---

## 4. 子 Agent 任务管理问题

### 4.1 任务执行超时/卡住

**问题现象**  
- 任务设计太宽泛，子 Agent 卡住 20 分钟无结果
- 进度文件更新不及时，无法监督
- 任务频繁失败或超时

**根本原因**  
1. 任务范围过大，子 Agent 无从下手
2. 没有强制进度更新机制
3. 缺少超时监控和处理

**解决方案**  
1. **任务要具体** — 明确指定 "查本地文件 X，找不到再上网搜"
2. **强制进度更新** — 要求 "每 2 分钟必须写进度文件"
3. **先本地后远程** — 优先查本地文档，减少网络搜索时间
4. **设置超时阈值** — 超过 5 分钟没进度就 kill 重启

**AGENTS.md 规范要求**  
- 每执行一个工具调用，立即写进度文件
- 双文件写入：
  - JSON 状态文件（`{TASK_ID}-progress.json`）→ 覆盖写入
  - 日志文件（`{TASK_ID}.log`）→ 追加写入

### 4.2 子 Agent 派生问题

**问题**  
藜诺作为秘书，不应该自己执行任务，但有时候子 Agent 执行不完整。

**正确流程**  
1. 用户确认任务计划
2. 藜诺生成 taskId，创建任务文件
3. 派子 Agent（注入 PARENT_SESSION_KEY、TASK_FILE_PATH、TASK_ID）
4. 子 Agent 完成后，藜诺检查任务完整性
5. 如有遗漏，继续派子 Agent 执行
6. **绝不自己接手执行**

---

## 5. Claude Code 环境配置问题

### 5.1 缺少 Anthropic API Key

**安装状态**  
| 组件 | 状态 | 版本 |
|-----|------|------|
| Claude Code CLI | ✅ 已安装 | v2.1.86 |
| everything-claude-code | ✅ 已配置 | 28 agents, 60 commands, 125 skills |

**待解决问题**  
- [ ] 配置 Anthropic API key 才能正常使用 Claude Code

**配置方法**  
```bash
# 方式1：环境变量
export ANTHROPIC_API_KEY="your-api-key"

# 方式2：Claude Code 配置
claude config set apiKey "your-api-key"
```

### 5.2 Everything Claude Code 项目调研

**项目信息**  
- **项目**: Everything Claude Code (ECC)
- **作者**: affaan-m (Anthropic Hackathon Winner)
- **GitHub**: https://github.com/affaan-m/everything-claude-code
- **Stars**: 112k+ | **Forks**: 14.7k+

**核心组件**  
- 28 个专业 Agents
- 125+ 个 Skills
- 60 个 Commands
- Hooks 系统
- 跨平台支持（Claude Code、Cursor、Codex、OpenCode）

**文章已发布**  
- `/root/.openclaw/workspace/dev-projects/clawbackup/source/_posts/everything-claude-code.md`

---

## 6. 待办事项清单

### 高优先级
- [ ] 给码哥配置独立 QQ channel（解决持久化 Agent 问题）
- [ ] 配置 Anthropic API key（启用 Claude Code）
- [ ] 修改 `openclaw.json` 启用 Agent 间通信
- [ ] 测试命令前缀路由（`/mage`）

### 中优先级
- [ ] 制定子 Agent 任务设计规范
- [ ] 建立任务超时监控机制
- [ ] 查看 OpenClaw 核心源码确认路由规则

### 已完成
- [x] 调研 Everything Claude Code 项目
- [x] 调研 AI Coding 测试和 Review 方案
- [x] 记录 Agent 团队协作问题
- [x] 整理核心问题汇总文档

---

## 关键配置总结

### Agent 间通信配置
```json
{
  "tools": {
    "sessions": {
      "visibility": "all"
    },
    "agentToAgent": {
      "enabled": true
    }
  }
}
```

### Git 全局配置
```bash
git config --global user.name "quanoc"
git config --global user.email "waisec@sina.com"
```

---

*文档生成时间: 2026-03-28 22:20*  
*关联文档: openclaw-agent-team-issues.md, ai-coding-test-review-survey.md, everything-claude-code.md*
