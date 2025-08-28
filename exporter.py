from datetime import datetime
import os
import glob

def generate_digest_markdown(papers, file_path, title):
    """
    주어진 논문 목록과 제목으로 마크다운 파일을 생성합니다.
    """
    today = datetime.today().strftime('%Y-%m-%d')
    
    lines = [f"# {title} - {today}\n"]

    if not papers:
        lines.append("해당하는 논문이 없습니다.")
    else:
        for i, paper in enumerate(papers, 1):
            safe_title = paper['title'].replace('|', '&#124;')
            lines.append(f"## {i}. {safe_title}")
            lines.append(f"- **Authors**: {paper['authors']}")
            lines.append(f"- **URL**: [{paper['url']}]({paper['url']})")
            abstract_formatted = '> ' + paper['abstract'].replace('\n', '\n> ')
            lines.append(f"- **Abstract**:\n{abstract_formatted}")
            lines.append("\n---\n")

    dir_name = os.path.dirname(file_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))
    
    print(f"마크다운 파일 생성 완료: {file_path}")

def generate_index_page(category_path, title, permalink):
    md_files = glob.glob(os.path.join(category_path, "*.md"))
    md_files = [f for f in md_files if not f.endswith("index.md")]
    
    date_files = []
    for file_path in md_files:
        filename = os.path.basename(file_path)
        if filename.count('-') >= 2:  
            try:
                date_str = filename.replace('.md', '')
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                date_files.append((date_obj, date_str, filename))
            except ValueError:
                continue
    
    date_files.sort(reverse=True)
    
    lines = [
        "---",
        "layout: default",
        f'title: "{title}"',
        f"permalink: {permalink}",
        "---",
        "",
        '<div class="header-flex">',
        f'  <h1>{title}</h1>',
        '</div>',
        "",
        f"{title.replace('논문 다이제스트', '관련 논문들의 일별 다이제스트입니다.')}",
        "",
        "## 최근 다이제스트",
        ""
    ]
    
    for date_obj, date_str, filename in date_files:
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        link_name = date_str.replace('.md', '')
        lines.append(f"- [{year}년 {month:02d}월 {day:02d}일]({link_name}) - {date_str}")
    
    lines.append("")
    
    index_path = os.path.join(category_path, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))
    
    print(f"인덱스 페이지 생성 완료: {index_path}")

def update_all_indexes():
    categories = [
        ("LLM", "LLM 논문 다이제스트", "/LLM/"),
        ("ALL", "전체 AI 논문 다이제스트", "/ALL/")
    ]
    
    for category, title, permalink in categories:
        if os.path.exists(category):
            generate_index_page(category, title, permalink)
