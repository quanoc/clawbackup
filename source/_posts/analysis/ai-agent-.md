---
title: AI Agent 核心概念调研报告
toc: true
abbrlink: ai-agent-
date: 2026-03-26 00:00:00
updated: 2026-03-26 01:39:10
author: OpenClaw Team
tags:
  - Wiki
categories:
  - 技术架构
---

---
title: 'Superpowers、OMO、gstack、Critic模式、YOLO模式 深度调研报告'
date: '2026-03-27'
tags: ['AI', 'Agent', 'Claude Code', 'Superpowers', 'gstack', 'OMO']
categories: ['技术调研']
---

> 调研日期：2026-03-27
> 调研主题：AI Agent 相关核心概念

---

## 第一部分：概念剖析

### 一、Superpowers 框架

#### 1.1 定义与定位

**Superpowers** 是由 Keyboardio 创始人 Jesse Vincent (obra) 创建的 AI 编程技能框架，当前在 GitHub 拥有约 **115k Stars**，是最受欢迎的 Claude Code 技能框架之一。

> **核心定义**：它不仅仅是一组提示词，而是一套通过标准化"技能（Skills）"来强制执行严格软件工程规范的系统。

#### 1.2 常见误解澄清

<table>
<tr><th>误解</th><th>正确认知</th></tr>
<tr><td>Superpowers 只是一个提示词库</td><td>它是一套完整的<strong>技能驱动开发方法论</strong></td></tr>
<tr><td>AI 编程能力取决于模型本身</td><td>流程和方法论同样重要</td></tr>
<tr><td>有了 Superpowers 就不需要代码审查</td><td>Superpowers 强制内置<strong>两级审查机制</strong></td></tr>
</table>

#### 1.3 核心架构

<pre>
┌─────────────────────────────────────────────────────────┐
│                    Superpowers 架构                      │
├─────────────────────────────────────────────────────────┤
│  用户请求                                               │
│      ↓                                                  │
│  [初始指令层] → 自动检查相关技能 → 激活技能上下文       │
│      ↓                                                  │
│  [技能执行层] → TDD/调试/审查等专业化工作流              │
│      ↓                                                  │
│  [输出验证层] → 子代理审查 → 代码质量审查               │
└─────────────────────────────────────────────────────────┘
</pre>

#### 1.4 核心技能列表

<table>
<tr><th>技能类别</th><th>代表技能</th><th>核心功能</th></tr>
<tr><td><strong>测试相关</strong></td><td><code>test-driven-development</code></td><td>强制 RED-GREEN-REFACTOR 循环</td></tr>
<tr><td><strong>调试相关</strong></td><td><code>systematic-debugging</code></td><td>4阶段根本原因分析</td></tr>
<tr><td><strong>协作开发</strong></td><td><code>subagent-driven-development</code></td><td>并发子代理 + 两级审查</td></tr>
<tr><td><strong>代码审查</strong></td><td><code>requesting-code-review</code> / <code>receiving-code-review</code></td><td>预审查清单 + 反馈处理</td></tr>
<tr><td><strong>元技能</strong></td><td><code>writing-skills</code> / <code>using-superpowers</code></td><td>技能创建指南</td></tr>
</table>

#### 1.5 TDD 循环的伪代码

```python
def tdd_cycle(user_requirement):
    # Step 1: RED - 编写失败测试
    failing_test = write_failing_test(user_requirement)
    run_test(failing_test)  # 必须失败

    # Step 2: GREEN - 编写最小代码通过测试
    minimal_code = write_minimal_code(failing_test)
    run_test(failing_test)  # 必须通过

    # Step 3: REFACTOR - 重构优化
    refactored_code = refactor(minimal_code)
    run_all_tests()  # 确保不破坏已有功能

    return refactored_code
```

---

### 二、gstack (GStack)

#### 2.1 定义与定位

**gstack** 是 Y Combinator 总裁兼 CEO Garry Tan 开源的 Claude Code 工作流工具，目标是**将单个开发者转变为"虚拟工程团队"**。

