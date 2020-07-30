from os import listdir
from os.path import isfile, join


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
    os.makedirs(directory_path)
