from django.test import (
    TestCase,
    Client,
)
from django.urls import reverse
from http import HTTPStatus


from ..models import Job
from .utility import TestData, get_admins, get_members, PASSWORD_ADMIN, PASSWORD_MEMBER


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
