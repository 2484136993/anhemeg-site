import os
import re
from collections import defaultdict

# 定义违规词汇和替换规则
REPLACEMENTS = {
    # 医疗相关
    r'\b医生\b': '顾问',
    r'\b医师\b': '专家',
    r'\b主治\b': '资深',
    r'\b执业医师\b': '专业顾问',
    r'\b主任\b': '总监',
    r'\b专家(?!号|家|业)': '顾问',  # 专家后面不是号/家/业
    
    # 医院/诊所相关
    r'\b医院\b': '机构',
    r'\b诊所\b': '中心',
    r'\b门诊\b': '接待',
    
    # 医疗相关
    r'\b医疗\b': '美学',
    r'\b手术\b': '项目',
    r'\b治疗\b': '服务',
    r'\b就诊\b': '体验',
    
    # 整形相关
    r'\b整形\b': '蜕变',
    r'\b整容\b': '美丽升级',
    
    # 效果承诺
    r'\b美白\b': '亮肤',
    r'\b祛斑\b': '淡斑',
    r'\b祛痘\b': '净肤',
    r'\b去皱\b': '紧致',
    r'\b瘦脸\b': '小颜',
    r'\b减肥\b': '塑形',
    r'\b增高\b': '提升',
    
    # 注射填充
    r'\b注射\b': '轻医美',
    r'\b填充\b': '塑形',
    r'\b移植\b': '优化',
    r'\b植入\b': '导入',
    
    # 药品相关
    r'\b处方\b': '方案',
    r'\b药物\b': '产品',
    r'\b药品\b': '产品',
    r'\b针剂\b': '精华',
    
    # 其他
    r'\b麻醉\b': '舒缓',
    r'\b手术室\b': '体验区',
    r'\b无菌\b': '洁净',
    r'\b创口\b': '肌肤',
    r'\b术后\b': '后续',
    r'\b术前\b': '前期',
}

# 需要特殊处理的词汇（在URL中保持不变）
SPECIAL_CASES = [
    ('医疗美容', '美学服务'),
    ('医疗', '美学'),
]

def scan_file(filepath):
    """扫描文件，返回违规词汇出现位置"""
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检测违规词汇
        violation_words = [
            '医生', '医师', '主治', '主任', '专家', '执业医师',
            '医院', '诊所', '门诊', '医疗', '手术', '治疗', '就诊',
            '整形', '整容',
            '美白', '祛斑', '祛痘', '去皱', '瘦脸', '减肥', '增高',
            '注射', '填充', '移植', '植入',
            '处方', '药物', '药品', '针剂',
            '麻醉', '手术室', '无菌', '创口', '术后', '术前'
        ]
        
        for word in violation_words:
            pattern = re.escape(word)
            matches = list(re.finditer(pattern, content))
            if matches:
                # 获取上下文
                contexts = []
                for m in matches[:3]:  # 最多显示3个上下文
                    start = max(0, m.start() - 20)
                    end = min(len(content), m.end() + 20)
                    ctx = content[start:end]
                    contexts.append(f"  ...{ctx}...")
                violations.append({
                    'word': word,
                    'count': len(matches),
                    'contexts': contexts
                })
    except Exception as e:
        return [], str(e)
    return violations, None

def replace_file(filepath):
    """替换文件中的违规词汇"""
    changes = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 先处理特殊组合词
        content = content.replace('医疗美容', '美学服务')
        content = content.replace('医美', '美丽服务')  # 特殊处理
        
        # 处理URL中的词汇（保护URL结构）
        # 提取所有URL
        urls = re.findall(r'https?://[^\s<>"\']+', content)
        url_placeholder = {}
        for i, url in enumerate(urls):
            placeholder = f"__URL_PLACEHOLDER_{i}__"
            url_placeholder[placeholder] = url
            content = content.replace(url, placeholder)
        
        # 应用替换规则
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                count = len(re.findall(pattern, content))
                changes.append({
                    'pattern': pattern,
                    'replacement': replacement,
                    'count': count
                })
                content = new_content
        
        # 恢复URL
        for placeholder, url in url_placeholder.items():
            content = content.replace(placeholder, url)
        
        # 特殊处理：保留一些必要的上下文
        # 恢复 "专家" 在特定组合中的使用
        content = re.sub(r'顾问(?=[^\s]*家)', '专家', content)  # 如"专家团队"
        content = re.sub(r'顾问(?=[^\s]*号)', '专家', content)  # 如"专家号"
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes, None
        return [], None
        
    except Exception as e:
        return [], str(e)

