import os


def get_path(script_path, relative_path):
    file_dir = os.path.dirname(os.path.realpath(script_path))

    return os.path.join(file_dir, relative_path)
