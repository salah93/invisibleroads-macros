import re
import shutil
from os import makedirs, walk
from os.path import dirname, join, normpath, relpath
from zipfile import ZipFile, ZIP_DEFLATED


def replace_folder(target_folder, source_folder):
    remove_folder(target_folder)
    make_folder(dirname(target_folder))
    shutil.copytree(source_folder, target_folder)


def clean_folder(folder):
    remove_folder(folder)
    make_folder(folder)


def remove_folder(folder):
    try:
        shutil.rmtree(folder)
    except OSError:
        pass


def make_folder(folder):
    try:
        makedirs(folder)
    except OSError:
        pass
    return folder


def find_path(name, folder):
    for root_folder, folder_names, file_names in walk(folder):
        if name in file_names:
            return join(root_folder, name)


def compress(source_folder, target_path=None):
    if not target_path:
        target_path = normpath(source_folder) + '.zip'
    with ZipFile(target_path, 'w', ZIP_DEFLATED) as target_file:
        for root, folders, paths in walk(source_folder):
            for path in paths:
                source_path = join(root, path)
                relative_path = relpath(source_path, source_folder)
                target_file.write(source_path, relative_path)
    return target_path


def uncompress(source_path, target_folder=None):
    if not target_folder:
        target_folder = re.sub(r'\.zip$', '', source_path)
    with ZipFile(source_path, 'r') as source_file:
        source_file.extractall(target_folder)
    return target_folder
