import re
from os.path import expanduser


def format_nested_dictionary(d, format_by_suffix=None, prefix=''):
    parts = []
    for key in sorted(d):
        left_hand_side = prefix + str(key)
        value = d[key]
        if isinstance(value, dict):
            parts.append(format_nested_dictionary(value, left_hand_side + '.'))
            continue
        for suffix, format_value in (format_by_suffix or {}).iteritems():
            if key.endswith(suffix):
                parts.append(left_hand_side + ' = ' + format_value(value))
                break
        else:
            if isinstance(value, basestring) and '\n' in value:
                text = format_indented_block(value)
                parts.append(left_hand_side + ' = ' + text)
            else:
                parts.append(left_hand_side + ' = ' + str(value))
    return '\n'.join(parts)


def format_path(x):
    return re.sub(r'^' + expanduser('~'), '~', x)


def format_hanging_indent(x):
    lines = x.strip().splitlines()
    if not lines:
        return ''
    if len(lines) == 1:
        return lines[0]
    return lines[0] + '\n' + '\n'.join('  ' + line for line in lines[1:])


def format_indented_block(x):
    return '\n' + '\n'.join('  ' + line for line in x.strip().splitlines())
