import os
import shutil
import random
import string


def path_join(*paths):
    return os.path.join(*paths)


def is_path_exists(path: str):
    return os.path.exists(path)


def is_dir(path: str):
    return os.path.isdir(path)


def is_file(path: str):
    return os.path.isfile(path)


def get_dir_path(path: str):
    return os.path.dirname(path)


def get_dir_name(path: str):
    return get_file_name(get_dir_path(path))


def get_file_name(path: str):
    return os.path.basename(path)


def get_file_name_wo_ext(path: str):
    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    return name


def get_file_ext(path: str):
    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    return ext[1:]


def make_dirs(dir_path: str, exist_ok=True):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=exist_ok)


def copy_file(src: str, dst: str):
    shutil.copy(src, dst)


def rename_file(old_path: str, new_path: str):
    os.rename(old_path, new_path)


def generate_filename(digits=6):
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set * digits, digits))


def delete_dir(dir_path: str, ignore_errors=True):
    shutil.rmtree(dir_path, ignore_errors=ignore_errors)


def delete_file(file_path: str):
    os.remove(file_path)


def read_as_bytes(file_path: str):
    with open(file_path, 'rb') as reader:
        return reader.read()


def read_as_text(file_path: str, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as reader:
        return reader.read()


def read_lines(file_path: str, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as reader:
        return reader.readlines()


def write_text(file_path: str, text, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as writer:
        return writer.write(text)


def write_bytes(file_path: str, bytes_data=[]):
    with open(file_path, 'wb') as writer:
        for data in bytes_data:
            writer.write(data)
