from flask import request
from flask.ext.restful import Resource, reqparse, fields
from mongostore import roboMongoClient
import datetime

serverClient = roboMongoClient(collection="servers")
statsClient = roboMongoClient(collection="stats")

def sanitize_data(res):
    res['_id'] = str(res['_id'])
    res['date_created'] = res['date_created'].strftime("%Y-%m-%d %H:%M:%S")
    try:
        res['updated'] = res['updated'].strftime("%Y-%m-%d %H:%M:%S")
    except:
        return res
    return res

def sanitize_stats(stats):
    for stat in stats:
        for key, value in stats[stat].iteritems():
            if isinstance(key, datetime.datetime):
                stringKey = key.strftime("%Y-%m-%d %H:%M:%S")
                stats[stat][stringKey] = value
                del(stats[stat][key])
    return stats

def organize_stats(statsList):
    #Get a list of unique things we've monitored
    l = []
    for result in statsList:
        for key in result:
            if key in ("_id", "date_created", "server_id"):
                pass
            else:
                try:
                    l.index(key)
                except:
                    l.append(key)
    #For the things that we're monitoring, create a dict of {thing:{time:value}}
    stats = {}
    for item in l:
        d = {}
        for result in statsList:
            try:
                d[result["date_created"]]=result[item]
            except:
                pass
        stats[item] = d
    return stats

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help="Required: Name of the Resource")
parser.add_argument('type', type=str, required=True, help="Required: Type of resource (ex: Terminal Server, Web Server, etc..)")
parser.add_argument('tags', type=str, help="Tags for server", action="append")

class apiServers(Resource):
    def get(self,resID):
        res = serverClient.find(key="_id", value=resID)
        statsList = statsClient.find(key="server_id", value=resID)
        stats = organize_stats(statsList)
        cleanStats = sanitize_stats(stats)
        res = sanitize_data(res[0])
        res["stats"] = cleanStats
        return res

    def post(self,resID):
        data = dict()
        if request.json:
            data = request.json
        else:
            for key,value in request.form.iteritems():
                data[key] = value
        data["server_id"] = resID
        stats = statsClient.insert(data)
        result = statsClient.find(key="_id", value=str(stats))
        result = sanitize_data(result[0])
        return result

    def put(self,resID):
        res = serverClient.find(key="_id", value=resID)
        for formkey, formdata in request.form.iteritems():
            if formkey in ("_id", "created", "updated"):
                pass
            else:
                res[0][formkey] = formdata
        obj = serverClient.update(res[0])
        obj = sanitize_data(obj)
        return obj

    def delete(self, resID):
        serverClient.delete(resID)
        return {"Status": "Deleted"}

class apiServersList(Resource):
    def get(self):
        servers = serverClient.find()
        i = 0
        d = []
        for server in servers:
            i = i + 1
            server = sanitize_data(server)
            d.append(server)
        results = {"count":i}
        results.update({"servers":d})
        return results

    def post(self):
        args = parser.parse_args()
        print args
        server = serverClient.insert(args)
        result = serverClient.find(key="_id", value=str(server))
        result = sanitize_data(result[0])
        return result
