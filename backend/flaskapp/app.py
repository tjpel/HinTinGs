from flask import Flask, app, request
from flask_restful import Api, Resource
from flaskapp import routes

app = Flask(__name__)

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        return 'POST received', 204
    return 'GET received', 200


@app.route('/documents')
def documents():
    return 'Hello, World!'


api = Api(app)

class HelloWorld(Resource):
    def __init__(self):
        pass
    def get(self):
        return json.dumps({'hello': 'world'})

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)