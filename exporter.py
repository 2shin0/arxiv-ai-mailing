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
            # 제목에 포함될 수 있는 특수문자 처리 (예: |)
            safe_title = paper['title'].replace('|', '&#124;')
            lines.append(f"## {i}. {safe_title}")
            lines.append(f"- **Authors**: {paper['authors']}")
            lines.append(f"- **URL**: [{paper['url']}]({paper['url']})")
            # Abstract의 줄바꿈을 유지하며 인용 블록으로 처리
            abstract_formatted = '> ' + paper['abstract'].replace('\n', '\n> ')
            lines.append(f"- **Abstract**:\n{abstract_formatted}")
            lines.append("\n---\n")

    # 파일이 저장될 디렉토리가 없으면 생성
    dir_name = os.path.dirname(file_path)
    os.makedirs(dir_name, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))
    
    print(f"마크다운 파일 생성 완료: {file_path}")

def generate_index_page(category_path, title, permalink):
    """
    카테고리별 인덱스 페이지를 자동으로 생성합니다.
    """
    # 해당 카테고리의 모든 마크다운 파일 찾기 (index.md 제외)
    md_files = glob.glob(os.path.join(category_path, "*.md"))
    md_files = [f for f in md_files if not f.endswith("index.md")]
    
    # 파일명에서 날짜 추출하여 정렬 (최신순)
    date_files = []
    for file_path in md_files:
        filename = os.path.basename(file_path)
        if filename.count('-') >= 2:  # YYYY-MM-DD 형식 확인
            try:
                date_str = filename.replace('.md', '')
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                date_files.append((date_obj, date_str, filename))
            except ValueError:
                continue
    
    # 날짜순 정렬 (최신순)
    date_files.sort(reverse=True)
    
    # 인덱스 페이지 내용 생성
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
    
    # 파일 링크 생성
    for date_obj, date_str, filename in date_files:
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        link_name = date_str.replace('.md', '')
        lines.append(f"- [{year}년 {month:02d}월 {day:02d}일]({link_name}) - {date_str}")
    
    lines.append("")
    
    # 인덱스 파일 저장
    index_path = os.path.join(category_path, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))
    
    print(f"인덱스 페이지 생성 완료: {index_path}")

def update_all_indexes():
    """
    모든 카테고리의 인덱스 페이지를 업데이트합니다.
    """
    categories = [
        ("LLM", "LLM 논문 다이제스트", "/LLM/"),
        ("ALL", "전체 AI 논문 다이제스트", "/ALL/")
    ]
    
    for category, title, permalink in categories:
        if os.path.exists(category):
            generate_index_page(category, title, permalink)
