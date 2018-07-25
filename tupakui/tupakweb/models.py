from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from math import pi
# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _

from tupakui.accounts.models import User

class Job(models.Model):
    user = models.ForeignKey(User, related_name='user_job')
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
    submission_time = models.DateTimeField(null=True)

    class Meta:
        unique_together = (
            ('user', 'id'),
        )

    def __unicode__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def as_json(self):
        return dict(
            id=self.id,
            value=dict(
                name=self.name,
                # user=self.user,
                status=self.status,
                creation_time=self.creation_time.strftime('%d %b %Y %I:%m %p'),
            ),
        )

def user_job_results_file_directory_path_not_field(instance):
    """Not a model field instance handler
    """
    return settings.MEDIA_ROOT + 'user_{0}/job_{1}/result_files/'.format(instance.user.id, instance.id)

def user_job_input_file_directory_path(instance):
    """Not a model field instance handler
    """
    return settings.MEDIA_ROOT + 'user_{0}/job_{1}/input_files/{2}'.format(instance.user.id, instance.id, "input.json")

def user_job_result_files_directory_path(instance, filename):
    return 'user_{0}/job_{1}/result_files/{2}'.format(instance.job.user_id, instance.job.id, filename)


"""

TAB 1: DATA (related to either OpenData or SimulatedData)

"""
class Data(models.Model):
    """Data class
    """
    job = models.OneToOneField(Job, related_name='job_data')

    SIMULATED_DATA = 'simulated'
    OPEN_DATA = 'open'

    DATA_CHOICES = [
        (SIMULATED_DATA, 'Simulated data'),
        (OPEN_DATA, 'Open data'),
    ]

    data_choice = models.CharField(max_length=20, choices=DATA_CHOICES, default=SIMULATED_DATA, blank=True)

    class Meta:
        unique_together = (
            ('job', 'id'),
        )

class OpenData(models.Model):
    """OpenData class
    """
    data = models.OneToOneField(Data, related_name='data_open_data')

    HANFORD = 'hanford'
    LIVINGSTON = 'livingston'
    VIRGO = 'virgo'

    DETECTOR_CHOICES = [
        (HANFORD, 'Hanford'),
        (LIVINGSTON, 'Livingston'),
        (VIRGO, 'Virgo'),
    ]

    detector_choice = models.CharField(max_length=20, choices=DETECTOR_CHOICES, default=HANFORD, blank=True)
    signal_duration = models.IntegerField(blank=False, null=False, default=4, validators=[MinValueValidator(0)])
    sample_frequency = models.IntegerField(blank=False, null=False, default=2048, validators=[MinValueValidator(0)])
    start_time = models.FloatField(blank=False, default=0., validators=[MinValueValidator(0)])

    class Meta:
        unique_together = (
            ('data', 'id'),
        )


class SimulatedData(models.Model):
    """SimulatedData class
    """
    data = models.OneToOneField(Data, related_name='data_simulated_data')

    HANFORD = 'hanford'
    LIVINGSTON = 'livingston'
    VIRGO = 'virgo'

    DETECTOR_CHOICES = [
        (HANFORD, 'Hanford'),
        (LIVINGSTON, 'Livingston'),
        (VIRGO, 'Virgo'),
    ]

    detector_choice = models.CharField(max_length=20, choices=DETECTOR_CHOICES, default=HANFORD, blank=True)
    signal_duration = models.IntegerField(blank=False, null=False, default=4, validators=[MinValueValidator(0)])
    sample_frequency = models.IntegerField(blank=False, null=False, default=2048, validators=[MinValueValidator(0)])
    start_time = models.FloatField(blank=False, default=0., validators=[MinValueValidator(0)])

    class Meta:
        unique_together = (
            ('data', 'id'),
        )

"""

TAB 2: SignalInjection (current signal type is SignalBinaryBlackHole)

"""

class SignalInjection(models.Model):
    """SignalInjection class
    """

    # NOTE: Not sure yet if this should be related to job or data

    job = models.OneToOneField(Job, related_name='job_signal_injection')

    inject_or_not = models.BooleanField(default=False)

    BINARY_BLACK_HOLE = "bbh"

    SIGNAL_CHOICES = [
        (BINARY_BLACK_HOLE, 'Binary Black Hole'),
    ]

    SIGNAL_choice = models.CharField(max_length=50, choices=SIGNAL_CHOICES, default=BINARY_BLACK_HOLE, blank=True)

    class Meta:
        unique_together = (
            ('job', 'id'),
        )


class SignalBbh(models.Model):
    signal = models.OneToOneField(Job, related_name='signal_injection_signal_bbh')

    MASS1 = 'mass_1'

    NAME_CHOICES = [
        (MASS1, 'Mass 1'),
    ]

    name = models.CharField(max_length=20, choices=NAME_CHOICES, default=MASS1, blank=True)
    value = models.FloatField(null=True)
    prior_fixed = models.FloatField(null=True)
    prior_min = models.FloatField(null=True)
    prior_max = models.FloatField(null=True)

    class Meta:
        unique_together = (
            ('signal', 'id'),
        )


class Sampler(models.Model):
    job = models.OneToOneField(Job, related_name='job_sampler')

    DYNESTY = 'dynesty'
    NESTLE = 'nestle'

    SAMPLER_CATEGORY_CHOICES = [
        (DYNESTY, 'Dynesty'),
        (NESTLE, 'Nestle'),
    ]

    category = models.CharField(max_length=15, choices=SAMPLER_TYPE_CHOICES, default=DYNESTY, blank=True)

    NUMBER_OF_LIVE_POINTS = 'number_of_live_points'
    NUMBER_OF_STEPS = 'number_of_steps'
    NA = "not_applicable"

    SAMPLER_INPUT_NAME_CHOICES = [
        (NUMBER_OF_LIVE_POINTS, 'Number of live points'),
        (NUMBER_OF_STEPS, 'Number of steps'),
        (NA, "N/A"),
    ]

    sampler_input_name = models.CharField(max_length=20, choices=NAME_CHOICES, default=NA, blank=True)
    sampler_input_value = models.IntegerField(null=True)

    class Meta:
        unique_together = (
            ('job', 'id'),
        )

