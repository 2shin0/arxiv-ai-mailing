> 보다 자세한 내용은 [위키독스](https://wikidocs.net/book/19300)를 참고해 주세요.

# 📰 arXiv AI Mailing

**arXiv AI Mailing**은 arXiv에서 최신 AI 논문을 자동으로 크롤링하고, 요약 및 번역하여 이메일로 전송하는 자동화 시스템입니다. 매일 새로운 AI 연구 동향을 놓치지 않고 받아볼 수 있도록 도와줍니다.

🌐 **웹사이트**: [https://2shin0.github.io/arxiv-ai-mailing/](https://2shin0.github.io/arxiv-ai-mailing/)

## 🎯 프로젝트 개요
이 프로젝트는 사용자가 arXiv에 업데이트된 AI와 LLM 논문 핵심을 빠르게 이해하고, 관심 논문을 깊이 있게 살펴볼 수 있도록 지원합니다.

### 주요 해결책
- GitHub Actions로 매일 자동 실행
- 자동 크롤링으로 최신 논문 수집
- AI 기반 요약 및 한국어 번역
- 이메일 자동 발송으로 편리한 정보 전달
- GitHub Pages를 통한 웹 아카이브 제공

## 🤖 자동화 시스템

### ⏰ 자동 실행 스케줄
- **매일 오전 10시 (KST)**: 기본 실행
- **오전 11시 (KST)**: 재시도 (실패 시)
- **오후 12시 (KST)**: 최종 재시도 (실패 시)
- **주말**: 자동 건너뜀 (arXiv 업데이트 없음)

### 재시도 로직
- 성공 시 나머지 시간대 자동 건너뜀
- 중복 처리 방지 기능
- 실행 상태 및 에러 로그 자동 기록

### 📊 모니터링 기능
- GitHub Actions Summary에서 실행 결과 확인
- 처리된 논문 수, 성공/실패 상태 표시
- 실행 로그 자동 저장 (7일간 보관)

## 📦 설치 방법

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

### 4. GitHub Secrets 설정 (자동화용)
GitHub Actions 자동화를 위해 저장소에 다음 시크릿을 설정하세요:

1. GitHub 저장소 → 설정 → 시크릿 및 변수 → Actions
2. 다음 시크릿을 추가하세요:

```bash
# 필수 시크릿
DEEPL_API_KEY=your_deepl_api_key_here
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIPIENT=recipient@example.com

# Google Sheets 연동
GOOGLE_SHEET_NAME=your_google_sheet_name
GOOGLE_WORKSHEET_NAME=your_worksheet_name
GOOGLE_SCRIPT_ID=your_google_script_id
GOOGLE_API_CREDENTIALS={"type":"service_account",...}  # 전체 JSON 내용

# GitHub Actions (선택사항)
PERSONAL_ACCESS_TOKEN=ghp_your_token_here  # 브랜치 작업을 위한 토큰
```

**중요한 사항:**
- `GOOGLE_API_CREDENTIALS`: 서비스 계정 자격 증명의 전체 JSON 내용을 붙여넣으세요
- `EMAIL_PASSWORD`: Gmail 앱 비밀번호를 사용하세요 (정규 비밀번호가 아닙니다)
- `PERSONAL_ACCESS_TOKEN`: 권한 문제가 발생할 경우에만 필요합니다

## 🚀 사용 방법 (Usage)

### 자동 실행 (권장)
GitHub Actions가 매일 자동으로 실행됩니다. 별도 작업이 필요 없습니다!

### 수동 실행 (테스트용)
1. GitHub 리포지토리 → Actions → "Daily arXiv AI Papers Digest"
2. "Run workflow" 버튼 클릭하여 즉시 실행

### 로컬 실행 (개발용)
```bash
# 의존성 설치
pip install -r requirements.txt

# 기본 실행
python main.py
```

### 실행 결과 예시
```
📊 크롤링 시작: 2025-08-25
🔍 총 143개 논문 발견
📝 LLM 관련 논문: 25개
📝 기타 AI 논문: 118개

[1/25] 요약 완료: "Attention Is All You Need: A Comprehensive Survey"
[1/25] 번역 완료: "Attention Is All You Need: A Comprehensive Survey"
...

✅ 요약 및 번역 완료
📧 이메일 발송 완료: 150명
🌐 GitHub Pages 배포 완료
```

### 개별 기능 실행
```bash
# 크롤링만 실행
python crawler.py

# 이메일 미리보기
python preview_email.py

# 다이제스트만 배포
./deploy_digest.sh
```

## 🚀 기능 목록 (Features)

### ✅ 현재 지원 기능
- **완전 자동화**: GitHub Actions를 통한 매일 자동 실행
- **자동 크롤링**: arXiv cs.AI 카테고리에서 전날 등록된 논문 수집
- **스마트 분류**: LLM 관련 논문과 기타 AI 논문 자동 분류
- **AI 요약**: google/pegasus-cnn_dailymail 모델을 활용한 논문 요약 생성
- **한국어 번역**: DeepL API를 통한 고품질 번역
- **이메일 발송**: HTML 형식의 예쁜 이메일 자동 발송
- **웹 아카이브**: GitHub Pages를 통한 논문 다이제스트 웹사이트
- **Google Sheets 연동**: 수신자 목록 관리
- **재시도 로직**: 자동 재시도 (11 AM, 12 PM)
- **모니터링**: 자동 실행 상태 및 에러 로그 기록

## 📁 프로젝트 구조

```
arxiv-ai-mailing/
├── .github/workflows/
│   └── daily-arxiv-digest.yml  # GitHub Actions 워크플로우
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

## 📞 연락처/링크 (Contact / Links)

### 🌐 관련 링크
- **웹사이트**: [https://2shin0.github.io/arxiv-ai-mailing/](https://2shin0.github.io/arxiv-ai-mailing/)
- **GitHub 저장소**: [https://github.com/2shin0/arxiv-ai-mailing](https://github.com/2shin0/arxiv-ai-mailing)
- **LLM 논문 다이제스트**: [https://2shin0.github.io/arxiv-ai-mailing/LLM/](https://2shin0.github.io/arxiv-ai-mailing/LLM/)
- **전체 AI 논문 다이제스트**: [https://2shin0.github.io/arxiv-ai-mailing/ALL/](https://2shin0.github.io/arxiv-ai-mailing/ALL/)

### 📧 연락처
- **개발자**: 2shin0
- **이슈 제보 및 기능 제안**: 02.shin.00@gmail.com

---

⭐ **이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!**

📧 **매일 최신 AI 논문을 받아보고 싶으시다면 [구독 신청하기!](https://script.google.com/macros/s/AKfycbzcG6pdTr1J-Gxn5tgAyfGsNQz_2-Xhm6EtSmGm9bYHEWgAw6yN7Ew89U92sQeXKaaI/exec)**

---

# 📰 arXiv AI Mailing (English)

**arXiv AI Mailing** is an automated system that crawls the latest AI papers from arXiv, summarizes and translates them, and sends them via email. It helps you stay updated with the latest AI research trends every day.

🌐 **Website**: [https://2shin0.github.io/arxiv-ai-mailing/](https://2shin0.github.io/arxiv-ai-mailing/)

## 🎯 Project Overview

This project helps users quickly understand the key points of AI and LLM papers updated on arXiv and explore papers of interest in depth.

### Key Solutions
- Daily automatic execution via GitHub Actions
- Automatic crawling of the latest papers
- AI-powered summarization and Korean translation
- Convenient email delivery
- Web archive through GitHub Pages

## 🤖 Automation System

### ⏰ Automatic Execution Schedule
- **Daily 10:00 AM (KST)**: Primary execution
- **11:00 AM (KST)**: Retry (if failed)
- **12:00 PM (KST)**: Final retry (if failed)
- **Weekends**: Automatically skipped (no arXiv updates)

### Smart Retry Logic
- Automatically skip remaining time slots on success
- Duplicate processing prevention
- Automatic execution status and error logging

### 📊 Monitoring Features
- Check execution results in GitHub Actions Summary
- Display processed paper count, success/failure status
- Automatic log storage (7-day retention)

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
# DeepL API Key (for translation)
DEEPL_API_KEY=your_deepl_api_key_here

# Gmail Settings (for email sending)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Google Sheets API (for subscriber list management)
GOOGLE_SHEET_NAME=your_google_sheet_name
GOOGLE_WORKSHEET_NAME=your_worksheet_name
GOOGLE_API_CREDENTIALS_PATH=path/to/credentials.json
GOOGLE_SCRIPT_ID=your_google_script_id
```

### 4. GitHub Secrets Setup (For Automation)
For GitHub Actions automation, set up the following secrets in your repository:

1. Go to GitHub Repository → Settings → Secrets and variables → Actions
2. Add the following secrets:

```bash
# Required Secrets
DEEPL_API_KEY=your_deepl_api_key_here
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIPIENT=recipient@example.com

# Google Sheets Integration
GOOGLE_SHEET_NAME=your_google_sheet_name
GOOGLE_WORKSHEET_NAME=your_worksheet_name
GOOGLE_SCRIPT_ID=your_google_script_id
GOOGLE_API_CREDENTIALS={"type":"service_account",...}  # Full JSON content

# GitHub Actions (Optional)
PERSONAL_ACCESS_TOKEN=ghp_your_token_here  # For branch operations
```

**Important Notes:**
- `GOOGLE_API_CREDENTIALS`: Paste the entire JSON content of your service account credentials
- `EMAIL_PASSWORD`: Use Gmail App Password, not your regular password
- `PERSONAL_ACCESS_TOKEN`: Only needed if you encounter permission issues

## 🚀 Usage

### Automatic Execution (Recommended)
GitHub Actions runs automatically every day. No additional work required!

### Manual Execution (For Testing)
1. GitHub Repository → Actions → "Daily arXiv AI Papers Digest"
2. Click "Run workflow" button for immediate execution

### Local Execution (For Development)
```bash
# Install dependencies
pip install -r requirements.txt

# Basic execution
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
- **Complete Automation**: Daily automatic execution via GitHub Actions
- **Automatic Crawling**: Collect papers from arXiv cs.AI category
- **Smart Classification**: Automatically classify LLM and other AI papers
- **AI Summarization**: Generate summaries using google/pegasus-cnn_dailymail model
- **Korean Translation**: High-quality translation via DeepL API
- **Email Delivery**: Send beautiful HTML-formatted emails
- **Web Archive**: Paper digest website through GitHub Pages
- **Google Sheets Integration**: Manage subscriber lists
- **Retry Logic**: Automatic retry on failure (11 AM, 12 PM)
- **Monitoring**: Automatic execution status and error logging

## 📁 Project Structure

```
arxiv-ai-mailing/
├── .github/workflows/
│   └── daily-arxiv-digest.yml  # GitHub Actions workflow
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

## 📞 Contact / Links

### 🌐 Related Links
- **Website**: [https://2shin0.github.io/arxiv-ai-mailing/](https://2shin0.github.io/arxiv-ai-mailing/)
- **GitHub Repository**: [https://github.com/2shin0/arxiv-ai-mailing](https://github.com/2shin0/arxiv-ai-mailing)
- **LLM Paper Digest**: [https://2shin0.github.io/arxiv-ai-mailing/LLM/](https://2shin0.github.io/arxiv-ai-mailing/LLM/)
- **All AI Paper Digest**: [https://2shin0.github.io/arxiv-ai-mailing/ALL/](https://2shin0.github.io/arxiv-ai-mailing/ALL/)

### 📧 Contact
- **Developer**: 2shin0
- **Issues and Feature Requests**: 02.shin.00@gmail.com

---

⭐ **If this project was helpful, please give it a Star!**

📧 **Want to receive the latest AI papers daily? [Subscribe here!](https://script.google.com/macros/s/AKfycbzcG6pdTr1J-Gxn5tgAyfGsNQz_2-Xhm6EtSmGm9bYHEWgAw6yN7Ew89U92sQeXKaaI/exec)**
