import process_images
from contentful import utils as contentful_utils
from . import utils
from . import app
import utils as file_utils # todo rename this in filesystem


import multiprocessing
import os
from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


upload = Blueprint('upload', __name__, template_folder='templates')

@upload.route('/upload', methods=['GET', 'POST'])
def main():
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
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(
                utils.get_uploaded_file_path(filename,
                                                 app.UPLOAD_FOLDER))
            return redirect(url_for('upload.main', filename=filename))

    filename = request.args.get('filename')
    if request.method == 'GET' and filename:
        file_path = utils.get_uploaded_file_path(
            filename, app.UPLOAD_FOLDER)
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
                space=file_utils.get_config()['contentful-space-id'],
                environment=file_utils.get_config()['contentful-environment'])
        else:
            return '''
            <!doctype html>
            <h1>Hmm...the file your provided doesn't exist...</h1>
            '''
    return render_template('upload.html')
