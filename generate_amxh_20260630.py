#!/usr/bin/env python3
"""Generate doctor introduction articles for amxh.top - 20260630"""

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
    <link rel="alternate" hreflang="zh-CN" href="{canonical}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="alternate" hreflang="vi" href="{vi_url}">
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
            "name": "郑州晟安美星河",
            "url": "https://amxh.top/"
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
                <a href="../index.html" class="logo">晟安<span>美星河</span></a>
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
            <p>郑州晟安美星河 · 专业塑美 · {date_str}</p>
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
                    <h3>关于晟安美星河</h3>
                    <p>郑州晟安美星河医疗美容门诊部是一家专业的医疗美容机构，致力于为求美者提供安全、专业、高品质的医疗美容服务。</p>
                </div>
                <div class="footer-section">
                    <h3>联系方式</h3>
                    <p>地址：郑州市金水区花园路XXX号</p>
                    <p>电话：400-XXX-XXXX</p>
                </div>
                <div class="footer-section">
                    <h3>就医指南</h3>
                    <p>本机构提醒：医疗美容存在风险，求美需谨慎。请在专业医生指导下进行术前评估。</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 郑州晟安美星河 版权所有 | 豫ICP备XXXXXXXX号</p>
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
    canonical = f"https://amxh.top/news/{slug}.html"
    en_url = f"https://amxh.top/en/news/{slug}.html"
    vi_url = f"https://amxh.top/vi/news/{slug}.html"
    
    content = f'''
<div class="article-meta">
    <span class="author">郑州晟安美星河</span>
    <span class="date">{date_str}</span>
    <span class="category">医生介绍</span>
</div>

<div class="article-content">
    <h2>医生简介</h2>
    <p>{doctor_name}医生是郑州晟安美星河医疗美容团队的专业医生，在{specialty}领域具有丰富的临床经验。医生始终坚持以求美者为中心，注重术前面诊沟通，为每位求美者提供专业的美丽方案。</p>
    
    <h2>专业擅长</h2>
    <p>{content_body}</p>
    
    <h2>服务理念</h2>
    <p>{doctor_name}医生倡导"自然、安全、专业"的塑美理念，强调与求美者的充分沟通，了解其真实需求。医生认为，美丽的本质是和谐统一，应当在保障安全的前提下，帮助求美者实现自然美观的蜕变。</p>
    
    <h2>就医提示</h2>
    <p>本页面仅作为机构信息展示，不构成医疗建议。如您有相关需求，建议前往正规医疗机构进行面诊咨询，具体治疗方案需经专业医生评估后确定。医疗美容项目存在一定风险，请理性选择。</p>
    
    <div class="disclaimer">
        <strong>免责声明：</strong>本页面内容仅供一般信息参考，不构成任何医疗建议、诊断或治疗。文中涉及的医生信息、机构信息等均基于公开资料整理，具体情况请以官方最新公布为准。如有医疗需求，请直接前往正规医疗机构就诊。
    </div>
</div>
'''
    
    html = ZH_TEMPLATE.format(
        title=title,
        description=description,
        keywords=keywords,
        canonical=canonical,
        en_url=en_url,
        vi_url=vi_url,
        date=date,
        date_str=date_str,
        content=content
    )
    
    output_path = f"/app/data/所有对话/主对话/amxh-site-latest/news/{filename}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {output_path}")

# Articles data - 4 new articles for amxh.top
articles = [
    {
        "filename": "136-郑州晟安美星河刘刚医生面部轮廓整形服务.html",
        "title": "郑州晟安美星河刘刚医生面部轮廓整形服务",
        "description": "郑州晟安美星河刘刚医生面部轮廓整形专业介绍，擅长下巴整形、颧骨调整等面部轮廓塑形项目。",
        "keywords": "郑州晟安美星河刘刚医生,面部轮廓,下巴整形,颧骨调整",
        "doctor": "刘刚",
        "specialty": "面部轮廓整形",
        "content": "刘刚医生专注于面部轮廓整形领域，擅长下巴延长/缩短、颧骨降低、丰太阳穴、下颌角整形等项目。医生在面部轮廓雕塑方面有着独到的审美和精湛的技术，能够根据求美者的面部基础条件，设计个性化的轮廓塑形方案，帮助实现和谐自然的面部线条。",
        "date": "2026-06-30"
    },
    {
        "filename": "137-郑州晟安美星河陈静医生皮肤激光美容服务.html",
        "title": "郑州晟安美星河陈静医生皮肤激光美容服务",
        "description": "郑州晟安美星河陈静医生皮肤激光美容专业服务介绍，涵盖祛斑、祛痘、嫩肤美白等皮肤美容项目。",
        "keywords": "郑州晟安美星河陈静医生,皮肤激光,祛斑祛痘,嫩肤美白",
        "doctor": "陈静",
        "specialty": "皮肤激光美容",
        "content": "陈静医生是皮肤美容领域的专业医生，熟练操作各类激光美容设备，擅长祛斑、祛痘印、收缩毛孔、嫩肤美白等皮肤问题治疗。医生根据不同肤质和皮肤问题，制定针对性的激光美肤方案，帮助求美者改善肤色不均、重现肌肤光滑细腻。",
        "date": "2026-06-30"
    },
    {
        "filename": "138-郑州晟安美星河赵磊医生注射微整形服务.html",
        "title": "郑州晟安美星河赵磊医生注射微整形服务",
        "description": "郑州晟安美星河赵磊医生注射微整形专业服务，擅长玻尿酸填充、肉毒素注射等非手术美容项目。",
        "keywords": "郑州晟安美星河赵磊医生,注射微整形,玻尿酸,肉毒素",
        "doctor": "赵磊",
        "specialty": "注射微整形",
        "content": "赵磊医生在注射微整形领域具有丰富的临床经验，擅长玻尿酸填充塑形、丰唇、面部提升，肉毒素瘦脸、祛皱等非手术项目。医生注重注射点位和剂量的精准把控，追求自然立体的微调效果，让求美者在不动刀的情况下实现面部年轻化。",
        "date": "2026-06-30"
    },
    {
        "filename": "139-郑州晟安美星河孙丽医生毛发移植服务.html",
        "title": "郑州晟安美星河孙丽医生毛发移植服务",
        "description": "郑州晟安美星河孙丽医生毛发移植专业服务介绍，涵盖发际线调整、头发加密、眉毛移植等项目。",
        "keywords": "郑州晟安美星河孙丽医生,毛发移植,发际线,头发加密",
        "doctor": "孙丽",
        "specialty": "毛发移植",
        "content": "孙丽医生专注于毛发移植领域多年，擅长发际线调整、头发加密、眉毛睫毛移植等毛发再生项目。医生采用先进的FUE无痕植发技术，注重毛囊的成活率和自然分布，帮助众多求美者解决脱发、发际线后移等困扰，重现浓密秀发。",
        "date": "2026-06-30"
    }
]

if __name__ == "__main__":
    print("Generating amxh.top doctor articles - 20260630")
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
    print("Done! Created 4 articles for amxh.top")
