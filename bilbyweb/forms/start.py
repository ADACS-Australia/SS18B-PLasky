"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Job


logger = logging.getLogger(__name__)


FIELDS = [
    'name',
    'description',
]

LABELS = {
    'name': _('Job name'),
    'description': _('Job description'),
}


class StartJobForm(forms.ModelForm):
    """
    Start form class
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job = kwargs.pop('job', None)
        super(StartJobForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Job
        fields = FIELDS
        labels = LABELS

    def clean_name(self):
        """
        Validates the name of the job. For a user, a job should must a unique name.
        :return: String value of the name field
        """
        name = self.cleaned_data['name']

        # if already validated before, there would be a match with itself and no problem with that
        if self.job and self.job.name == name:
            return name

        # if exists, raise the validation error
        if Job.objects.filter(
                user=self.request.user,
                name=self.cleaned_data.get('name')
        ).exists():
            logger.info("You already have a job with the same name")
            raise forms.ValidationError(
                "You already have a job with the same name"
            )

        return name

    def save(self, **kwargs):
        """
        Overrides the default save method
        :param kwargs: Dictionary of keyword arguments
        :return: Nothing
        """
        self.full_clean()
        data = self.cleaned_data

        job_created, created = Job.objects.update_or_create(
            user=self.request.user,
            name=self.job.name if self.job else None,
            defaults={
                'name': data.get('name'),
                'description': data.get('description'),
            }
        )

        self.request.session['draft_job'] = job_created.as_json()

