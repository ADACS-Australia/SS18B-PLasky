from collections import OrderedDict

from ...utility.display_names import DYNESTY
from ..dynamic import field
from ...models import SamplerParameter, Sampler
from ..dynamic.form import DynamicForm
from ...utility.display_names import (
    NUMBER_OF_LIVE_POINTS,
    NUMBER_OF_LIVE_POINTS_DISPLAY,
)

DYNESTY_FIELDS_PROPERTIES = OrderedDict([
    (NUMBER_OF_LIVE_POINTS, {
        'type': field.POSITIVE_INTEGER,
        'label': NUMBER_OF_LIVE_POINTS_DISPLAY,
        'placeholder': '1000',
        'initial': None,
        'required': True,
    }),
])


class SamplerDynestyParameterForm(DynamicForm):

    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'data-parameter'
        kwargs['fields_properties'] = DYNESTY_FIELDS_PROPERTIES
        self.job = kwargs.pop('job', None)

        super(SamplerDynestyParameterForm, self).__init__(*args, **kwargs)

    def save(self):
        # find the sampler first
        sampler = Sampler.objects.get(job=self.job)
        for name, value in self.cleaned_data.items():
            SamplerParameter.objects.update_or_create(
                sampler=sampler,
                name=name,
                defaults={
                    'value': value,
                }
            )

    def update_from_database(self, job):
        if not job:
            return
        else:
            try:
                sampler = Sampler.objects.get(job=job)
                if sampler.sampler_choice != DYNESTY:
                    return
            except Sampler.DoesNotExist:
                return

        for name in DYNESTY_FIELDS_PROPERTIES.keys():
            try:
                value = SamplerParameter.objects.get(sampler=sampler, name=name).value
                self.fields[name].initial = value
            except SamplerParameter.DoesNotExist:
                pass
