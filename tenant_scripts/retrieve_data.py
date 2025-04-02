import pymongo
import os
from dotenv import load_dotenv
load_dotenv()


class Retriever:
    def __init__(
        self,
        mongo_url,
        database_name,
        collection_name
    ):
        self.client = pymongo.MongoClient(mongo_url)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
    
    def retrieve_latest_data(self, number_of_data):
        return self.collection.find().sort([("_id", -1)]).limit(number_of_data)
    
    def process_output(self, data):
        return data["review_headline"]
    def process_retrieve_results_raw(self, res):
        full_data = []
        for data in res:
            full_data.append(data)
        return full_data

    def retrieve_latest_reviews(self, number_of_reviews):
        res_retrieve = self.retrieve_latest_data(number_of_reviews)
        comments = []
        full_data = self.process_retrieve_results_raw(res_retrieve)
        # print(len(full_data))
        for data in full_data:
            comments.append(self.process_output(data))
        return comments, full_data

if __name__ == "__main__":
    retriever = Retriever(
        mongo_url="mongodb+srv://huytrinh:anhhuy123@bdp.bek7v.mongodb.net/",
        database_name="test_streaming",
        collection_name="test2"
    )
    comments, data = retriever.retrieve_latest_reviews(5)
    # print(res[1])
    # print(len(res))
    print(len(data), len(comments))
