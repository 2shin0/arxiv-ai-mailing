from crawler import fetch_recent_ai_papers
from summarizer import summarize_text, translate_text
from email_sender import send_email
from datetime import datetime
import re
import os
import json
import subprocess
from exporter import generate_digest_markdown, update_all_indexes

LLM_PATTERN = re.compile(r'\b(llm|language model(?:s)?|(?:^|[^a-zA-Z])lm(?:$|[^a-zA-Z]))\b', re.IGNORECASE)

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
        llm_url = f"https://2shin0.github.io/arxiv-ai-mailing/LLM/{today}"
        lines.append(f'<a href="{llm_url}" target="_blank" style="display: inline-block; padding: 10px 15px; font-size: 14px; color: #fff; background-color: #007bff; text-decoration: none; border-radius: 5px;">📎 LLM 논문 모두 보기</a><br><br>')

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
        all_url = f"https://2shin0.github.io/arxiv-ai-mailing/ALL/{today}"
        lines.append(f'<a href="{all_url}" target="_blank" style="display: inline-block; padding: 10px 15px; font-size: 14px; color: #fff; background-color: #28a745; text-decoration: none; border-radius: 5px;">📚 전체 논문 보러가기</a>')

    return '\n'.join(lines)

def main():
    # 0. 당일 이미 메일이 발송되었는지 확인
    today_str = datetime.today().strftime('%Y-%m-%d')
    email_flag_file = f"results/{today_str}_email_sent.flag"
    
    if os.path.exists(email_flag_file):
        print(f"오늘({today_str}) 이미 메일이 발송되었습니다. 작업을 종료합니다.")
        print(f"상태 파일: {email_flag_file}")
        return
    
    # 1. 어제자 논문 크롤링
    papers = fetch_recent_ai_papers()
    if not papers:
        print("어제 등록된 논문이 없습니다.")
        return

    # 2. 크롤링 결과 저장 (JSON 백업)
    today_str = datetime.today().strftime('%y%m%d')
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    file_path = os.path.join(results_dir, f"arxiv_{today_str}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=4)
    print(f"크롤링된 논문 {len(papers)}개가 '{file_path}'에 저장되었습니다.")

    # 3. 마크다운 파일 생성 (GitHub 배포용)
    print("마크다운 다이제스트 파일을 생성합니다...")
    llm_papers = [
        p for p in papers
        if LLM_PATTERN.search(p['title'] + ' ' + p['abstract'])
    ]
    today_for_md = datetime.today().strftime('%Y-%m-%d')
    llm_md_path = os.path.join('digest', 'LLM', f"{today_for_md}.md")
    all_md_path = os.path.join('digest', 'ALL', f"{today_for_md}.md")
    generate_digest_markdown(llm_papers, llm_md_path, "LLM 관련 주요 논문")
    generate_digest_markdown(papers, all_md_path, "전체 AI 논문")

    # 3.1. 인덱스 페이지 업데이트
    print("인덱스 페이지를 업데이트합니다...")
    update_all_indexes()

    # # 4. GitHub으로 다이제스트 배포
    # print("GitHub으로 다이제스트 배포 중...")
    # try:
    #     subprocess.run(
    #         "bash ./deploy_digest.sh",
    #         check=True,
    #         shell=True
    #     )
    #     print("배포 성공!")
    # except subprocess.CalledProcessError as e:
    #     print(f"배포 실패: 스크립트가 오류 코드 {e.returncode}(으)로 종료되었습니다.")
    #     print("배포에 실패하여 이메일 전송을 건너뜁니다.")
    #     return # 배포 실패 시 여기서 중단

    # # 5. 이메일 본문 생성 및 전송
    # print("이메일 전송을 준비합니다...")
    # digest_html = make_digest(papers) # 요약/번역 기능이 포함된 이메일 본문 생성
    # email_result = send_email("[LLMxiv] 데일리 논문 리뷰", digest_html)

    # if email_result:
    #     print("모든 처리가 완료되었습니다.")
    #     # 이메일 발송 완료 후 상태 파일 생성
    #     with open(email_flag_file, "w") as f:
    #         f.write("Email sent successfully.")
    # else:
    #     print("이메일 전송에 실패했습니다. 로그를 확인하세요.")
    #     # 실패 시 다이제스트를 HTML 파일로 저장
    #     with open(f"results_html/arxiv_digest_{today_str}.html", "w", encoding="utf-8") as f:
    #         f.write(digest_html)
    #     print(f"다이제스트가 HTML 파일로 저장되었습니다: results_html/arxiv_digest_{today_str}.html")

if __name__ == "__main__":
    main()
