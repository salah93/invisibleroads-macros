import re
import subprocess
from os.path import exists

from .disk import cd
from .exceptions import BadURL, BadRepository, InvisibleRoadsError


def get_github_repository(target_folder, github_url):
    if not exists(target_folder):
        try:
            subprocess.check_output([
                'git', 'clone', get_github_ssh_url(github_url), target_folder,
            ], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            o = e.output.lower()
            if 'not found' in o:
                m = 'Could not access repository (github_url = %s)'
                raise BadURL(m % github_url)
            raise InvisibleRoadsError(e.output)
    with cd(target_folder):
        try:
            subprocess.check_output(['git', 'fetch'], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            o = e.output.lower()
            if 'not a git repository' in o:
                m = 'Could not update repository (target_folder = %s)'
                raise BadRepository(m % target_folder)
            raise InvisibleRoadsError(e.output)


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
        raise BadURL(m % github_url)
