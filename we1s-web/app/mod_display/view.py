import io, mimetypes, json, traceback
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
		pp(publicationList)

		return render_template('display/publications.html', publicationList=publicationList,
							   formname='Publications Manifest Form',
							   formfile='display/editpubform.html',
							   use_date=True,
							   use_files=False)
	except Exception as e:
		traceback.print_exc()
		abort(500)

@app.route('/display/publications/table')
def table_data():
	table_data = []
	loop_index = 0
	for pub in db.Publications.find():
		loop_index += 1
		pub_row = [loop_index]
		pub_row += [pub['publication']]
		data_id = pub['_id']
		pub_row += ['<button type="button" title="Edit" class="btn btn-default" id="edit" data-id="{0}"><span class="glyphicon glyphicon-pencil"></span></button><button type="button" title="Delete" class="btn btn-default" id="delete" data-id="{0}"><span class="glyphicon glyphicon-trash"></span></button><button type="button" title="Export Manifest" class="btn btn-default" id="export" data-id="{0}"><span class="glyphicon glyphicon-download"></span></button>'.format(data_id)]
		table_data += [pub_row]

	return jsonify(table_data)

@app.route('/display/rawdata/<name>')
def display_raw_data(name):
    d = db.Corpus.find_one({'name': name})
    mimetype = mimetypes.guess_type(name)[0] # Gets the mimetype from the extension
    if d:
        return send_file(io.BytesIO(d['content']), mimetype=mimetype)
    return render_template('404.html'), 404

@app.route('/display/publications/delete', methods=['POST'])
def delete():
	if '_id' in request.form:
		pub_id = request.form.get('_id')
		db.Publications.delete_one({'_id':pub_id})
	return ''


@app.route('/display/publications/export/', methods=['POST'])
def export():
	print request.form
	if '_id' in request.form:
		pub_id = request.form.get('_id')
		pub = db.Publications.find_one({'_id': pub_id})
		return Response(json.dumps(pub, indent=4),
			 mimetype='application/json',
			 headers={'Content-Disposition': 'attachment;filename={}.json'.format(pub_id)})
	return ''
