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
		# TODO: set defaults for each form using publicatoinList and jquery
		return render_template('display/publications.html', publicationList=publicationList,
							   formname='Publications Manifest Form',
							   formfile='display/editpubform.html',
							   use_date=True,
							   use_files=False)
	except Exception as e:
		traceback.print_exc()
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
		return Response(json.dumps(pub, indent=4),
			 mimetype='application/json',
			 headers={'Content-Disposition': 'attachment;filename={}.json'.format(pub_id)})
	return ''
