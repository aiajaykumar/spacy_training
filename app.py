from flask import *
from flask import Flask,request,jsonify
from werkzeug.utils import secure_filename
import shutil
import pickle
import spacy
import textract
import os
import json
import pandas as pd

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

@app.route('/upload', methods = ['GET', 'POST'])
def main():
    if request.method== 'GET':
        return render_template('upload.html')

@app.route('/results', methods = ['POST','GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file'] 
        filename, file_extension = os.path.splitext(f.filename)
        PATH=os.path.abspath(os.path.dirname(__file__))
        f.save(os.path.join(PATH, secure_filename(f.filename)))
        file_path=os.path.join(PATH,secure_filename(f.filename))
        obj2 = {"status":"True","msg":"successfully uploaded","file_path":file_path,"file_extension":file_extension}
        nlp2 = spacy.load("/home/ajay/spacy_models/14nov-updated_model_0.1_dropout {'ner': 7020.282915422188}")
        print("model loaded")
        try:
            examples = textract.process(file_path,encoding = "utf-8")
            # examples = open(file_path, 'r').readlines()
            examples = examples.decode()
            doc = nlp2(examples)
            # entities = dict([(str(x), x.label_) for x in nlp2(examples).ents])
            # print(entities)
            # return jsonify(entities)
            entities = [{ent.label_:ent.text} for ent in doc.ents]
            return {'entities': entities}
        except:
            return "There was an error while reading your file Please upload valid file"

if __name__=='__main__':
    app.run("192.168.1.4",debug=True)

    