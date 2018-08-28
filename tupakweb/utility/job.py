from ..models import (
    Job,
    Data,
    Signal,
    SignalParameter,
    DataParameter)

from ..forms.signal.signal_parameter import BBH_FIELDS_PROPERTIES
from ..forms.data.data_open import DATA_FIELDS_PROPERTIES as OPEN_DATA_FIELDS_PROPERTIES
from ..forms.data.data_simulated import DATA_FIELDS_PROPERTIES as SIMULATED_DATA_FIELDS_PROPERTIES


class TupakJob:

    job = None
    data = None
    data_parameters = None
    signal = None
    signal_parameters = None

    def __init__(self, job_id):
        # populating data tab information
        try:
            self.data = Data.objects.get(job=self.job)
        except Data.DoesNotExist:
            pass
        else:
            self.data_parameters = []
            # finding the correct signal parameters for the signal type
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
            # finding the correct signal parameters for the signal type
            all_signal_parameters = SignalParameter.objects.filter(signal=self.signal)
            for name in BBH_FIELDS_PROPERTIES.keys():
                self.signal_parameters.append(all_signal_parameters.get(name=name))

    def __new__(cls, *args, **kwargs):
        try:
            cls.job = Job.objects.get(id=kwargs.get('job_id', None))
        except Job.DoesNotExist:
            return None

        return super(TupakJob, cls).__new__(cls)
