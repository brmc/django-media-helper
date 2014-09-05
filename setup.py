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
    requires = ['python (>= 2.5)', 'django (>= 1.6)', 'Pillow (>= 2.1.0)'],
    description  = 'A image resizing and management app for Django',
    long_description = open('README.markdown').read(), 
    author       = 'Brian McClure',
    author_email = 'brian.mcclr@gmail.com',
    url          = 'https://bitbucket.org/brmcllr/django_media_helper.git',
    download_url = 'https://github.com/un1t/django-cleanup/tarball/master',
    license      = 'MIT License',
    keywords     = 'django, imaging, ajax',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
