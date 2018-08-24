from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Signal

FIELDS = [
    'signal_choice',
]

WIDGETS = {
    'signal_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'signal_choice': _('Signal type'),
}


class SignalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job = kwargs.pop('job', None)
        super(SignalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Signal
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        Signal.objects.create(
            job=self.job,
            data_choice=data.get('signal_choice'),
        )
