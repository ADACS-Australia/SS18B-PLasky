from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, SamplerDynesty

FIELDS = ['n_livepoints',]

WIDGETS = {
    'n_livepoints': forms.Select(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'n_livepoints': _('Number of live points'),
}

class SamplerDynestyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(SamplerDynesty, self).__init__(*args, **kwargs)

    class Meta:
        model = SamplerDynesty
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        result = SamplerDynesty.objects.update_or_create(
            sampler=job.sampler,
            n_livepoints=data.get('n_livepoints'),
        )

        self.request.session['sampler_dynesty'] = self.as_array(data)
