class Blog:
    def __init__(self, review_id, text):
        self._review_id = review_id
        self._text = text

    @property
    def review_id(self):
        return self._review_id

    @property
    def text(self):
        return self._text
