#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2014 Brian McClure
#
#  django-media-helper is free software under terms of the MIT License.
#
# Fork of django-cleanup

from setuptools import setup, find_packages

description = """# **django-media-helper** #

When dealing with content from unacquainted sources(e.g., clients or designers)
one often gets images with absurd dimensions and/or filesizes: A 3000px-wide
play-button, a 10MB logo, etc.  Media-helper attempts to mitigate this problem
by automating image-resizing, delivering the most appropriately sized image to
the browser.

It is also designed to be dropped into existing projects with minimal effort.
It's still in the alpha stage, but if you're careful it might make your life a
little bit easier while also speeding up your load times and reducing data
transfer."""

setup(
    name     = 'django-media-helper',
    version  = '0.3.1-bugfix',
    packages = find_packages(),
    include_package_data=True,
    requires = ['python (>= 2.7)', 'django (>= 1.6)', 'Pillow (>= 2.1.0)'],
    description  = 'An image resizing and management app for Django',
    long_description = description,
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
