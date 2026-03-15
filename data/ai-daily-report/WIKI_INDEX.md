# AI 每日深度报告 - Wiki 索引

> **更新频率**: 每天早上 9:30 自动生成  
> **内容范围**: AI Agent、大模型、工程实践、研究论文  
> **语言**: 中文翻译版  
> **发布**: GitHub Pages

---

## 📅 最新报告

| 日期 | 报告链接 | 条目数 | 生成时间 |
|------|---------|--------|---------|
| 2026-03-15 | [ai-daily-2026-03-15.md](reports/ai-daily-2026-03-15.md) | 12 条 | 09:46:17 |

---

## 📂 历史报告

### 2026 年 3 月

| 日期 | 报告链接 | 条目数 | 备注 |
|------|---------|--------|------|
| 2026-03-15 | [ai-daily-2026-03-15.md](reports/ai-daily-2026-03-15.md) | 12 条 | ✅ 已发布 |
| 2026-03-14 | [ai-daily-2026-03-14.md](reports/ai-daily-2026-03-14.md) | 12 条 | ✅ 已发布 |
| 2026-03-13 | [ai-daily-2026-03-13.md](reports/ai-daily-2026-03-13.md) | 12 条 | ✅ 已发布 |
| 2026-03-12 | [ai-daily-2026-03-12.md](reports/ai-daily-2026-03-12.md) | 12 条 | ✅ 已发布 |
| 2026-03-11 | [ai-daily-2026-03-11.md](reports/ai-daily-2026-03-11.md) | 12 条 | ✅ 已发布 |
| 2026-03-10 | [ai-daily-2026-03-10.md](reports/ai-daily-2026-03-10.md) | 12 条 | ✅ 已发布 |
| 2026-03-09 | [ai-daily-2026-03-09.md](reports/ai-daily-2026-03-09.md) | 12 条 | ✅ 已发布 |
| 2026-03-08 | [ai-daily-2026-03-08.md](reports/ai-daily-2026-03-08.md) | 12 条 | ✅ 已发布 |
| 2026-03-07 | [ai-daily-2026-03-07.md](reports/ai-daily-2026-03-07.md) | 12 条 | ✅ 已发布 |
| 2026-03-06 | [ai-daily-2026-03-06.md](reports/ai-daily-2026-03-06.md) | 12 条 | ✅ 首发测试 |

---

## 📊 统计信息

| 指标 | 数值 |
|------|------|
| **累计报告数** | 10 期 |
| **累计条目数** | ~120 条 |
| **最早报告** | 2026-03-06 |
| **最新报告** | 2026-03-15 |
| **平均每条报告** | ~12 条 |

---

## 🔍 内容分类

报告内容涵盖以下领域：

| 分类 | 说明 | 典型来源 |
|------|------|---------|
| **🏗️ 架构设计** | AI Agent 架构、设计模式 | Anthropic、LangChain、Google |
| **📊 生产实践** | 工程实践、最佳实践 | McKinsey、MIT、企业博客 |
| **🔬 研究论文** | arXiv 论文、学术研究 | arXiv、大学研究机构 |
| **🛠️ 工具框架** | 开发工具、框架更新 | LangChain、LlamaIndex |
| **💡 行业洞察** | 行业趋势、市场分析 | 咨询公司、科技媒体 |
| **📰 公司动态** | 大厂动态、融资新闻 | Anthropic、OpenAI、Google |

---

## 📝 使用说明

### 在线查看

访问 GitHub Pages 查看最新报告：
```
https://<your-username>.github.io/<repo>/data/ai-daily-report/reports/ai-daily-2026-03-15.html
```

### 本地查看

```bash
# 查看最新报告
cat ~/.openclaw/workspace/data/ai-daily-report/reports/ai-daily-$(date +%Y-%m-%d).md

# 或查看历史报告
ls -lt ~/.openclaw/workspace/data/ai-daily-report/reports/
```

### 搜索特定主题

```bash
# 搜索包含特定关键词的报告
grep -l "Agent" ~/.openclaw/workspace/data/ai-daily-report/reports/*.md

# 搜索特定来源的内容
grep -l "anthropic.com" ~/.openclaw/workspace/data/ai-daily-report/reports/*.md
```

---

## ⚙️ 技术配置

### Cron 任务配置

```cron
# 每天早上 9:30 生成报告
30 9 * * * /home/admin/.openclaw/workspace/scripts/ai-daily-cron-job.sh
```

### 报告生成脚本

- **位置**: `scripts/ai-daily-report.py`
- **功能**: 搜索、筛选、翻译、生成报告
- **翻译**: 使用 Google Translate 自动翻译为中文

### 存储位置

| 类型 | 位置 |
|------|------|
| **报告目录** | `data/ai-daily-report/reports/` |
| **日志文件** | `data/ai-daily-report/cron.log` |
| **历史索引** | `data/ai-daily-report/history.json` |
| **Wiki 索引** | `data/ai-daily-report/WIKI_INDEX.md` |

### GitHub Pages 发布

```bash
# 添加新报告
git add data/ai-daily-report/reports/ai-daily-2026-03-15.md
git add data/ai-daily-report/WIKI_INDEX.md

# 提交
git commit -m "📰 AI Daily Report: 2026-03-15 (12 条)"

# 推送
git push origin main
```

---

## 📧 更新通知

**当前配置**: 
- ✅ 保存到 Wiki
- ✅ 发布到 GitHub Pages
- ❌ 不推送钉钉

**查看更新**:
1. 访问 GitHub Pages 网站
2. 查看最新报告文件
3. 订阅 Git 仓库更新通知

---

## 🔗 相关链接

- [GitHub 仓库](https://github.com/<your-username>/<repo>)
- [GitHub Pages](https://<your-username>.github.io/<repo>)
- [报告生成脚本](../../../scripts/ai-daily-report.py)
- [Cron 任务配置](../../../scripts/ai-daily-cron-job.sh)

---

## 📈 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-03-15 | ✅ 新增 GitHub Pages 发布功能 |
| 2026-03-15 | ✅ 更新 Wiki 索引模板 |
| 2026-03-06 | ✅ AI 日报系统上线 |

---

**最后更新**: 2026-03-15 09:53  
**维护者**: AI Assistant  
**发布平台**: GitHub Pages

---

*注：报告每日早上 9:30 自动生成并更新到 GitHub Pages*
