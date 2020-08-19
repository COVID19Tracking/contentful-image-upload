from contentful import contentful
import utils

from os.path import join
import os
import shutil
import zipfile
from PIL import Image
import logging

# todo optimize and upload images in parallel

images_directory = utils.get_images_directory()

IMAGE_EXTENSIONS = (".png", ".jpeg", ".jpg")  # todo add gifs


def extract_images_from_word(docx_path):
    """
    Pulls the images from a Word document into images_directory
    """
    logging.info('Extracting images from Word')

    doc = zipfile.ZipFile(docx_path)

    for info in doc.infolist():
        if info.filename.endswith(IMAGE_EXTENSIONS):
            doc.extract(info.filename, images_directory)
            shutil.copy(
                join(images_directory, info.filename),
                join(images_directory,
                     'contentful_' + info.filename.split("/")[-1]))
    doc.close()


def optimize_images():
    """
    Optimizes the images in images_directory with PIL's optimization.
    This works with PNG and JPEG files.
    """
    # todo bypass with gifs
    files = utils.get_image_files()
    for index, file in enumerate(files):
        logging.info('Optimizing image ' + str(index + 1) + ' of ' +
                     str(len(files)))
        Image.open(join(images_directory,
                        file)).save(join(images_directory,
                                         'optimized_' + file),
                                    optimized=True)
        os.remove(join(images_directory, file))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_upload_meets_maximum(docx_path):
    """
    Checks if the uploaded file has fewer than the maximum number of allowed images.
    Returns a tuple like: (has_too_many_images<bool>, attempted_image_count<int>, max_image_count<int>)
    has_too_many_images:
        False: this file has too many images
        True: the number of images in this file is below the maximum
    """
    max_images = 15  # the maximum allowed number of images per uploaded file

    doc = zipfile.ZipFile(docx_path)  # todo handle the docx not existing

    count_images_in_file = sum(
        file for file in
        [info.filename.endswith(IMAGE_EXTENSIONS) for info in doc.infolist()])

    return (count_images_in_file < max_images, count_images_in_file,
            max_images)


def main(file_path, contentful_token=None, delete_file=True):
    optimize_images()

    contentful.upload_images(contentful_token)

    if delete_file:
        logger.info('Deleting ' + file_path)
        os.remove(file_path)  # delete doc when done

    logger.info('Clearing imgs directory')
    utils.clear_images_directory()

    logger.info('Completed run for ' + file_path)
