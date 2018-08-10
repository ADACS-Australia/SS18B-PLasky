from django import forms
from django.utils.translation import ugettext_lazy as _
from ..models import Job

FIELDS = [
    'name',
    'description',
]

LABELS = {
    'name': _('Job name'),
    'description': _('Job description'),
}


class StartJobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StartJobForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Job
        fields = FIELDS
        labels = LABELS

    def clean_name(self):
        name = self.cleaned_data['name']
        # the user either needs to select a draft job from the list or enter a new
        # job name for which a draft is going to be created
        if name is None or name == '':
            raise forms.ValidationError(
                "You must select a job or provide a job name"
            )
        else:
            if Job.objects.filter(
                    user=self.request.user,
                    name=self.cleaned_data.get('name')
            ).exists():
                raise forms.ValidationError(
                    "You already have a job with the same name"
                )
        return name

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        job_created = Job.objects.create(
            user=self.request.user,
            name=data.get('name'),
            description=data.get('description'),
        )
        if job_created:
            self.request.session['draft_job'] = job_created.as_json()


class EditJobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['draft_job'] = Job.objects.get(id=self.job_id).as_json()
            except:
                pass
        super(EditJobForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Job
        fields = FIELDS
        labels = LABELS
