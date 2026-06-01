import bibtexparser
import os
import re

os.makedirs('_publications', exist_ok=True)

with open('publications.bib', encoding='utf-8') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

print(f"📌 Found {len(bib_database.entries)} papers, generating Markdown files...")

for entry in bib_database.entries:
    # 1. 基础信息提取
    title = entry.get('title', 'Untitled').replace('{', '').replace('}', '')
    year = entry.get('year', '2026')
    venue = entry.get('booktitle') or entry.get('journal') or 'Conference/Journal'
    venue = venue.replace('{', '').replace('}', '')
    authors = entry.get('author', '').replace(' and ', ', ')
    url = entry.get('url', '').strip()
    
    # 2. 获奖信息提取
    award = entry.get('note', '').replace('{', '').replace('}', '').strip()
    award_html = f' <span style="color:red"> {award} </span>' if award else ''
    
    # 3. 构造文件名
    clean_title = re.sub(r'[^a-zA-Z0-9]', '-', title.lower())
    clean_title = re.sub(r'-+', '-', clean_title).strip('-')[:50]
    date_str = f"{year}-01-01" 
    file_name = f"{date_str}-{clean_title}.md"
    file_path = os.path.join('_publications', file_name)
    
    # 4. 构造引用文本
    citation_text = f'{authors} ({year}). "{title}." <i>{venue}</i>.{award_html}'
    download_link_md = f"[Download PDF]({url})" if url else ""
    
    # --- 关键修复：安全转义处理 ---
    # 把文本里所有的双引号转义，防止破坏 YAML 结构
    safe_title = title.replace('"', '\\"')
    safe_venue = venue.replace('"', '\\"')
    safe_citation = citation_text.replace('"', '\\"')
    
    # 全部改用双引号包裹 YAML 变量
    yaml_content = f"""---
title: "{safe_title}"
collection: publications
permalink: /publication/{date_str}-{clean_title}
date: {date_str}
venue: "{safe_venue}"
paperurl: "{url}"
citation: "{safe_citation}"
---

{award_html}

{download_link_md}
"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
        print(f"✅ Generated: {file_name}")

print("🎉 All publication Markdown files generated successfully!")