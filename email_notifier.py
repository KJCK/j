import smtplib  # 이걸 꼭 추가해야 합니다
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from news_crawler import fetch_top_3_articles_combined


def send_email_notification(user_email):
    articles = fetch_top_3_articles_combined()
    if not articles:
        print("뉴스를 가져오지 못했습니다.")
        return

    msg = MIMEMultipart()
    msg["Subject"] = "오늘의 추천 뉴스"
    msg["From"] = "jseo1564@gmail.com"
    msg["To"] = user_email

    html_content = """
    <html>
    <body style="font-family:Arial, sans-serif; line-height:1.6;">
        <h1 style="color:#333;">오늘의 추천 뉴스</h1>
    """

    for idx, article in enumerate(articles, start=1):
        html_content += f"""
        <div style="
          border: 1px solid #ddd; 
          border-radius: 10px; 
          padding: 15px; 
          margin-bottom: 20px; 
          box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
          background-color: #f9f9f9;
        ">
            <h2 style="color:#444;">{idx}. {article['title']}</h2>
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
            server.login("jseo1564@gmail.com", "yvwgtpvimaxblpyo")  # 본인 정보로 바꾸세요
            server.sendmail("jseo1564@gmail.com", user_email, msg.as_string())
            print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print("이메일 전송 실패:", e)
