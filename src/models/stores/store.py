import uuid

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store:
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def get_tag(self):
        return self.tag_name

    def get_query(self):
        return self.query

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    def save_to_db(self):
        Database.update(StoreConstants.COLLECTION, {"_id": self._id}, self.json() )

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, self.json())

    @classmethod
    def get_by_name(cls, name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": name}))

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    # @classmethod
    # def find_by_url(cls, url):
    #     for i in range(1, len(url)+1):
    #         store = cls.get_by_url_prefix(url[:i])
    #         return store
    #     else:
    #         raise StoreErrors.StoreNotFoundError('store not found')

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]


