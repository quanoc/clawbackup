---
title: OpenClaw 核心运行机制与流程分析
toc: true
abbrlink: openclaw-architecture
date: 2026-03-27 00:00:00
updated: 2026-03-27 20:55:00
author: WorkBuddy
tags:
  - OpenClaw
  - AI Agent
  - 源码解读
  - 架构分析
  - 消息处理
categories:
  - Agent 框架
---

> **源码路径**: `/Users/zhangquanquan/WorkBuddy/20260327195403/openclaw`  
> **版本**: latest（2026年初）  
> **项目定位**: 开源个人 AI 助手，运行在自己的设备上，接入 30+ 消息平台

---

## 一、项目全局架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                          OpenClaw 整体架构                           │
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────────┐   │
│  │   CLI Entry  │    │   Gateway    │    │    Channel Layer     │   │
│  │  entry.ts    │───▶│  server.impl │───▶│  WhatsApp/Telegram  │   │
│  │  index.ts    │    │  .ts         │    │  Slack/Discord/etc   │   │
│  └──────────────┘    └──────┬───────┘    └─────────────────────┘   │
│                             │                                       │
│                    ┌────────▼────────┐                              │
│                    │   Agent Layer   │                              │
│                    │  agent-command  │                              │
│                    │  pi-embedded    │                              │
│                    └────────┬────────┘                              │
│                             │                                       │
│          ┌──────────────────┼──────────────────┐                   │
│          ▼                  ▼                  ▼                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Plugins    │  │   Skills     │  │    Memory     │             │
│  │  (npm pkg)   │  │  (ClawHub)   │  │  (per-agent)  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 二、启动流程（Cold Start）

### 2.1 入口：`src/entry.ts` → `src/index.ts`

```
openclaw gateway 命令
        │
        ▼
entry.ts（主进程入口）
  ├─ normalizeEnv()              // 标准化环境变量
  ├─ ensureOpenClawExecMarkerOnProcess()  // 标记进程
  ├─ enableCompileCache()        // Node 编译缓存
  ├─ buildCliRespawnPlan()       // 检查是否需要 respawn（如权限不足时）
  └─ runMainOrRootHelp()
        │
        ▼
src/cli/run-main.ts → runCli(argv)
        │
        ▼
gateway 子命令 → startGatewayServer()
```

### 2.2 Gateway 启动序列：`server.impl.ts → startGatewayServer()`

```
startGatewayServer()
  │
  ├─ 1. 读取 & 验证配置 (loadConfig / readConfigFileSnapshot)
  ├─ 2. 准备启动授权 (ensureGatewayStartupAuth)
  │       └─ 激活 Secrets 运行时快照 (activateSecretsRuntimeSnapshot)
  ├─ 3. 初始化模型目录 (ensureOpenClawModelsJson)
  ├─ 4. 启动插件系统 (loadGatewayStartupPlugins)
  ├─ 5. 启动 HTTP/WebSocket 服务器 (server-http.ts)
  ├─ 6. 启动渠道健康监控 (startChannelHealthMonitor)
  ├─ 7. 启动 Sidecar 服务 (startGatewaySidecars)
  │       ├─ 清理过期 Session 锁文件
  │       ├─ Gmail Watcher（如已配置）
  │       └─ 模型预热 (prewarmConfiguredPrimaryModel)
  ├─ 8. 执行 BOOT.md（如存在则运行引导 Agent）
  ├─ 9. 启动 Cron 任务 (buildGatewayCronService)
  ├─ 10. 启动配置热重载 (startGatewayConfigReloader)
  └─ 11. 启动 Tailscale / Discovery / Canvas 等可选服务
```

---

## 三、消息处理核心流程

### 3.1 入站消息全链路

```
用户在 WhatsApp/Telegram 等渠道发送消息
           │
           ▼
  Channel Plugin（如 wacli、telegram-cli 等）
           │ 接收原始消息
           ▼
  MsgContext 构建
  (src/auto-reply/templating.ts)
           │
           ▼
  dispatchInboundMessage()
  (src/auto-reply/dispatch.ts)
     │
     ├─ finalizeInboundContext()    // 标准化消息上下文
     ├─ 创建 ReplyDispatcher       // 管理回复并发与排队
     └─ dispatchReplyFromConfig()
           │
           ▼
  getReplyFromConfig()
  (src/auto-reply/reply/get-reply.ts)
     │
     ├─ 命令检测 (command-detection.ts)
     │    └─ 是命令 → 走命令路由 (commands-registry)
     │
     └─ 普通消息 → agentCommand()
           │
           ▼
```

