import logging
from os.path import join

import file_utils
from . import contentful as cf

# todo break into components
def upload_to_contentful(contentful_token):
    """
    Uploads the images in the images directory to Contentful

    @param contentful_token: the authentication token for Contentful
    """
    space = cf.__get_contentful_client(contentful_token).spaces().find(
        cf.__get_contentful_space_id())  # get the proper space

    environment = cf.__get_contentful_environment(space)

    images_directory = file_utils.get_images_directory()

    uploads = []
    for index, file in enumerate(file_utils.get_image_files()):
        logging.info('Uploading upload: ' + cf.__get_title(index))

        upload = space.uploads().create(join(images_directory,
                                             file))  # upload the image
        uploads.append(upload)

    assets = []
    for index, upload in enumerate(uploads):
        # create the asset, linked to the upload
        asset = cf.__create_asset(environment, cf.__get_title(index),
                                  cf.__get_title(index),
                                  upload.to_link().to_json())
        asset.process()
        assets.append(asset)

    image_content_blocks = []
    for index, asset in enumerate(assets):
        # create the image content block, linked to the asset
        image_content_block = cf.__create_image_content_block(
            environment, cf.__get_title(index),
            asset.to_link().to_json())
        image_content_blocks.append(image_content_block)

    assets = [environment.assets().find(a.id)
              for a in assets]  # update from Contentful
    logging.info('Publishing ' + str(len(assets)) + ' assets')
    cf.__publish_items(assets)

    image_content_blocks = [
        environment.entries().find(icb.id) for icb in image_content_blocks
    ]  # update from Contentful
    logging.info('Publishing ' + str(len(image_content_blocks)) +
                 ' image content blocks')
    cf.__publish_items(image_content_blocks)
