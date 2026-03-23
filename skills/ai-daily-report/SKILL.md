---
name: ai-daily-report
description: 每日 AI Agent 深度报告。智能搜索、去重优化、质量评分，生成高质量 Agent 架构与工程实践内容。
metadata: {"openclaw":{"emoji":"🧠"}}
---

# AI Daily Report - 每日 AI Agent 深度报告

自动搜索、筛选和推送 AI Agent & LLM 领域的高质量内容，聚焦架构设计、工程实践与研究洞察。

## 📋 功能特性

### 核心功能
- 🔍 **智能搜索**: 从 14+ 个精心设计的查询中搜索高质量内容
- ⭐ **质量评分**: 自动评分（1-10 分），优先推送高价值内容
- 🔄 **智能去重**: 
  - 基于 URL 和标题哈希去重
  - 仅保留最近 2 天的新内容
  - 与昨日报告对比去重
- 💾 **历史保存**: 每期报告保存到磁盘，可随时查阅
- 📝 **格式统一**: 统一使用 13 号报告格式（英文摘要 + 中文分类）
- 🌐 **中文翻译**: 可选中文翻译（使用 `--translate` 参数）
- 🚀 **Hexo 集成**: 自动部署到 GitHub Pages

---

## 🎯 搜索主题

| 分类 | 查询关键词 | 优先级 |
|------|-----------|--------|
| **🏗️ 架构设计** | AI agent architecture patterns design principles | P0 |
| **📊 生产实践** | AI agent production deployment best practices | P0 |
| **🔬 研究论文** | AI agent research paper arxiv cs.AI cs.LG | P0 |
| **🤖 多 Agent 系统** | multi-agent systems coordination collaboration | P1 |
| **🛠️ 工具框架** | LangChain LlamaIndex agent engineering | P1 |
| **💡 行业洞察** | Anthropic OpenAI Google DeepMind AI trends | P1 |
| **🧠 上下文工程** | AI agent memory context management RAG | P2 |
| **📰 公司动态** | AI company funding acquisition launch | P2 |

---

## 📦 安装

```bash
# 技能已预装，无需额外安装
# 文件位置：~/.openclaw/workspace/scripts/ai-daily-report.py
# Skill 位置：~/.openclaw/workspace/skills/ai-daily-report/
```

---

## ⚙️ 配置

### 基础配置

```python
# 在 ai-daily-report.py 中配置
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "ai-daily-report"
HEXO_SITE = Path.home() / ".openclaw" / "workspace" / "hexo-site"

# 去重配置
DEDUP_DAYS = 2  # 保留最近 2 天的内容
```

### 定时任务配置

```bash
# 编辑 cron 配置
crontab -e

# 每天早上 9:30 生成报告（仅保存到 Wiki）
30 9 * * * cd /home/admin/.openclaw/workspace && python3 scripts/ai-daily-report.py --translate

# 或手动执行
cd ~/.openclaw/workspace
python3 scripts/ai-daily-report.py --translate
```

### Hexo 部署配置

```yaml
# hexo-site/_config.yml
deploy:
  type: git
  repo: git@github.com:quanoc/clawbackup.git
  branch: page
```

---

## 🚀 使用方式

### 基本用法

```bash
# 生成今日报告（英文）
cd ~/.openclaw/workspace
python3 scripts/ai-daily-report.py

# 生成今日报告（中文翻译版）
python3 scripts/ai-daily-report.py --translate

# 生成报告并部署到 GitHub Pages
python3 scripts/ai-daily-report.py --translate --deploy
```

### 查看报告

```bash
# 查看最新报告
cat ~/.openclaw/workspace/data/ai-daily-report/reports/ai-daily-$(date +%Y-%m-%d).md

# 查看历史报告
ls -lt ~/.openclaw/workspace/data/ai-daily-report/reports/

# 查看报告统计
cat ~/.openclaw/workspace/data/ai-daily-report/history.json | jq '.total_generated'
```

### 去重管理

```bash
# 查看已去重内容数量
cat ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json | jq 'keys | length'

# 重置去重记录（重新推送所有内容）
rm ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json

# 查看昨日报告用于对比
cat ~/.openclaw/workspace/data/ai-daily-report/reports/ai-daily-$(date -d "yesterday" +%Y-%m-%d).md
```

---

## 📊 报告格式（13 号格式标准）

### 标准格式

