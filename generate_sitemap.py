# -*- coding: utf-8 -*-
import os
from datetime import datetime

def generate_sitemap(base_dir, domain='https://anhemeg.top'):
    """根据HTML文件生成sitemap.xml"""
    
    # 定义页面优先级
    priority_map = {
        'index.html': 0.9,
        'about.html': 0.8,
        'contact.html': 0.8,
        'doctors.html': 0.8,
        'services.html': 0.8,
        'news.html': 0.8,
    }
    
    priority_default = 0.7
    
    # 定义更新频率
    changefreq_map = {
        'index.html': 'daily',
        'about.html': 'weekly',
        'contact.html': 'weekly',
        'doctors.html': 'weekly',
        'services.html': 'weekly',
        'news.html': 'daily',
    }
    
    changefreq_default = 'weekly'
    
    urls = []
    
    # 收集所有HTML文件
    for root, dirs, files in os.walk(base_dir):
        for file in sorted(files):
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, base_dir)
                
                # 构建URL
                if rel_path == 'index.html':
                    url = domain
                else:
                    url = f"{domain}/{rel_path}"
                
                # 确定优先级
                if file in priority_map:
                    priority = priority_map[file]
                elif rel_path.startswith('doctors/'):
                    priority = 0.6
                elif rel_path.startswith('guide/'):
                    priority = 0.6
                elif rel_path.startswith('news/'):
                    priority = 0.7
                else:
                    priority = priority_default
                
                # 确定更新频率
                if file in changefreq_map:
                    changefreq = changefreq_map[file]
                elif rel_path.startswith('news/'):
                    changefreq = 'weekly'
                else:
                    changefreq = changefreq_default
                
                urls.append({
                    'loc': url,
                    'lastmod': '2026-05-01',  # 统一使用当前日期
                    'changefreq': changefreq,
                    'priority': priority
                })
    
    # 生成XML
    today = datetime.now().strftime('%Y-%m-%d')
    
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for url in urls:
        xml_lines.append('    <url>')
        xml_lines.append(f'        <loc>{url["loc"]}</loc>')
        xml_lines.append(f'        <lastmod>{today}</lastmod>')
        xml_lines.append(f'        <changefreq>{url["changefreq"]}</changefreq>')
        xml_lines.append(f'        <priority>{url["priority"]}</priority>')
        xml_lines.append('    </url>')
    
    xml_lines.append('</urlset>')
    
    return '\n'.join(xml_lines)

# 生成sitemap.xml
sitemap = generate_sitemap('anhemeg-site')

# 保存
with open('anhemeg-site/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f"sitemap.xml 已重新生成")
print(f"包含 {sitemap.count('<url>')} 个URL")
