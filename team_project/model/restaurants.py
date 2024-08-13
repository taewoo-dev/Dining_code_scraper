class Restaurant:
    def __init__(self, name, address, latitude, longitude, biz_id):
        self._name = name
        self._address = address
        self._latitude = latitude
        self._longitude = longitude
        self._review_crawling_check = 0

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def review_crawling_check(self):
        return self._review_crawling_check
