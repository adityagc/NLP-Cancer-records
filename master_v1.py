# python packages
import json
import os
from os import listdir
import sys
import shutil
import requests
import io
import datetime
from flask import Flask, flash, request, redirect, url_for, Response, jsonify
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin

# nlp-commander packages
from security import authenticate, identity
from processing_path import *


# static api variables

UPLOAD_FOLDER = ('/home/adityagc/Desktop/nlp_commanders/Data-clean')
#UPLOAD_FOLDER = 'local_data'
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'naaccr_2018'
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWT(app, authenticate, identity)

# internal processing


def api_processing(zname, new_dir):
    extracting_dir = 'tempdata'
    extracted_text_dir = ("%s/%s" % (new_dir, extracting_dir))
    if not os.path.exists(extracted_text_dir):
        os.mkdir(extracted_text_dir)
    shutil.unpack_archive(zname, extract_dir=extracted_text_dir)
    input_dir = extracted_text_dir
    os.remove(zname)
    if input_dir[-1] != '/':
        input_dir += '/'

    processed_files = []
    for fi in listdir(input_dir):
        for_processing = (input_dir + fi)
        return_site_jsons = get_cancer_site(for_processing, fi)
        processed_files.append(return_site_jsons)

    return processed_files


# api functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process_path', methods=['GET', 'POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@jwt_required()
def process_path():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dir_set = listdir(app.config['UPLOAD_FOLDER'])
            dir_length = str(len(dir_set))
            subfolder = ("data_run_%s" % dir_length)
            new_dir = ("%s/%s" % (app.config['UPLOAD_FOLDER'], subfolder))
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            zname = os.path.join(new_dir, filename)
            file.save(zname)
            site_jsons = api_processing(zname, new_dir)
            rdump = json.dumps(site_jsons)
            res = Response(rdump, mimetype='application/json')

            return res

    else:
        return jsonify({'message': 'store not found'})

    return


@app.route('/', methods=['GET'])
def get_health():
    return jsonify({'message': 'healthy', "date": datetime.datetime.utcnow(), "ext": list(ALLOWED_EXTENSIONS)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(host='0.0.0.0', port=80, debug=True)
