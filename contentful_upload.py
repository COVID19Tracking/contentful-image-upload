import json
from contentful_management import Client
import utils
from os.path import join
import datetime


def __create_asset(environment, title, file, uploadFrom):
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


def __create_image_content_block(environment, title, asset_link):
    """
    Creates a Contentful Image Content Block (a type of Entry)
    """
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


def upload(directory_path):
    """
    Uploads the images in directory_path to Contentful
    """
    website_content_space_id = 'o2ll9t4ee8tq'

    space = __get_client().spaces().find(website_content_space_id)

    environment = space.environments().find('image-optimization')

    for index, file in enumerate(utils.get_files(directory_path)):
        upload = space.uploads().create(join(directory_path, file))
        asset = __create_asset(environment, __get_title(index), file,
                               upload.to_link().to_json())
        asset.process()
        asset.publish()
        image_content_block = __create_image_content_block(
            environment, __get_title(index),
            asset.to_link().to_json())
        image_content_block.publish()