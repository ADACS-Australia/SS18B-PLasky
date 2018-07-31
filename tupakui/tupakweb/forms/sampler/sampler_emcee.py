from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, SamplerEmcee

FIELDS = ['n_steps',]

WIDGETS = {
    'n_steps': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'n_steps': _('Number of live points'),
}

class SamplerEmceeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(SamplerEmcee, self).__init__(*args, **kwargs)

    class Meta:
        model = SamplerEmcee
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        result = SamplerEmcee.objects.update_or_create(
            sampler=job.sampler,
            n_steps=data.get('n_steps'),
        )

        self.request.session['sampler_emcee'] = self.as_array(data)
