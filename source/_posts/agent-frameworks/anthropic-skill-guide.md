---
title: Anthropic Skill 构建完全指南 - 核心要点解读
toc: true
abbrlink: anthropic-skill-guide
author: 藜诺
date: 2026-03-24 03:58:00
updated: 2026-03-24 03:58:00
tags:
  - AI
  - Agent
  - Skill
  - Claude
  - MCP
categories:
  - Agent框架分析
  - 技术架构
  - AI-Agent
---

> 原文：The Complete Guide to Building Skills for Claude
> 来源：Anthropic 官方资源

## 什么是 Skill？

**Skill** 是一套指令的集合，打包成一个简单的文件夹，教会 Claude 如何处理特定任务或工作流。

**核心价值**：不用每次对话都重新解释偏好、流程和领域专业知识，教 Claude 一次，每次都能受益。

**典型应用场景**：
- 根据规范生成前端设计
- 用一致的方法论进行研究
- 创建符合团队风格指南的文档
- 编排多步骤流程

---

## Skill 与 MCP 的关系

**厨房类比**：
- **MCP** = 专业厨房：提供工具、食材、设备（连接性）
- **Skill** = 食谱：逐步指导如何创造有价值的东西（知识层）

**协作方式**：

| 层面 | MCP | Skill |
|------|-----|-------|
| 功能 | 连接 Claude 到你的服务 | 教会 Claude 高效使用服务 |
| 提供 | 实时数据访问和工具调用 | 捕获工作流和最佳实践 |
| 定义 | Claude 能做什么 | Claude 应该怎么做 |

**为什么重要**：
- ❌ 没有 Skill：用户连接 MCP 后不知道下一步该做什么
- ✅ 有 Skill：预构建工作流自动激活，一致可靠的工具使用，降低学习曲线

---

## Skill 的核心设计原则

### 渐进式披露（三层系统）

1. **第一层（YAML frontmatter）**：始终在系统提示中加载，提供足够信息让 Claude 知道何时使用该 Skill
2. **第二层（SKILL.md 正文）**：当 Claude 认为 Skill 与当前任务相关时加载，包含完整指令
3. **第三层（链接文件）**：Skill 目录中的附加文件，Claude 按需导航和发现

**优势**：最小化 token 使用，同时保持专业 expertise。

### 可组合性
Claude 可同时加载多个 Skill。你的 Skill 应能与其他 Skill 协同工作，不假设自己是唯一能力。

### 可移植性
Skill 在 Claude.ai、Claude Code 和 API 中工作方式相同。创建一次，跨平台使用。

---

## Skill 的文件结构

```
your-skill-name/
├── SKILL.md              # 必需 - 主 Skill 文件
├── scripts/              # 可选 - 可执行代码
│   ├── process_data.py
│   └── validate.sh
├── references/           # 可选 - 按需加载的文档
│   ├── api-guide.md
│   └── examples/
└── assets/               # 可选 - 模板、字体、图标等
    └── report-template.md
```

---

## YAML Frontmatter 规范

**最关键的部分** - 决定 Claude 是否加载你的 Skill。

### 必需字段

```yaml
---
name: your-skill-name           # kebab-case，无空格，无大写
description: What it does and when to use it. Include specific trigger phrases.
---
```

### name 字段规则
- ✅ `kebab-case`：`notion-project-setup`
- ❌ 有空格：`Notion Project Setup`
- ❌ 下划线：`notion_project_setup`
- ❌ 大写：`NotionProjectSetup`

### description 字段规则
**必须包含**：
1. **WHAT** - Skill 做什么
2. **WHEN** - 何时使用（触发条件）

**好例子**：
```yaml
# 好的描述 - 具体可操作
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

# 好的描述 - 包含触发短语
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".
```

**坏例子**：
```yaml
# 太模糊
description: Helps with projects.

# 缺少触发条件
description: Creates sophisticated multi-page documentation systems.

# 太技术化，没有用户触发词
description: Implements the Project entity model with hierarchical relationships.
```

