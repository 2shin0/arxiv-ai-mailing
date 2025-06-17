def preview_email_html(subject, body, output_path="preview_email.html"):
    body_html = body.replace('\n', '<br>')  # 먼저 처리

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
            문의: <a href="mailto:support@example.com" style="color: #999999;">support@example.com</a>
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