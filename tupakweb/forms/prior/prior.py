from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..dynamic.form import DynamicForm
from ...models import Job, Prior, Signal
from .utility import get_field_properties_by_signal_choice, classify_fields

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

    def update_fields_to_required(self):
        for field_name in self.fields:
            # print(self.fields[field_name].name, self.fields[field_name].required)
            self.fields[field_name].required = True

    def clean(self):
        data = self.cleaned_data
        for fieldset_fields in self.fieldsets.values():
            field_classifications = classify_fields(fieldset_fields)

            if data.get(field_classifications.get('type_field'), None) == 'uniform':
                min_data = data.get(field_classifications.get('min_field'))
                max_data = data.get(field_classifications.get('max_field'))

                try:
                    if float(min_data) >= float(max_data):
                        error_msg = forms.ValidationError("Must be less than Max")
                        # field_name = field_classifications.get('min_field')
                        # field = self.fields[field_name]
                        self.add_error(field_classifications.get('min_field'), error_msg)
                        error_msg = forms.ValidationError("Must greater than Min")
                        self.add_error(field_classifications.get('max_field'), error_msg)
                except TypeError:
                    pass

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
