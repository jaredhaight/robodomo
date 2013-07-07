import datetime

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

def validate_stats(key, value):
    if key.find(" ") > -1:
        return "Name can not contain spaces"
    if type(value) is not int:
        return "Values must be integers"
    return True

def validate_server(data):
    try:
        data["name"]
    except:
        return "Need name"
    try:
        data["type"]
    except:
        return "Need type"
    return True

def get_data_from_request(request):
    if request.json:
        data = request.json
    else:
        data = dict()
        for key,value in request.form.iteritems():
            data[key] = value
    return data

