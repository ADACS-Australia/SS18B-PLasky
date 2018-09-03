from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..dynamic.form import DynamicForm
from ...models import Job, Prior, Signal
from .utility import get_field_properties_by_signal_choice

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


class PriorForm(DynamicForm):
    fieldsets = None

    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'prior'
        self.job = kwargs.pop('job', None)
        kwargs['fields_properties'] = self.get_field_properties()

        super(PriorForm, self).__init__(*args, **kwargs)

    def get_field_properties(self):
        if not self.job:
            return OrderedDict()
        else:
            try:
                signal = Signal.objects.get(job=self.job)
                self.fieldsets, field_properties = get_field_properties_by_signal_choice(signal)
                return field_properties
            except Signal.DoesNotExist:
                return OrderedDict()

    class Meta:
        model = Prior
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self, **kwargs):
        # self.full_clean()
        # data = self.cleaned_data
        #
        # result = Prior.objects.create(
        #     job=self.job,
        #     prior_choice=data.get('prior_choice'),
        # )
        pass
