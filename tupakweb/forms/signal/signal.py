from django import forms
from django.utils.translation import ugettext_lazy as _
from ...models import Signal, Data

FIELDS = [
    'signal_choice',
]

WIDGETS = {
    'signal_choice': forms.Select(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'signal_choice': _('Signal type'),
}


class SignalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job = kwargs.pop('job', None)
        super(SignalForm, self).__init__(*args, **kwargs)

        # checking the data_choice to decide whether skip should be there
        show_skip = True
        if self.job:
            try:
                data = Data.objects.get(job=self.job)
                if data.data_choice != Data.OPEN_DATA:
                    show_skip = False
            except Data.DoesNotExist:
                pass

        self.fields['signal_choice'] = forms.ChoiceField(
            choices=Signal.SIGNAL_CHOICES[1:] if not show_skip else Signal.SIGNAL_CHOICES,
            widget=forms.Select(
                attrs={'class': 'form-control'},
            )
        )

    class Meta:
        model = Signal
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        signal_choice = data.get('signal_choice')

        if signal_choice == Signal.SKIP:
            # signal should be deleted if there is a change of choice
            # currently as there is only one available, it does not
            # have any adverse effect.
            Signal.objects.filter(job=self.job).delete()
        else:
            Signal.objects.update_or_create(
                job=self.job,
                defaults={
                    'signal_choice': data.get('signal_choice'),
                }
            )
