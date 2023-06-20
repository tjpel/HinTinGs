from flaskapp import app
from flask import request

# This is the main entry point for the application.

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        return 'POST received', 204
    return 'GET received', 200


@app.route('/documents')
def documents():
    return 'Hello, World!'
