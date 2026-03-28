---
name: wiki-publisher
description: 自动化发布文章到 Wiki 系统。当用户提到"发布到wiki"、"部署wiki"、"wiki发布"、"更新wiki"等关键词时触发。支持环境准备、创建文章、清理、生成、部署等完整流程。
version: 1.0.0
author: quanoc
metadata: {"openclaw":{"emoji":"📝","category":"publish"}}
---

# Wiki Publisher Skill

自动化发布文章到 Wiki 系统的 Skill。

## 触发条件

当用户提到以下关键词或意图时自动触发：
- "发布到wiki" / "发布到 wiki"
- "把文章发布到wiki" / "把文章发布到 wiki"
- "发布文章到wiki" / "发布文章到 wiki"
- "publish to wiki"
- "部署wiki" / "部署 wiki"
- "wiki发布" / "wiki 发布"
- "wiki部署" / "wiki 部署"
- "更新wiki" / "更新 wiki"
- "发布文章"（结合上下文判断为wiki发布时）
- "生成wiki" / "生成 wiki"
- "build wiki" / "deploy wiki"

## 功能

- 检查并clone clawbackup仓库
- 检查并clone主题（如果主题目录为空）
- 切换到wiki/project分支
- 检查并安装hexo和pnpm
- 安装项目依赖
- 参考指定文章结构创建markdown文档
- Hexo清理、生成和部署（带详细日志和错误处理）

## 流程步骤

1. 检查并clone仓库
2. 检查主题目录，为空则clone主题
3. 切换分支
4. 检查并安装工具（pnpm、hexo）
5. 安装项目依赖
6. 检查环境
7. 创建文章（如果提供内容）
8. Hexo清理
9. Hexo生成（带详细日志）
10. Hexo部署

## 用法

### 环境准备
```bash
node wiki-publisher.js setup
```

### 创建文章
```bash
node wiki-publisher.js create "文章标题" "文章内容"
```

### 仅清理
```bash
node wiki-publisher.js clean
```

### 仅生成
```bash
node wiki-publisher.js generate
```

### 仅部署
```bash
node wiki-publisher.js deploy
```

### 完整流程（带文章创建）
```bash
node wiki-publisher.js full "文章标题" [内容文件路径]
```

## 示例

```bash
# 完整发布流程（不带新文章）
node wiki-publisher.js full

# 完整发布流程（带新文章）
node wiki-publisher.js full "MLOps自动化与监控" ./content.md
```

## Agent 使用说明

当触发此 skill 时，应该：

1. 询问用户是否有新文章要发布，还是仅重新生成/部署现有内容
2. 如果有新文章，请用户提供：
   - 文章标题
   - 文章内容（可以是文件路径或直接文本）
   - 可选：标签、分类等元数据
3. 执行 `node wiki-publisher.js full [标题] [内容]`
4. 返回执行结果和日志

## 配置

配置文件位于技能目录的 wiki-publisher.js 中，可根据需要修改：
- `repoUrl`: 仓库地址
- `workDir`: 工作目录
- `branch`: 分支名称
- `themeRepo`: 主题仓库地址

## 依赖

- Node.js
- Git
- SSH密钥配置（用于GitHub部署）

## SSH 密钥配置

本 skill 使用项目目录下的 SSH 密钥进行部署，无需手动配置 `~/.ssh/`。

项目目录结构：
```
clawbackup/
├── deploy_key          # 私钥（由仓库维护者提供）
├── deploy_key.pub      # 公钥
├── ssh_config          # SSH 配置文件
└── ...
```

`ssh_config` 示例：
```
Host github.com
    HostName github.com
    User git
    IdentityFile /path/to/project/deploy_key
    IdentitiesOnly yes
    StrictHostKeyChecking no
```

部署时自动使用项目目录下的 `ssh_config` 配置，通过 `GIT_SSH_COMMAND` 环境变量注入。如果 `ssh_config` 不存在，则回退到默认 SSH 配置。

## 日志输出

- 生成文件数统计
- 警告数和错误数统计
- 关键文件检查（index.html、atom.xml等）
- 详细的错误信息
