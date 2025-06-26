from crawler import fetch_recent_ai_papers
from email_sender import send_email
from datetime import datetime

def main():
    papers = fetch_recent_ai_papers()
    if not papers:
        print("어제 등록된 논문이 없습니다.")
        return

    digest = make_digest(papers)
    
    # 이메일 전송 시도 및 결과 처리
    email_result = send_email("[arXiv AI Digest] 어제의 논문 요약", digest)
    
    # 이메일 전송 결과에 따른 처리
    if email_result:
        print("처리가 완료되었습니다.")
    else:
        print("이메일 전송에 실패했습니다. 로그를 확인하세요.")
        # 실패 시 다이제스트를 파일로 저장
        with open(f"arxiv_digest_{datetime.today().strftime('%Y%m%d')}.txt", "w", encoding="utf-8") as f:
            f.write(digest)
        print(f"다이제스트가 파일로 저장되었습니다: arxiv_digest_{datetime.today().strftime('%Y%m%d')}.txt")

if __name__ == "__main__":
    main()