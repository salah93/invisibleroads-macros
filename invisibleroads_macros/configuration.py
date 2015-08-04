import re
from collections import defaultdict
from os import makedirs
from os.path import abspath, dirname, join

from .disk import get_nickname


def get_interpretation_by_name(settings, prefix, interpret_setting):
    interpretation_by_name = defaultdict(dict)
    pattern_key = re.compile(prefix.replace('.', r'\.') + r'(.*)\.(.*)')
    for key, value in settings.iteritems():
        try:
            name, attribute = pattern_key.match(key).groups()
        except AttributeError:
            continue
        interpretation = interpretation_by_name[name]
        interpretation.update(interpret_setting(attribute, value))
    return interpretation_by_name


def suggest_target_folder(package_name, root_folder='/tmp'):
    target_index = 0
    while True:
        target_folder = join(root_folder, package_name, str(target_index))
        try:
            makedirs(target_folder)
        except OSError:
            target_index += 1
        else:
            break
    return target_folder


def get_package_name(script_path):
    package_name = get_nickname(script_path)
    if 'run' == package_name:
        package_folder = dirname(abspath(script_path))
        package_name = get_nickname(package_folder)
    return package_name
