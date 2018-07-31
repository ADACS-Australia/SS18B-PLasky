"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django import forms
from ...models import SignalBbhParameter

# GLOBAL DECLARATIONS
RADIO = 'radio'
SELECT = 'select'
TEXT = 'text'
NUMBER = 'number'
DEFAULT_CHOICES = SignalBbhParameter.NAME_CHOICES
DEFAULT_INITIAL = SignalBbhParameter.MASS1

def get_radio_input(label, choices=None, initial=None):
    if not choices:
        choices = DEFAULT_CHOICES
        initial = DEFAULT_INITIAL

    return forms.ChoiceField(
        label=label,
        widget=forms.RadioSelect,
        choices=choices,
        initial=initial,
    )

def get_text_input(label, placeholder=None, initial=None):
    return forms.CharField(
        label=label,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': placeholder,
            }
        ),
        required=False,
        initial=initial,
    )

def get_number_input(label):
    return forms.CharField(
        label=label,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )

def get_select_input(label, choices=None, initial=None):
    if not choices:
        choices = DEFAULT_CHOICES
        initial = DEFAULT_INITIAL

    return forms.ChoiceField(
        label=label,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        choices=choices,
        initial=initial,

    )

class SignalBbhParameter(forms.Form):
    """Class to represent a SignalBbhParameter. It can be any of the following types:
    1. Radio (Currently in use)
    2. Select
    3. Text (Currently in use)
    4. Number

    """
    field_types = [
        RADIO,
        SELECT,
        TEXT,
        NUMBER,
    ]

    field_type = field_types[2]

    def __init__(self, name, label, choices=None, initial=None, field_type='', placeholder='', *args, **kwargs):
        super(SignalBbhParameter, self).__init__(*args, **kwargs)

        self.field_type = field_type if self.field_types.__contains__(field_type) else self.field_type

        # adding custom fields
        if self.field_type == RADIO:
            self.fields[name] = get_radio_input(
                label=label,
                choices=choices,
                initial=initial
            )
        elif self.field_type == SELECT:
            self.fields[name] = get_select_input(
                label=label,
                choices=choices,
                initial=initial,
            )
        elif self.field_type == TEXT:
            self.fields[name] = get_text_input(
                label=label,
                placeholder=placeholder,
                initial=initial,
            )
        elif self.field_type == NUMBER:
            self.fields[name] = get_number_input(
                label=label,
            )
