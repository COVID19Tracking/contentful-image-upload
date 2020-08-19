import utils

import json
from contentful_management import Client
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
                        'contentType':
                        'image/png',  # todo set based on image type
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


def __get_contentful_client(contentful_token):
    return Client(contentful_token)


def __get_contentful_space_id():
    return utils.get_config()["contentful-space-id"]


def __get_contentful_environment(space):
    environment_name = utils.get_config()["contentful-environment"]
    return space.environments().find(environment_name)


def __publish_items(items):
    """
    Publishes a list of Contentful assets/entries.
    """
    [item.publish() for item in items]

