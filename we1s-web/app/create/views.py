from flask import Blueprint, render_template, redirect, request

create = Blueprint('create', __name__,
                   template_folder='templates')


@create.route('/create/publication', methods=['GET', 'POST'])
def create_publication():
    if request.method == 'POST':
        print request.get_json()
        redirect('index')

    return render_template('create/main.html',
                           formname='Publications Manifest Form',
                           formfile='create/publication.html')


@create.route('/create/corpus')
def create_corpus():
    return render_template('create/corpus.html')


@create.route('/create/collection', methods=['GET', 'POST'])
def create_collection():
    return render_template('create/main.html',
                           formname='Collection Manifest Form',
                           formfile='create/collection.html')


@create.route('/create/rawdata', methods=['GET', 'POST'])
def create_rawdata():
    return render_template('create/main.html',
                           formname='Raw Data Manifest Form',
                           formfile='create/rawdata.html')


@create.route('/create/processeddata', methods=['GET', 'POST'])
def create_processeddata():
    return render_template('create/main.html',
                           formname='Processed Data Manifest Form',
                           formfile='create/processeddata.html')


@create.route('/create/metadata', methods=['GET', 'POST'])
def create_metadata():
    return render_template('create/main.html',
                           formname='Metadata Manifest Form',
                           formfile='create/metadata.html')


@create.route('/create/outputs', methods=['GET', 'POST'])
def create_outputs():
    return render_template('create/main.html',
                           formname='Outputs Manifest Form',
                           formfile='create/outputs.html')


@create.route('/create/related', methods=['GET', 'POST'])
def create_related():
    return render_template('create/main.html',
                           formname='Related Manifest Form',
                           formfile='create/related.html')
