from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import (
    Job, PriorFixed, Signal
)

FIELDS = [
    'value',
]

WIDGETS = {
    'value': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'value': _('Value'),
}


class PriorFixedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(PriorFixedForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)
        if job.signal.signal_choice == Signal.BINARY_BLACK_HOLE:
            prior = job.signal.signal_bbh_parameter.prior

        result = PriorFixed.objects.create(
            prior=prior,
            value=data.get('value'),
        )

        self.request.session['prior_fixed'] = self.as_array(data)

    class Meta:
        model = PriorFixed
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS


class EditPriorFixedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['prior_fixed'] = PriorFixed.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditPriorFixedForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PriorFixed
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
