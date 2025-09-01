# crawler.py
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
    """
    날짜 헤더(페이지 상단 h3)를 기준으로 '가장 최신 묶음'의 논문만 수집합니다.
    - 첫 페이지를 받아 최신 헤더 날짜를 감지한 뒤(target_date),
      그 날짜 섹션에 속한 항목만 모읍니다.
    - 이후 페이지를 진행하다가 더 오래된 날짜 섹션이 나타나면 중단합니다.

    Args:
        max_pages (int): 크롤링할 최대 페이지 수 (기본값: 10)

    Returns:
        list: 최신 날짜 섹션의 논문 목록
    """
    print("[INFO] Fetching arXiv recent cs.AI papers...")

    all_papers = []

    utc_now = datetime.now(timezone.utc)
    et_tz = pytz.timezone('US/Eastern')
    et_now = utc_now.astimezone(et_tz)
    cutoff = et_now.replace(hour=20, minute=0, second=0, microsecond=0)
    et_adjusted = (et_now + timedelta(days=1)).date() if et_now >= cutoff else et_now.date()
    print(f"[INFO] Current ET time: {et_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"[INFO] ET daily announcement cutoff: 20:00 ET")
    print(f"[INFO] Heuristic target date (cutoff-adjusted): {et_adjusted}")

    first_url = f"{ARXIV_BASE_URL}?skip=0&show=50"
    print("[INFO] Fetching page 1/{} (papers 1-50)".format(max_pages))
    try:
        resp = requests.get(first_url, headers=headers, timeout=30)
        if resp.status_code != 200:
            print(f"[ERROR] Failed to fetch page 1. Status code: {resp.status_code}")
            return []
        first_html = resp.text
    except Exception as e:
        print(f"[ERROR] Exception fetching page 1: {e}")
        return []

    target_date = detect_latest_header_date(first_html)
    if not target_date:
        target_date = et_adjusted
        print(f"[WARN] Failed to detect header date. Falling back to ET-adjusted date: {target_date}")
    else:
        print(f"[INFO] Detected latest header date on page: {target_date} (ET)")

    page_papers, should_continue = parse_arxiv_page_by_date_header(first_html, target_date)
    all_papers.extend(page_papers)
    print(f"[INFO] Accumulated papers after page 1: {len(all_papers)}")
    page = 2
    while should_continue and page <= max_pages:
        skip = (page - 1) * 50
        url = f"{ARXIV_BASE_URL}?skip={skip}&show=50"
        print(f"[INFO] Fetching page {page}/{max_pages} (papers {skip+1}-{skip+50})")

        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code != 200:
                print(f"[ERROR] Failed to fetch arXiv page {page}. Status code: {resp.status_code}")
                break
            time.sleep(1)  
            page_papers, should_continue = parse_arxiv_page_by_date_header(resp.text, target_date)
            all_papers.extend(page_papers)
            print(f"[INFO] Accumulated papers after page {page}: {len(all_papers)}")
        except Exception as e:
            print(f"[ERROR] Exception occurred while processing page {page}: {e}")
            break

        page += 1

    print(f"[INFO] Total papers found: {len(all_papers)}")
    return all_papers


def detect_latest_header_date(html_content):
    """
    /list/cs.AI/recent 페이지의 가장 최신 h3 헤더에서 날짜를 감지합니다.
    형식 예: "Mon, 01 Sep 2025 (new submissions)"
    성공 시 date 객체를 반환, 실패 시 None 반환.
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        h3 = soup.select_one("#dlpage h3")
        if not h3:
            h3 = soup.find("h3")
        if not h3:
            print("[WARN] No h3 header found on page.")
            return None

        date_text = h3.get_text(separator=" ", strip=True)
        print(f"[DEBUG] Latest header text: {date_text}")

        m = re.search(r'([A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4})', date_text)
        if not m:
            print("[WARN] Could not parse date from header text.")
            return None

        date_str = m.group(1)
        parsed = datetime.strptime(date_str, "%a, %d %b %Y").date()
        return parsed
    except Exception as e:
        print(f"[WARN] Exception while detecting header date: {e}")
        return None


def parse_arxiv_page_by_date_header(html_content, target_date):
    """
    날짜 헤더를 기준으로 논문을 파싱합니다.

    Args:
        html_content (str): HTML 내용
        target_date (date): 수집할 날짜(헤더 날짜)

    Returns:
        tuple[list, bool]: (논문 목록, 계속 처리할지 여부)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    papers = []
    should_continue = True
    current_date_section = None

    content_div = soup.find('div', id='dlpage')
    if not content_div:
        print("[WARN] Could not find main content div")
        return papers, False

    elements = content_div.find_all(['h3', 'dt', 'dd'])

    i = 0
    while i < len(elements):
        element = elements[i]

        if element.name == 'h3':
            date_text = element.get_text(separator=" ", strip=True)
            print(f"[DEBUG] Found date header: {date_text}")

            try:
                date_match = re.search(r'([A-Za-z]{3},\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4})', date_text)
                if date_match:
                    date_str = date_match.group(1)
                    parsed_date = datetime.strptime(date_str, '%a, %d %b %Y').date()
                    current_date_section = parsed_date
                    print(f"[DEBUG] Parsed date: {parsed_date}")

                    if parsed_date < target_date:
                        print(f"[INFO] Reached older date section ({parsed_date}). Stopping.")
                        should_continue = False
                        break
            except Exception as e:
                print(f"[WARN] Failed to parse date header '{date_text}': {e}")

        elif element.name == 'dt' and i + 1 < len(elements) and elements[i + 1].name == 'dd':
            if current_date_section == target_date:
                dt_element = element
                dd_element = elements[i + 1]

                paper = parse_single_paper(dt_element, dd_element)
                if paper:
                    papers.append(paper)
                    print(f"[INFO] Added: {paper['title']}")
            i += 1  

        i += 1

    print(f"[INFO] Papers found in this page: {len(papers)}")
    return papers, should_continue


def parse_single_paper(dt_element, dd_element):
    try:
        a_tag = dt_element.find('a', href=re.compile(r"^/abs/"))
        if not a_tag:
            return None

        abstract_url = "https://arxiv.org" + a_tag['href']

        title_tag = dd_element.find('div', class_='list-title')
        authors_tag = dd_element.find('div', class_='list-authors')

        if not title_tag or not authors_tag:
            return None

        title = re.sub(r"^\s*Title:\s*", "", title_tag.get_text(separator=" ", strip=True)).strip()
        authors = re.sub(r"^\s*Authors?:\s*", "", authors_tag.get_text(separator=" ", strip=True)).strip()

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
    try:
        resp = requests.get(abstract_url, headers=headers, timeout=30)
        if resp.status_code != 200:
            return "Abstract not available"

        soup = BeautifulSoup(resp.text, "html.parser")
        abstract_tag = soup.find('blockquote', class_='abstract')
        if abstract_tag:
            text = abstract_tag.get_text(separator=" ", strip=True)
            text = re.sub(r"^\s*Abstract:\s*", "", text).strip()
            return text
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
