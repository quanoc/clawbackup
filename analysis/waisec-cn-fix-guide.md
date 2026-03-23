# waisec.cn SEO 快速修复指南

> **创建时间**: 2026-03-07 10:40  
> **预计耗时**: 15 分钟  
> **难度**: ⭐⭐☆☆☆ 简单

---

## 🚀 立即修复（按顺序执行）

### 第 1 步：修复 robots.txt（2 分钟）🔴 紧急

找到你的 Hexo 博客的 `source/robots.txt` 文件，修改 Sitemap 地址：

```diff
# source/robots.txt

User-agent: *
Allow: /
Allow: /archives/
Allow: /categories/
Allow: /wk/
Allow: /about/
Disallow: /vendors/
Disallow: /js/
Disallow: /libs/
Disallow: /css/
Disallow: /vendor/
Disallow: /content.json
Disallow: /404.html

- Sitemap: https://ixynova.cn/sitemap.xml
+ Sitemap: https://waisec.cn/sitemap.xml
```

**保存后重新部署**:
```bash
hexo clean
hexo generate
hexo deploy
```

---

### 第 2 步：修复 Hexo 配置（5 分钟）🟡 重要

编辑 Hexo 根目录的 `_config.yml` 文件：

```yaml
# _config.yml

# Open Graph 配置
open_graph:
  twitter_id:
  google_plus:
  fb_admins:
  fb_app_id:
+ title: Nova's Wiki - 个人知识库
+ locale: zh_CN

# 或者检查 theme 配置
# themes/quinoa/_config.yml
```

**同时检查主题配置** `themes/quinoa/_config.yml`:
```yaml
# 确保有以下配置
language: zh-CN
favicon: /favicon.ico
```

**保存后重新部署**:
```bash
hexo clean
hexo generate
hexo deploy
```

---

### 第 3 步：优化文章标题（5 分钟）🟡 重要

检查你的文章 front-matter，确保标题简洁：

```diff
# source/_posts/xxx.md 或 source/wk/xxx/index.md

---
title: Agent 架构详解
-date: 2026-03-01 10:00:00
+date: 2026-03-01 10:00:00
+tags: [AI, Agent, 架构]
+categories: [AI, 大模型]
---
```

**避免过长的标题**:
```diff
- title: [0]平台建设/[03]AI 中台建设/002.AI 中台建设概述
+ title: AI 中台建设概述
```

---

### 第 4 步：优化 URL 结构（可选，30 分钟）🟢 推荐

如果想优化 URL 结构（将中文转为拼音），安装插件：

```bash
cd /path/to/hexo-blog
npm install hexo-permalink-pinyin --save
```

编辑 `_config.yml`:
```yaml
# _config.yml
permalink: :category/:title/
permalink_defaults:
  lang: en

# 启用拼音插件
permalink_pinyin:
  separator: "-"
  lowercase: true
```

**效果对比**:
```
修复前：/wk/算法|AI 与机器学习/000.大模型/01.Agent 构建/
修复后：/suan-fa-ai-yu-ji-qi-xue-xi/da-mo-xing/agent-gou-jian/
```

---

## ✅ 验证修复

### 1. 验证 robots.txt

访问：https://waisec.cn/robots.txt

应该看到：
```txt
Sitemap: https://waisec.cn/sitemap.xml
```

### 2. 验证 OG 标签

访问：https://waisec.cn
右键 → 查看页面源代码

搜索 `og:title` 和 `og:locale`：
```html
<meta property="og:title" content="Nova's Wiki - 个人知识库">
<meta property="og:locale" content="zh_CN">
```

### 3. 验证 sitemap

访问：https://waisec.cn/sitemap.xml

应该能正常访问，没有 404 错误

### 4. 使用 SEO 工具验证

- **Google Search Console**: https://search.google.com/search-console
- **必应网站管理员工具**: https://www.bing.com/webmasters
- **SEO 检查工具**: https://seositecheckup.com/

---

## 📊 修复前后对比

| 项目 | 修复前 | 修复后 |
|------|--------|--------|
| Sitemap 域名 | ❌ ixynova.cn | ✅ waisec.cn |
| OG:title | ❌ "Z" | ✅ "Nova's Wiki - 个人知识库" |
| OG:locale | ❌ en_US | ✅ zh_CN |
| SEO 评分 | 74/100 | 预计 85+/100 |

---

## 🔧 常见问题

### Q1: 修改后多久生效？

**答**: 
- 搜索引擎重新抓取：1-7 天
- Google Search Console 提交后：几小时到 1 天
- 社交媒体缓存：立即清除（使用 Facebook Debugger 等工具）

### Q2: 如何清除社交媒体缓存？

**Facebook**:
https://developers.facebook.com/tools/debug/

**Twitter**:
https://cards-dev.twitter.com/validator

**LinkedIn**:
https://www.linkedin.com/post-inspector/

### Q3: 部署后网站没变化？

**答**: 清除 CDN 缓存：
```bash
# GitHub Pages 通常自动刷新，如未刷新：
# 1. 等待 5-10 分钟
# 2. 强制刷新 Ctrl+F5
# 3. 检查 GitHub Actions 是否部署成功
```

---

## 📈 后续优化建议

修复完成后，可以考虑：

1. **提交搜索引擎**
   ```bash
   # Google Search Console 提交 sitemap
   # 必应网站管理员工具提交 sitemap
   ```

2. **添加结构化数据**
   ```html
   <!-- 在 themes/quinoa/layout/_partial/head.ejs 添加 -->
   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "WebSite",
     "name": "Nova's Wiki",
     "url": "https://waisec.cn"
   }
   </script>
   ```

3. **添加内部链接**
   - 在文章底部添加"相关文章"
   - 添加面包屑导航

4. **性能优化**
   - 图片压缩（tinypng.com）
   - 启用懒加载
   - 精简 CSS/JS

---

## 🎯 检查清单

完成后勾选：

- [ ] robots.txt 中的 Sitemap 地址已修正
- [ ] _config.yml 中 og:title 已修改
- [ ] _config.yml 中 og:locale 已改为 zh_CN
- [ ] 重新部署了网站 (hexo clean && hexo g && hexo d)
- [ ] 验证了 robots.txt 可访问
- [ ] 验证了 sitemap.xml 可访问
- [ ] 检查了页面源代码中的 OG 标签
- [ ] 在 Google Search Console 提交了 sitemap

---

**预计完成时间**: 15 分钟  
**难度**: 简单  
**影响**: SEO 评分从 74 提升到 85+

有任何问题随时问我！🚀
