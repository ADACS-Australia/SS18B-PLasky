from django.shortcuts import render

from django.forms import Form
from django_jsonforms.forms import JSONSchemaField, JSONSchemaForm


json_schema = {
            'type': 'object',
            'properties': {
                'color': {
                    'description': 'a color',
                    'type': 'string'
                },
                'number': {
                    'description': 'a very nice number',
                    'type': 'integer'
                },
                'list': {
                    'description': 'what a list',
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            }
        }

json_options = {'theme': 'html'}


class JSONTestForm(Form):
    json = JSONSchemaField(
        schema=json_schema,
        options=json_options,
    )


def index(request):
    return render(
        request,
        "tupakweb/welcome.html",
    )


def about(request):
    from ..forms.job import StartJobForm
    from ..forms.dynamic.form import DynamicForm

    fields_properties = {
        'Name': {
            'type': 'text',
            'placeholder': None,
            'initial': None,
            'required': True,
        },
        'Description': {
            'type': 'text-area',
            'placeholder': 'write a description about this job...',
        },
    }

    dynamic_form = DynamicForm(name='testform', fields_properties=fields_properties)

    # start_form = StartJobForm()

    # json_form = JSONTestForm()

    if request.method == 'POST':
        # start_form = StartJobForm(request.POST, request=request)
        dynamic_form = DynamicForm(request.POST, name='testform', fields_properties=fields_properties, request=request,)

    return render(
        request,
        'tupakweb/about.html',
        {
            'start_form': dynamic_form,
        }
    )
