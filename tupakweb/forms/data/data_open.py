from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, DataOpen

FIELDS = ['detector_choice',
          'signal_duration',
          'sample_frequency',
          'start_time', ]

WIDGETS = {
    'detector_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
    'signal_duration': forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '4',
        },
    ),
    'sample_frequency': forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '2048',
        },
    ),
    'start_time': forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '0.0',
        },
    ),
}

LABELS = {
    'detector_choice': _('Detector choice'),
    'signal_duration': _('Signal duration(s)'),
    'sample_frequency': _('Sampling frequency(Hz)'),
    'start_time': _('Start time'),
}


class DataOpenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job = kwargs.pop('job', None)
        super(DataOpenForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataOpen
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        DataOpen.objects.update_or_create(
            job=self.job,
            defaults={
                'detector_choice': data.get('detector_choice'),
                'signal_duration': data.get('signal_duration'),
                'sample_frequency': data.get('sample_frequency'),
                'start_time': data.get('start_time'),
            }
        )
