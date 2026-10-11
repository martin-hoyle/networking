from pymongo import MongoClient
from tabulate import tabulate

client = MongoClient("mongodb://localhost:27017")

db = client["network_inventory"]
devices = db["devices"]

device = {
    "hostname": "test-switch2",
    "ip": "192.168.1.20",
    "status": "up"
}

result = devices.insert_one(device)

print(f"Inserted: {result.inserted_id}")

found = devices.find_one({"hostname": "test-switch2"})

# Tabulate a single document: one row, fields as columns
print(tabulate([found], headers="keys", tablefmt="github"))

client.close()