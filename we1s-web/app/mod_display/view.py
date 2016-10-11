import io, mimetypes

from flask import render_template, send_file, abort, request, jsonify, Response

from app import app, db

@app.route('/display/publications')
def display_publications():
	try:
		publications = db.Publications
		publicationList = []
		for item in publications.find():
			publicationList.append(item)
		return render_template('display/publications.html', publicationList=publicationList)
	except Exception:
		abort(500)
 
@app.route('/display/rawdata/<name>')
def display_raw_data(name):
    d = db.Corpus.find_one({'name': name})
    mimetype = mimetypes.guess_type(name)[0] # Gets the mimetype from the extension
    if d:
        return send_file(io.BytesIO(d['content']), mimetype=mimetype)
    return render_template('404.html'), 404

@app.route('/display/publications/delete', methods=['POST'])
def delete():
	print request.form
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
		# pub_json = jsonify(pub)
		# pub_json.headers['Content-Type'] = 'application/download'
		# pub_json.headers['Content-Disposition'] = 'attachment;filename={}.json'.format(pub_id)
		# return pub_json
		return Response(str(pub),
			 mimetype='application/json',
			 headers={'Content-Disposition': 'attachment;filename={}.json'.format(pub_id)})
	return ''