```markdown
# 🧠 AI Agent & LLM 深度日报

**日期**: YYYY-MM-DD
**生成时间**: YYYY-MM-DD HH:MM:SS
**本期条目**: N 条

---

## 🏗️ 架构设计 (N)

🔥 **文章标题**
> 摘要内容（英文原文，保留关键信息）...

**来源**: domain.com · **质量评分**: X/10 · **引擎**: search_engine · [查看](url)

---

## 📊 生产实践 (N)

...

---

## 🔬 研究论文 (N)

...

---

## 🛠️ 工具框架 (N)

...

---

## 📰 公司动态 (N)

...

---

## 📚 其他资源 (N)

...

---

## 📊 本期概览与统计

- **搜索查询数**: 14
- **本期精选**: N 条
- **累计保存**: M 期
- **去重过滤**: X 条（与昨日重复）
- **评分维度**: 核心价值（40）+ 内容深度（30）+ 实用性（20）+ 时效性（10）

---

*本报告由 AI 日报生成器自动生成*
*聚焦高质量代理架构、工程实践与研究分析*
```

---

## 🎯 质量评分规则

### 评分标准

| 维度 | 权重 | 说明 |
|------|------|------|
| **核心价值** | 40 分 | 内容对 AI 开发者的核心价值 |
| **内容深度** | 30 分 | 技术深度和分析深度 |
| **实用性** | 20 分 | 实际应用场景和可操作性 |
| **时效性** | 10 分 | 内容新鲜度（2025-2026） |

### 加分规则

| 条件 | 加分 |
|------|------|
| 基础分 | 5 分 |
| 高质量来源（Anthropic、OpenAI、arXiv、MIT 等） | +2 分 |
| 关键主题（architecture、production、best practice） | +1 分 |
| 近期内容（2026 年） | +1 分 |
| Sebastian Raschka、Andrej Karpathy 等专家内容 | +1 分 |
| 已推送过（去重） | 0 分（过滤） |

### 质量等级

| 评分 | 等级 | 图标 | 说明 |
|------|------|------|------|
| 9-10 | 🔥 必读 | 🔥 | 极高价值内容 |
| 7-8 | ✨ 推荐 | ✨ | 高质量内容 |
| 5-6 | 📌 参考 | 📌 | 一般参考内容 |
| <5 | ❌ 过滤 | - | 不收录 |

---

## 🔄 去重逻辑

### 去重策略

```python
# 1. 基于 URL 和标题生成唯一 ID
def generate_item_id(title, url):
    content = f"{title}:{url}"
    return hashlib.md5(content.encode()).hexdigest()[:16]

# 2. 仅保留最近 2 天的新内容
def filter_recent_results(results, days=2):
    cutoff = datetime.now() - timedelta(days=days)
    return [r for r in results if get_publish_date(r) >= cutoff]

# 3. 与昨日报告对比去重
def dedup_with_yesterday(today_results, yesterday_file):
    yesterday_ids = load_seen_ids(yesterday_file)
    return [r for r in today_results if generate_item_id(...) not in yesterday_ids]
```

### 去重流程

```
搜索结果 (70-100 条)
    ↓
质量评分过滤 (评分>0)
    ↓
最近 2 天内容过滤
    ↓
与昨日报告对比去重
    ↓
URL 去重
    ↓
最终结果 (10-15 条)
```

---

## 📁 文件结构

```
~/.openclaw/workspace/
├── scripts/
│   ├── ai-daily-report.py      # 主报告生成脚本
│   ├── ai-daily-cron-job.sh    # Cron 执行脚本
│   └── translate-zh.py         # 中文翻译工具
├── skills/
│   └── ai-daily-report/
│       └── SKILL.md            # 技能文档（本文件）
├── hexo-site/
│   └── source/
│       └── ai-daily-report/    # Hexo 博客目录
│           ├── index.md        # Wiki 索引
│           └── reports/        # 报告文件
└── data/
    └── ai-daily-report/
        ├── README.md           # 使用说明
        ├── WIKI_INDEX.md       # Wiki 索引页面
        ├── history.json        # 报告历史记录
        ├── seen_ids.json       # 已推送内容 ID（去重）
        ├── cron.log            # Cron 执行日志
        └── reports/            # 每期报告
            └── ai-daily-YYYY-MM-DD.md
```

---

## 🌐 Hexo 部署流程

### 自动部署

```bash
# 生成报告后自动部署
python3 scripts/ai-daily-report.py --translate --deploy
```

### 手动部署

