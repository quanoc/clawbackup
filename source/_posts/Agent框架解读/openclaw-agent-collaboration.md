---
title: OpenClaw Agent 协作全景解析
toc: true
abbrlink: openclaw-agent-collaboration
date: 2026-03-29 04:44:00
updated: 2026-03-29 04:44:00
author: WorkBuddy
tags:
  - OpenClaw
  - AI Agent
  - 源码解读
  - 多 Agent
  - ACP
  - A2A
  - Ping-Pong
categories:
---

# Agent 协作解析：spawn、send、ACP、subagent 与 Ping-Pong 的关系与限制

> **源码路径**: `~/WorkBuddy/20260327195403/openclaw`
> **关键文件**: `src/agents/acp-spawn.ts`、`src/agents/tools/sessions-send-tool.ts`、`src/agents/tools/sessions-send-tool.a2a.ts`、`src/agents/tools/sessions-send-helpers.ts`、`src/agents/tools/sessions-spawn-tool.ts`、`src/agents/tools/sessions-helpers.ts`、`src/acp/policy.ts`、`src/plugins/config-state.ts`

<!-- more -->

## 一、背景与问题

在多 Agent 系统中，Agent 之间的协作方式决定了整个系统的灵活性、可靠性和可维护性。OpenClaw 作为一个支持多 Channel（Discord、Telegram、飞书、微信等）的 Agent 网关框架，提供了一套完整的 Agent 协作机制。然而，这套机制涉及多个容易混淆的概念：

- `sessions_spawn` 和 `sessions_send` 是什么关系？
- subagent 和 ACP 有什么区别？它们是互斥的吗？
- A2A（Agent-to-Agent）到底是什么？
- Ping-Pong 协商机制在什么时候触发？
- Thread Binding 对微信 Channel 为什么不可用？
- `mode: "run"` 和 `mode: "session"` 如何选择？

本文从 OpenClaw 源码出发，用一张架构图把这些概念的关系讲清楚，然后逐一深入定义、对比、分析限制，最后给出实践决策建议。

{% tips:question %}
先给出最佳实践！
可以利用拆分多步骤 spawn 子agent + Ping-Pong 协商 机制 让子agent 分步骤 汇报，以防止走偏 而无感知。
- 拆分 spawn + Ping-Pong 是最佳"防走偏 + 汇报"方案

注意⚠️：每次 spawn（run 模式）是一个全新 Session，子agent 没有上一步的记忆。
可以用 mode: "session" 保持 Session（微信上用 subagent + session + thread: false）

注意⚠️⚠️⚠️⚠️⚠️：mode="session" 必须搭配 thread=true 【上一条是错的， 大模型真离谱！！！】
所以只能是 mode="run" 的spawn  + Ping-Pong 协商， 实现子Agent的进度上报，以实现可控、防止走偏无感知。


```
spawn({ mode: "session", task: "设计 Schema" })  → 创建常驻 Session
send({ message: "根据刚才的 Schema 写代码" })     → 有上下文
send({ message: "补充单元测试" })                 → 有完整上下文
```

{% endtips%}

## 二、架构全景图
{% tips:warning %}
了解协作机制是为了让我们更好懂OpenClaw，更好的调教OpenClaw
1. 人到Agent、Agent之间协作 通常涉及有两个核心阶段：创建 Session（spawn）、Session 间通信（send/A2A）
2. 创建 Session（spawn）支持两种方式：subagent、ACP
3. sessions_spawn 有两种模式：mode: "run"、mode: "session"
4. Thread 是把一个子 Session 绑定到一个聊天线程的机制。适用于每个 Agent 独立 Thread，用户直接对话。
{% endtips%}

