import fnmatch
import re
import tarfile
from contextlib import contextmanager
from os import chdir, getcwd, makedirs, remove, walk, listdir
from os.path import (
    abspath, basename, dirname,
    exists, isdir, isfile,
    join, normpath, realpath,
    relpath, sep, splitext)
from pathlib import Path
from shutil import copytree, rmtree
from tempfile import mkdtemp
from zipfile import ZipFile, ZIP_DEFLATED


def make_folder(folder):
    """
        makes a folder, doesn't raise an exception if folder already exists
    """
    try:
        makedirs(folder)
    except OSError:
        pass
    return folder


def clean_folder(folder):
    """
        removes folder contents
    """
    remove_path(folder)
    return make_folder(folder)


def replace_folder(target_folder, source_folder):
    """
        replaces a folder with source_folder
    """
    if isfile(target_folder):
        raise OSError('must pass directory')
    remove_path(target_folder)
    copytree(source_folder, target_folder)
    return target_folder


def remove_path(path):
    """ removes a file or directory from disk """
    try:
        rmtree(path)
    except OSError:
        try:
            remove(path)
        except OSError:
            pass
    return path


def get_nickname(path):
    """
        returns the name of file,
        example: ./file.txt -> file
    """
    return splitext(basename(path))[0]


def make_link(source_path, target_path):
    """
        creates a symbolic link to source_path
    """
    from os import readlink, symlink
    source_path = normpath(source_path)
    if not exists(target_path):
        symlink(source_path, target_path)
        return target_path
    try:
        if normpath(readlink(target_path)) != source_path:
            raise IOError('could not make link; target_path is another link')
        else:
            return target_path
    except OSError:
        path_type = 'file' if isfile(target_path) else 'folder'
        raise IOError(
            'could not make link; target_path is a {0}'.format(path_type))


def find_path(name, folder):
    """
        finds the file in folder/sub-folders
    """
    for root, folders, files in walk(folder):
        if name in files:
            return join(root, name)
    raise IOError('cannot find {0} in {1}'.format(name, folder))


def find_paths(name_expression, folder):
    """
        finds files matching the expression in folder,
        and subfolders
    """
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
    """
        compresses a folder to a target_path
        if folder ends with '.tar.gz' a tarball is produced
        otherwise it is compressed into a zip file
    """
    if not target_path:
        target_path = source_folder + '.tar.gz'
    if target_path.endswith('.tar.gz'):
        compress_tar_gz(source_folder, target_path)
    else:
        compress_zip(source_folder, target_path)
    return target_path


def compress_tar_gz(source_folder, target_path=None):
    """
        compresses into a tarball
    """
    if not target_path:
        target_path = source_folder + '.tar.gz'
    with tarfile.open(target_path, 'w:gz', dereference=True) as target_file:
        for path in find_paths('*', source_folder):
            if isdir(path):
                continue
            target_file.add(str(path), str(relpath(path, source_folder)))
    return target_path


def compress_zip(source_folder, target_path=None, excludes=None):
    if not target_path:
        target_path = source_folder + '.zip'
    with ZipFile(
        target_path, 'w', ZIP_DEFLATED, allowZip64=True,
    ) as target_file:
        for path in Path(source_folder).rglob('*'):
            if path.is_dir():
                continue
            if has_name_match(path, excludes):
                continue
            target_file.write(
                str(path), str(path.relative_to(source_folder)))
    return target_path


def uncompress(source_path, target_folder=None):
    if source_path.endswith('.tar.gz'):
        source_file = tarfile.open(source_path, 'r:gz')
        target_folder = re.sub(r'\.tar.gz$', '', source_path)
    else:
        source_file = ZipFile(source_path, 'r')
        target_folder = re.sub(r'\.zip$', '', source_path)
    source_file.extractall(target_folder)
    source_file.close()
    return target_folder


def are_same_path(path1, path2):
    return realpath(path1) == realpath(path2)


def has_name_match(path, expressions):
    name = basename(str(path))
    for expression in expressions or []:
        if fnmatch.fnmatch(name, expression):
            return True
    return False


@contextmanager
def cd(target_folder):
    source_folder = getcwd()
    try:
        chdir(target_folder)
        yield
    finally:
        chdir(source_folder)


@contextmanager
def make_temporary_folder(suffix='', prefix='tmp', target_folder=None):
    temporary_folder = mkdtemp(suffix, prefix, target_folder)
    yield temporary_folder
    rmtree(temporary_folder)


def make_enumerated_folder_for(script_path, first_index=1):
    package_name = get_nickname(script_path)
    if 'run' == package_name:
        package_folder = get_package_folder(script_path)
        package_name = get_nickname(package_folder)
    return make_enumerated_folder(join(sep, 'tmp', package_name), first_index)


def make_enumerated_folder(base_folder, index=1):
    """make an indexed subfolder to base_folder"""
    target_folder = join(base_folder, str(index))
    if exists(target_folder):
        return make_enumerated_folder(base_folder, index + 1)
    else:
        makedirs(target_folder)
        return target_folder


def get_package_folder(script_path):
    return dirname(abspath(script_path))


def change_owner_and_group_recursively(target_folder, target_username):
    'Change uid and gid of folder and its contents, treating links as files'
    from os import lchown
    from pwd import getpwnam
    pw_record = getpwnam(target_username)
    target_uid = pw_record.pw_uid
    target_gid = pw_record.pw_gid
    for root_folder, folders, names in walk(target_folder):
        for folder in folders:
            lchown(join(root_folder, folder), target_uid, target_gid)
        for name in names:
            lchown(join(root_folder, name), target_uid, target_gid)
    lchown(target_folder, target_uid, target_gid)
