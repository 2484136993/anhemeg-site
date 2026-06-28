#!/usr/bin/env python3
"""Generate Chinese facelift cost article HTML - 20260627"""

import re
import os
from datetime import datetime

def read_md(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if match:
        fm = {}
        for line in match.group(1).split('\n'):
            if ': ' in line:
                key, val = line.split(': ', 1)
                fm[key] = val
        return fm, match.group(2)
    return {}, content

# ZH Article Template
ZH_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="alternate" hreflang="vi" href="{vi_url}">
    <link rel="alternate" hreflang="zh-CN" href="{canonical}">
    <link rel="stylesheet" href="styles.css">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{description}",
        "url": "{canonical}",
        "publisher": {{
            "@type": "Organization",
            "name": "上海安禾美阁",
            "url": "https://anhemeg.top/"
        }},
        "datePublished": "{date}",
        "mainEntityOfPage": "{{canonical}}"
    }}
    </script>
</head>
<body>
    <header>
        <nav>
            <div class="container">
                <a href="index.html" class="logo">上海<span>安禾美阁</span></a>
                <ul class="nav-links" id="navLinks">
                    <li><a href="index.html">首页</a></li>
                    <li><a href="about.html">关于我们</a></li>
                    <li><a href="services.html">服务项目</a></li>
                    <li><a href="doctors.html">医生团队</a></li>
                    <li><a href="contact.html">联系我们</a></li>
                    <li><a href="en/index.html" class="lang-switch">🇺🇸 English</a></li>
                    <li><a href="vi/index.html" class="lang-switch">🇻🇳 Tiếng Việt</a></li>
                </ul>
                <button class="menu-toggle" onclick="toggleMenu()" aria-label="菜单">☰</button>
            </div>
        </nav>
    </header>

    <section class="page-header">
        <div class="container">
            <h1>{title}</h1>
            <p>上海安禾美阁 · 面部年轻化指南 · 更新于 {date_str}</p>
        </div>
    </section>

    <div class="container">
        <div class="breadcrumb">
            <a href="index.html">首页</a>
            <span>/</span>
            <a href="news.html">新闻资讯</a>
            <span>/</span>
            拉皮手术费用指南
        </div>
    </div>

    <section class="content-wrapper">
        <div class="container">
            <article class="article-detail">
                {content}
                
                <div class="disclaimer">
                    <h3>免责声明</h3>
                    <p>本文仅供参考，不构成医疗建议。拉皮手术为医疗美容项目，存在一定风险性，个体效果因人而异。请在充分了解手术信息后，与合格的医疗专业人员详细咨询，做出适合自身情况的治疗决策。本文中的价格信息为参考范围，实际费用以各医疗机构正式报价为准。</p>
                </div>
            </article>
        </div>
    </section>

    <section class="contact-section">
        <div class="container">
            <h2>了解上海拉皮手术更多信息</h2>
            <p>欢迎联系上海安禾美阁获取个性化咨询服务。</p>
            <div class="contact-methods">
                <div class="contact-item">
                    <h3>微信咨询</h3>
                    <p>kyt3158</p>
                </div>
                <div class="contact-item">
                    <h3>联系电话</h3>
                    <p>+86 18221354269</p>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2026 上海安禾美阁. 保留所有权利.</p>
            <p>免责声明：本文内容仅供参考，不构成医疗建议。具体诊疗请咨询专业医护人员。</p>
        </div>
    </footer>

    <script>
        function toggleMenu() {{
            const nav = document.getElementById('navLinks');
            nav.classList.toggle('active');
        }}
    </script>
</body>
</html>'''

def md_to_html(md_content):
    html = md_content
    # H1 -> H2
    html = re.sub(r'^# (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    # H2 -> H3
    html = re.sub(r'^## (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    # H3 -> H4
    html = re.sub(r'^### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    # Lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>\n?)+', lambda m: '<ul>' + m.group() + '</ul>', html, flags=re.DOTALL)
    # Paragraphs
    paragraphs = []
    for line in html.split('\n'):
        line = line.strip()
        if line and not line.startswith('<') and line != '---':
            paragraphs.append(f'<p>{line}</p>')
        elif line:
            paragraphs.append(line)
    html = '\n'.join(paragraphs)
    return html

os.chdir('/app/data/所有对话/主对话/anhemeg-site')

date = datetime.now().strftime('%Y-%m-%d')
date_str = datetime.now().strftime('%Y年%m月')

zh_md = read_md('/app/data/所有对话/主对话/SEO优化/原创文章/20260627/facelift-surgery-cost-shanghai-2026-zh.md')
fm_zh, zh_body = parse_frontmatter(zh_md)

zh_content = md_to_html(zh_body)
zh_html = ZH_TEMPLATE.format(
    title=fm_zh.get('title', '上海拉皮手术费用完整指南2026'),
    description=fm_zh.get('description', ''),
    keywords=fm_zh.get('keywords', ''),
    canonical=fm_zh.get('canonical', 'https://anhemeg.top/news/facelift-surgery-cost-shanghai-2026/'),
    en_url='https://anhemeg.top/en/facelift-surgery-cost-shanghai-2026/',
    vi_url='https://anhemeg.top/vi/gia-cang-da-mat-thuong-hai-2026/',
    date=date,
    date_str=date_str,
    content=zh_content
)

with open('news/facelift-surgery-cost-shanghai-2026.html', 'w', encoding='utf-8') as f:
    f.write(zh_html)
print(f"ZH article created: news/facelift-surgery-cost-shanghai-2026.html")
print("Done!")
