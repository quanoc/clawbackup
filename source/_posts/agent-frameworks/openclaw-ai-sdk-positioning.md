---
title: AI SDK 在 OpenClaw 中的定位与交互关系
toc: true
abbrlink: openclaw-ai-sdk-positioning
date: 2026-03-27 00:00:00
updated: 2026-03-27 21:45:00
author: WorkBuddy
tags:
  - OpenClaw
  - AI SDK
  - pi-coding-agent
  - 架构分析
  - 源码解读
categories:
  - Agent 框架
---

> **源码路径**: `/Users/zhangquanquan/WorkBuddy/20260327195403/openclaw`  
> **SDK 版本**: `@mariozechner/pi-coding-agent@0.63.0`  
> **分析日期**: 2026-03-27

---

## 一、AI SDK 是什么

OpenClaw 使用的 AI SDK 是 **`@mariozechner/pi-coding-agent`**（版本 0.63.0），由 Mario Zechner 开发。它实际上是一组协同工作的包：

| 包名 | 职责 |
|------|------|
| `@mariozechner/pi-coding-agent` | 核心 Agent 运行时，提供 `createAgentSession`、`SessionManager` 等 |
| `@mariozechner/pi-ai` | AI 模型交互层，提供 `streamSimple` 等流式调用 API |
| `@mariozechner/pi-agent-core` | 核心类型定义，如 `AgentMessage`、`AgentTool`、`AgentToolResult` |
| `@mariozechner/pi-tui` | 终端 UI 组件（用于本地调试） |

**重要说明**：这不是第三方 SDK，而是由 OpenClaw 核心开发者维护的**底层引擎库**，与 OpenClaw 是同一生态下的分层设计。

---

