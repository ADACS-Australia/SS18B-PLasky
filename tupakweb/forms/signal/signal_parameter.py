"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from ..dynamic.form import DynamicForm
from ...models import SignalParameter

BBH_FIELDS_PROPERTIES = {
    SignalParameter.MASS1: {
        'type': 'text',
        'label': 'Mass 1 (M☉)',
        'placeholder': '2.0',
        'initial': None,
        'required': True,
    },
    SignalParameter.MASS2: {
        'type': 'text',
        'label': 'Mass 2 (M☉)',
        'placeholder': '1.0',
        'initial': None,
        'required': True,
    },
    SignalParameter.LUMINOSITY_DISTANCE: {
        'type': 'text',
        'label': 'Luminosity distance (Mpc)',
        'placeholder': '2000',
        'initial': None,
        'required': True,
    },
    SignalParameter.IOTA: {
        'type': 'text',
        'label': 'iota',
        'placeholder': '0.4',
        'initial': None,
        'required': True,
    },
    SignalParameter.PSI: {
        'type': 'text',
        'label': 'psi',
        'placeholder': '2.659',
        'initial': None,
        'required': True,
    },
    SignalParameter.PHASE: {
        'type': 'text',
        'label': 'phase',
        'placeholder': '1.3',
        'initial': None,
        'required': True,
    },
    SignalParameter.MERGER_TIME: {
        'type': 'text',
        'label': 'Merger time (GPS time)',
        'placeholder': '1126259642.413',
        'initial': None,
        'required': True,
    },
    SignalParameter.RA: {
        'type': 'text',
        'label': 'Right ascension',
        'placeholder': '1.375',
        'initial': None,
        'required': True,
    },
    SignalParameter.DEC: {
        'type': 'text',
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
        super(SignalParameterBbhForm, self).__init__(*args, **kwargs)
