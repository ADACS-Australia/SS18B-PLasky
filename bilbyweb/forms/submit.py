"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import logging
from collections import OrderedDict

from .dynamic.form import DynamicForm
from .dynamic import field

from ..utility.job import BilbyJob


logger = logging.getLogger(__name__)


FIELDS_PROPERTIES = OrderedDict([
    ('json_representation', {
        'type': field.TEXT_AREA,
        'label': 'JSON',
        'initial': None,
        'required': True,
    }),
])


class SubmitJobForm(DynamicForm):
    """
    Submit form extending Dynamic Form
    """
    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'data-parameter'
        kwargs['fields_properties'] = FIELDS_PROPERTIES
        self.job = kwargs.pop('job', None)
        super(SubmitJobForm, self).__init__(*args, **kwargs)

    def save(self):
        """
        Overrides the default Django Form's save method
        :return: Nothing
        """
        self.full_clean()
        data = self.cleaned_data

        # the json representation of the job is to be saved in the Job model
        self.job.json_representation = data.get('json_representation')

        # Submit the job to HPC
        self.job.submit(self.job.json_representation)

        # remove the draft job from the session as it is not draft anymore
        self.request.session['draft_job'] = None

    def update_from_database(self, job=None):
        """
        Populates the form field with the values stored in the database
        :param job: instance of job model for which the sampler parameters belong to
        :return: Nothing
        """
        if job:
            bilby_job = BilbyJob(job_id=job.id)

            # as currently it is the only field, we are not using a loop like other forms
            self.fields['json_representation'].initial = bilby_job.as_json()


