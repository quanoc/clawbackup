# ClawBackup - OpenClaw 配置备份

## 备份时间
2026-03-13 22:30 GMT+8

## 备份内容

### 1. workspace/
完整的 OpenClaw 工作目录，包含：
- 记忆文件 (MEMORY.md, memory/*.md)
- 配置文件 (SOUL.md, USER.md, IDENTITY.md, AGENTS.md, TOOLS.md)
- 技能文件 (skills/)
- 项目文件

### 2. openclaw.json.sanitized.json
**脱敏后的配置文件**

⚠️ **敏感信息已移除**：
- API Keys (DashScope)
- Gateway Auth Token
- DingTalk ClientID/Secret
- 公网 IP 地址
- 本地路径信息

🔐 **原始配置文件位置**：`~/.openclaw/openclaw.json` (未备份，需手动保存)

## 恢复说明

### 恢复 Workspace
```bash
git clone git@github.com:quanoc/clawbackup.git
cp -r clawbackup/workspace/* ~/.openclaw/workspace/
```

### 恢复配置
⚠️ 需要手动填写敏感信息：
1. 复制 `openclaw.json.sanitized.json` 为 `openclaw.json`
2. 填写真实的 API Keys、Tokens 等
3. 运行 `openclaw doctor` 验证配置

## 安全提示
- 此仓库仅包含脱敏配置，可直接公开
- 敏感信息需通过安全渠道单独保存
- 建议配合密码管理器存储 API Keys

## 原始数据位置
- 配置：`~/.openclaw/openclaw.json`
- 凭证：`~/.openclaw/credentials/` (如有)
- 扩展：`~/.openclaw/extensions/`
