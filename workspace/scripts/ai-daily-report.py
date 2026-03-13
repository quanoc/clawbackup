#!/usr/bin/env python3
"""
Daily AI Agent & LLM Deep Report Generator
Generates high-quality agent architecture and research insights
With optional Chinese translation
"""

import json
import os
import subprocess
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

# Try to import translation library
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("⚠️ Translation not available. Install: pip3 install --user deep-translator", file=sys.stderr)

# Configuration
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "ai-daily-report"
HISTORY_FILE = DATA_DIR / "history.json"
SEEN_IDS_FILE = DATA_DIR / "seen_ids.json"
REPORTS_DIR = DATA_DIR / "reports"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Search queries for high-quality content
SEARCH_QUERIES = [
    # Core architecture & patterns
    "AI agent architecture patterns design principles production",
    "LLM agent workflow orchestrator evaluator optimizer",
    "building effective AI agents Anthropic research",
    
    # Engineering best practices
    "AI agent production deployment lessons learned",
    "LangChain LlamaIndex agent engineering best practices",
    "AI agent evaluation monitoring observability",
    
    # Research & insights
    "AI agent research paper arxiv cs.AI cs.LG",
    "multi-agent systems coordination collaboration",
    "AI agent memory context management RAG",
    
    # Industry insights from key players
    "Andrej Karpathy AI agent commentary",
    "Harrison Chase LangChain agent insights",
    "Anthropic Claude agent SDK engineering",
    
    # Sebastian Raschka's Ahead of AI newsletter (high-quality AI/ML content)
    "Sebastian Raschka Ahead of AI newsletter LLM transformer",
    "raschka substack AI machine learning deep learning",
]

def load_json_file(filepath, default=None):
    """Load JSON file or return default"""
    if default is None:
        default = {}
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return default