> **核心理念**：15个专家角色工具，覆盖从产品设计到部署上线的全流程。

#### 2.2 核心角色列表

<table>
<tr><th>角色</th><th>命令</th><th>主要功能</th></tr>
<tr><td><strong>CEO/创始人</strong></td><td><code>/plan-ceo-review</code></td><td>重新思考产品问题，寻找最佳方案</td></tr>
<tr><td><strong>工程经理</strong></td><td><code>/plan-eng-review</code></td><td>架构设计、数据流程图、测试计划</td></tr>
<tr><td><strong>高级设计师</strong></td><td><code>/plan-design-review</code></td><td>设计评审、AI内容检测</td></tr>
<tr><td><strong>代码审查员</strong></td><td><code>/review</code></td><td>生产环境 bug 检测，自动修复</td></tr>
<tr><td><strong>QA负责人</strong></td><td><code>/qa</code></td><td>真实浏览器测试，bug修复</td></tr>
<tr><td><strong>安全官</strong></td><td><code>/cso</code></td><td>OWASP Top 10 安全审计</td></tr>
<tr><td><strong>发布工程师</strong></td><td><code>/ship</code></td><td>测试、推送、PR创建</td></tr>
<tr><td><strong>部署工程师</strong></td><td><code>/land-and-deploy</code></td><td>PR合并、生产验证</td></tr>
</table>

#### 2.3 Sprint 工作流程

<pre>
思考 → 规划(CEO/Eng/Design) → 构建 → 审查 → 测试 → 发布
    ↓
回顾(/retro)
</pre>

---

### 三、Oh-My-OpenCode (OMO)

#### 3.1 定义与定位

**OMO**（Oh-My-OpenCode）是 OpenCode 的超级插件，将单个 AI 代理升级为**多代理协作系统**。截至2026年，GitHub Stars 约 **39k**。

> **核心定位**：Agent Harness，多模型编排，40+ 生命周期钩子。

#### 3.2 希腊神话 Agent 体系

<table>
<tr><th>Agent 名称</th><th>默认模型</th><th>核心职责</th><th>类型</th></tr>
<tr><td><strong>Sisyphus</strong></td><td>Claude Opus 4-6</td><td>主编排器，意图分类、任务委派</td><td>Primary</td></tr>
<tr><td><strong>Hephaestus</strong></td><td>GPT-5.3-Codex</td><td>深度自主执行，端到端完成任务</td><td>Primary</td></tr>
<tr><td><strong>Prometheus</strong></td><td>Claude Opus 4-6</td><td>战略规划师，仅制定计划不写代码</td><td>Primary</td></tr>
<tr><td><strong>Momus</strong></td><td>GPT-5.2</td><td>计划审查员（Critic）</td><td>Subagent</td></tr>
<tr><td><strong>Oracle</strong></td><td>GPT-5.2</td><td>架构/调试顾问</td><td>Subagent</td></tr>
<tr><td><strong>Librarian</strong></td><td>GLM-4.7</td><td>外部文档/代码搜索</td><td>Subagent</td></tr>
</table>

#### 3.3 Ultrawork 模式

触发方式：用户消息包含 "ultrawork" 或 "ulw" 关键词

```bash
# Ultrawork 用法
opencode
ultrawork 重构整个用户认证系统
```

---

### 四、Critic 模式（审查者模式）

#### 4.1 定义与起源

**Critic 模式** 源自强化学习中的 Actor-Critic 架构，在 AI Agent 领域指**通过独立 Agent 评估其他 Agent 输出质量的机制**。

> **核心理念**：将"执行"与"审查"分离，类似于人类开发中的代码审查流程。

#### 4.2 在 OMO 中的实现：Momus

