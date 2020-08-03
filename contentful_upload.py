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


def __get_client(contentful_token):
    return Client(contentful_token)


def __get_contentful_space_id():
    return utils.get_config()["contentful-space-id"]


def __get_contentful_environment(space):
    environment_name = utils.get_config()["contentful-environment"]
    return space.environments().find(environment_name)


def __publish_items(items):
    for attempt in range(3):
        try:
            [item.publish() for item in items]
        except VersionMismatchError as e:
            print(item, 'publising failed')


def upload(contentful_token):
    """
    Uploads the images in directory_path to Contentful
    """
    space = __get_client(contentful_token).spaces().find(
        __get_contentful_space_id())  # get the proper space

    environment = __get_contentful_environment(space)

    directory_path = utils.get_directory_path()

    uploads = []
    for index, file in enumerate(utils.get_files()):
        logging.info('Uploading upload: ' + __get_title(index))

        upload = space.uploads().create(join(directory_path,
                                             file))  # upload the image
        uploads.append(upload)

    assets = []
    for index, upload in enumerate(uploads):
        # create the asset, linked to the upload
        asset = __create_asset(environment, __get_title(index),
                               __get_title(index),
                               upload.to_link().to_json())
        asset.process()
        assets.append(asset)

    image_content_blocks = []
    for index, asset in enumerate(assets):
        # create the image content block, linked to the asset
        image_content_block = __create_image_content_block(
            environment, __get_title(index),
            asset.to_link().to_json())
        image_content_blocks.append(image_content_block)

    # image_content_block.publish()
    __publish_items(assets)
    __publish_items(image_content_blocks)
