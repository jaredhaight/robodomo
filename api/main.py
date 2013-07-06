from flask import request
from flask.ext.restful import Resource
from mongostore import find_data, update_data, delete_data

def sanitize_data(res):
    res['_id'] = str(res['_id'])
    res['date_created'] = res['date_created'].strftime("%Y-%m-%d %H:%M:%S")
    try:
        res['updated'] = res['updated'].strftime("%Y-%m-%d %H:%M:%S")
    except:
        return res
    return res

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class apiData(Resource):
    def get(self,resID):
        res = find_data(key="_id", value=resID)
        res = sanitize_data(res[0])
        return res

    def put(self,resID):
        res = find_data(key="_id", value=resID)
        for formkey, formdata in request.form.iteritems():
            if formkey in ("_id", "created", "updated"):
                pass
            else:
                res[0][formkey] = formdata
        obj = update_data(res[0])
        obj = sanitize_data(obj)
        return obj

    def delete(self, resID):
        delete_data(resID)
        return {"Status": "Deleted"}