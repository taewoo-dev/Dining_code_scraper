import requests
from bs4 import BeautifulSoup


def get_naver_place_urls(search_query):
    # 네이버 플레이스 검색 URL
    search_url = f'https://m.place.naver.com/restaurant/list?query={search_query}'

    # 네이버 검색 페이지 요청
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(search_url, headers=headers)

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')

    # 식당 URL 추출
    restaurant_links = soup.find_all('a', class_='place_bluelink')
    restaurant_urls = ['https://m.place.naver.com' + link['href'] for link in restaurant_links]

    return restaurant_urls


# 검색할 키워드
search_query = '강남역 맛집'
restaurant_urls = get_naver_place_urls(search_query)

# 결과 출력
for url in restaurant_urls:
    print(url)
