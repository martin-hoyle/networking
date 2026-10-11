from pymongo import MongoClient
from tabulate import tabulate

client = MongoClient("mongodb://localhost:27017")

db = client["network_inventory"]
devices = db["devices"]

rows = list(devices.find({}, {"_id": 0}))

print(tabulate(rows, headers="keys", tablefmt="github"))

client.close()