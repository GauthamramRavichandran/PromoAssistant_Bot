from pymongo import MongoClient

client = MongoClient()
print(client.list_database_names())  # Databases
db = client.promo_assistant
print(db.collection_names())  # Collections
