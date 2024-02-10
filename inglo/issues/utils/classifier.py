# (제목,내용)을 바탕으로 (국가,SDGs)를 분류하는 분류모델

def classify_news(title, content):
    """
    뉴스 기사의 제목과 내용을 바탕으로
    국가와 SDGs를 분류하는 모델
    """
    # 분류 모델이 (제목, 내용)을 가지고 '어떤 국가와 관련된 기사'인지, '어떤 SDGs와 관련된 기사'인지 분류한다고 가정.
    country = '1'  # 국가는 1번으로 가정
    sdgs = '1'  # SDGs는 1번으로 가정
    return country, sdgs