from django.shortcuts import render

from django.forms import Form
from django_jsonforms.forms import JSONSchemaField, JSONSchemaForm

from tupakweb.forms.data.data_parameter import DataParameterForm

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
    from ..utility.validators import validate_positive_float
    from django.core.validators import MinLengthValidator

    fields_properties = {
        'Name': {
            'type': 'zero-to-pi',
            'placeholder': 'Job Name',
            'initial': None,
            'required': True,
            'validators': [],
        },
        'Description': {
            'type': 'text-area',
            'placeholder': 'write a description about this jobs...',
        },
    }

    dynamic_form = DynamicForm(name='testform', fields_properties=fields_properties)

    data_param_form = DataParameterForm()

    # start_form = StartJobForm()

    # json_form = JSONTestForm()

    if request.method == 'POST':
        # start_form = StartJobForm(request.POST, request=request)
        print(request.POST.get('detector_choice'))
        data_param_form = DataParameterForm(request.POST, request=request)
        # dynamic_form = DynamicForm(request.POST, name='testform', fields_properties=fields_properties, request=request,)
        if data_param_form.is_valid():
            data = data_param_form.cleaned_data
            print(data)

    return render(
        request,
        'tupakweb/about.html',
        {
            'start_form': data_param_form,
        }
    )
