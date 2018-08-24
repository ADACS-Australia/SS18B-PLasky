from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, Sampler

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
        self.id = kwargs.pop('id', None)
        super(SamplerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sampler
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        result = Sampler.objects.create(
            job=job,
            sampler_choice=data.get('sampler_choice'),
        )
