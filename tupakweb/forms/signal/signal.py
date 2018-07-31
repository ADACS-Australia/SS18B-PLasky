from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Job, Signal

FIELDS = ['inject_or_not',
          'signal_choice']

WIDGETS = {
    'inject_or_not': forms.Select(
        attrs={'class': 'form-control'},
    ),
    'signal_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'inject_or_not': _('Inject a signal?'),
    'signal_choice': _('Signal type'),
}

class SignalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(SignalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Signal
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        result = Signal.objects.update_or_create(
            job=job,
            data_choice=data.get('data_choice'),
        )

        self.request.session['dataset'] = self.as_array(data)



