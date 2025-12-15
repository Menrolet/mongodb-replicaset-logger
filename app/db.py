from pymongo import MongoClient

MONGO_URI = (
    "mongodb://mongo1:27017,"
    "mongo2:27017,"
    "mongo3:27017/"
    "?replicaSet=rs0"
)

client = MongoClient(MONGO_URI)
db = client["event_db"]
events = db["events"]

events.create_index("timestamp")
events.create_index("level")
events.create_index("service")
