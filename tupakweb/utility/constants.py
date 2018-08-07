from ..models import (
    Job,
    Data, DataOpen, DataSimulated,
    Signal, SignalBbhParameter,
    Prior, PriorFixed, PriorUniform,
    Sampler, SamplerDynesty, SamplerEmcee, SamplerNestle
)

from ..forms.job import StartJobForm, EditJobForm
from ..forms.data.data import DataForm, EditDataForm
from ..forms.data.data_simulated import DataSimulatedForm, EditDataSimulatedForm
from ..forms.data.data_open import DataOpenForm, EditDataOpenForm
from ..forms.signal.signal import SignalForm, EditSignalForm
from ..forms.prior.prior import PriorForm, EditPriorForm
from ..forms.prior.prior_uniform import PriorUniformForm, EditPriorUniformForm
from ..forms.prior.prior_fixed import PriorFixedForm, EditPriorFixedForm
from ..forms.sampler.sampler import SamplerForm, EditSamplerForm
from ..forms.sampler.sampler_dynesty import SamplerDynestyForm, EditSamplerDynestyForm
from ..forms.sampler.sampler_emcee import SamplerEmceeForm, EditSamplerEmceeForm

def set_dict_indices(my_array):
    """Creates a dictionary based on values in my_array, and links each of them to an indice.

    Parameters
    ----------
    my_array:
        An array (e.g. [a,b,c])

    Returns
    -------
    my_dict:
        A dictionary (e.g. {a:0, b:1, c:2})
    """
    my_dict = {}
    i = 0
    for value in my_array:
        my_dict[value] = i
        i += 1

    return my_dict


# Job Creation/Edit/Summary related
START = 'start'
DATA = 'data'
DATA_OPEN = 'data-open'
DATA_SIMULATED = 'data-simulated'
SIGNAL = 'signal'
SIGNAL_BBH_PARAMETERS = 'signal-bbh-parameter'
PRIOR = 'prior'
PRIOR_FIXED = 'prior-fixed'
PRIOR_UNIFORM = 'prior-uniform'
SAMPLER = 'sampler'
SAMPLER_DYNESTY = 'sampler-dynesty'
SAMPLER_EMCEE = 'sampler-emcee'
SAMPLER_NESTLE = 'sampler-nestle'
LAUNCH = 'launch'

TABS = [
    START,
    DATA,
    SIGNAL,
    PRIOR,
    SAMPLER,
    LAUNCH,
]
TABS_INDEXES = set_dict_indices(TABS)

BLOCKS = [
    START,
    DATA,
    DATA_SIMULATED,
    DATA_OPEN,
    SIGNAL,
    SIGNAL_BBH_PARAMETERS,
    PRIOR,
    PRIOR_FIXED,
    PRIOR_UNIFORM,
    SAMPLER,
    SAMPLER_DYNESTY,
    SAMPLER_EMCEE,
    LAUNCH,
]
BLOCKS_INDEXES = set_dict_indices(BLOCKS)


FORMS_NEW = {
    START: StartJobForm,
    DATA: DataForm,
    DATA_SIMULATED: DataSimulatedForm,
    DATA_OPEN: DataOpenForm,
    SIGNAL: SignalForm,
    SIGNAL_BBH_PARAMETERS: None, # Need to figure this one out!
    PRIOR: PriorForm,
    PRIOR_FIXED: PriorFixedForm,
    PRIOR_UNIFORM: PriorUniformForm,
    SAMPLER: SamplerForm,
    SAMPLER_DYNESTY: SamplerDynestyForm,
    SAMPLER_EMCEE: SamplerEmceeForm,
}

FORMS_EDIT = {
    START: EditJobForm,
    DATA: EditDataForm,
    DATA_SIMULATED: EditDataSimulatedForm,
    DATA_OPEN: EditDataOpenForm,
    SIGNAL: EditSignalForm,
    SIGNAL_BBH_PARAMETERS: None, # Need to figure this one out!
    PRIOR: EditPriorForm,
    PRIOR_FIXED: EditPriorFixedForm,
    PRIOR_UNIFORM: EditPriorUniformForm,
    SAMPLER: EditSamplerForm,
    SAMPLER_DYNESTY: EditSamplerDynestyForm,
    SAMPLER_EMCEE: EditSamplerEmceeForm,
}

MODELS = {
    START: Job,
    DATA: Data,
    DATA_SIMULATED: DataSimulated,
    DATA_OPEN: DataOpen,
    SIGNAL: Signal,
    SIGNAL_BBH_PARAMETERS: SignalBbhParameter,
    PRIOR: Prior,
    PRIOR_FIXED: PriorFixed,
    PRIOR_UNIFORM: PriorUniform,
    SAMPLER: Sampler,
    SAMPLER_DYNESTY: SamplerDynesty,
    SAMPLER_EMCEE: SamplerEmcee,
}

data, data_form = None, None
data_simulated, data_simulated_form = None, None
data_open, data_open_form = None, None
signal, signal_form = None, None
prior, prior_form = None, None
prior_fixed, prior_fixed_form = None, None
prior_uniform, prior_uniform_form = None, None
sampler, sampler_form = None, None
sampler_dynesty, sampler_dynesty_form = None, None
sampler_emcee, sampler_emcee_form = None, None

variables = {
    DATA: data,
    DATA_SIMULATED: data_simulated,
    DATA_OPEN: data_open,
    SIGNAL: signal,
    PRIOR: prior,
    PRIOR_FIXED: prior_fixed,
    PRIOR_UNIFORM: prior_uniform,
    SAMPLER: sampler,
    SAMPLER_DYNESTY: sampler_dynesty,
    SAMPLER_EMCEE: sampler_emcee,
}

form_variables = {
    DATA: data_form,
    DATA_SIMULATED: data_simulated_form,
    DATA_OPEN: data_open_form,
    SIGNAL: signal_form,
    PRIOR: prior_form,
    PRIOR_FIXED: prior_fixed_form,
    PRIOR_UNIFORM: prior_uniform_form,
    SAMPLER: sampler_form,
    SAMPLER_DYNESTY: sampler_dynesty_form,
    SAMPLER_EMCEE: sampler_emcee_form,
}