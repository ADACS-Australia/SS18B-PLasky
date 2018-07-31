from .job_utils import set_dict_indices
from ..models import (
    Job,
    Data, DataOpen, DataSimulated,
    Signal, SignalBbhParameter,
    Prior, PriorFixed, PriorUniform,
    Sampler, SamplerDynesty, SamplerEmcee, SamplerNestle
)

from ..forms.job import StartJobForm
from ..forms.data.data import DataForm
from ..forms.data.data_simulated import DataSimulatedForm
from ..forms.data.data_open import DataOpenForm
from ..forms.signal.signal import SignalForm
from ..forms.prior.prior import PriorForm
from ..forms.prior.prior_uniform import PriorUniformForm
from ..forms.prior.prior_fixed import PriorFixedForm
from ..forms.sampler.sampler import SamplerForm
from ..forms.sampler.sampler_dynesty import SamplerDynestyForm
from ..forms.sampler.sampler_emcee import SamplerEmceeForm

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

FORMS = {
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