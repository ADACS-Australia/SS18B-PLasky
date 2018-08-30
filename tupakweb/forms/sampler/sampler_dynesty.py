from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, SamplerDynesty

FIELDS = [
    'n_livepoints',
]

WIDGETS = {
    'n_livepoints': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'n_livepoints': _('Number of live points'),
}


class SamplerDynestyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job = kwargs.pop('job', None)
        super(SamplerDynestyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SamplerDynesty
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        result = SamplerDynesty.objects.create(
            sampler=self.job.sampler,
            n_livepoints=data.get('n_livepoints'),
        )