```bash
# 1. 复制报告到 Hexo 目录
cp data/ai-daily-report/reports/ai-daily-2026-03-15.md \
   hexo-site/source/ai-daily-report/reports/

# 2. 更新 Wiki 索引
cp data/ai-daily-report/WIKI_INDEX.md \
   hexo-site/source/ai-daily-report/index.md

# 3. 生成并部署
cd hexo-site
hexo clean && hexo generate && hexo deploy
```

### GitHub Pages 访问

```
https://quanoc.github.io/clawbackup/ai-daily-report/
https://quanoc.github.io/clawbackup/ai-daily-report/reports/ai-daily-2026-03-15.html
```

---

## 🛠️ 故障排查

### 报告生成失败

```bash
# 查看日志
tail -100 ~/.openclaw/workspace/data/ai-daily-report/cron.log

# 手动测试
python3 ~/.openclaw/workspace/scripts/ai-daily-report.py --translate

# 检查 Python 依赖
pip3 list | grep deep-translator
```

### 搜索无结果

```bash
# 检查 searxng 服务
cd ~/.openclaw/workspace/skills/searxng
uv run scripts/searxng.py search "test" -n 3

# 检查 SearXNG URL
echo $SEARXNG_URL
```

### 去重失效

```bash
# 检查 seen_ids.json 格式
cat ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json | jq '.'

# 重置去重记录
rm ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json

# 重新生成
python3 scripts/ai-daily-report.py
```

### Hexo 部署失败

```bash
# 检查 Hexo 配置
cd hexo-site
hexo clean

# 检查 Git 配置
git remote -v

# 重新部署
hexo generate && hexo deploy
```

---

## 📈 统计与监控

### 基础统计

```bash
# 累计生成报告数
cat ~/.openclaw/workspace/data/ai-daily-report/history.json | jq '.total_generated'

# 已去重内容数
cat ~/.openclaw/workspace/data/ai-daily-report/seen_ids.json | jq 'keys | length'

# 本期报告条目数
cat ~/.openclaw/workspace/data/ai-daily-report/reports/ai-daily-$(date +%Y-%m-%d).md | grep "本期条目"
```

### 内容分析

```bash
# 搜索特定主题的报告
grep -l "LangChain" ~/.openclaw/workspace/data/ai-daily-report/reports/*.md

# 统计各分类文章数
grep -c "🏗️架构设计" ~/.openclaw/workspace/data/ai-daily-report/reports/*.md

# 查看质量分布
grep "质量评分" ~/.openclaw/workspace/data/ai-daily-report/reports/ai-daily-*.md | \
  grep -oE '[8-9]/10|10/10' | wc -l
```

---

## 🔧 高级用法

### 自定义搜索查询

```python
# 在 ai-daily-report.py 中修改
SEARCH_QUERIES = [
    "your custom query here",
    "AI agent specific topic",
    # ...
]
```

### 调整去重天数

```python
# 修改去重天数（默认 2 天）
DEDUP_DAYS = 3  # 保留最近 3 天的内容
```

### 修改质量阈值

```python
# 修改最低收录分数（默认>0）
MIN_SCORE = 6  # 只收录 6 分以上的内容
```

### 批量导出报告

```bash
# 导出所有报告链接
cat ~/.openclaw/workspace/data/ai-daily-report/history.json | \
  jq -r '.reports[].file'

# 批量导出为 HTML
for f in ~/.openclaw/workspace/data/ai-daily-report/reports/*.md; do
  pandoc "$f" -o "${f%.md}.html"
done

# 打包下载
tar -czf ai-daily-reports.tar.gz \
  ~/.openclaw/workspace/data/ai-daily-report/reports/
```

---

## 📝 更新日志

### v1.1.0 (2026-03-15)
- ✅ 优化去重逻辑（仅保留最近 2 天新内容）
- ✅ 添加与昨日报告对比去重
- ✅ 统一报告格式（13 号格式标准）
- ✅ 集成 Hexo 部署到 GitHub Pages
- ✅ 添加质量评分维度说明
- ✅ 优化分类结构

### v1.0.0 (2026-03-06)
- ✅ 初始版本
- ✅ 智能搜索和评分
- ✅ 自动去重
- ✅ 历史保存
- ✅ 定时推送

---

## 📚 相关资源

- [SearXNG 技能文档](../searxng/SKILL.md)
- [Hexo 部署文档](../../../hexo-site/DEPLOYMENT.md)
- [AI 日报 Wiki](https://quanoc.github.io/clawbackup/ai-daily-report/)

---

**作者**: AI Assistant  
**许可**: MIT  
**依赖**: Python 3, searxng skill, deep-translator (可选)  
**最后更新**: 2026-03-15