def save_json_file(filepath, data):
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def search_searxng(query, limit=8):
    """Execute search using searxng skill"""
    try:
        cmd = [
            "uv", "run", "scripts/searxng.py",
            "search", query,
            "-n", str(limit),
            "--format", "json"
        ]
        result = subprocess.run(
            cmd,
            cwd=Path.home() / ".openclaw" / "workspace" / "skills" / "searxng",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # SearXNG returns {"results": [...], ...}
            return data.get('results', [])
    except Exception as e:
        print(f"Search error for '{query}': {e}")
    return []

def generate_item_id(title, url):
    """Generate unique ID for deduplication"""
    content = f"{title}:{url}"
    return hashlib.md5(content.encode()).hexdigest()[:16]

def fetch_web_content(url, max_chars=6000):
    """Fetch and extract content from URL"""
    try:
        cmd = [
            "uv", "run", "scripts/searxng.py",
            "fetch", url,
            "--max-chars", str(max_chars)
        ]
        result = subprocess.run(
            cmd,
            cwd=Path.home() / ".openclaw" / "workspace" / "skills" / "searxng",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=45
        )
        if result.returncode == 0:
            return result.stdout[:max_chars]
    except Exception as e:
        print(f"Fetch error for '{url}': {e}")
    return None

def score_result(result, seen_ids):
    """Score search result for relevance and quality"""
    score = 5  # Base score
    
    title = result.get('title', '').lower()
    url = result.get('url', '').lower()
    # SearXNG uses 'content' instead of 'snippet'
    snippet = result.get('content', result.get('snippet', '')).lower()
    
    # High-quality source boost
    high_quality_domains = [
        'anthropic.com', 'openai.com', 'google.com', 'deepmind.com',
        'langchain.com', 'llamaindex.ai', 'arxiv.org',
        'mckinsey.com', 'technologyreview.com', 'nature.com',
        'blog.langchain.dev', 'docs.langchain.com',
        # Sebastian Raschka's Ahead of AI newsletter
        'magazine.sebastianraschka.com', 'substack.com',
    ]
    for domain in high_quality_domains:
        if domain in url:
            score += 2
            break
    
    # Extra boost for Sebastian Raschka's content
    if 'raschka' in title or 'raschka' in url or 'ahead of ai' in title:
        score += 2
    
    # Key topics boost
    key_topics = ['architecture', 'pattern', 'production', 'engineering', 
                  'best practice', 'lesson', 'design', 'framework']
    for topic in key_topics:
        if topic in title or topic in snippet:
            score += 1
            break
    
    # Recent content boost (check for year)
    if '2025' in title or '2026' in title or '2025' in snippet or '2026' in snippet:
        score += 1
    
    # Deduplication penalty
    item_id = generate_item_id(title, url)
    if item_id in seen_ids:
        score = 0  # Already seen
    
    return score

def categorize_result(result):
    """Categorize search result"""
    title = result.get('title', '').lower()
    # SearXNG uses 'content' instead of 'snippet'
    snippet = result.get('content', result.get('snippet', '')).lower()
    url = result.get('url', '').lower()
    
    categories = {
        '🏗️ 架构设计': ['architecture', 'pattern', 'design', 'framework', 'system'],
        '📊 生产实践': ['production', 'deployment', 'engineering', 'best practice', 'lesson'],
        '🔬 研究论文': ['arxiv', 'research', 'paper', 'study', 'academic'],
        '💡 行业洞察': ['insight', 'trend', 'analysis', 'report', 'mckinsey'],
        '🛠️ 工具框架': ['langchain', 'llamaindex', 'framework', 'sdk', 'tool'],
        '📰 公司动态': ['anthropic', 'openai', 'google', 'release', 'launch', 'funding'],
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title or keyword in snippet or keyword in url:
                return category
    
    return '📚 其他资源'

def generate_report(translate=False):
    """Generate daily AI agent report"""
    print(f"🚀 Generating AI Daily Report - {datetime.now().isoformat()}")
    
    # Load history
    history = load_json_file(HISTORY_FILE, {'reports': [], 'total_generated': 0})
    seen_ids = load_json_file(SEEN_IDS_FILE, {})
    
    all_results = []
    
    # Execute searches
    print("🔍 Searching for content...")
    for query in SEARCH_QUERIES:
        results = search_searxng(query, limit=5)
        if isinstance(results, list):
            all_results.extend(results)
    
    print(f"📥 Found {len(all_results)} raw results")
    
    # Score and filter
    scored_results = []
    for result in all_results:
        if not isinstance(result, dict):
            continue
        score = score_result(result, seen_ids)
        if score > 0:
            result['_score'] = score
            result['_category'] = categorize_result(result)
            scored_results.append(result)
    
    # Sort by score
    scored_results.sort(key=lambda x: x['_score'], reverse=True)
    
    # Deduplicate by URL
    seen_urls = set()
    unique_results = []
    for result in scored_results:
        url = result.get('url', '')
        if url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)
    
    # Take top 10-15 results
    top_results = unique_results[:12]
    
    if not top_results:
        print("⚠️ No new high-quality content found today")
        return None
    
    # Generate report
    report_date = datetime.now().strftime('%Y-%m-%d')
    report_id = f"ai-daily-{report_date}"
    
    report_content = generate_report_content(report_date, top_results, translate=translate)
    
    # Translate if requested
    if translate and TRANSLATION_AVAILABLE:
        print("🌏 Translating to Chinese...")
        report_content = translate_content(report_content)
    
    # Save report to file
    report_file = REPORTS_DIR / f"{report_id}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    # Update seen IDs
    for result in top_results:
        item_id = generate_item_id(result.get('title', ''), result.get('url', ''))
        seen_ids[item_id] = {
            'title': result.get('title', ''),
            'url': result.get('url', ''),
            'first_seen': report_date
        }
    
    # Update history
    history['reports'].append({
        'id': report_id,
        'date': report_date,
        'file': str(report_file),
        'item_count': len(top_results),
        'generated_at': datetime.now().isoformat()
    })
    history['total_generated'] += 1
    
    # Save state
    save_json_file(HISTORY_FILE, history)
    save_json_file(SEEN_IDS_FILE, seen_ids)
    
    print(f"✅ Report saved to {report_file}")
    print(f"📊 Total items: {len(top_results)}")
    
    return {
        'report_id': report_id,
        'date': report_date,
        'content': report_content,
        'file': str(report_file),
        'item_count': len(top_results)
    }

def translate_content(content):
    """Translate content to Chinese using Google Translate"""
    if not TRANSLATION_AVAILABLE:
        return content
    
    try:
        translator = GoogleTranslator(source='en', target='chinese (simplified)')
        
        # Split into chunks to avoid API limits
        chunks = []
        current_chunk = []
        current_length = 0
        
        lines = content.split('\n')
        for line in lines:
            if current_length + len(line) > 4000:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_length = len(line)
            else:
                current_chunk.append(line)
                current_length += len(line)
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            if chunk.strip() and any(ord(c) > 127 for c in chunk) is False:  # Only translate if mostly ASCII
                try:
                    translated = translator.translate(chunk)
                    translated_chunks.append(translated)
                except Exception as e:
                    print(f"⚠️ Translation error: {e}", file=sys.stderr)
                    translated_chunks.append(chunk)
            else:
                translated_chunks.append(chunk)
        
        return '\n'.join(translated_chunks)
    except Exception as e:
        print(f"⚠️ Translation failed: {e}", file=sys.stderr)
        return content

def generate_report_content(date, results, translate=False):
    """Format report as markdown"""
    content = f"""# 🧠 AI Agent & LLM 深度日报

**日期**: {date}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**本期条目**: {len(results)}

---

"""
    
    # Group by category
    categories = {}
    for result in results:
        cat = result.get('_category', '📚 其他资源')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(result)
    
    # Output by category
    for category, items in categories.items():
        content += f"## {category} ({len(items)})\n\n"
        
        for i, item in enumerate(items, 1):
            title = item.get('title', '无标题')
            url = item.get('url', '#')
            # SearXNG uses 'content' instead of 'snippet'
            snippet = item.get('content', item.get('snippet', ''))
            score = item.get('_score', 0)
            engines = item.get('engines', [])
            engine = engines[0] if isinstance(engines, list) and engines else 'unknown'
            
            # Quality indicator
            quality = '🔥' if score >= 8 else '✨' if score >= 6 else '📌'
            
            content += f"{quality} **{title}**\n"
            if snippet:
                # Truncate snippet
                snippet = snippet[:200] + '...' if len(snippet) > 200 else snippet
                content += f"> {snippet}\n"
            content += f"\n**来源**: {url.split('/')[2]} · **质量评分**: {score}/10 · **引擎**: {engine} · [查看]({url})\n\n"
        
        content += "---\n\n"
    
    # Footer
    content += f"""
## 📊 统计

- **搜索查询数**: {len(SEARCH_QUERIES)}
- **本期精选**: {len(results)} 条
- **累计保存**: {len(load_json_file(HISTORY_FILE, {}).get('reports', []))} 期

---

*本报告由 AI Daily Report Generator 自动生成*
*聚焦高质量 Agent 架构、工程实践与研究洞察*
"""
    
    return content

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Daily Report Generator')
    parser.add_argument('--translate', '-t', action='store_true', 
                       help='Translate report to Chinese (Simplified)')
    args = parser.parse_args()
    
    report = generate_report(translate=args.translate)
    if report:
        print("\n" + "="*60)
        print("REPORT PREVIEW:")
        print("="*60)
        print(report['content'][:2000])
        print("...")
        print(f"\n[完整报告保存在：{report['file']}]")
