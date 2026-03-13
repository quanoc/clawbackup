#!/usr/bin/env python3
"""
AI Daily Report - DingTalk Auto-Sender
Designed to be called by OpenClaw cron tool
Generates report and outputs message for delivery
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
        cwd=str(WORKSPACE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=180
    )
    return result.returncode == 0

def format_message(report_file):
    """Format report for DingTalk message"""
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract preview (first ~1200 chars)
    lines = content.split('\n')
    preview_lines = []
    char_count = 0
    
    for line in lines:
        if char_count + len(line) > 1200:
            break
        preview_lines.append(line)
        char_count += len(line)
    
    preview = '\n'.join(preview_lines)
    
    # Get stats
    report_date = report_file.stem.replace('ai-daily-', '')
    
    message = f"""🧠 **AI Agent 深度日报** - {report_date}

{preview}

...

📄 **完整报告已保存到磁盘**
位置：`{report_file}`

**快速查看**:
```bash
cat {report_file}
```

**历史报告**: `~/.openclaw/workspace/data/ai-daily-report/reports/`

---
*自动推送 · 高质量 Agent 架构与工程实践 · 已去重*
"""
    return message

if __name__ == '__main__':
    print("🚀 AI Daily Report - Auto Sender", file=sys.stderr)
    print(f"Time: {datetime.now().isoformat()}", file=sys.stderr)
    
    try:
        # Generate report
        print("📝 Generating report...", file=sys.stderr)
        if not generate_report():
            print("❌ Failed to generate report", file=sys.stderr)
            sys.exit(1)
        
        # Get latest report
        report_file = get_latest_report()
        if not report_file:
            print("❌ No report found", file=sys.stderr)
            sys.exit(1)
        
        print(f"✅ Report generated: {report_file}", file=sys.stderr)
        
        # Format message
        message = format_message(report_file)
        
        # Output the message for cron payload
        print("\n" + "="*60)
        print(message)
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