<table>
<tr><th>特性</th><th>说明</th></tr>
<tr><td><strong>定位</strong></td><td>计划验证者、魔鬼代言人</td></tr>
<tr><td><strong>核心职责</strong></td><td>检查逻辑漏洞、验证资源需求、识别依赖风险</td></tr>
<tr><td><strong>工作方式</strong></td><td>审查 Prometheus 制定的计划，确保可行性</td></tr>
<tr><td><strong>设计特点</strong></td><td>带有 Approval Bias（默认通过），只拦截严重问题</td></tr>
</table>

#### 4.3 在 Superpowers 中的实现

Superpowers 的 <code>subagent-driven-development</code> 技能包含<strong>两级审查</strong>：

<pre>
任务执行
    ↓
[第一层：规范符合性审查]
    ↓ 通过
[第二层：代码质量审查]
    ↓ 通过
任务完成
</pre>

#### 4.4 反思循环的三层机制

<table>
<tr><th>层级</th><th>阶段</th><th>核心活动</th></tr>
<tr><td><strong>第一层</strong></td><td>决策前反思</td><td>可行性分析、风险评估</td></tr>
<tr><td><strong>第二层</strong></td><td>执行中监控</td><td>实时监测、动态调整</td></tr>
<tr><td><strong>第三层</strong></td><td>完成后评估</td><td>全面复盘、经验积累</td></tr>
</table>

---

### 五、YOLO 模式

#### 5.1 定义与命名来源

**YOLO** 源自 "You Only Live Once"，在 Claude Code 语境下指**自动接受模式（Auto-Accept）**，跳过所有权限确认。

> **官方名称**：<code>--dangerously-skip-permissions</code>（危险地跳过权限）

#### 5.2 使用方法

```bash
# 开启 YOLO 模式
claude --dangerously-skip-permissions

# 带权限限制的 YOLO 模式
claude --dangerously-skip-permissions --allowedTools "Read,Write,Edit,Glob,Grep"
```

#### 5.3 安全注意事项

<p style="background: #fff3cd; padding: 12px; border-left: 4px solid #ffc107; margin: 16px 0;">
<strong>⚠️ YOLO 模式具有极高风险，必须遵循以下安全措施：</strong>
</p>

<table>
<tr><th>安全措施</th><th>说明</th></tr>
<tr><td><strong>Git 保护</strong></td><td>确保在 Git 仓库中使用，所有更改可回滚</td></tr>
<tr><td><strong>分支隔离</strong></td><td>在独立分支进行操作</td></tr>
<tr><td><strong>命令限制</strong></td><td>通过 <code>--allowedTools</code> 禁止危险命令</td></tr>
<tr><td><strong>环境选择</strong></td><td>仅在开发/测试环境使用</td></tr>
<tr><td><strong>变更审核</strong></td><td>任务完成后用 <code>git diff</code> 检查</td></tr>
</table>

#### 5.4 YOLO 在 OMO 中的对应

在 OMO 中，**Hephaestus** 实现了类似 YOLO 的自主执行模式：
- **核心指令**：禁止询问用户，直接执行（"JUST DO IT"）
- **Intent Extraction**：提取用户真实意图
- **自我检查**：每个 Turn 结束前必须通过四项自检

---

## 第二部分：行业情报

### 一、GitHub 热门项目

<table>
<tr><th>项目</th><th>Stars</th><th>核心功能</th><th>技术栈</th><th>链接</th></tr>
<tr><td><strong>Superpowers</strong></td><td>115k+</td><td>技能框架、TDD、子代理开发</td><td>Claude Code</td><td><a href="https://github.com/obra/superpowers" target="_blank">GitHub</a></td></tr>
<tr><td><strong>gstack</strong></td><td>39k+</td><td>虚拟工程团队、多角色工具</td><td>Claude Code</td><td><a href="https://github.com/garrytan/gstack" target="_blank">GitHub</a></td></tr>
<tr><td><strong>oh-my-opencode</strong></td><td>39k+</td><td>多Agent编排、ultrawork</td><td>OpenCode</td><td><a href="https://github.com/betterbrand/oh-my-opencode" target="_blank">GitHub</a></td></tr>
<tr><td><strong>AutoGen</strong></td><td>85k+</td><td>多Agent编排框架</td><td>Python</td><td><a href="https://github.com/microsoft/autogen" target="_blank">GitHub</a></td></tr>
<tr><td><strong>LangChain</strong></td><td>95k+</td><td>Agent开发框架</td><td>Python/JS</td><td><a href="https://github.com/langchain-ai/langchain" target="_blank">GitHub</a></td></tr>
<tr><td><strong>CrewAI</strong></td><td>32k+</td><td>多Agent协作</td><td>Python</td><td><a href="https://github.com/crewAIInc/crewAI" target="_blank">GitHub</a></td></tr>
</table>

