from crawler import fetch_recent_ai_papers
from summarizer import summarize_text
from email_sender import send_email
from datetime import datetime

def make_digest(papers):
    lines = [f"## arXiv cs.AI 논문 요약 Digest - {datetime.today().strftime('%Y-%m-%d')}\n"]
    for i, paper in enumerate(papers, 1):
        summary = summarize_text(paper['abstract'])
        lines.append(f"### {i}. {paper['title']}")
        lines.append(f"- Authors: {paper['authors']}")
        lines.append(f"- URL: {paper['url']}")
        lines.append(f"- 요약: {summary}\n")
    return '\n'.join(lines)

def main():
    papers = fetch_recent_ai_papers()
    if not papers:
        print("어제 등록된 논문이 없습니다.")
        return

    digest = make_digest(papers)
    send_email("[arXiv AI Digest] 어제의 논문 요약", digest)
    print("이메일 전송 완료!")

if __name__ == "__main__":
    main()
