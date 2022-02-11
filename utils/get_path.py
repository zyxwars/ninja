import os


def get_path(file_path, relative_path):
    relative_path = os.path.normpath(relative_path)
    file_dir = os.path.dirname(os.path.realpath(file_path))

    return os.path.join(file_dir, relative_path)
