import io, mimetypes, json, traceback, re
from pprint import pprint as pp
from flask import render_template, send_file, abort, request, jsonify, Response

from app import app, db

@app.route('/display/publications')
def display_publications():
	try:
		publications = db.Publications
		publicationList = []
		for item in publications.find():
			item['path'] = item['path'].replace(',','/')
			publicationList.append(item)
		# pp(publicationList)

		return render_template('display/publications.html', publicationList=publicationList,
							   formname='Publications Manifest Form',
							   formfile='display/editpubform.html',
							   use_date=True,
							   use_files=False)
	except Exception as e:
		traceback.print_exc()
		abort(500)


@app.route('/display/publications/table')
def pub_table_data():
	table_data = []
	loop_index = 0
	for pub in db.Publications.find():
		loop_index += 1
		pub_row = [pub['_id']]
		pub_row += [pub['publication']]
		data_id = pub['_id']
		pub_row += ['<button type="button" title="Edit" class="btn btn-default" id="edit" data-id="{0}"><span class="glyphicon glyphicon-pencil"></span></button><button type="button" title="Delete" class="btn btn-default" id="delete" data-id="{0}"><span class="glyphicon glyphicon-trash"></span></button><button type="button" title="Export Manifest" class="btn btn-default" id="export" data-id="{0}"><span class="glyphicon glyphicon-download"></span></button>'.format(data_id)]
		table_data += [pub_row]

	return json.dumps(table_data)

@app.route('/display/corpus')
def display_corpora():
	try:
		corpus = db.Corpus
		corpusList = []
		for item in corpus.find():
			item['path'] = item['path'].replace(',','/')
			corpusList.append(item)
		# pp(publicationList)

		return render_template('display/abstract_display.html', publicationList=corpusList,
							   item_name='corpus',
							   collection_name='corpus',
							   columns=['Corpus ID','Path'],
							   formname='Publications Manifest Form',
							   formfile='display/editpubform.html',
							   use_date=True,
							   use_files=False)
	except Exception as e:
		traceback.print_exc()
		abort(500)


@app.route('/display/corpus/table')
def corpus_table_data():
	table_data = []
	loop_index = 0
	for pub in db.Corpus.find():
		loop_index += 1
		pub_row = [pub['_id'],pub['_id'],pub['path']]
		data_id = pub['_id']
		pub_row += ['<button type="button" title="Edit" class="btn btn-default" id="edit" data-id="{0}"><span class="glyphicon glyphicon-pencil"></span></button><button type="button" title="Delete" class="btn btn-default" id="delete" data-id="{0}"><span class="glyphicon glyphicon-trash"></span></button><button type="button" title="Export Manifest" class="btn btn-default" id="export" data-id="{0}"><span class="glyphicon glyphicon-download"></span></button>'.format(data_id)]
		table_data += [pub_row]

	return json.dumps(table_data)

@app.route('/display/rawdata/<name>')
def display_raw_data(name):
    d = db.Corpus.find_one({'name': name})
    mimetype = mimetypes.guess_type(name)[0] # Gets the mimetype from the extension
    if d:
        return send_file(io.BytesIO(d['content']), mimetype=mimetype)
    return render_template('404.html'), 404


@app.route('/display/<collection_name>/delete/', methods=['POST'])
def delete(collection_name):
	if '_id' in request.form:
		doc_id = request.form.get('_id')
		db[collection_name.capitalize()].delete_one({'_id':doc_id})
	return ''


@app.route('/display/<collection_name>/export/', methods=['POST'])
def export(collection_name):
	if '_id' in request.form:
		doc_id = request.form.get('_id')
		doc = db[collection_name.capitalize()].find_one({'_id': doc_id})
		return Response(json.dumps(doc, indent=4),
			 mimetype='application/json',
			 headers={'Content-Disposition': 'attachment;filename={}.json'.format(doc_id)})
	return ''


@app.route('/display/<collection_name>/multiexport/', methods=['POST'])
def multiexport(collection_name):
	if '_ids' in request.form:
		return_docs = []
		id_list = json.loads(request.form.get('_ids'))

		for doc_id in id_list:
			doc = db[collection_name.capitalize()].find_one({'_id': doc_id})
			return_docs += [doc]
		return Response(json.dumps(return_docs, indent=4),
			 mimetype='application/json',
			 headers={'Content-Disposition': 'attachment;filename={}.json'.format('MultiExport')})
	return ''


@app.route('/display/<collection_name>/multidelete/', methods=['POST'])
def multidelete(collection_name):
	if '_ids' in request.form:
		id_list = json.loads(request.form.get('_ids'))
		for doc_id in id_list:
			db[collection_name.capitalize()].delete_one({'_id':doc_id})
	return ''


