def print_nested_dictionary(d, prefix=''):
    for key in sorted(d):
        left_hand_side = prefix + str(key)
        value = d[key]
        if isinstance(value, dict):
            print_nested_dictionary(value, left_hand_side + '.')
        elif isinstance(value, basestring) and '\n' in value:
            print(left_hand_side + ' = ')
            for line in value.splitlines():
                print '  ' + line
        else:
            print(left_hand_side + ' = ' + str(value))
    return d
