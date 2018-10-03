from collections import OrderedDict

from django import forms

from ...utility.display_names import UNIFORM, FIXED
from ..dynamic.form import DynamicForm
from ...models import (
    Prior,
    Signal,
)
from .utility import (
    get_field_properties_by_signal_choice,
    classify_fields,
)


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
        if not self.fieldsets:
            return
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
                        error_msg = forms.ValidationError("Must be greater than Min")
                        self.add_error(field_classifications.get('max_field'), error_msg)
                except TypeError:
                    pass

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        if not self.fieldsets:
            return

        for fieldset_fields in self.fieldsets.values():
            field_classifications = classify_fields(fieldset_fields)

            prior_choice = data.get(field_classifications.get('type_field'))

            Prior.objects.update_or_create(
                job=self.job,
                name=field_classifications.get('signal_parameter_name'),
                defaults={
                    'prior_choice': prior_choice,
                    'fixed_value': data.get(
                        field_classifications.get('fixed_field')) if prior_choice == FIXED else None,
                    'uniform_min_value': data.get(
                        field_classifications.get('min_field')) if prior_choice == UNIFORM else None,
                    'uniform_max_value': data.get(
                        field_classifications.get('max_field')) if prior_choice == UNIFORM else None,
                },
            )

    def update_from_database(self, job):
        if not job or not self.fieldsets:
            return

        for fieldset_fields in self.fieldsets.values():
            field_classifications = classify_fields(fieldset_fields)

            # get prior
            try:
                prior = Prior.objects.get(
                    job=self.job,
                    name=field_classifications.get('signal_parameter_name'),
                )

                self.fields[field_classifications.get('type_field')].initial = prior.prior_choice
                self.fields[field_classifications.get('fixed_field')].initial = prior.fixed_value
                self.fields[field_classifications.get('min_field')].initial = prior.uniform_min_value
                self.fields[field_classifications.get('max_field')].initial = prior.uniform_max_value
            except Prior.DoesNotExist:
                pass