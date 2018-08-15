from ..models import (
    Job,
    Data,
    DataSimulated,
    DataOpen,
)


class TupakJob:

    job = None
    data = None
    data_simulated = None
    data_open = None

    def __init__(self, job_id):
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

    def __new__(cls, *args, **kwargs):
        try:
            cls.job = Job.objects.get(id=kwargs.get('job_id', None))
        except Job.DoesNotExist:
            return None

        return super(TupakJob, cls).__new__(cls)
