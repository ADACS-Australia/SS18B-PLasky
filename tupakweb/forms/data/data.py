from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Data

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
        self.job = kwargs.pop('job', None)
        super(DataForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Data
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        # deleting data object will make sure that there exists no parameter
        # this avoids duplicating parameters
        Data.objects.filter(job=self.job).delete()

        Data.objects.update_or_create(
            job=self.job,
            defaults={
                'data_choice': data.get('data_choice'),
            }
        )
