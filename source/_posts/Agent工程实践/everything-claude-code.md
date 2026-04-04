---
title: Everything Claude Code：AI编码Agent的性能优化系统
tags:
  - AI
  - Claude
  - 开发工具
  - Agent
  - 代码助手
  - 技术调研
abbrlink: 34742
date: 2026-03-28 11:30:00
categories:
  - Agent工程实践
---

## 项目简介

**Everything Claude Code (ECC)** 是一个专为 AI 编码 Agent 设计的性能优化系统，由 Anthropic Hackathon 获奖者 **affaan-m** 开发。该项目在 GitHub 上已获得 **112k+ Stars** 和 **14.7k+ Forks**，是 Claude Code 生态中最受欢迎的配置集合之一。

- **GitHub 地址**: https://github.com/affaan-m/everything-claude-code
- **作者**: affaan-m (Anthropic Hackathon Winner)
- **最新版本**: v1.9.0 (2026年3月发布)
- **许可证**: MIT

> 项目背景：作者自 Claude Code 实验版本发布以来就是 avid 用户，并在 2025 年 9 月的 Anthropic x Forum Ventures 黑客松中，完全使用 Claude Code 构建了 zenith.chat 项目并获奖。

---

## 核心功能和特性

ECC 不仅仅是一组配置文件，而是一个完整的系统，包含以下核心组件：

### 1. 28 个专业化的 Agents（子代理）

项目提供了覆盖多种编程语言和场景的专用代理：

| Agent 类型 | 用途 |
|-----------|------|
| `planner` | 功能实现规划 |
| `architect` | 系统架构设计 |
| `tdd-guide` | 测试驱动开发指导 |
| `code-reviewer` | 代码质量和安全审查 |
| `security-reviewer` | 漏洞分析 |
| `build-error-resolver` | 构建错误修复 |
| `typescript-reviewer` | TypeScript 代码审查 |
| `python-reviewer` | Python 代码审查 |
| `go-reviewer` / `go-build-resolver` | Go 语言支持 |
| `java-reviewer` / `java-build-resolver` | Java/Spring Boot 支持 |
| `rust-reviewer` / `rust-build-resolver` | Rust 语言支持 |
| `kotlin-reviewer` / `kotlin-build-resolver` | Kotlin/Android 支持 |

### 2. 125+ 个 Skills（技能）

Skills 是工作流程定义和领域知识，包括：

- **开发流程**: TDD 工作流、安全审查、E2E 测试、持续学习
- **后端模式**: API 设计、数据库模式、部署模式、Docker 模式
- **前端模式**: React/Next.js 模式、前端幻灯片、Liquid Glass 设计
- **语言特定**: Python/Django、Go、Java/Spring Boot、Rust、Swift、PHP 等
- **高级技能**: 成本感知 LLM 管道、内容哈希缓存、自主循环

### 3. 60 个 Commands（命令）

提供快速执行的斜杠命令：

- `/plan` - 创建实现计划
- `/tdd` - 强制执行 TDD 工作流
- `/code-review` - 代码审查
- `/build-fix` - 修复构建错误
- `/e2e` - 生成 E2E 测试
- `/learn` - 从会话中提取模式
- `/security-scan` - 安全扫描
- `/harness-audit` - 审计 Harness 可靠性

### 4. Hooks（钩子系统）

基于事件触发的自动化：

- **PreToolUse**: 工具执行前（验证、提醒）
- **PostToolUse**: 工具执行后（格式化、反馈）
- **Stop**: 会话结束时（保存状态）
- **SessionStart**: 新会话开始时（加载上下文）

### 5. 跨平台支持

ECC 是目前唯一最大化支持所有主流 AI 编码工具的项目：

| 平台 | 支持状态 | 特点 |
|------|---------|------|
| **Claude Code** | ✅ 原生支持 | 主要目标平台 |
| **Cursor IDE** | ✅ 完整支持 | 15 种 Hook 事件 |
| **OpenAI Codex** | ✅ 完整支持 | App + CLI |
| **OpenCode** | ✅ 完整支持 | 20+ 事件类型 |
| **Antigravity** | ✅ 支持 | 集成工作流程 |

---

## 使用场景和案例

### 场景 1: 新功能开发

```
/everything-claude-code:plan "添加用户 OAuth 认证"
→ planner 创建实现蓝图

/tdd
→ tdd-guide 强制执行测试优先

/code-review
→ code-reviewer 检查工作成果
```

### 场景 2: Bug 修复

