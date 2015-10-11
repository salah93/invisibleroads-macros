import re
from os import getcwd

from .disk import cd
from .exceptions import BadCommitHash, BadRepository, BadRepositoryURL, BadURL
from .shell import run_command


GITHUB_URL_PATTERN = re.compile(
    r'github.com[/:]([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)(?:\.git)?$')


def download_github_repository(target_folder, github_url):
    github_url = get_github_ssh_url(github_url)
    run_git(['git', 'clone', github_url, target_folder])
    return get_repository_commit_hash(target_folder)


def update_github_repository(target_folder):
    run_git('git fetch', target_folder)
    return get_repository_commit_hash(target_folder)


def get_repository_url(folder=None):
    github_url = run_git('git config --get remote.origin.url', folder)
    return get_github_https_url(github_url)


def get_repository_commit_hash(folder=None):
    return run_git('git rev-parse HEAD', folder)


def get_repository_folder(folder=None):
    return run_git('git rev-parse --show-toplevel', folder)


def get_github_ssh_url(github_url):
    user_name, repository_name = parse_github_url(github_url)
    return 'git@github.com:%s/%s.git' % (user_name, repository_name)


def get_github_https_url(github_url):
    user_name, repository_name = parse_github_url(github_url)
    return 'https://github.com/%s/%s' % (user_name, repository_name)


def parse_github_url(github_url):
    try:
        return GITHUB_URL_PATTERN.search(github_url).groups()
    except AttributeError:
        m = 'Could not parse as GitHub URL (github_url = %s)'
        raise BadRepositoryURL(m % github_url)


def run_git(command_args, folder=None, exception_by_error=None):
    if not folder:
        folder = getcwd()
    exception_by_error = dict({
        'Could not read': BadURL,
        'Not a git repository': BadRepository,
        'not found': BadURL,
        'not a tree object': BadCommitHash,
        'Not a valid object name': BadCommitHash,
    }, **(exception_by_error or {}))
    with cd(folder):
        output = run_command(command_args, exception_by_error)
    return output


def validate_commit_hash(commit_hash):
    # Screen for non-alphanumeric characters
    match = re.search(r'[^a-zA-Z0-9]+', commit_hash)
    if match:
        raise BadCommitHash
    return commit_hash
