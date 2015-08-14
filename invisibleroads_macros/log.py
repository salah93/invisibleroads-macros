import re
from os.path import expanduser


def format_nested_dictionary(d, format_by_suffix=None, prefix=''):
    parts = []
    for key in sorted(d):
        left_hand_side = prefix + str(key)
        value = d[key]
        if isinstance(value, dict):
            parts.append(format_nested_dictionary(
                value, format_by_suffix, left_hand_side + '.'))
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


def parse_nested_dictionary(s, parse_by_suffix=None):
    raw_dictionary, key = {}, None
    for line in s.splitlines():
        if line.startswith('  '):
            if key is not None:
                value = line[2:].rstrip()
                raw_dictionary[key].append(value)
            continue
        try:
            key, value = line.split('=', 1)
        except ValueError:
            key = None
        else:
            key = key.strip()
            value = value.strip()
            raw_dictionary[key] = [value]
    d = {}
    for k, v in raw_dictionary.iteritems():
        v = '\n'.join(v).strip()
        for suffix, parse_value in (parse_by_suffix or {}).iteritems():
            if k.endswith(suffix):
                v = parse_value(v)
        _set_nested_value(d, k, v)
    return d


def _set_nested_value(target_dictionary, key_string, value):
    this_dictionary = target_dictionary
    for key in key_string.split('.'):
        key = key.strip()
        last_dictionary = this_dictionary
        try:
            this_dictionary = this_dictionary[key]
        except KeyError:
            this_dictionary[key] = {}
            this_dictionary = this_dictionary[key]
    last_dictionary[key] = value
    return target_dictionary
