import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

# ✅ BBC: 원래 코드 유지
def fetch_top_3_bbc_korea_headlines():
    url = "https://www.bbc.com/korean"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch BBC Korea page")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # BBC 뉴스 기사 리스트 (li 단위)
    items = soup.select("li.bbc-19fk8fk")
    if not items:
        print("BBC 뉴스 항목을 찾을 수 없습니다.")
        return []

    articles = []
    for item in items:
        link_tag = item.select_one("h3 a")
        if not link_tag:
            continue

        title = link_tag.get_text(strip=True)
        link = link_tag.get("href")
        if not link.startswith("http"):
            link = "https://www.bbc.com" + link

        # 썸네일: img 태그 직접 접근
        img_tag = item.select_one("picture img")
        thumbnail = img_tag.get("src") if img_tag else None

        articles.append({
            "title": title,
            "link": link,
            "thumbnail": thumbnail
        })

        if len(articles) >= 3:
            break

    return articles



# ✅ 연합뉴스: <div class="top-news-list"> > <div> > <a> + <img>
def fetch_top_3_yna_headlines():
    url = "https://www.yna.co.kr/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch YNA page")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    articles_raw = soup.select("div.item-box02")
    if not articles_raw:
        print("YNA 뉴스 블록을 찾을 수 없습니다.")
        return []

    articles = []
    for block in articles_raw:
        title_tag = block.select_one("span.title01")
        link_tag = block.select_one("a.tit-news")
        img_tag = block.select_one("img")

        if not (title_tag and link_tag and img_tag):
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag["href"]
        if not link.startswith("http"):
            link = "https:" + link
        thumbnail = img_tag.get("src")

        articles.append({
            "title": title,
            "link": link,
            "thumbnail": thumbnail
        })

        if len(articles) >= 5:  # 여유 있게 확보
            break

    return articles


# ✅ 한겨레: <article class="MainTopArticle_card__ftSeV"> 내부에 제목/링크/이미지 분리
def fetch_top_3_hani_headlines():
    url = "https://www.hani.co.kr/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch Hani page")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    articles_raw = soup.select("article.MainTopArticle_card__ftSeV")

    if not articles_raw:
        print("Hani 뉴스 블록을 찾을 수 없습니다.")
        return []

    articles = []
    for card in articles_raw:
        link_tag = card.select_one("a.MainTopArticle_link__qambB")
        title_tag = card.select_one("strong.MainTopArticle_title__4v5vz")
        if not link_tag or not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag["href"]
        if not link.startswith("http"):
            link = "https://www.hani.co.kr" + link

        img_tag = card.select_one("img")
        thumbnail = img_tag["src"] if img_tag else None

        articles.append({
            "title": title,
            "link": link,
            "thumbnail": thumbnail
        })

        if len(articles) >= 3:
            break

    return articles


# ✅ 통합 함수
def fetch_top_3_articles_combined():
    bbc_articles = fetch_top_3_bbc_korea_headlines()[:1]
    for article in bbc_articles:
        article["source"] = "BBC"

    hani_articles = fetch_top_3_hani_headlines()[:1]
    for article in hani_articles:
        article["source"] = "한겨레"
    hani_titles = {a["title"] for a in hani_articles}

    yna_candidates = fetch_top_3_yna_headlines()
    yna_article = next((a for a in yna_candidates if a["title"] not in hani_titles), None)
    if yna_article:
        yna_article["source"] = "연합뉴스"

    result = bbc_articles
    if yna_article:
        result.append(yna_article)
    else:
        print("⚠ 연합뉴스 뉴스가 한겨레와 중복되어 제외되었습니다.")

    result += hani_articles
    return result
