from django import template
from ..utility.display_names import DISPLAY_NAME_MAP


register = template.Library()


@register.filter(name='uniform')
def uniform(value):
    index = value.rfind('_')
    return 'div-' + value[:(index+1)] + 'uniform'


@register.filter(name='display_name')
def display_name(value):
    return DISPLAY_NAME_MAP.get(value, value)
