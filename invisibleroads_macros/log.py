import re
from os import getcwd
from os.path import expanduser, relpath


def format_nested_dictionary(d, prefix=''):
    lines = []
    for key in sorted(d):
        left_hand_side = prefix + str(key)
        value = d[key]
        if isinstance(value, dict):
            lines.append(format_nested_dictionary(value, left_hand_side + '.'))
        elif isinstance(value, basestring) and '\n' in value:
            lines.append(left_hand_side + ' = ')
            for line in value.splitlines():
                lines.append('  ' + line)
        else:
            lines.append(left_hand_side + ' = ' + str(value))
    return '\n'.join(lines)


def format_relative_path(path):
    relative_path = relpath(path, getcwd())
    return format_path(relative_path)


def format_path(path):
    return re.sub(r'^' + expanduser('~'), '~', path)
