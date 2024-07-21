from model.crawling import Crawling


if __name__ == "main":
    app = Crawling()
    app.get_reviews()