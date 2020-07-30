import contentful_upload
import utils

from os.path import join
import os
import shutil
import tinify
import json
import zipfile

# todo pass document as CLI argument
# todo add logging

FILE_PATH = "input doc.docx"
DIR_PATH = "imgs"
CONTENTFUL_SPACE_ID = 'o2ll9t4ee8tq'

with open('config.json') as json_file:
    config = json.load(json_file)

tinify.key = config['tinify-api-key']


def extract_images_from_word(docxpath):
    """
    Pulls the images from a word document into DIR_PATH
    """
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
    for file in utils.get_files(DIR_PATH):
        tinify.from_file(join(DIR_PATH, file)).to_file(
            join(DIR_PATH, 'optimized_' + file))
        os.remove(join(DIR_PATH, file))


if __name__ == '__main__':
    utils.clear_directory(DIR_PATH)
    extract_images_from_word(FILE_PATH)
    # todo check is png / convert to png
    optimize_images()
    contentful_upload.upload(DIR_PATH, CONTENTFUL_SPACE_ID)
