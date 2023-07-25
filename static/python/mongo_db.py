import pymongo
import os


class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient(os.environ.get("MONGO_CONNECTION_ADDRESS"))
        self.db = self.client["pingu-shop"]

    def insert_to_db(self, collection_name, query_dict):
        collection = self.db[collection_name]
        collection.insert_one(query_dict)

    def select_from_db(self, collection_name, query_dict):
        collection = self.db[collection_name]
        result_list = [item for item in collection.find(query_dict)]

        return result_list

    def delete_from_db(self, collection_name, query_dict):
        collection = self.db[collection_name]
        collection.delete_many(query_dict)

    def update_db(self, collection_name, filter_query_dict, update_query_dict):
        collection = self.db[collection_name]
        collection.update_one(filter_query_dict, update_query_dict)

    def aggregate_from_db(self, collection_name, query_list):
        collection = self.db[collection_name]
        result_list = [item for item in collection.aggregate(query_list)]

        return result_list