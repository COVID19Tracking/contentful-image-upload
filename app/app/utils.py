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


def get_directory_path():
    return get_config()['directory-path']


def get_files():
    """
    Gets the files in the images directory
    """
    return [
        f for f in listdir(get_directory_path())
        if isfile(join(get_directory_path(), f))
    ]


def clear_directory(directory_path):
    """
    Clears the directory_path directory, ensures that a directory exists at directory_path
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
    clear_directory(get_directory_path())


def get_file_path():
    """
    Gets the file path from the CLI arguments
    """
    logging.info('Getting file path')
    try:
        file_path = sys.argv[1]
    except IndexError as e:
        print('You need to pass a docx file as an argument...quitting.')
        quit(1)
    if not isfile(file_path):
        print('"' + file_path + "\" doesn't seem to exist...quitting")
        quit(1)
    return file_path
