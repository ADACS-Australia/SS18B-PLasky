from django import forms

from .field import (
    get_text_input,
    get_text_area_input,
    get_select_input,
    get_radio_input,
    get_positive_integer_input,
    get_multiple_choices_input,
    get_positive_float_input,
    get_zero_to_pi_input,
    get_zero_to_2pi_input,
    get_float_input,
    POSITIVE_INTEGER,
    FLOAT,
    POSITIVE_FLOAT,
    MULTIPLE_CHOICES,
    ZERO_TO_PI,
    ZERO_TO_2PI,
    TEXT,
    TEXT_AREA,
    SELECT,
    RADIO,
)


class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # name of the form
        self.name = kwargs.pop('name', None)
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
                    validators=properties.get('validators', ()),
                )

            elif properties.get('type') == TEXT_AREA:
                self.fields[name] = get_text_area_input(
                    label=properties.get('label', name),
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                )

            elif properties.get('type') == POSITIVE_FLOAT:
                self.fields[name] = get_positive_float_input(
                    label=properties.get('label', name),
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                    validators=properties.get('validators', ()),
                )

            elif properties.get('type') == ZERO_TO_PI:
                self.fields[name] = get_zero_to_pi_input(
                    label=properties.get('label', name),
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                    validators=properties.get('validators', ()),
                )

            elif properties.get('type') == ZERO_TO_2PI:
                self.fields[name] = get_zero_to_2pi_input(
                    label=properties.get('label', name),
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                    validators=properties.get('validators', ()),
                )

            elif properties.get('type') == POSITIVE_INTEGER:
                self.fields[name] = get_positive_integer_input(
                    label=properties.get('label', name),
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                    validators=properties.get('validators', ()),
                )

            elif properties.get('type') == FLOAT:
                self.fields[name] = get_float_input(
                    label=properties.get('label', name),
                    placeholder=properties.get('placeholder', None),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                    validators=properties.get('validators', ()),
                )

            elif properties.get('type') == SELECT:
                self.fields[name] = get_select_input(
                    label=properties.get('label', name),
                    initial=properties.get('initial', None),
                    # required=properties.get('required', False),
                    # validators=properties.get('validators', ()),
                    choices=properties.get('choices'),
                )

            elif properties.get('type') == MULTIPLE_CHOICES:
                self.fields[name] = get_multiple_choices_input(
                    label=properties.get('label', name),
                    initial=properties.get('initial', None),
                    required=properties.get('required', False),
                    # validators=properties.get('validators', ()),
                    choices=properties.get('choices'),
                )
