import smtplib
import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, GOOGLE_SHEET_NAME, GOOGLE_WORKSHEET_NAME, GOOGLE_API_CREDENTIALS_PATH

# 오프라인 모드 설정
OFFLINE_MODE = os.environ.get('OFFLINE_MODE', 'False').lower() in ('true', '1', 't')
if '--offline' in sys.argv:
    OFFLINE_MODE = True

def get_recipients_from_sheet():
    """Google Sheets에서 수신자 이메일 목록을 가져옵니다."""
    try:
        # 권한 범위 확장 - 읽기 전용과 드라이브 권한 추가
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        creds = Credentials.from_service_account_file(GOOGLE_API_CREDENTIALS_PATH, scopes=scopes)
        client = gspread.authorize(creds)

        sheet = client.open(GOOGLE_SHEET_NAME).worksheet(GOOGLE_WORKSHEET_NAME)
        # 첫 번째 열(A열)의 모든 값을 가져옵니다.
        recipients = sheet.col_values(1)
        # 헤더(첫 번째 행)가 있다면 제외합니다.
        if recipients and '@' not in recipients[0]:
            return recipients[1:]
        return recipients
    except FileNotFoundError:
        print(f"\n[오류] Google API 인증 파일을 찾을 수 없습니다: {GOOGLE_API_CREDENTIALS_PATH}")
        return []
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"\n[오류] 스프레드시트를 찾을 수 없습니다: {GOOGLE_SHEET_NAME}")
        return []
    except Exception as e:
        print(f"\n[오류] Google Sheets에서 데이터를 가져오는 중 오류 발생: {e}")
        return []

def send_email(subject, body):
    # 오프라인 모드: 이메일 출력만
    if OFFLINE_MODE:
        print("\n[오프라인 모드] 이메일 전송을 건너뜁니다.")
        print(f"제목: {subject}")
        print("내용 미리보기:")
        print(body[:200] + "..." if len(body) > 200 else body)
        return True

    # 이메일 설정 확인
    if not all([EMAIL_ADDRESS, EMAIL_PASSWORD]):
        print("\n[오류] 이메일 설정이 완료되지 않았습니다. .env 파일을 확인하세요.")
        return False

    # Google Sheets에서 수신자 목록 가져오기
    recipients = get_recipients_from_sheet()
    if not recipients:
        print("\n[정보] 전송할 수신자가 없습니다. Google Sheets 설정을 확인하세요.")
        return False

    print(f"\n총 {len(recipients)}명에게 이메일을 전송합니다...")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            for recipient in recipients:
                if not recipient.strip():
                    continue

                msg = MIMEMultipart("alternative")
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = recipient
                msg['Subject'] = subject

                # HTML 본문 생성
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
                msg.attach(html_part)

                smtp.send_message(msg)
                print(f"  - {recipient} 에게 전송 완료")

        print("\n[성공] 모든 이메일이 성공적으로 전송되었습니다.")
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
    send_email("테스트 메일", "안녕하세요,\n\n이것은 구글 시트와 연동하여 보내는 테스트 메일입니다.\n\n감사합니다.")
