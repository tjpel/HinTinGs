from flask import Flask, app, request, render_template, Response, make_response, jsonify
from werkzeug.utils import secure_filename
#from flask_restful import Api, Resource
from flask_cors import CORS
import os
import json

def get_base_url(port:int) -> str:
    '''
    Returns the base URL to the webserver if available.
    
    i.e. if the webserver is running on coding.ai-camp.org port 12345, then the base url is '/<your project id>/port/12345/'
    
    Inputs: port (int) - the port number of the webserver
    Outputs: base_url (str) - the base url to the webserver
    '''
    
    try:
        info = json.load(open(os.path.join(os.environ['HOME'], '.smc', 'info.json'), 'r'))
        project_id = info['project_id']
        base_url = f'/{project_id}/port/{port}/'
    except Exception as e:
        print(f'Server is probably running in production, so a base url does not apply: \n{e}')
        base_url = '/'
    return base_url


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

port = 5000
base_url = get_base_url(port)

# @app.route('/query', methods=['GET', 'POST'])
# def query():
#     if request.method == 'POST':
#         return 'POST received', 204
#     return 'GET received', 200

@app.route(f'{base_url}/query/', methods=['POST'])
def query():
    print("I'm getting queried or something")
    
    if request.method == 'POST':
        print("I'm RECEIVING A POST REQUEST")
        req = request.get_json()
        question = req['question']
        print("Question was: " + question)
        return make_response(
            jsonify(question=question,
                answer='your question was boring so this is your answer',
                sources=['i made it all up'],
                status=200)
                             )
    return Response(jsonify('something broke'), status=401)


@app.route(f'{base_url}/documents/', methods=['POST'])
def documents():
    print("I'm RECEIVING A POST REQUEST")
    print("Request Method: " + str(request.method))
    print("Request Files: " + str(request.files))
    
    files = request.files['files']
    print("Files: " + str(files))
    if not files or len(request.files) < 1:
        return Response('No files received', status=400)

    data = []
    sources = []
        # ext = os.path.splitext(file[0])[1]
        # if ext.lower() in ['.md', '.txt']:
        #     data.append(str(file.read(), encoding='utf-8', errors='ignore'))
        #     sources.append(file.name)
    # text_splitter = CharacterTextSplitter(chunk_size=1500, separator='\n')
    # docs = []
    # metadatas = []
    # for i, d in enumerate(data):
    #     splits = text_splitter.split_text(d)
    #     docs.extend(splits)
    #     metadatas.extend([{'source': sources[i]}] * len(splits))

    # embeddings = embedding.embed_documents(docs)

    # SourceDocument.objects.all().delete()

    # for i in range(len(embeddings)):
    #     SourceDocument.objects.create(
    #         name=metadatas[i]['source'],
    #         content=docs[i],
    #         embedding=embeddings[i]
    #     )
    return make_response(jsonify('files received! ready to be queried'), 200)




if __name__ == '__main__':
    app.run(debug=True)