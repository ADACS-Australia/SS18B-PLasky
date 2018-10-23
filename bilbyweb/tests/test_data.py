"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.test import (
    TestCase,
    Client,
)
from django.urls import reverse
from http import HTTPStatus

from ..models import (
    Job,
    Data,
    DataParameter,
)
from .utility import TestData, get_admins, get_members, PASSWORD_MEMBER


class TestDataForm(TestCase):
    client = None

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.data = TestData()
        cls.members = get_members()
        cls.admins = get_admins()

    def test_data_form_invalid_choice(self):
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.login(username=self.members[0].username, password=PASSWORD_MEMBER)

        response = self.client.post(reverse('new_job'), data={
            'form-tab': 'data',
            'data-data_choice': 'bingo',
        })

        # check error exists in the response
        self.assertTrue(
            '<ul class="errorlist"><li>Select a valid choice. bingo is not one of the available choices.</li></ul>' in
            str(response.content)
        )

        # status would be OK anyhow
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # check there is no data created for the form
        data_created = Data.objects.filter(job=job).exists()
        self.assertEquals(data_created, False)

    def test_data_form_invalid_data_simulated(self):
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.login(username=self.members[0].username, password=PASSWORD_MEMBER)

        response = self.client.post(reverse('new_job'), data={
            'form-tab': 'data',
            'data-data_choice': 'simulated',
        })

        # check error exists in the response
        self.assertTrue(
            '<ul class="errorlist"><li>This field is required.</li></ul>' in
            str(response.content)
        )

        # status would be OK anyhow
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # check there is no data created for the form
        data_created = Data.objects.filter(job=job).exists()
        self.assertEquals(data_created, False)

    def test_data_form_valid(self):
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.login(username=self.members[0].username, password=PASSWORD_MEMBER)

        # forcefully setting up the session
        session = self.client.session
        session['draft_job'] = {'id': job.pk, 'value': {}}
        session.save()

        response = self.client.post(reverse('new_job'), data={
            'form-tab': 'data',
            'data-data_choice': 'simulated',
            'data-simulated-detector_choice': 'hanford',
            'data-simulated-signal_duration': 2,
            'data-simulated-sampling_frequency': 2,
            'data-simulated-start_time': 2.1,
        })

        # status would be OK
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # check data created for the form
        data_created = Data.objects.filter(job=job)
        self.assertEquals(data_created.exists(), True)

        # check data parameters are created for the form
        data_parameter_created = DataParameter.objects.filter(data=data_created[0]).exists()
        self.assertEquals(data_parameter_created, True)
