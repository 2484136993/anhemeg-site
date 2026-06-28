#!/usr/bin/env python3
"""Generate plastic surgery guide articles HTML - 20260628"""

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

# EN Template
EN_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
    <link rel="alternate" hreflang="vi" href="{vi_url}">
    <link rel="alternate" hreflang="en" href="{canonical}">
    <link rel="stylesheet" href="../styles-en.css">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{description}",
        "url": "{canonical}",
        "publisher": {{
            "@type": "Organization",
            "name": "Anhe Meige",
            "url": "https://anhemeg.top/en/"
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
                <a href="../index.html" class="logo">Anhe<span>Meige</span></a>
                <ul class="nav-links" id="navLinks">
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../services.html">Services</a></li>
                    <li><a href="../visa.html">Visa</a></li>
                    <li><a href="../travel.html">Travel Guide</a></li>
                    <li><a href="../aftercare.html">Aftercare</a></li>
                    <li><a href="../faq.html">FAQ</a></li>
                    <li><a href="../pricing.html">Pricing</a></li>
                    <li><a href="../doctors.html">Doctors</a></li>
                    <li><a href="../recovery.html">Recovery</a></li>
                    <li><a href="../reviews.html">Reviews</a></li>
                    <li><a href="../contact.html">Contact</a></li>
                    <li><a href="../../index.html" class="lang-switch">🇨🇳 中文</a></li>
                    <li><a href="../../vi/index.html" class="lang-switch">🇻🇳 Tiếng Việt</a></li>
                </ul>
                <button class="menu-toggle" onclick="toggleMenu()" aria-label="Menu">☰</button>
            </div>
        </nav>
    </header>

    <section class="page-header">
        <div class="container">
            <h1>{title}</h1>
            <p>Anhe Meige · Plastic Surgery Guide · Updated {date_str}</p>
        </div>
    </section>

    <div class="container">
        <div class="breadcrumb">
            <a href="../index.html">Home</a>
            <span>/</span>
            <a href="index.html">News</a>
            <span>/</span>
            Plastic Surgery Guide
        </div>
    </div>

    <section class="content-wrapper">
        <div class="container">
            <article class="article-detail">
                {content}
                
                <div class="disclaimer">
                    <h3>Disclaimer</h3>
                    <p>This article is for informational purposes only and does not constitute medical advice. Plastic surgery carries inherent risks. Individual results vary based on anatomy and health status. Please consult with qualified medical professionals for personalized assessment.</p>
                </div>
            </article>
        </div>
    </section>

    <section class="contact-section">
        <div class="container">
            <h2>Learn More About Plastic Surgery in Shanghai</h2>
            <p>Contact Anhe Meige for personalized consultation.</p>
            <div class="contact-methods">
                <div class="contact-item">
                    <h3>WeChat</h3>
                    <p>kyt3158</p>
                </div>
                <div class="contact-item">
                    <h3>Phone</h3>
                    <p>+86 18221354269</p>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2026 Anhe Meige. All rights reserved.</p>
            <p>Disclaimer: This content is for informational purposes only. Please consult with qualified medical professionals.</p>
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

# VI Template
VI_TEMPLATE = '''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="zh-CN" href="{zh_url}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="alternate" hreflang="vi" href="{canonical}">
    <link rel="stylesheet" href="../styles-vi.css">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{description}",
        "url": "{canonical}",
        "publisher": {{
            "@type": "Organization",
            "name": "Anhe Meige",
            "url": "https://anhemeg.top/vi/"
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
                <a href="../index.html" class="logo">Anhe<span>Meige</span></a>
                <ul class="nav-links" id="navLinks">
                    <li><a href="../index.html">Trang chủ</a></li>
                    <li><a href="../services.html">Dịch vụ</a></li>
                    <li><a href="../visa.html">Visa</a></li>
                    <li><a href="../travel.html">Hướng dẫn du lịch</a></li>
                    <li><a href="../aftercare.html">Chăm sóc sau</a></li>
                    <li><a href="../faq.html">Câu hỏi thường gặp</a></li>
                    <li><a href="../pricing.html">Bảng giá</a></li>
                    <li><a href="../doctors.html">Bác sĩ</a></li>
                    <li><a href="../recovery.html">Hồi phục</a></li>
                    <li><a href="../reviews.html">Đánh giá</a></li>
                    <li><a href="../contact.html">Liên hệ</a></li>
                    <li><a href="../../index.html" class="lang-switch">🇨🇳 中文</a></li>
                    <li><a href="../../en/index.html" class="lang-switch">🇺🇸 English</a></li>
                </ul>
                <button class="menu-toggle" onclick="toggleMenu()" aria-label="Menu">☰</button>
            </div>
        </nav>
    </header>

    <section class="page-header">
        <div class="container">
            <h1>{title}</h1>
            <p>Anhe Meige · Hướng dẫn phẫu thuật thẩm mỹ · Cập nhật {date_str}</p>
        </div>
    </section>

    <div class="container">
        <div class="breadcrumb">
            <a href="../index.html">Trang chủ</a>
            <span>/</span>
            <a href="index.html">Tin tức</a>
            <span>/</span>
            Hướng dẫn phẫu thuật thẩm mỹ
        </div>
    </div>

    <section class="content-wrapper">
        <div class="container">
            <article class="article-detail">
                {content}
                
                <div class="disclaimer">
                    <h3>Tuyên bố miễn trừ trách nhiệm</h3>
                    <p>Bài viết này chỉ nhằm mục đích tham khảo, không cấu thành lời khuyên y tế. Phẫu thuật thẩm mỹ mang rủi ro cố hữu. Kết quả cá nhân khác nhau theo giải phẫu và tình trạng sức khỏe. Vui lòng tham vấn chuyên gia y tế đủ trình độ để đánh giá cá nhân hóa.</p>
                </div>
            </article>
        </div>
    </section>

    <section class="contact-section">
        <div class="container">
            <h2>Tìm Hiểu Thêm Về Phẫu Thuật Thẩm Mỹ Tại Thượng Hải</h2>
            <p>Liên hệ Anhe Meige để được tư vấn cá nhân hóa.</p>
            <div class="contact-methods">
                <div class="contact-item">
                    <h3>WeChat</h3>
                    <p>kyt3158</p>
                </div>
                <div class="contact-item">
                    <h3>Điện thoại</h3>
                    <p>+86 18221354269</p>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2026 Anhe Meige. Mọi quyền được bảo lưu.</p>
            <p>Tuyên bố miễn trừ trách nhiệm: Nội dung này chỉ nhằm mục đích tham khảo. Vui lòng tham vấn chuyên gia y tế đủ trình độ.</p>
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

# ZH Template
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
            <p>上海安禾美阁 · 整形手术指南 · 更新于 {date_str}</p>
        </div>
    </section>

    <div class="container">
        <div class="breadcrumb">
            <a href="index.html">首页</a>
            <span>/</span>
            <a href="news.html">新闻资讯</a>
            <span>/</span>
            整形注意事项
        </div>
    </div>

    <section class="content-wrapper">
        <div class="container">
            <article class="article-detail">
                {content}
                
                <div class="disclaimer">
                    <h3>免责声明</h3>
                    <p>本文仅供参考，不构成医疗建议。整形手术存在固有风险，个体效果因解剖结构和健康状况而异。请咨询合格的医疗专业人员以获取个性化评估和建议。</p>
                </div>
            </article>
        </div>
    </section>

    <section class="contact-section">
        <div class="container">
            <h2>了解更多上海整形信息</h2>
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
    html = re.sub(r'^# (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>\n?)+', lambda m: '<ul>' + m.group() + '</ul>', html, flags=re.DOTALL)
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
date_str = datetime.now().strftime('%B %Y')

# EN article
en_md = read_md('/app/data/所有对话/主对话/SEO优化/原创文章/20260628/plastic-surgery-shanghai-what-to-note-en.md')
fm_en, en_body = parse_frontmatter(en_md)
en_content = md_to_html(en_body)
en_html = EN_TEMPLATE.format(
    title=fm_en.get('title', 'Plastic Surgery in Shanghai Guide'),
    description=fm_en.get('description', ''),
    keywords=fm_en.get('keywords', ''),
    canonical=fm_en.get('canonical', 'https://anhemeg.top/en/plastic-surgery-shanghai-what-to-note/'),
    zh_url='https://anhemeg.top/news/plastic-surgery-shanghai-what-to-note/',
    vi_url='https://anhemeg.top/vi/phau-thuat-tham-my-thuong-hai-can-luu-y-gi/',
    date=date,
    date_str=date_str,
    content=en_content
)
with open('en/news/plastic-surgery-shanghai-what-to-note.html', 'w', encoding='utf-8') as f:
    f.write(en_html)
print("EN article created: en/news/plastic-surgery-shanghai-what-to-note.html")

# VI article
vi_md = read_md('/app/data/所有对话/主对话/SEO优化/原创文章/20260628/phau-thuat-tham-my-thuong-hai-can-luu-y-gi-vi.md')
fm_vi, vi_body = parse_frontmatter(vi_md)
vi_content = md_to_html(vi_body)
vi_html = VI_TEMPLATE.format(
    title=fm_vi.get('title', 'Phẫu Thuật Thẩm Mỹ Thượng Hải'),
    description=fm_vi.get('description', ''),
    keywords=fm_vi.get('keywords', ''),
    canonical=fm_vi.get('canonical', 'https://anhemeg.top/vi/phau-thuat-tham-my-thuong-hai-can-luu-y-gi/'),
    zh_url='https://anhemeg.top/news/plastic-surgery-shanghai-what-to-note/',
    en_url='https://anhemeg.top/en/plastic-surgery-shanghai-what-to-note/',
    date=date,
    date_str=date_str,
    content=vi_content
)
with open('vi/news/phau-thuat-tham-my-thuong-hai-can-luu-y-gi.html', 'w', encoding='utf-8') as f:
    f.write(vi_html)
print("VI article created: vi/news/phau-thuat-tham-my-thuong-hai-can-luu-y-gi.html")

# ZH article
zh_md = read_md('/app/data/所有对话/主对话/SEO优化/原创文章/20260628/plastic-surgery-shanghai-what-to-note-zh.md')
fm_zh, zh_body = parse_frontmatter(zh_md)
zh_content = md_to_html(zh_body)
zh_html = ZH_TEMPLATE.format(
    title=fm_zh.get('title', '上海整形注意事项指南'),
    description=fm_zh.get('description', ''),
    keywords=fm_zh.get('keywords', ''),
    canonical=fm_zh.get('canonical', 'https://anhemeg.top/news/plastic-surgery-shanghai-what-to-note/'),
    en_url='https://anhemeg.top/en/plastic-surgery-shanghai-what-to-note/',
    vi_url='https://anhemeg.top/vi/phau-thuat-tham-my-thuong-hai-can-luu-y-gi/',
    date=date,
    date_str=datetime.now().strftime('%Y年%m月'),
    content=zh_content
)
with open('news/plastic-surgery-shanghai-what-to-note.html', 'w', encoding='utf-8') as f:
    f.write(zh_html)
print("ZH article created: news/plastic-surgery-shanghai-what-to-note.html")

print("All articles generated successfully!")
