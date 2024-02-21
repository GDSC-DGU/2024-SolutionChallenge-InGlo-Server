import requests
import os
from dotenv import load_dotenv

def fetch_news(keyword):
    """
    뉴스 API를 호출하여 키워드에 해당하는 뉴스 데이터를 가져옴
    """
    load_dotenv()
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    BASE_URL = os.getenv('BASE_URL')

    params = {
        'q': keyword,
        'apikey': NEWS_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        return results
    else:
        print('Failed to fetch news')