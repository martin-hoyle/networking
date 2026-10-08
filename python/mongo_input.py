from pymongo import MongoClient

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

print(found)

client.close()