# -*- coding: utf-8 -*-
import os
import re
from collections import defaultdict

def replace_chinese_text(content):
    """替换中文文本中的违规词汇"""
    original = content
    
    # 定义替换规则（按优先级排序，避免冲突）
    replacements = [
        # 高优先级：完整词组替换
        ('执业医师', '专业顾问'),
        ('主治医师', '资深顾问'),
        ('主治医生', '资深顾问'),
        ('主任医师', '资深总监'),
        ('美容医生', '美丽顾问'),
        ('医疗美容', '美学服务'),
        ('医美', '美丽服务'),
        
        # 单个词汇替换
        ('执业', '专业'),
        ('医师', '顾问'),
        ('医生', '顾问'),
        ('院长', '负责人'),
        ('主任', '总监'),
        ('专家', '顾问'),
        ('主治', '资深'),
        
        ('医院', '机构'),
        ('诊所', '中心'),
        ('门诊', '接待'),
        
        ('医疗', '美学'),
        ('手术', '项目'),
        ('治疗', '服务'),
        ('就诊', '体验'),
        
        ('整形', '蜕变'),
        ('整容', '美丽升级'),
        
        ('美白', '亮肤'),
        ('祛斑', '淡斑'),
        ('祛痘', '净肤'),
        ('去皱', '紧致'),
        ('瘦脸', '小颜'),
        ('减肥', '塑形'),
        ('增高', '提升'),
        
        ('注射', '轻医美'),
        ('填充', '塑形'),
        ('移植', '优化'),
        ('植入', '导入'),
        
        ('处方', '方案'),
        ('药物', '产品'),
        ('药品', '产品'),
        ('针剂', '精华'),
        
        ('麻醉', '舒缓'),
        ('手术室', '体验区'),
        ('无菌', '洁净'),
        ('创口', '肌肤'),
        ('术后', '后续'),
        ('术前', '前期'),
    ]
    
    # 特殊修复：某些替换需要回退
    fixups = [
        # 避免"顾问团队"变成"专家团队"，应该保持"顾问团队"
        # 避免"顾问号"这样的奇怪组合
        ('顾问团队', '顾问团队'),  # 保持不变
        ('专家号', '顾问号'),
        ('资深号', '顾问号'),
    ]
    
    changes = []
    
    for old, new in replacements:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            changes.append({'old': old, 'new': new, 'count': count})
    
    # 应用修复
    for old, new in fixups:
        if old in content and old != new:
            content = content.replace(old, new)
    
    return content, changes

def process_file(filepath):
    """处理单个HTML文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changes = replace_chinese_text(content)
        
        if changes:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
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
    
    # 处理所有文件
    all_changes = {}
    total_replacements = 0
    
    for filepath in sorted(html_files):
        changes, error = process_file(filepath)
        if error:
            print(f"处理错误: {filepath} - {error}")
            continue
        if changes:
            rel_path = os.path.relpath(filepath, base_dir)
            all_changes[rel_path] = changes
            total_replacements += sum(c['count'] for c in changes)
    
    print(f"修改文件数: {len(all_changes)}")
    print(f"总替换次数: {total_replacements}")
    
    # 统计各类替换
    replace_stats = defaultdict(int)
    for changes in all_changes.values():
        for c in changes:
            replace_stats[c['old']] = replace_stats.get(c['old'], 0) + c['count']
    
    print("\n各类词汇替换统计:")
    for word, count in sorted(replace_stats.items(), key=lambda x: -x[1])[:20]:
        print(f"  {word}: {count}处")
    
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
| 医师 | 顾问 | 避免医疗人员称谓 |
| 执业医师 | 专业顾问 | 避免资质暗示 |
| 主任 | 总监 | 避免行政称谓 |
| 院长 | 负责人 | 避免管理职位 |
| 专家 | 顾问 | 避免专业权威暗示 |
| 主治 | 资深 | 避免医疗职称 |
| 医院 | 机构 | 避免医疗场所 |
| 诊所 | 中心 | 避免医疗场所 |
| 门诊 | 接待 | 避免医疗功能 |
| 医疗 | 美学 | 中性化表述 |
| 医疗美容 | 美学服务 | 避免医疗美容词汇 |
| 医美 | 美丽服务 | 避免医美词汇 |
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
| 移植 | 优化 | 中性化表述 |
| 植入 | 导入 | 中性化表述 |
| 药物/药品 | 产品 | 规避药品暗示 |
| 处方 | 方案 | 规避医疗文件 |
| 麻醉 | 舒缓 | 规避医疗程序 |
| 术后 | 后续 | 规避医疗阶段 |
| 术前 | 前期 | 规避医疗阶段 |
| 手术室 | 体验区 | 规避医疗场所 |
| 创口 | 肌肤 | 规避医疗术语 |
| 无菌 | 洁净 | 规避医疗环境 |

## 修改详情

"""
    
    for filepath, changes in sorted(all_changes.items()):
        report += f"### 📄 {filepath}\n\n"
        for change in changes:
            report += f"- `{change['old']}` → `{change['new']}` ({change['count']}处)\n"
        report += "\n"

    report += """## 注意事项

1. **保持SEO友好**：替换时考虑了SEO效果，选用语义相近的词汇
2. **URL保护**：sitemap.xml中的URL保持不变，避免链接失效
3. **可读性**：替换后内容仍保持通顺易懂
4. **建议**：清理完成后请人工检查关键页面内容，确保表述自然
5. **关于医生页面**：由于网站主要是医生介绍页面，全部替换"医生"为"顾问"后可能影响专业形象，建议后续考虑：
   - 保留医生姓名的同时，将描述性词汇如"擅长XX手术"改为"擅长XX项目"
   - 将"XX医生建议"改为"XX顾问建议"

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
