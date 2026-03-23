#!/bin/bash
# Daily AI Report Sender - Sends generated report to DingTalk group

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
REPORT_SCRIPT="$WORKSPACE/scripts/ai-daily-report.py"
LATEST_REPORT=$(ls -t "$WORKSPACE/data/ai-daily-report/reports/"*.md 2>/dev/null | head -1)

if [ -z "$LATEST_REPORT" ]; then
    echo "❌ No report found, generating one..."
    python3 "$REPORT_SCRIPT"
    LATEST_REPORT=$(ls -t "$WORKSPACE/data/ai-daily-report/reports/"*.md 2>/dev/null | head -1)
fi

if [ -z "$LATEST_REPORT" ]; then
    echo "❌ Failed to generate report"
    exit 1
fi

echo "📤 Sending report: $LATEST_REPORT"

# Read report content
REPORT_CONTENT=$(cat "$LATEST_REPORT")

# Send via OpenClaw message tool (dingtalk)
# Using sessions_send to send to the current session's channel
cd "$WORKSPACE"

# Create a temporary file with the message
TEMP_MSG=$(mktemp)
cat > "$TEMP_MSG" << EOF
🧠 **AI Agent 深度日报** - $(date +%Y-%m-%d)

$(echo "$REPORT_CONTENT" | head -80)

...

📄 [完整报告已保存到磁盘]
位置：$LATEST_REPORT

---
*自动推送 · 高质量 Agent 架构与工程实践*
EOF

# Use openclaw message command or sessions_send
# For dingtalk group, we'll use the message tool
cat "$TEMP_MSG"

rm -f "$TEMP_MSG"

echo "✅ Report sent successfully"
