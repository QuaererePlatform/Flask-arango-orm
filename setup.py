#!/usr/bin/env python
"""Setup for Flask-arango-orm
"""

from setuptools import find_packages, setup

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
    'mock;python_version<"3.3"', ]


def readme():
    with open('README.rst') as fh:
        return fh.read()


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
              'source_dir': ('setup.py', 'docs')}})
