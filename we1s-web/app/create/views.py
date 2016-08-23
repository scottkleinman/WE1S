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


@create.route('/create/collection')
def create_collection():
    return render_template('create/corpus.html')


@create.route('/create/rawdata')
def create_rawdata():
    return render_template('create/corpus.html')


@create.route('/create/processeddata')
def create_processeddata():
    return render_template('create/corpus.html')


@create.route('/create/metadata')
def create_metadata():
    return render_template('create/corpus.html')


@create.route('/create/outputs')
def create_outputs():
    return render_template('create/corpus.html')


@create.route('/create/related')
def create_related():
    return render_template('create/corpus.html')
