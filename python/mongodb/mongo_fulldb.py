from pymongo import MongoClient
from tabulate import tabulate

client = MongoClient("mongodb://localhost:27017")
db = client["network_inventory"]

for collection_name in db.list_collection_names():
    print(f"\n### {collection_name}\n")

    rows = list(db[collection_name].find({}, {"_id": 0}))

    if not rows:
        print("(empty)")
        continue

    print(tabulate(rows, headers="keys", tablefmt="github"))

client.close()