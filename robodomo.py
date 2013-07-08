from flask import Flask, render_template
from flask.ext import restful
from api.server import apiServers, apiServersList, serverClient

app = Flask(__name__)
app.debug = True
app.config.from_object('settings.dev')
api = restful.Api(app)

@app.route('/servers')
def list_data():
    client = apiServersList()
    results = client.get()
    return render_template('list.html', results=results)

@app.route('/servers/<resID>')
def view_resource(resID):
    apiClient = apiServers()
    results = apiClient.get(resID)
    return render_template("servers/view.html", results=results)


api.add_resource(apiServers,'/api/servers/<resID>')
api.add_resource(apiServersList, '/api/servers')

if __name__ == '__main__':
    app.run()