#!/usr/bin/env python3
"""Generate doctor introduction articles for anhemeg.top - 20260630"""

import os
import re
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
                <a href="../index.html" class="logo">安禾<span>美阁</span></a>
                <ul class="nav-links" id="navLinks">
                    <li><a href="../index.html">首页</a></li>
                    <li><a href="../services.html">服务项目</a></li>
                    <li><a href="../about.html">关于我们</a></li>
                    <li><a href="../doctors.html">专家团队</a></li>
                    <li><a href="../news.html">美丽资讯</a></li>
                    <li><a href="../contact.html">联系我们</a></li>
                    <li><a href="../en/index.html" class="lang-switch">🇺🇸 English</a></li>
                    <li><a href="../vi/index.html" class="lang-switch">🇻🇳 Tiếng Việt</a></li>
                </ul>
                <button class="menu-toggle" onclick="toggleMenu()" aria-label="菜单">☰</button>
            </div>
        </nav>
    </header>

    <section class="page-header">
        <div class="container">
            <h1>{title}</h1>
            <p>上海安禾美阁 · 专业塑美 · {date_str}</p>
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
                    <h3>关于安禾美阁</h3>
                    <p>上海安禾美阁医疗美容门诊部是一家专业的医疗美容机构，致力于为求美者提供安全、专业、高品质的医疗美容服务。</p>
                </div>
                <div class="footer-section">
                    <h3>联系方式</h3>
                    <p>地址：上海市静安区灵石路XXX号</p>
                    <p>电话：400-XXX-XXXX</p>
                </div>
                <div class="footer-section">
                    <h3>就医指南</h3>
                    <p>本机构提醒：医疗美容存在风险，求美需谨慎。请在专业医生指导下进行术前评估。</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 上海安禾美阁 版权所有 | 沪ICP备XXXXXXXX号</p>
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
    canonical = f"https://anhemeg.top/news/{slug}.html"
    en_url = f"https://anhemeg.top/en/news/{slug}.html"
    vi_url = f"https://anhemeg.top/vi/news/{slug}.html"
    
    content = f'''
<div class="article-meta">
    <span class="author">上海安禾美阁</span>
    <span class="date">{date_str}</span>
    <span class="category">医生介绍</span>
</div>

<div class="article-content">
    <h2>医生简介</h2>
    <p>{doctor_name}医生是上海安禾美阁医疗美容团队的核心成员之一，具备丰富的临床经验和专业技术。医生专注于{specialty}领域多年，始终坚持以求美者需求为中心，提供个性化的专业服务。</p>
    
    <h2>专业擅长</h2>
    <p>{content_body}</p>
    
    <h2>服务理念</h2>
    <p>{doctor_name}医生始终坚持"安全、专业、自然"的塑美理念，注重与求美者的充分沟通，了解其美丽诉求，制定科学合理的个性化方案。医生认为，每位求美者都有独特的美，应当在安全前提下实现自然和谐的美丽蜕变。</p>
    
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
    
    output_path = f"/app/data/所有对话/主对话/anhemeg-site/news/{filename}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {output_path}")

# Articles data - 5 new articles for anhemeg.top
articles = [
    {
        "filename": "268-上海安禾美阁李明医生鼻部整形专业评价.html",
        "title": "上海安禾美阁李明医生鼻部整形专业评价",
        "description": "了解上海安禾美阁李明医生在鼻部整形领域的专业评价，李明医生专注于鼻部塑形多年，为众多求美者实现自然立体美鼻。",
        "keywords": "上海安禾美阁李明医生,鼻部整形,鼻部塑形,上海整形",
        "doctor": "李明",
        "specialty": "鼻部整形",
        "content": "李明医生擅长各类鼻部整形手术，包括假体隆鼻、自体软骨鼻整形、鼻综合塑形等。医生注重鼻部与面部整体的协调美感，能够根据求美者的面部特征和个人需求，制定专属的鼻部塑形方案。在手术操作中，医生追求精细化、个性化的服务理念，力求为每位求美者打造自然美观的鼻部形态。",
        "date": "2026-06-30"
    },
    {
        "filename": "269-上海安禾美阁王芳医生眼部年轻化服务.html",
        "title": "上海安禾美阁王芳医生眼部年轻化服务",
        "description": "上海安禾美阁王芳医生眼部年轻化服务介绍，专注眼部抗衰、双眼皮、眼袋去除等眼部整形项目多年，技术娴熟。",
        "keywords": "上海安禾美阁王芳医生,眼部年轻化,眼部整形,双眼皮",
        "doctor": "王芳",
        "specialty": "眼部年轻化",
        "content": "王芳医生专注于眼部整形与年轻化领域，擅长双眼皮手术、开眼角、眼袋去除、上眼睑下垂矫正等项目。医生在眼部年轻化方面有着深入的研究，能够针对不同年龄段的求美者，制定适合的眼部抗衰方案。通过精细化的手术操作，帮助求美者重塑明亮有神的眼部轮廓。",
        "date": "2026-06-30"
    },
    {
        "filename": "270-上海安禾美阁张华医生胸部整形服务口碑.html",
        "title": "上海安禾美阁张华医生胸部整形服务口碑",
        "description": "上海安禾美阁张华医生胸部整形服务口碑评价，涵盖假体隆胸、自体脂肪隆胸等技术项目的专业介绍。",
        "keywords": "上海安禾美阁张华医生,胸部整形,隆胸手术,上海隆胸",
        "doctor": "张华",
        "specialty": "胸部整形",
        "content": "张华医生在胸部整形领域具有丰富的临床经验，熟练掌握假体隆胸、自体脂肪隆胸、乳头乳晕整形等技术。医生注重术前沟通与个性化设计，根据求美者的身形比例和个人意愿，选择最适合的隆胸方案。在手术过程中，医生严格把控每一个细节，力求实现安全、自然、满意的术后效果。",
        "date": "2026-06-30"
    },
    {
        "filename": "271-上海安禾美阁赵丽医生皮肤管理项目介绍.html",
        "title": "上海安禾美阁赵丽医生皮肤管理项目介绍",
        "description": "上海安禾美阁赵丽医生皮肤管理项目介绍，涵盖激光美肤、水光注射、化学换肤等皮肤美容服务的专业评价。",
        "keywords": "上海安禾美阁赵丽医生,皮肤管理,激光美肤,水光注射",
        "doctor": "赵丽",
        "specialty": "皮肤管理",
        "content": "赵丽医生是皮肤美容领域的专业医生，擅长运用激光、光子、水光注射等先进技术，为求美者解决各类皮肤问题。医生注重皮肤健康与美丽的结合，根据不同肤质和皮肤问题，制定个性化的皮肤管理方案。无论是色斑、痘痘、抗衰老还是肤色提亮，赵丽医生都能提供专业的皮肤美容服务。",
        "date": "2026-06-30"
    },
    {
        "filename": "272-上海安禾美阁刘洋医生面部轮廓塑形服务.html",
        "title": "上海安禾美阁刘洋医生面部轮廓塑形服务",
        "description": "上海安禾美阁刘洋医生面部轮廓塑形服务，包含下巴塑形、颧骨调整、面部脂肪填充等面部轮廓整形项目的专业介绍。",
        "keywords": "上海安禾美阁刘洋医生,面部轮廓塑形,下巴塑形,颧骨调整",
        "doctor": "刘洋",
        "specialty": "面部轮廓塑形",
        "content": "刘洋医生专注于面部轮廓雕塑领域，擅长下巴整形、颧骨调整、面部脂肪填充等手术项目。医生对面部美学有着深入的理解，能够根据求美者的面部特征和审美需求，进行精细化的轮廓雕塑。在手术设计上，医生追求自然和谐的面部比例，帮助求美者实现理想的面部轮廓线条。",
        "date": "2026-06-30"
    }
]

if __name__ == "__main__":
    print("Generating anhemeg.top doctor articles - 20260630")
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
    print("Done! Created 5 articles for anhemeg.top")