## 二、SDK 在项目中的定位

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 700" style="background:#1a1a2e">
  <defs>
    <linearGradient id="openclawGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#16213e"/>
      <stop offset="100%" style="stop-color:#0f3460"/>
    </linearGradient>
    <linearGradient id="sdkGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#e94560"/>
      <stop offset="100%" style="stop-color:#c23a51"/>
    </linearGradient>
    <linearGradient id="providerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#533483"/>
      <stop offset="100%" style="stop-color:#3d2661"/>
    </linearGradient>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#fff"/>
    </marker>
    <marker id="arrowheadDown" markerWidth="10" markerHeight="7" refX="5" refY="7" orient="auto">
      <polygon points="0 0, 10 0, 5 7" fill="#fff"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="450" y="30" text-anchor="middle" fill="#fff" font-size="20" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">OpenClaw AI SDK 架构定位图</text>

  <!-- ========== Layer 1: User & Channels ========== -->
  <rect x="50" y="50" width="800" height="80" rx="8" fill="#2d2d44" stroke="#4a4a6a" stroke-width="2"/>
  <text x="450" y="75" text-anchor="middle" fill="#aaa" font-size="12" font-family="system-ui, -apple-system, sans-serif">用户接入层</text>
  
  <!-- Channel icons -->
  <rect x="80" y="85" width="100" height="35" rx="5" fill="#25d366"/>
  <text x="130" y="108" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">WhatsApp</text>
  
  <rect x="200" y="85" width="100" height="35" rx="5" fill="#0088cc"/>
  <text x="250" y="108" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Telegram</text>
  
  <rect x="320" y="85" width="100" height="35" rx="5" fill="#4a154b"/>
  <text x="370" y="108" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Slack</text>
  
  <rect x="440" y="85" width="100" height="35" rx="5" fill="#5865f2"/>
  <text x="490" y="108" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Discord</text>
  
  <rect x="560" y="85" width="100" height="35" rx="5" fill="#0084ff"/>
  <text x="610" y="108" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Messenger</text>
  
  <rect x="680" y="85" width="100" height="35" rx="5" fill="#ea4335"/>
  <text x="730" y="108" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Gmail</text>

  <!-- Arrow down -->
  <line x1="450" y1="130" x2="450" y2="150" stroke="#fff" stroke-width="2" marker-end="url(#arrowheadDown)"/>

  <!-- ========== Layer 2: OpenClaw Gateway ========== -->
  <rect x="50" y="150" width="800" height="200" rx="8" fill="url(#openclawGrad)" stroke="#4a90d9" stroke-width="3"/>
  <text x="450" y="175" text-anchor="middle" fill="#4a90d9" font-size="14" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">OpenClaw 网关层（应用层）</text>

  <!-- OpenClaw modules -->
  <rect x="70" y="190" width="140" height="140" rx="5" fill="#1a1a2e" stroke="#4a90d9" stroke-width="1"/>
  <text x="140" y="215" text-anchor="middle" fill="#4a90d9" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">消息调度</text>
  <text x="140" y="240" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Dispatcher</text>
  <text x="140" y="255" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">ReplyDispatcher</text>
  <text x="140" y="270" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">MsgContext</text>
  <text x="140" y="285" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Channel Plugins</text>
  <text x="140" y="300" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">并发控制 (Lane)</text>

  <rect x="230" y="190" width="140" height="140" rx="5" fill="#1a1a2e" stroke="#4a90d9" stroke-width="1"/>
  <text x="300" y="215" text-anchor="middle" fill="#4a90d9" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Session 管理</text>
  <text x="300" y="240" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">SessionManager</text>
  <text x="300" y="255" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">多 Agent 隔离</text>
  <text x="300" y="270" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">会话持久化</text>
  <text x="300" y="285" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">历史修剪</text>
  <text x="300" y="300" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">子 Agent (ACP)</text>

  <rect x="390" y="190" width="140" height="140" rx="5" fill="#1a1a2e" stroke="#4a90d9" stroke-width="1"/>
  <text x="460" y="215" text-anchor="middle" fill="#4a90d9" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">工具策略</text>
  <text x="460" y="240" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Tool Policy Pipeline</text>
  <text x="460" y="255" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">权限检查</text>
  <text x="460" y="270" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">审批流程</text>
  <text x="460" y="285" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">沙箱隔离</text>
  <text x="460" y="300" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">工具白名单</text>

  <rect x="550" y="190" width="140" height="140" rx="5" fill="#1a1a2e" stroke="#4a90d9" stroke-width="1"/>
  <text x="620" y="215" text-anchor="middle" fill="#4a90d9" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">模型管理</text>
  <text x="620" y="240" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Model Failover</text>
  <text x="620" y="255" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Auth Profile 轮转</text>
  <text x="620" y="270" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Rate Limit 处理</text>
  <text x="620" y="285" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Context Overflow</text>
  <text x="620" y="300" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Compaction</text>

  <rect x="710" y="190" width="120" height="140" rx="5" fill="#1a1a2e" stroke="#4a90d9" stroke-width="1"/>
  <text x="770" y="215" text-anchor="middle" fill="#4a90d9" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">扩展生态</text>
  <text x="770" y="240" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Skills (ClawHub)</text>
  <text x="770" y="255" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Plugins (npm)</text>
  <text x="770" y="270" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Hooks</text>
  <text x="770" y="285" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">BOOT.md</text>
  <text x="770" y="300" text-anchor="middle" fill="#aaa" font-size="9" font-family="system-ui, -apple-system, sans-serif">Cron 任务</text>

  <!-- Arrow down -->
  <line x1="450" y1="350" x2="450" y2="370" stroke="#fff" stroke-width="2" marker-end="url(#arrowheadDown)"/>

  <!-- ========== Layer 3: AI SDK Core ========== -->
  <rect x="150" y="370" width="600" height="150" rx="8" fill="url(#sdkGrad)" stroke="#ff6b6b" stroke-width="3"/>
  <text x="450" y="395" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">AI SDK 层 (@mariozechner/pi-coding-agent)</text>
  <text x="450" y="412" text-anchor="middle" fill="#ffcccc" font-size="10" font-family="system-ui, -apple-system, sans-serif">OpenClaw 的 AI 引擎内核</text>

  <!-- SDK modules -->
  <rect x="170" y="425" width="120" height="80" rx="5" fill="#8b2635" stroke="#fff" stroke-width="1"/>
  <text x="230" y="448" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">pi-coding-agent</text>
  <text x="230" y="468" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">createAgentSession</text>
  <text x="230" y="482" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">SessionManager</text>
  <text x="230" y="496" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">工具循环</text>

  <rect x="310" y="425" width="120" height="80" rx="5" fill="#8b2635" stroke="#fff" stroke-width="1"/>
  <text x="370" y="448" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">pi-ai</text>
  <text x="370" y="468" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">streamSimple</text>
  <text x="370" y="482" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">模型调用抽象</text>
  <text x="370" y="496" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">流式响应</text>

  <rect x="450" y="425" width="120" height="80" rx="5" fill="#8b2635" stroke="#fff" stroke-width="1"/>
  <text x="510" y="448" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">pi-agent-core</text>
  <text x="510" y="468" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">AgentMessage</text>
  <text x="510" y="482" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">AgentTool</text>
  <text x="510" y="496" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">AgentToolResult</text>

  <rect x="590" y="425" width="140" height="80" rx="5" fill="#8b2635" stroke="#fff" stroke-width="1"/>
  <text x="660" y="448" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">SDK 核心职责</text>
  <text x="660" y="468" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">LLM 通信抽象</text>
  <text x="660" y="482" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">Tool Use Loop</text>
  <text x="660" y="496" text-anchor="middle" fill="#ffcccc" font-size="8" font-family="system-ui, -apple-system, sans-serif">上下文管理</text>

  <!-- Arrow down -->
  <line x1="450" y1="520" x2="450" y2="540" stroke="#fff" stroke-width="2" marker-end="url(#arrowheadDown)"/>

  <!-- ========== Layer 4: Model Providers ========== -->
  <rect x="50" y="540" width="800" height="140" rx="8" fill="url(#providerGrad)" stroke="#9b59b6" stroke-width="3"/>
  <text x="450" y="565" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">模型 Provider 层</text>

  <!-- Providers -->
  <rect x="80" y="580" width="130" height="85" rx="5" fill="#3d2661" stroke="#9b59b6" stroke-width="1"/>
  <text x="145" y="605" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Anthropic</text>
  <text x="145" y="625" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">Claude 3/4</text>
  <text x="145" y="642" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">Claude Code</text>
  <text x="145" y="657" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">Vertex AI</text>

  <rect x="230" y="580" width="130" height="85" rx="5" fill="#3d2661" stroke="#9b59b6" stroke-width="1"/>
  <text x="295" y="605" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">OpenAI</text>
  <text x="295" y="625" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">GPT-4o</text>
  <text x="295" y="642" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">Codex</text>
  <text x="295" y="657" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">o1/o3</text>

  <rect x="380" y="580" width="130" height="85" rx="5" fill="#3d2661" stroke="#9b59b6" stroke-width="1"/>
  <text x="445" y="605" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Google</text>
  <text x="445" y="625" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">Gemini 2.0</text>
  <text x="445" y="642" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">Gemini 1.5</text>
  <text x="445" y="657" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">Vertex AI</text>

  <rect x="530" y="580" width="130" height="85" rx="5" fill="#3d2661" stroke="#9b59b6" stroke-width="1"/>
  <text x="595" y="605" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">OpenRouter</text>
  <text x="595" y="625" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">统一 API</text>
  <text x="595" y="642" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">多模型路由</text>
  <text x="595" y="657" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">...</text>

  <rect x="680" y="580" width="150" height="85" rx="5" fill="#3d2661" stroke="#9b59b6" stroke-width="1"/>
  <text x="755" y="605" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">其他兼容服务</text>
  <text x="755" y="625" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">Ollama (本地)</text>
  <text x="755" y="642" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">vLLM / TGI</text>
  <text x="755" y="657" text-anchor="middle" fill="#d4a5d4" font-size="9" font-family="system-ui, -apple-system, sans-serif">自托管模型</text>

  <!-- Side annotations -->
  <rect x="860" y="150" width="30" height="200" rx="3" fill="#4a90d9" opacity="0.3"/>
  <text x="875" y="250" text-anchor="middle" fill="#4a90d9" font-size="10" font-weight="bold" font-family="system-ui, -apple-system, sans-serif" transform="rotate(90, 875, 250)">OpenClaw 封装扩展</text>

  <rect x="860" y="370" width="30" height="150" rx="3" fill="#e94560" opacity="0.3"/>
  <text x="875" y="445" text-anchor="middle" fill="#e94560" font-size="10" font-weight="bold" font-family="system-ui, -apple-system, sans-serif" transform="rotate(90, 875, 445)">AI SDK 核心引擎</text>

  <!-- Legend -->
  <rect x="50" y="655" width="800" height="35" rx="5" fill="#2d2d44"/>
  <text x="70" y="677" fill="#aaa" font-size="10" font-family="system-ui, -apple-system, sans-serif">图例说明：</text>
  <rect x="140" y="662" width="15" height="15" fill="#4a90d9"/>
  <text x="160" y="677" fill="#aaa" font-size="10" font-family="system-ui, -apple-system, sans-serif">OpenClaw 自研</text>
  <rect x="240" y="662" width="15" height="15" fill="#e94560"/>
  <text x="260" y="677" fill="#aaa" font-size="10" font-family="system-ui, -apple-system, sans-serif">底层引擎 SDK</text>
  <rect x="340" y="662" width="15" height="15" fill="#9b59b6"/>
  <text x="360" y="677" fill="#aaa" font-size="10" font-family="system-ui, -apple-system, sans-serif">模型服务</text>
  <text x="500" y="677" fill="#888" font-size="9" font-family="system-ui, -apple-system, sans-serif">箭头方向表示数据流向：用户消息 → 渠道 → OpenClaw → SDK → 模型 → 返回</text>
