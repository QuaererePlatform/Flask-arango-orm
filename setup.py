#!/usr/bin/env python
"""Setup for Flask-arango-orm
"""

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

PROJECT_NAME = 'Flask-arango-orm'
PROJECT_RELEASE = '0.1.0'
PROJECT_VERSION = '.'.join(PROJECT_RELEASE.split('.')[:2])
INSTALL_REQUIRES = [
    'arango-orm>=0.5.3',
    'Flask>=1.0.0', ]
SETUP_REQUIRES = [
    'setuptools',
    'pytest-runner',
    'Sphinx>=1.8.0',
    'sphinx_rtd_theme', ]
TESTS_REQUIRES = [
    'pytest>=4.3.0',
    'pytest-cov',
    'pytest-flake8',
    'mock;python_version<"3.3"', ]


def readme():
    with open('README.rst') as fh:
        return fh.read()


# Taken from https://circleci.com/blog/continuously-deploying-python-\
# packages-to-pypi-with-circleci/
class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != PROJECT_RELEASE:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, PROJECT_RELEASE
            )
            sys.exit(info)


class WriteRequirementsCommand(install):
    """Writes all package requirements into requirements.txt"""
    description = 'creates requirements.txt'

    def run(self):
        header = '# Generated file, do not edit\n'
        all_requirements = INSTALL_REQUIRES + SETUP_REQUIRES + TESTS_REQUIRES
        all_requirements = [I + '\n' for I in all_requirements]
        all_requirements.insert(0, header)
        with open('requirements.txt', 'w') as fh:
            fh.writelines(all_requirements)


setup(name=PROJECT_NAME,
      version=PROJECT_RELEASE,
      description='Flask extension for arango-orm',
      license='LGPL-3.0',
      long_description=readme(),
      packages=find_packages(exclude=['docs', 'tests']),
      zip_safe=True,
      test_suite='tests',
      python_requires='~=3.6',
      install_requires=INSTALL_REQUIRES,
      setup_requires=SETUP_REQUIRES,
      tests_require=TESTS_REQUIRES,
      entry_points={
          'distutils.commands': [
              'build_sphinx = sphinx.setup_command:BuildDoc']},
      command_options={
          'build_sphinx': {
              'project': ('setup.py', PROJECT_NAME),
              'version': ('setup.py', PROJECT_VERSION),
              'release': ('setup.py', PROJECT_RELEASE),
              'source_dir': ('setup.py', 'docs'), }, },
      cmdclass={
          'mk_reqs': WriteRequirementsCommand,
          'verify': VerifyVersionCommand, }, )
