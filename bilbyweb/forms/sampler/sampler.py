from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Sampler

FIELDS = [
    'sampler_choice',
]

WIDGETS = {
    'sampler_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'sampler_choice': _('Sampler'),
}


class SamplerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job = kwargs.pop('job', None)
        super(SamplerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sampler
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        # deleting sampler object will make sure that there exists no parameter
        # this avoids duplicating parameters
        Sampler.objects.filter(job=self.job).delete()

        Sampler.objects.update_or_create(
            job=self.job,
            defaults={
                'sampler_choice': data.get('sampler_choice'),
            },
        )
