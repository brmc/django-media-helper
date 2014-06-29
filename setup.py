#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2014 Brian McClure 
#
#  django-media-helper is free software under terms of the MIT License.
#
# Fork of django-cleanup

import os
from setuptools import setup, find_packages


setup(
    name     = 'django-media-helper',
    version  = '0.1.1',
    packages = find_packages(),
    include_package_data=True,
    requires = ['python (>= 2.5)', 'django (>= 1.3)', 'Pillow (>= 2.1.0)'],
    description  = 'Deletes old files and resizes new ones for different resolutions. A fork of django-cleanup.',
    long_description = open('README.markdown').read(), 
    author       = 'Brian McClure',
    author_email = 'brian.mcclr@gmail.com',
    url          = 'https://github.com/un1t/django-cleanup',
    download_url = 'https://github.com/un1t/django-cleanup/tarball/master',
    license      = 'MIT License',
    keywords     = 'django',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
