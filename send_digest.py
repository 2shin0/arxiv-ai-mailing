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
        # 메일 발송 성공 시 상태 파일 생성
        create_email_sent_flag()
    else:
        print("[실패] 이메일 발송에 실패했습니다.")
    
    return result

def find_latest_html_file():
    """가장 최근의 HTML 다이제스트 파일을 찾습니다."""
    import glob

    # 우선 고정 경로들 탐색
    candidates = []
    for path in [
        "latest_digest.html",
        *glob.glob("results_html/arxiv_digest_*.html"),
        *glob.glob("arxiv_digest_*.html"),
    ]:
        if os.path.exists(path):
            candidates.append(path)

    if not candidates and os.path.exists("results_html"):
        # 혹시 확장자가 다를 수 있으니 .html 전체를 수집
        candidates = [os.path.join("results_html", f)
                      for f in os.listdir("results_html")
                      if f.endswith(".html")]

    if not candidates:
        return None

    # 수정시간(mtime) 최신순으로 선택
    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return candidates[0]


def generate_digest_from_json():
    """JSON 파일에서 HTML 다이제스트를 생성합니다."""
    from datetime import datetime
    import glob
    import json

    def load_json_any(path):
        """JSON 또는 NDJSON 모두 지원."""
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
            # NDJSON 추정: 줄이 많고 각 줄이 {}로 시작/끝
            if "\n" in text and text.lstrip().startswith("{") and "\n{" in text:
                objs = []
                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        objs.append(json.loads(line))
                    except Exception:
                        # 한 줄이라도 실패하면 NDJSON 아님: 전체로 파싱 시도
                        objs = None
                        break
                if objs is not None:
                    return objs
            # 일반 JSON
            return json.loads(text)

    def coerce_papers(data):
        """data가 list든 dict든 papers 리스트로 강제 변환."""
        # 이미 리스트인 경우
        if isinstance(data, list):
            # 리스트 안이 dict인지 간단 검증
            if data and not isinstance(data[0], dict):
                raise ValueError("JSON 최상위 리스트 요소가 dict가 아닙니다.")
            return data

        # dict인 경우 흔한 키들을 순서대로 탐색
        if isinstance(data, dict):
            for key in ("papers", "items", "results", "data"):
                v = data.get(key)
                if isinstance(v, list):
                    return v

            # dict인데 루트가 곧 paper 하나인 경우 -> 단일 원소 리스트로 래핑
            # (ex. {"title": "...", "authors": [...]})
            # 최소한의 휴리스틱: title/summary/abstract 중 하나가 있으면 paper로 간주
            if any(k in data for k in ("title", "summary", "abstract")):
                return [data]

        # 여기까지 오면 지원 불가 구조
        raise ValueError(
            f"지원하지 않는 JSON 구조입니다 (type={type(data).__name__})."
        )

    today_str = datetime.today().strftime('%y%m%d')
    json_file = f"results/arxiv_{today_str}.json"

    # 오늘 파일이 없으면 가장 최근 파일 사용
    if not os.path.exists(json_file):
        print(f"[정보] 오늘 날짜의 JSON 파일을 찾을 수 없습니다: {json_file}")
        if os.path.exists("results"):
            json_files = glob.glob("results/arxiv_*.json")
            if json_files:
                # mtime 기준 최신
                json_files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                json_file = json_files[0]
                print(f"[정보] 가장 최근의 JSON 파일을 사용합니다: {json_file}")
            else:
                print("[오류] results 폴더에 JSON 파일이 없습니다.")
                return None
        else:
            print("[오류] results 폴더가 존재하지 않습니다.")
            return None

    try:
        data = load_json_any(json_file)
        papers = coerce_papers(data)

        if not papers:
            print("[오류] JSON 파일에 논문 데이터가 없습니다.")
            return None

        # 디버깅 보강: 타입/샘플 출력
        print(f"[정보] 로드된 papers 개수: {len(papers)} / 타입예시: {type(papers[0]).__name__}")
        if isinstance(papers[0], dict):
            sample_keys = list(papers[0].keys())[:8]
            print(f"[정보] 첫 논문 키: {sample_keys}")

        # make_digest 사용
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from main import make_digest

        html_content = make_digest(papers)

        # 파일로 저장
        os.makedirs("results_html", exist_ok=True)
        html_file = f"results_html/arxiv_digest_{today_str}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[정보] HTML 다이제스트를 생성했습니다: {html_file}")
        return html_content

    except Exception as e:
        print(f"[오류] JSON에서 HTML 생성 실패: {e}")
        return None


def create_email_sent_flag():
    """이메일 발송 성공 시 상태 파일을 생성합니다."""
    from datetime import datetime
    import os
    
    # results 디렉터리 생성
    os.makedirs("results", exist_ok=True)
    
    # 날짜 형식을 다른 파일들과 통일 (YYYY-MM-DD)
    today = datetime.today().strftime('%Y-%m-%d')
    flag_file = f"results/{today}_email_sent.flag"
    
    with open(flag_file, 'w') as f:
        f.write("email_sent")
    print(f"[정보] 이메일 발송 성공 상태 파일을 생성했습니다: {flag_file}")


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
                    # 메일 발송 성공 시 상태 파일 생성
                    create_email_sent_flag()
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
