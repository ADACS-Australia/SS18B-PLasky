import ast
from collections import OrderedDict

from django import forms

from ...utility.display_names import SIMULATED_DATA
from ..dynamic import field
from ...models import DataParameter, Data
from ..dynamic.form import DynamicForm
from ...utility.display_names import (
    DETECTOR_CHOICE,
    DETECTOR_CHOICE_DISPLAY,
    SIGNAL_DURATION,
    SIGNAL_DURATION_DISPLAY,
    SAMPLING_FREQUENCY,
    SAMPLING_FREQUENCY_DISPLAY,
    START_TIME,
    START_TIME_DISPLAY,
    HANFORD,
    HANFORD_DISPLAY,
    LIVINGSTON,
    LIVINGSTON_DISPLAY,
    VIRGO,
    VIRGO_DISPLAY,
)

DETECTOR_CHOICES = [
    (HANFORD, HANFORD_DISPLAY),
    (LIVINGSTON, LIVINGSTON_DISPLAY),
    (VIRGO, VIRGO_DISPLAY),
]


DATA_FIELDS_PROPERTIES = OrderedDict([
    (DETECTOR_CHOICE, {
        'type': field.MULTIPLE_CHOICES,
        'label': DETECTOR_CHOICE_DISPLAY,
        'initial': None,
        'required': True,
        'choices': DETECTOR_CHOICES,
    }),
    (SIGNAL_DURATION, {
        'type': field.POSITIVE_INTEGER,
        'label': SIGNAL_DURATION_DISPLAY,
        'placeholder': '2',
        'initial': None,
        'required': True,
    }),
    (SAMPLING_FREQUENCY, {
        'type': field.POSITIVE_INTEGER,
        'label': SAMPLING_FREQUENCY_DISPLAY,
        'placeholder': '2',
        'initial': None,
        'required': True,
    }),
    (START_TIME, {
        'type': field.POSITIVE_FLOAT,
        'label': START_TIME_DISPLAY,
        'placeholder': '2.1',
        'initial': None,
        'required': True,
    }),
])


class SimulatedDataParameterForm(DynamicForm):

    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'data-parameter'
        kwargs['fields_properties'] = DATA_FIELDS_PROPERTIES
        self.job = kwargs.pop('job', None)

        super(SimulatedDataParameterForm, self).__init__(*args, **kwargs)

    def save(self):
        # find the data first
        data = Data.objects.get(job=self.job)
        for name, value in self.cleaned_data.items():
            DataParameter.objects.update_or_create(
                data=data,
                name=name,
                defaults={
                    'value': value,
                }
            )

    def update_from_database(self, job):
        if not job:
            return
        else:
            try:
                data = Data.objects.get(job=job)
                if data.data_choice != SIMULATED_DATA:
                    return
            except Data.DoesNotExist:
                return

        for name in DATA_FIELDS_PROPERTIES.keys():
            try:
                value = DataParameter.objects.get(data=data, name=name).value
                self.fields[name].initial = ast.literal_eval(value) if name == 'detector_choice' else value
            except DataParameter.DoesNotExist:
                continue
