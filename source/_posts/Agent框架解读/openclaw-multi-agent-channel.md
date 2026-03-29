---
title: OpenClaw 多 Agent 持久化交互与 Channel-Agent 协作机制深度解读
toc: true
abbrlink: openclaw-multi-agent-channel
date: 2026-03-28 22:16:00
updated: 2026-03-28 22:16:00
author: WorkBuddy
tags:
  - OpenClaw
  - AI Agent
  - 源码解读
  - 多 Agent
  - Channel
  - ACP
  - 协作机制
categories:
  - Agent 框架
---

> **源码路径**: `/Users/zhangquanquan/WorkBuddy/20260327195403/openclaw`  
> **版本**: latest（2026年初）  
> **关键文件**: `src/agents/acp-spawn.ts`、`src/agents/subagent-control.ts`、`src/agents/subagent-announce.ts`、`src/config/types.agents.ts`、`src/channels/plugins/binding-types.ts`

<!-- more -->

## 一、持久化 Agent 之间可以交互吗？

**可以，有两种交互模式**，对应两种 Runtime 类型：

### 1. Subagent 模式（`runtime: "subagent"`）

这是**树状父子通信**模型：

```
Main Agent (持久 Session)
    ├── 调用 sessions_spawn → 创建 Child Agent A
    │       └── Child A 完成后通过 subagent-announce 机制
    │           "自动推送"结果回 Main Agent
    ├── 调用 sessions_spawn → 创建 Child Agent B
    │       └── 同上，push-based 回调
    └── 等待所有子 Agent 的完成事件，然后汇总回复用户
```

关键交互机制来自 `subagent-announce.ts` 的系统提示规范：

> "Auto-announce is push-based. After spawning children, do NOT call sessions_list, sessions_history, exec sleep, or any polling tool. Wait for completion events to arrive as user messages, track expected child session keys, and only send your final answer after ALL expected completions arrive."

这意味着：**子 Agent 完成后不是主动通知，而是由 OpenClaw 基础设施将子 Agent 的最终输出注入到父 Agent 的下一轮 user 消息中**，触发父 Agent 继续运行。

### 2. ACP 模式（`runtime: "acp"`）——持久化 Agent 的核心

这是**独立持久会话**模型，支持真正的"持久化 Agent 互相交互"：

```typescript
// acp-spawn.ts 中的核心逻辑
export const ACP_SPAWN_MODES = ["run", "session"] as const;
//    "run"     = 一次性执行，完成即销毁
//    "session" = 持久化，与特定 thread 绑定，保持活跃

const sessionKey = `agent:${targetAgentId}:acp:${crypto.randomUUID()}`;
// 会话 Key 格式：agent:{agentId}:acp:{uuid}
```

**持久 ACP Session 的生命周期**：

```
Agent A (持久 Session) ──sessions_spawn(runtime="acp", mode="session")──► Agent B (持久 Session)
                                                                              │
                                              ┌───────────────────────────────┘
                                              │  thread=true → 绑定到 channel 的某个子 Thread
                                              │  streamTo="parent" → 实时流式输出回 Agent A
                                              ▼
                                    Agent B 持续运行，接受 follow-up 消息
                                    （通过 thread-binding 的 channel 继续对话）
```

**Agent 间的"steer"（转向）操作**：

`subagent-control.ts` 暴露了完整的控制接口：

```typescript
// 父 Agent 可以向运行中的子 Agent 发送新指令（不等待其完成）
steerControlledSubagentRun({
  controller: { controllerSessionKey: "agent:main:xxx" },
  entry: childRunRecord,
  message: "改变方向：不用分析数据了，直接给出结论",
});

// 父 Agent 可以向子 Agent 发消息并等待回复
sendControlledSubagentMessage({
  message: "当前进度如何？",
});
// 最多等待 30s，返回子 Agent 的最新回复文本

// 父 Agent 可以终止子 Agent（级联杀死整个子树）
killControlledSubagentRun({ entry: childRunRecord });
// cascadeKillChildren 会递归终止所有后代
```

### 3. Agent 间交互能力对比

