import pymongo
import os 
from dotenv import load_dotenv
load_dotenv()

class Updater:
    def __init__(
        self,
        mongo_url,
        database_name,
        collection_name
    ):
        self.client = pymongo.MongoClient(mongo_url)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
    
    def merge_data(self, full_data, labels):
        # print(len(full_data), len(labels))
        for i in range(len(full_data)):
            full_data[i]["label"] = labels[i]
            del full_data[i]["_id"]
        return full_data

    def update_data(self, data, labels):
        update_records = self.merge_data(data, labels)
        # print(len(update_records), type(update_records))
        self.collection.insert_many(update_records)
        # print(update_records[0])
        return update_records
    