</svg>

**架构分层说明**：

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw 项目整体                          │
├─────────────────────────────────────────────────────────────┤
│  上层应用 (OpenClaw Gateway)                                  │
│  ├── 多渠道接入 (WhatsApp/Telegram/Slack/...)                │
│  ├── 消息调度与路由                                           │
│  ├── Session 管理与持久化                                     │
│  ├── 工具策略与权限控制                                       │
│  ├── 多 Agent 编排 (ACP 协议)                                 │
│  └── 插件/技能生态系统                                        │
├─────────────────────────────────────────────────────────────┤
│  底层引擎 (pi-coding-agent SDK)                               │
│  ├── Agent 生命周期管理                                       │
│  ├── LLM 通信抽象层                                           │
│  ├── Tool Use Loop 实现                                       │
│  └── 消息历史与上下文管理                                      │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  外部模型服务 (Anthropic/OpenAI/Google/...)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、SDK 与 OpenClaw 各模块的交互关系

### 1. Agent 执行层 (`src/agents/pi-embedded-runner/`)

这是与 SDK 交互最紧密的模块：

```typescript
// run/attempt.ts - 核心调用点
import { createAgentSession, SessionManager } from "@mariozechner/pi-coding-agent";
import { streamSimple } from "@mariozechner/pi-ai";
import type { AgentMessage } from "@mariozechner/pi-agent-core";

// 创建 Agent 会话
const { session } = await createAgentSession({
  cwd: resolvedWorkspace,
  agentDir,
  authStorage: params.authStorage,
  thinkingLevel: mapThinkingLevel(params.thinkLevel),
  tools: builtInTools,           // OpenClaw 提供的工具
  customTools: allCustomTools,   // 插件扩展的工具
  sessionManager,               // OpenClaw 封装的 SessionManager
  settingsManager,
  resourceLoader,
});
```