| 能力 | Subagent (runtime="subagent") | ACP (runtime="acp") |
|------|------------------------------|---------------------|
| 持久化会话 | ❌ 一次性 | ✅ 支持 persistent 模式 |
| 跨 Agent 发消息 | ✅（通过 announce 推送） | ✅（通过 thread binding） |
| 实时转向（steer） | ✅ 支持 | ❌ 不支持 steer |
| 流式输出回父 | 有限（announce 批量） | ✅（streamTo="parent"） |
| 可接受 follow-up | ❌ | ✅ |
| 深度嵌套 | ✅ 支持多层 | ❌ 沙箱中不能 spawn ACP |
| 适用场景 | 并行工作任务分解 | 长期运行的专家 Agent |

---

## 二、一个 Channel 可以和多个 Agent 交互吗？

**可以，这是 OpenClaw 最核心的路由架构之一**，通过 `bindings` 配置实现。

### 1. Channel → Agent 的路由绑定机制

`types.agents.ts` 定义了两种 Binding 类型：

```typescript
// 类型1: Route Binding —— 固定路由，将某 Channel 的对话转发给指定 Agent
export type AgentRouteBinding = {
  type?: "route";
  agentId: string;           // 指向哪个 Agent
  match: AgentBindingMatch;  // 匹配规则
};

// 类型2: ACP Binding —— 动态路由，将某 Channel 的对话绑定到持久化 ACP Agent
export type AgentAcpBinding = {
  type: "acp";
  agentId: string;
  match: AgentBindingMatch;
  acp?: {
    mode?: "persistent" | "oneshot";
    label?: string;
    cwd?: string;
    backend?: string;
  };
};

// 匹配规则可以精确到 channel、账号、用户ID、Discord 角色、Guild 等
export type AgentBindingMatch = {
  channel: string;       // "discord" | "telegram" | "whatsapp" | ...
  accountId?: string;    // 特定账号（多账号场景）
  peer?: { kind: ChatType; id: string };  // 精确到对话类型+ID
  guildId?: string;      // Discord 服务器
  teamId?: string;       // Slack 工作区
  roles?: string[];      // Discord 角色（RBAC！）
};
```

### 2. 一个 Channel 路由多个 Agent 的实现

配置示例（一个 Discord 频道根据角色路由到不同 Agent）：

```yaml
# openclaw.yml 示例配置
bindings:
  # 普通用户 → 默认 main Agent
  - type: route
    agentId: main
    match:
      channel: discord
      accountId: default
      peer:
        kind: channel
        id: "1234567890"

  # 开发者角色 → 代码 Agent (ACP)
  - type: acp
    agentId: codex
    match:
      channel: discord
      accountId: default
      peer:
        kind: channel
        id: "1234567890"
      roles: ["DEVELOPER"]   # ← 按 Discord 角色路由！
    acp:
      mode: persistent

  # 运维 DM → 运维专用 Agent
  - type: route
    agentId: ops-agent
    match:
      channel: discord
      accountId: default
      peer:
        kind: dm           # ← 私信路由
        id: "OPS_USER_ID"
```

### 3. Thread Binding —— Channel 与 Agent 的动态绑定

OpenClaw 还支持**动态 Thread 绑定**（来自 `thread-bindings-policy.ts`）：

```
用户在 Slack 的 #engineering 频道发消息
            │
            ▼
Main Agent 收到消息，决定创建一个专项 Agent
            │  sessions_spawn(thread=true, runtime="acp")
            ▼
OpenClaw 在 Slack 中创建一个子 Thread
            │  并将这个子 Thread 绑定到新建的 ACP Agent
            ▼
后续用户在子 Thread 中的消息直接路由到该 ACP Agent
（绕过 Main Agent，直连 Agent B）
```

这意味着**一个 Channel 可以动态孵化多个绑定到不同 Agent 的子 Thread**。

### 4. Channel 与 Agent 交互关系全景图

