from ..models import (
    Job,
    Data,
    DataSimulated,
    DataOpen,
    Signal,
    SignalParameter,
)

from ..forms.signal.signal_parameter import BBH_FIELDS_PROPERTIES


class TupakJob:

    job = None
    data = None
    data_simulated = None
    data_open = None
    signal = None
    signal_parameters = None

    def __init__(self, job_id):
        # populating data tab information
        try:
            self.data = Data.objects.get(job=self.job)
        except Data.DoesNotExist:
            pass
        else:
            if self.data.data_choice == Data.SIMULATED_DATA:
                try:
                    self.data_simulated = DataSimulated.objects.get(job=self.job)
                except DataSimulated.DoesNotExist:
                    pass
            elif self.data.data_choice == Data.OPEN_DATA:
                try:
                    self.data_open = DataOpen.objects.get(job=self.job)
                except DataOpen.DoesNotExist:
                    pass

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
