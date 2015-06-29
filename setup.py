from os.path import abspath, dirname, join
from setuptools import setup


FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst', 'CHANGES.rst'])
setup(
    name='invisibleroads-macros',
    version='0.1.1',
    description='Shortcut functions',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
    ],
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='http://invisibleroads.com',
    keywords='invisibleroads',
    packages=['invisibleroads_macros'],
    include_package_data=True,
    zip_safe=False)
