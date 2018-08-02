from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, DataSimulated

FIELDS = ['detector_choice',
          'signal_duration',
          'sample_frequency',
          'start_time',]

WIDGETS = {
    'detector_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
    'signal_duration': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
    'sample_frequency': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
    'start_time': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'detector_choice': _('Detector choice'),
    'signal_duration': _('Signal duration (s)'),
    'sample_frequency': _('Signal frequency (Hz)'),
    'start_time': _('Start time'),
}

class DataSimulatedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(DataSimulated, self).__init__(*args, **kwargs)

    class Meta:
        model = DataSimulated
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        result = DataSimulated.objects.update_or_create(
            data=job.data,
            detector_choice=data.get('detector_choice'),
            signal_duration=data.get('signal_duration'),
            sample_frequency=data.get('sample_frequency'),
            start_time=data.get('start_time'),
        )

        self.request.session['data_open'] = self.as_array(data)
