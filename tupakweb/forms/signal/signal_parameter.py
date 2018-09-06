"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from collections import OrderedDict

from ..dynamic.form import DynamicForm
from ..dynamic import field
from ...models import SignalParameter, Signal
from ...utility.display_names import (
    MASS1,
    MASS1_DISPLAY,
    MASS2,
    MASS2_DISPLAY,
    LUMINOSITY_DISTANCE,
    LUMINOSITY_DISTANCE_DISPLAY,
    IOTA,
    IOTA_DISPLAY,
    PSI,
    PSI_DISPLAY,
    PHASE,
    PHASE_DISPLAY,
    MERGER_TIME,
    MERGER_TIME_DISPLAY,
    RA,
    RA_DISPLAY,
    DEC,
    DEC_DISPLAY,
)

BBH_FIELDS_PROPERTIES = OrderedDict([
    (MASS1, {
        'type': field.POSITIVE_FLOAT,
        'label': MASS1_DISPLAY,
        'placeholder': '2.0',
        'initial': None,
        'required': True,
    }),
    (MASS2, {
        'type': field.POSITIVE_FLOAT,
        'label': MASS2_DISPLAY,
        'placeholder': '1.0',
        'initial': None,
        'required': True,
    }),
    (LUMINOSITY_DISTANCE, {
        'type': field.POSITIVE_FLOAT,
        'label': LUMINOSITY_DISTANCE_DISPLAY,
        'placeholder': '2000',
        'initial': None,
        'required': True,
    }),
    (IOTA, {
        'type': field.ZERO_TO_PI,
        'label': IOTA_DISPLAY,
        'placeholder': '0.4',
        'initial': None,
        'required': True,
    }),
    (PSI, {
        'type': field.ZERO_TO_2PI,
        'label': PSI_DISPLAY,
        'placeholder': '2.659',
        'initial': None,
        'required': True,
    }),
    (PHASE, {
        'type': field.ZERO_TO_2PI,
        'label': PHASE_DISPLAY,
        'placeholder': '1.3',
        'initial': None,
        'required': True,
    }),
    (MERGER_TIME, {
        'type': field.POSITIVE_FLOAT,
        'label': MERGER_TIME_DISPLAY,
        'placeholder': '1126259642.413',
        'initial': None,
        'required': True,
    }),
    (RA, {
        'type': field.POSITIVE_FLOAT,
        'label': RA_DISPLAY,
        'placeholder': '1.375',
        'initial': None,
        'required': True,
    }),
    (DEC, {
        'type': field.FLOAT,
        'label': DEC_DISPLAY,
        'placeholder': '-1.2108',
        'initial': None,
        'required': True,
    }),
])


class SignalParameterBbhForm(DynamicForm):
    """Class to represent a SignalBbhParameter. It can be any of the following types:
    """

    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'signal-binary_black_hole'
        kwargs['fields_properties'] = BBH_FIELDS_PROPERTIES
        self.job = kwargs.pop('job', None)
        super(SignalParameterBbhForm, self).__init__(*args, **kwargs)

    def save(self):
        # find the signal first
        signal = Signal.objects.get(job=self.job)
        for name, value in self.cleaned_data.items():
            SignalParameter.objects.update_or_create(
                signal=signal,
                name=name,
                defaults={
                    'value': value,
                }
            )

    def update_from_database(self, job):
        if not job:
            return

        for name in BBH_FIELDS_PROPERTIES.keys():
            try:
                value = SignalParameter.objects.get(signal__job=job, name=name).value
                self.fields[name].initial = value
            except SignalParameter.DoesNotExist:
                continue
