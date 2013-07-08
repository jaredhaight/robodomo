from flask import request
from bson import ObjectId
import datetime
valid_server_keys = ("_id","name","type","tags")

def clean_response_data(res):
    for key, value in res.iteritems():
        if isinstance(key, datetime.datetime):
            stringKey = key.strftime("%Y-%m-%d %H:%M:%S")
            res[stringKey] = value
            del(res[key])
        if isinstance(value, datetime.datetime):
            res[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(value, ObjectId):
            res[key] = str(value)
    return res

def clean_request_data(data):
    try:
        data["tags"] = data["tags"].split()
    except:
        pass
    return data

def sanitize_data(res):
    for obj in res:
        for key, value in res[obj].iteritems():
            if isinstance(key, datetime.datetime):
                stringKey = key.strftime("%Y-%m-%d %H:%M:%S")
                res[obj][stringKey] = value
                del(res[obj][key])
            if isinstance(value, datetime.datetime):
                res[obj][key] = value.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(value, ObjectId):
                res[obj][key] = str(value)
    return res

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

def validate_stats(key, value):
    if key.find(" ") > -1:
        return "Name can not contain spaces"
    if type(value) is not int:
        return "Values must be integers"
    return True

def validate_server(data):
    if request.method == "POST":
        try:
            data["name"]
        except:
            return "Need name"
        try:
            data["type"]
        except:
            return "Need type"
    for key, value in data.iteritems():
        if key not in valid_server_keys:
            return "%s is not a recognized key for server" % (key)
    return True

def get_data_from_request(request):
    if request.json:
        data = request.json
    else:
        data = dict()
        for key,value in request.form.iteritems():
            data[key] = value
    return data

