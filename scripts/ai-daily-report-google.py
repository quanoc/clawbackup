#!/usr/bin/env python3
"""
AI Daily Report - Google Search Edition
Uses Google via SearXNG with direct HTTP calls
"""

import json
import httpx
import hashlib
from datetime import datetime
from pathlib import Path

# Configuration
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "ai-daily-report"
REPORTS_DIR = DATA_DIR / "reports-google"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

SEARXNG_URL = "http://localhost:8080"

# Search queries
SEARCH_QUERIES = [
    "AI agent architecture patterns design principles production",
    "LLM agent workflow orchestrator evaluator optimizer",
    "building effective AI agents Anthropic research",
    "AI agent production deployment lessons learned",
    "LangChain LlamaIndex agent engineering best practices",
    "AI agent evaluation monitoring observability",
    "AI agent research paper arxiv cs.AI cs.LG",
    "multi-agent systems coordination collaboration",
    "AI agent memory context management RAG",
    "Anthropic Claude agent SDK engineering",
]

def search_google(query, limit=10):
    """Search Google via SearXNG"""
    params = {
        "q": query,
        "format": "json",
        "engines": "google",
        "language": "en",
    }
    
    try:
        response = httpx.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=30,
            verify=False
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        print(f"  ✓ Google: {len(results)} results")
        return results[:limit]
    except Exception as e:
        print(f"  ⚠ Google search error: {e}")
        # Fallback to default search (all engines)
        return search_default(query, limit)

def search_default(query, limit=10):
    """Fallback: search all engines"""
    params = {
        "q": query,
        "format": "json",
    }
    
    try:
        response = httpx.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=30,
            verify=False
        )
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])[:limit]
    except Exception as e:
        print(f"  ⚠ Default search error: {e}")
        return []

def generate_item_id(title, url):
    """Generate unique ID for deduplication"""
    content = f"{title}:{url}"
    return hashlib.md5(content.encode()).hexdigest()[:16]

def score_result(result, seen_ids):
    """Score search result for relevance and quality"""
    score = 5  # Base score
    
    title = result.get('title', '').lower()
    url = result.get('url', '').lower()
    snippet = result.get('content', result.get('snippet', '')).lower()
    
    # High-quality source boost
    high_quality_domains = [
        'anthropic.com', 'openai.com', 'google.com', 'deepmind.com',
        'langchain.com', 'llamaindex.ai', 'arxiv.org',
        'mckinsey.com', 'technologyreview.com', 'nature.com',
        'blog.langchain.dev', 'docs.langchain.com', 'cloud.google.com'
    ]
    for domain in high_quality_domains:
        if domain in url:
            score += 2
            break
    
    # Key topics boost
    key_topics = ['architecture', 'pattern', 'production', 'engineering', 
                  'best practice', 'lesson', 'design', 'framework']
    for topic in key_topics:
        if topic in title or topic in snippet:
            score += 1
            break
    
    # Recent content boost
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

def generate_report():
    """Generate daily AI agent report using Google search"""
    print(f"🚀 Generating AI Daily Report (Google Edition) - {datetime.now().isoformat()}")
    
    # Load seen IDs for deduplication
    seen_ids_file = DATA_DIR / "seen_ids.json"
    seen_ids = {}
    if seen_ids_file.exists():
        with open(seen_ids_file, 'r', encoding='utf-8') as f:
            seen_ids = json.load(f)
    
    all_results = []
    
    # Execute Google searches
    print("🔍 Searching Google...")
    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"  [{i}/{len(SEARCH_QUERIES)}] {query[:50]}...")
        results = search_google(query, limit=5)
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
    
    # Take top 12 results
    top_results = unique_results[:12]
    
    if not top_results:
        print("⚠️ No new high-quality content found today")
        return None
    
    # Generate report
    report_date = datetime.now().strftime('%Y-%m-%d')
    report_id = f"ai-daily-google-{report_date}"
    
    report_content = generate_report_content(report_date, top_results, source="Google")
    
    # Save report to file
    report_file = REPORTS_DIR / f"{report_id}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Report saved to {report_file}")
    print(f"📊 Total items: {len(top_results)}")
    
    return {
        'report_id': report_id,
        'date': report_date,
        'content': report_content,
        'file': str(report_file),
        'item_count': len(top_results)
    }

def generate_report_content(date, results, source="Google"):
    """Format report as markdown"""
    content = f"""# 🧠 AI Agent & LLM 深度日报（{source}搜索版）

**日期**: {date}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**搜索源**: {source}
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
            snippet = item.get('content', item.get('snippet', ''))
            score = item.get('_score', 0)
            engines = item.get('engines', [])
            engine = engines[0] if isinstance(engines, list) and engines else source.lower()
            
            # Quality indicator
            quality = '🔥' if score >= 8 else '✨' if score >= 6 else '📌'
            
            content += f"{quality} **{title}**\n"
            if snippet:
                # Truncate snippet
                snippet = snippet[:200] + '...' if len(snippet) > 200 else snippet
                content += f"> {snippet}\n"
            content += f"\n**来源**: {url.split('/')[2]} · [查看]({url})\n"
            content += f"**质量评分**: {score}/10 · **引擎**: {engine}\n\n"
        
        content += "---\n\n"
    
    # Footer
    content += f"""
## 📊 统计

- **搜索查询数**: {len(SEARCH_QUERIES)}
- **搜索源**: {source}
- **本期精选**: {len(results)} 条

---

*本报告由 AI Daily Report Generator 自动生成*
*聚焦高质量 Agent 架构、工程实践与研究洞察*
"""
    
    return content

if __name__ == '__main__':
    report = generate_report()
    if report:
        print("\n" + "="*60)
        print("REPORT PREVIEW:")
        print("="*60)
        print(report['content'][:2000])
        print("...")
        print(f"\n[完整报告保存在：{report['file']}]")
