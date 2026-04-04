---
title: OpenClaw 子 Agent run/session 模式源码分析
tags:
  - OpenClaw
  - Agent
  - 源码分析
  - 技术架构
  - Agent 框架分析，技术架构
abbrlink: 8082
date: 2026-03-28 11:07:00
categories:
  - Agent框架解读
---

# OpenClaw 子 Agent run/session 模式源码分析

> 分析时间：2026 年 3 月 28 日  
> 源码版本：OpenClaw v2026.2.24

---

## 一、核心源码文件路径

| 文件 | 路径 |
|------|------|
| sessions-spawn-tool.ts | `/opt/openclaw/src/agents/tools/sessions-spawn-tool.ts` |
| subagent-spawn.ts | `/opt/openclaw/src/agents/subagent-spawn.ts` |
| subagent-registry.ts | `/opt/openclaw/src/agents/subagent-registry.ts` |
| sessions-send-tool.ts | `/opt/openclaw/src/agents/tools/sessions-send-tool.ts` |

---

## 二、sessions_spawn 实现流程

```
sessions_spawn 调用
    ↓
spawnSubagentDirect(subagent-spawn.ts)
    ↓
1. 参数解析与验证
2. 模式解析 (resolveSpawnMode)
3. 深度检查 (callerDepth < maxSpawnDepth)
4. 子 Agent 数量检查 (activeChildren < maxChildren)
5. 创建 childSessionKey
6. 调用 Gateway 设置 session 属性 (spawnDepth, model, thinking)
7. 如果 thread=true → 调用 ensureThreadBindingForSubagentSpawn
8. 构建子 Agent 系统提示 (buildSubagentSystemPrompt)
9. 调用 Gateway agent 方法启动子 Agent
10. 注册子 Agent 到注册表 (registerSubagentRun)
11. 触发生命周期钩子 (subagent_spawned)
```

---

## 三、run vs session 模式核心差异

### 3.1 模式定义

```typescript
function resolveSpawnMode(params: {
  requestedMode?: SpawnSubagentMode;
  threadRequested: boolean;
}): SpawnSubagentMode {
  if (params.requestedMode === "run" || params.requestedMode === "session") {
    return params.requestedMode;
  }
  // Thread-bound spawns should default to persistent sessions.
  return params.threadRequested ? "session" : "run";
}
```

### 3.2 生命周期对比

| 维度 | run 模式 | session 模式 |
|------|---------|-------------|
| **设计目标** | 一次性任务执行 | 持久化线程内协作 |
| **thread 绑定** | 不需要 | 必须 (thread=true) |
| **生命周期** | 短暂 (默认 60 分钟归档) | 持久 (无归档时间) |
| **清理策略** | 可配置 | 固定 keep |
| **后续交互** | ❌ 不支持 | ✅ 支持 follow-up |
| **适用场景** | 独立任务、批处理 | 持续对话、复杂工作流 |

### 3.3 关键代码片段

```typescript
// mode="session" 强制要求 thread=true
if (spawnMode === "session" && !requestThreadBinding) {
  return {
    status: "error",
    error: 'mode="session" requires thread=true so the subagent can stay bound to a thread.',
  };
}

// cleanup 策略自动推导
const cleanup =
  spawnMode === "session"
    ? "keep"  // session 模式强制 keep
    : params.cleanup === "keep" || params.cleanup === "delete"
      ? params.cleanup
      : "keep";

// 归档时间设置
const archiveAfterMs = resolveArchiveAfterMs(cfg);
const archiveAtMs =
  spawnMode === "session" ? undefined : archiveAfterMs ? now + archiveAfterMs : undefined;
```

---

## 四、thread=true 限制原因

### 4.1 技术原因

**thread=true 仅在支持线程绑定的渠道可用，目前仅 Discord 支持。**

### 4.2 实现逻辑

```typescript
async function ensureThreadBindingForSubagentSpawn(params: {...}) {
  const hookRunner = params.hookRunner;
  
  // 检查是否有渠道插件注册了 subagent_spawning 钩子
  if (!hookRunner?.hasHooks("subagent_spawning")) {
    return {
      status: "error",
      error: "thread=true is unavailable because no channel plugin registered subagent_spawning hooks.",
    };
  }

  // 调用渠道插件的钩子进行线程绑定
  const result = await hookRunner.runSubagentSpawning({...}, {...});
  
  if (result?.status === "error") {
    return { status: "error", error: result.error };
  }
  
  if (result?.status !== "ok" || !result.threadBindingReady) {
    return {
      status: "error",
      error: "Unable to create or bind a thread for this subagent session.",
    };
  }
  
  return { status: "ok" };
}
```

### 4.3 渠道支持情况

| 渠道 | thread=true 支持 | 原因 |
|------|-----------------|------|
| Discord | ✅ 支持 | 实现了 subagent_spawning 钩子 |
| Dingtalk | ❌ 不支持 | 未实现线程绑定钩子 |
| Telegram | ❌ 不支持 | 未实现线程绑定钩子 |
| QQ | ❌ 不支持 | 未实现线程绑定钩子 |

---

## 五、sessions_send 消息投递机制

### 5.1 执行流程

