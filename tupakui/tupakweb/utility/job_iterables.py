from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from collections import OrderedDict
from os.path import basename
from ..utility.constants import *

def model_instance_to_iterable(object, model=START, views=[]):
    """Converts the object returned from a Model query into an iterable object to be used by a template

    Parameters
    ----------
    object:
        object returned from a Model query
    model:
        Model to be considered (using the tabs convention used in job.py)
    views:
        list of views currently active

    Returns
    -------
    object:
        the newly iterable object, or None.
    """
    fields, labels = get_metadata(model, views, object)

    try:
        object.fields = OrderedDict(((field.name, [labels[field.name], field.value_to_string(object)])
                             if 'file' not in field.name else
                                     ((field.name, [labels[field.name], basename(field.value_to_string(object))])
                                      if 'filename' not in field.name else
                                      (field.name, [labels[field.name], field.value_to_string(object)])
                                      )
                                     )
                             for field in object._meta.fields if field.name in fields)

        return object
    except:
        return None

def get_metadata(model, views, object):
    """Get metadata about a model

    (e.g. fields and labels to be displayed by a template.)

    Parameters
    ----------
    model:
        Model to be considered (using the tabs convention used in job_utils.py)
    views:
        list of views currently active
    object:
        object returned from a Model query
    Returns
    -------
    fields, labels
    """
    if model == START:
        fields = ['name', 'description']
        labels = {'name': _('Job name'), 'description': _('Job description')}

    if model == DATA:
        fields = ['data_choice',]
        fields = filter_data_model_fields(fields, object)

        labels = {
            'dmodel_type': _('Type'),
            'method': _('Method'),
            'scale_x': _('Scale X'),
            'scale_y': _('Scale Y'),
            'scale_z': _('Scale Z'),
            'step_x': _('Step X'),
            'step_y': _('Step Y'),
            'step_z': _('Step Z'),
        }

    return fields, labels

def filter_data_model_fields(fields, object):
    pass