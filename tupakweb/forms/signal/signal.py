from collections import OrderedDict
from copy import deepcopy
from ..dynamic import field
from ..dynamic.form import DynamicForm
from ...utility.display_names import (
    OPEN_DATA,
    SIGNAL_CHOICE,
    SIGNAL_CHOICE_DISPLAY,
    SIGNAL_MODEL,
    SIGNAL_MODEL_DISPLAY,
    SKIP,
)
from ...models import Signal, Data

SIGNAL_FIELDS_PROPERTIES = OrderedDict([
    (SIGNAL_CHOICE, {
        'type': field.SELECT,
        'label': SIGNAL_CHOICE_DISPLAY,
        'choices': Signal.SIGNAL_CHOICES,
        'required': True,
    }),
    ('same_model', {
        'type': field.CHECKBOX,
        'label': 'Same for Signal Model?',
        # 'placeholder': '1.0',
        'initial': True,
    }),
    (SIGNAL_MODEL, {
        'type': field.SELECT,
        'label': SIGNAL_MODEL_DISPLAY,
        'choices': Signal.SIGNAL_CHOICES[1:],
        'required': True,
    }),
])


class SignalForm(DynamicForm):
    def __init__(self, *args, **kwargs):
        kwargs['name'] = 'signal-binary_black_hole'
        kwargs['fields_properties'] = deepcopy(SIGNAL_FIELDS_PROPERTIES)
        self.job = kwargs.pop('job', None)

        # checking the data_choice to decide whether skip should be there
        show_skip = True
        if self.job:
            try:
                data = Data.objects.get(job=self.job)
                if data.data_choice != OPEN_DATA:
                    show_skip = False
            except Data.DoesNotExist:
                pass

        if not show_skip:
            kwargs['fields_properties'][SIGNAL_CHOICE].update({
                'choices': Signal.SIGNAL_CHOICES[1:],
            })

        super(SignalForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        self.full_clean()
        data = self.cleaned_data

        signal_choice = data.get('signal_choice')

        if signal_choice == SKIP:
            # signal should be deleted if there is a change of choice
            # currently as there is only one available, it does not
            # have any adverse effect.
            Signal.objects.filter(job=self.job).delete()
        else:
            Signal.objects.update_or_create(
                job=self.job,
                defaults={
                    'signal_choice': data.get('signal_choice'),
                }
            )