<!-- <details>
<summary>点击展开 SVG 架构图</summary> -->

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" font-family="'SF Pro Display', -apple-system, 'Segoe UI', sans-serif">
  <defs>
    <marker id="arrow" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="10" markerHeight="7" orient="auto-start-reverse">
      <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="10" markerHeight="7" orient="auto-start-reverse">
      <polygon points="0 0, 10 3.5, 0 7" fill="#3b82f6"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="10" markerHeight="7" orient="auto-start-reverse">
      <polygon points="0 0, 10 3.5, 0 7" fill="#10b981"/>
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="10" markerHeight="7" orient="auto-start-reverse">
      <polygon points="0 0, 10 3.5, 0 7" fill="#f59e0b"/>
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="10" markerHeight="7" orient="auto-start-reverse">
      <polygon points="0 0, 10 3.5, 0 7" fill="#ef4444"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="10" markerHeight="7" orient="auto-start-reverse">
      <polygon points="0 0, 10 3.5, 0 7" fill="#8b5cf6"/>
    </marker>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.10"/>
    </filter>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1200" height="900" rx="12" fill="url(#bgGrad)"/>
  <!-- Title -->
  <text x="600" y="38" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">OpenClaw Agent 协作架构</text>
  <text x="600" y="58" text-anchor="middle" font-size="12" fill="#94a3b8">spawn / send / A2A / Ping-Pong / Thread Binding 关系全景</text>

  <!-- ═══════════════════════════════════════ -->
  <!-- LEFT SECTION: sessions_spawn            -->
  <!-- ═══════════════════════════════════════ -->
  <rect x="30" y="80" width="520" height="780" rx="10" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="30" y="80" width="520" height="40" rx="10" fill="#3b82f6"/>
  <rect x="30" y="110" width="520" height="10" fill="#3b82f6"/>
  <text x="290" y="106" text-anchor="middle" font-size="15" font-weight="700" fill="#ffffff">sessions_spawn — 创建子 Session</text>

  <!-- Agent A box -->
  <rect x="55" y="140" width="140" height="56" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="125" y="163" text-anchor="middle" font-size="13" font-weight="600" fill="#1e40af">Agent A</text>
  <text x="125" y="181" text-anchor="middle" font-size="10" fill="#3b82f6">(发起方 / Requester)</text>

  <!-- Arrow from A to spawn -->
  <line x1="195" y1="168" x2="280" y2="168" stroke="#3b82f6" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <text x="237" y="162" text-anchor="middle" font-size="9" fill="#3b82f6" font-weight="600">调用</text>

  <!-- Spawn decision diamond -->
  <polygon points="370,140 440,168 370,196 300,168" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="370" y="165" text-anchor="middle" font-size="10" font-weight="600" fill="#92400e">runtime</text>
  <text x="370" y="178" text-anchor="middle" font-size="9" fill="#b45309">= ?</text>

  <!-- ═══ LEFT BRANCH: subagent ═══ -->
  <line x1="300" y1="168" x2="170" y2="230" stroke="#10b981" stroke-width="2" marker-end="url(#arrow-green)"/>
  <text x="218" y="196" text-anchor="middle" font-size="11" font-weight="600" fill="#10b981">subagent</text>

  <!-- Subagent box -->
  <rect x="60" y="230" width="210" height="100" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="165" y="253" text-anchor="middle" font-size="13" font-weight="700" fill="#065f46">subagent (embedded)</text>
  <line x1="75" y1="262" x2="255" y2="262" stroke="#d1fae5" stroke-width="1"/>
  <text x="80" y="280" font-size="10.5" fill="#374151">• 运行在 OpenClaw 进程内</text>
  <text x="80" y="296" font-size="10.5" fill="#374151">• 自动继承父 workspace</text>
  <text x="80" y="312" font-size="10.5" fill="#374151">• 支持 attachments / model 覆盖</text>
  <text x="80" y="328" font-size="10.5" fill="#374151">• 轻量级，无独立进程</text>

  <!-- ═══ RIGHT BRANCH: ACP ═══ -->
  <line x1="440" y1="168" x2="365" y2="230" stroke="#8b5cf6" stroke-width="2" marker-end="url(#arrow-purple)"/>
  <text x="418" y="196" text-anchor="middle" font-size="11" font-weight="600" fill="#8b5cf6">ACP</text>

  <!-- ACP box -->
  <rect x="280" y="230" width="250" height="100" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="405" y="253" text-anchor="middle" font-size="13" font-weight="700" fill="#5b21b6">ACP (独立进程)</text>
  <line x1="295" y1="262" x2="515" y2="262" stroke="#ede9fe" stroke-width="1"/>
  <text x="295" y="280" font-size="10.5" fill="#374151">• spawn 独立 CLI 进程 (claude/codex)</text>
  <text x="295" y="296" font-size="10.5" fill="#374151">• 进程间通过 stdin/stdout 通信</text>
  <text x="295" y="312" font-size="10.5" fill="#374151">• 支持 resume / stream</text>
  <text x="295" y="328" font-size="10.5" fill="#374151">• 需要 acpx 插件</text>

  <!-- ═══════════════════════════════════════ -->
  <!-- MODE SECTION: run vs session            -->
  <!-- ═══════════════════════════════════════ -->
  <!-- Subagent mode branching -->
  <line x1="120" y1="330" x2="100" y2="370" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="200" y1="330" x2="220" y2="370" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,3"/>

  <!-- ACP mode branching -->
  <line x1="360" y1="330" x2="340" y2="370" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="450" y1="330" x2="470" y2="370" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="4,3"/>
  <!-- MODE label -->
  <text x="290" y="370" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">mode 参数</text>

  <!-- Subagent: run -->
  <rect x="45" y="385" width="115" height="65" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1"/>
  <text x="102" y="405" text-anchor="middle" font-size="11" font-weight="600" fill="#166534">mode: "run"</text>
  <text x="102" y="421" text-anchor="middle" font-size="9" fill="#4b5563">一次性</text>
  <text x="102" y="435" text-anchor="middle" font-size="9" fill="#4b5563">处理完即退出</text>

  <!-- Subagent: session -->
  <rect x="170" y="385" width="115" height="65" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1"/>
  <text x="227" y="405" text-anchor="middle" font-size="11" font-weight="600" fill="#166534">mode: "session"</text>
  <text x="227" y="421" text-anchor="middle" font-size="9" fill="#4b5563">常驻</text>
  <text x="227" y="435" text-anchor="middle" font-size="9" fill="#4b5563">进程保持运行</text>

  <!-- ACP: run -->
  <rect x="285" y="385" width="115" height="65" rx="6" fill="#faf5ff" stroke="#c4b5fd" stroke-width="1"/>
  <text x="342" y="405" text-anchor="middle" font-size="11" font-weight="600" fill="#5b21b6">mode: "run"</text>
  <text x="342" y="421" text-anchor="middle" font-size="9" fill="#4b5563">一次性</text>
  <text x="342" y="435" text-anchor="middle" font-size="9" fill="#4b5563">处理完进程退出</text>

  <!-- ACP: session -->
  <rect x="410" y="385" width="115" height="65" rx="6" fill="#faf5ff" stroke="#c4b5fd" stroke-width="1"/>
  <text x="467" y="405" text-anchor="middle" font-size="11" font-weight="600" fill="#5b21b6">mode: "session"</text>
  <text x="467" y="421" text-anchor="middle" font-size="9" fill="#4b5563">常驻</text>
  <text x="467" y="435" text-anchor="middle" font-size="9" fill="#4b5563">进程常驻运行</text>

  <!-- ═══════════════════════════════════════ -->
  <!-- THREAD BINDING SECTION                  -->
  <!-- ═══════════════════════════════════════ -->
  <rect x="30" y="470" width="520" height="200" rx="8" fill="#fffbeb" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="6,3"/>
  <text x="55" y="492" font-size="13" font-weight="700" fill="#92400e">Thread Binding 限制矩阵</text>

  <!-- Table header -->
  <rect x="45" y="505" width="195" height="26" rx="4" fill="#f59e0b"/>
  <text x="142" y="522" text-anchor="middle" font-size="10" font-weight="600" fill="#ffffff">subagent</text>
  <rect x="250" y="505" width="195" height="26" rx="4" fill="#f59e0b"/>
  <text x="347" y="522" text-anchor="middle" font-size="10" font-weight="600" fill="#ffffff">ACP</text>
  <!-- Column sub-headers -->
  <text x="100" y="548" text-anchor="middle" font-size="9" fill="#92400e" font-weight="600">thread=false</text>
  <text x="185" y="548" text-anchor="middle" font-size="9" fill="#92400e" font-weight="600">thread=true</text>
  <text x="305" y="548" text-anchor="middle" font-size="9" fill="#92400e" font-weight="600">thread=false</text>
  <text x="390" y="548" text-anchor="middle" font-size="9" fill="#92400e" font-weight="600">thread=true</text>

  <!-- Row: mode=run -->
  <rect x="45" y="556" width="400" height="28" rx="0" fill="#fff7ed"/>
  <text x="55" y="575" font-size="10" fill="#374151" font-weight="500">mode: "run"</text>
  <!-- subagent run + no thread -->
  <rect x="65" y="558" width="60" height="24" rx="4" fill="#dcfce7" stroke="#86efac" stroke-width="1"/>
  <text x="95" y="574" text-anchor="middle" font-size="9" font-weight="600" fill="#166534">✓ 可用</text>
  <!-- subagent run + thread -->
  <rect x="150" y="558" width="60" height="24" rx="4" fill="#fef9c3" stroke="#fde047" stroke-width="1"/>
  <text x="180" y="574" text-anchor="middle" font-size="8" font-weight="600" fill="#854d0e">✓ 需支持</text>
  <!-- acp run + no thread -->
  <rect x="270" y="558" width="60" height="24" rx="4" fill="#dcfce7" stroke="#86efac" stroke-width="1"/>
  <text x="300" y="574" text-anchor="middle" font-size="9" font-weight="600" fill="#166534">✓ 可用</text>
  <!-- acp run + thread -->
  <rect x="355" y="558" width="60" height="24" rx="4" fill="#fef9c3" stroke="#fde047" stroke-width="1"/>
  <text x="385" y="574" text-anchor="middle" font-size="8" font-weight="600" fill="#854d0e">✓ 需支持</text>

  <!-- Row: mode=session -->
  <rect x="45" y="588" width="400" height="28" rx="0" fill="#fffbeb"/>
  <text x="55" y="607" font-size="10" fill="#374151" font-weight="500">mode: "session"</text>
  <!-- subagent session + no thread -->
  <rect x="65" y="590" width="60" height="24" rx="4" fill="#dcfce7" stroke="#86efac" stroke-width="1"/>
  <text x="95" y="606" text-anchor="middle" font-size="9" font-weight="600" fill="#166534">✓ 可用</text>
  <!-- subagent session + thread -->
  <rect x="150" y="590" width="60" height="24" rx="4" fill="#fef9c3" stroke="#fde047" stroke-width="1"/>
  <text x="180" y="606" text-anchor="middle" font-size="8" font-weight="600" fill="#854d0e">✓ 需支持</text>
  <!-- acp session + no thread -->
  <rect x="270" y="590" width="60" height="24" rx="4" fill="#fecaca" stroke="#f87171" stroke-width="1"/>
  <text x="300" y="606" text-anchor="middle" font-size="9" font-weight="700" fill="#991b1b">✗ 禁止</text>
  <!-- acp session + thread -->
  <rect x="355" y="590" width="60" height="24" rx="4" fill="#fef9c3" stroke="#fde047" stroke-width="1"/>
  <text x="385" y="606" text-anchor="middle" font-size="8" font-weight="600" fill="#854d0e">✓ 必须</text>
  <!-- Thread note -->
  <text x="55" y="640" font-size="10" fill="#92400e" font-weight="600">Thread Binding 支持的 Channel:</text>
  <text x="55" y="656" font-size="9.5" fill="#374151">Discord ✓ · Telegram ✓ · Feishu ✓ · Matrix ✓</text>
  <text x="55" y="672" font-size="9.5" fill="#ef4444" font-weight="600">微信 (openclaw-weixin) ✗ — 不支持 Thread Binding</text>

  <!-- Thread definition -->
  <rect x="45" y="682" width="480" height="28" rx="4" fill="#fefce8" stroke="#fde047" stroke-width="1"/>
  <text x="285" y="700" text-anchor="middle" font-size="9.5" fill="#713f12">Thread: 把子 Session 绑定到聊天线程，子 Agent 回复直接投递到该 Thread，而非发起方 Channel</text>

  <!-- ═══════════════════════════════════════ -->
  <!-- RIGHT SECTION: sessions_send / A2A      -->
  <!-- ═══════════════════════════════════════ -->
  <rect x="570" y="80" width="600" height="380" rx="10" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="570" y="80" width="600" height="40" rx="10" fill="#10b981"/>
  <rect x="570" y="110" width="600" height="10" fill="#10b981"/>
  <text x="870" y="106" text-anchor="middle" font-size="15" font-weight="700" fill="#ffffff">sessions_send (A2A) — 向已有 Session 发消息</text>

  <!-- Prerequisite note -->
  <rect x="590" y="130" width="560" height="30" rx="5" fill="#fef2f2" stroke="#fca5a5" stroke-width="1"/>
  <text x="870" y="149" text-anchor="middle" font-size="10" fill="#991b1b" font-weight="600">前提: 目标 Session 必须已存在（通过 sessions_spawn 或 bindings 路由创建）</text>

  <!-- Agent A (right side) -->
  <rect x="600" y="175" width="130" height="50" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="665" y="197" text-anchor="middle" font-size="12" font-weight="600" fill="#1e40af">Agent A</text>
  <text x="665" y="212" text-anchor="middle" font-size="9" fill="#3b82f6">sessions_send()</text>

  <!-- Arrow A → B -->
  <line x1="730" y1="200" x2="830" y2="200" stroke="#10b981" stroke-width="2" marker-end="url(#arrow-green)"/>
  <text x="780" y="193" text-anchor="middle" font-size="9" fill="#10b981" font-weight="600">message</text>

  <!-- Agent B Session -->
  <rect x="835" y="170" width="150" height="60" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
  <text x="910" y="193" text-anchor="middle" font-size="12" font-weight="600" fill="#065f46">Agent B Session</text>
  <text x="910" y="210" text-anchor="middle" font-size="9" fill="#4b5563">(已存在，不管怎么创建的)</text>
  <text x="910" y="224" text-anchor="middle" font-size="8" fill="#94a3b8">subagent / ACP / bindings 均可</text>
  <!-- Round 1 -->
  <text x="910" y="255" text-anchor="middle" font-size="10" font-weight="700" fill="#374151">Round 1: B 处理消息，返回回复</text>

  <!-- Ping-Pong section -->
  <rect x="600" y="268" width="540" height="110" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="620" y="288" font-size="12" font-weight="700" fill="#5b21b6">Ping-Pong 自动协商（后台异步，最多 5 轮）</text>

  <!-- Turn 1 -->
  <rect x="615" y="298" width="245" height="36" rx="5" fill="#ede9fe" stroke="#c4b5fd" stroke-width="1"/>
  <text x="630" y="313" font-size="9.5" fill="#5b21b6" font-weight="600">Turn 1:</text>
  <text x="680" y="313" font-size="9.5" fill="#374151">A 收到 B 的回复 → 判断是否需要补充</text>
  <text x="680" y="327" font-size="8.5" fill="#94a3b8">回复 "REPLY_SKIP" 可提前终止</text>

  <!-- Turn 2 -->
  <rect x="615" y="340" width="245" height="30" rx="5" fill="#ede9fe" stroke="#c4b5fd" stroke-width="1"/>
  <text x="630" y="358" font-size="9.5" fill="#5b21b6" font-weight="600">Turn 2:</text>
  <text x="680" y="358" font-size="9.5" fill="#374151">B 收到 A 的补充 → 继续处理...</text>
  <!-- More turns -->
  <text x="880" y="320" text-anchor="middle" font-size="20" fill="#8b5cf6">. . .</text>
  <text x="880" y="340" text-anchor="middle" font-size="9" fill="#8b5cf6">最多 5 轮</text>

  <!-- Termination -->
  <rect x="950" y="298" width="175" height="72" rx="5" fill="#fef2f2" stroke="#fca5a5" stroke-width="1"/>
  <text x="1037" y="315" text-anchor="middle" font-size="9.5" font-weight="600" fill="#991b1b">终止条件:</text>
  <text x="960" y="332" font-size="9" fill="#374151">• 某方回复 REPLY_SKIP</text>
  <text x="960" y="347" font-size="9" fill="#374151">• 达到 maxPingPongTurns</text>
  <text x="960" y="362" font-size="9" fill="#374151">• 配置: session.agentToAgent.maxPingPongTurns</text>

  <!-- ═══════════════════════════════════════ -->
  <!-- RIGHT BOTTOM: Announce                  -->
  <!-- ═══════════════════════════════════════ -->
  <rect x="570" y="470" width="600" height="200" rx="10" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="570" y="470" width="600" height="36" rx="10" fill="#f59e0b"/>
  <rect x="570" y="496" width="600" height="10" fill="#f59e0b"/>
  <text x="870" y="494" text-anchor="middle" font-size="14" font-weight="700" fill="#ffffff">Announce — 最终结果投递</text>

  <!-- Announce flow -->
  <rect x="600" y="520" width="180" height="50" rx="6" fill="#fef3c7" stroke="#fbbf24" stroke-width="1"/>
  <text x="690" y="542" text-anchor="middle" font-size="10" font-weight="600" fill="#92400e">最终结果</text>
  <text x="690" y="558" text-anchor="middle" font-size="9" fill="#92400e">(Ping-Pong 最后一轮的回复)</text>

  <line x1="780" y1="545" x2="840" y2="545" stroke="#f59e0b" stroke-width="2" marker-end="url(#arrow-amber)"/>

  <!-- Decision: bound or not -->
  <polygon points="910,515 980,545 910,575 840,545" fill="#fef9c3" stroke="#fde047" stroke-width="1.5"/>
  <text x="910" y="541" text-anchor="middle" font-size="9" font-weight="600" fill="#854d0e">Thread</text>
  <text x="910" y="553" text-anchor="middle" font-size="8" fill="#854d0e">绑定?</text>

  <!-- No thread →发起方 Channel -->
  <line x1="910" y1="575" x2="810" y2="620" stroke="#ef4444" stroke-width="1.5" marker-end="url(#arrow-red)"/>
  <text x="840" y="594" font-size="9" fill="#ef4444" font-weight="500">否</text>
  <rect x="710" y="620" width="200" height="35" rx="5" fill="#fef2f2" stroke="#fca5a5" stroke-width="1"/>
  <text x="810" y="641" text-anchor="middle" font-size="10" fill="#991b1b" font-weight="600">投递到发起方 Channel</text>

  <!-- Yes thread → Thread -->
  <line x1="980" y1="545" x2="1030" y2="620" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow-green)"/>
  <text x="1015" y="584" font-size="9" fill="#10b981" font-weight="500">是</text>
  <rect x="980" y="620" width="170" height="35" rx="5" fill="#ecfdf5" stroke="#86efac" stroke-width="1"/>
  <text x="1065" y="641" text-anchor="middle" font-size="10" fill="#166534" font-weight="600">投递到绑定的 Thread</text>

  <!-- ═══════════════════════════════════════ -->
  <!-- BOTTOM: Full lifecycle flow              -->
  <!-- ═══════════════════════════════════════ -->
  <rect x="30" y="790" width="1140" height="60" rx="8" fill="#0f172a"/>
  <text x="600" y="813" text-anchor="middle" font-size="12" font-weight="600" fill="#f8fafc">完整生命周期</text>
  <text x="600" y="835" text-anchor="middle" font-size="11" fill="#94a3b8">
    <tspan fill="#3b82f6" font-weight="700">① sessions_spawn</tspan>
    <tspan fill="#64748b"> (创建 Session) → </tspan>
    <tspan fill="#10b981" font-weight="700">② sessions_send</tspan>
    <tspan fill="#64748b"> (发消息) → </tspan>
    <tspan fill="#8b5cf6" font-weight="700">③ Ping-Pong</tspan>
    <tspan fill="#64748b"> (自动协商) → </tspan>
    <tspan fill="#f59e0b" font-weight="700">④ Announce</tspan>
    <tspan fill="#64748b"> (投递给用户)</tspan>
  </text>
