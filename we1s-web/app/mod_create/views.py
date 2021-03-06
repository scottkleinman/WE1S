import os
import shutil

from bson import Binary
from flask import abort, Blueprint, render_template, request

from app import db, app

create = Blueprint('create', __name__,
                   template_folder='templates')


def trim_json(json):
    if isinstance(json, unicode):
        return json
    for key, value in json.iteritems():
        if isinstance(value, dict):
            json[key] = trim_json(value)
        elif isinstance(value, list):
            for i in range(len(value)):
                value[i] = trim_json(value[i])
            json[key] = value
        elif isinstance(value, basestring):
            json[key] = value.strip(' \t')
    return json


def process_files(json):
    files = json['files']
    for f in files:
        path = os.path.join(app.config['UPLOAD_FOLDER'], f['transactionId'], f['name'])
        content = open(path, 'rb').read()
        f.update({'content': Binary(content), 'path': json['path'] + ',' + f['name']})
        db.Corpus.insert_one(f)
    return json


def clean_up_fs(json):
    # In case that files were uploaded in different transactions, i.e editing a collection
    # delete all possible directories
    for uploaded_file in json['files']:
        path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file['transactionId'])
        if os.path.exists(path):
            shutil.rmtree(path)
    del json['files']


def write_to_db(json, collection):
    json = trim_json(json)
    json['path'] = json['path'].replace('/', ',')
    if 'files' in json:
        json = process_files(json)
        clean_up_fs(json)
    db[collection].update_one({'_id': json['_id']}, {'$set': json}, upsert=True)


@create.route('/create/corpus')
def create_corpus():
    return render_template('create/corpus.html')


@create.route('/create/publication', methods=['GET', 'POST'])
def create_publication():
    if request.method == 'POST':
        try:
            write_to_db(request.get_json(), 'Publications')
            return 'OK', 200
        except Exception:
            abort(500)
    return render_template('create/main.html',
                           formname='Publications Manifest Form',
                           formfile='create/publication.html',
                           use_date=True,
                           use_files=False)


@create.route('/create/collection', methods=['GET', 'POST'])
def create_collection():
    if request.method == 'POST':
            write_to_db(request.get_json(), 'Corpus')
            return 'OK', 200

    return render_template('create/main.html',
                           formname='Collection Manifest Form',
                           formfile='create/collection.html',
                           use_date=True,
                           use_files=False)


@create.route('/create/rawdata', methods=['GET', 'POST'])
def create_raw_data():
    if request.method == 'POST':
        try:
            write_to_db(request.get_json(), 'Corpus')
            return 'OK', 200
        except IOError:
            return 'Failed to locate file', 500
        except Exception as err:
            print err
            abort(500)
    return render_template('create/main.html',
                           formname='Raw Data Manifest Form',
                           formfile='create/rawdata.html',
                           use_date=False,
                           use_files=True)


@create.route('/create/processeddata', methods=['GET', 'POST'])
def create_processed_data():
    if request.method == 'POST':
        try:
            write_to_db(request.get_json(), 'Corpus')
            return 'OK', 200
        except Exception:
            abort(500)
    return render_template('create/main.html',
                           formname='Processed Data Manifest Form',
                           formfile='create/processeddata.html',
                           use_date=False,
                           use_files=True)


@create.route('/create/outputs', methods=['GET', 'POST'])
def create_outputs():
    if request.method == 'POST':
        try:
            write_to_db(request.get_json(), 'Corpus')
            return 'OK', 200
        except Exception:
            abort(500)
    return render_template('create/main.html',
                           formname='Outputs Manifest Form',
                           formfile='create/outputs.html',
                           use_date=False,
                           use_files=True)


@create.route('/create/related', methods=['GET', 'POST'])
def create_related():
    if request.method == 'POST':
        try:
            write_to_db(request.get_json(), 'Corpus')
            return 'OK', 200
        except Exception:
            abort(500)
    return render_template('create/main.html',
                           formname='Related Manifest Form',
                           formfile='create/related.html',
                           use_date=False,
                           use_files=True)


@create.route('/create/metadata', methods=['GET', 'POST'])
def create_metadata():
    if request.method == 'POST':
        try:
            write_to_db(request.get_json(), 'Corpus')
            return 'OK', 200
        except Exception:
            abort(500)
    return render_template('create/main.html',
                           formname='Metadata Manifest Form',
                           formfile='create/metadata.html',
                           use_date=False,
                           use_files=False)
