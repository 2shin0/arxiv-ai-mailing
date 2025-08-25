# 📰 arXiv AI Mailing

**arXiv AI Mailing**은 arXiv에서 최신 AI 논문을 자동으로 크롤링하고, 요약 및 번역하여 이메일로 전송하는 자동화 시스템입니다. 매일 새로운 AI 연구 동향을 놓치지 않고 받아볼 수 있도록 도와줍니다.

🌐 **웹사이트**: [https://2shin0.github.io/arxiv-ai-mailing/](https://2shin0.github.io/arxiv-ai-mailing/)

## 🎯 프로젝트 개요 (Introduction)
이 프로젝트는 사용자가 arXiv에 업데이트된 AI와 LLM 논문 핵심을 빠르게 이해하고, 관심 논문을 깊이 있게 살펴볼 수 있도록 지원합니다.

### 주요 해결책
- 자동 크롤링으로 최신 논문 수집
- AI 기반 요약 및 한국어 번역
- 이메일 자동 발송으로 편리한 정보 전달
- GitHub Pages를 통한 웹 아카이브 제공

## 📦 설치 방법 (Installation)

### 1. 저장소 클론
```bash
git clone https://github.com/2shin0/arxiv-ai-mailing.git
cd arxiv-ai-mailing
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요:
```bash
# DeepL API 키 (번역용) - 무료 플랜: 월 50만 자까지 무료
DEEPL_API_KEY=your_deepl_api_key_here

# Gmail 설정 (이메일 발송용)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Google Sheets API (수신자 목록 관리용)
GOOGLE_SHEET_NAME=your_google_sheet_name
GOOGLE_WORKSHEET_NAME=your_worksheet_name
GOOGLE_API_CREDENTIALS_PATH=path/to/credentials.json
GOOGLE_SCRIPT_ID=your_google_script_id
```

## 🚀 사용 방법 (Usage)

### 기본 실행
```bash
python main.py
```

### 실행 결과 예시
```
📊 크롤링 시작: 2025-08-22
🔍 총 45개 논문 발견
📝 LLM 관련 논문: 12개
📝 기타 AI 논문: 33개

[1/12] 요약 완료: "Attention Is All You Need: A Comprehensive Survey"
[1/12] 번역 완료: "Attention Is All You Need: A Comprehensive Survey"
...

✅ 요약 및 번역 완료
📧 이메일 발송 완료: 150명
🌐 GitHub Pages 배포 완료
```

### 개별 기능 실행
```bash
# 논문 크롤링만 실행
python crawler.py

# 이메일 미리보기
python preview_email.py

# 다이제스트 배포만 실행
./deploy_digest.sh
```

## 🚀 기능 목록 (Features)

### ✅ 현재 지원 기능
- **자동 크롤링**: arXiv cs.AI 카테고리에서 전날 등록된 논문 수집
- **스마트 분류**: LLM 관련 논문과 기타 AI 논문 자동 분류
- **AI 요약**: OpenAI GPT를 활용한 논문 요약 생성
- **한국어 번역**: 영문 초록 및 요약의 한국어 번역
- **이메일 발송**: HTML 형식의 예쁜 이메일 자동 발송
- **웹 아카이브**: GitHub Pages를 통한 논문 다이제스트 웹사이트
- **Google Sheets 연동**: 수신자 목록 관리

### 🔄 추후 계획 기능
- **자동화 스케줄링**: GitHub Actions를 통한 완전 자동화

## 📁 프로젝트 구조

```
arxiv-ai-mailing/
├── main.py              # 메인 실행 파일
├── crawler.py           # arXiv 크롤링
├── summarizer.py        # 논문 요약 및 번역
├── email_sender.py      # 이메일 발송
├── exporter.py          # 마크다운 파일 생성
├── config.py            # 설정 관리
├── requirements.txt     # 의존성 목록
├── deploy_digest.sh     # GitHub Pages 배포 스크립트
├── _config.yml          # Jekyll 설정
├── index.md             # 메인 페이지
├── assets/css/          # 웹사이트 스타일
├── _layouts/            # 웹사이트 레이아웃
├── LLM/                 # LLM 논문 다이제스트
├── ALL/                 # 전체 AI 논문 다이제스트
└── digest/              # 생성된 다이제스트 파일
```

### 브랜치 구조
- **main**: GitHub Pages 웹사이트 소스 (웹 UI, 레이아웃, 설정)
- **arxiv-digest**: 논문 다이제스트 데이터 (일별 마크다운 파일)

## 📄 라이선스 (License)

이 프로젝트는 [MIT License](LICENSE)를 따릅니다.

```
MIT License

Copyright (c) 2025 2shin0

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 📞 연락처/링크 (Contact / Links)

### 🌐 관련 링크
- **웹사이트**: [https://2shin0.github.io/arxiv-ai-mailing/](https://2shin0.github.io/arxiv-ai-mailing/)
- **GitHub 저장소**: [https://github.com/2shin0/arxiv-ai-mailing](https://github.com/2shin0/arxiv-ai-mailing)
- **LLM 논문 다이제스트**: [https://2shin0.github.io/arxiv-ai-mailing/LLM/](https://2shin0.github.io/arxiv-ai-mailing/LLM/)
- **전체 AI 논문 다이제스트**: [https://2shin0.github.io/arxiv-ai-mailing/ALL/](https://2shin0.github.io/arxiv-ai-mailing/ALL/)

### 📧 연락처
- **개발자**: 2shin0
- **이슈 제보 및 기능 제안**: 02.shin0@gmail.com

---

⭐ **이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!**

📧 **매일 최신 AI 논문을 받아보고 싶으시다면 [구독 신청하기!](https://script.google.com/macros/s/AKfycbzcG6pdTr1J-Gxn5tgAyfGsNQz_2-Xhm6EtSmGm9bYHEWgAw6yN7Ew89U92sQeXKaaI/exec)**

---

# 📰 arXiv AI Mailing (English)

**arXiv AI Mailing** is an automated system that crawls the latest AI papers from arXiv, summarizes and translates them, and sends them via email. It helps you stay updated with the latest AI research trends every day.

🌐 **Website**: [https://2shin0.github.io/arxiv-ai-mailing/](https://2shin0.github.io/arxiv-ai-mailing/)

## 🎯 Project Overview (Introduction)

This project helps users quickly understand the key points of AI and LLM papers updated on arXiv and explore papers of interest in depth.

### Key Solutions
- Automatic crawling of the latest papers
- AI-powered summarization and Korean translation
- Convenient email delivery
- Web archive through GitHub Pages

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/2shin0/arxiv-ai-mailing.git
cd arxiv-ai-mailing
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables Setup
Create a `.env` file and add the following content:
```bash
# DeepL API 키 (for translation) - Free plan: Free up to 500,000 characters per month
DEEPL_API_KEY=your_deepl_api_key_here

# Gmail 설정 (for email sending)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Google Sheets API (for subscriber list management)
GOOGLE_SHEET_NAME=your_google_sheet_name
GOOGLE_WORKSHEET_NAME=your_worksheet_name
GOOGLE_API_CREDENTIALS_PATH=path/to/credentials.json
GOOGLE_SCRIPT_ID=your_google_script_id
```

## 🚀 Usage

### Basic Execution
```bash
python main.py
```

### Example Output
```
📊 Crawling started: 2025-08-22
🔍 Total 45 papers found
📝 LLM-related papers: 12
📝 Other AI papers: 33

[1/12] Summary completed: "Attention Is All You Need: A Comprehensive Survey"
[1/12] Translation completed: "Attention Is All You Need: A Comprehensive Survey"
...

✅ Summarization and translation completed
📧 Email sent to: 150 recipients
🌐 GitHub Pages deployed
```

### Individual Feature Execution
```bash
# Run crawling only
python crawler.py

# Email preview
python preview_email.py

# Deploy digest only
./deploy_digest.sh
```

## 🚀 Features

### ✅ Current Features
- **Automatic Crawling**: Collect papers submitted the previous day from arXiv cs.AI category
- **Smart Classification**: Automatically classify LLM-related papers and other AI papers
- **AI Summarization**: Generate paper summaries using OpenAI GPT
- **Korean Translation**: Translate English abstracts and summaries to Korean
- **Email Delivery**: Send beautiful HTML-formatted emails automatically
- **Web Archive**: Paper digest website through GitHub Pages
- **Google Sheets Integration**: Manage subscriber lists

### 🔄 Future Features
- **Automation Scheduling**: Complete automation through GitHub Actions

## 📁 Project Structure

```
arxiv-ai-mailing/
├── main.py              # Main execution file
├── crawler.py           # arXiv crawling
├── summarizer.py        # Paper summarization and translation
├── email_sender.py      # Email sending
├── exporter.py          # Markdown file generation
├── config.py            # Configuration management
├── requirements.txt     # Dependencies list
├── deploy_digest.sh     # GitHub Pages deployment script
├── _config.yml          # Jekyll configuration
├── index.md             # Main page
├── assets/css/          # Website styles
├── _layouts/            # Website layouts
├── LLM/                 # LLM paper digests
├── ALL/                 # All AI paper digests
└── digest/              # Generated digest files
```

### Branch Structure
- **main**: GitHub Pages website source (web UI, layouts, configurations)
- **arxiv-digest**: Paper digest data (daily markdown files)

## 📄 License

This project follows the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2025 2shin0

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 📞 Contact / Links

### 🌐 Related Links
- **Website**: [https://2shin0.github.io/arxiv-ai-mailing/](https://2shin0.github.io/arxiv-ai-mailing/)
- **GitHub Repository**: [https://github.com/2shin0/arxiv-ai-mailing](https://github.com/2shin0/arxiv-ai-mailing)
- **LLM Paper Digest**: [https://2shin0.github.io/arxiv-ai-mailing/LLM/](https://2shin0.github.io/arxiv-ai-mailing/LLM/)
- **All AI Paper Digest**: [https://2shin0.github.io/arxiv-ai-mailing/ALL/](https://2shin0.github.io/arxiv-ai-mailing/ALL/)

### 📧 Contact
- **Developer**: 2shin0
- **Issues and Feature Requests**: 02.shin0@gmail.com

---

⭐ **If this project was helpful, please give it a Star!**

📧 **Want to receive the latest AI papers daily? [Subscribe here!](https://script.google.com/macros/s/AKfycbzcG6pdTr1J-Gxn5tgAyfGsNQz_2-Xhm6EtSmGm9bYHEWgAw6yN7Ew89U92sQeXKaaI/exec)**
