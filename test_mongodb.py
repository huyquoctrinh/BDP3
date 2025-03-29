import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['tenant']
collection = db['list_tenant']
# print(collection.find_one(filter={"tenant_id": "9"}))
collection.insert_one({"tenant_id": "10"})
# print(inserted.inserted_id)
print(collection.find_one(filter={"tenant_id": "10"}))