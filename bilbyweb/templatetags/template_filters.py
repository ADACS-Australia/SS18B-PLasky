"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import ast
from django import template

from ..utility.display_names import *


register = template.Library()


@register.filter(name='uniform')
def uniform(value):
    """
    Create uniform div for displaying
    :param value: String of the name
    :return: String containing div name
    """
    index = value.rfind('_')

    return 'div-' + value[:(index+1)] + 'uniform'


@register.filter(name='display_name')
def display_name(value):
    """
    Find and return the display name that corresponds the value
    :param value: String of the name
    :return: Display name or names separated by comma if a list
    """

    # displaying array (for detector choice at this moment)
    try:
        value_list = ast.literal_eval(value)
        display_list = [DISPLAY_NAME_MAP.get(x, x) for x in value_list]
        return ', '.join(display_list)
    except (ValueError, TypeError):
        pass

    return DISPLAY_NAME_MAP.get(value, value)


@register.filter(name='status_color')
def status_color(status):
    """
    Return the status colour for the bootstrap theme
    :param status: String (status name)
    :return: a bootstrap class according to the dictionary mapping
    """
    status_color_map = {
        DRAFT: 'secondary',
        PENDING: 'secondary',
        SUBMITTING: 'primary',
        SUBMITTED: 'primary',
        QUEUED: 'primary',
        IN_PROGRESS: 'primary',
        COMPLETED: 'success',
        CANCELLING: 'dark',
        CANCELLED: 'dark',
        ERROR: 'danger',
        WALL_TIME_EXCEEDED: 'warning',
        OUT_OF_MEMORY: 'warning',
        DELETING: 'muted',
        DELETED: 'muted',
        PUBLIC: 'info',
    }

    return status_color_map.get(status, 'secondary')
