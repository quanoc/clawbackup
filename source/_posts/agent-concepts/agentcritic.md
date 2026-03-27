---
title: Agent的Critic机制
toc: true
abbrlink: agent-critic-mechanism
date: 2026-03-26 00:00:00
updated: 2026-03-26 00:59:00
author: quanoc
tags:
  - Agent
  - AI
  - Critic
  - 技术架构
categories:
  - Agent核心概念
  - 技术架构
---

我用**最直白、不绕弯**的方式给你讲清楚：**Agent 的 Critic（评论家/评判器）机制**到底是什么、干什么、怎么用。

# 一、一句话定义

**Critic 机制 = 给 Agent 打分 + 挑错 + 提改进建议的"AI裁判"**
它不直接执行任务，**只负责评判 Agent 做得好不好**，并把结果反馈给 Agent，让它**自我修正、越做越准**。

# 二、核心作用（3 件事）

1. **打分（Reward）**
   给 Agent 的行动/结果打一个分数（好/坏）。
2. **纠错（Critique）**
   指出哪里错了、哪里不合理、哪里不符合规则。
3. **指导（Refine）**
   告诉 Agent 下一步该怎么改。

# 三、典型工作流程（极简版）

1. Agent 生成一个**方案/回答/动作**
2. Critic 接收 → **评判**
   - 对不对？
   - 全不全？
   - 有没有幻觉？
   - 符不符合约束？
3. Critic 返回**分数 + 改进意见**
4. Agent 根据反馈**重写/重试/优化**
5. 循环直到 Critic 满意

这就是 **Self-Refine（自我迭代）**、**Self-Correction（自我纠错）** 的核心。

# 四、和强化学习（RL）里的 Critic 是一回事吗？

**同源，但现在 LLM Agent 里更广义。**
- 传统 RL：Critic 预测**未来奖励**（Q 值/价值函数），指导 Actor 学习。
- 现代 LLM Agent：Critic 就是**一个专门做评判的 LLM**，负责**即时评判 + 修正**。

可以理解为：
> **Actor（做事） + Critic（评判） = 更稳、更准的 Agent**

# 五、实际例子（最容易懂）

### 场景：让 Agent 写代码
1. Agent 写了一段代码
2. Critic 检查：
   - 有语法错误
   - 逻辑漏洞
   - 没处理边界
3. Critic 返回：
   > 错误：数组越界；建议：增加长度判断
4. Agent 重写 → Critic 再检查 → 通过

### 场景：RAG 问答
1. Agent 生成回答
2. Critic 检查：
   - 是否引用原文？
   - 是否幻觉？
   - 是否跑题？
3. 不合格 → 让 Agent 重新检索+回答

这就是 **Critic-Augmented RAG**。

# 六、Critic 机制的常见形态

1. **单轮评判**：只判一次，过/不过
2. **多轮迭代（Self-Refine）**：反复改到合格
3. **多 Critic 集成**：安全Critic、事实Critic、格式Critic
4. **奖励模型（RM）**：用 LLM 做偏好打分，训练更好的 Agent
5. **工具验证 Critic**：用代码解释器、搜索、计算器当 Critic

# 七、为什么现在都在用 Critic？

- 解决 LLM **幻觉**
- 提升**可靠性**
- 满足**严格规则/格式**
- 让 Agent 从"一次生成"变成**闭环可进化系统**

# 八、一句话总结（背下来就能面试）

> **Critic 机制是 Agent 系统里的"评判模块"，负责对 Agent 的输出进行评估、纠错、打分与反馈，形成自我修正闭环，大幅提升准确性与可靠性。**

---

*原文链接：https://www.doubao.com/thread/a10d3feaa1f23*