</svg>



<!-- </details> -->

这张图展示了一个核心认知：OpenClaw 的 Agent 协作分为三个独立阶段——**创建 Session**（spawn）、**Session 间通信**（send/A2A）、**通信后协商**（Ping-Pong）——它们各自解决不同的问题，彼此正交，可以自由组合。

## 三、核心概念定义

### 3.1 sessions_spawn：创建子 Session

`sessions_spawn` 是一个 Tool，允许一个 Agent 在其 Tool Loop 中创建新的子 Session。它有两个关键参数决定子任务的运行方式：

- **runtime**: 决定子 Agent 怎么跑。可选 `subagent`（默认，嵌入式）或 `acp`（独立进程）。
- **mode**: 决定子 Session 的生命周期。可选 `run`（一次性）或 `session`（常驻）。
- **thread**: 决定是否绑定到聊天线程，影响回复的投递目标。

源码定义在 `sessions-spawn-tool.ts` 中，`SESSIONS_SPAWN_RUNTIMES = ["subagent", "acp"]` 明确了两种互斥的运行时类型。

### 3.2 sessions_send（A2A）：向已有 Session 发消息

`sessions_send` 是一个 Tool，允许一个 Agent 向另一个已存在的 Session 发送消息。它的核心特征是**不创建 Session**——如果目标 Session 不存在，会直接报错 `No session found with label: xxx`。

