import utils

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}

app = Flask(__name__, template_folder='templates')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def check_has_contentful_cookie(request):
    return request.cookies.get('contentful_token') is not None


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def uploaded_file_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET'])
def main():
    if check_has_contentful_cookie(request):
        return upload_file()
    else:
        return contentful_authentication()


def contentful_authentication():
    client_id = utils.get_config()['contentful-client-id']
    redirect_uri = utils.get_config()['redirect-uri']
    return '''
    <!doctype html>
    <h1>
        <a href="https://be.contentful.com/oauth/authorize?response_type=token&client_id={0}&redirect_uri={1}&scope=content_management_manage">
        Authenticate on Contentful
        </a>
    </h1>
    '''.format(client_id, redirect_uri)


@app.route('/authenticate', methods=['GET'])
def contentful_callback():
    return render_template('authenticate.html')


@app.route('/upload', methods=['GET', 'POST'])
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
    <p>authenticated with contentful &#10004;</p>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
