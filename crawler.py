import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import re
import time
import pytz

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; ArxivPaperFetcher/1.0; +https://github.com/2shin0/arxiv-ai-mailing/tree/main)"
}

ARXIV_BASE_URL = "https://arxiv.org/list/cs.AI/recent"

def fetch_recent_ai_papers(max_pages=10):
    """날짜 헤더를 기준으로 오늘 공개된 논문을 효율적으로 가져옵니다.
    
    Args:
        max_pages (int): 크롤링할 최대 페이지 수 (기본값: 10)
        
    Returns:
        list: 오늘 공개된 논문 목록
    """
    print("[INFO] Fetching arXiv recent cs.AI papers...")
    
    all_papers = []
    
    # 오늘 날짜 (ET 기준) - arXiv는 ET 기준으로 운영
    # EST/EDT 자동 처리
    utc_now = datetime.now(timezone.utc)
    et_tz = pytz.timezone('US/Eastern')
    et_now = utc_now.astimezone(et_tz)
    target_date = et_now.date()
    
    print(f"[INFO] Looking for papers announced on: {target_date.strftime('%Y-%m-%d')} (ET)")
    
    for page in range(max_pages):
        skip = page * 50
        url = f"{ARXIV_BASE_URL}?skip={skip}&show=50"
        print(f"[INFO] Fetching page {page+1}/{max_pages} (papers {skip+1}-{skip+50})")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"[ERROR] Failed to fetch arXiv page {page+1}. Status code: {response.status_code}")
                continue
                
            # 서버 부하 방지를 위한 대기
            time.sleep(1)
            
            page_papers, should_continue = parse_arxiv_page_by_date_header(response.text, target_date)
            all_papers.extend(page_papers)
            
            # 오늘 날짜 섹션이 끝나면 중단
            if not should_continue:
                print(f"[INFO] Finished processing today's papers. Stopping at page {page+1}.")
                break
                
        except Exception as e:
            print(f"[ERROR] Exception occurred while processing page {page+1}: {e}")
    
    print(f"[INFO] Total papers found: {len(all_papers)}")
    return all_papers


def parse_arxiv_page_by_date_header(html_content, target_date):
    """날짜 헤더를 기준으로 논문을 파싱합니다.
    
    Args:
        html_content (str): HTML 내용
        target_date (date): 찾고자 하는 날짜
        
    Returns:
        tuple: (논문 목록, 계속 처리할지 여부)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    papers = []
    should_continue = True
    current_date_section = None
    
    # 모든 요소를 순차적으로 처리
    content_div = soup.find('div', id='dlpage')
    if not content_div:
        print("[WARN] Could not find main content div")
        return papers, False
    
    elements = content_div.find_all(['h3', 'dt', 'dd'])
    
    i = 0
    while i < len(elements):
        element = elements[i]
        
        # 날짜 헤더 확인
        if element.name == 'h3':
            date_text = element.get_text().strip()
            print(f"[DEBUG] Found date header: {date_text}")
            
            # 날짜 파싱 (예: "Mon, 25 Aug 2025 (showing first 50 of 143 entries)")
            try:
                # 날짜 부분만 추출
                date_match = re.search(r'(\w+,\s+\d+\s+\w+\s+\d+)', date_text)
                if date_match:
                    date_str = date_match.group(1)
                    # "Mon, 25 Aug 2025" -> datetime
                    parsed_date = datetime.strptime(date_str, '%a, %d %b %Y').date()
                    current_date_section = parsed_date
                    print(f"[DEBUG] Parsed date: {parsed_date}")
                    
                    # 오늘 날짜가 아닌 이전 날짜 섹션이 나오면 중단
                    if parsed_date < target_date:
                        print(f"[INFO] Reached older date section ({parsed_date}). Stopping.")
                        should_continue = False
                        break
                        
            except Exception as e:
                print(f"[WARN] Failed to parse date header '{date_text}': {e}")
        
        # dt, dd 쌍으로 논문 정보 처리
        elif element.name == 'dt' and i + 1 < len(elements) and elements[i + 1].name == 'dd':
            # 현재 날짜 섹션이 오늘 날짜인 경우에만 논문 추가
            if current_date_section == target_date:
                dt_element = element
                dd_element = elements[i + 1]
                
                paper = parse_single_paper(dt_element, dd_element)
                if paper:
                    papers.append(paper)
                    print(f"[INFO] Added: {paper['title']}")
            
            i += 1  # dd 요소도 건너뛰기
        
        i += 1
    
    print(f"[INFO] Papers found in this page: {len(papers)}")
    return papers, should_continue


def parse_single_paper(dt_element, dd_element):
    """개별 논문 정보를 파싱합니다."""
    try:
        # arXiv ID 및 URL 추출
        a_tag = dt_element.find('a', href=re.compile(r"^/abs/"))
        if not a_tag:
            return None
            
        abstract_url = "https://arxiv.org" + a_tag['href']
        
        # 제목과 저자 추출
        title_tag = dd_element.find('div', class_='list-title')
        authors_tag = dd_element.find('div', class_='list-authors')
        
        if not title_tag or not authors_tag:
            return None
            
        title = title_tag.text.replace("Title:", "").strip()
        authors = authors_tag.text.replace("Authors:", "").strip()
        
        # 초록은 개별 페이지에서 가져오기 (필요시)
        abstract = get_abstract_from_url(abstract_url)
        
        return {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "url": abstract_url
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to parse paper: {e}")
        return None


def get_abstract_from_url(abstract_url):
    """개별 논문 페이지에서 초록을 가져옵니다."""
    try:
        response = requests.get(abstract_url, headers=headers)
        if response.status_code != 200:
            return "Abstract not available"
            
        soup = BeautifulSoup(response.text, "html.parser")
        abstract_tag = soup.find('blockquote', class_='abstract')
        
        if abstract_tag:
            return abstract_tag.text.replace("Abstract:", "").strip()
        else:
            return "Abstract not available"
            
    except Exception as e:
        print(f"[WARN] Failed to fetch abstract from {abstract_url}: {e}")
        return "Abstract not available"


if __name__ == "__main__":
    today_papers = fetch_recent_ai_papers()
    for paper in today_papers:
        print(paper['title'])
        print(paper['authors'])
        print(paper['abstract'][:200] + "...")
        print(paper['url'])
        print("-" * 80)
