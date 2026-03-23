# AI Daily Report - 每日 AI Agent 深度报告

自动生成高质量的 AI Agent & LLM 深度报告，聚焦架构设计、工程实践与研究洞察。

## 📁 目录结构

```
~/.openclaw/workspace/
├── scripts/
│   ├── ai-daily-report.py      # 主报告生成脚本
│   ├── send-daily-report.sh    # 发送报告脚本（待完善）
│   └── ai-daily-cron           # Cron 配置文件
└── data/
    └── ai-daily-report/
        ├── history.json         # 报告历史记录
        ├── seen_ids.json        # 已推送内容 ID（去重用）
        ├── cron.log             # Cron 执行日志
        └── reports/             # 每期报告 Markdown 文件
            └── ai-daily-YYYY-MM-DD.md
```

## ⏰ 定时任务

**每天上午 9:30** 自动生成报告（上海时间）

Cron 配置：
```bash
30 9 * * * cd /home/admin/.openclaw/workspace && python3 scripts/ai-daily-report.py >> cron.log 2>&1
```

## 🔧 手动操作

### 生成今日报告
```bash
cd /home/admin/.openclaw/workspace
python3 scripts/ai-daily-report.py
```

### 查看历史报告
```bash
ls -lt ~/.openclaw/workspace/data/ai-daily-report/reports/
```

### 查看某期报告
```bash
cat ~/.openclaw/workspace/data/ai-daily-report/reports/ai-daily-2026-03-06.md
```

### 查看历史索引
```bash
cat ~/.openclaw/workspace/data/ai-daily-report/history.json | jq '.reports'
```

### 重置去重记录（重新推送所有内容）
```bash
rm ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json
```

### 查看 Cron 日志
```bash
tail -f ~/.openclaw/workspace/data/ai-daily-report/cron.log
```

## 📊 搜索源

报告从以下主题搜索高质量内容：

1. **架构设计** - Agent architecture patterns, design principles
2. **生产实践** - Production deployment, engineering best practices
3. **研究论文** - arXiv cs.AI, cs.LG 论文
4. **多 Agent 系统** - Multi-agent collaboration, coordination
5. **工具框架** - LangChain, LlamaIndex, Claude Agent SDK
6. **行业洞察** - Anthropic, OpenAI, Google DeepMind 动态
7. **上下文工程** - Memory, context management, RAG

## 🎯 质量评分

每条内容自动评分（1-10 分）：

- **基础分**: 5 分
- **高质量来源** (Anthropic, OpenAI, arXiv 等): +2 分
- **关键主题** (architecture, production, best practice): +1 分
- **近期内容** (2025-2026): +1 分
- **已推送过**: 0 分（过滤掉）

**推送阈值**: 评分 > 0 的内容（即未推送过的）

## 📝 报告格式

每期报告包含：

- 🏗️ 架构设计
- 📊 生产实践
- 🔬 研究论文
- 💡 行业洞察
- 🛠️ 工具框架
- 📰 公司动态

每条包含：
- 标题
- 摘要
- 来源链接
- 质量评分
- 搜索引擎来源

## 🔍 自定义配置

### 修改搜索查询
编辑 `scripts/ai-daily-report.py` 中的 `SEARCH_QUERIES` 列表：

```python
SEARCH_QUERIES = [
    "your custom query here",
    # ...
]
```

### 修改推送时间
编辑 `scripts/ai-daily-cron`：
```bash
# 改为每天早上 8:00
0 8 * * * cd /home/admin/.openclaw/workspace && python3 scripts/ai-daily-report.py >> cron.log 2>&1
```

然后重新安装：
```bash
crontab /home/admin/.openclaw/workspace/scripts/ai-daily-cron
```

### 修改报告保存位置
编辑 `scripts/ai-daily-report.py` 中的 `DATA_DIR`：
```python
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "ai-daily-report"
```

## 📤 推送到 DingTalk（待实现）

目前报告保存到磁盘，推送功能需要完善 `send-daily-report.sh`。

推荐使用 OpenClaw 的 cron skill 来实现推送：

1. 使用 qqbot-cron skill 设置定时推送
2. 或使用 OpenClaw 的原生 cron 功能

## 🛠️ 故障排查

### 报告生成失败
```bash
# 查看日志
tail -100 ~/.openclaw/workspace/data/ai-daily-report/cron.log

# 手动测试
python3 ~/.openclaw/workspace/scripts/ai-daily-report.py
```

### 搜索无结果
检查 searxng 服务是否正常：
```bash
cd ~/.openclaw/workspace/skills/searxng
uv run scripts/searxng.py search "test" -n 3
```

### Cron 未执行
```bash
# 检查 cron 服务状态
systemctl status cron

# 查看系统日志
grep CRON /var/log/syslog | tail -20
```

## 📈 统计信息

查看累计生成报告数量：
```bash
cat ~/.openclaw/workspace/data/ai-daily-report/history.json | jq '.total_generated'
```

查看已去重内容数量：
```bash
cat ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json | jq 'keys | length'
```

---

**维护者**: AI Assistant
**创建日期**: 2026-03-06
**版本**: 1.0.0
