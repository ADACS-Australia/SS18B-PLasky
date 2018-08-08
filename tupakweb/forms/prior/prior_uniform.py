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
        self.id = kwargs.pop('id', None)
        super(PriorUniformForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)
        if job.signal.signal_choice == Signal.BINARY_BLACK_HOLE:
            prior = job.signal.signal_bbh_parameter.prior

        result = PriorUniform.objects.create(
            prior=prior,
            value_min=data.get('value_min'),
            value_max=data.get('value_max'),
        )

        self.request.session['prior_uniform'] = self.as_array(data)

    class Meta:
        model = PriorUniform
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS


class EditPriorUniformForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['prior_uniform'] = PriorUniform.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditPriorUniformForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PriorUniform
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
