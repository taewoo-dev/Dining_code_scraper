from config import RESTAURANTS
from database.diningcode_db import excute_query
from config import CONNECTION

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
import time
from datetime import datetime


# (1). RESTAURANTS 리스트를 한번씩 돌면서 식당 이름, 리뷰 제목, 리뷰 링크, 리뷰 요약 수집 (데이터베이스에 바로 연동)
class Crawling:
    """
    다이닝 코드 크롤링 클래스
    1) 리뷰를 크롤링하여 데이터베이스에 저장하는 매서드
    2) 각 식당별 리뷰의 블로그 내용을 크롤링하여 데이터베이스에 저장하는 매서드
    """

    def __init__(self) -> object:
        self._review_links = [] # 필요할까? -> 데이터베이스에서 블로그 크롤링 시 링크만 모두 담아오기
        self._browser: object

        ChromeDriverManager().install()
        self._browser = webdriver.Chrome()

    def get_reviews(self) -> None:
        """
        검색어를 하나씩 입력하고 순회하며 리뷰를 크롤링하는 매서드
        :return: None
        """

        url = "https://map.naver.com/p?c=15.00,0,0,0,dh"
        self._browser.get(url)

        for restaurant in RESTAURANTS:
            # 네이버 플레이스 검색 창에 식당명 입력

            print(f"{restaurant} 블로그 링크 수집중")
            search_element = self._browser.find_element(By.CLASS_NAME, "input_search")
            search_element.send_keys(f"{restaurant}")
            search_element.send_keys(Keys.ENTER)
            time.sleep(2)

            # 크롤링 경우의 수를 검사하는 매서드
            condition = self.check_review_condition()
            try:
                if condition == 1:
                    # 1-1) searchIframe에 검색 식당이 1개인 경우
                    self._browser.switch_to.default_content()
                    self.process_review(restaurant=restaurant)

                elif condition == 2:
                    # 1-2) searchIframe이 검색 식당이 여러 개인 경우
                    first_result = self._browser.find_element(By.CLASS_NAME, "place_bluelink")
                    first_result.click()
                    time.sleep(2) # 클릭 후 반응까지 2초 대기

                    self._browser.switch_to.default_content()
                    self.process_review(restaurant=restaurant) # 키워드 인자
            except:
                # 1-3) 망해서 사라진 가게
                self._browser.switch_to.default_content()
                self.set_restaurant_table(restaurant)
                self.get_review_db(name=restaurant, title="x", link="x",
                                   description="망함")
            # 다음 검색어를 입력하기 위해서 검색창 비우기
            search_element.send_keys(Keys.COMMAND + "a")
            time.sleep(1.5) # (커맨드 + 'a') 키를 누르고 반응까지 1.5초 대기
            search_element.send_keys(Keys.BACK_SPACE)

        print("블로그 링크 수집 완료")

    def process_review(self, restaurant: str) -> None:
        """
        블로그 리뷰 크롤링의 메인 part 매서드
        :param restaurant: 검색 식당
        :return: None
        """
        # 리뷰가 담긴 프레임으로 이동
        self._browser.switch_to.frame(self._browser.find_element(By.ID, 'entryIframe'))

        reviews_btn = self._browser.find_elements(By.CLASS_NAME, "veBoZ")
        for review_btn in reviews_btn:
            if review_btn.text == "리뷰":
                review_btn.click()
                break
        # 메인 프레임으로 이동
        self._browser.switch_to.default_content()

        # 블로그 리뷰 프레임으로 이동
        self._browser.switch_to.frame(self._browser.find_element(By.ID, 'entryIframe'))
        self._browser.find_elements(By.CLASS_NAME, "YsfhA")[1].click()  # 블로그 리뷰 버튼 클릭
        time.sleep(2) # 클릭 후 반응이 나오기까지의 대기시간

        # 여기부터 리뷰 크롤링
        reviews = self._browser.find_elements(By.CLASS_NAME, "xg2_q")

        self.set_restaurant_table(restaurant)

        for review in reviews:
            review_title = review.find_element(By.CLASS_NAME, "s2opK").text
            review_link = review.find_element(By.CLASS_NAME, "uUMhQ").get_attribute("href")
            review_description = review.find_element(By.CLASS_NAME, "j0LvW").text

            self.get_review_db(name=restaurant, title=review_title, link=review_link,
                               description=review_description)

        self.set_crawling_check(restaurant)
        # 메인 프레임으로 이동
        self._browser.switch_to.default_content()

    def check_review_condition(self) -> int:
        """
        검색 식당의 갯수에 따른 옵션을 정해주는 매서드
        1) 검색 시 식당이 1곳일 경우 1 반환
        2) 검색 시 식당이 여러 곳일 경우 2 반환
        :return:  크롤링 옵션 1 or 2
        """

        self._browser.switch_to.frame(self._browser.find_element(By.ID, 'searchIframe'))
        restaurant_count = len(self._browser.find_elements(By.CLASS_NAME, "VLTHu"))

        if restaurant_count == 1:
            print("식당 바로 찾음")
            return 1
        else:
            print("식당 분점 존재")
            return 2

    @staticmethod
    def set_restaurant_table(restaurant: str) -> None:
        """
        restaurant 테이블에 크롤링 하는 식당 이름을 생성 매서드
        :param restaurant: 식당명
        :return: None
        """
        sql_restaurants_table = """
                               insert into restaurants (restaurant_name)
                               values (%s)
                               """
        excute_query(CONNECTION, sql_restaurants_table, restaurant)

    @staticmethod
    def get_review_db(name: str, title: str, link: str, description: str) -> None:
        """
        restaurant 테이블의 크롤링 하는 식당 레코드(행)을 생성하는 매서드
        :param name:
        :param title:
        :param link:
        :param description:
        :return:
        """
        sql = """
        select restaurants.restaurant_ID from restaurants
        where restaurant_name = (%s) limit 1;
        """
        restaurants_id = excute_query(CONNECTION, sql, name)[0]["restaurant_ID"]

        sql = """
        insert into reviews (restaurant_ID, review_title, review_link, review_description)
        values (%s, %s, %s, %s)
        """
        excute_query(CONNECTION, sql, restaurants_id, title, link, description)

    @staticmethod
    def set_crawling_check(restaurant) -> None:
        """
        식당 하나의 리뷰 크롤링이 끝낫을 시 restaurant 테이블에 크롤링 완료 표시
        :param restaurant: 식당명
        :return: None
        """
        sql = """
        update restaurants
        set restaurant_review_get_check = 1
        where restaurant_name = (%s);
        """
        excute_query(CONNECTION, sql, restaurant)

    # (2). 모은 블로그 리스트를 순회하며 블로그 main 내용 수집 -> 이건 다른 클래스로 만들기
    def get_blogs(self) -> None:
        """
        리뷰 크롤링 과정에서 얻은 링크를 바탕으로 각각의 블로그에 접속하여 메인 text를 크롤링하는 매서드
        :return: None
        """
        print("블로그 내용 수집 시작")

        sql = """
            select review_ID, review_link from reviews;
        """

        reviews = excute_query(CONNECTION, sql)
        for review in reviews:
            review_id = review["review_ID"]
            review_link = review["review_link"]

            # 2-1) blog main -> beautifulsoup4로 훨씬 빠르게 -> 블로그 크롤링 class 만들기
            self._browser.get(review_link)
            self._browser.switch_to.frame(self._browser.find_element(By.ID, 'mainFrame'))
            blog = self._browser.find_element(By.CLASS_NAME, "se-main-container").text
            print(blog)

            sql = """
                    insert into blogs (review_ID, blog_text)
                    values (%s, %s)
                    """
            excute_query(CONNECTION, sql,review_id, blog)

            # 2-2) cafe main
    def set_blog_crawling_check(self) -> None:
        pass

# (3). 데이터베이스의 셋팅 테이블에 식당별 리뷰 크롤링 (ok), 블로그 크롤링 유무 체크 (x)

# (4). 크롤링 도중 멈췄을 시 멈춘 부분부터 다시 크롤링하는 기능 구현

# (5). 데이터 베이스에 없는 식당을 추가로 크롤링하는 기능 구현

# (6). 비동기 방식으로 병렬 크롤링 구현

# (7). 로그 남기는 기능
app = Crawling()
app.get_blogs()

