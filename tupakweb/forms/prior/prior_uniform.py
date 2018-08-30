from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import (
    Job, PriorUniform, Signal
)

FIELDS = [
    'value_min',
    'value_max',
]

WIDGETS = {
    'value_min': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
    'value_max': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'value_min': _('Minimum value'),
    'value_max': _('Maximum value'),
}


class PriorUniformForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job = kwargs.pop('job', None)
        super(PriorUniformForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PriorUniform
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        if self.job.signal.signal_choice == Signal.BINARY_BLACK_HOLE:
            prior = self.job.signal.signal_bbh_parameter.prior

        result = PriorUniform.objects.create(
            prior=prior,
            value_min=data.get('value_min'),
            value_max=data.get('value_max'),
        )
