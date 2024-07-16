class Review:

    def __init__(self, name: str, title: str, link: str, description: str, main: str) -> None:
        self._name = name
        self._title = title
        self._link = link
        self._description = description
        self._main = main

    def __str__(self):
        return f"name: {self._name}, title: {self._title}, link: {self._link}, dsc: {self._description}"

    def get_review_dict(self) -> dict:
        return {
            "name": self._name,
            "title": self._title,
            "link": self._link,
            "description": self._description,
            # "main": self._main
            # "main": "pass"
        }