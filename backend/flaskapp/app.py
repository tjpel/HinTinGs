from flask import Flask, app
from flask_restful import Api, Resource
from flaskapp import routes

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def __init__(self):
        pass
    def get(self):
        return json.dumps({'hello': 'world'})

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)