```
sessions_send 调用
    ↓
1. 解析目标 sessionKey 或 label
2. 检查会话可见性 (visibility guard)
3. 构建发送参数 (deliver=false, lane=AGENT_LANE_NESTED)
4. 调用 Gateway agent 方法发送消息
5. 如果 timeoutSeconds > 0:
   - 调用 agent.wait 等待响应
   - 读取聊天记录获取回复
6. 启动 A2A (Agent-to-Agent) 通知流
7. 返回结果 (runId, status, reply)
```

### 5.2 两种模式下的行为

| 场景 | run 模式子 Agent | session 模式子 Agent |
|------|----------------|-------------------|
| **发送时机** | 子 Agent 运行中或已完成 | 子 Agent 持续活跃 |
| **消息处理** | 正常处理，追加到对话历史 | 正常处理，作为线程内 follow-up |
| **超时行为** | timeoutSeconds 超时后返回 | 可持续接收消息 |
| **通知流** | 触发 A2A 通知 | 不触发完成通知（保持活跃） |

### 5.3 关键参数

```typescript
await callGateway({
  method: "agent",
  params: {
    message: childTaskMessage,
    sessionKey: childSessionKey,
    channel: requesterOrigin?.channel,
    to: requesterOrigin?.to,
    accountId: requesterOrigin?.accountId,
    threadId: requesterOrigin?.threadId,
    idempotencyKey: childIdem,
    deliver: false,  // 不对外投递，内部处理
    lane: AGENT_LANE_NESTED,  // 嵌套 Agent 车道
    extraSystemPrompt: childSystemPrompt,
    thinking: thinkingOverride,
    timeout: runTimeoutSeconds,
    label: label || undefined,
    spawnedBy: spawnedByKey,
  },
  timeoutMs: 10_000,
});
```

---

## 六、子 Agent 消息处理机制

### 6.1 系统提示结构

```typescript
export function buildSubagentSystemPrompt(params: {...}) {
  const lines = [
    "# Subagent Context",
    "",
    `You are a **subagent** spawned by the ${parentLabel} for a specific task.`,
    "",
    "## Your Role",
    `- You were created to handle: ${taskText}`,
    "- Complete this task. That's your entire purpose.",
    `- You are NOT the ${parentLabel}. Don't try to be.`,
    "",
    "## Rules",
    "1. **Stay focused** - Do your assigned task, nothing else",
    `2. **Complete the task** - Your final message will be automatically reported to the ${parentLabel}`,
    "3. **Don't initiate** - No heartbeats, no proactive actions, no side quests",
    "4. **Be ephemeral** - You may be terminated after task completion. That's fine.",
    "5. **Trust push-based completion** - Descendant results are auto-announced back to you; do not busy-poll for status.",
  ];
  return lines.join("\n");
}
```

### 6.2 完成通知流程

```
子 Agent 完成
    ↓
Gateway 触发 lifecycle end 事件
    ↓
subagent-registry.ts 监听事件
    ↓
completeSubagentRun()
    ↓
startSubagentAnnounceCleanupFlow()
    ↓
runSubagentAnnounceFlow()
    ↓
1. 等待子 Agent 输出稳定
2. 读取最新回复
3. 检查是否有活跃的后代子 Agent
4. 构建通知消息
5. 解析投递目标
6. 发送通知
7. 清理子 Agent 会话 (如果 cleanup="delete")
```

---

## 七、决策矩阵：如何选择模式

| 需求 | 推荐模式 | 关键参数 |
|------|----------|----------|
| 一次性任务 | `run` | `mode: "run"` |
| 多轮对话 | `session` | `mode: "session", thread: true` |
| 并行处理 | `run` | `mode: "run"`（多次调用） |
| Discord 线程助手 | `session` | `mode: "session", thread: true` |
| 后台批处理 | `run` | `mode: "run"` |
| 长期项目协作 | `session` | `mode: "session", cleanup: "keep"` |

---

## 八、注意事项

1. **深度限制**：默认最大派生深度为 2 级（`maxSpawnDepth=2`）
2. **子 Agent 数量限制**：默认每个会话最多 5 个活跃子 Agent（`maxChildrenPerAgent=5`）
3. **超时控制**：可通过 `runTimeoutSeconds` 参数设置子 Agent 运行超时
4. **线程绑定依赖**：`session` 模式依赖 channel plugin 实现 `subagent_spawning` hook
5. **跨 Agent 通信**：需要显式配置 `tools.agentToAgent.enabled=true` 才能跨 Agent 发送消息

---

## 九、总结

### 核心差异

- **run 模式**：一次性任务执行，完成后自动归档，适合独立任务和批处理
- **session 模式**：持久化线程内协作，需要 thread=true，适合多轮对话和复杂工作流

### thread=true 限制

- 依赖渠道插件实现 `subagent_spawning` 钩子
- 目前仅 Discord 渠道支持
- dingtalk/Telegram/QQ 等渠道暂不支持

### sessions_send 机制

- 通过 Gateway `agent` 方法内部注入消息
- 使用 `AGENT_LANE_NESTED` 车道
- `deliver=false` 不对外投递
- 触发 A2A 通知流

---

*分析完成时间：2026-03-28T11:07:00+08:00*
