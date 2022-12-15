from pymongo import MongoClient
client = MongoClient()
db = client["my_db"]
db["camera"].drop()
db["alert"].drop()
#db["user"].drop()
db["fs.chunks"].drop()
db["fs.files"].drop()
