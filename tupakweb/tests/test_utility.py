from django.test import (
    TestCase,
)

from ..utility.job import TupakJob

from ..models import Job
from .utility import TestData, get_members


class TestTupakJob(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = TestData()
        cls.members = get_members()

    def test_job_creation(self):
        job = Job.objects.create(
            user=self.members[0],
            name='a job',
            description='a job description',
        )

        t_job = TupakJob(job_id=job.id)
        self.assertNotEquals(t_job, None)
        self.assertEquals(t_job.job, job)

    def test_job_creation_invalid(self):
        Job.objects.create(
            user=self.members[0],
            name='a job',
            description='a job description',
        )

        t_job = TupakJob(job_id=-1)
        self.assertEquals(t_job, None)
