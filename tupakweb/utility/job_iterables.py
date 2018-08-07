from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict
from os.path import basename
from ..utility.constants import *
from ..forms.job import (
    FIELDS as fields_job,
    LABELS as labels_job
)
from ..forms.data.data import (
    FIELDS as fields_data,
    LABELS as labels_data
)
from ..forms.data.data_simulated import (
    FIELDS as fields_data_simulated,
    LABELS as labels_data_simulated
)
from ..forms.data.data_open import (
    FIELDS as fields_data_open,
    LABELS as labels_data_open
)
from ..forms.signal.signal import (
    FIELDS as fields_signal,
    LABELS as labels_signal
)
from ..forms.prior.prior import (
    FIELDS as fields_prior,
    LABELS as labels_prior
)
from ..forms.prior.prior_uniform import (
    FIELDS as fields_prior_uniform,
    LABELS as labels_prior_uniform
)
from ..forms.prior.prior_fixed import (
    FIELDS as fields_prior_fixed,
    LABELS as labels_prior_fixed
)
from ..forms.sampler.sampler import (
    FIELDS as fields_sampler, 
    LABELS as labels_sampler
)
from ..forms.sampler.sampler_dynesty import (
    FIELDS as fields_sampler_dynesty,
    LABELS as labels_sampler_dynesty
)
from ..forms.sampler.sampler_emcee import (
    FIELDS as fields_sampler_emcee,
    LABELS as labels_sampler_emcee
)


def model_instance_to_iterable(object, model=START, views=[]):
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
        fields = fields_job
        labels = labels_job

    if model == DATA:
        fields = fields_data
        labels = labels_data

    if model == DATA_OPEN:
        fields = fields_data_open
        labels = labels_data_open

    if model == DATA_SIMULATED:
        fields = fields_data_simulated
        labels = labels_data_simulated

    if model == SIGNAL:
        fields = fields_signal
        labels = labels_signal

    if model == PRIOR:
        fields = fields_prior
        labels = labels_prior

    if model == PRIOR_FIXED:
        fields = fields_prior_fixed
        labels = labels_prior_fixed

    if model == PRIOR_UNIFORM:
        fields = fields_prior_uniform
        labels = labels_prior_uniform

    if model == SAMPLER:
        fields = fields_sampler
        labels = labels_sampler

    if model == SAMPLER_DYNESTY:
        fields = fields_sampler_dynesty
        labels = labels_sampler_dynesty

    if model == SAMPLER_EMCEE:
        fields = fields_sampler_emcee
        labels = labels_sampler_emcee

    return fields, labels
