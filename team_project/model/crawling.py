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

    def __init__(self) -> object:
        self._review_links = []

    def get_reviews(self):
        ChromeDriverManager().install()
        browser = webdriver.Chrome()
        url = "https://map.naver.com/p?c=15.00,0,0,0,dh"
        browser.get(url)

        for restaurant in RESTAURANTS:
            try:
                print(f"{restaurant} 블로그 링크 수집중")
                search_element = browser.find_element(By.CLASS_NAME, "input_search")
                search_element.send_keys(f"{restaurant}")
                search_element.send_keys(Keys.ENTER)
                search_element.send_keys(Keys.COMMAND + "a")
                time.sleep(1.5)
                search_element.send_keys(Keys.BACK_SPACE)

                # 리뷰가 담긴 프레임으로 이동
                browser.switch_to.frame(browser.find_element(By.ID, 'entryIframe'))

                reviews_btn = browser.find_elements(By.CLASS_NAME, "veBoZ")
                for review_btn in reviews_btn:
                    if review_btn.text == "리뷰":
                        review_btn.click()
                        break
                # 메인프레임으로 이동
                browser.switch_to.default_content()

                # 블로그 리뷰 프레임으로 이동
                browser.switch_to.frame(browser.find_element(By.ID, 'entryIframe'))
                browser.find_elements(By.CLASS_NAME, "YsfhA")[1].click()  # 블로그 리뷰 버튼 클릭
                time.sleep(1.5)

                # 여기부터 리뷰 크롤링하기
                reviews = browser.find_elements(By.CLASS_NAME, "xg2_q")

                self.set_restaurant_table(restaurant)

                for review in reviews:
                    review_title = review.find_element(By.CLASS_NAME, "s2opK").text
                    review_link = review.find_element(By.CLASS_NAME, "uUMhQ").get_attribute("href")
                    review_description = review.find_element(By.CLASS_NAME, "j0LvW").text

                    self.get_review_db(name=restaurant, title=review_title, link=review_link, description=review_description)
                    self._review_links.append(review_link)

                self.set_crawling_check(restaurant)
                # 메인프레임으로 이동
                browser.switch_to.default_content()

                # 다음 리뷰 검색을 위해서 검색창 비우기
            except:
                self.set_restaurant_table(restaurant)
                self.get_review_db(name=restaurant, title="x", link="x",
                                   description="분점 or 망함")
                continue

        print("블로그 링크 수집 완료")

    @staticmethod
    def set_restaurant_table(restaurant: str) -> None:
        sql_restaurants_table = """
                               insert into restaurants (restaurant_name)
                               values (%s)
                               """
        excute_query(CONNECTION, sql_restaurants_table, restaurant)

    @staticmethod
    def get_review_db(name: str, title: str, link: str, description: str) -> None:

        sql= """
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
    def set_crawling_check(restaurant):
        sql = """
        update restaurants
        set restaurant_review_get_check = 1
        where restaurant_name = (%s);
        """
        excute_query(CONNECTION, sql, restaurant)

    def get_blogs(self):
        print("블로그 내용 수집 시작")
        ChromeDriverManager().install()
        browser = webdriver.Chrome()

        print(self._review_links)
        for link in self._review_links:
            browser.get(link)
            browser.switch_to.frame(browser.find_element(By.ID, 'mainFrame'))
            blog = browser.find_element(By.CLASS_NAME, "se-main-container").text
            print(blog)

    # (2). 모은 블로그 리스트를 순회하며 블로그 main 내용 수집

# (3). 분점 and 폐점 식당 처리

# (4). 데이터베이스의 셋팅 테이블에 수집 유무를 체크

# (5). 데이터 베이스에 없는 식당을 추가로 획득

# (6). 비동기 방식으로 병렬 크롤링

app = Crawling()
app.get_reviews()
app.get_blogs()

