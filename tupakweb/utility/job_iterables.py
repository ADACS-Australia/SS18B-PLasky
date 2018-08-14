from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict
from os.path import basename

from ..utility.constants import *
from ..forms.job import (
    FIELDS as FIELDS_JOB,
    LABELS as LABELS_JOB
)
from ..forms.data.data import (
    FIELDS as FIELDS_DATA,
    LABELS as LABELS_DATA,
)
from ..forms.data.data_simulated import (
    FIELDS as FIELDS_DATA_SIMULATED,
    LABELS as LABELS_DATA_SIMULATED,
)
from ..forms.data.data_open import (
    FIELDS as FIELDS_DATA_OPEN,
    LABELS as LABELS_DATA_OPEN
)
from ..forms.signal.signal import (
    FIELDS as FIELDS_SIGNAL,
    LABELS as LABELS_SIGNAL
)
from ..forms.prior.prior import (
    FIELDS as FIELDS_PRIOR,
    LABELS as LABELS_PRIOR
)
from ..forms.prior.prior_uniform import (
    FIELDS as FIELDS_PRIOR_UNIFORM,
    LABELS as LABELS_PRIOR_UNIFORM
)
from ..forms.prior.prior_fixed import (
    FIELDS as FIELDS_PRIOR_FIXED,
    LABELS as LABELS_PRIOR_FIXED
)
from ..forms.sampler.sampler import (
    FIELDS as FIELDS_SAMPLER,
    LABELS as LABELS_SAMPLER,
)
from ..forms.sampler.sampler_dynesty import (
    FIELDS as FIELDS_SAMPLER_DYNESTY,
    LABELS as LABELS_SAMPLER_DYNESTY
)
from ..forms.sampler.sampler_emcee import (
    FIELDS as FIELDS_SAMPLER_EMCEE,
    LABELS as LABELS_SAMPLER_EMCEE
)


def model_instance_to_iterable(object, model=START, views=None):
    """Converts the object returned from a Model query into an iterable object to be used by a template

    Parameters
    ----------
    object:
        object returned from a Model query
    model:
        Model to be considered (using the tabs convention used in job.py)
    views:
        list of views currently active

    Returns
    -------
    object:
        the newly iterable object, or None.
    """
    fields, labels = get_metadata(model, views, object)

    try:
        object.fields = OrderedDict(((field.name, [labels[field.name], field.value_to_string(object)])
                                     if 'file' not in field.name else
                                     ((field.name, [labels[field.name], basename(field.value_to_string(object))])
                                      if 'filename' not in field.name else
                                      (field.name, [labels[field.name], field.value_to_string(object)])
                                      )
                                     )
                                    for field in object._meta.fields if field.name in fields)

        return object
    except:
        return None


def get_metadata(model, views, object):
    """Get metadata about a model

    (e.g. fields and labels to be displayed by a template.)

    Parameters
    ----------
    model:
        Model to be considered (using the tabs convention used in job_utils.py)
    views:
        list of views currently active
    object:
        object returned from a Model query
    Returns
    -------
    fields, labels
    """
    if model == START:
        fields = FIELDS_JOB
        labels = LABELS_JOB

    elif model == DATA:
        fields = FIELDS_DATA
        labels = LABELS_DATA

    elif model == DATA_OPEN:
        fields = FIELDS_DATA_OPEN
        labels = LABELS_DATA_OPEN

    elif model == DATA_SIMULATED:
        fields = FIELDS_DATA_SIMULATED
        labels = LABELS_DATA_SIMULATED

    elif model == SIGNAL:
        fields = FIELDS_SIGNAL
        labels = LABELS_SIGNAL

    elif model == PRIOR:
        fields = FIELDS_PRIOR
        labels = LABELS_PRIOR

    elif model == PRIOR_FIXED:
        fields = FIELDS_PRIOR_FIXED
        labels = LABELS_PRIOR_FIXED

    elif model == PRIOR_UNIFORM:
        fields = FIELDS_PRIOR_UNIFORM
        labels = LABELS_PRIOR_UNIFORM

    elif model == SAMPLER:
        fields = FIELDS_SAMPLER
        labels = LABELS_SAMPLER

    elif model == SAMPLER_DYNESTY:
        fields = FIELDS_SAMPLER_DYNESTY
        labels = LABELS_SAMPLER_DYNESTY

    elif model == SAMPLER_EMCEE:
        fields = FIELDS_SAMPLER_EMCEE
        labels = LABELS_SAMPLER_EMCEE

    else:
        fields = None
        labels = None

    return fields, labels
