import csv

import requests
from bs4 import BeautifulSoup

from review import Review
from url import Url

restaurants = [
    "명동교자",
    "옛날민속집 본점",
    "만족 오향족발",
    "쟈니덤플링",
    "미즈컨테이너",
    "마코토",
    "을밀대",
    "혜화돌쇠아저씨",
    "우래옥",
    "바토스",
    "오율",
    "마리쿡",
    "청솔나무",
    "지하손만두",
    "초마",
    "삼청동수제비",
    "토속촌 삼계탕",
    "대원갈비",
    "청담돈가",
    "윤씨밀방",
    "바바인디아",
    "육회자매집",
    "청진옥",
    "하카다분코",
    "모모코",
    "툭툭누들타이",
    "귀족족발",
    "테이스팅룸 이태원점",
    "이문설농탕",
    "리틀사이공",
    "활화산 조개구이 칼국수",
    "홍스쭈꾸미",
    "어부와백정 영등포 본점",
    "아이해브어드림",
    "필동면옥",
    "대장장이화덕피자",
    "부자피자",
    "미진",
    "단",
    "서부면옥",
    "고상",
    "역전회관",
    "마론키친앤바",
    "더함",
    "새벽집",
    "떼아떼베네",
    "소프트리",
    "스테파니카페 2호점",
    "알리고떼",
    "연남 서서갈비",
    "대게나라 방이점",
    "올리아 키친 앤 그로서리",
    "서울서 둘째로 잘하는 집",
    "노블카페 강남점",
    "황소고집",
    "참설농탕 송파본점",
    "우노",
    "순희네빈대떡",
    "을지면옥",
    "돈코보쌈",
    "애플하우스",
    "봉우화로",
    "메리고라운드 신천점",
    "패션 5",
    "버터핑거팬케이크",
    "우대가",
    "성수족발",
    "마도니셰프 명동점",
    "노블카페 가로수길점",
    "먹쉬돈나 삼청동점",
    "부처스컷 청담",
    "군산오징어",
    "진주집",
    "웃사브",
    "미미네",
    "뿔레치킨 홍대본점",
    "남포면옥",
    "밀탑",
    "부첼라",
    "스시효 청담본점",
    "동빙고",
    "서린낙지",
    "오자오동 함흥냉면",
    "우성갈비",
    "평래옥",
    "피자힐",
    "호수삼계탕",
    "호우양꼬치",
    "마포 본점최대포",
    "비스떼까",
    "프로간장게장 본점",
    "피자리움",
    "마마스",
    "맛있는 교토 1호점",
    "영동왕족발",
    "커피스튜디오",
    "한일관 압구정본점",
    "계열사",
    "더 가든 키친",
    "더 스테이크 하우스"
]


class Scraper:

    def __init__(self) -> None:
        self._reviews = []
        self._urls = dict()

    def get_url(self) -> None:
        base_url = Url(restaurants)
        base_url.generate_url()
        self._urls = base_url.get_url()

    def main(self) -> None:
        for keyword, url in zip(self._urls.keys(), self._urls.values()):
            self.get_review(_keyword=keyword, _url=url)
            # scraper.view_reviews()
        self.get_csv_file()

    def get_review(self, _keyword: str, _url: str) -> None:
        try:
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
                review_class_ = Review(name=_keyword, title=title, link=link, description=description, main=main)
                self._reviews.append(review_class_)
        except:
            pass

    def view_reviews(self) -> None:
        for review in self._reviews:
            print(review)

    @staticmethod
    def _get_review_main(link: str) -> str:
        """
        일단 review를 scrape해오고 각 링크에 들어가 main를 하나씩 가져온다.
        :param link: Review 블로그 main contents
        """
        try:
            response = requests.get(link)

            soup = BeautifulSoup(
                response.content,
                "html.parser",
            )

            return soup.find("div", class_="se-main-container").text.replace("\n", "")
        except:
            return None

    def get_csv_file(self) -> None:
        with open("review.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Name",
                    "Title",
                    "Link",
                    "Description",
                    "Main",
                ]
            )
            for review in self._reviews:
                writer.writerow(review.get_review_dict().values())
