#!/usr/bin/env python

import utils
from . import app_utils  # todo rename this
from . import process_images
from contentful import utils as contentful_utils

import logging
import multiprocessing
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'  # uploaded files live here

# configure the Flask app
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(42)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=False)


@app.route('/', methods=['GET'])
def main():
    if contentful_utils.check_has_contentful_cookie(request):
        # go to the upload page if the user is authenticated
        return upload_file()
    else:
        # otherwise, authenticate the user
        return contentful_authentication()


def contentful_authentication():
    """
    A page to begin the Contentful OAuth workflow. Asks the user to
    authenticate with Contentful.
    """
    client_id = utils.get_config()['contentful-client-id']
    redirect_uri = utils.get_config()['redirect-uri']
    return render_template('index.html',
                           client_id=client_id,
                           redirect_uri=redirect_uri)


@app.route('/authenticate', methods=['GET'])
def contentful_callback():
    """
    The URI callback for the Contentful OAuth workflow. Saves the user's
    token to cookies and then redirects to home.
    """
    return render_template('authenticate.html')


@app.route('/too-many-images', methods=['GET'])
def too_many_images(attempted_image_count, max_images):
    """
    An error page for image uploads that exceed the limit.

    @param attempted_image_count: the number of images the user tried to upload
    @param max_images: the maximum number of images allowed per upload
    """
    # todo set the proper invalid request error code
    return render_template('too_many_images.html',
                           attempted_image_count=attempted_image_count,
                           max_images=max_images)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Uploads images to contentful via POST, and accepts image uploads via GET.
    """
    if request.method == 'POST':
        # todo perform these checks somewhere else
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
        if file and app_utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(
                app_utils.get_uploaded_file_path(filename,
                                                 app.config['UPLOAD_FOLDER']))
            return redirect(url_for('upload_file', filename=filename))

    filename = request.args.get('filename')
    if request.method == 'GET' and filename:
        file_path = app_utils.get_uploaded_file_path(
            filename, app.config['UPLOAD_FOLDER'])
        file_exists = os.path.isfile(file_path)
        meets_maximum, attempted_image_count, max_image_count = process_images.check_upload_meets_maximum(
            file_path)
        if not meets_maximum:  # check if this file has more images than the maximum allowed value
            logging.info(filename + ' has too many images: ' +
                         str(attempted_image_count) +
                         ' attempted images exceeds the maximum of ' +
                         str(max_image_count))
            return render_template(
                'too_many_images.html',
                attempted_image_count=attempted_image_count,
                max_image_count=max_image_count,
            )
        if file_exists:
            contentful_token = contentful_utils.get_contentful_cookie(request)
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
