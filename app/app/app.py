#!/usr/bin/env python

from . import utils
from . import process_images

import logging
import multiprocessing
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(42)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=False)


def get_contentful_cookie(request):
    """
    Returns the Contentful authentication token from a request

    @param request: the request that contains the cookie
    """
    return request.cookies.get('contentful_token')


def check_has_contentful_cookie(request):
    """
    Checks if a request has a Contentful authentication cookie

    @param request: the request that contains the cookie
    @return: True if the request has a contentful cookie, False otherwise
    """
    return get_contentful_cookie(
        request) is not None  # todo more robust check here


def allowed_file(filename):
    """
    Checks if a file ends with .docx

    @param filename: the name of the file
    @return: True if the file ends with docx, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'docx'


def uploaded_file_path(filename):
    """
    Returns the path of an uploaded file
    """
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
    return render_template('index.html',
                           client_id=client_id,
                           redirect_uri=redirect_uri)


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
        file_path = uploaded_file_path(filename)
        file_exists = os.path.isfile(file_path)
        if file_exists:
            contentful_token = get_contentful_cookie(request)
            thread = multiprocessing.Process(target=process_images.main,
                                             args=(file_path,
                                                   contentful_token))
            thread.start()
            return render_template(
                'upload_success.html',
                space=utils.get_config()['contentful-space-id'],
                environment=utils.get_config()['contentful-environment'])
        else:
            return '''
            <!doctype html>
            <h1>Hmm...the file your provided doesn't exist...</h1>
            '''
    return render_template('upload.html')
