from django import forms
from django.utils.translation import ugettext_lazy as _

from ...models import Data
from ...utility.display_names import DATA_CHOICE_DISPLAY, DATA_CHOICE

FIELDS = [DATA_CHOICE, ]

WIDGETS = {
    'data_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    DATA_CHOICE: _(DATA_CHOICE_DISPLAY),
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
                DATA_CHOICE: data.get(DATA_CHOICE),
            }
        )
