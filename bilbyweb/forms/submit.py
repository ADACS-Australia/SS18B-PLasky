import logging
from collections import OrderedDict
from django.utils import timezone

from .dynamic.form import DynamicForm
from .dynamic import field

from ..utility.display_names import SUBMITTED
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
    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'data-parameter'
        kwargs['fields_properties'] = FIELDS_PROPERTIES
        self.job = kwargs.pop('job', None)
        super(SubmitJobForm, self).__init__(*args, **kwargs)

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        self.job.json_representation = data.get('json_representation')
        self.job.status = SUBMITTED
        self.job.submission_time = timezone.now()
        self.job.save()

        self.request.session['draft_job'] = None

    def update_from_database(self, job=None):
        if job:
            bilby_job = BilbyJob(job_id=job.id)
            self.fields['json_representation'].initial = bilby_job.as_json()


