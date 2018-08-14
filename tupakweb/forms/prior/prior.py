from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, Prior

FIELDS = [
    'prior_choice',
]

WIDGETS = {
    'prior_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'prior_choice': _('Prior'),
}


class PriorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(PriorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Prior
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        result = Prior.objects.create(
            job=job,
            prior_choice=data.get('prior_choice'),
        )

        self.request.session['prior'] = self.as_array(data)


class EditPriorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['prior'] = Prior.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditPriorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Prior
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
