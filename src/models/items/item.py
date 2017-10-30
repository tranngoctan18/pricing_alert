import uuid

from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse

from src.common.database import Database
from src.models.stores.store import Store
import src.models.items.constants as ItemConstants
import src.models.alerts.errors as AlertErrors


class Item:
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}".format(self.name, self.url)

    def get_price(self):
        """Get item's price from URL"""

        store = Store.get_by_url_prefix(urlparse(self.url).hostname)
        tag_name, query = store.get_tag(), store.get_query()
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(tag_name, query)
        if element is None:
            raise AlertErrors.TagNameError("tag name bi sai")
        element_text = element.text.strip()
        pattern = re.compile("(\d+\.*,*)+(\d+\.*,*)+")
        match = pattern.search(element_text).group()
        if "." in match:
            self.price = int(match.replace(".", ""))
        elif "," in match:
            self.price = int(match.replace(",", ""))
        else:
            raise AlertErrors.ReError("regular expression tag bi sai")

    def save_to_db(self):
        Database.update(ItemConstants.COLLECTION, query={"_id": self._id}, data=self.json())

    def json(self):
        return {"name": self.name,
                "url": self.url,
                "_id": self._id,
                "price": self.price
                }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": _id}))
