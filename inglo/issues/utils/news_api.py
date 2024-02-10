# news api 호출, news들이 담긴 딕셔너리 배열 리턴
from django.utils import timezone
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

def fetch_news(keyword, today):
    """
    뉴스 API를 호출하여 키워드에 해당하는 뉴스 데이터를 가져옴
    """
    load_dotenv()
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    BASE_URL = os.getenv('BASE_URL')
    # 오늘로부터 일주일 전 날짜를 구함
    from7days = today - timedelta(days=7)

    params = {
        'q': keyword,
        'language': 'en',  # 영어 기사만 포함
        'sortBy': 'relevance',  # 관련성 순 정렬
        'from': from7days,  # 오늘 날짜부터 가져옴
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    else:
        print('Failed to fetch news')