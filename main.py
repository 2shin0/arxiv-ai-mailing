from crawler import fetch_recent_ai_papers
from summarizer import summarize_text, translate_text
from email_sender import send_email
from exporter import generate_digest_markdown
from config import GITHUB_REPO_URL
from datetime import datetime
import re
import os
import json
import subprocess

LLM_PATTERN = re.compile(r'\b(llm|language model(?:s)?|(?:^|[^a-zA-Z])lm(?:$|[^a-zA-Z]))\b', re.IGNORECASE)

def process_papers(papers):
    """논문 목록을 받아 요약 및 번역을 추가합니다."""
    processed_papers = []
    total = len(papers)
    for i, paper in enumerate(papers, 1):
        print(f"[{i}/{total}] '{paper['title']}' 요약 및 번역 중...")
        try:
            summary_en = summarize_text(paper['abstract'])
            summary_ko = translate_text(summary_en)
            paper['summary_en'] = summary_en
            paper['summary_ko'] = summary_ko
            processed_papers.append(paper)
            print(f"[{i}/{total}] 완료")
        except Exception as e:
            print(f"[{i}/{total}] 처리 중 오류 발생: {e}")
    return processed_papers

def make_digest(papers, llm_papers):
    today = datetime.today().strftime('%Y-%m-%d')
    lines = [f"<strong>arXiv cs.AI 논문 요약 Digest - {today}</strong><br><br>"]

    other_papers = [p for p in papers if p not in llm_papers]
    
    llm_papers_to_display = llm_papers[:5]
    other_papers_to_display = other_papers[:5]

    if llm_papers_to_display:
        lines.append("<h3>🔤 LLM 관련 논문</h3>")
        for i, paper in enumerate(llm_papers_to_display, 1):
            lines.append(f"<strong>{i}. {paper['title']}</strong><br>")
            lines.append(f"- Authors: {paper['authors']}<br>")
            lines.append(f"- URL: <a href='{paper['url']}'>{paper['url']}</a><br>")
            lines.append(f"- 요약 (영문): {paper['summary_en']}<br>")
            lines.append(f"- 요약 (한글): {paper['summary_ko']}<br><br>")
        
        llm_digest_url = f"{GITHUB_REPO_URL}/LLM/{today}.md"
        button_html = f'''
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
  <tr>
    <td align="center" bgcolor="#2196F3" role="presentation" style="border:none;border-radius:5px;cursor:auto;mso-padding-alt:10px 20px;background:#2196F3;" valign="middle">
      <a href="{llm_digest_url}"
         style="display:inline-block;
                background:#2196F3;
                color:#ffffff;
                font-family:sans-serif;
                font-size:13px;
                font-weight:bold;
                line-height:25px;
                margin:0;
                text-decoration:none;
                text-transform:none;
                padding:10px 20px;
                mso-padding-alt:10px 20px;
                border-radius:5px;"
         target="_blank">
        🔤 LLM 논문 보러가기
      </a>
    </td>
  </tr>
</table>

        '''
        lines.append(button_html)

    if other_papers_to_display:
        lines.append("<h3 style='margin-top: 60px;'>📚 전체 논문</h3>")
        for i, paper in enumerate(other_papers_to_display, 1):
            lines.append(f"<strong>{i}. {paper['title']}</strong><br>")
            lines.append(f"- Authors: {paper['authors']}<br>")
            lines.append(f"- URL: <a href='{paper['url']}'>{paper['url']}</a><br>")
            lines.append(f"- 요약 (영문): {paper['summary_en']}<br>")
            lines.append(f"- 요약 (한글): {paper['summary_ko']}<br><br>")

    all_digest_url = f"{GITHUB_REPO_URL}/ALL/{today}.md"
    button_html = f'''
<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:separate;line-height:100%;">
  <tr>
    <td align="center" bgcolor="#2196F3" role="presentation" style="border:none;border-radius:5px;cursor:auto;mso-padding-alt:10px 20px;background:#2196F3;" valign="middle">
      <a href="{all_digest_url}"
         style="display:inline-block;
                background:#2196F3;
                color:#ffffff;
                font-family:sans-serif;
                font-size:13px;
                font-weight:bold;
                line-height:25px;
                margin:0;
                text-decoration:none;
                text-transform:none;
                padding:10px 20px;
                mso-padding-alt:10px 20px;
                border-radius:5px;"
         target="_blank">
        📚 전체 논문 보러가기
      </a>
    </td>
  </tr>
</table>
'''
    lines.append(button_html)

    return '\n'.join(lines)

def main():
    # 1. 어제자 논문 크롤링
    papers = fetch_recent_ai_papers()
    if not papers:
        print("어제 등록된 논문이 없습니다.")
        return

    # 2. 논문 요약 및 번역
    processed_papers = process_papers(papers)

    # 3. LLM 관련 논문 분류
    llm_papers = []
    for paper in processed_papers:
        combined_text = (paper['title'] + ' ' + paper['abstract'])
        if LLM_PATTERN.search(combined_text):
            llm_papers.append(paper)

    # 4. 마크다운 다이제스트 생성 및 배포
    today_str_for_md = datetime.today().strftime('%Y-%m-%d')
    digest_dir = "digest"
    llm_digest_dir = os.path.join(digest_dir, "LLM")
    all_digest_dir = os.path.join(digest_dir, "ALL")
    os.makedirs(llm_digest_dir, exist_ok=True)
    os.makedirs(all_digest_dir, exist_ok=True)

    llm_md_path = os.path.join(llm_digest_dir, f"{today_str_for_md}.md")
    all_md_path = os.path.join(all_digest_dir, f"{today_str_for_md}.md")

    print("LLM 관련 논문 다이제스트 생성 중...")
    generate_digest_markdown(llm_papers, llm_md_path)
    print(f"'{llm_md_path}'에 저장되었습니다.")
    
    print("전체 논문 다이제스트 생성 중...")
    generate_digest_markdown(processed_papers, all_md_path)
    print(f"'{all_md_path}'에 저장되었습니다.")

    print("GitHub으로 다이제스트 배포 중...")
    try:
        subprocess.run(["bash", "./deploy_digest.sh"], check=True, shell=True)
        print("배포 성공!")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"배포 실패: {e}")

    # 5. 이메일 생성 및 전송
    print("이메일 다이제스트 생성 중...")
    digest_html = make_digest(processed_papers, llm_papers)
    
    print("이메일 전송 중...")
    today = datetime.today().strftime('%Y-%m-%d')
    email_result = send_email(f"[AI 페이퍼 루틴] {today} 논문 읽는 습관 완료!", digest_html)
    
    if email_result:
        print("모든 처리가 완료되었습니다.")
    else:
        print("이메일 전송에 실패했습니다. 로그를 확인하세요.")

if __name__ == "__main__":
    main()
