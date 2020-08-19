import sys
from os import listdir, makedirs
import shutil
from os.path import isfile, join, isfile
import logging
import json

with open('config.json') as json_file:
    config = json.load(json_file)


def get_config():
    return config


def get_images_directory():
    return get_config()['images-directory']


def get_image_files():
    """
    Gets the files in the images directory
    """
    return [
        f for f in listdir(get_images_directory())
        if isfile(join(get_images_directory(), f))
    ]


def clear_directory(directory_path):
    """
    Clears the directory_path directory, ensures that a directory exists at directory_path

    @param directory_path: The path of the directory to clear
    """
    logging.info('Clearing directory ' + directory_path)
    try:
        shutil.rmtree(directory_path)
    except FileNotFoundError as e:
        pass  # directory doesn't exist, probably the first run
    makedirs(directory_path)


def make_logs_directory():
    """
    Clears the images directory, makes sure the logs directory exists
    """
    clear_directory('logs')


def clear_images_directory():
    """
    Clears the images directory, makes sure the directory exists
    """
    clear_directory(get_images_directory())
