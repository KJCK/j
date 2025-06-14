import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from news_crawler import fetch_top_3_articles_combined

def send_email_notification(user_email):
    articles = fetch_top_3_articles_combined()
    if not articles:
        print("뉴스를 가져오지 못했습니다.")
        return

    # ⛳️ 환경 변수에서 가져오기
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("PASSWORD")

    msg = MIMEMultipart()
    msg["Subject"] = "오늘의 주요 뉴스"
    msg["From"] = sender_email
    msg["To"] = user_email

    html_content = """
    <html>
    <body style="font-family:Arial, sans-serif; line-height:1.6;">
        <h1 style="color:#333;">오늘의 주요 뉴스</h1>
    """

    for idx, article in enumerate(articles, start=1):
        source = article.get("source", "뉴스")
        html_content += f"""
        <div style="
          border: 1px solid #ddd; 
          border-radius: 10px; 
          padding: 15px; 
          margin-bottom: 20px; 
          box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
          background-color: #f9f9f9;
        ">
            <h2 style="color:#444;">{idx}. [{source}] {article['title']}</h2>
            <a href="{article['link']}" style="font-size:16px; font-weight:bold; text-decoration:none; color:#3366cc;">기사 보러가기</a><br>
            <img src="{article['thumbnail']}" alt="썸네일" style="width:100%; max-width:400px; border-radius: 8px; margin-top: 10px;">
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())
            print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print("이메일 전송 실패:", e)
