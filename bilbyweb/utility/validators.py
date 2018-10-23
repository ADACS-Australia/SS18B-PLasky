"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import math
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_positive_float(value):
    """
    Validates a value whether it is a positive floating number
    :param value: value to validate
    :return: Nothing
    """
    try:
        float_val = float(value)
        if float_val <= 0.0:
            raise ValidationError(_("Must be greater than 0"))
    except ValueError:
        raise ValidationError(_("Must be a float number"))


def validate_positive_integer(value):
    """
    Validates a value whether it is a positive integer number
    :param value: value to validate
    :return: Nothing
    """
    try:
        int_val = int(value)
        if int_val <= 0 or int_val != value:
            raise ValidationError(_("Must be greater than 0 and whole number"))
    except ValueError:
        raise ValidationError(_("Must be a number"))


def validate_less_than_equal_hundred(value):
    """
    Validates a value whether it is a floating number that is less than or equal to 100.0
    :param value: value to validate
    :return: Nothing
    """
    try:
        float_val = float(value)
        if float_val > 100.0:
            raise ValidationError(_("Must not be greater than 100"))
    except ValueError:
        raise ValidationError(_("Must be a float number"))


def validate_less_than_pi(value):
    """
    Validates a value whether it is a floating number that is less than or equal to pi (math.pi)
    :param value: value to validate
    :return: Nothing
    """
    try:
        float_val = float(value)
        if float_val > math.pi:
            raise ValidationError(_("Must be less than pi"))
    except ValueError:
        raise ValidationError(_("Must be a float number"))


def validate_less_than_2pi(value):
    """
    Validates a value whether it is a floating number that is less than or equal to 2pi (2 * math.pi)
    :param value: value to validate
    :return: Nothing
    """
    try:
        float_val = float(value)
        if float_val > math.pi * 2:
            raise ValidationError(_("Must be less than 2*pi"))
    except ValueError:
        raise ValidationError(_("Must be a float number"))
