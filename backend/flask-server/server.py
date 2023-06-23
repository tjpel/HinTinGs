from flask import Flask, app, request, render_template, Response
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource
import os
# import json

app = Flask(__name__)
api = Api(app)

# @app.route('/query', methods=['GET', 'POST'])
# def query():
#     if request.method == 'POST':
#         return 'POST received', 204
#     return 'GET received', 200

class Query(Resource):
    def __init__(self):
        self.format = {
            'question': 'What is Django?',
            'answer': 'Django is a web framework',
            'sources': "placeholder"
            }
    def get(self):
        return Response(self.format, status=200)
    
    def put(self, question="", answer="", sources=""):
        if question:
            self.format['question'] = question
        if answer:
            self.format['answer'] = answer
        if sources:
            self.format['sources'] = sources
        return Response(self.format, status=201)

api.add_resource(Query, '/query')



@app.route('/documents/', methods=['POST'])
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
    for file in files:
        print("File is just the entire text file so I won't print it all.")
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
    return Response('files ingested! ready to be queried', status=200)

@app.route('/about')
def about():
    print("SOMEONE IS TRYING TO GO TO THE ABOUT PAGE")
    return "About page"



if __name__ == '__main__':
    app.run(debug=True)