import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import re

ARXIV_URL = "https://arxiv.org/list/cs.AI/recent"

def fetch_recent_ai_papers():
    print("[INFO] Fetching arXiv recent cs.AI papers...")
    response = requests.get(ARXIV_URL)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch arXiv page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    print("[INFO] Successfully parsed HTML content.")

    # 어제 날짜 (UTC 기준)
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    print(f"[INFO] Filtering papers submitted on: {yesterday.strftime('%d %b %Y')} (arXiv format)")

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
                print(f"[DEBUG] Parsed date: {submitted_dt.date()} vs {yesterday.date()}")
                if submitted_dt.date() != yesterday.date():
                    print(f"[INFO] Skipping {title}, not submitted yesterday.")
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
