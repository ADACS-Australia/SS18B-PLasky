from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from tupakweb.forms.dynamic import field
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


class DataParameterForm(DynamicForm):

    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'data-parameter'
        kwargs['fields_properties'] = DATA_FIELDS_PROPERTIES
        self.job = kwargs.pop('job', None)

        super(DataParameterForm, self).__init__(*args, **kwargs)