源码定义在 `sessions-send-tool.ts` 中。当消息发送成功后，会自动触发后台的 A2A 流程（Ping-Pong + Announce）。

A2A 需要配置权限，通过 `tools.agentToAgent.enabled = true` 和 `tools.agentToAgent.allow` 白名单控制。

### 3.3 subagent：嵌入式运行时

subagent 是 `sessions_spawn` 的默认运行时。子 Agent 运行在 OpenClaw 进程内部，作为父 Agent 的一个函数调用执行。它自动继承父 Agent 的 workspace，支持 attachments 和 model 覆盖，轻量无独立进程开销。

### 3.4 ACP（Agent Communication Protocol）：独立进程运行时

ACP 是另一种运行时选择。子 Agent 作为一个独立的 CLI 进程（如 claude、codex）被 spawn 出来，通过标准输入/输出与 OpenClaw Gateway 通信。它需要 `acpx` 插件提供运行时 backend，支持 session resume 和 stream 输出，但需要额外配置且占用独立进程资源。

### 3.5 Ping-Pong：A2A 的自动协商机制

Ping-Pong 是 `sessions_send` 完成后的后台异步流程。当 Agent A 向 Agent B 发送消息并收到回复后，OpenClaw 会自动在 A 和 B 之间来回传递消息，让双方有机会补充和确认，直到某方回复 `REPLY_SKIP` 或达到最大轮数（默认 5 轮）。

