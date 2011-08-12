import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup (
    name='ploufseo',
    version='0.0.4',
    description='A command-line tool to get some informations about websites',
    author='Felix Delval',
    author_email='felixdelval@gmail.com',
    license = 'GPLv3',
    packages=['plouflib'],
    scripts=['bin/ploufseo'],
    long_description = read('README'),
    install_requires=['lxml','BeautifulSoup','progressbar'],
    url='http://www.bitbucket/felixdelval/pyseo',
)
