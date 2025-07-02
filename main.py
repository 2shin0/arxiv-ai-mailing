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
        lines.append("<h3>🔍 LLM 관련 논문</h3>")
        for i, paper in enumerate(llm_papers_to_display, 1):
            lines.append(f"<strong>{i}. {paper['title']}</strong>")
            lines.append(f"- Authors: {paper['authors']}")
            lines.append(f"- URL: <a href='{paper['url']}'>{paper['url']}</a>")
            lines.append(f"- 요약 (영문): {paper['summary_en']}")
            lines.append(f"- 요약 (한글): {paper['summary_ko']}<br><br>")
        
        llm_digest_url = f"{GITHUB_REPO_URL}/LLM/{today}.md"
        lines.append(f"<a href='{llm_digest_url}' target='_blank'>📎 LLM 논문 모두 보기</a><br><br>")

    if other_papers_to_display:
        lines.append("<h3>📚 전체 논문</h3>")
        for i, paper in enumerate(other_papers_to_display, 1):
            lines.append(f"<strong>{i}. {paper['title']}</strong>")
            lines.append(f"- Authors: {paper['authors']}")
            lines.append(f"- URL: <a href='{paper['url']}'>{paper['url']}</a>")
            lines.append(f"- 요약 (영문): {paper['summary_en']}")
            lines.append(f"- 요약 (한글): {paper['summary_ko']}<br><br>")

    all_digest_url = f"{GITHUB_REPO_URL}/ALL/{today}.md"
    lines.append(f"<a href='{all_digest_url}' target='_blank'>📚 전체 논문 보러가기</a>")

    return '\n'.join(lines)

def main():
    # --- 경로 및 기본 설정 ---
    today_str = datetime.today().strftime('%Y-%m-%d')
    digest_dir = "digest"
    llm_digest_dir = os.path.join(digest_dir, "LLM")
    all_digest_dir = os.path.join(digest_dir, "ALL")
    
    os.makedirs(llm_digest_dir, exist_ok=True)
    os.makedirs(all_digest_dir, exist_ok=True)

    all_md_path = os.path.join(all_digest_dir, f"{today_str}.md")
    processed_papers_path = os.path.join(all_digest_dir, f"processed_{today_str}.json")

    # --- 조건부 실행 로직 ---
    if os.path.exists(all_md_path):
        print(f"오늘의 다이제스트 파일 '{all_md_path}'이(가) 이미 존재합니다.")
        print("GitHub 배포 및 이메일 전송을 시작합니다.")
        
        if not os.path.exists(processed_papers_path):
            print(f"오류: 이메일 전송에 필요한 데이터 파일 '{processed_papers_path}'이(가) 없습니다.")
            print("프로세스를 중단합니다. 다이제스트 파일과 캐시 파일을 삭제하고 다시 실행해주세요.")
            return
        
        with open(processed_papers_path, "r", encoding="utf-8") as f:
            processed_papers = json.load(f)

    else:
        print("새로운 다이제스트 생성을 시작합니다.")
        
        # 1. 논문 크롤링
        papers = fetch_recent_ai_papers()
        if not papers:
            print("어제 등록된 논문이 없습니다.")
            return

        # 2. 논문 요약 및 번역 후 캐시 저장
        processed_papers = process_papers(papers)
        with open(processed_papers_path, "w", encoding="utf-8") as f:
            json.dump(processed_papers, f, ensure_ascii=False, indent=4)
        print(f"처리된 논문 데이터가 '{processed_papers_path}'에 저장되었습니다.")

        # 3. 마크다운 다이제스트 생성
        llm_papers_for_md = [p for p in processed_papers if LLM_PATTERN.search(p.get('title', '') + ' ' + p.get('abstract', ''))]
        llm_md_path = os.path.join(llm_digest_dir, f"{today_str}.md")

        print("LLM 관련 논문 다이제스트 생성 중...")
        generate_digest_markdown(llm_papers_for_md, llm_md_path)
        print(f"'{llm_md_path}'에 저장되었습니다.")
        
        print("전체 논문 다이제스트 생성 중...")
        generate_digest_markdown(processed_papers, all_md_path)
        print(f"'{all_md_path}'에 저장되었습니다.")

    if not processed_papers:
        print("처리할 논문이 없습니다.")
        return

    # --- 공통 실행 로직 ---
    # 4. LLM 관련 논문 분류 (이메일용)
    llm_papers = [p for p in processed_papers if LLM_PATTERN.search(p.get('title', '') + ' ' + p.get('abstract', ''))]

    # 5. GitHub으로 다이제스트 배포
    print("GitHub으로 다이제스트 배포 중...")
    try:
        result = subprocess.run(
            ["bash", "./deploy_digest.sh"], 
            check=True, 
            shell=True,
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        print("배포 성공!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"배포 실패: {e}")
        print("\n--- SCRIPT OUTPUT (STDOUT) ---")
        print(e.stdout)
        print("\n--- SCRIPT ERROR (STDERR) ---")
        print(e.stderr)
        return

    # 6. 이메일 생성 및 전송
    print("이메일 다이제스트 생성 중...")
    digest_html = make_digest(processed_papers, llm_papers)
    
    print("이메일 전송 중...")
    email_result = send_email("[arXiv AI Digest] 어제의 논문 요약", digest_html)
    
    if email_result:
        print("모든 처리가 완료되었습니다.")
    else:
        print("이메일 전송에 실패했습니다. 로그를 확인하세요.")

if __name__ == "__main__":
    main()
