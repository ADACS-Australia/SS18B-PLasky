from ..models import (
    Job,
    Data,
    Signal,
    Sampler,
)

from ..forms.job import StartJobForm
from ..forms.data.data import DataForm
from ..forms.data.data_simulated import SimulatedDataParameterForm
from ..forms.data.data_open import OpenDataParameterForm
from ..forms.signal.signal import SignalForm
from ..forms.signal.signal_parameter import SignalParameterBbhForm
from ..forms.prior.prior import PriorForm
from ..forms.sampler.sampler import SamplerForm
from ..forms.sampler.sampler_dynesty import SamplerDynestyParameterForm
from ..forms.sampler.sampler_nestle import SamplerNestleParameterForm
from ..forms.sampler.sampler_emcee import SamplerEmceeParameterForm


def set_dict_indices(my_array):
    """Creates a dictionary based on values in my_array, and links each of them to an index.

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
SIGNAL_PARAMETER_BBH = 'signal-parameter-bbh'
PRIOR = 'prior'
SAMPLER = 'sampler'
SAMPLER_DYNESTY = 'sampler-dynesty'
SAMPLER_EMCEE = 'sampler-emcee'
SAMPLER_NESTLE = 'sampler-nestle'
LAUNCH = 'launch'

SKIP_FORWARD = 'SKIP >'
SKIP_BACKWARD = '< SKIP'
REMOVE_FORWARD = 'REMOVE >'
REMOVE_BACKWARD = '< REMOVE'

TABS = [
    START,
    DATA,
    SIGNAL,
    PRIOR,
    SAMPLER,
    LAUNCH,
]
TABS_INDEXES = set_dict_indices(TABS)

TAB_FORMS = {
    START: [START],
    DATA: [DATA, DATA_SIMULATED, DATA_OPEN, ],
    SIGNAL: [SIGNAL, SIGNAL_PARAMETER_BBH, ],
    PRIOR: [PRIOR, ],
    SAMPLER: [SAMPLER, SAMPLER_DYNESTY, SAMPLER_NESTLE, SAMPLER_EMCEE, ],
}

FORMS_NEW = {
    START: StartJobForm,
    DATA: DataForm,
    DATA_SIMULATED: SimulatedDataParameterForm,
    DATA_OPEN: OpenDataParameterForm,
    SIGNAL: SignalForm,
    SIGNAL_PARAMETER_BBH: SignalParameterBbhForm,
    PRIOR: PriorForm,
    SAMPLER: SamplerForm,
    SAMPLER_DYNESTY: SamplerDynestyParameterForm,
    SAMPLER_NESTLE: SamplerNestleParameterForm,
    SAMPLER_EMCEE: SamplerEmceeParameterForm,
}

MODELS = {
    START: Job,
    DATA: Data,
    SIGNAL: Signal,
    SAMPLER: Sampler,
}
