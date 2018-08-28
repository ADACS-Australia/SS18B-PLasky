import ast
from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..dynamic import field
from ...models import Job, DataParameter, Data
from ..dynamic.form import DynamicForm


HANFORD = 'hanford'
LIVINGSTON = 'livingston'
VIRGO = 'virgo'

DETECTOR_CHOICES = [
    (HANFORD, 'Hanford'),
    (LIVINGSTON, 'Livingston'),
    (VIRGO, 'Virgo'),
]

detectors = forms.MultipleChoiceField(choices=DETECTOR_CHOICES)


DATA_FIELDS_PROPERTIES = OrderedDict([
    ('detector_choice', {
        'type': field.MULTIPLE_CHOICES,
        'label': 'Detector choice',
        'initial': None,
        'required': True,
        'choices': DETECTOR_CHOICES,
    }),
    ('signal_duration', {
        'type': field.POSITIVE_FLOAT,
        'label': 'Signal duration (s)',
        'placeholder': '2',
        'initial': None,
        'required': True,
    }),
    ('sampling_frequency', {
        'type': field.POSITIVE_FLOAT,
        'label': 'Sampling frequency (Hz)',
        'placeholder': '2',
        'initial': None,
        'required': True,
    }),
    ('start_time', {
        'type': field.POSITIVE_FLOAT,
        'label': 'Start time',
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
            data = Data.objects.get(job=job)
            if data.data_choice != Data.SIMULATED_DATA:
                return

        for name in DATA_FIELDS_PROPERTIES.keys():
            try:
                value = DataParameter.objects.get(data=data, name=name).value
                self.fields[name].initial = ast.literal_eval(value) if name == 'detector_choice' else value
            except DataParameter.DoesNotExist:
                continue
