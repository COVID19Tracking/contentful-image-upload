import contentful_upload
import utils

from os.path import join
import os
import shutil
import zipfile
from PIL import Image
import logging

# todo optimize and upload images in parallel

config = utils.get_config()

directory_path = utils.get_directory_path()


def extract_images_from_word(docxpath):
    """
    Pulls the images from a word document into directory_path
    """
    logging.info('Extracting images from Word')

    doc = zipfile.ZipFile(docxpath)

    for info in doc.infolist():
        if info.filename.endswith((".png", ".jpeg")):
            doc.extract(info.filename, directory_path)
            shutil.copy(
                join(directory_path, info.filename),
                join(directory_path,
                     'contentful_' + info.filename.split("/")[-1]))
    doc.close()


def optimize_images():
    """
    Optimizes the images in directory_path with PIL's optimization.
    This works with PNG and JPEG files.
    """
    files = utils.get_files()
    for index, file in enumerate(files):
        logging.info('Optimizing image ' + str(index + 1) + ' of ' +
                     str(len(files)))

        Image.open(join(directory_path,
                        file)).save(join(directory_path, 'optimized_' + file),
                                    optimized=True)
        os.remove(join(directory_path, file))


logging.basicConfig(level=logging.INFO)


def main():
    file_path = utils.get_file_path()

    utils.clear_directory()

    extract_images_from_word(file_path)

    optimize_images()

    contentful_upload.upload()

    # todo delete Word doc
    # todo add cap to total # of images, maybe 25?


if __name__ == '__main__':
    main()