```
/tdd
→ 编写重现 bug 的失败测试
→ 实现修复，验证测试通过

/code-review
→ 检查回归问题
```

### 场景 3: 生产环境准备

```
/security-scan
→ security-reviewer 进行 OWASP Top 10 审计

/e2e
→ e2e-runner 测试关键用户流程

/test-coverage
→ 验证 80%+ 覆盖率
```

### 场景 4: Token 优化

ECC 提供了详细的 Token 优化指南：

```json
{
  "model": "sonnet",
  "env": {
    "MAX_THINKING_TOKENS": "10000",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50"
  }
}
```

- 使用 Sonnet 替代 Opus：约 60% 成本降低
- 限制思考 Token：约 70% 隐藏成本降低
- 早期 Context 压缩：提高长会话质量

---

## 安装和使用方式

### 方式 1: 作为插件安装（推荐）

```bash
# 添加 marketplace
/plugin marketplace add affaan-m/everything-claude-code

# 安装插件
/plugin install everything-claude-code@everything-claude-code
```

### 方式 2: 手动安装

```bash
# 克隆仓库
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# 安装依赖
npm install

# 安装规则（选择你需要的语言）
./install.sh typescript    # 或 python、golang、swift、php
```

### 方式 3: npm 包安装

```bash
npm install -g ecc-universal
npx ecc-install typescript
```

---

## 生态系统工具

### 1. Skill Creator（技能创建器）

分析 Git 历史自动生成 Skills：

```bash
/skill-create                    # 分析当前仓库
/skill-create --instincts        # 同时生成 instincts
```

GitHub App 版本: https://github.com/apps/ecc-tools

### 2. AgentShield（安全审计）

在 Claude Code Hackathon 中构建的安全审计工具：

```bash
npx ecc-agentshield scan
npx ecc-agentshield scan --fix   # 自动修复安全问题
```

- 1282 个测试，98% 覆盖率
- 102 个静态分析规则
- 支持红队/蓝队/审计员三代理管道

### 3. Continuous Learning v2（持续学习）

基于 instinct 的学习系统自动学习你的模式：

```bash
/instinct-status        # 查看学习的 instincts
/instinct-export        # 导出 instincts 分享
/evolve                 # 将 instincts 聚合成 skills
```

---

## 亮点和个人评价

### 🌟 项目亮点

1. **实战验证**: 作者经过 10+ 个月的日常使用打磨，构建实际产品的经验总结
2. **跨平台一致**: 首创支持所有主流 AI 编码工具的统一配置方案
3. **社区活跃**: 30+ 贡献者，支持 7 种语言文档
4. **企业级质量**: 1540+ 内部测试通过，生产环境就绪
5. **持续演进**: 从 v1.0 到 v1.9，平均每 2-3 周发布一个版本

### 💡 核心价值

- **不是配置包，而是性能优化系统**: 超越简单的配置集合，提供完整的 Agent Harness 性能优化方案
- **Token 经济学**: 提供详细的 Token 优化策略，显著降低使用成本
- **Memory 持久化**: Hooks 自动保存/加载跨会话上下文
- **持续学习**: 自动从会话中提取模式转化为可重用技能
- **安全第一**: 内置完整的安全审查和扫描机制

### 📝 使用建议

1. **新手**: 从 Shorthand Guide 开始，快速上手核心概念
2. **进阶**: 阅读 Longform Guide，掌握 Token 优化、并行化、验证循环
3. **团队**: 使用 Skill Creator 分析团队代码风格，生成统一规范
4. **企业**: 集成 AgentShield 到 CI/CD 流程，确保代码安全

---

## 相关资源

- **项目主页**: https://github.com/affaan-m/everything-claude-code
- **简短指南**: https://github.com/affaan-m/everything-claude-code/blob/main/the-shortform-guide.md
- **详细指南**: https://github.com/affaan-m/everything-claude-code/blob/main/the-longform-guide.md
- **安全指南**: https://github.com/affaan-m/everything-claude-code/blob/main/the-security-guide.md
- **作者 Twitter**: @affaanmustafa
- **ECC Tools**: https://ecc.tools

---

## 总结

Everything Claude Code 是目前最全面、最成熟的 Claude Code 配置系统。它不仅提供了丰富的 Agents、Skills 和 Commands，更重要的是建立了一套完整的 AI 编码工作流方法论。对于希望提升 AI 编码效率的开发者和团队来说，这是一个值得深入研究和使用的项目。

如果你正在使用 Claude Code 或其他 AI 编码工具，强烈建议尝试 ECC，它可能会显著改变你的开发体验。