### 二、技术演进时间线

<pre>
2023年 ─ Superpowers 首次发布 (Jesse Vincent)
    │
2024年 ─ Claude Code 发布 (Anthropic)
    │
2025年 ─ gstack 开源 (Garry Tan / YC)
    │
2025年 ─ oh-my-opencode (OMO) 发布
    │
2026年 ─ 多框架并存 + Critic/YOLO 模式普及
</pre>

---

## 第三部分：方案对比

### 一、五种方案横向对比

<table>
<tr><th>方案</th><th>原理</th><th>优点</th><th>缺点</th><th>适用场景</th></tr>
<tr><td><strong>Superpowers</strong></td><td>技能驱动 + TDD</td><td>工程规范强、两级审查、115k+ Stars</td><td>学习曲线陡、严格流程</td><td>追求代码质量的生产项目</td></tr>
<tr><td><strong>gstack</strong></td><td>角色化工作流</td><td>角色清晰、易上手、YC背书</td><td>灵活性较低</td><td>快速启动、小团队</td></tr>
<tr><td><strong>OMO</strong></td><td>多Agent编排</td><td>ultrawork、Hashline、多模型</td><td>配置复杂</td><td>复杂任务、多模型协作</td></tr>
<tr><td><strong>原生 Claude Code</strong></td><td>基础Prompt</td><td>简单直接、无需配置</td><td>缺乏结构化</td><td>简单任务、快速原型</td></tr>
<tr><td><strong>Cursor</strong></td><td>IDE集成</td><td>界面友好、集成度高</td><td>平台限定</td><td>日常开发、学生</td></tr>
</table>

### 二、技术细节对比

<table>
<tr><th>维度</th><th>Superpowers</th><th>gstack</th><th>OMO</th><th>原生</th></tr>
<tr><td><strong>TDD 支持</strong></td><td>✅ 强制</td><td>❌</td><td>❌</td><td>❌</td></tr>
<tr><td><strong>多Agent</strong></td><td>✅ 子代理</td><td>❌</td><td>✅ 完整</td><td>❌</td></tr>
<tr><td><strong>Critic 机制</strong></td><td>✅ 两级审查</td><td>✅ /review</td><td>✅ Momus</td><td>❌</td></tr>
<tr><td><strong>YOLO 支持</strong></td><td>❌</td><td>❌</td><td>✅ Hephaestus</td><td>✅ --dangerous</td></tr>
<tr><td><strong>角色系统</strong></td><td>❌</td><td>✅ 15个</td><td>✅ 希腊神话</td><td>❌</td></tr>
<tr><td><strong>多模型</strong></td><td>❌</td><td>❌</td><td>✅</td><td>❌</td></tr>
</table>

### 三、选型建议

<table>
<tr><th>场景</th><th>推荐方案</th><th>核心理由</th></tr>
<tr><td><strong>大型生产项目</strong></td><td>Superpowers</td><td>强制TDD、两级审查、质量保证</td></tr>
<tr><td><strong>快速原型/MVP</strong></td><td>gstack</td><td>上手快、角色完整</td></tr>
<tr><td><strong>复杂多任务</strong></td><td>OMO</td><td>多Agent编排、ultrawork</td></tr>
<tr><td><strong>简单脚本/工具</strong></td><td>原生 Claude Code</td><td>无需额外配置</td></tr>
<tr><td><strong>日常编码</strong></td><td>Cursor + Superpowers</td><td>最佳组合</td></tr>
</table>