### 安全限制
- **禁止**：XML 尖括号 `< >`
- **禁止**：Skill 名称包含 "claude" 或 "anthropic"（保留）

---

## 三种常见 Skill 类型

### 类型 1：文档与资源创建
**用途**：创建一致、高质量的输出，包括文档、演示文稿、应用、设计、代码等。

**关键技术**：
- 嵌入风格指南和品牌标准
- 模板结构保证一致输出
- 最终确定前的质量检查清单
- 无需外部工具 - 使用 Claude 内置能力

### 类型 2：工作流自动化
**用途**：多步骤流程，受益于一致的方法论，包括跨多个 MCP 服务器的协调。

**关键技术**：
- 带验证门的分步工作流
- 常见结构的模板
- 内置审查和改进建议
- 迭代优化循环

### 类型 3：MCP 增强
**用途**：工作流指导，增强 MCP 服务器提供的工具访问。

**关键技术**：
- 按顺序协调多个 MCP 调用
- 嵌入领域专业知识
- 提供用户原本需要指定的上下文
- 常见 MCP 问题的错误处理

---

## 编写有效 Skill 的最佳实践

### 指令编写建议

**✅ 好**：具体可操作
```markdown
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)
```

**❌ 坏**：太模糊
```markdown
Validate the data before proceeding.
```

### 使用渐进式披露
- 保持 SKILL.md 专注于核心指令
- 将详细文档移到 `references/` 并链接到它
- 保持 SKILL.md 在 5000 词以内

### 包含错误处理
```markdown
## Common Issues
### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect
```

### 引用资源
```markdown
Before writing queries, consult `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes and handling
```

---

## 测试与迭代

### 推荐测试方法

1. **触发测试**
   - ✅ 在明显任务上触发
   - ✅ 在同义请求上触发
   - ❌ 在不相关主题上不触发

2. **功能测试**
   - 验证有效输出生成
   - API 调用成功
   - 错误处理工作正常
   - 边缘情况已覆盖

3. **性能对比**
   - 对比使用 Skill 前后的工具调用次数
   - 对比 token 消耗

### 成功指标

**量化指标**：
- Skill 在 90% 的相关查询上触发
- 工作流在 X 次工具调用内完成
- 每次工作流 0 次失败的 API 调用

**定性指标**：
- 用户不需要提示 Claude 下一步
- 工作流无需用户纠正即可完成
- 跨会话结果一致

---

## 五种实用模式

### 模式 1：顺序工作流编排
**适用**：用户需要按特定顺序执行多步骤流程。

```markdown
## Workflow: Onboard New Customer
### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company

### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification

### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)
```

### 模式 2：多 MCP 协调
**适用**：工作流跨越多个服务。

示例：设计到开发交接
- Phase 1: Figma MCP - 导出设计资源
- Phase 2: Drive MCP - 存储资源
- Phase 3: Linear MCP - 创建开发任务
- Phase 4: Slack MCP - 发送交接摘要

### 模式 3：迭代优化
**适用**：输出质量随迭代提升。

```markdown
## Iterative Report Creation
### Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file

### Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues
3. Regenerate affected sections
4. Re-validate
5. Repeat until quality threshold met
```

### 模式 4：上下文感知工具选择
**适用**：相同结果，根据上下文使用不同工具。

```markdown
## Smart File Storage
### Decision Tree
1. Check file type and size
2. Determine best storage location:
   - Large files (>10MB): Use cloud storage MCP
   - Collaborative docs: Use Notion/Docs MCP
   - Code files: Use GitHub MCP
   - Temporary files: Use local storage
