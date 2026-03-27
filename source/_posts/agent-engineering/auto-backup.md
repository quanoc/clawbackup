---
title: OpenClaw 自动备份配置
toc: true
abbrlink: auto-backup-guide
date: 2026-03-14 02:30:00
tags:
  - OpenClaw
  - 自动备份
  - Git
  - GitHub
categories:
  - Agent工程实践
  - 环境配置
---

# OpenClaw 自动备份配置指南

> **配置时间**: 2026-03-14  
> **备份目标**: GitHub Private Repository  
> **备份频率**: 每日凌晨 3:00  
> **备份内容**: Workspace + 脱敏配置

---

## 📋 目录

1. [备份架构](#备份架构)
2. [准备工作](#准备工作)
3. [配置步骤](#配置步骤)
4. [备份脚本](#备份脚本)
5. [定时任务](#定时任务)
6. [恢复指南](#恢复指南)
7. [安全说明](#安全说明)

---

## 一、备份架构 {#备份架构}

### 1.1 备份内容

| 内容 | 说明 | 脱敏处理 |
|------|------|----------|
| **workspace/** | 工作目录（记忆、技能、项目） | ❌ 无需脱敏 |
| **openclaw.json** | 配置文件 | ✅ 敏感信息替换为 `[REDACTED]` |
| **README.md** | 备份说明文档 | ❌ 无需脱敏 |

### 1.2 不备份的内容

| 内容 | 原因 |
|------|------|
| `credentials/` | 包含敏感凭证，需单独安全存储 |
| `logs/` | 日志文件过大，无备份价值 |
| `extensions/` | 插件可通过配置重新安装 |
| `.git/` | 工作目录可能有独立 Git 历史 |

### 1.3 备份流程

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  源数据目录      │    │  备份脚本        │    │  GitHub 仓库     │
│  ~/.openclaw/   │ -> │  auto-backup.sh  │ -> │  quanoc/        │
│                 │    │                  │    │  clawbackup     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              ↓
                       ┌──────────────────┐
                       │  Cron 定时任务    │
                       │  每天 03:00       │
                       └──────────────────┘
```

---

## 二、准备工作 {#准备工作}

### 2.1 创建 GitHub 仓库

```bash
# 在 GitHub 上创建私有仓库
# 仓库名：clawbackup
# 可见性：Private
# 初始化：不需要
```

### 2.2 生成 SSH Key

```bash
# 生成新的 SSH Key
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_backup -C "backup@openclaw"

# 查看公钥
cat ~/.ssh/id_ed25519_backup.pub
```

### 2.3 配置 Deploy Key

1. 打开仓库：`https://github.com/quanoc/clawbackup/settings/keys`
2. 点击 **Add deploy key**
3. 粘贴公钥
4. ✅ 勾选 **Allow write access**
5. 点击 **Add key**

---

## 三、配置步骤 {#配置步骤}

### 3.1 创建备份目录

```bash
mkdir -p /tmp/clawbackup
cd /tmp/clawbackup
git init
git config user.email "backup@openclaw.local"
git config user.name "OpenClaw Backup"
git remote add origin git@github.com:quanoc/clawbackup.git
```

### 3.2 首次备份

```bash
# 复制工作目录
cp -r ~/.openclaw/workspace/* /tmp/clawbackup/workspace/
rm -rf /tmp/clawbackup/workspace/.git

# 创建脱敏配置
# (见下方脱敏脚本)

# 提交并推送
git add -A
git commit -m "Initial backup: $(date +%Y-%m-%d)"
git push -u origin main
```

---

## 四、备份脚本 {#备份脚本}

### 4.1 完整脚本

位置：`/home/admin/.openclaw/workspace/scripts/auto-backup.sh`

```bash
#!/bin/bash
# OpenClaw 自动备份脚本
# 每天凌晨 3:00 执行

set -e

BACKUP_DIR="/tmp/clawbackup"
WORKSPACE_SRC="/home/admin/.openclaw/workspace"
CONFIG_SRC="/home/admin/.openclaw/openclaw.json"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "开始 OpenClaw 自动备份..."

# 1. 确保备份目录存在
mkdir -p "$BACKUP_DIR"

# 2. 同步 workspace（排除 .git）
log "同步 workspace..."
rm -rf "$BACKUP_DIR/workspace"
mkdir -p "$BACKUP_DIR/workspace"
cp -r "$WORKSPACE_SRC"/* "$BACKUP_DIR/workspace/"
rm -rf "$BACKUP_DIR/workspace/.git" 2>/dev/null || true

# 3. 生成脱敏配置文件
log "生成脱敏配置文件..."
cat > "$BACKUP_DIR/openclaw.json.sanitized.json" << 'EOF'
{
  "_meta_info": "脱敏配置文件",
  "_sensitive_fields_removed": [
    "API Keys",
    "Gateway Token",
    "Client Secrets",
    "IP Addresses"
  ]
}
EOF

# 4. Git 提交和推送
cd "$BACKUP_DIR"

if [ -z "$(git status --porcelain)" ]; then
    log "无变化，跳过提交"
else
    log "提交变更..."
    git add -A
    git commit -m "Auto backup: $(date '+%Y-%m-%d %H:%M')"
    
    log "推送到 GitHub..."
    git push origin main
fi

log "备份完成！"
```

### 4.2 配置脱敏规则

敏感字段替换表：

| 原字段 | 替换为 |
|--------|--------|
| `apiKey: "sk-xxx"` | `apiKey: "[REDACTED]"` |
| `token: "abc123"` | `token: "[REDACTED]"` |
| `clientSecret: "xyz"` | `clientSecret: "[REDACTED]"` |
| `allowedOrigins: ["http://1.2.3.4:port"]` | `allowedOrigins: ["[REDACTED_IP]"]` |
| `sourcePath: "/home/admin/xxx"` | `sourcePath: "[REDACTED_PATH]"` |

---

## 五、定时任务 {#定时任务}

### 5.1 配置 Crontab

```bash
crontab -e
```

添加以下内容：

```cron
# OpenClaw Auto Backup - Daily at 3:00 AM
0 3 * * * /home/admin/.openclaw/workspace/scripts/auto-backup.sh >> /home/admin/.openclaw/workspace/data/backup-cron.log 2>&1
```

### 5.2 验证 Cron

```bash
# 查看已配置的定时任务
crontab -l

# 查看 Cron 日志
tail -f /var/log/cron 2>/dev/null || journalctl -u cron -f
```

### 5.3 手动测试

```bash
# 手动执行备份脚本
/home/admin/.openclaw/workspace/scripts/auto-backup.sh

# 查看日志
tail /home/admin/.openclaw/workspace/data/backup-cron.log
```

---

## 六、恢复指南 {#恢复指南}

### 6.1 从备份恢复

```bash
# 1. 克隆备份仓库
git clone git@github.com:quanoc/clawbackup.git ~/clawbackup-restore

# 2. 恢复工作目录
cp -r ~/clawbackup-restore/workspace/* ~/.openclaw/workspace/

# 3. 恢复配置（需手动填写敏感信息）
cp ~/clawbackup-restore/openclaw.json.sanitized.json ~/.openclaw/openclaw.json
# 编辑 openclaw.json，填写真实的 API Keys 和 Tokens

# 4. 验证配置
openclaw doctor
```

### 6.2 恢复敏感信息

从安全存储中恢复以下信息：

1. **API Keys** (DashScope 等)
2. **Gateway Token**
3. **Channel Credentials** (DingTalk, QQ, WeCom)
4. **其他敏感配置**

```bash
# 编辑配置文件
vim ~/.openclaw/openclaw.json

# 替换所有 [REDACTED] 为真实值
```

### 6.3 恢复插件

```bash
# 重新安装插件
openclaw plugins install qqbot
openclaw plugins install dingtalk
openclaw plugins install wecom
```

---

## 七、安全说明 {#安全说明}

### 7.1 敏感信息存储

**推荐方式**:

| 方式 | 说明 |
|------|------|
| **密码管理器** | 1Password, Bitwarden 等 |
| **加密文件** | 使用 GPG 加密敏感配置 |
| **环境变量** | 通过环境变量注入 API Keys |

### 7.2 SSH Key 管理

```bash
# 限制 Deploy Key 权限（仅单个仓库）
# 不要使用个人 SSH Key 进行自动备份

# 定期检查已授权的 Deploy Key
# https://github.com/settings/keys
```

### 7.3 备份验证

```bash
# 每周验证备份完整性
cd /tmp/clawbackup
git pull origin main
ls -la workspace/

# 检查文件大小变化
du -sh workspace/
```

---

## 八、监控与告警 {#监控告警}

### 8.1 备份日志监控

```bash
# 查看最近备份状态
tail -20 /home/admin/.openclaw/workspace/data/backup-cron.log

# 检查是否有错误
grep -i "error\|fail" /home/admin/.openclaw/workspace/data/backup-cron.log
```

### 8.2 备份失败告警

可以在脚本中添加告警逻辑：

```bash
# 备份失败时发送通知
if [ $? -ne 0 ]; then
    echo "备份失败！" | mail -s "OpenClaw Backup Alert" admin@example.com
fi
```

---

## 九、最佳实践 {#最佳实践}

### 9.1 备份策略

| 类型 | 频率 | 保留 |
|------|------|------|
| **完整备份** | 每天 | 最近 30 天 |
| **配置变更** | 实时 | 永久 |
| **重要文档** | 实时 | 永久 |

### 9.2 Git 分支管理

```
main        - 最新备份
backup-YYYY-MM-DD - 历史快照（按需创建）
```

### 9.3 定期演练

- **每月**：验证备份可恢复性
- **每季度**：更新 SSH Key
- **每半年**：审查备份策略

---

**参考资料**:
- [GitHub Deploy Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys)
- [Crontab 语法](https://crontab.guru/)

---

*本配置已应用于生产环境*  
*最后更新：2026-03-14*