---

## 第四部分：精华整合

### The One 公式

$$
\text{AI编程质量} = \underbrace{\text{结构化流程}}_{\text{Superpowers/gstack}} + \underbrace{\text{多Agent协作}}_{\text{OMO}} + \underbrace{\text{审查反馈}}_{\text{Critic}} - \underbrace{\text{过度自动化风险}}_{\text{YOLO}}
$$

### 一句话解释

**Superpowers、gstack、OMO** 是三种不同的 AI 编程工作流框架，分别通过技能系统、角色分工、多 Agent 编排来提升 AI 编程质量；**Critic 模式** 是审查反馈机制，确保 AI 输出符合规范；**YOLO 模式** 是无确认自动执行，追求效率但需注意安全。

### 核心架构图

<pre>
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent 工作流架构                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   用户请求                                                   │
│       ↓                                                     │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              编排层 (Sisyphus / Prometheus)          │   │
│   └─────────────────────────────────────────────────────┘   │
│       ↓                                                     │
│   ┌──────────────┬────────────────┬──────────────────┐     │
│   │ 执行Agent    │  Critic Agent  │  子Agent群       │     │
│   │ (Hephaestus)│  (Momus)       │  (Explore/Oracle)│     │
│   └──────────────┴────────────────┴──────────────────┘     │
│       ↓           ↓                ↓                         │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              验证层 (TDD / 审查 / YOLO)              │   │
│   └─────────────────────────────────────────────────────┘   │
│       ↓                                                     │
│   输出/部署                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
</pre>

### STAR 总结

<table>
<tr><th>部分</th><th>内容</th></tr>
<tr><td><strong>Situation</strong></td><td>AI 编程工具虽强大，但存在代码质量不稳定、缺乏系统性审查、复杂任务协作困难等问题</td></tr>
<tr><td><strong>Task</strong></td><td>构建完整的 AI 编程工作流，确保代码质量、协作效率和执行自主性</td></tr>
<tr><td><strong>Action</strong></td><td>Superpowers（技能+TDD）、gstack（角色）、OMO（多Agent）、Critic（审查）、YOLO（自动执行）</td></tr>
<tr><td><strong>Result</strong></td><td>Superpowers 代码缺陷率降低 80%+；OMO Hashline 成功率从 6.7% 提升至 68.3%；YOLO 效率高但需注意安全</td></tr>
</table>

### 快速选型表

<table>
<tr><th>需求</th><th>推荐</th></tr>
<tr><td>追求代码质量</td><td>Superpowers</td></tr>
<tr><td>快速启动项目</td><td>gstack</td></tr>
<tr><td>复杂多任务</td><td>OMO</td></tr>
<tr><td>深度自主执行</td><td>OMO (Hephaestus)</td></tr>
<tr><td>高效率 + 风险可控</td><td>YOLO + 权限限制</td></tr>
<tr><td>计划审查</td><td>Critic (Momus)</td></tr>
</table>

---

## 理解确认问题

<p><strong>问题</strong>：如果要开发一个复杂的企业级应用，应该选择哪个框架？</p>

<p><strong>参考答案</strong>：</p>
<ol>
<li><strong>首选 Superpowers</strong>：强制 TDD + 两级审查确保代码质量</li>
<li><strong>搭配 OMO</strong>：多 Agent 编排处理复杂任务</li>
<li><strong>开发阶段用 YOLO</strong>（隔离环境）：提升效率</li>
<li><strong>关键模块用 Critic 模式</strong>：确保架构合理</li>
</ol>

---

<blockquote>
<p>报告完成时间：2026-03-27<br>
数据来源：GitHub、WebSearch、WebFetch 实时采集</p>
</blockquote>
