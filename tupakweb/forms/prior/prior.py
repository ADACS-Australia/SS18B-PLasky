from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..dynamic.form import DynamicForm
from ...models import (
    Prior,
    Signal,
    SignalParameter,
)
from .utility import (
    get_field_properties_by_signal_choice,
    classify_fields,
)

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

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        for fieldset_fields in self.fieldsets.values():
            field_classifications = classify_fields(fieldset_fields)

            # get signal parameter
            signal_parameter = SignalParameter.objects.get(
                signal__job=self.job,
                name=field_classifications.get('signal_parameter_name')
            )

            prior_choice = data.get(field_classifications.get('type_field'))

            Prior.objects.update_or_create(
                signal_parameter=signal_parameter,
                defaults={
                    'prior_choice': prior_choice,
                    'fixed_value': data.get(
                        field_classifications.get('fixed_field')) if prior_choice == Prior.FIXED else None,
                    'uniform_min_value': data.get(
                        field_classifications.get('min_field')) if prior_choice == Prior.UNIFORM else None,
                    'uniform_max_value': data.get(
                        field_classifications.get('max_field')) if prior_choice == Prior.UNIFORM else None,
                },
            )

    def update_from_database(self, job):
        if not job:
            return

        for fieldset_fields in self.fieldsets.values():
            field_classifications = classify_fields(fieldset_fields)

            # get prior
            prior = Prior.objects.get(
                signal_parameter=SignalParameter.objects.get(
                    signal__job=self.job,
                    name=field_classifications.get('signal_parameter_name')
                ),
            )

            self.fields[field_classifications.get('type_field')].initial = prior.prior_choice
            self.fields[field_classifications.get('fixed_field')].initial = prior.fixed_value
            self.fields[field_classifications.get('min_field')].initial = prior.uniform_min_value
            self.fields[field_classifications.get('max_field')].initial = prior.uniform_max_value