### 3.2 Agent 命令执行：`src/agents/agent-command.ts`

```
agentCommand(opts)
  │
  ├─ 1. 解析 & 验证参数
  │       ├─ 消息体处理 (prependInternalEventContext)
  │       ├─ 解析 sessionKey / agentId
  │       └─ 验证 think / verbose 级别
  │
  ├─ 2. 加载配置 (loadConfig + 合并 secrets)
  │
  ├─ 3. 解析 Session (resolveSession)
  │       ├─ 查找现有 session 或创建新 session
  │       ├─ 加载历史会话记录
  │       └─ 确定 sessionKey / sessionId
  │
  ├─ 4. 准备工作空间 (ensureAgentWorkspace)
  │       └─ 创建/验证 workspaceDir，写入 bootstrap 文件
  │
  ├─ 5. 解析模型 (resolveConfiguredModelRef)
  │       └─ 支持 provider/model override + fallback 链
  │
  ├─ 6. 构建技能快照 (buildWorkspaceSkillSnapshot)
  │
  └─ 7. 启动 Agent 尝试 (runAgentAttempt → runWithModelFallback)
```

### 3.3 Agent 执行核心：`pi-embedded-runner/run.ts`

```
runEmbeddedPiAgent(params)
  │
  ├─ 入队执行（session-level + global-level 两层队列）
  │   enqueueCommandInLane(sessionLane, () => enqueueCommandInLane(globalLane, run))
  │
  ├─ 解析工作目录 & 插件加载
  │
  ├─ 模型解析链：
  │   Hook → 配置 → model.json → 最终 effectiveModel
  │
  ├─ 认证配置：
  │   resolveAuthProfileOrder → profileCandidates[]
  │   → createEmbeddedRunAuthController（支持多 profile 轮转）
  │
  └─ 主循环（retry loop）：
      ├─ runEmbeddedAttempt()   // 调用 @mariozechner/pi-coding-agent SDK
      │   └─ SessionManager.appendMessage() → 推送消息到 AI 模型
      │
      ├─ 失败处理（FailoverError）：
      │   ├─ auth_error → 切换认证 profile
      │   ├─ rate_limit → backoff + 重试
      │   ├─ context_overflow → 触发 compaction
      │   └─ model_not_found → 尝试 fallback 模型
      │
      └─ 成功 → emitAgentEvent() → 回传结果
```

---

## 四、会话（Session）管理机制

```
Session 标识体系：
  ┌──────────────────────────────────────────────────┐
  │  sessionKey  = "phone/+1234567890"（按渠道推导）   │
  │  sessionId   = "boot-2026-03-27_xxx"（每次运行）   │
  │  agentId     = "default"（多 Agent 支持）          │
  └──────────────────────────────────────────────────┘

存储：
  ~/.config/openclaw/sessions/<agentId>/store.json
  ~/.config/openclaw/sessions/<agentId>/transcripts/

SessionEntry 核心字段：
  {
    sessionId,          // 上次 session ID（续连续对话）
    lastChannel,        // 最近交互渠道（用于回复路由）
    to,                 // 回复目标地址
    modelOverride,      // 本 session 的模型覆盖
    authProfileOverride,// 认证 profile 覆盖
    claudeCliSessionId, // CLI provider 的 session binding
    systemPromptReport, // 系统提示 bootstrap 签名
    updatedAt           // 最后更新时间
  }
```

---

## 五、工具（Tools）执行架构

```
AI 模型生成 tool_use 请求
        │
        ▼
  Tool Policy Pipeline
  (gateway/tool-policy-pipeline.ts)
     │
     ├─ 许可检查 (tool-policy.ts)
     │    ├─ allowlist 匹配
     │    ├─ 角色权限校验 (role-policy.ts)
     │    └─ Plugin-only 工具隔离
     │
     ├─ 需要审批？→ ExecApprovalManager
     │    └─ 暂停执行，通知用户审批
     │
     └─ 执行工具
          ├─ bash/shell 工具 (bash-tools.exec-runtime.ts)
          ├─ 消息发送工具 (message tool)
          ├─ 插件工具 (plugin tools)
          └─ 内置工具（文件读写等）
```

---

## 六、Hooks 系统

