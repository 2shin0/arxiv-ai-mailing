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

def main():
    if len(sys.argv) != 2:
        print("사용법: python send_digest.py <HTML_파일_경로>")
        print("예시: python send_digest.py arxiv_digest_250814.html")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    # 상대 경로인 경우 절대 경로로 변환
    if not os.path.isabs(html_file):
        html_file = os.path.join(os.getcwd(), html_file)
    
    print(f"[정보] HTML 다이제스트 발송을 시작합니다: {html_file}")
    
    success = send_html_digest(html_file)
    
    if success:
        print("\n✅ 모든 작업이 완료되었습니다!")
    else:
        print("\n❌ 작업이 실패했습니다. 설정을 확인해주세요.")
        sys.exit(1)

if __name__ == "__main__":
    main()
