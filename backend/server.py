from flask import Flask, app, request, render_template, Response, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os, shutil
import json
import bot as bot

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

def clear_files():
    '''
    Clears all files in the 'files' folder.
    '''
    UPLOAD_FOLDER = 'files'
    #clears uploads folder on flask app run
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@app.route(f'{base_url}/query/', methods=['POST'])
def query():
    print("I'm getting queried or something")
    
    if request.method == 'POST':
        req = request.get_json()
        question = req['question'] # This is the question that the user asked in the form
        # answer = query(question)
        answer = "your question was boring so this is your answer"
        # source_list = get_sources(question)
        source_list = ["source1", "source2", "source3"]
        return make_response(
            jsonify(question=question,
                answer=answer,
                sources=source_list,
                status=200)
                             )
    return Response(jsonify('something broke'), status=401)


@app.route(f'{base_url}/documents/', methods=['POST'])
def documents():
    files = request.files['files'] 
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
    hintings = bot.Bot('files')
    app.run(debug=True)