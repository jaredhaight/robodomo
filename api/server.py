from flask import request
from flask.ext.restful import Resource, reqparse, abort
from mongostore import roboMongoClient
from utils import sanitize_data, sanitize_stats, organize_stats, validate_stats, validate_server, get_data_from_request

serverClient = roboMongoClient(collection="servers")
statsClient = roboMongoClient(collection="stats")

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
        data = get_data_from_request(request)
        for key, value in data.iteritems():
            test = validate_stats(key, value)
            if test is not True:
                return abort(400, message=test)
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
        data = get_data_from_request(request)
        test = validate_server(data)
        if test is not True:
            return abort(400, message=test)
        server = serverClient.insert(data)
        result = serverClient.find(key="_id", value=str(server))
        result = sanitize_data(result[0])
        return result
