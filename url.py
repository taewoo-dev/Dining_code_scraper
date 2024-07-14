from urllib import parse


class Url:

    def __init__(self, url_keywords: list) -> None:
        self._url_keywords = url_keywords
        self._url_list = []

    def generate_url(self) -> None:

        for url_keyword in self._url_keywords:
            encoding_keyword = parse.quote(url_keyword)
            url = f"https://m.search.naver.com/search.naver?ssc=tab.m_blog.all&query={encoding_keyword}&sm=tab_opt&nso=so%3Ar%2Cp%3A3m"
            self._url_list.append(url)

    def get_url(self) -> list:
        return self._url_list