从源码 `sessions-send-tool.a2a.ts` 可以看到，Ping-Pong 的触发条件只依赖三个因素：`maxPingPongTurns > 0`、有发起方 Session、目标不是自己。它**不关心** Session 是 subagent 还是 ACP 创建的，也**不依赖** Thread Binding。

### 3.6 Thread Binding：聊天线程绑定

Thread Binding 是一种将子 Session 绑定到特定聊天线程（如 Discord 帖子、Telegram 话题）的机制。绑定后，子 Agent 的回复会直接投递到该线程，而非发起方的 Channel。只有 Discord、Telegram、飞书、Matrix 四个 Channel 实现了 Thread Binding adapter，微信（openclaw-weixin）不支持。

### 3.7 mode: "run" vs mode: "session"

`mode` 控制子 Session 的生命周期。`run` 模式下子 Session 处理完一个任务后立即结束，资源释放，不能再用 `sessions_send` 往里面发消息。`session` 模式下子 Session 保持活跃，可以反复通过 `sessions_send` 继续交互，子 Agent 保留完整的历史上下文。

## 四、多维度对比

### 4.1 sessions_spawn vs sessions_send

| 维度 | sessions_spawn | sessions_send |
|------|---------------|---------------|
| 本质 | 创建新的子 Session | 向已有 Session 发消息 |
| 前置条件 | Agent 在 `agents.list` 中有定义 | 目标 Session 必须已存在 |
| 是否创建 Session | 是 | 否 |
| runtime 参数 | `subagent` / `acp` | 不涉及（Session 已确定） |
| mode 参数 | `run` / `session` | 不涉及 |
| thread 参数 | 支持 | 不涉及 |
| 典型用途 | 初始化子任务 | 后续交互、补充需求 |