```
Discord 频道 #general
    ├── (default)     ──route──► Main Agent (持久 Session)
    │                                │
    │                                └──sessions_spawn(thread=true)──►
    │                                           子 Thread A ──bind──► Agent B (ACP, persistent)
    │
    ├── (role: DEVELOPER) ──acp──► Codex Agent (ACP, persistent)
    │                                  └── 子 Thread B ──bind──► Codex ACP Session
    │
    └── (peer: DM #ops_user) ──route──► Ops Agent

Telegram 群组 #mygroup
    └── (default)     ──route──► Main Agent (共享同一 Agent 实例！)
                                     └── 注意：Session 是按 sender+channel 隔离的
```

**关键点**：多个 Channel 可以路由到同一个 `agentId`（逻辑上同一个 Agent），但每个对话的 **Session 是独立隔离的**（`agent:{agentId}:{channel}:{userId}` 格式）。

---

## 三、协作模式与优秀实践

### 实践一：分层 Orchestrator 模式

```
用户消息 → Main Agent（协调者）
                ├── sessions_spawn("分析数据", label="data-analyst")
                ├── sessions_spawn("编写代码", label="coder")
                └── sessions_spawn("搜索资料", label="researcher")
                        ↓ （三者并行执行）
                所有子任务完成后 announce 回 Main Agent
                Main Agent 汇总结果回复用户
```

**关键注意**（来自源码注释）：子 Agent 完成后**不要轮询**，用 push-based 机制等待。

### 实践二：专家 Agent 持久化绑定（ACP + Thread）

将专业领域 Agent 绑定到特定 Channel 的 Thread：

```yaml
bindings:
  - type: acp
    agentId: security-auditor
    match:
      channel: slack
      peer:
        kind: channel
        id: "C_SECURITY_CHANNEL"
    acp:
      mode: persistent    # 保持会话，记住上下文
      cwd: /opt/security-tools
```

这个 `security-auditor` Agent 会在 `#security` 频道中持续存在，记住所有历史对话。

### 实践三：RBAC 角色路由

利用 Discord roles 或 Slack 权限来路由到不同能力的 Agent：

```yaml
bindings:
  # 普通用户 → 友好的 main Agent
  - type: route
    agentId: main
    match: { channel: discord, peer: { kind: channel, id: "..." } }

  # 有 dev 角色的用户 → 代码 Agent（工具权限更强）
  - type: acp
    agentId: dev-assistant
    match:
      channel: discord
      peer: { kind: channel, id: "..." }
      roles: ["dev", "engineer"]
```

### 实践四：跨 Agent 协作（steer + message）

父 Agent 在子 Agent 运行过程中动态干预：

```typescript
// 父 Agent 通过 subagents 工具发现子 Agent 运行过慢
// 可以 steer（转向）而不是 kill + respawn
sessions_spawn({
  task: "分析这份报告并给出建议",
  label: "report-analyst"
})

// ... 等待一段时间 ...

// 发现方向需要调整，steer 它
subagents_steer({
  target: "report-analyst",   // 按 label 定位
  message: "重点关注安全风险部分，其他不用了"
})
// OpenClaw 会 abort 当前 run，注入新指令，重新启动
```

### 实践五：深度隔离的沙箱子 Agent

`sandbox: "require"` 参数让子 Agent 运行在沙箱中（但注意：沙箱 Session 不能再 spawn ACP，只能 spawn subagent）：

```typescript
sessions_spawn({
  task: "运行这段不可信的代码并给出结果",
  sandbox: "require",     // 必须在沙箱中运行
  runtime: "subagent",    // ACP 不支持 sandbox="require"
})
```

---

## 四、总结

| 问题 | 答案 |
|------|------|
| 持久化 Agent 间能交互吗？ | ✅ 能，ACP session 模式支持持久双向通信；Subagent 模式支持父子 push-based 回调 |
| 一个 Channel 能和多个 Agent 交互吗？ | ✅ 能，通过 bindings 配置 + ThreadBinding 动态绑定实现 1:N 路由 |
| Agent 间如何协作？ | 父生子（spawn）、推送结果（announce）、转向（steer）、发消息（send）、终止（kill） |
| 最佳实践是什么？ | 用 Orchestrator + 并行 Subagent 分解任务；用 ACP persistent 绑定专家 Agent；用 RBAC roles 做渠道级权限隔离 |
