import csv

import requests
from bs4 import BeautifulSoup

from review import Review


class Scraper:

    def __init__(self) -> None:
        self._reviews = []

    def get_review(self, _url: str) -> None:

        response = requests.get(_url)

        soup = BeautifulSoup(
            response.content,
            "html.parser",
        )

        reviews = soup.find("ul", class_="lst_view _fe_view_infinite_scroll_append_target").find_all("li",
                                                                                                     class_="bx _slog_visible")

        for review in reviews[:10]:
            title = review.find("div", class_="title_area").text
            link = review.find("div", class_="title_area").find("a")["href"]
            description = review.find("div", class_="dsc_area").text
            main = self._get_review_main(link)
            review_class_ = Review(title=title, link=link, description=description, main=main)
            self._reviews.append(review_class_)

    def view_reviews(self) -> None:
        for review in self._reviews:
            print(review)

    @staticmethod
    def _get_review_main(link: str) -> str:
        """
        일단 review를 scrape해오고 각 링크에 들어가 main를 하나씩 가져온다.
        :param link: Review 블로그 main contents
        """
        response = requests.get(link)

        soup = BeautifulSoup(
            response.content,
            "html.parser",
        )

        return soup.find("div", class_="se-main-container").text

    def get_csv_file(self) -> None:
        with open("review.csv","w") as file:
            writer = csv.writer(file)
            writer.writerow(
            [
                "Title",
                "Link",
                "Description",
                "Main",
            ]
            )
            for review in self._reviews:
                writer.writerow(review.get_review_dict().values())