def main():
    base_dir = 'anhemeg-site'
    html_files = []
    
    # 收集所有HTML文件
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"找到 {len(html_files)} 个HTML文件")
    print("=" * 60)
    
    # 第一遍：扫描所有文件
    all_violations = {}
    for filepath in sorted(html_files):
        violations, error = scan_file(filepath)
        if error:
            print(f"扫描错误: {filepath} - {error}")
            continue
        if violations:
            all_violations[filepath] = violations
    
    print(f"\n包含违规词汇的文件: {len(all_violations)} 个")
    
    # 打印扫描结果
    total_violations = 0
    for filepath, violations in all_violations.items():
        rel_path = os.path.relpath(filepath, base_dir)
        print(f"\n📄 {rel_path}")
        for v in violations:
            print(f"   [{v['word']}] 出现 {v['count']} 次")
            total_violations += v['count']
    
    print(f"\n总计发现 {total_violations} 处违规词汇")
    print("=" * 60)
    
    # 第二遍：执行替换
    print("\n开始执行替换...")
    all_changes = {}
    for filepath in sorted(html_files):
        changes, error = replace_file(filepath)
        if error:
            print(f"替换错误: {filepath} - {error}")
            continue
        if changes:
            rel_path = os.path.relpath(filepath, base_dir)
            all_changes[rel_path] = changes
    
    print(f"已完成 {len(all_changes)} 个文件的替换")
    
    # 生成报告
    report = """# 违规词清理报告

## 清理概况
- 执行时间：自动生成
- 处理文件总数：{total_files}
- 修改文件数：{modified_files}
- 总替换次数：{total_replacements}

## 替换规则对照表

| 违规词 | 替换词 | 说明 |
|--------|--------|------|
| 医生 | 顾问 | 避免医疗人员称谓 |
| 医师 | 专家 | 避免医疗人员称谓 |
| 主任 | 总监 | 避免行政称谓 |
| 专家 | 顾问 | 避免专业权威暗示 |
| 执业医师 | 专业顾问 | 避免资质暗示 |
| 医院 | 机构 | 避免医疗场所 |
| 诊所 | 中心 | 避免医疗场所 |
| 门诊 | 接待 | 避免医疗功能 |
| 医疗 | 美学 | 中性化表述 |
| 手术 | 项目 | 避免侵入性暗示 |
| 治疗 | 服务 | 中性化表述 |
| 就诊 | 体验 | 中性化表述 |
| 整形 | 蜕变 | 规避整形词汇 |
| 整容 | 美丽升级 | 规避整容词汇 |
| 美白 | 亮肤 | 规避效果承诺 |
| 祛斑 | 淡斑 | 规避效果承诺 |
| 祛痘 | 净肤 | 规避效果承诺 |
| 瘦脸 | 小颜 | 规避效果承诺 |
| 注射 | 轻医美 | 规避侵入性操作 |
| 填充 | 塑形 | 中性化表述 |
| 麻醉 | 舒缓 | 规避医疗程序 |
| 术后 | 后续 | 规避医疗阶段 |
| 术前 | 前期 | 规避医疗阶段 |
| 药物/药品 | 产品 | 规避药品暗示 |

## 修改详情

""".format(
    total_files=len(html_files),
    modified_files=len(all_changes),
    total_replacements=sum(len(c) for c in all_changes.values())
)

    for filepath, changes in sorted(all_changes.items()):
        report += f"### 📄 {filepath}\n\n"
        for change in changes:
            report += f"- `{change['pattern']}` → `{change['replacement']}` ({change['count']}处)\n"
        report += "\n"

    report += """## 注意事项

1. **保持SEO友好**：替换时考虑了SEO效果，选用语义相近的词汇
2. **URL保护**：sitemap.xml中的URL保持不变，避免链接失效
3. **可读性**：替换后内容仍保持通顺易懂
4. **建议**：清理完成后请人工检查关键页面内容，确保表述自然

---
*本报告由自动化脚本生成*
"""

    # 保存报告
    report_path = os.path.join(base_dir, '违规词清理报告.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 清理报告已生成: {report_path}")
    
    return all_changes

if __name__ == '__main__':
    main()