**交互模式**：
- OpenClaw 准备 `tools`（工具定义）和 `sessionManager`（会话状态）
- SDK 负责与模型通信、管理工具调用循环
- SDK 回调 OpenClaw 提供的工具函数执行实际操作

### 2. 工具系统 (`src/agents/pi-tools.ts`)

```typescript
import { codingTools, createReadTool, readTool } from "@mariozechner/pi-coding-agent";

// OpenClaw 基于 SDK 的基础工具构建自己的工具集
export function createOpenClawCodingTools(...) {
  const builtInTools = [
    ...codingTools,  // SDK 提供的标准工具（bash、read、write等）
    // OpenClaw 扩展的工具
    createOpenClawReadTool(...),
    createSandboxedReadTool(...),
    createSandboxedWriteTool(...),
    // ...
  ];
}
```

**关系**：SDK 提供基础工具实现，OpenClaw 在此基础上封装：
- 沙箱隔离（Sandboxed tools）
- 权限策略（Tool Policy Pipeline）
- 渠道特定工具（Channel tools）

### 3. Session 管理 (`src/agents/pi-embedded-runner/session-manager-init.ts`)

```typescript
// OpenClaw 封装 SDK 的 SessionManager
sessionManager = guardSessionManager(SessionManager.open(params.sessionFile), {
  agentId: sessionAgentId,
  sessionKey: params.sessionKey,
  allowedToolNames,
  // ...
});
```

