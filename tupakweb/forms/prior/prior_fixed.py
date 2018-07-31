from django import forms
from django.utils.translation import ugettext_lazy as _
from tupakui.tupakweb.models import (
    Job, PriorFixed, Signal, SignalBbh
)

FIELDS = ['value',]

WIDGETS = {
    'value': forms.FloatField(
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

    class Meta:
        model = PriorFixed
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)
        if job.signal.signal_choice == Signal.BINARY_BLACK_HOLE:
            prior = job.signal.signal_bbh_parameter.prior

        result = PriorFixed.objects.update_or_create(
            prior=prior,
            value=data.get('value'),
        )

        self.request.session['prior_fixed'] = self.as_array(data)

    class Meta:
        model = PriorFixed
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
