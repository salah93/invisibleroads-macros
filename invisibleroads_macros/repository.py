import re
from os import getcwd
from os.path import exists

from .disk import cd
from .exceptions import BadURL, BadRepositoryURL, BadRepository
from .shell import run_command


def download_github_repository(target_folder, github_url):
    if not exists(target_folder):
        m = 'Could not access repository (github_url = %s)'
        run_command([
            'git', 'clone', get_github_ssh_url(github_url), target_folder,
        ], exception_by_error={
            'not found': BadURL(m % github_url)
        })
    run_git('git fetch', target_folder)
    return get_repository_commit_hash(target_folder)


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
        return re.search(
            r'([^/:]+)/([^/.]+)(\.git)?$', github_url).groups()[:2]
    except AttributeError:
        m = 'Could not parse as GitHub URL (github_url = %s)'
        raise BadRepositoryURL(m % github_url)


def run_git(command_args, folder=None, exception_by_error=None):
    if not folder:
        folder = getcwd()
    exception_by_error = dict({
        'Not a git repository': BadRepository(
            'Not a git repository (folder = %s)' % folder),
    }, **(exception_by_error or {}))
    with cd(folder):
        output = run_command(command_args, exception_by_error)
    return output
