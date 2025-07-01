from crawler import fetch_recent_ai_papers
from summarizer import summarize_text, translate_text
from email_sender import send_email
from datetime import datetime
import re
import os
import json

LLM_PATTERN = re.compile(r'\b(llm|language model(?:s)?|(?:^|[^a-zA-Z])lm(?:$|[^a-zA-Z]))\b')

def make_digest(papers):
    today = datetime.today().strftime('%Y-%m-%d')
    lines = [f"<strong>arXiv cs.AI 논문 요약 Digest - {today}</strong><br><br>"]

    llm_papers = []
    other_papers = []

    for paper in papers:
        combined_text = (paper['title'] + ' ' + paper['abstract'])
        if LLM_PATTERN.search(combined_text):
            llm_papers.append(paper)
        else:
            other_papers.append(paper)

    llm_papers = llm_papers[:5]
    other_papers = other_papers[:5]

    if llm_papers:
        lines.append("<h3>🔍 LLM 관련 논문</h3>")
        for i, paper in enumerate(llm_papers, 1):
            summary_en = summarize_text(paper['abstract'])
            summary_ko = translate_text(summary_en)
            lines.append(f"<strong>{i}. {paper['title']}</strong>")
            lines.append(f"- Authors: {paper['authors']}")
            lines.append(f"- URL: <a href='{paper['url']}'>{paper['url']}</a>")
            lines.append(f"- 요약 (영문): {summary_en}")
            lines.append(f"- 요약 (한글): {summary_ko}<br><br>")
        lines.append("<a href='https://2shin0.tistory.com/14' target='_blank'>📎 LLM 논문 모두 보기</a><br><br>")

    if other_papers:
        lines.append("<h3>📚 그 외 논문</h3>")
        for i, paper in enumerate(other_papers, 1):
            summary_en = summarize_text(paper['abstract'])
            summary_ko = translate_text(summary_en)
            lines.append(f"<strong>{i}. {paper['title']}</strong>")
            lines.append(f"- Authors: {paper['authors']}")
            lines.append(f"- URL: <a href='{paper['url']}'>{paper['url']}</a>")
            lines.append(f"- 요약 (영문): {summary_en}")
            lines.append(f"- 요약 (한글): {summary_ko}<br><br>")

    lines.append("<a href='https://2shin0.tistory.com/14' target='_blank'>📚 전체 논문 보러가기</a>")

    return '\n'.join(lines)

def main():
    papers = fetch_recent_ai_papers()
    if not papers:
        print("어제 등록된 논문이 없습니다.")
        return

    today_str = datetime.today().strftime('%y%m%d')
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    file_path = os.path.join(results_dir, f"arxiv_{today_str}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=4)
    print(f"크롤링된 논문 {len(papers)}개가 '{file_path}'에 저장되었습니다.")

    digest = make_digest(papers)
    
    # 이메일 전송 시도 및 결과 처리
    email_result = send_email("[arXiv AI Digest] 어제의 논문 요약", digest)
    
    # 이메일 전송 결과에 따른 처리
    if email_result:
        print("처리가 완료되었습니다.")
    else:
        print("이메일 전송에 실패했습니다. 로그를 확인하세요.")
        # 실패 시 다이제스트를 파일로 저장
        with open(f"arxiv_digest_{today_str}.txt", "w", encoding="utf-8") as f:
            f.write(digest)
        print(f"다이제스트가 파일로 저장되었습니다: arxiv_digest_{today_str}.txt")

if __name__ == "__main__":
    main()
