import re


WHITESPACE_PATTERN = re.compile(r'\s+', re.MULTILINE)


def parse_words(x):
    return x.replace(',', ' ').split()


def strip_whitespace(string):
    return WHITESPACE_PATTERN.sub('', string)


def compact_whitespace(string):
    return WHITESPACE_PATTERN.sub(' ', string).strip()
