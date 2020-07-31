import json
from contentful_management import Client
import utils
from os.path import join
import datetime
import logging


def __create_asset(environment, title, file, uploadFrom):
    """
    Creates a Contentful asset
    """
    logging.info('Creating asset: ' + title)
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


def __create_image_content_block(environment, title, asset_link):
    """
    Creates a Contentful Image Content Block (a type of Entry)
    """
    logging.info('Creating image content block: ' + title)
    return environment.entries().create(
        None, {
            'content_type_id': 'contentBlockImage',
            'fields': {
                'nameInternal': {
                    'en-US': title
                },
                'image': {
                    'en-US': asset_link
                }
            }
        })


def __get_title(index):
    """
    Gets the asset/entry title for Contentful
    """
    return 'Auto-uploaded image (' + str(index + 1) + ') at ' + str(
        datetime.datetime.now().replace(microsecond=0))


def __get_client():
    with open('config.json') as json_file:
        config = json.load(json_file)

    return Client(config['contentful-access-token'])


def upload(directory_path, space_id):
    """
    Uploads the images in directory_path to Contentful
    """
    space = __get_client().spaces().find(space_id)  # get the proper space

    environment = space.environments().find('image-optimization')

    for index, file in enumerate(utils.get_files()):
        upload = space.uploads().create(join(directory_path,
                                             file))  # upload the image

        # create the asset, linked to the upload
        asset = __create_asset(environment, __get_title(index), file,
                               upload.to_link().to_json())
        asset.process()
        asset.publish()

        # create the image content block, linked to the asset
        image_content_block = __create_image_content_block(
            environment, __get_title(index),
            asset.to_link().to_json())
        image_content_block.publish()
