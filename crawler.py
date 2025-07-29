import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; ArxivPaperFetcher/1.0; +https://github.com/2shin0/arxiv-ai-mailing/tree/main)"
}

ARXIV_BASE_URL = "https://arxiv.org/list/cs.AI/recent"

def fetch_recent_ai_papers(max_pages=10):
    """여러 페이지를 크롤링하여 어제 등록된 모든 논문을 가져옵니다.
    
    Args:
        max_pages (int): 크롤링할 최대 페이지 수 (기본값: 10)
        
    Returns:
        list: 어제 등록된 논문 목록
    """
    print("[INFO] Fetching arXiv recent cs.AI papers...")
    
    all_papers = []
    found_target_date = False
    
    # 어제 날짜 (UTC 기준)
    # yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    # 테스트용 고정 날짜 (필요시 사용)
    yesterday = datetime(2025, 7, 29, tzinfo=timezone.utc)
    print(f"[INFO] Filtering papers submitted on: {yesterday.strftime('%Y-%m-%d')}")
    
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
            
            page_papers = parse_arxiv_page(response.text, yesterday)
            all_papers.extend(page_papers)
            
            # 이전 날짜의 논문이 나오기 시작하면 중단 (최적화)
            if len(page_papers) == 0 and found_target_date:
                print(f"[INFO] No more papers found for target date. Stopping at page {page+1}.")
                break
                
            if len(page_papers) > 0:
                found_target_date = True
                
        except Exception as e:
            print(f"[ERROR] Exception occurred while processing page {page+1}: {e}")
    
    print(f"[INFO] Total papers found: {len(all_papers)}")
    return all_papers


def parse_arxiv_page(html_content, target_date):

    soup = BeautifulSoup(html_content, "html.parser")
    
    papers = []
    total_checked = 0

    for i, (dt, dd) in enumerate(zip(soup.find_all('dt'), soup.find_all('dd'))):
        print(f"[STEP] Processing entry {i+1}")
        a_tag = dt.find('a', href=re.compile(r"^/abs/"))
        if not a_tag:
            print("[WARN] Skipping entry without valid abstract link.")
            continue

        abstract_url = "https://arxiv.org" + a_tag['href']
        print(f"[INFO] Abstract URL: {abstract_url}")

        title_tag = dd.find('div', class_='list-title')
        authors_tag = dd.find('div', class_='list-authors')
        if not title_tag or not authors_tag:
            print("[WARN] Missing title or authors.")
            continue

        title = title_tag.text.replace("Title:", "").strip()
        authors = authors_tag.text.replace("Authors:", "").strip()

        try:
            print(f"[INFO] Fetching abstract page for: {title}")
            abs_response = requests.get(abstract_url)
            if abs_response.status_code != 200:
                print(f"[ERROR] Failed to fetch abstract page for {title}. Status: {abs_response.status_code}")
                continue

            abs_soup = BeautifulSoup(abs_response.text, "html.parser")
            dateline = abs_soup.find('div', class_='dateline')
            if not dateline:
                print(f"[WARN] No dateline found for: {title}")
                continue

            submitted_text = dateline.text.strip()
            print(f"[DEBUG] {title} | {submitted_text}")

            try:
                submitted_text = submitted_text.strip('[]').replace('Submitted on ', '').strip()
                submitted_dt = datetime.strptime(submitted_text, '%d %b %Y')
                print(f"[DEBUG] Parsed date: {submitted_dt.date()} vs {target_date.date()}")
                if submitted_dt.date() != target_date.date():
                    print(f"[INFO] Skipping {title}, not submitted on target date.")
                    continue
            except Exception as e:
                print(f"[WARN] Failed to parse date for {title}: {e}")
                continue

            abstract_tag = abs_soup.find('blockquote', class_='abstract')
            if not abstract_tag:
                print(f"[WARN] No abstract block found for: {title}")
                continue

            abstract = abstract_tag.text.replace("Abstract:", "").strip()

            papers.append({
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "url": abstract_url
            })
            print(f"[INFO] Added: {title}")

        except Exception as e:
            print(f"[ERROR] Exception occurred while processing {abstract_url}: {e}")

        total_checked += 1

    print(f"[INFO] Total papers checked: {total_checked}, matched: {len(papers)}")
    return papers

if __name__ == "__main__":
    yesterday_papers = fetch_recent_ai_papers()
    for paper in yesterday_papers:
        print(paper['title'])
        print(paper['authors'])
        print(paper['abstract'][:200] + "...")
        print(paper['url'])
        print("-" * 80)
