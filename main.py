import schedule
import time
import os

# 시크릿에서 가져온 환경변수들
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
password = os.getenv("PASSWORD")

from news_crawler import fetch_top_3_articles_combined as fetch_top_3_bbc_korea_headlines
from email_notifier import send_email_notification

def display_top_3_articles():
    articles = fetch_top_3_bbc_korea_headlines()
    if not articles:
        print("오늘의 뉴스 기사를 불러오지 못했습니다.")
        return

    print("오늘의 화제 뉴스 상위 3개:")
    for article in articles:
        print(f"제목: {article['title']}")
        print(f"링크: {article['link']}")
        print(f"썸네일: {article['thumbnail']}\n")

def test_email_notification(user_email):
    send_email_notification(user_email)

def schedule_tasks(user_email):
    schedule.every().day.at("08:00").do(display_top_3_articles)
    schedule.every().day.at("20:00").do(test_email_notification, user_email=user_email)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    user_email = os.getenv("RECEIVER_EMAIL")  # ✅ 수정됨!
    if not user_email:
        user_email = input("이메일 주소를 입력하세요: ")
    display_top_3_articles()
    test_email_notification(user_email)
