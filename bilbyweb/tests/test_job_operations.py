from django.test import (
    TestCase,
    Client,
)

from django.urls import reverse
from http import HTTPStatus

from ..utility.display_names import PUBLIC
from ..models import (
    Job,
)

from .utility import (
    TestData,
    get_admins,
    get_members,
)


class TestJobView(TestCase):
    client = None

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.data = TestData()
        cls.members = get_members()
        cls.admins = get_admins()

    def test_non_member(self):
        """
        Test a non member or not logged in user cannot view the job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        response = self.client.get(reverse('job', kwargs={'job_id': job.id}))

        # redirected to login
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue('/login/' in response.url)

    def test_other_member(self):
        """
        Test other members cannot view a job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.force_login(self.members[1])

        response = self.client.get(reverse('job', kwargs={'job_id': job.id}))

        # 404 page displayed
        self.assertTemplateUsed(response, 'bilbyweb/error_404.html')

    def test_job_owner(self):
        """
        Test job owner can view a job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.force_login(self.members[0])

        response = self.client.get(reverse('job', kwargs={'job_id': job.id}))

        # check view job template is used
        self.assertTemplateUsed(response, 'bilbyweb/job/view_job.html')

    def test_admin(self):
        """
        Test admin can view a job even it is private
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.force_login(self.admins[0])

        response = self.client.get(reverse('job', kwargs={'job_id': job.id}))

        # check view job template is used
        self.assertTemplateUsed(response, 'bilbyweb/job/view_job.html')

    def test_members_can_view_public_job(self):
        """
        Test members can view a public job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
            extra_status=PUBLIC,
        )

        self.client.force_login(self.members[1])

        response = self.client.get(reverse('job', kwargs={'job_id': job.id}))

        # check view job template is used
        self.assertTemplateUsed(response, 'bilbyweb/job/view_job.html')
