def preview_email_html(subject, body, output_path="preview_email.html"):
    body_html = body.replace('\n', '<br>')  # 먼저 처리

    html_body = f"""
    <html>
      <head>
        <meta charset="UTF-8">
      </head>
      <body style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f8f9fa; padding: 40px 0; margin: 0;">
        <div style="max-width: 640px; margin: auto; background-color: #ffffff; border-radius: 12px; padding: 40px 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
          <h1 style="color: #222222; font-size: 24px; margin-bottom: 20px;">주제입니다.</h1>
          <div style="color: #444444; font-size: 16px; line-height: 1.7; white-space: pre-wrap;">
            이메일 내용입니다.
          </div>
          <hr style="margin: 40px 0; border: none; border-top: 1px solid #e0e0e0;">
          <div style="font-size: 12px; color: #999999; text-align: center;">
            이 메일은 시스템에서 자동 발송되었습니다.<br>
            문의: <a href="mailto:02.shin.00@gmail.com" style="color: #999999;">02.shin.00@gmail.com</a>
          </div>
        </div>
      </body>
    </html>
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_body)
    print(f"[미리보기 생성 완료] '{output_path}' 파일을 브라우저에서 열어보세요.")

if __name__ == "__main__":
    preview_email_html(
        subject="모던 이메일 디자인 테스트",
        body="안녕하세요,\n\n이것은 미리보기용 HTML 이메일 디자인입니다.\n이메일을 보내지 않고도 이렇게 확인할 수 있어요!\n\n감사합니다."
    )