"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.test import (
    TestCase,
    Client,
)
from django.urls import reverse
from http import HTTPStatus

from testfixtures.logcapture import LogCapture

from ..models import Job
from .utility import TestData, get_admins, get_members, PASSWORD_MEMBER


class TestNewJob(TestCase):
    client = None

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.data = TestData()
        cls.members = get_members()
        cls.admins = get_admins()

    def test_new_job_without_login(self):
        response = self.client.get(reverse('new_job'))
        # should redirect to login page
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual('login/?next=/new_job' in response.url, True)

    def test_new_job_logged_in_ok(self):
        self.client.login(username=self.members[0].username, password=PASSWORD_MEMBER)
        response = self.client.get(reverse('new_job'))
        # should not redirect to login page
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_new_job_start(self):
        self.client.login(username=self.members[0].username, password=PASSWORD_MEMBER)
        response = self.client.post(reverse('new_job'), data={
            'start-name': 'a job',
            'start-description': 'a job description',
        })

        self.assertEqual(response.status_code, HTTPStatus.OK)

        # checkout the created job
        created_job = Job.objects.get(name='a job', user=self.members[0])
        self.assertEqual(created_job.description, 'a job description')

    def test_new_job_duplicate_name(self):
        job_name = 'a job'
        job_description = 'a job description'

        Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.login(username=self.members[0].username, password=PASSWORD_MEMBER)

        with LogCapture() as logger:
            # try using the same name and description
            response = self.client.post(reverse('new_job'), data={
                'start-name': job_name,
                'start-description': job_description,
            })

        logger.check(('bilbyweb.forms.start', 'INFO', 'You already have a job with the same name'), )

        self.assertEqual(response.status_code, HTTPStatus.OK)