两者是"建房间"和"进房间说话"的关系。必须先 spawn 创建 Session，然后才能 send 向其发消息。

### 4.2 subagent vs ACP

| 维度 | subagent | ACP |
|------|----------|-----|
| 本质 | 嵌入式运行时 | 独立进程运行时 |
| 运行位置 | OpenClaw 进程内 | 独立 CLI 进程 |
| workspace | 自动继承父 Agent | 需要指定或从 binding 读取 |
| attachments | 支持 | 不支持（报错） |
| resumeSessionId | 不支持 | 支持（恢复已有 CLI 会话） |
| streamTo | 不支持 | 支持（流式输出到父 Agent） |
| model 覆盖 | 支持 | 不支持（由 CLI 进程决定） |
| 依赖 | 无 | 需要 acpx 插件 |
| 资源开销 | 轻量 | 重量级（独立进程） |

两者是 `sessions_spawn` 的两种互斥运行时选择，解决"子任务怎么跑"的问题，与通信方式（A2A）无关。

### 4.3 mode: "run" vs mode: "session"

| 维度 | mode: "run" | mode: "session" |
|------|------------|-----------------|
| 生命周期 | 处理完即退出 | 保持活跃 |
| 后续 sessions_send | 不可能（Session 已结束） | 支持（保留上下文） |
| 资源占用 | 用完即释放 | 持续占用 |
| 典型场景 | 搜索、翻译、一次性分析 | 编码项目、长期协作 |
| ACP + thread:false | 允许 | **硬性禁止**（源码强制约束） |

