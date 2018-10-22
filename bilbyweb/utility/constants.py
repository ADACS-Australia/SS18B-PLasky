"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from ..models import (
    Job,
    Data,
    Sampler,
)

from ..forms.start import StartJobForm
from ..forms.submit import SubmitJobForm
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

# Number of jobs to be displayed in a page showing list view
# Ex: My Jobs, My Drafts, All Jobs, Public Jobs etc.
JOBS_PER_PAGE = 50


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


# Number of TABs to show up in the UI. We currently have 6 TABs
TABS = [
    START,
    DATA,
    SIGNAL,
    PRIOR,
    SAMPLER,
    LAUNCH,
]
TABS_INDEXES = set_dict_indices(TABS)


# Tab Forms, defines the forms of a Tab. Based on this, forms are saved when Next or Previous buttons are pressed.
TAB_FORMS = {
    START: [START],
    DATA: [DATA, DATA_SIMULATED, DATA_OPEN, ],
    SIGNAL: [SIGNAL, SIGNAL_PARAMETER_BBH, ],
    PRIOR: [PRIOR, ],
    SAMPLER: [SAMPLER, SAMPLER_DYNESTY, SAMPLER_NESTLE, SAMPLER_EMCEE, ],
    LAUNCH: [LAUNCH, ]
}


# Form Dictionary, Maps the form key to the actual form class
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
    LAUNCH: SubmitJobForm,
}


# Maps models to form keys for models that use Django Model Forms.
MODELS = {
    START: Job,
    DATA: Data,
    SAMPLER: Sampler,
}
