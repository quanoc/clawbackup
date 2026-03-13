---
name: ai-daily-report
description: 每日 AI Agent 深度报告。自动生成并推送高质量 Agent 架构、工程实践与研究洞察内容。支持去重和历史保存。
metadata: {"openclaw":{"emoji":"🧠"}}
---

# AI Daily Report - 每日 AI Agent 深度报告

自动搜索、筛选和推送 AI Agent & LLM 领域的高质量内容，聚焦架构设计、工程实践与研究洞察。

## 📋 功能

- 🔍 **智能搜索**: 从 12+ 个精心设计的查询中搜索高质量内容
- ⭐ **质量评分**: 自动评分（1-10 分），优先推送高价值内容
- 🔄 **自动去重**: 记录已推送内容，避免重复
- 💾 **历史保存**: 每期报告保存到磁盘，可随时查阅
- ⏰ **定时推送**: 每天上午 9:30 自动推送（可配置）

## 🎯 搜索主题

1. **🏗️ 架构设计** - Agent architecture patterns, design principles
2. **📊 生产实践** - Production deployment, engineering best practices
3. **🔬 研究论文** - arXiv cs.AI, cs.LG 论文
4. **🤖 多 Agent 系统** - Multi-agent collaboration
5. **🛠️ 工具框架** - LangChain, LlamaIndex, Claude Agent SDK
6. **💡 行业洞察** - Anthropic, OpenAI, Google DeepMind 动态
7. **🧠 上下文工程** - Memory, context management, RAG

## 📦 安装

```bash
# 技能已预装，无需额外安装
# 文件位置：~/.openclaw/workspace/scripts/ai-daily-report.py
```

## ⚙️ 配置

### 修改推送时间

编辑 cron 配置：
```bash
crontab -e
# 修改这一行（默认 9:30 AM）：
30 9 * * * cd /home/admin/.openclaw/workspace && python3 scripts/ai-daily-report.py >> data/ai-daily-report/cron.log 2>&1
```

### 修改搜索查询

编辑 `~/.openclaw/workspace/scripts/ai-daily-report.py`：
```python
SEARCH_QUERIES = [
    "your custom query here",
    # ...
]
```

### 修改质量阈值

编辑评分函数 `score_result()` 中的基础分和加分规则。

## 🚀 使用

### 手动生成报告

```bash
cd ~/.openclaw/workspace
python3 scripts/ai-daily-report.py
```

### 查看最新报告

```bash
cat ~/.openclaw/workspace/data/ai-daily-report/reports/ai-daily-$(date +%Y-%m-%d).md
```

### 查看历史报告列表

```bash
ls -lt ~/.openclaw/workspace/data/ai-daily-report/reports/
```

### 查看历史索引

```bash
cat ~/.openclaw/workspace/data/ai-daily-report/history.json | jq '.reports'
```

### 重置去重记录

```bash
rm ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json
# 下次运行时会重新推送所有内容
```

### 查看 Cron 日志

```bash
tail -f ~/.openclaw/workspace/data/ai-daily-report/cron.log
```

## 📊 报告格式

每期报告包含：

```markdown
# 🧠 AI Agent & LLM 深度日报

**日期**: YYYY-MM-DD
**生成时间**: YYYY-MM-DD HH:MM:SS
**本期条目**: N 条

---

## 🏗️ 架构设计 (N)

🔥 **文章标题**
> 摘要内容...

**来源**: domain.com · [查看](url)
**质量评分**: X/10 · **引擎**: search_engine

---

## 📊 统计
- 搜索查询数：12
- 本期精选：N 条
- 累计保存：M 期
```

## 🎯 质量评分规则

| 条件 | 分数 |
|------|------|
| 基础分 | 5 |
| 高质量来源 (Anthropic, OpenAI, arXiv 等) | +2 |
| 关键主题 (architecture, production, best practice) | +1 |
| 近期内容 (2025-2026) | +1 |
| 已推送过 | 0 (过滤) |

**推送**: 评分 > 0 的所有内容

## 📁 文件结构

```
~/.openclaw/workspace/
├── scripts/
│   ├── ai-daily-report.py      # 主报告生成脚本
│   └── ai-daily-cron           # Cron 配置文件
└── data/
    └── ai-daily-report/
        ├── README.md            # 本文档
        ├── history.json         # 报告历史记录
        ├── seen_ids.json        # 已推送内容 ID（去重）
        ├── cron.log             # Cron 执行日志
        └── reports/             # 每期报告
            └── ai-daily-YYYY-MM-DD.md
```

## 💬 推送消息格式

定时任务生成的报告会自动推送到当前会话渠道（DingTalk 群）。

推送消息包含：
- 报告预览（前 1400 字符）
- 完整报告保存位置
- 快速查看命令

## 🛠️ 故障排查

### 报告生成失败
```bash
# 查看日志
tail -100 ~/.openclaw/workspace/data/ai-daily-report/cron.log

# 手动测试
python3 ~/.openclaw/workspace/scripts/ai-daily-report.py
```

### 搜索无结果
检查 searxng 服务：
```bash
cd ~/.openclaw/workspace/skills/searxng
uv run scripts/searxng.py search "test" -n 3
```

### Cron 未执行
```bash
# 检查 cron 服务
systemctl status cron

# 查看系统日志
grep CRON /var/log/syslog | tail -20

# 重新安装 cron
crontab ~/.openclaw/workspace/scripts/ai-daily-cron
```

## 📈 统计查询

```bash
# 累计生成报告数
cat ~/.openclaw/workspace/data/ai-daily-report/history.json | jq '.total_generated'

# 已去重内容数
cat ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json | jq 'keys | length'

# 本期报告条目数
cat ~/.openclaw/workspace/data/ai-daily-report/reports/ai-daily-$(date +%Y-%m-%d).md | grep "本期条目"
```

## 🔧 高级用法

### 导出所有报告链接
```bash
cat ~/.openclaw/workspace/data/ai-daily-report/history.json | \
  jq -r '.reports[].file'
```

### 搜索特定主题的历史报告
```bash
grep -l "LangChain" ~/.openclaw/workspace/data/ai-daily-report/reports/*.md
```

### 批量导出为 HTML
```bash
for f in ~/.openclaw/workspace/data/ai-daily-report/reports/*.md; do
  pandoc "$f" -o "${f%.md}.html"
done
```

## 📝 更新日志

- **v1.0.0** (2026-03-06) - 初始版本
  - 智能搜索和评分
  - 自动去重
  - 历史保存
  - 定时推送

---

**作者**: AI Assistant
**许可**: MIT
**依赖**: Python 3, searxng skill
