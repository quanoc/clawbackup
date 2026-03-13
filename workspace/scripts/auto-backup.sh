#!/bin/bash
# OpenClaw 自动备份脚本
# 每天凌晨 3:00 执行，备份 workspace 和脱敏配置到 GitHub

set -e

BACKUP_DIR="/tmp/clawbackup"
WORKSPACE_SRC="/home/admin/.openclaw/workspace"
CONFIG_SRC="/home/admin/.openclaw/openclaw.json"
CONFIG_SANITIZED="$BACKUP_DIR/openclaw.json.sanitized.json"
REPO_DIR="/tmp/clawbackup"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "开始 OpenClaw 自动备份..."

# 1. 确保备份目录存在
mkdir -p "$BACKUP_DIR"

# 2. 如果是首次运行，初始化 git 仓库
if [ ! -d "$REPO_DIR/.git" ]; then
    log "首次运行，初始化 git 仓库..."
    cd "$BACKUP_DIR"
    git init
    git config user.email "backup@openclaw.local"
    git config user.name "OpenClaw Auto Backup"
    git remote add origin git@github.com:quanoc/clawbackup.git
fi

# 3. 同步 workspace（排除 .git）
log "同步 workspace..."
rm -rf "$BACKUP_DIR/workspace"
mkdir -p "$BACKUP_DIR/workspace"
cp -r "$WORKSPACE_SRC"/* "$BACKUP_DIR/workspace/"
rm -rf "$BACKUP_DIR/workspace/.git" 2>/dev/null || true

# 4. 生成脱敏配置文件
log "生成脱敏配置文件..."
cat > "$CONFIG_SANITIZED" << 'SANITIZE_EOF'
{
  "_meta_info": "这是脱敏后的配置文件，敏感信息已替换为占位符",
  "_sanitized_at": "AUTO_GENERATED",
  "_sensitive_fields_removed": [
    "models.providers.*.apiKey - 真实 API Key 已隐藏",
    "gateway.auth.token - 网关认证 Token 已隐藏",
    "channels.*.clientId - Client ID 已隐藏",
    "channels.*.clientSecret - Client Secret 已隐藏",
    "gateway.controlUi.allowedOrigins - 公网 IP 已隐藏",
    "plugins.installs.*.sourcePath/installPath - 本地路径已隐藏"
  ],
  "meta": {
    "lastTouchedVersion": "AUTO",
    "lastTouchedAt": "AUTO"
  },
  "browser": {
    "executablePath": "/usr/bin/google-chrome",
    "headless": true,
    "defaultProfile": "openclaw"
  },
  "models": {
    "providers": {
      "dashscope": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "[REDACTED]",
        "api": "openai-completions"
      },
      "dashscope-us": {
        "baseUrl": "https://dashscope-us.aliyuncs.com/compatible-mode/v1",
        "apiKey": "[REDACTED]",
        "api": "openai-completions"
      },
      "dashscope-coding": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "[REDACTED]",
        "api": "openai-completions"
      }
    }
  },
  "gateway": {
    "port": 18027,
    "mode": "local",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "[REDACTED]"
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
  },
  "plugins": {
    "enabled": true,
    "allow": ["dingtalk", "qqbot", "dashscope-cfg", "wecom"]
  }
}
SANITIZE_EOF

# 5. 确保 README.md 存在
if [ ! -f "$BACKUP_DIR/README.md" ]; then
    log "创建 README.md..."
    cat > "$BACKUP_DIR/README.md" << 'README_EOF'
# ClawBackup - OpenClaw 配置备份

## 备份内容

### 1. workspace/
完整的 OpenClaw 工作目录，包含记忆文件、配置文件、技能、项目等。

### 2. openclaw.json.sanitized.json
**脱敏后的配置文件** - 敏感信息已移除（API Keys, Tokens, IP 地址等）

## 自动备份
每天凌晨 3:00 自动执行

## 恢复说明
```bash
git clone git@github.com:quanoc/clawbackup.git
cp -r clawbackup/workspace/* ~/.openclaw/workspace/
```

⚠️ 敏感信息需手动填写回 `~/.openclaw/openclaw.json`
README_EOF
fi

# 6. Git 提交和推送
cd "$REPO_DIR"

# 检查是否有变化
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
