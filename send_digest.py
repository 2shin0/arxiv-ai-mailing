#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from email_sender import send_email

def send_html_digest(html_file_path):
    """HTML 다이제스트 파일을 읽어서 이메일로 발송합니다."""
    
    # HTML 파일 존재 확인
    if not os.path.exists(html_file_path):
        print(f"[오류] HTML 파일을 찾을 수 없습니다: {html_file_path}")
        return False
    
    # HTML 파일 읽기
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"[정보] HTML 파일을 성공적으로 읽었습니다: {html_file_path}")
    except Exception as e:
        print(f"[오류] HTML 파일 읽기 실패: {e}")
        return False
    
    # 이메일 제목 생성
    file_name = os.path.basename(html_file_path)
    if 'digest' in file_name:
        subject = "[arXiv AI Digest] 오늘의 논문 요약"
    else:
        subject = f"[arXiv AI] {file_name}"
    
    # 이메일 발송
    print(f"[정보] 이메일 발송을 시작합니다...")
    print(f"[정보] 제목: {subject}")
    
    result = send_email(subject, html_content)
    
    if result:
        print("[성공] 이메일이 성공적으로 발송되었습니다!")
    else:
        print("[실패] 이메일 발송에 실패했습니다.")
    
    return result

def find_latest_html_file():
    """가장 최근의 HTML 다이제스트 파일을 찾습니다."""
    from datetime import datetime
    
    today_str = datetime.today().strftime('%y%m%d')
    
    # 가능한 HTML 파일 경로들
    possible_paths = [
        f"results_html/arxiv_digest_{today_str}.html",
        f"arxiv_digest_{today_str}.html",
        "latest_digest.html"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # results_html 디렉토리에서 가장 최근 파일 찾기
    if os.path.exists("results_html"):
        html_files = [f for f in os.listdir("results_html") if f.endswith('.html')]
        if html_files:
            html_files.sort(reverse=True)  # 최신 파일 먼저
            return os.path.join("results_html", html_files[0])
    
    return None

def generate_digest_from_json():
    """JSON 파일에서 HTML 다이제스트를 생성합니다."""
    from datetime import datetime
    import glob
    
    today_str = datetime.today().strftime('%y%m%d')
    json_file = f"results/arxiv_{today_str}.json"
    
    # 먼저 오늘 날짜의 JSON 파일을 찾아봄
    if not os.path.exists(json_file):
        print(f"[정보] 오늘 날짜의 JSON 파일을 찾을 수 없습니다: {json_file}")
        
        # results 폴더에서 가장 최근의 JSON 파일을 찾아봄
        if os.path.exists("results"):
            json_files = glob.glob("results/arxiv_*.json")
            if json_files:
                json_files.sort(reverse=True)  # 최신 파일 먼저
                json_file = json_files[0]
                print(f"[정보] 가장 최근의 JSON 파일을 사용합니다: {json_file}")
            else:
                print("[오류] results 폴더에 JSON 파일이 없습니다.")
                return None
        else:
            print("[오류] results 폴더가 존재하지 않습니다.")
            return None
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        papers = data.get('papers', [])
        if not papers:
            print("[오류] JSON 파일에 논문 데이터가 없습니다.")
            return None
        
        # main.py의 make_digest 함수를 임포트하여 사용
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from main import make_digest
        
        html_content = make_digest(papers)
        
        # HTML 파일로 저장
        os.makedirs("results_html", exist_ok=True)
        html_file = f"results_html/arxiv_digest_{today_str}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[정보] HTML 다이제스트를 생성했습니다: {html_file}")
        return html_content
        
    except Exception as e:
        print(f"[오류] JSON에서 HTML 생성 실패: {e}")
        return None

def main():
    import json
    
    # 인자가 제공된 경우 기존 방식 사용
    if len(sys.argv) == 2:
        html_file = sys.argv[1]
        
        # 상대 경로인 경우 절대 경로로 변환
        if not os.path.isabs(html_file):
            html_file = os.path.join(os.getcwd(), html_file)
        
        print(f"[정보] HTML 다이제스트 발송을 시작합니다: {html_file}")
        success = send_html_digest(html_file)
    
    # 인자가 없는 경우 자동으로 파일 찾기 또는 생성
    elif len(sys.argv) == 1:
        print("[정보] HTML 파일을 자동으로 찾거나 생성합니다...")
        
        # 1. 기존 HTML 파일 찾기
        html_file = find_latest_html_file()
        
        if html_file:
            print(f"[정보] 기존 HTML 파일을 찾았습니다: {html_file}")
            success = send_html_digest(html_file)
        else:
            print("[정보] HTML 파일이 없어서 JSON에서 생성합니다...")
            # 2. JSON에서 HTML 생성
            html_content = generate_digest_from_json()
            
            if html_content:
                # 이메일 제목 생성
                from datetime import datetime
                today = datetime.today().strftime('%Y-%m-%d')
                subject = f"[arXiv AI Digest] {today} 논문 요약"
                
                # 이메일 발송
                print(f"[정보] 이메일 발송을 시작합니다...")
                print(f"[정보] 제목: {subject}")
                
                result = send_email(subject, html_content)
                
                if result:
                    print("[성공] 이메일이 성공적으로 발송되었습니다!")
                    success = True
                else:
                    print("[실패] 이메일 발송에 실패했습니다.")
                    success = False
            else:
                print("[오류] HTML 다이제스트 생성에 실패했습니다.")
                success = False
    
    else:
        print("사용법: python send_digest.py [HTML_파일_경로]")
        print("예시: python send_digest.py arxiv_digest_250814.html")
        print("또는: python send_digest.py (자동으로 최신 파일 찾기)")
        sys.exit(1)
    
    if success:
        print("\n✅ 모든 작업이 완료되었습니다!")
    else:
        print("\n❌ 작업이 실패했습니다. 설정을 확인해주세요.")
        sys.exit(1)

if __name__ == "__main__":
    main()
