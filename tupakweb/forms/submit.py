import logging
from collections import OrderedDict

from .dynamic.form import DynamicForm
from .dynamic import field

from ..utility.display_names import SUBMITTED
from ..utility.job import TupakJob


logger = logging.getLogger(__name__)

DATA_FIELDS_PROPERTIES = OrderedDict([
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
        kwargs['fields_properties'] = DATA_FIELDS_PROPERTIES
        self.job = kwargs.pop('job', None)
        super(SubmitJobForm, self).__init__(*args, **kwargs)

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        self.job.json_representation = data.get('json_representation')
        self.job.status = SUBMITTED
        self.job.save()

        self.request.session['draft_job'] = None

    def update_from_database(self, job=None):
        if job:
            tupak_job = TupakJob(job_id=job.id)
            self.fields['json_representation'].initial = tupak_job.as_json()


