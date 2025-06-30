import os
import glob
from one_email_sender import send_email
from datetime import datetime

def find_latest_result_file():
    """results 폴더에서 가장 최신 결과 파일을 찾습니다."""
    # one_main.py는 one_sender 폴더 안에 있으므로 상위 폴더로 이동해야 합니다.
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_path = os.path.join(base_path, 'results', 'arxiv_*.txt')
    
    list_of_files = glob.glob(results_path)
    if not list_of_files:
        return None
    
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def main():
    """
    결과 파일에서 내용을 읽어 이메일을 전송합니다.
    """
    latest_result_file = find_latest_result_file()
    
    if not latest_result_file:
        print("처리할 결과 파일이 'results' 폴더에 없습니다.")
        return

    print(f"가장 최신 결과 파일을 사용합니다: {os.path.basename(latest_result_file)}")
    
    try:
        with open(latest_result_file, 'r', encoding='utf-8') as f:
            digest = f.read()
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return
        
    if not digest:
        print("파일 내용이 비어있습니다.")
        return

    # 이메일 제목에 날짜 포함
    today_str = datetime.today().strftime('%Y-%m-%d')
    subject = f"[arXiv AI Digest] {today_str} 논문 요약"
    
    # 이메일 전송
    email_sent = send_email(subject, digest)
    
    if email_sent:
        print("성공적으로 이메일을 전송했습니다.")
    else:
        print("이메일 전송에 실패했습니다.")

if __name__ == "__main__":
    main()