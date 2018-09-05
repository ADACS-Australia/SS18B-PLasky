from django.conf import settings
from django.db import models


class Job(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_job', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    DRAFT = 'Draft'
    SUBMITTED = 'Submitted'
    QUEUED = 'Queued'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    ERROR = 'Error'
    SAVED = 'Saved'
    WALL_TIME_EXCEEDED = 'Wall Time Exceeded'
    DELETED = 'Deleted'
    STATUS_CHOICES = [
        (DRAFT, DRAFT),
        (SUBMITTED, SUBMITTED),
        (QUEUED, QUEUED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
        (ERROR, ERROR),
        (SAVED, SAVED),
        (WALL_TIME_EXCEEDED, WALL_TIME_EXCEEDED),
        (DELETED, DELETED),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=False, default=DRAFT)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    submission_time = models.DateTimeField(null=True, blank=True)
    json_representation = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (
            ('user', 'name'),
        )

    def __str__(self):
        return '{}'.format(self.name)

    def as_json(self):
        return dict(
            id=self.id,
            value=dict(
                name=self.name,
                username=self.user.username,
                status=self.status,
                creation_time=self.creation_time.strftime('%d %b %Y %I:%m %p'),
            ),
        )


def user_job_results_file_directory_path_not_field(instance):
    return settings.MEDIA_ROOT + 'user_{0}/job_{1}/result_files/'.format(instance.user.id, instance.id)


def user_job_input_file_directory_path(instance):
    return settings.MEDIA_ROOT + 'user_{0}/job_{1}/input_files/{2}'.format(instance.user.id, instance.id, "input.json")


def user_job_result_files_directory_path(instance, filename):
    return 'user_{0}/job_{1}/result_files/{2}'.format(instance.job.user_id, instance.job.id, filename)


class Data(models.Model):
    job = models.OneToOneField(Job, related_name='job_data', on_delete=models.CASCADE)

    SIMULATED_DATA = 'simulated'
    OPEN_DATA = 'open'

    DATA_CHOICES = [
        (SIMULATED_DATA, 'Simulated data'),
        (OPEN_DATA, 'Open data'),
    ]

    data_choice = models.CharField(max_length=20, choices=DATA_CHOICES, default=SIMULATED_DATA)

    def __str__(self):
        return '{} ({})'.format(self.data_choice, self.job.name)

    def as_json(self):
        return dict(
            id=self.id,
            value=dict(
                job=self.job.id,
                choice=self.data_choice,
            ),
        )


class DataParameter(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=False, null=False)
    value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{} - {} ({})'.format(self.name, self.value, self.data)


class Signal(models.Model):
    job = models.OneToOneField(Job, related_name='job_signal', on_delete=models.CASCADE)

    SKIP = 'skip'
    BINARY_BLACK_HOLE = "binary_black_hole"

    SIGNAL_CHOICES = [
        (SKIP, 'None'),
        (BINARY_BLACK_HOLE, 'Binary Black Hole'),
    ]

    signal_choice = models.CharField(max_length=50, choices=SIGNAL_CHOICES, default=SKIP)

    def __str__(self):
        return '{} - ({}[{}])'.format(self.signal_choice, self.job.name, self.job.user.username)


class SignalParameter(models.Model):
    signal = models.ForeignKey(Signal, related_name='signal_signal_parameter', on_delete=models.CASCADE)

    MASS1 = 'mass_1'
    MASS2 = 'mass_2'
    LUMINOSITY_DISTANCE = 'luminosity_distance'
    IOTA = 'iota'
    PSI = 'psi'
    PHASE = 'phase'
    MERGER_TIME = 'merger_time'
    RA = 'ra'
    DEC = 'dec'

    NAME_CHOICES = [
        (MASS1, 'Mass 1 (M☉)'),
        (MASS2, 'Mass 2 (M☉)'),
        (LUMINOSITY_DISTANCE, 'Luminosity distance (Mpc)'),
        (IOTA, 'iota'),
        (PSI, 'psi'),
        (PHASE, 'Phase'),
        (MERGER_TIME, 'Merger time (GPS time)'),
        (RA, 'Right ascension'),
        (DEC, 'Declination'),
    ]

    name = models.CharField(max_length=20, choices=NAME_CHOICES, blank=False, null=False)
    value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '{}: {} ({})'.format(self.name, self.value, self.signal)


class Prior(models.Model):
    signal_parameter = models.ForeignKey(SignalParameter, on_delete=models.CASCADE,
                                         related_name='signal_parameter_prior')
    FIXED = 'fixed'
    UNIFORM = 'uniform'
    CHOICES = [
        (FIXED, 'Fixed'),
        (UNIFORM, 'Uniform'),
    ]
    prior_choice = models.CharField(max_length=20, choices=CHOICES, default=FIXED, blank=True)
    fixed_value = models.FloatField(blank=True, null=True)
    uniform_min_value = models.FloatField(blank=True, null=True)
    uniform_max_value = models.FloatField(blank=True, null=True)

    def get_display_value(self):
        if self.prior_choice == self.FIXED:
            return '{}'.format(self.fixed_value)
        elif self.prior_choice == self.UNIFORM:
            return '[{}, {}]'.format(self.uniform_min_value, self.uniform_max_value)


class Sampler(models.Model):
    job = models.OneToOneField(Job, related_name='job_sampler', on_delete=models.CASCADE)

    DYNESTY = 'dynesty'
    NESTLE = 'nestle'

    SAMPLER_CHOICES = [
        (DYNESTY, 'Dynesty'),
        (NESTLE, 'Nestle'),
    ]

    sampler_choice = models.CharField(max_length=15, choices=SAMPLER_CHOICES, default=DYNESTY, blank=True)


class SamplerDynesty(models.Model):
    sampler = models.OneToOneField(Sampler, related_name='sampler_sampler_dynesty', on_delete=models.CASCADE)
    n_livepoints = models.IntegerField(null=True)


class SamplerNestle(models.Model):
    sampler = models.OneToOneField(Sampler, related_name='sampler_sampler_nestle', on_delete=models.CASCADE)
    n_steps = models.IntegerField(null=True)


class SamplerEmcee(models.Model):
    sampler = models.OneToOneField(Sampler, related_name='sampler_sampler_emcee', on_delete=models.CASCADE)
    n_steps = models.IntegerField(null=True)
