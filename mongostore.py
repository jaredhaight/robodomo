from pymongo import MongoClient
from bson.objectid import ObjectId
from settings.dev import MONGODB_DB, MONGODB_COLLECTION
from datetime import datetime
client = MongoClient()
db = client[MONGODB_DB]



class roboMongoClient(object):
    def __init__(self, collection=MONGODB_COLLECTION):
        self.collection = db[collection]


    def insert(self, data):
        #Takes a dict, saves it to Mongo
        data["date_created"] = datetime.utcnow()
        obj = self.collection.insert(data)
        return obj

    def update(self, data):
        #Takes a dict, updates in Mongo
        data["updated"] = datetime.utcnow()
        self.collection.save(data)
        obj = self.collection.find_one({"_id":data["_id"]})
        return obj

    def find(self, **kwargs):
        #Returns a list of results
        key = kwargs.get('key', None)
        value = kwargs.get('value', None)
        l = []
        if key and not value:
            results = self.collection.find({key:{"$exists": "true"}})
        elif key == "_id" and value:
            results = self.collection.find({key:ObjectId(value)})
        elif key and value:
            results = self.collection.find({key:value})
        else:
            results = self.collection.find()
        for result in results:
            l.append(result)
        if len(l) == 0:
            return None
        return l

    def delete(self, objid):
        self.collection.remove({'_id': ObjectId(objid)})
