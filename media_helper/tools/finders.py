#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
import warnings


def find_models_with_field(field_type):
    """Returns a list of models that have the specified field type.

    Arguments:
    :param field_type: the type of field to search for
    :type field_type: a field from django.db.models

    :returns: list of models from installed apps
    """
    result = []
    for model in models.get_models():
        for field in model._meta.fields:
            if isinstance(field, field_type):
                result.append(model)
                break
    return result


def find_upload_dirs(*model_list):
    """Finds all upload_to directories for ImageFields

    Arguments:
    :param model_list: a list of models from installed apps
    :type model_list: a list of models
    :returns: list of upload paths
    """
    warnings.warn(
        "This isn't necessary anymore with the new folder structure, but"
        "it will be left in in case the directory structure turns out to"
        "be a bad idea.  ",
        DeprecationWarning)

    dirs = []
    for model in model_list:
        for field in model._meta.fields:
            if (isinstance(field, models.ImageField)
               and field.upload_to is not '.'):
                    dirs.append(field.upload_to)

    return dirs


def find_field_attribute(attribute, *model_list):
    """ Returns ImageField attributes for a list of models

    So far this is just used to return the upload paths or field names.

    :param attribute: name of the attribute to search for
    :type attribute: str
    :param model_list: a list...of models, imagine that
    :type model_list: see above
    :returns: list
    """

    attributes = []
    for model in model_list:
        for field in model._meta.fields:
            if (isinstance(field, models.ImageField)
               and field.upload_to is not '.'):
                    attributes.append(getattr(field, attribute))

    return attributes
