from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

try:
    client.admin.command("ping")
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
finally:
    client.close()