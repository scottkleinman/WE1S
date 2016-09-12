import io

from flask import render_template
from flask import send_file

from app import app, db


@app.route('/display/rawdata/<name>')
def display_raw_data(name):
    d = db.Corpus.find_one({'name': name})
    if d:
        return send_file(io.BytesIO(d['content']), mimetype='application/pdf')
    return render_template('404.html'), 404
