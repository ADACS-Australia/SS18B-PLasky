"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

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
    DRAFT,
    COMPLETED,
    PENDING,
    ERROR,
    CANCELLED,
    WALL_TIME_EXCEEDED,
    OUT_OF_MEMORY,
    PUBLIC,
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
    """
    Copy job data across two jobs
    :param from_job: instance of Job that will be used as a source
    :param to_job: instance of Job that will be used as a target
    :return: Nothing
    """
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
    """
    Class representing a Bilby Job. The bilby job parameters are scattered in different models in the database.
    This class used to collects the correct job parameters in one place. It also defines the json representation
    of the job.
    """

    # variable to hold the Job model instance
    job = None

    # variable to hold the Data model instance
    data = None

    # list to hold the Data Parameters instances
    data_parameters = None

    # variable to hold the Signal instance
    signal = None

    # list to hold the Signal Parameters instances
    signal_parameters = None

    # list to hold the Prior instances
    priors = None

    # variable to hold the Sampler instance
    sampler = None

    # list to hold the Sampler Parameters instances
    sampler_parameters = None

    # what actions a user can perform on this job
    job_actions = None

    def clone_as_draft(self, user):
        """
        Clones the bilby job for the user as a Draft Job
        :param user: the owner of the new Draft Job
        :return: Nothing
        """

        if not self.job:
            return

        # try to generate a unique name for the job owner
        name = self.job.name
        while Job.objects.filter(user=user, name=name).exists():
            name = (self.job.name + '_' + uuid.uuid4().hex)[:255]

            # This will be true if the job has 255 Characters in it,
            # In this case, we cannot get a new name by adding something to it.
            # This can be altered later based on the requirement.
            if name == self.job.name:
                # cannot generate a new name, returning none
                return None

        # Once the name is set, creating the draft job with new name and owner and same description
        cloned = Job.objects.create(
            name=name,
            user=user,
            description=self.job.description,
        )

        # copying other parameters of the job
        clone_job_data(self.job, cloned)

        return cloned

    def list_actions(self, user):
        """
        List the actions a user can perform on this Job
        :param user: User for whom the actions will be generated
        :return: Nothing
        """

        self.job_actions = []

        # Job Owners and Admins get most actions
        if self.job.user == user or user.is_admin():

            # any job can be copied
            self.job_actions.append('copy')

            # job can only be deleted if in the following status:
            # 1. draft
            # 2. completed
            # 3. error (wall time and out of memory)
            # 4. cancelled
            # 5. public
            if self.job.status in [DRAFT, COMPLETED, ERROR, CANCELLED, WALL_TIME_EXCEEDED, OUT_OF_MEMORY, PUBLIC]:
                self.job_actions.append('delete')

            # edit a job if it is a draft
            if self.job.status in [DRAFT]:
                self.job_actions.append('edit')

            # cancel a job if it is not finished processing
            if self.job.status in [PENDING, SUBMITTED, QUEUED, IN_PROGRESS]:
                self.job_actions.append('cancel')

            # completed job can be public and vice versa
            if self.job.status in [COMPLETED]:
                self.job_actions.append('make_it_public')
            elif self.job.status in [PUBLIC]:
                self.job_actions.append('make_it_private')

        else:
            # non admin and non owner can copy a PUBLIC job
            if self.job.status in [PUBLIC]:
                self.job_actions.append('copy')

    def __init__(self, job_id, light=False):
        """
        Initialises the Bilby Job
        :param job_id: id of the job
        :param light: Whether used for only job variable to be initialised atm
        """
        # do not need to do further processing for light bilby jobs
        # it is used only for status check mainly from the model itself to list the
        # actions a user can do on the job
        if light:
            return

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

    def __new__(cls, *args, **kwargs):
        """
        Instantiate the Bilby Job
        :param args: arguments
        :param kwargs: keyword arguments
        :return: Instance of Bilby Job with job variable initialised from job_id if exists
                 otherwise returns None
        """
        result = super(BilbyJob, cls).__new__(cls)
        try:
            result.job = Job.objects.get(id=kwargs.get('job_id', None))
        except Job.DoesNotExist:
            return None
        return result

    def as_json(self):
        """
        Generates the json representation of the Bilby Job so that Bilby Core can digest it
        :return: Json Representation
        """

        # processing data dict
        data_dict = dict()
        if self.data:
            data_dict.update({
                'type': self.data.data_choice,
            })
            for data_parameter in self.data_parameters:
                data_dict.update({
                    data_parameter.name: data_parameter.value,
                })

        # processing signal dict
        signal_dict = dict()
        if self.signal and self.signal.signal_choice != SKIP:
            signal_dict.update({
                'type': self.signal.signal_choice,
            })
            for signal_parameter in self.signal_parameters:
                signal_dict.update({
                    signal_parameter.name: signal_parameter.value,
                })

        # processing prior dict
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

        # processing sampler dict
        sampler_dict = dict()
        if self.sampler:
            sampler_dict.update({
                'type': self.sampler.sampler_choice,
            })
            for sampler_parameter in self.sampler_parameters:
                sampler_dict.update({
                    sampler_parameter.name: sampler_parameter.value,
                })

        # accumulating all in one dict
        json_dict = dict(
            name=self.job.name,
            description=self.job.description,
            data=data_dict,
            signal=signal_dict,
            priors=priors_dict,
            sampler=sampler_dict,
        )

        # returning json with correct indentation
        return json.dumps(json_dict, indent=4)
