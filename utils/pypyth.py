import os


def pre_handle_path(*path):
    for p in path:
        if not os.path.exists(p):
            os.makedirs(p)


def standardized_path(file_dir):
    return file_dir if file_dir[-1] == '/' or file_dir[-1] == '\\' else file_dir + '/'
