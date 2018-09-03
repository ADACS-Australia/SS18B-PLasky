"""
Source: https://www.djangosnippets.org/snippets/1019/

Adapted by DV.

Syntax: {% get_fieldset list,of,fields as new_form_object from original_form %}

note: list,of,fields doesn't allow spaces before/after comma.

Example:

{% load fieldsets %}
...
<fieldset id="contact_details">
    <legend>Contact details</legend>
    <ul>
{% get_fieldset first_name,last_name,email,cell_phone as personal_fields from form %}
{{ personal_fields.as_ul }}
    </ul>
</fieldset>

<fieldset>
    <legend>Address details</legend>
    <ul>
{% get_fieldset street_address,post_code,city as address_fields from form %}
{{ address_fields.as_ul }}
    </ul>
</fieldset>
"""


import copy

from django import template
from collections import OrderedDict

register = template.Library()


@register.filter(name='uniform')
def uniform(value):
    index = value.rfind('_')
    return 'div-' + value[:(index+1)] + 'uniform'


def get_fieldset(parser, token):
    try:
        args = token.split_contents()
        name = args[0]
        fields = args[1]
        as_ = args[2]
        variable_name = args[3]
        from_ = args[4]
        form = args[5]
        # name, fields, as_, variable_name, from_, form = args
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r' % token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form)


get_fieldset = register.tag(get_fieldset)


class FieldSetNode(template.Node):
    def __init__(self, fields, variable_name, form_variable):
        self.fields = fields
        self.variable_name = variable_name
        self.form_variable = form_variable

    def render(self, context):
        form = template.Variable(self.form_variable).resolve(context)
        new_form = copy.copy(form)
        try:
            new_form.fields = OrderedDict(((key, value) for key, value in form.fields.items() if key in self.fields))
            context[self.variable_name] = new_form
        except:
            pass

        return u''
