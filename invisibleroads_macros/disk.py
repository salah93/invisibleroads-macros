import fnmatch
import re
import shutil
import subprocess
from contextlib import contextmanager
from glob import glob
from os import chdir, getcwd, makedirs, readlink, symlink, walk
from os.path import (
    exists, isfile, join, splitext,
    abspath, basename, dirname, normpath, realpath, relpath)

from .exceptions import BadArchive, InvisibleRoadsError


def clean_folder(folder):
    remove_folder(folder)
    return make_folder(folder)


def replace_folder(target_folder, source_folder):
    remove_folder(target_folder)
    make_folder(dirname(target_folder))
    shutil.copytree(source_folder, target_folder)
    return target_folder


def make_folder(folder):
    try:
        makedirs(folder)
    except OSError:
        pass
    return folder


def remove_folder(folder):
    try:
        shutil.rmtree(folder)
    except OSError:
        pass
    return folder


def get_nickname(path):
    return splitext(basename(path))[0]


def make_link(source_path, target_path):
    source_path = normpath(source_path)
    if not exists(target_path):
        symlink(source_path, target_path)
        return target_path
    try:
        if normpath(readlink(target_path)) != source_path:
            raise IOError('could not make link; target_path is another link')
    except OSError:
        path_type = 'file' if isfile(target_path) else 'folder'
        raise IOError('could not make link; target_path is a %s' % path_type)
    return target_path


def find_path(name, folder):
    for root_folder, folder_names, file_names in walk(folder):
        if name in file_names:
            return join(root_folder, name)
    raise IOError('cannot find "%s" in "%s"' % (name, folder))


def find_paths(name_expression, folder):
    return [
        join(root_folder, file_name)
        for root_folder, folder_names, file_names in walk(folder)
        for file_name in fnmatch.filter(file_names, name_expression)]


def resolve_relative_path(relative_path, folder):
    relative_path = relpath(join(folder, relative_path), folder)
    if relative_path.startswith('..'):
        raise IOError('relative_path must refer to a file inside folder')
    return join(folder, relative_path)


def compress(source_folder, target_path=None):
    if not target_path:
        target_path = normpath(source_folder) + '.tar.gz'
    target_path = abspath(target_path)
    if target_path.endswith('.tar.gz'):
        command_terms = ['tar', 'czhf']
    else:
        command_terms = ['zip', '-r', '-9']
    with cd(source_folder):
        source_paths = glob('*')
        if not source_paths:
            raise IOError('cannot compress empty folder "%s"' % source_folder)
        subprocess.check_output(command_terms + [target_path] + source_paths)
    return target_path


def compress_zip(source_folder, target_path=None):
    if not target_path:
        target_path = source_folder + '.zip'
    return compress(source_folder, target_path)


def uncompress(source_path, target_folder=None):
    if source_path.endswith('.tar.gz'):
        command_terms = ['tar', 'xf', source_path, '-C']
        target_extension = '.tar.gz'
    else:
        command_terms = ['unzip', source_path, '-d']
        target_extension = '.zip'
    if not target_folder:
        target_folder = re.sub(
            target_extension.replace('.', '\.') + '$', '', source_path)
    make_folder(target_folder)
    try:
        subprocess.check_output(
            command_terms + [target_folder], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        o = e.output
        if 'does not look like a tar archive' in o:
            m = 'could not unpack archive (source_path = %s)'
            raise BadArchive(m % source_path)
        raise InvisibleRoadsError(o)
    return target_folder


@contextmanager
def cd(target_folder):
    source_folder = getcwd()
    try:
        chdir(target_folder)
        yield
    finally:
        chdir(source_folder)


def are_same_path(path1, path2):
    return realpath(path1) == realpath(path2)
