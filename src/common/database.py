import pymongo


class Database:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize(): # create table
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["fullstack"]

    @staticmethod
    def insert(collection, data): # create
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query): # retrieve
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query): # retrieve
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)