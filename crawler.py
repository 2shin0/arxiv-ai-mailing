import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

ARXIV_URL = "https://arxiv.org/list/cs.AI/recent"

def fetch_recent_ai_papers():
    print("[INFO] Fetching arXiv recent cs.AI papers...")
    response = requests.get(ARXIV_URL)
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch arXiv page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # 어제 날짜 (UTC 기준)
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    print(f"[INFO] Filtering papers submitted on: {yesterday.strftime('%d %b %Y')} (arXiv format)")

    papers = []
    total_checked = 0

    for dt, dd in zip(soup.find_all('dt'), soup.find_all('dd')):
        id_tag = dt.find('span', class_='list-identifier')
        a_tag = None
        if id_tag:
            for a in id_tag.find_all('a'):
                if a.get('title') == 'Abstract':
                    a_tag = a
                    break

        if not a_tag:
            print("[WARN] Skipping entry without valid abstract link.")
            continue

        abstract_url = "https://arxiv.org" + a_tag['href']

        title = dd.find('div', class_='list-title').text.replace("Title:", "").strip()
        authors = dd.find('div', class_='list-authors').text.replace("Authors:", "").strip()

        try:
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
                submitted_date = submitted_text.replace('Submitted on ', '').strip()
                submitted_dt = datetime.strptime(submitted_date, '%d %b %Y')
                if submitted_dt.date() != yesterday.date():
                    continue
            except Exception as e:
                print(f"[WARN] Failed to parse date for {title}: {e}")
                continue

            abstract = abs_soup.find('blockquote', class_='abstract').text.replace("Abstract:", "").strip()

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
