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

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        result = Signal.objects.create(
            job=job,
            data_choice=data.get('signal_choice'),
        )

        self.request.session['signal'] = self.as_array(data)

class EditSignalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['signal'] = Signal.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditSignalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Signal
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
