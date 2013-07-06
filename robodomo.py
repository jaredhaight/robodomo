from flask import Flask, render_template, flash, request, abort, redirect, url_for
from flask.ext import restful
from api.server import apiServers, apiServersList, serverClient

app = Flask(__name__)
app.debug = True
app.config.from_object('settings.dev')
api = restful.Api(app)

@app.route('/')
def list_data():
    results = serverClient.find()
    return render_template('list.html', results=results)

@app.route('/resource/<resID>')
def view_resource(resID):
    results = serverClient.find(key="_id", value=resID)
    return render_template("resource/view.html", results=results[0])

@app.route('/delete/<objid>')
def delete_view(objid):
    serverClient.delete(objid)
    return redirect(url_for('list_data'))

api.add_resource(apiServers,'/api/servers/<resID>')
api.add_resource(apiServersList, '/api/servers')

if __name__ == '__main__':
    app.run()