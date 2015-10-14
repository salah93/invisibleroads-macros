from pytest import raises

from invisibleroads_macros.exceptions import BadCommitHash, BadRepositoryURL
from invisibleroads_macros.repository import (
    parse_github_url, validate_github_commit_hash)


class TestParseGithubURL(object):

    def test_valid_urls(self):
        urls = [
            'https://github.com/abc/xyz.git',
            'https://github.com/abc/xyz',
            'https://github.com/abc-def/uvw-xyz',
            'git@github.com:abc/xyz.git',
            'git@github.com:abc/xyz',
            'git@github.com:abc-def/uvw-xyz',
        ]
        for url in urls:
            parse_github_url(url)

    def test_invalid_urls(self):
        urls = [
            'https://github.com/a;bc/xyz.git',
            'https://github.com/abc/x;yz.git',
            'https://github.com/a bc/xyz.git',
            'https://github.com/abc/x yz.git',
        ]
        for url in urls:
            with raises(BadRepositoryURL):
                parse_github_url(url)


class TestValidateCommitHash(object):

    def test_valid_commit_hashes(self):
        commit_hashes = [
            'f62921979e93007e27bf31e00b723576ab77097c',
            'ee27b30cdae419d1dbd3a6b54a7d8bf7fb51f03e',
            'bbcd52a1f7a817ccab03f0c13fc123bb2c53bb58',
            'c38c653958cf6e23161db3518d66bf1f7ff2771c',
            'cbc8cbe9cf203da62ea95dc8463d38d01e03b468',
        ]
        for commit_hash in commit_hashes:
            validate_github_commit_hash(commit_hash)

    def test_invalid_commit_hashes(self):
        commit_hashes = [
            'f62921979e93007e27b;31e00b723576ab77097c',
            'ee27b30cdae419d1dbd|a6b54a7d8bf7fb51f03e',
            'bbcd52a1f7a817ccab0&f0c13fc123bb2c53bb58',
            'c38c653958cf6e23161<b3518d66bf1f7ff2771c',
            'cbc8cbe9cf203da62ea>5dc8463d38d01e03b468',
        ]
        for commit_hash in commit_hashes:
            with raises(BadCommitHash):
                validate_github_commit_hash(commit_hash)
