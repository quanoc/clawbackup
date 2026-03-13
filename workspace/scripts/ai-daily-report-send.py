#!/usr/bin/env python3
"""
AI Daily Report - DingTalk Delivery Wrapper
Generates report and sends to DingTalk group
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.home() / ".openclaw" / "workspace"
REPORT_SCRIPT = WORKSPACE / "scripts" / "ai-daily-report.py"
REPORTS_DIR = WORKSPACE / "data" / "ai-daily-report" / "reports"

def get_latest_report():
    """Get the most recent report file"""
    reports = sorted(REPORTS_DIR.glob("ai-daily-*.md"), reverse=True)
    return reports[0] if reports else None

def generate_report():
    """Run the report generator"""
    result = subprocess.run(
        [sys.executable, str(REPORT_SCRIPT)],
        cwd=WORKSPACE,
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def format_message(report_file):
    """Format report for DingTalk message"""
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract first ~1500 chars for preview
    lines = content.split('\n')
    preview_lines = []
    char_count = 0
    
    for line in lines:
        if char_count + len(line) > 1400:
            break
        preview_lines.append(line)
        char_count += len(line)
    
    preview = '\n'.join(preview_lines)
    
    message = f"""🧠 **AI Agent 深度日报** - {datetime.now().strftime('%Y-%m-%d')}

{preview}

...

📄 **完整报告已保存**
位置：`{report_file}`

查看历史：`ls ~/.openclaw/workspace/data/ai-daily-report/reports/`

---
*自动推送 · 高质量 Agent 架构与工程实践 · 已去重*
"""
    return message

if __name__ == '__main__':
    print("🚀 Generating and sending AI Daily Report...")
    
    # Generate report
    if not generate_report():
        print("❌ Failed to generate report")
        sys.exit(1)
    
    # Get latest report
    report_file = get_latest_report()
    if not report_file:
        print("❌ No report found")
        sys.exit(1)
    
    # Format message
    message = format_message(report_file)
    
    # Output message for OpenClaw to send
    print("\n" + "="*60)
    print("MESSAGE TO SEND:")
    print("="*60)
    print(message)
    print("="*60)
    
    # In cron mode, we'll use a special output format
    if len(sys.argv) > 1 and sys.argv[1] == '--cron':
        # Output JSON for cron job to process
        output = {
            'action': 'send_message',
            'channel': 'dingtalk',
            'message': message,
            'report_file': str(report_file)
        }
        print(json.dumps(output))
    
    print(f"\n✅ Report ready: {report_file}")
