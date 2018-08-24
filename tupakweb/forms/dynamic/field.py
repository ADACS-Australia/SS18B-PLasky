import itertools
from django import forms

from ...utility.validators import (
    validate_positive_float,
    validate_less_than_pi,
    validate_less_than_2pi,
)

# field types
TEXT = 'text'
FLOAT = 'float'
POSITIVE_FLOAT = 'positive-float'
ZERO_TO_PI = 'zero-to-pi'
ZERO_TO_2PI = 'zero-to-2pi'
TEXT_AREA = 'text-area'
SELECT = 'select'
RADIO = 'radio'


class CustomCharField(forms.CharField):

    description = "A custom text field"

    def __init__(self, placeholder=None, **kwargs):

        super(CustomCharField, self).__init__(**kwargs)

        # apply bootstrap theme
        extra_attrs = {
            'class': 'form-control',
            'placeholder': placeholder if placeholder else '',
        }

        self.widget = forms.TextInput()
        self.widget.attrs.update(extra_attrs)


def get_text_input(label, required, placeholder=None, initial=None, validators=()):
    return CustomCharField(
        label=label,
        required=required,
        initial=initial,
        placeholder=placeholder,
        validators=validators,
    )


class CustomFloatField(forms.FloatField):

    description = "A custom text field"

    def __init__(self, placeholder=None, **kwargs):

        super(CustomFloatField, self).__init__(**kwargs)

        # apply bootstrap theme
        extra_attrs = {
            'class': 'form-control',
            'placeholder': placeholder if placeholder else '',
        }

        self.widget = forms.TextInput()
        self.widget.attrs.update(extra_attrs)


def get_float_input(label, required, placeholder=None, initial=None, validators=()):

    return CustomFloatField(
        label=label,
        required=required,
        initial=initial,
        placeholder=placeholder,
        validators=validators,
    )


def get_positive_float_input(label, required, placeholder=None, initial=None, validators=()):
    default_validators = [validate_positive_float, ]

    return CustomFloatField(
        label=label,
        required=required,
        initial=initial,
        placeholder=placeholder,
        validators=list(itertools.chain(default_validators, validators)),
    )


def get_zero_to_pi_input(label, required, placeholder=None, initial=None, validators=()):
    default_validators = [validate_positive_float, validate_less_than_pi, ]

    return CustomFloatField(
        label=label,
        required=required,
        initial=initial,
        placeholder=placeholder,
        validators=list(itertools.chain(default_validators, validators)),
    )


def get_zero_to_2pi_input(label, required, placeholder=None, initial=None, validators=()):
    default_validators = [validate_positive_float, validate_less_than_2pi, ]

    return CustomFloatField(
        label=label,
        required=required,
        initial=initial,
        placeholder=placeholder,
        validators=list(itertools.chain(default_validators, validators)),
    )


class CustomTextAreaField(forms.CharField):

    description = "A custom text-area field"

    def __init__(self, placeholder=None, **kwargs):

        super(CustomTextAreaField, self).__init__(**kwargs)

        # apply bootstrap theme
        extra_attrs = {
            'class': 'form-control',
            'placeholder': placeholder if placeholder else '',
        }

        self.widget = forms.Textarea()
        self.widget.attrs.update(extra_attrs)


def get_text_area_input(label, required, placeholder=None, initial=None):
    return CustomTextAreaField(
        label=label,
        placeholder=placeholder,
        required=required,
        initial=initial,
    )


def get_radio_input(label, choices=None, initial=None):
    # if not choices:
    #     # choices = DEFAULT_CHOICES
    #     # initial = DEFAULT_INITIAL

    return forms.ChoiceField(
        label=label,
        widget=forms.RadioSelect,
        choices=choices,
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
    # if not choices:
    #     choices = DEFAULT_CHOICES
    #     initial = DEFAULT_INITIAL

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