```
外部事件触发入口（HTTP）：
  POST /hooks/<token>
        │
        ▼
  hooks.ts → resolveHooksConfig()
     │
     ├─ token 验证
     ├─ 解析目标 agentId & sessionKey
     ├─ mapping 路由（可将事件路由到不同 session）
     └─ → agentCommand()（复用 Agent 执行路径）

典型使用场景：
  - Gmail 邮件触发 (hooks.gmail)
  - 定时任务 (server-cron.ts)
  - 外部 Webhook
```

---

## 七、插件（Plugin）系统

```
插件类型：
  ├─ Channel Plugin   // 消息渠道（WhatsApp、Telegram 等）
  ├─ Memory Plugin    // 记忆存储（每 Agent 只能一个）
  ├─ Tool Plugin      // 扩展工具（自定义工具）
  └─ Hook Plugin      // 生命周期钩子

加载流程：
  loadGatewayStartupPlugins()
     └─ npm 包 / 本地路径 → 注册到 PluginRegistry
     └─ startPluginServices() → 启动插件服务

Skills（技能）：
  ├─ 本地 skills/  目录（内置）
  ├─ 工作空间 skills（~/.config/openclaw/skills/）
  └─ ClawHub 远程技能（npm 分发）

技能实质是注入到系统提示中的 Markdown 上下文
  buildWorkspaceSkillSnapshot() → 合并进 system prompt
```

---

## 八、多 Agent 架构

```
默认 Agent：agents.defaults 配置

多 Agent 支持：
  agents:
    work:           // 工作 Agent
      model: claude-opus-4
      workspaceDir: ~/work
    personal:       // 个人 Agent
      model: gpt-4o

子 Agent（Subagent）：
  AI 在执行过程中可通过 ACP（Agent Communication Protocol）
  动态 spawn 子 Agent：
    acp-spawn.ts → 创建子 Agent 会话
    acp-spawn-parent-stream.ts → 子 Agent 流式结果回传父 Agent

Lane 并发控制：
  ├─ session lane  // 同一 session 串行
  ├─ global lane   // 全局并发限制
  └─ subagent lane // 子 Agent 独立 lane
```

---

## 九、BOOT.md 引导机制

```
Gateway 启动时检测工作空间下的 BOOT.md
        │
        ▼
  runBootOnce()
     ├─ 读取 BOOT.md 内容
     ├─ 构建 Boot Prompt（指令 AI 按 BOOT.md 操作）
     ├─ 执行 agentCommand()（一次性运行）
     └─ 恢复 session 映射（Boot 运行不污染历史会话）

用途：
  - 启动时发送通知
  - 检查环境状态
  - 执行初始化任务
```

---

## 十、关键数据流总结

```
                    ┌─────────────────┐
  消息入站           │  Channel Plugin  │ ← WhatsApp/Telegram/etc
                    └────────┬─────────┘
                             │ MsgContext
                    ┌────────▼─────────┐
  消息路由           │    Dispatcher    │ 命令 or 普通消息
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
  指令路由           │  getReplyFromConfig │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
  Agent 执行        │  agentCommand()  │ 解析 session/model/workspace
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
  模型推理          │runEmbeddedPiAgent│ 入队 → 认证 → 调用 AI
                    └────────┬─────────┘
                             │ tool_use / text
                    ┌────────▼─────────┐
  工具执行          │  Tool Pipeline   │ 权限检查 → 执行
                    └────────┬─────────┘
                             │ 最终回复文本
                    ┌────────▼─────────┐
  回复分发          │ ReplyDispatcher  │ → 送回原渠道
                    └─────────────────┘
```

---

## 十一、技术栈总览

| 层次 | 技术 |
|------|------|
| 运行时 | Node.js 22/24，TypeScript |
| AI SDK | `@mariozechner/pi-coding-agent`（内嵌 Agent 核心） |
| 消息协议 | WebSocket（内部）+ HTTP REST（控制面） |
| 并发模型 | 基于 Lane 的任务队列（session 级 + 全局级） |
| 配置格式 | TOML（openclaw.toml） |
| 会话存储 | JSON 文件（~/.config/openclaw/sessions/） |
| 插件分发 | npm 包 + ClawHub 平台 |
| 测试框架 | Vitest（单元/集成/E2E） |
| 容器化 | Docker + docker-compose + Podman |
| 守护进程 | launchd（macOS）/ systemd（Linux） |
