#!/usr/bin/env python

# Setup script for the `wsgi_statsd' package.
#
# Author: Wouter Lansu <wouter.lansu@paylogic.eu>
# Last Change: January, 6, 2015

import os
import re
import setuptools

# External dependencies.
install_requires = [
    'statsd >= 3.0.1',
]


def get_contents(filename):
    """Get the contents of a file relative to the source distribution directory."""
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root, filename)) as handle:
        return handle.read()


def get_version(filename):
    """Extract the version number from a Python module."""
    contents = get_contents(filename)
    metadata = dict(re.findall('__([a-z]+)__ = [\'"]([^\'"]+)', contents))
    return metadata['version']


setuptools.setup(
    name='wsgi_statsd',
    version=get_version('wsgi_statsd/__init__.py'),
    description="WSGI middleware for stasd integration",
    long_description=get_contents('README.rst'),
    url='https://wsgi_statsd.readthedocs.org/en/latest/',
    author='Wouter Lansu',
    author_email='wouter.lansu@paylogic.eu',
    packages=setuptools.find_packages(),
    entry_points=dict(console_scripts=['wsgi_statsd = wsgi_statsd:main']),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    ])
