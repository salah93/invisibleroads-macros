def merge_dictionaries(*ds):
    'http://stackoverflow.com/a/26853961'
    x = {}
    for d in ds:
        x.update(d)
    return x
