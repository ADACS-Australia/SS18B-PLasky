import math
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_positive_float(value):
    try:
        float_val = float(value)
        if float_val <= 0.0:
            raise ValidationError(_("Must be greater than 0"))
    except ValueError:
        raise ValidationError(_("Must be a float number"))


def validate_less_than_pi(value):
    try:
        float_val = float(value)
        if float_val > math.pi:
            raise ValidationError(_("Must be less than pi"))
    except ValueError:
        raise ValidationError(_("Must be a float number"))


def validate_less_than_2pi(value):
    try:
        float_val = float(value)
        if float_val > math.pi * 2:
            raise ValidationError(_("Must be less than 2*pi"))
    except ValueError:
        raise ValidationError(_("Must be a float number"))
