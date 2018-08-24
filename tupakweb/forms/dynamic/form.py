from django import forms
from .field import (
    get_text_input,
    get_text_area_input,
    get_select_input,
    get_radio_input,
    get_number_input,
)

TEXT = 'text'
TEXT_AREA = 'text-area'
SELECT = 'select'
RADIO = 'radio'


class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # name of the form
        self.name = kwargs.pop('name')
        # dictionary of fields, each containing field_name as key, field_type, placeholder, choices etc. as values
        self.fields_properties = kwargs.pop('fields_properties')

        # request might be needed
        self.request = kwargs.pop('request', None)

        super(DynamicForm, self).__init__(*args, **kwargs)

        for name, properties in self.fields_properties.items():

            if properties.get('type') == TEXT:
                self.fields[name] = get_text_input(
                    label=properties.get('label', name),
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                )

            elif properties.get('type') == TEXT_AREA:
                self.fields[name] = get_text_area_input(
                    label=properties.get('label', name),
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                )
