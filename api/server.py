from flask import request
from flask.ext.restful import Resource, reqparse, abort
from mongostore import roboMongoClient
from utils import sanitize_data, clean_response_data, clean_request_data, organize_stats, validate_stats, validate_server, get_data_from_request

serverClient = roboMongoClient(collection="servers")
statsClient = roboMongoClient(collection="stats")

class apiServers(Resource):
    def get(self,resID):
        result = serverClient.find(key="_id", value=resID)
        try:
            statsList = statsClient.find(key="server_id", value=resID)
            stats = organize_stats(statsList)
            cleanStats = sanitize_data(stats)
        except:
            cleanStats = None
        result = clean_response_data(result[0])
        if cleanStats:
            result["stats"] = cleanStats
        return result

    def post(self,resID):
        data = get_data_from_request(request)
        for key, value in data.iteritems():
            test = validate_stats(key, value)
            if test is not True:
                return abort(400, message=test)
        data["server_id"] = resID
        data = clean_request_data(data)
        stats = statsClient.insert(data)
        result = statsClient.find(key="_id", value=str(stats))
        obj = clean_response_data(result[0])
        return obj

    def put(self,resID):
        result = serverClient.find(key="_id", value=resID)
        data = get_data_from_request(request)
        test = validate_server(data)
        if test is not True:
            return abort(400, message=test)
        else:
            for key, value in data.iteritems():
                if key in ("_id", "created", "updated"):
                    pass
                else:
                    result[0][key] = value
        cleanRes = clean_request_data(result[0])
        obj = serverClient.update(cleanRes)
        obj = clean_response_data(obj)
        return obj

    def delete(self, resID):
        serverClient.delete(resID)
        return {"message": "Object deleted"}

class apiServersList(Resource):
    def get(self):
        if request.args.get('tag'):
            servers = serverClient.find(key="tags", value=request.args.get('tag'))
        else:
            servers = serverClient.find()
        i = 0
        d = []
        for server in servers:
            i = i + 1
            server = clean_response_data(server)
            d.append(server)
        results = {"count":i}
        results.update({"servers":d})
        return results

    def post(self):
        data = get_data_from_request(request)
        test = validate_server(data)
        if test is not True:
            return abort(400, message=test)
        data = clean_request_data(data)
        server = serverClient.insert(data)
        result = serverClient.find(key="_id", value=str(server))
        result = sanitize_data(result[0])
        return result
