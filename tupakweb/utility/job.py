import json

from ..models import (
    Job,
    Data,
    Signal,
    SignalParameter,
    DataParameter,
    Prior,
    Sampler,
    SamplerParameter,
)

from ..forms.signal.signal_parameter import BBH_FIELDS_PROPERTIES
from ..forms.data.data_open import DATA_FIELDS_PROPERTIES as OPEN_DATA_FIELDS_PROPERTIES
from ..forms.data.data_simulated import DATA_FIELDS_PROPERTIES as SIMULATED_DATA_FIELDS_PROPERTIES
from ..forms.sampler.sampler_dynesty import DYNESTY_FIELDS_PROPERTIES
from ..forms.sampler.sampler_nestle import NESTLE_FIELDS_PROPERTIES
from ..forms.sampler.sampler_emcee import EMCEE_FIELDS_PROPERTIES


class TupakJob(object):

    job = None
    data = None
    data_parameters = None
    signal = None
    signal_parameters = None
    priors = None
    sampler = None
    sampler_parameters = None

    def __init__(self, job_id):
        # populating data tab information
        try:
            self.data = Data.objects.get(job=self.job)
        except Data.DoesNotExist:
            pass
        else:
            self.data_parameters = []
            # finding the correct data parameters for the data type
            all_data_parameters = DataParameter.objects.filter(data=self.data)

            if self.data.data_choice == Data.OPEN_DATA:
                for name in OPEN_DATA_FIELDS_PROPERTIES.keys():
                    self.data_parameters.append(all_data_parameters.get(name=name))
            elif self.data.data_choice == Data.SIMULATED_DATA:
                for name in SIMULATED_DATA_FIELDS_PROPERTIES.keys():
                    self.data_parameters.append(all_data_parameters.get(name=name))

        # populating signal tab information
        try:
            self.signal = Signal.objects.get(job=self.job)
        except Signal.DoesNotExist:
            pass
        else:
            self.signal_parameters = []
            self.priors = []
            # finding the correct signal parameters for the signal type
            all_signal_parameters = SignalParameter.objects.filter(signal=self.signal)
            for name in BBH_FIELDS_PROPERTIES.keys():
                self.signal_parameters.append(all_signal_parameters.get(name=name))

            # populating prior
            for signal_parameter in all_signal_parameters:
                try:
                    prior = Prior.objects.get(signal_parameter=signal_parameter)
                    self.priors.append(prior)
                except Prior.DoesNotExist:
                    # this can happen when user just filled up the signal parameters
                    # yet to fill up the prior form
                    pass

        # populating sampler tab information
        try:
            self.sampler = Sampler.objects.get(job=self.job)
        except Sampler.DoesNotExist:
            pass
        else:
            self.sampler_parameters = []
            # finding the correct sampler parameters for the sampler type
            all_sampler_parameters = SamplerParameter.objects.filter(sampler=self.sampler)

            if self.sampler.sampler_choice == Sampler.DYNESTY:
                for name in DYNESTY_FIELDS_PROPERTIES.keys():
                    self.sampler_parameters.append(all_sampler_parameters.get(name=name))
            elif self.sampler.sampler_choice == Sampler.NESTLE:
                for name in NESTLE_FIELDS_PROPERTIES.keys():
                    self.sampler_parameters.append(all_sampler_parameters.get(name=name))
            elif self.sampler.sampler_choice == Sampler.EMCEE:
                for name in EMCEE_FIELDS_PROPERTIES.keys():
                    self.sampler_parameters.append(all_sampler_parameters.get(name=name))

        self.as_json()

    def __new__(cls, *args, **kwargs):
        try:
            cls.job = Job.objects.get(id=kwargs.get('job_id', None))
        except Job.DoesNotExist:
            return None

        return super(TupakJob, cls).__new__(cls)

    def as_json(self):
        # data_dict
        data_dict = dict()
        if self.data:
            data_dict.update({
                'type': self.data.data_choice,
            })
            for data_parameter in self.data_parameters:
                data_dict.update({
                    data_parameter.name: data_parameter.value,
                })

        # signal_dict
        signal_dict = dict()
        if self.signal:
            signal_dict.update({
                'type': self.signal.signal_choice,
            })
            for signal_parameter in self.signal_parameters:
                signal_dict.update({
                    signal_parameter.name: signal_parameter.value,
                })

        # prior dict
        priors_dict = dict()
        if self.priors:
            for prior in self.priors:
                prior_dict = dict()
                prior_dict.update({
                    'type': prior.prior_choice,
                })
                if prior.prior_choice == Prior.FIXED:
                    prior_dict.update({
                        'value': prior.fixed_value,
                    })
                elif prior.prior_choice == Prior.UNIFORM:
                    prior_dict.update({
                        'min': prior.uniform_min_value,
                        'max': prior.uniform_max_value,
                    })
                priors_dict.update({
                    prior.signal_parameter.name: prior_dict,
                })

        # sampler_dict
        sampler_dict = dict()
        if self.sampler:
            sampler_dict.update({
                'type': self.sampler.sampler_choice,
            })
            for sampler_parameter in self.sampler_parameters:
                sampler_dict.update({
                    sampler_parameter.name: sampler_parameter.value,
                })

        json_dict = dict(
            name=self.job.name,
            description=self.job.description,
            data=data_dict,
            signal=signal_dict,
            priors=priors_dict,
            sampler=sampler_dict,
        )

        return json.dumps(json_dict, indent=4)
