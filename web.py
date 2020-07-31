from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def uploaded_file_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(uploaded_file_path(filename))
            return redirect(url_for('upload_file', filename=filename))

    filename = request.args.get('filename')
    if request.method == 'GET' and filename:
        file_exists = os.path.isfile(uploaded_file_path(filename))
        if file_exists:
            return '''
            <!doctype html>
            <h1>You uploaded a file!</h1>
            '''
        else:
            return '''
            <!doctype html>
            <h1>You uploaded a file that doesn't exist...</h1>
            '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
