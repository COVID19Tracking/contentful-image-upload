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

CONTENTFUL_SPACE_ID = 'o2ll9t4ee8tq'

with open('config.json') as json_file:
    config = json.load(json_file)

directory_path = utils.get_directory_path()
tinify.key = config['tinify-api-key']


def extract_images_from_word(docxpath):
    """
    Pulls the images from a word document into directory_path
    """
    logging.info('Extracting images from Word')

    doc = zipfile.ZipFile(docxpath)

    for info in doc.infolist():
        if info.filename.endswith((".png", ".jpeg", ".gif")):
            doc.extract(info.filename, directory_path)
            shutil.copy(
                join(directory_path, info.filename),
                join(directory_path,
                     'contentful_' + info.filename.split("/")[-1]))
    doc.close()


def optimize_images():
    """
    Optimizes the images in directory_path via tinify
    """
    files = utils.get_files()
    for index, file in enumerate(files):
        logging.info('Optimizing image ' + str(index + 1) + ' of ' +
                     str(len(files)))

        tinify.from_file(join(directory_path, file)).to_file(
            join(directory_path, 'optimized_' + file))
        os.remove(join(directory_path, file))


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    file_path = utils.get_file_path()
    utils.clear_directory()
    extract_images_from_word(file_path)
    # todo check is png / convert to png
    optimize_images()
    contentful_upload.upload(directory_path, CONTENTFUL_SPACE_ID)
