import json
import uuid

from ..utility.display_names import (
    OPEN_DATA,
    SIMULATED_DATA,
    BINARY_BLACK_HOLE,
    DYNESTY,
    NESTLE,
    EMCEE,
    FIXED,
    UNIFORM,
    SKIP,
    SUBMITTED,
    QUEUED,
    IN_PROGRESS,
    PUBLIC,
    DRAFT,
    COMPLETED,
    DELETED,
)

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


def clone_job_data(from_job, to_job):
    # cloning data and data parameters
    try:
        from_data = Data.objects.get(job=from_job)
        data_created = Data.objects.create(
            job=to_job,
            data_choice=from_data.data_choice,
        )
    except Data.DoesNotExist:
        pass
    else:
        # creating the data parameters
        data_parameters = DataParameter.objects.filter(data=from_data)

        for data_parameter in data_parameters:
            DataParameter.objects.create(
                data=data_created,
                name=data_parameter.name,
                value=data_parameter.value,
            )

    # cloning signal and signal parameters
    try:
        from_signal = Signal.objects.get(job=from_job)
        signal_created = Signal.objects.create(
            job=to_job,
            signal_choice=from_signal.signal_choice,
            signal_model=from_signal.signal_model,
        )
    except Signal.DoesNotExist:
        pass
    else:
        # creating the signal parameters
        signal_parameters = SignalParameter.objects.filter(signal=from_signal)

        for signal_parameter in signal_parameters:
            SignalParameter.objects.create(
                signal=signal_created,
                name=signal_parameter.name,
                value=signal_parameter.value,
            )

    # populating prior
    priors = Prior.objects.filter(job=from_job)
    for prior in priors:
        Prior.objects.create(
            job=to_job,
            name=prior.name,
            prior_choice=prior.prior_choice,
            fixed_value=prior.fixed_value,
            uniform_min_value=prior.uniform_min_value,
            uniform_max_value=prior.uniform_max_value,
        )

    # cloning sampler and sampler parameters
    try:
        from_sampler = Sampler.objects.get(job=from_job)
        sampler_created = Sampler.objects.create(
            job=to_job,
            sampler_choice=from_sampler.sampler_choice,
        )
    except Sampler.DoesNotExist:
        pass
    else:
        # creating the sampler parameters
        sampler_parameters = SamplerParameter.objects.filter(sampler=from_sampler)

        for sampler_parameter in sampler_parameters:
            SamplerParameter.objects.create(
                sampler=sampler_created,
                name=sampler_parameter.name,
                value=sampler_parameter.value,
            )


class BilbyJob(object):
    job = None
    data = None
    data_parameters = None
    signal = None
    signal_parameters = None
    priors = None
    sampler = None
    sampler_parameters = None

    # what actions a user can perform on this job
    job_actions = None

    def clone_as_draft(self, user):
        if not self.job:
            return

        name = self.job.name
        while Job.objects.filter(user=user, name=name).exists():
            name = (self.job.name + '_' + uuid.uuid4().hex)[:255]

            if name == self.job.name:
                # cannot generate a new name, returning none
                return None

        cloned = Job.objects.create(
            name=name,
            user=user,
            description=self.job.description,
        )

        clone_job_data(self.job, cloned)

        return cloned

    def list_actions(self, user):
        self.job_actions = []
        if self.job.user == user or user.is_admin():

            # any job can be copied
            self.job_actions.append('copy')

            # job can only be deleted if not in the following status:
            # 1. submitted
            # 2. queued
            # 3. in progress
            if self.job.status not in [SUBMITTED, QUEUED, IN_PROGRESS, DELETED]:
                self.job_actions.append('delete')

            # edit a job if it is a draft
            if self.job.status in [DRAFT]:
                self.job_actions.append('edit')

            # completed job can be public and vice versa
            if self.job.status in [COMPLETED]:
                self.job_actions.append('make_it_public')
            elif self.job.status in [PUBLIC]:
                self.job_actions.append('make_it_private')

        else:
            # non admin and non owner can copy a PUBLIC job
            if self.job.status in [PUBLIC]:
                self.job_actions.append('copy')

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

            if self.data.data_choice == OPEN_DATA:
                for name in OPEN_DATA_FIELDS_PROPERTIES.keys():
                    self.data_parameters.append(all_data_parameters.get(name=name))
            elif self.data.data_choice == SIMULATED_DATA:
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
            if self.signal.signal_choice == BINARY_BLACK_HOLE:
                for name in BBH_FIELDS_PROPERTIES.keys():
                    self.signal_parameters.append(all_signal_parameters.get(name=name))

        # populating prior
        # self.priors = Prior.objects.filter(job=self.job)
        # would be suffice if ordering is not required
        # however for displaying the fields in order the following have been added
        all_priors = Prior.objects.filter(job=self.job)
        if all_priors.exists():
            if self.signal and self.signal.signal_model == BINARY_BLACK_HOLE:
                for name in BBH_FIELDS_PROPERTIES.keys():
                    self.priors.append(all_priors.get(name=name))

        # populating sampler tab information
        try:
            self.sampler = Sampler.objects.get(job=self.job)
        except Sampler.DoesNotExist:
            pass
        else:
            self.sampler_parameters = []
            # finding the correct sampler parameters for the sampler type
            all_sampler_parameters = SamplerParameter.objects.filter(sampler=self.sampler)

            if self.sampler.sampler_choice == DYNESTY:
                for name in DYNESTY_FIELDS_PROPERTIES.keys():
                    self.sampler_parameters.append(all_sampler_parameters.get(name=name))
            elif self.sampler.sampler_choice == NESTLE:
                for name in NESTLE_FIELDS_PROPERTIES.keys():
                    self.sampler_parameters.append(all_sampler_parameters.get(name=name))
            elif self.sampler.sampler_choice == EMCEE:
                for name in EMCEE_FIELDS_PROPERTIES.keys():
                    self.sampler_parameters.append(all_sampler_parameters.get(name=name))

        self.as_json()

    def __new__(cls, *args, **kwargs):
        try:
            cls.job = Job.objects.get(id=kwargs.get('job_id', None))
        except Job.DoesNotExist:
            return None

        return super(BilbyJob, cls).__new__(cls)

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
        if self.signal and self.signal.signal_choice != SKIP:
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
                if prior.prior_choice == FIXED:
                    prior_dict.update({
                        'value': prior.fixed_value,
                    })
                elif prior.prior_choice == UNIFORM:
                    prior_dict.update({
                        'min': prior.uniform_min_value,
                        'max': prior.uniform_max_value,
                    })
                priors_dict.update({
                    prior.name: prior_dict,
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