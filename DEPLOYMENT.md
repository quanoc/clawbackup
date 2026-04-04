# Hexo + Quinoa 主题部署完成

## ✅ 部署状态

**部署时间**: 2026-03-14 02:17 GMT+8  
**站点地址**: http://localhost:4000/  
**主题**: Quinoa (from git@github.com:quanoc/hexo-theme-Quinoa.git)

## 📁 项目结构

```
/home/admin/.openclaw/workspace/claw-wiki/
├── _config.yml              # 站点配置
├── themes/Quinoa/           # Quinoa 主题
│   └── _config.yml          # 主题配置
├── source/                  # 源文件
│   ├── _posts/              # 文章
│   └── about/               # 页面
├── scaffolds/               # 模板
└── public/                  # 生成的静态文件
```

## 🎯 已完成配置

### 站点配置 (`_config.yml`)
- ✅ 主题：Quinoa
- ✅ 永久链接：`wiki/:abbrlink/`
- ✅ 短链接插件：hexo-abbrlink (crc32 + hex)
- ✅ 搜索配置：jsonContent
- ✅ SEO：sitemap

### 已安装插件
- hexo-abbrlink
- hexo-autonofollow
- hexo-directory-category
- hexo-generator-feed
- hexo-generator-json-content
- hexo-generator-sitemap
- hexo-renderer-kramed
- hexo-renderer-stylus

## 🚀 使用命令

```bash
cd /home/admin/.openclaw/workspace/claw-wiki

# 本地预览
hexo server

# 生成静态文件
hexo generate

# 创建新文章
hexo new "文章标题"

# 清理并重新生成
hexo clean && hexo generate
```

## 🌐 访问模式

### 单页模式（默认）
干净的文章页面，适合分享：
```
http://localhost:4000/wiki/f3763a72/
```

### 全站模式（SPA）
完整的 Wiki 体验，带侧边栏导航：
```
http://localhost:4000/?fullpage=1
```

## 📝 测试文章

已创建测试文章：
- **标题**: 欢迎使用 Quinoa 主题
- **分类**: 入门指南
- **标签**: Hexo, Quinoa
- **链接**: http://localhost:4000/wiki/f3763a72/

## ⚙️ 待配置项

### 主题配置 (`themes/Quinoa/_config.yml`)
需要修改以下内容：
- [ ] `customize.social_links.github` - 你的 GitHub 地址
- [ ] `history_control.user` - GitHub 用户名
- [ ] `history_control.repertory` - 仓库名
- [ ] `plugins.google_analytics` - GA 跟踪 ID（可选）
- [ ] `plugins.baidu_analytics` - 百度统计 ID（可选）

### 站点配置 (`_config.yml`)
需要修改：
- [ ] `url` - 你的域名
- [ ] `author` - 作者名
- [ ] `language` - 语言（zh-CN）
- [ ] `timezone` - 时区（Asia/Shanghai）

## 📦 部署到生产环境

### 方式 1: GitHub Pages
```bash
pnpm add hexo-deployer-git
# 编辑 _config.yml 配置 deploy 部分
hexo deploy
```

### 方式 2: 手动部署
```bash
hexo generate
# 将 public/ 目录内容上传到服务器
```

## 🔗 相关链接

- **主题仓库**: https://github.com/quanoc/hexo-theme-Quinoa
- **在线演示**: https://waisec.cn/
- **Hexo 文档**: https://hexo.io/docs/

---

**部署完成！** 🎉
