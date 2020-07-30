import contentful_upload
import utils

from os.path import join
import os
import shutil
import tinify
import json
import zipfile
import logging

# todo add dir path, contentful space id to config
# todo optimize and upload images in parallel

DIR_PATH = "imgs"
CONTENTFUL_SPACE_ID = 'o2ll9t4ee8tq'

with open('config.json') as json_file:
    config = json.load(json_file)

tinify.key = config['tinify-api-key']


def extract_images_from_word(docxpath):
    """
    Pulls the images from a word document into DIR_PATH
    """
    logging.info('Extracting images from Word')

    doc = zipfile.ZipFile(docxpath)

    for info in doc.infolist():
        if info.filename.endswith((".png", ".jpeg", ".gif")):
            doc.extract(info.filename, DIR_PATH)
            shutil.copy(
                join(DIR_PATH, info.filename),
                join(DIR_PATH, 'contentful_' + info.filename.split("/")[-1]))
    doc.close()


def optimize_images():
    """
    Optimizes the images in DIR_PATH via tinify
    """
    files = utils.get_files(DIR_PATH)
    for index, file in enumerate(files):
        logging.info('Optimizing image ' + str(index + 1) + ' of ' +
                     str(len(files)))

        tinify.from_file(join(DIR_PATH, file)).to_file(
            join(DIR_PATH, 'optimized_' + file))
        os.remove(join(DIR_PATH, file))


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    file_path = utils.get_file_path(DIR_PATH)
    utils.clear_directory(DIR_PATH)
    extract_images_from_word(file_path)
    # todo check is png / convert to png
    optimize_images()
    contentful_upload.upload(DIR_PATH, CONTENTFUL_SPACE_ID)
