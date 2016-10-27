import os

from flask import url_for, request
from flask import json
from flask import render_template
from werkzeug.utils import secure_filename

from app import app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def response_JSON(upfile, transactionId, path):
    response = {
        'name': upfile.filename,
        'size': os.path.getsize(path),
        'deleteUrl': url_for('delete_file', transactionId=transactionId, filename=upfile.filename),
        'deleteType': 'DELETE'
    }
    return json.dumps({"files": [response]})


def save_file(uploaded_file, transactionId):
    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], transactionId)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filepath = os.path.join(filepath, filename)
    uploaded_file.save(filepath)

    return filepath


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files_files[]' not in request.files:
            return 'no file part', 400
        upfile = request.files['files_files[]']

        if 'transactionId' not in request.form:
            return 'no transaction id', 400
        transactionId = str(request.form['transactionId'])

        # if user does not select file, browser also
        # submit a empty part without filename
        if upfile.filename == '':
            return 'no file', 400

        if upfile and allowed_file(upfile.filename):
            filepath = save_file(upfile, transactionId)
            return response_JSON(upfile, transactionId, filepath)

        return 'Forbidden', 403
    return render_template("upload/upload.html")


@app.route("/upload/<string:transactionId>/<string:filename>", methods=["DELETE"])
def delete_file(transactionId, filename):
    if len(filename) < 1 or len(transactionId) < 1 or not allowed_file(filename):
        return 'Forbidden', 403
    try:
        filename = secure_filename(filename)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], transactionId, filename))
        return 'OK', 200
    except OSError:
        return 'Not found', 404
