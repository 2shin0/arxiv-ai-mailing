#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template_string, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEET_NAME, GOOGLE_WORKSHEET_NAME, GOOGLE_API_CREDENTIALS_PATH
import hashlib
import hmac
import base64
from urllib.parse import unquote

app = Flask(__name__)

# 보안을 위한 시크릿 키 (실제 운영시에는 환경변수로 관리)
SECRET_KEY = "your-secret-key-here"

def generate_unsubscribe_token(email):
    """이메일 주소로부터 구독 해지 토큰을 생성합니다."""
    message = email.encode('utf-8')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), message, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    return token

def verify_unsubscribe_token(email, token):
    """구독 해지 토큰이 유효한지 확인합니다."""
    expected_token = generate_unsubscribe_token(email)
    return hmac.compare_digest(token, expected_token)

def remove_email_from_sheet(email):
    """구글 시트에서 이메일 주소를 삭제합니다."""
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        creds = Credentials.from_service_account_file(GOOGLE_API_CREDENTIALS_PATH, scopes=scopes)
        client = gspread.authorize(creds)

        sheet = client.open(GOOGLE_SHEET_NAME).worksheet(GOOGLE_WORKSHEET_NAME)
        
        # 이메일 주소 찾기
        try:
            cell = sheet.find(email)
            if cell:
                # 해당 행 삭제
                sheet.delete_rows(cell.row)
                return True, "구독이 성공적으로 해지되었습니다."
            else:
                return False, "해당 이메일 주소를 찾을 수 없습니다."
        except gspread.exceptions.CellNotFound:
            return False, "해당 이메일 주소를 찾을 수 없습니다."
            
    except Exception as e:
        return False, f"오류가 발생했습니다: {str(e)}"

@app.route('/unsubscribe')
def unsubscribe():
    """구독 해지 페이지"""
    email = request.args.get('email', '')
    token = request.args.get('token', '')
    
    if not email or not token:
        return render_template_string(ERROR_TEMPLATE, 
                                    message="잘못된 구독 해지 링크입니다.")
    
    # URL 디코딩
    email = unquote(email)
    
    # 토큰 검증
    if not verify_unsubscribe_token(email, token):
        return render_template_string(ERROR_TEMPLATE, 
                                    message="유효하지 않은 구독 해지 링크입니다.")
    
    return render_template_string(UNSUBSCRIBE_TEMPLATE, email=email, token=token)

@app.route('/unsubscribe/confirm', methods=['POST'])
def unsubscribe_confirm():
    """구독 해지 처리"""
    email = request.form.get('email', '')
    token = request.form.get('token', '')
    
    if not email or not token:
        return render_template_string(ERROR_TEMPLATE, 
                                    message="잘못된 요청입니다.")
    
    # 토큰 재검증
    if not verify_unsubscribe_token(email, token):
        return render_template_string(ERROR_TEMPLATE, 
                                    message="유효하지 않은 요청입니다.")
    
    # 이메일 삭제 처리
    success, message = remove_email_from_sheet(email)
    
    if success:
        return render_template_string(SUCCESS_TEMPLATE, message=message)
    else:
        return render_template_string(ERROR_TEMPLATE, message=message)

# HTML 템플릿들
UNSUBSCRIBE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>구독 해지 - arXiv AI Digest</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .container { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .email { background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 20px 0; }
        .buttons { text-align: center; margin-top: 30px; }
        .btn { padding: 12px 24px; margin: 0 10px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-secondary { background: #6c757d; color: white; }
        .btn:hover { opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔔 구독 해지</h2>
            <p>arXiv AI Digest 구독을 해지하시겠습니까?</p>
        </div>
        
        <div class="email">
            <strong>이메일:</strong> {{ email }}
        </div>
        
        <p>구독을 해지하시면 더 이상 AI 논문 요약 이메일을 받지 않으실 수 있습니다.</p>
        
        <form method="POST" action="/unsubscribe/confirm">
            <input type="hidden" name="email" value="{{ email }}">
            <input type="hidden" name="token" value="{{ token }}">
            <div class="buttons">
                <button type="submit" class="btn btn-danger">구독 해지</button>
                <button type="button" class="btn btn-secondary" onclick="window.close()">취소</button>
            </div>
        </form>
    </div>
</body>
</html>
'''

SUCCESS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>구독 해지 완료 - arXiv AI Digest</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .container { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        .success { color: #28a745; font-size: 48px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="success">✅</div>
        <h2>구독 해지 완료</h2>
        <p>{{ message }}</p>
        <p>그동안 arXiv AI Digest를 이용해주셔서 감사합니다.</p>
    </div>
</body>
</html>
'''

ERROR_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>오류 - arXiv AI Digest</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .container { background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        .error { color: #dc3545; font-size: 48px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="error">❌</div>
        <h2>오류 발생</h2>
        <p>{{ message }}</p>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
