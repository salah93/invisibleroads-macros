import re


def get_github_https_url(github_url):
    user_name, repository_name = parse_github_url(github_url)
    return 'https://github.com/%s/%s' % (user_name, repository_name)


def get_github_ssh_url(github_url):
    user_name, repository_name = parse_github_url(github_url)
    return 'git@github.com:%s/%s.git' % (user_name, repository_name)


def parse_github_url(github_url):
    return re.search(r'([^/:]+)/([^/.]+)(\.git)?$', github_url).groups()[:2]
