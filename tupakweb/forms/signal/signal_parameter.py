"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from ..dynamic.form import DynamicForm
from ..dynamic import field
from ...models import SignalParameter

BBH_FIELDS_PROPERTIES = {
    SignalParameter.MASS1: {
        'type': field.POSITIVE_FLOAT,
        'label': 'Mass 1 (M☉)',
        'placeholder': '2.0',
        'initial': None,
        'required': True,
    },
    SignalParameter.MASS2: {
        'type': field.POSITIVE_FLOAT,
        'label': 'Mass 2 (M☉)',
        'placeholder': '1.0',
        'initial': None,
        'required': True,
    },
    SignalParameter.LUMINOSITY_DISTANCE: {
        'type': field.POSITIVE_FLOAT,
        'label': 'Luminosity distance (Mpc)',
        'placeholder': '2000',
        'initial': None,
        'required': True,
    },
    SignalParameter.IOTA: {
        'type': field.ZERO_TO_PI,
        'label': 'iota',
        'placeholder': '0.4',
        'initial': None,
        'required': True,
    },
    SignalParameter.PSI: {
        'type': field.ZERO_TO_2PI,
        'label': 'psi',
        'placeholder': '2.659',
        'initial': None,
        'required': True,
    },
    SignalParameter.PHASE: {
        'type': field.ZERO_TO_2PI,
        'label': 'phase',
        'placeholder': '1.3',
        'initial': None,
        'required': True,
    },
    SignalParameter.MERGER_TIME: {
        'type': field.POSITIVE_FLOAT,
        'label': 'Merger time (GPS time)',
        'placeholder': '1126259642.413',
        'initial': None,
        'required': True,
    },
    SignalParameter.RA: {
        'type': field.POSITIVE_FLOAT,
        'label': 'Right ascension',
        'placeholder': '1.375',
        'initial': None,
        'required': True,
    },
    SignalParameter.DEC: {
        'type': field.FLOAT,
        'label': 'Declination',
        'placeholder': '-1.2108',
        'initial': None,
        'required': True,
    },
}


class SignalParameterBbhForm(DynamicForm):
    """Class to represent a SignalBbhParameter. It can be any of the following types:
    """

    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'signal-binary_black_hole'
        kwargs['fields_properties'] = BBH_FIELDS_PROPERTIES
        self.job = kwargs.pop('job', None)
        super(SignalParameterBbhForm, self).__init__(*args, **kwargs)
