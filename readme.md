# 📰 arXiv AI Mailing

Automatically fetches, filters, and summarizes the most recent **cs.AI** papers from arXiv, then sends them via email — every day.

## 🚀 Features

- ✅ Crawls the latest papers from [arXiv cs.AI](https://arxiv.org/list/cs.AI/recent)
- ✅ Filters papers **submitted on the previous day (UTC)**
- ✅ Extracts title, authors, abstract, and link
- ✅ (Optional) Automatically summarizes and translates abstracts
- ✅ (Optional) Sends summaries via email
- ✅ Lightweight and fully automatable (e.g., GitHub Actions, cron jobs)

---

## 📦 Installation

```bash
git clone https://github.com/2shin0/arxiv-ai-mailing.git
cd arxiv-ai-mailing
pip install -r requirements.txt
