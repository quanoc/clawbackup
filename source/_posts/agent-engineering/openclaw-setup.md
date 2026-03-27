---
title: OpenClaw 环境配置指南
toc: true
abbrlink: openclaw-setup
date: 2026-03-14 02:00:00
tags:
  - OpenClaw
  - 环境配置
  - AI Agent
  - 部署指南
categories:
  - Agent工程实践
  - 环境配置
---

# OpenClaw 环境配置指南

> **配置时间**: 2026-03-14  
> **OpenClaw 版本**: 2026.2.26  
> **Node.js**: v24.14.0  
> **操作系统**: Linux 5.10.134-19.2.al8.x86_64

---

## 📋 目录

1. [系统要求](#系统要求)
2. [安装步骤](#安装步骤)
3. [配置说明](#配置说明)
4. [插件配置](#插件配置)
5. [模型配置](#模型配置)
6. [常用命令](#常用命令)
7. [故障排查](#故障排查)

---

## 一、系统要求 {#系统要求}

### 1.1 硬件要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| **CPU** | 2 核 | 4 核 + |
| **内存** | 4GB | 8GB+ |
| **磁盘** | 10GB | 20GB+ SSD |
| **网络** | 宽带连接 | 稳定宽带 |

### 1.2 软件要求

| 软件 | 版本 | 用途 |
|------|------|------|
| **Node.js** | v18+ | 运行时环境 |
| **pnpm** | v10+ | 包管理器 |
| **Google Chrome** | Latest | 浏览器自动化 |
| **Git** | Latest | 版本控制 |

---

## 二、安装步骤 {#安装步骤}

### 2.1 安装 Node.js 和 pnpm

```bash
# 使用 nvm 安装 Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 24
nvm use 24

# 安装 pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

### 2.2 安装 OpenClaw

```bash
# 方法 1: 使用官方安装脚本（推荐）
curl -fsSL https://openclaw.ai/install.sh | bash

# 方法 2: 使用 npm/pnpm
pnpm add -g openclaw@latest
```

### 2.3 启动 Gateway

```bash
# 启动服务
openclaw gateway start

# 查看状态
openclaw gateway status

# 查看日志
openclaw logs --follow
```

---

## 三、配置说明 {#配置说明}

### 3.1 配置文件位置

```
~/.openclaw/
├── openclaw.json          # 主配置文件
├── credentials/           # 凭证目录（敏感）
├── workspace/             # 工作目录
└── extensions/            # 插件目录
```

### 3.2 基础配置

```json
{
  "gateway": {
    "port": 18027,
    "mode": "local",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "[你的 Token]"
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "dashscope-coding/qwen3.5-plus"
      },
      "workspace": "/home/admin/.openclaw/workspace"
    }
  },
  "cron": {
    "enabled": true
  }
}
```

### 3.3 敏感信息脱敏

⚠️ **以下内容需要脱敏处理**:

| 字段 | 说明 | 脱敏方式 |
|------|------|----------|
| `models.providers.*.apiKey` | API 密钥 | `[REDACTED]` |
| `gateway.auth.token` | 网关 Token | `[REDACTED]` |
| `channels.*.clientSecret` | 客户端密钥 | `[REDACTED]` |
| `channels.*.clientId` | 客户端 ID | `[REDACTED]` |

---

## 四、插件配置 {#插件配置}

### 4.1 已安装插件

| 插件 | 版本 | 用途 |
|------|------|------|
| **qqbot** | 1.5.0 | QQ 机器人 |
| **dingtalk** | 3.1.4 | 钉钉集成 |
| **wecom** | 0.1.28 | 企业微信 |
| **dashscope-cfg** | 2026.2.25 | 通义千问配置 |

### 4.2 插件配置示例

```json
{
  "plugins": {
    "enabled": true,
    "allow": ["dingtalk", "qqbot", "dashscope-cfg", "wecom"],
    "entries": {
      "qqbot": { "enabled": true },
      "dingtalk": { "enabled": true }
    }
  },
  "channels": {
    "dingtalk": {
      "enabled": true,
      "clientId": "[REDACTED]",
      "clientSecret": "[REDACTED]",
      "dmPolicy": "open",
      "groupPolicy": "open"
    }
  }
}
```

---

## 五、模型配置 {#模型配置}

### 5.1 通义千问配置

```json
{
  "models": {
    "providers": {
      "dashscope": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "[REDACTED]",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "Qwen3.5-Plus",
            "contextWindow": 1000000,
            "maxTokens": 65536
          }
        ]
      },
      "dashscope-coding": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "[REDACTED]",
        "api": "openai-completions"
      }
    }
  }
}
```

### 5.2 模型别名

```json
{
  "agents": {
    "defaults": {
      "models": {
        "dashscope/qwen3.5-plus": { "alias": "qwen3.5-plus" },
        "dashscope-us/qwen3-max-2025-09-23": { "alias": "qwen3-max-2025-09-23" },
        "dashscope-coding/qwen3.5-plus": { "alias": "qwen3.5-plus" }
      }
    }
  }
}
```

---

## 六、常用命令 {#常用命令}

### 6.1 服务管理

```bash
# 启动/停止/重启
openclaw gateway start
openclaw gateway stop
openclaw gateway restart

# 查看状态
openclaw gateway status
openclaw status
```

### 6.2 日志查看

```bash
# 实时日志
openclaw logs --follow

# 最近 100 行
openclaw logs --limit 100
```

### 6.3 配置管理

```bash
# 运行健康检查
openclaw doctor

# 更新配置
openclaw config set gateway.port 18027
```

### 6.4 更新维护

```bash
# 更新 OpenClaw
openclaw update

# 查看更新状态
openclaw update status
```

---

## 七、故障排查 {#故障排查}

### 7.1 常见问题

#### Gateway 无法启动

```bash
# 检查端口占用
netstat -tlnp | grep 18027

# 查看详细错误
openclaw logs --follow
```

#### 插件加载失败

```bash
# 重新安装插件
cd ~/.openclaw/extensions/qqbot
pnpm install

# 检查插件状态
openclaw plugins list
```

#### API 调用失败

```bash
# 检查 API Key 配置
cat ~/.openclaw/openclaw.json | grep apiKey

# 测试 API 连接
curl -H "Authorization: Bearer [REDACTED]" \
  https://dashscope.aliyuncs.com/compatible-mode/v1/models
```

---

### 7.2 调试模式

```bash
# 启用详细日志
export DEBUG=openclaw:*
openclaw gateway start

# 浏览器调试
openclaw browser debug
```

---

### 7.3 备份与恢复

```bash
# 备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 备份工作目录
tar -czf workspace-backup.tar.gz ~/.openclaw/workspace/

# 恢复配置
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
```

---

## 八、安全建议 {#安全建议}

### 8.1 敏感信息管理

1. **不要提交 API Keys 到 Git**
2. **使用环境变量存储敏感信息**
3. **定期轮换 Token 和密钥**
4. **限制 Gateway 访问权限**

### 8.2 网络安全

```json
{
  "gateway": {
    "bind": "lan",  // 仅监听内网
    "auth": {
      "mode": "token"  // 启用 Token 认证
    }
  }
}
```

### 8.3 权限控制

```json
{
  "gateway": {
    "nodes": {
      "denyCommands": [
        "camera.snap",
        "screen.record",
        "calendar.add"
      ]
    }
  }
}
```

---

## 九、性能优化 {#性能优化}

### 9.1 内存优化

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard"  // 自动压缩长对话
      }
    }
  }
}
```

### 9.2 缓存配置

```bash
# 启用浏览器缓存
openclaw config set browser.cache.enabled true
```

---

**参考资料**:
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [GitHub 仓库](https://github.com/openclaw/openclaw)
- [Discord 社区](https://discord.gg/clawd)

---

*本配置基于生产环境，敏感信息已脱敏*  
*最后更新：2026-03-14*
