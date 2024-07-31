from database.diningcode_db import excute_query
from config import CONNECTION


class Review:

    def __init__(self, name: str, title: str, link: str, description: str) -> None:
        self._name = name
        self._title = title
        self._link = link
        self._description = description
        self._blog = None

    def __str__(self):
        return f"name: {self._name}, title: {self._title}, link: {self._link}, dsc: {self._description}"

    def get_review_db(self) -> None:
        sql_restaurants_table = """
        insert into restaurants (restaurant_name)
        values (%s)
        """
        excute_query(CONNECTION, sql_restaurants_table, self._name)

        sql_restaurants_ID = """
        select restaurants.restaurant_ID from restaurants
        where restaurant_name = (%s) limit 1;
        """
        restaurants_ID = excute_query(CONNECTION, sql_restaurants_ID, self._name)[0]["restaurant_ID"]

        sql = """
        insert into reviews (restaurant_ID, review_title, review_link, review_description)
        values (%s, %s, %s, %s)
        """
        excute_query(CONNECTION, sql, restaurants_ID, self._title, self._link, self._description)