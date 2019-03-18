#!/usr/bin/env python
"""Setup for the columbia micro-service, part of the Quaerere Platform
"""

from setuptools import find_packages, setup

PROJECT_NAME = 'Flask-arango-orm'
PROJECT_VERSION = '0.0.0a0.dev0'
PROJECT_RELEASE = '.'.join(PROJECT_VERSION.split('.')[:2])
INSTALL_REQUIRES = [
    'arango-orm',
    'Flask', ]
SETUP_REQUIRES = [
    'setuptools', ]


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name=PROJECT_NAME,
      version=PROJECT_VERSION,
      description='Flask wrapper for arango-orm',
      long_description=readme(),
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python :: 3.6', ],
      author="Caitlyn O'Hanna",
      author_email='caitlyn.ohanna@virtualxistenz.com',
      url='https://github.com/QuaererePlatform/Flask-arango-orm',
      packages=find_packages(exclude=['docs', 'tests']),
      zip_safe=False,
      test_suite='tests',
      python_requires='~=3.6',
      install_requires=INSTALL_REQUIRES,
      setup_requires=SETUP_REQUIRES, )