```

### 模式 5：领域特定智能
**适用**：Skill 添加超越工具访问的专业知识。

```markdown
## Payment Processing with Compliance
### Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision
```

---

## 故障排除指南

### Skill 无法上传
**错误**："Could not find SKILL.md in uploaded folder"
- 原因：文件未命名为精确的 SKILL.md（区分大小写）
- 解决：重命名为 SKILL.md，用 `ls -la` 验证

### Skill 不触发
**症状**：Skill 从不自动加载
- 原因：description 字段太泛或缺少触发词
- 解决：修订 description，包含具体触发短语

### Skill 触发过于频繁
**症状**：Skill 在不相关查询上加载
- 解决 1：添加负面触发词
- 解决 2：更具体
- 解决 3：澄清范围

### MCP 连接问题
**检查清单**：
1. 验证 MCP 服务器已连接
2. 检查认证（API key 有效、权限正确）
3. 独立测试 MCP
4. 验证工具名称正确（区分大小写）

---

## 发布与分享

### 当前分发模型

**个人用户**：
1. 下载 Skill 文件夹
2. 压缩为 ZIP
3. 上传到 Claude.ai：Settings > Capabilities > Skills
4. 或放置到 Claude Code skills 目录

**组织级 Skills**：
- 管理员可工作区范围部署
- 自动更新
- 集中管理

### 推荐发布方式

1. **GitHub 托管**
   - 开源 Skill 用公共仓库
   - 清晰的 README（给人看的）
   - 示例用法和截图

2. **MCP 文档中链接**
   - 从 MCP 文档链接到 Skill
   - 解释两者一起使用的价值
   - 提供快速入门指南

3. **创建安装指南**
   ```markdown
   ## Installing the [Your Service] Skill
   1. Download the skill:
      - Clone repo: `git clone https://github.com/yourcompany/skills`
   2. Install in Claude:
      - Open Claude.ai > Settings > Skills
      - Click "Upload skill"
      - Select the skill folder (zipped)
   3. Enable the skill
   4. Test: Ask Claude to perform a task
   ```

---

## 快速检查清单

### 开发前
- [ ] 确定 2-3 个具体用例
- [ ] 确定工具（内置或 MCP）
- [ ] 审阅指南和示例 Skill
- [ ] 规划文件夹结构

### 开发中
- [ ] 文件夹名 kebab-case
- [ ] SKILL.md 存在（精确拼写）
- [ ] YAML frontmatter 有 `---` 分隔符
- [ ] name 字段：kebab-case，无空格，无大写
- [ ] description 包含 WHAT 和 WHEN
- [ ] 无 XML 标签 `< >`
- [ ] 指令清晰可操作
- [ ] 包含错误处理
- [ ] 提供示例
- [ ] 引用文件清晰链接

### 上传后
- [ ] 在明显任务上测试触发
- [ ] 在同义请求上测试触发
- [ ] 验证不在不相关主题上触发
- [ ] 功能测试通过
- [ ] 监控欠触发/过触发
- [ ] 收集用户反馈

---

## 资源与参考

### 官方文档
- [Best Practices Guide](https://docs.anthropic.com/)
- [Skills Documentation](https://docs.anthropic.com/)
- [API Reference](https://docs.anthropic.com/)
- [MCP Documentation](https://modelcontextprotocol.io/)

### 示例 Skill
- [Anthropic Skills GitHub](https://github.com/anthropics/skills)
- Document Skills（PDF、DOCX、PPTX、XLSX 创建）
- Partner Skills Directory（Asana、Atlassian、Canva、Figma、Sentry、Zapier 等）

### 工具
- **skill-creator Skill**：内置 Claude.ai，可从描述生成 Skill
- **Claude Developers Discord**：社区支持

---

## 总结

构建有效 Skill 的关键：

1. **明确的用例** - 解决具体问题
2. **精准的描述** - 包含 WHAT 和 WHEN
3. **渐进式披露** - 三层信息架构
4. **清晰的指令** - 具体、可操作
5. **充分测试** - 触发、功能、性能
6. **持续迭代** - 根据反馈优化

> **预期时间**：使用 skill-creator 工具，首次构建和测试可在 15-30 分钟内完成。
