import os


def allowed_file(filename):
    """
    Checks if a file ends with .docx

    @param filename: the name of the file
    @return: True if the file ends with docx, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'docx'


def get_uploaded_file_path(filename, upload_folder):
    """
    Returns the path of an uploaded file

    @param filename: the name of the file
    @param upload_folder: the folder that contains uploaded files
    @return: the path to filename
    """
    return os.path.join(upload_folder, filename)
