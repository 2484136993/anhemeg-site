#!/usr/bin/env python3
"""Generate doctor introduction articles for zzumi.top - 20260630"""

import os
import re
from datetime import datetime

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
    <link rel="stylesheet" href="../styles.css">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{description}",
        "url": "{canonical}",
        "publisher": {{
            "@type": "Organization",
            "name": "郑州UMI有美",
            "url": "https://zzumi.top/"
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
                <a href="../index.html" class="logo">UMI<span>有美</span></a>
                <ul class="nav-links" id="navLinks">
                    <li><a href="../index.html">首页</a></li>
                    <li><a href="../services.html">服务项目</a></li>
                    <li><a href="../about.html">关于我们</a></li>
                    <li><a href="../doctors.html">专家团队</a></li>
                    <li><a href="../news.html">美丽资讯</a></li>
                    <li><a href="../contact.html">联系我们</a></li>
                </ul>
                <button class="menu-toggle" onclick="toggleMenu()" aria-label="菜单">☰</button>
            </div>
        </nav>
    </header>

    <section class="page-header">
        <div class="container">
            <h1>{title}</h1>
            <p>郑州UMI有美 · 专业塑美 · {date_str}</p>
        </div>
    </section>

    <div class="container">
        <div class="breadcrumb">
            <a href="../index.html">首页</a>
            <span>/</span>
            <a href="../news.html">美丽资讯</a>
            <span>/</span>
            <span class="current">医生介绍</span>
        </div>
    </div>

    <section class="content-wrapper">
        <div class="container">
            <article class="article-detail">
                {content}
            </article>
        </div>
    </section>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>关于UMI有美</h3>
                    <p>郑州UMI有美医疗美容门诊部是一家专业的医疗美容机构，致力于为求美者提供安全、专业、高品质的医疗美容服务。</p>
                </div>
                <div class="footer-section">
                    <h3>联系方式</h3>
                    <p>地址：郑州市二七区大学路XXX号</p>
                    <p>电话：400-XXX-XXXX</p>
                </div>
                <div class="footer-section">
                    <h3>就医指南</h3>
                    <p>本机构提醒：医疗美容存在风险，求美需谨慎。请在专业医生指导下进行术前评估。</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 郑州UMI有美 版权所有 | 豫ICP备XXXXXXXX号</p>
            </div>
        </div>
    </footer>

    <script src="../main.js"></script>
</body>
</html>
'''

def create_doctor_article(filename, title, description, keywords, doctor_name, specialty, content_body, date):
    """Create doctor introduction article HTML"""
    date_str = datetime.now().strftime("%Y年%m月%d日")
    slug = filename.replace('.html', '')
    canonical = f"https://zzumi.top/news/{slug}.html"
    
    content = f'''
<div class="article-meta">
    <span class="author">郑州UMI有美</span>
    <span class="date">{date_str}</span>
    <span class="category">医生介绍</span>
</div>

<div class="article-content">
    <h2>医生简介</h2>
    <p>{doctor_name}医生是郑州UMI有美的专业医生，在{specialty}领域具有丰富的临床经验。医生注重与求美者的沟通交流，根据个人情况提供专业的美丽方案。</p>
    
    <h2>专业擅长</h2>
    <p>{content_body}</p>
    
    <h2>服务理念</h2>
    <p>{doctor_name}医生始终坚持"安全第一、专业服务"的理念，为每位求美者提供个性化的美丽服务。</p>
    
    <h2>就医提示</h2>
    <p>本页面仅作为机构信息展示，不构成医疗建议。如有需求，请前往正规医疗机构面诊咨询。</p>
    
    <div class="disclaimer">
        <strong>免责声明：</strong>本页面内容仅供一般信息参考，不构成任何医疗建议。如有医疗需求，请直接前往正规医疗机构就诊。
    </div>
</div>
'''
    
    html = ZH_TEMPLATE.format(
        title=title,
        description=description,
        keywords=keywords,
        canonical=canonical,
        date=date,
        date_str=date_str,
        content=content
    )
    
    output_path = f"/app/data/所有对话/主对话/zzumi-site/news/{filename}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {output_path}")

# Articles data - 2 new articles for zzumi.top
articles = [
    {
        "filename": "92-郑州UMI有美刘葵医生鼻部整形口碑评价.html",
        "title": "郑州UMI有美刘葵医生鼻部整形口碑评价",
        "description": "郑州UMI有美刘葵医生鼻部整形口碑评价，擅长假体隆鼻、自体软骨鼻整形等鼻部塑形项目。",
        "keywords": "郑州UMI有美刘葵医生,鼻部整形,假体隆鼻,自体软骨鼻整形",
        "doctor": "刘葵",
        "specialty": "鼻部整形",
        "content": "刘葵医生专注于鼻部整形领域多年，擅长假体隆鼻、自体软骨鼻综合、耳软骨垫鼻尖等手术项目。医生注重鼻部与面部整体的协调美感，能够根据求美者的面部特征和个人需求，制定专属的鼻部塑形方案，帮助实现自然立体的鼻部形态。",
        "date": "2026-06-30"
    },
    {
        "filename": "93-郑州UMI有美李森林医生眼部整形服务评价.html",
        "title": "郑州UMI有美李森林医生眼部整形服务评价",
        "description": "郑州UMI有美李森林医生眼部整形服务评价，涵盖双眼皮手术、开眼角、眼袋去除等项目。",
        "keywords": "郑州UMI有美李森林医生,眼部整形,双眼皮手术,开眼角",
        "doctor": "李森林",
        "specialty": "眼部整形",
        "content": "李森林医生是眼部整形的专业医生，擅长双眼皮手术、开眼角、眼袋去除、上眼睑下垂矫正等项目。医生在眼部美学方面有着深入的研究，能够根据求美者的眼型特征和审美偏好，设计自然美观的眼部形态，帮助求美者拥有明亮有神的双眼。",
        "date": "2026-06-30"
    }
]

if __name__ == "__main__":
    print("Generating zzumi.top doctor articles - 20260630")
    print("=" * 50)
    for article in articles:
        create_doctor_article(
            article["filename"],
            article["title"],
            article["description"],
            article["keywords"],
            article["doctor"],
            article["specialty"],
            article["content"],
            article["date"]
        )
    print("=" * 50)
    print("Done! Created 2 articles for zzumi.top")
