#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Extensible Application DSL for Hoverfly, WSGI and any other backend"


import ast
import os
from setuptools import setup, find_packages


local_file = lambda *f: open(os.path.join(os.path.dirname(__file__), *f)).read()


class VersionFinder(ast.NodeVisitor):
    VARIABLE_NAME = 'version'

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == self.VARIABLE_NAME:
                self.version = node.value.s
        except:
            pass


def read_version():
    finder = VersionFinder()
    finder.visit(ast.parse(local_file('hovercrafty', 'version.py')))
    return finder.version


def read_requirements():
    return local_file('requirements.txt').splitlines()


def read_readme():
    """Read README content.
    If the README.rst file does not exist yet
    (this is the case when not releasing)
    only the short description is returned.
    """
    try:
        return local_file('README.rst')
    except IOError:
        return __doc__


setup(
    author='Gabriel Falcao',
    author_email='gfalcao@newstore.com',
    description=read_version(),
    include_package_data=True,
    install_requires=read_requirements(),
    long_description=read_readme(),
    name='hovercrafty',
    packages=find_packages(exclude=['*tests*']),
    test_suite='nose.collector',
    version=read_version(),
    entry_points={
        'console_scripts': ['hovercrafty = hovercrafty.console:entrypoint'],
    },
    package_data={
        'hovercrafty': ' '.join([
            '*.cfg',
            '*.py',
            '*.rst',
            '*.txt',
        ]),
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    zip_safe=False,
)