### 4.4 Thread Binding 限制矩阵

| 组合 | 可用性 | 说明 |
|------|--------|------|
| subagent + run + thread=false | 可用 | 所有 Channel |
| subagent + run + thread=true | 需 Channel 支持 | Discord/Telegram/飞书/Matrix |
| **subagent + session + thread=false** | **禁止** | **源码硬约束，直接报错** |
| subagent + session + thread=true | 需 Channel 支持 | Discord/Telegram/飞书/Matrix |
| ACP + run + thread=false | 可用 | 所有 Channel（需 acpx） |
| ACP + run + thread=true | 需 Channel 支持 | Discord/Telegram/飞书/Matrix |
| **ACP + session + thread=false** | **禁止** | 源码硬约束，直接报错 |
| ACP + session + thread=true | 需 Channel 支持 | 必须绑定 Thread |

关键约束来自 `acp-spawn.ts` 第 733-737 行：当 `mode="session"` 且 `thread` 不为 true 时，直接返回错误。这是因为常驻 ACP 进程需要一个 Thread 来持续投递回复，没有 Thread 绑定则回复无处可去。

### 4.5 Ping-Pong 与其他概念的关系

| 维度 | 关系 |
|------|------|
| 与 subagent/ACP | 完全无关，不关心 Session 的运行时类型 |
| 与 Thread Binding | 完全无关，Ping-Pong 在 Gateway 内部通过 `agent.run` 执行 |
| 与 mode | 完全无关，只操作已有 Session |
| 与 sessions_send | Ping-Pong 是 send 的后处理流程，自动触发 |
| 触发条件 | `maxPingPongTurns > 0` + 有发起方 + 目标不是自己 |
| 终止条件 | 某方回复 `REPLY_SKIP` 或达到轮数上限 |
| 配置位置 | `session.agentToAgent.maxPingPongTurns`（默认 5，设为 0 关闭） |

## 五、完整生命周期

一次典型的多 Agent 协作包含四个阶段：

**阶段一：创建 Session（sessions_spawn）**

Agent A 在 Tool Loop 中调用 `sessions_spawn`，根据任务性质选择 runtime（subagent 或 ACP）和 mode（run 或 session）。子 Agent 在新的 Session 中处理初始任务，返回结果给 Agent A。

**阶段二：发送消息（sessions_send / A2A）**

Agent A 调用 `sessions_send` 向已创建的 Session 发送消息。Gateway 通过 `sessions.resolve` 找到目标 Session，检查 A2A 权限后触发 `agent.run`，目标 Agent 处理消息并回复。

**阶段三：自动协商（Ping-Pong）**

`sessions_send` 返回后，后台自动启动 Ping-Pong 流程。Gateway 把目标 Agent 的回复发给发起方 Agent，让发起方判断是否满意；如果需要补充，再把补充内容发回目标 Agent。如此来回最多 5 轮，直到某方回复 `REPLY_SKIP` 或达到上限。整个过程对用户透明。

