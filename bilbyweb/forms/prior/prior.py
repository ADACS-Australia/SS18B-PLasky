"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

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
    """
    Data form class which extends the DynamicForm.
    It is not known beforehand which fields are to be rendered, we only know this information once there is a
    signal entry. Therefore, unlike the other forms we cannot use any predefined list of fields.
    """

    # stores the fieldsets in order
    # A Ordered Dictionary to render the fields in order in the template
    fieldsets = None

    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'prior'
        self.job = kwargs.pop('job', None)
        kwargs['fields_properties'] = self.get_field_properties()

        super(PriorForm, self).__init__(*args, **kwargs)

    def get_field_properties(self):
        """
        Finds out the required fields based on the signal, if no signal it returns an empty Ordered Dictionary
        :return: Ordered Dictionary
        """
        if not self.job:

            # if a draft job has not been created, returning an empty dict.
            return OrderedDict()

        else:

            # check whether a signal information is present, if it is, the field properties will be formed based on
            # the signal model field.
            try:
                signal = Signal.objects.get(job=self.job)

                self.fieldsets, field_properties = get_field_properties_by_signal_choice(signal)

                return field_properties

            except Signal.DoesNotExist:
                return OrderedDict()

    def update_fields_to_required(self):
        """
        Makes every field as required, initially it is not set as required to escape the form validation.
        This should be called just before rendering the form in the template.
        :return: Nothing
        """
        for field_name in self.fields:
            self.fields[field_name].required = True

    def clean(self):
        """
        Checks the validation of the form. Note: Default Django Form field cleaning cannot be done with this type of
        form as there is no fixed field. This is mainly used for additional field input checking and dependent field
        input checking like min and max.
        :return:
        """

        if not self.fieldsets:
            # this means that we have no fields in the form, so we do not need to process further
            return

        data = self.cleaned_data

        # number of non_fixed fields, to check minimum of one non fixed prior
        non_fixed_fields = 0

        for fieldset_fields in self.fieldsets.values():

            # gets the fields classified, i.e., min_field, max_field, type_fields are categorised for common processing.
            field_classifications = classify_fields(fieldset_fields)

            # for uniform field type we will checking whether max is greater than min
            if data.get(field_classifications.get('type_field'), None) == 'uniform':
                # increasing the number of uniform fields
                non_fixed_fields += 1
                min_data = data.get(field_classifications.get('min_field'))
                max_data = data.get(field_classifications.get('max_field'))

                try:

                    # checking min max validation
                    if float(min_data) >= float(max_data):
                        error_msg = forms.ValidationError("Must be less than Max")
                        self.add_error(field_classifications.get('min_field'), error_msg)
                        error_msg = forms.ValidationError("Must be greater than Min")
                        self.add_error(field_classifications.get('max_field'), error_msg)
                except TypeError:
                    pass

        # al least one prior should be uniform, otherwise bilby job will fail
        # if that is not the case, adding non field errors.
        if not non_fixed_fields:
            self.add_error(forms.forms.NON_FIELD_ERRORS, 'At least one prior should be uniform.')

    def save(self):
        """
        Saves a prior form
        :return: Nothing
        """
        self.full_clean()
        data = self.cleaned_data

        if not self.fieldsets:
            return

        for fieldset_fields in self.fieldsets.values():

            # gets the fields classified, i.e., min_field, max_field, type_fields are categorised for common processing.
            field_classifications = classify_fields(fieldset_fields)

            prior_choice = data.get(field_classifications.get('type_field'))

            # for a particular prior type, we will be updating all the fields, the non-relevant fields to be set to None
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
        """
        Populates the form field with the values stored in the database
        :param job: instance of job model for which the prior parameters belong to
        :return: Nothing
        """

        if not job or not self.fieldsets:
            return

        for fieldset_fields in self.fieldsets.values():

            # gets the fields classified, i.e., min_field, max_field, type_fields are categorised for common processing.
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
