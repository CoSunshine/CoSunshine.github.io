import bibtexparser
import os
import re

# Ensure the target directory exists
os.makedirs('_publications', exist_ok=True)

with open('publications.bib', encoding='utf-8') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

print(f"📌 Found {len(bib_database.entries)} papers, generating Markdown files...")

for entry in bib_database.entries:
    # 1. Extract and clean basic fields
    title = entry.get('title', 'Untitled').replace('{', '').replace('}', '')
    year = entry.get('year', '2026')
    venue = entry.get('booktitle') or entry.get('journal') or 'Conference/Journal'
    venue = venue.replace('{', '').replace('}', '')
    authors = entry.get('author', '').replace(' and ', ', ')
    url = entry.get('url', '').strip()
    
    # 2. Extract award/note information (e.g., Best Paper Award)
    award = entry.get('note', '').replace('{', '').replace('}', '').strip()
    award_html = f' <span style="color:red"> {award} </span>' if award else ''
    
    # 3. Create a safe, clean filename and permalink URL
    clean_title = re.sub(r'[^a-zA-Z0-9]', '-', title.lower())
    clean_title = re.sub(r'-+', '-', clean_title).strip('-')[:50]
    date_str = f"{year}-01-01" 
    file_name = f"{date_str}-{clean_title}.md"
    file_path = os.path.join('_publications', file_name)
    
    # 4. Construct the HTML citation string
    citation_text = f'{authors} ({year}). "{title}." <i>{venue}</i>.{award_html}'

    # 5. Generate English download link in Markdown body
    download_link_md = f"[Download PDF]({url})" if url else ""
    
    # 6. Build the AcademicPages Front Matter (YAML)
    yaml_content = f"""---
title: "{title}"
collection: publications
permalink: /publication/{date_str}-{clean_title}
date: {date_str}
venue: '{venue}'
paperurl: '{url}'
citation: '{citation_text}'
---

{award_html}

{download_link_md}
"""
    
    # Write to the markdown file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
        print(f"✅ Generated: {file_name}")

print("🎉 All publication Markdown files generated successfully!")