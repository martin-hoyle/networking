from pprint import pprint
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

print("MongoDB connection successful!")

print("\nDatabases:")
for database in client.list_database_names():
    print(f"  {database}")


db = client["network_inventory"]
devices = db["devices"]

print("Database:", db.name)
print("Collections:", db.list_collection_names())

for device in devices.find():
    pprint(device)

client.close()
