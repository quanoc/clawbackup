#!/bin/bash
# AI Daily Report - Cron Job Script
# 每天早上 9:30 执行，生成报告并保存到 Wiki

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
REPORT_SCRIPT="$WORKSPACE/scripts/ai-daily-report.py"
LOG_FILE="$WORKSPACE/data/ai-daily-report/cron.log"
WIKI_INDEX="$WORKSPACE/data/ai-daily-report/README.md"

# 记录开始时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始生成 AI 每日深度报告..." >> "$LOG_FILE"

# 生成报告（带中文翻译）
cd "$WORKSPACE"
if python3 "$REPORT_SCRIPT" --translate >> "$LOG_FILE" 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 报告生成成功" >> "$LOG_FILE"
    
    # 获取最新报告文件名
    LATEST_REPORT=$(ls -t "$WORKSPACE/data/ai-daily-report/reports/"ai-daily-*.md 2>/dev/null | head -1)
    
    if [ -n "$LATEST_REPORT" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📄 报告文件：$LATEST_REPORT" >> "$LOG_FILE"
        
        # 更新 Wiki 索引（可选）
        # 可以在这里添加更新 Wiki 索引的逻辑
    fi
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 报告生成失败" >> "$LOG_FILE"
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
