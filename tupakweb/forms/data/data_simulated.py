from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, DataSimulated

FIELDS = [
    'detector_choice',
    'signal_duration',
    'sample_frequency',
    'start_time',
]

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
        self.job = kwargs.pop('job', None)
        super(DataSimulatedForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataSimulated
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        result = DataSimulated.objects.create(
            job=self.job,
            detector_choice=data.get('detector_choice'),
            signal_duration=data.get('signal_duration'),
            sample_frequency=data.get('sample_frequency'),
            start_time=data.get('start_time'),
        )

        # self.request.session['data_simulated'] = self.as_array(data)


class EditDataSimulatedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['data_simulated'] = DataSimulated.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditDataSimulatedForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataSimulated
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
