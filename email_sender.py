import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT

# 오프라인 모드 설정
OFFLINE_MODE = os.environ.get('OFFLINE_MODE', 'False').lower() in ('true', '1', 't')
if '--offline' in sys.argv:
    OFFLINE_MODE = True

def send_email(subject, body):
    # 오프라인 모드: 이메일 출력만
    if OFFLINE_MODE:
        print("\n[오프라인 모드] 이메일 전송을 건너뜁니다.")
        print(f"제목: {subject}")
        print("내용 미리보기:")
        print(body[:200] + "..." if len(body) > 200 else body)
        return True

    # 이메일 설정 확인
    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT]):
        print("\n[오류] 이메일 설정이 완료되지 않았습니다. .env 파일을 확인하세요.")
        return False

    msg = MIMEMultipart("alternative")
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT
    msg['Subject'] = subject

    # 일반 텍스트 버전
    text_part = MIMEText(body, 'plain')

    # HTML 버전 - 줄바꿈을 <br>로 변환
    body_html = body.replace('\n', '<br>')

    html_body = f"""
    <html>
      <head>
        <meta charset="UTF-8">
      </head>
      <body style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f4f4f4; padding: 30px; margin: 0;">
        <div style="max-width: 600px; margin: auto; background-color: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
          <h2 style="color: #333333; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">{subject}</h2>
          <p style="color: #555555; line-height: 1.6; font-size: 16px;">
            {body_html}
          </p>
          <div style="margin-top: 30px; font-size: 12px; color: #999999; border-top: 1px solid #e0e0e0; padding-top: 20px;">
            이 메일은 시스템에서 자동 발송되었습니다.<br>
            문의: <a href="mailto:02.shin.00@gmail.com" style="color: #999999;">02.shin.00@gmail.com</a>
          </div>
        </div>
      </body>
    </html>
    """
    html_part = MIMEText(html_body, 'html')

    # 이메일에 첨부
    msg.attach(text_part)
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("\n[성공] 이메일이 성공적으로 전송되었습니다.")
        return True
    except smtplib.SMTPAuthenticationError:
        print("\n[오류] 이메일 인증 실패. 계정 정보와 앱 비밀번호를 확인하세요.")
        return False
    except TimeoutError:
        print("\n[오류] 연결 시간 초과. 인터넷 연결을 확인하세요.")
        return False
    except Exception as e:
        print(f"\n[오류] 이메일 전송 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    send_email("테스트 메일", "안녕하세요,\n\n이것은 모던한 디자인을 적용한 테스트 메일입니다.\n\n감사합니다.")
