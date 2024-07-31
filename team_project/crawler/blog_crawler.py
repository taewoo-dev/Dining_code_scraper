from database.diningcode_db import excute_query
from config import CONNECTION

import requests
from bs4 import BeautifulSoup


class BlogCrawler:

    def __init__(self):
        pass

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

            try:
                response = requests.get(review_link)

                soup_sub = BeautifulSoup(
                    response.content,
                    "html.parser",
                )
                iframe_tag = soup_sub.find('iframe')["src"]
                url = f"https://blog.naver.com{iframe_tag}"

                response2 = requests.get(url)

                soup_main = BeautifulSoup(
                    response2.content,
                    "html.parser"
                )

                blog = soup_main.find("div", class_="se-main-container").text.replace("\n", "")
                print(blog)

                sql = """
                        insert into blogs (review_ID, blog_text)
                        values (%s, %s)
                        """
                excute_query(CONNECTION, sql, review_id, blog)
                self.set_blog_crawling_check(review_id=review_id)

            except:
                sql = """
                                        insert into blogs (review_ID, blog_text)
                                        values (%s, %s)
                                        """
                excute_query(CONNECTION, sql, review_id, "카페")
                self.set_blog_crawling_check(review_id=review_id)

    @staticmethod
    def set_blog_crawling_check(review_id) -> None:
        sql = """
                update reviews
                set blog_crawling_check = 1
                where review_ID = (%s);
                """
        excute_query(CONNECTION, sql, review_id)
        pass
