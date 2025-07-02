from datetime import datetime
import os

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
