import os
import webbrowser
from datetime import datetime
from main import make_digest

def preview_email(subject, body_html):
    """이메일 미리보기용 HTML 파일을 생성합니다."""
    full_html = f"""
    <html>
      <head>
        <meta charset="UTF-8">
      </head>
      <body style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f4f4f4; padding: 30px; margin: 0;">
        <div style="max-width: 600px; margin: auto; background-color: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
          <h2 style="color: #333333; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">{subject}</h2>
          <div style="font-size: 14px; color: #888888; margin-bottom: 20px;">
            📌 본 Digest는 한국 시간 기준 <strong>오늘 오전 9시 arXiv에 발표된 AI 논문</strong>을 요약한 것입니다.
          </div>
          <div style="color: #555555; line-height: 1.6; font-size: 16px;">
            {body_html}
          </div>
          <div style="margin-top: 30px; font-size: 12px; color: #999999; border-top: 1px solid #e0e0e0; padding-top: 20px;">
            이 메일은 시스템에서 자동 발송되었습니다.<br>
            문의: <a href="mailto:02.shin.00@gmail.com" style="color: #999999;">02.shin.00@gmail.com</a>
          </div>
        </div>
      </body>
    </html>
    """
    preview_path = "email_preview.html"
    with open(preview_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"이메일 미리보기를 '{preview_path}'로 저장했습니다.")
    try:
        webbrowser.open(f"file://{os.path.abspath(preview_path)}")
    except Exception as e:
        print(f"브라우저 열기에 실패했습니다: {e}")

if __name__ == "__main__":
    # --- 미리보기를 위한 가상 데이터 --- #
    mock_llm_paper = {
        'title': 'Awesome LLM Paper Title',
        'authors': 'John Doe, Jane Smith',
        'url': 'http://arxiv.org/abs/2301.00001',
        'summary_en': 'This is an English summary of the awesome LLM paper.',
        'summary_ko': '이것은 멋진 LLM 논문의 한글 요약입니다.',
    }
    mock_other_paper = {
        'title': 'Interesting AI Paper Title',
        'authors': 'Peter Jones',
        'url': 'http://arxiv.org/abs/2301.00002',
        'summary_en': 'This is an English summary of another interesting AI paper.',
        'summary_ko': '이것은 또 다른 흥미로운 AI 논문의 한글 요약입니다.',
    }
    mock_papers = [mock_llm_paper, mock_other_paper]
    mock_llm_papers = [mock_llm_paper]
    # --- --- #

    today_str = datetime.today().strftime('%Y-%m-%d')
    subject = f"[미리보기] arXiv AI Digest - {today_str}"
    
    # main.py의 make_digest 함수를 사용하여 이메일 본문 생성
    email_body = make_digest(mock_papers, mock_llm_papers)
    
    # 미리보기 생성
    preview_email(subject, email_body)
