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
