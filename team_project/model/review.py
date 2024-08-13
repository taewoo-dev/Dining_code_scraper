class Review:

    def __init__(self, restaurant_id, name: str, title: str, link: str, description: str) -> None:
        self._restaurant_id = restaurant_id
        self._title = title
        self._link = link
        self._description = description
        self._blog_crawling_check = 0

    @property
    def restaurant_id(self):
        return self._restaurant_id

    @property
    def title(self):
        return self._title

    @property
    def link(self):
        return self._link

    @property
    def description(self):
        return self._description

    @property
    def blog(self):
        return self._blog_crawling_check
