import ast
from django import template
from ..utility.display_names import DISPLAY_NAME_MAP


register = template.Library()


@register.filter(name='uniform')
def uniform(value):
    index = value.rfind('_')
    return 'div-' + value[:(index+1)] + 'uniform'


@register.filter(name='display_name')
def display_name(value):
    # displaying array (for detector choice at this moment)
    try:
        value_list = ast.literal_eval(value)
        display_list = [DISPLAY_NAME_MAP.get(x, x) for x in value_list]
        return ', '.join(display_list)
    except (ValueError, TypeError):
        pass

    return DISPLAY_NAME_MAP.get(value, value)
