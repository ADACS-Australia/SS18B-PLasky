from django.test import (
    TestCase,
    Client,
)

from django.urls import reverse
from http import HTTPStatus
from testfixtures.logcapture import LogCapture

from ..utility.display_names import PUBLIC
from ..models import (
    Job,
    JobStatus,
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


class TestJobCopy(TestCase):
    client = None

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.data = TestData()
        cls.members = get_members()
        cls.admins = get_admins()

    def test_non_member(self):
        """
        Test a non member or not logged in user cannot copy the job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        response = self.client.get(reverse('copy_job', kwargs={'job_id': job.id}))

        # redirected to login
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue('/login/' in response.url)

    def test_other_member(self):
        """
        Test other members cannot copy a private job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.force_login(self.members[1])

        response = self.client.get(reverse('copy_job', kwargs={'job_id': job.id}))

        # 404 page displayed
        self.assertTemplateUsed(response, 'bilbyweb/error_404.html')

    def test_job_owner(self):
        """
        Test job owner can copy a job
        """
        # remove all drafts for the user for checking
        Job.objects.filter(job_status=JobStatus.DRAFT, user=self.members[0]).delete()

        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            job_status=JobStatus.COMPLETED,
            user=self.members[0],
        )

        self.client.force_login(self.members[0])

        response = self.client.get(reverse('copy_job', kwargs={'job_id': job.id}))

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        # check draft job has been created
        self.assertEquals(Job.objects.filter(job_status=JobStatus.DRAFT, user=self.members[0]).exists(), True)

    def test_admin(self):
        """
        Test admin can copy a job
        """
        # remove all drafts for the user for checking
        Job.objects.filter(job_status=JobStatus.DRAFT, user=self.admins[0]).delete()

        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            job_status=JobStatus.COMPLETED,
            user=self.members[0],
        )

        self.client.force_login(self.admins[0])

        response = self.client.get(reverse('copy_job', kwargs={'job_id': job.id}))

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        # check draft job has been created
        self.assertEquals(Job.objects.filter(job_status=JobStatus.DRAFT, user=self.admins[0]).exists(), True)

    def test_members_can_copy_public_job(self):
        """
        Test any logged in user can copy a public
        """
        # remove all drafts for the user for checking
        Job.objects.filter(job_status=JobStatus.DRAFT, user=self.members[1]).delete()

        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            job_status=JobStatus.COMPLETED,
            extra_status=PUBLIC,
            user=self.members[0],
        )

        self.client.force_login(self.members[1])

        response = self.client.get(reverse('copy_job', kwargs={'job_id': job.id}))

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        # check draft job has been created
        self.assertEquals(Job.objects.filter(job_status=JobStatus.DRAFT, user=self.members[1]).exists(), True)

    def test_job_name_error(self):
        """
        Test job owner can copy a job
        """
        # remove all drafts for the user for checking
        Job.objects.filter(job_status=JobStatus.DRAFT, user=self.members[0]).delete()

        job_name = 'a' * 255
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            job_status=JobStatus.COMPLETED,
            user=self.members[0],
        )

        self.client.force_login(self.members[0])

        with LogCapture() as logger:
            response = self.client.get(reverse('copy_job', kwargs={'job_id': job.id}))

        logger.check(
            ('bilbyweb.views.job.jobs',
             'INFO',
             'Cannot copy job due to name length, job id: {}'.format(job.id)),
        )

        self.assertEquals(response.status_code, HTTPStatus.OK)

        # check draft job has NOT been created
        self.assertEquals(Job.objects.filter(job_status=JobStatus.DRAFT, user=self.members[0]).exists(), False)

        # 404 page displayed
        self.assertTemplateUsed(response, 'bilbyweb/error_404.html')


class TestJobEdit(TestCase):
    client = None

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.data = TestData()
        cls.members = get_members()
        cls.admins = get_admins()

    def test_non_member(self):
        """
        Test a non member or not logged in user cannot edit the job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        response = self.client.get(reverse('edit_job', kwargs={'job_id': job.id}))

        # redirected to login
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue('/login/' in response.url)

    def test_other_member(self):
        """
        Test other members cannot edit a private job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.force_login(self.members[1])

        response = self.client.get(reverse('edit_job', kwargs={'job_id': job.id}))

        # 404 page displayed
        self.assertTemplateUsed(response, 'bilbyweb/error_404.html')

    def test_job_owner(self):
        """
        Test job owner can edit a job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            job_status=JobStatus.DRAFT,
            user=self.members[0],
        )

        self.client.force_login(self.members[0])

        response = self.client.get(reverse('edit_job', kwargs={'job_id': job.id}))

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_admin(self):
        """
        Test admin can edit a job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            job_status=JobStatus.DRAFT,
            user=self.members[0],
        )

        self.client.force_login(self.admins[0])

        response = self.client.get(reverse('edit_job', kwargs={'job_id': job.id}))

        self.assertEquals(response.status_code, HTTPStatus.FOUND)


class TestJobCancel(TestCase):
    client = None

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.data = TestData()
        cls.members = get_members()
        cls.admins = get_admins()

    def test_non_member(self):
        """
        Test a non member or not logged in user cannot cancel a job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        response = self.client.get(reverse('cancel_job', kwargs={'job_id': job.id}))

        # redirected to login
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue('/login/' in response.url)

    def test_other_member(self):
        """
        Test other members cannot cancel a private job
        """
        job_name = 'a job'
        job_description = 'a job description'

        job = Job.objects.create(
            name=job_name,
            description=job_description,
            user=self.members[0],
        )

        self.client.force_login(self.members[1])

        response = self.client.get(reverse('cancel_job', kwargs={'job_id': job.id}))

        # 404 page displayed
        self.assertTemplateUsed(response, 'bilbyweb/error_404.html')
