from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, Data

FIELDS = ['data_choice', ]

WIDGETS = {
    'data_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'data_choice': _('Type of data'),
}


class DataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(DataForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Data
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        result = Data.objects.create(
            job=job,
            data_choice=data.get('data_choice'),
        )

        # self.request.session['data'] = self.as_array(data)


class EditDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['data'] = Data.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditDataForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Data
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