**关系**：
- SDK 的 `SessionManager` 负责消息历史的底层存储和检索
- OpenClaw 通过 `guardSessionManager` 包装，添加：
  - 工具结果守卫（防止过大工具结果）
  - 会话写入锁（并发控制）
  - 工具名白名单检查

### 4. Channel 插件层 (`src/channels/plugins/`)

```typescript
// types.core.ts
import type { AgentTool, AgentToolResult } from "@mariozechner/pi-agent-core";

export type ChannelAgentTool = AgentTool<TSchema, unknown> & {
  ownerOnly?: boolean;  // OpenClaw 扩展的属性
};
```

Channel 插件可以注册自己的 `AgentTool`，这些工具最终会通过 SDK 暴露给 AI 模型。

### 5. 消息调度层 (`src/auto-reply/`)

```
用户消息 → Channel Plugin → MsgContext → dispatchInboundMessage()
                                              │
                                              ▼
                                    getReplyFromConfig()
                                              │
                                              ▼
                                    agentCommand() ─────┐
                                                        │
                              ┌─────────────────────────┘
                              ▼
                    runEmbeddedPiAgent()  [OpenClaw 封装]
                              │
                              ▼
                    createAgentSession()  [SDK API]
                              │
                              ▼
                    SDK 内部工具循环与模型交互
                              │
                              ▼
                    工具执行结果 → OpenClaw 回调
                              │
                              ▼
                    ReplyDispatcher → 原渠道回复
```

---

## 四、为什么要拆分成独立的 SDK

1. **职责分离**
   - `pi-coding-agent`：专注 AI Agent 核心能力（与模型对话、工具循环）
   - `openclaw`：专注多渠道网关和用户交互

2. **复用性**
   - SDK 可以被其他项目使用，不仅限于 OpenClaw
   - 类似 Anthropic 的 `claude-code` 也是一个独立可复用的 Agent 内核

3. **版本管理**
   - SDK 独立发版（当前 0.63.0）
   - OpenClaw 按需升级依赖

---

## 五、OpenClaw 对 SDK 的扩展

| SDK 能力 | OpenClaw 扩展 |
|---------|--------------|
| 基础工具执行 | 工具策略管道（审批、权限、沙箱） |
| 简单 Session 存储 | 多 Agent 隔离、会话锁、历史修剪 |
| 单模型调用 | 多模型 Failover、Auth Profile 轮转 |
| 本地运行 | 30+ 消息渠道集成、Webhook Hooks |
| 标准系统提示 | Skills 系统（ClawHub + 本地技能） |

---

## 六、总结

**AI SDK (`@mariozechner/pi-coding-agent`)** 是 OpenClaw 的 **底层 AI 引擎**，负责：
1. 与各种 LLM Provider 的通信抽象
2. 工具调用循环（Tool Use Loop）的实现
3. 消息历史的存储和上下文构建

**OpenClaw** 在 SDK 之上构建了 **完整的 AI 网关层**：
1. **多渠道接入**（WhatsApp、Telegram、Slack 等）
2. **企业级管控**（工具策略、审批流程、权限隔离）
3. **高可用设计**（模型 Failover、Auth 轮转、并发控制）
4. **扩展生态**（Plugin 系统、Skills 系统、Hooks 系统）

简单来说：**SDK 让 AI 能"思考"和"使用工具"，OpenClaw 让 AI 能"服务多用户、多渠道、多场景"**。

---

## 参考

- OpenClaw 源码: https://github.com/openclaw/openclaw
- SDK 包: `@mariozechner/pi-coding-agent@0.63.0`
- 相关文章: [OpenClaw 核心运行机制与流程分析](/clawbackup/agent-frameworks/openclaw-architecture)
