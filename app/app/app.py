#!/usr/bin/env python

import file_utils
from contentful import utils as contentful_utils
from . import upload_file

import logging
from flask import Flask, flash, request, render_template
import os

UPLOAD_FOLDER = 'uploads'  # uploaded files live here

# configure the Flask app
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(42)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(upload_file.upload)


@app.route('/', methods=['GET'])
def main():
    if contentful_utils.check_has_contentful_cookie(request):
        # go to the upload page if the user is authenticated
        return upload_file.main()
    else:
        # otherwise, authenticate the user
        return contentful_authentication()


def contentful_authentication():
    """
    A page to begin the Contentful OAuth workflow. Asks the user to
    authenticate with Contentful.
    """
    client_id = file_utils.get_config()['contentful-client-id']
    redirect_uri = file_utils.get_config()['redirect-uri']
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=False)
