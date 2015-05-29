import re


PATTERN_WHITESPACE = re.compile(r'\s+')


def parse_words(x):
    return x.replace(',', ' ').split()


def strip_whitespace(string):
    return PATTERN_WHITESPACE.sub('', string)
