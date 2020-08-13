from . import contentful_upload
from . import utils

from os.path import join
import os
import shutil
import zipfile
from PIL import Image
import logging

# todo optimize and upload images in parallel

images_directory = utils.get_images_directory()


def extract_images_from_word(docxpath):
    """
    Pulls the images from a Word document into images_directory
    """
    logging.info('Extracting images from Word')

    doc = zipfile.ZipFile(docxpath)

    for info in doc.infolist():
        if info.filename.endswith((".png", ".jpeg", ".jpg")):  # todo add gifs
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
    files = utils.get_files()
    for index, file in enumerate(files):
        logging.info('Optimizing image ' + str(index + 1) + ' of ' +
                     str(len(files)))
        Image.open(join(images_directory,
                        file)).save(join(images_directory, 'optimized_' + file),
                                    optimized=True)
        os.remove(join(images_directory, file))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# utils.clear_images_directory()


def main(file_path, contentful_token=None, delete_file=True):
    extract_images_from_word(file_path)

    optimize_images()

    contentful_upload.upload(contentful_token)

    # todo add cap to total # of images, maybe 25?
    if delete_file:
        logger.info('Deleting ' + file_path)
        os.remove(file_path)  # delete doc when done

    logger.info('Clearing imgs directory')
    utils.clear_images_directory()

    logger.info('Completed run for ' + file_path)


if __name__ == '__main__':
    main('file2.docx',
         utils.get_config()['development-contentful-token'],
         delete_file=False)
