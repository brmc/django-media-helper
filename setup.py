#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2014 Brian McClure
#
#  django-media-helper is free software under terms of the MIT License.
#
# Fork of django-cleanup

from setuptools import setup, find_packages


setup(
    name     = 'django-media-helper',
    version  = '0.2.1.2',
    packages = find_packages(),
    include_package_data=True,
    requires = ['python (>= 2.7)', 'django (>= 1.6)', 'Pillow (>= 2.1.0)'],
    description  = 'A image resizing and management app for Django',
    long_description = open('README.markdown').read(),
    author       = 'Brian McClure',
    author_email = 'brian.mcclr@gmail.com',
    url          = 'https://github.com/brmc/django-media-helper',
    download_url = 'https://github.com/brmc/django-media-helper.git',
    license      = 'MIT License',
    keywords     = 'django, imaging, ajax',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
