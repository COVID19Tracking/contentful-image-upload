import sys
from os import listdir, makedirs
import shutil
from os.path import isfile, join, isfile


def get_files(directory_path):
    """
    Gets the files in the images directory, specified by directory_path
    """
    return [
        f for f in listdir(directory_path) if isfile(join(directory_path, f))
    ]


def clear_directory(directory_path):
    """
    Clears the directory_path directory, ensures that a directory exists at directory_path
    """
    try:
        shutil.rmtree(directory_path)
    except FileNotFoundError as e:
        pass  # directory doesn't exist, probably the first run
    makedirs(directory_path)


def get_file_path(directory_path):
    try:
        file_path = sys.argv[1]
    except IndexError as e:
        print('You need to pass a docx file as an argument...quitting.')
        quit(1)
    if not isfile(file_path):
        print('"' + file_path + "\" doesn't seem to exist...quitting")
        quit(1)
    return file_path