**阶段四：投递结果（Announce）**

Ping-Pong 结束后，Gateway 把最终结果发给目标 Agent 做最后确认（可通过 `ANNOUNCE_SKIP` 保持沉默），然后根据 Thread 绑定状态投递到对应位置——有 Thread 则投递到 Thread，没有则投递到发起方的 Channel。

## 六、常见错误与排查

### 6.1 "No session found with label: xxx"

`sessions_send` 找不到目标 Session。`sessions_send` 不会自动创建 Session，必须先通过 `sessions_spawn` 或 bindings 路由创建。检查目标 Agent 的 label 是否正确，Session 是否已经被关闭。

### 6.2 "Thread bindings are unavailable for openclaw-weixin"

微信 Channel 不支持 Thread Binding。解决方案：使用 `thread: false` 参数，或改用支持 Thread Binding 的 Channel（Discord/Telegram/飞书/Matrix）。微信上推荐 `runtime: "subagent"` + `thread: false`。

### 6.3 "ACP runtime backend is not configured"

ACP 运行时需要 `acpx` 插件，且该插件默认不在启用列表中。解决方案：在 `openclaw.json` 中添加 `"plugins": { "entries": { "acpx": { "enabled": true } } }` 并配置 `"acp": { "backend": "acpx" }`。

### 6.4 ACP + session + thread=false 报错

这是源码硬约束。ACP 的 `mode: "session"`（常驻模式）必须配合 `thread: true`，因为常驻进程需要 Thread 来持续投递回复。如果 Channel 不支持 Thread Binding，则无法使用 ACP 的常驻模式，只能用 `mode: "run"` 或改用 subagent。

## 七、实践决策指南

### 7.1 选择 runtime：subagent 还是 ACP？

默认选 subagent。它轻量、无额外依赖、自动继承 workspace，覆盖绝大多数场景。只有在以下情况才考虑 ACP：

- 需要独立开发环境（文件系统隔离）
- 需要 resume 之前的编码会话
- 需要流式输出到父 Agent

### 7.2 选择 mode：run 还是 session？

一次性任务选 `run`，多轮交互选 `session`。判断标准是：后续是否需要通过 `sessions_send` 继续往这个 Session 发消息、是否需要子 Agent 保持历史上下文。

### 7.3 是否开启 Thread？

如果 Channel 支持（Discord/Telegram/飞书/Matrix），且希望子 Agent 的回复直接投递到特定线程（而非发起方 Channel），则开启。否则不需要。

### 7.4 微信 Channel 的推荐配置

由于微信不支持 Thread Binding，推荐以下组合：

```json5
// 一次性任务
sessions_spawn({
  agentId: "magerd",
  label: "magerd",
  task: "用户的请求",
  runtime: "subagent",
  mode: "run",
  thread: false
})

// 需要多轮交互
sessions_spawn({
  agentId: "magerd",
  label: "magerd",
  task: "初始任务",
  runtime: "subagent",
  mode: "session",
  thread: false
})
// 后续通过 sessions_send({ label: "magerd", message: "..." }) 继续交互
```

### 7.5 ACP 配置检查清单

如果需要使用 ACP 模式，确保以下配置到位：

1. `plugins.entries.acpx.enabled = true`（启用 acpx 插件）
2. `acp.backend = "acpx"`（指定 ACP backend）
3. `tools.agentToAgent.enabled = true`（开启 A2A 权限）
4. `tools.agentToAgent.allow` 包含相关 Agent ID（白名单）
5. Channel 支持 Thread Binding（如果使用 `mode: "session"`）

## 八、总结

OpenClaw 的 Agent 协作机制可以用一句话概括：**spawn 创建 Session，send 使用 Session，Ping-Pong 协商结果，Announce 投递给用户**。subagent 和 ACP 是 spawn 时的运行时选择，run 和 session 是生命周期选择，Thread Binding 是投递路由选择，Ping-Pong 是通信后处理选择——它们各自独立、正交互补，共同构成了一套灵活而完整的 Multi-Agent 协作框架。

---

## 参考

1. [OpenClaw 源码](https://github.com/nicepkg/openclaw) — `src/agents/acp-spawn.ts`, `src/agents/tools/sessions-send-tool.ts`, `src/agents/tools/sessions-send-tool.a2a.ts`
2. [OpenClaw 多 Agent 持久化交互与 Channel-Agent 协作机制深度解读](https://quanoc.github.io/clawbackup/2026/03/28/openclaw-multi-agent-channel/)
3. [OpenClaw 架构深度解读：核心运行机制](https://quanoc.github.io/clawbackup/2026/03/28/openclaw-architecture/)
