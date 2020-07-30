from contentful_management import Client
from os import listdir
from os.path import isfile, join
import os
import shutil
import tinify
import json
import zipfile
"""
pip install tinify contentful_management
"""

# todo pass document as CLI argument

FILE_PATH = "input doc.docx"
DIR_PATH = "imgs"

with open('config.json') as json_file:
    config = json.load(json_file)

client = Client(config['contentful-access-token'])
tinify.key = config['tinify-api-key']


def get_files():
    """
    Gets the files in the images directory, specified by DIR_PATH
    """
    return [f for f in listdir(DIR_PATH) if isfile(join(DIR_PATH, f))]


def clear_directory():
    """
    Clears the DIR_PATH directory, ensures that a directory exists at DIR_PATH
    """
    try:
        shutil.rmtree(DIR_PATH)
    except FileNotFoundError as e:
        pass  # directory doesn't exist, probably the first run
    os.makedirs(DIR_PATH)


def extract_images_from_word(docxpath):
    """
    Pulls the images from a word document into DIR_PATH
    """
    doc = zipfile.ZipFile(docxpath)
    for info in doc.infolist():
        if info.filename.endswith((".png", ".jpeg", ".gif")):
            doc.extract(info.filename, DIR_PATH)
            shutil.copy(
                DIR_PATH + "\\" + info.filename,
                DIR_PATH + "\\" + 'contentful_' + info.filename.split("/")[-1])
    doc.close()


def optimize_images():
    """
    Optimizes the images in DIR_PATH via tinify
    """
    for file in get_files():
        tinify.from_file(join(DIR_PATH, file)).to_file(
            join(DIR_PATH, 'optimized_' + file))
        os.remove(join(DIR_PATH, file))


def _create_asset(environment, title, file, uploadFrom):
    """
    Creates a Contentful asset
    """
    return environment.assets().create(
        None,  # no set id
        {
            'fields': {
                'title': {
                    'en-US': title,
                },
                'file': {
                    'en-US': {
                        'fileName': file,
                        'contentType': 'image/png',
                        'uploadFrom': uploadFrom
                    }
                }
            }
        })


def _get_title(index):
    """
    Gets the asset/entry title for Contentful
    """
    return 'Auto-uploaded image (' + str(index + 1) + ')'


def upload_images_to_contentful():
    """
    Uploads the images in DIR_PATH to Contentful
    """
    website_content_space_id = 'o2ll9t4ee8tq'
    space = client.spaces().find(website_content_space_id)
    environment = space.environments().find('image-optimization')
    for index, file in enumerate(get_files()):
        upload = space.uploads().create(join(DIR_PATH, file))
        asset = _create_asset(environment, _get_title(index), file,
                              upload.to_link().to_json())
        asset.process()
        asset.publish()
        image_content_block = environment.entries().create(
            None, {
                'content_type_id': 'contentBlockImage',
                'fields': {
                    'nameInternal': {
                        'en-US': _get_title(index)
                    },
                    'image': {
                        'en-US': asset.to_link().to_json()
                    }
                }
            })
        image_content_block.publish()


clear_directory()
extract_images_from_word(FILE_PATH)
# todo check is png / convert to png
optimize_images()

upload_images_to_contentful()
