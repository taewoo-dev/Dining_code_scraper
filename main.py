from scraper import Scraper
from url import Url

keywords = [
    "명동교자",
    "옛날민속집 본점",
    "만족 오향족발",
    "쟈니덤플링",
    "미즈컨테이너",
]


def main(scraper: Scraper):
    base_url = Url(keywords)
    base_url.generate_url()
    urls = base_url.get_url()

    for url in urls:
        scraper.get_review(url)
        # scraper.view_reviews()
        scraper.get_csv_file()


if __name__ == "__main__":
    scraper = Scraper()
    main(scraper=scraper)
