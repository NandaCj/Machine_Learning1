from pymongo import MongoClient as MG

client = MG("mongodb://127.0.0.1:27017")
db = client.NseDb

print (len(list(db.NseCodesCollection.find({"_id":"NseCodes"}))))


