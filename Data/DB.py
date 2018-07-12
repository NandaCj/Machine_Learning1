import pymongo
from pymongo import MongoClient
import re



class Connection:
    def __init__(self):
        pass

    @property
    def Connect(self):
        client = MongoClient('mongodb://localhost:27017/')
        return client

if __name__ == "__main__":
    obj = Connection()
    client = obj.Connect
    db = client.ET.ETCompanyCodes
    print (db)
    print (list(db.find({})))