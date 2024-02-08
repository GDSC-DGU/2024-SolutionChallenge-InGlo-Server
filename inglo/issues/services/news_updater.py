from issues.utils.news_api import fetch_news
from issues.utils.classifier import classify_news

def update_issues_from_news():
    # news api 호출하여 뉴스데이터 얻어옴
    news_items = fetch_news()
    news_properties = [] # 뉴스 api를 사용해서 가져온 뉴스 데이터들 각각을 {link, writer, title, content, created_at, image_url, description, country, sdgs } 형태로 저장할 배열 

    # 각 뉴스 아이템을 지정된 속성에 맞게 변환
    for news_item in news_items:
        # 분류 모델이 (제목, 내용)을 가지고 '어떤 국가와 관련된 기사'인지, '어떤 SDGs와 관련된 기사'인지 분류한다고 가정.
        country, sdgs = classify_news(news_item.get('title', ''), news_item.get('content', ''))

        # country와 sdgs가 숫자가 아니거나, 범위를 벗어나면 다음 뉴스로 넘어감. 국가는 총 10개가 있다고 가정.
        if(not country.isdigit() or not sdgs.isdigit() or not (1 <= int(country) <= 10) or not (1<= int(sdgs) <= 17)):
            continue

        processed_item = {
            "link": news_item.get('url', ''),
            "writer": news_item.get('author', ''),
            "title": news_item.get('title', ''),
            "content": news_item.get('content', ''),
            "created_at": news_item.get('publishedAt', ''),
            "image_url": news_item.get('urlToImage', ''),
            "description": news_item.get('description', ''),
            "country": country,
            "sdgs": sdgs,
        }
        news_properties.append(processed_item)
    
    return news_properties