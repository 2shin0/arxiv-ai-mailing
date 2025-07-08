from datetime import datetime

def generate_digest_markdown(papers, file_path):
    today = datetime.today().strftime("%Y-%m-%d")
    lines = [f"# [arXiv Digest] {today}\n\n"]

    for i, paper in enumerate(papers, 1):
        summary_en = paper["summary_en"]
        summary_ko = paper["summary_ko"]
        lines.append(f"## {i}. {paper['title']}")
        lines.append(f"- **Authors:** {paper['authors']}")
        lines.append(f"- **URL:** {paper['url']}")
        lines.append(f"- **요약 (영문):** {summary_en}")
        lines.append(f"- **요약 (한글):** {summary_ko}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
