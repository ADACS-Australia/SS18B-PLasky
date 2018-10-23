"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User model extending AbstractUser
    """
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    institution = models.CharField(max_length=100)

    IS_ADMIN = 'Admin'
    IS_USER = 'User'
    ROLE_CHOICES = [
        (IS_ADMIN, IS_ADMIN),
        (IS_USER, IS_USER),
    ]
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default=IS_USER, blank=False)

    UNVERIFIED = 'Unverified'
    VERIFIED = 'Verified'
    CONFIRMED = 'Confirmed'
    DELETED = 'Deleted'
    STATUS_CHOICES = [
        (UNVERIFIED, UNVERIFIED),
        (VERIFIED, VERIFIED),
        (CONFIRMED, CONFIRMED),
        (DELETED, DELETED),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=False, default=UNVERIFIED)

    def is_admin(self):
        """
        Checks whether a user is an admin or not
        :return: True or False
        """
        return self.role == self.IS_ADMIN

    def display_name(self):
        """
        Builds up the display name from the user name parts
        :return: String containing full name of the user
        """
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

    def __str__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.username)

    def as_json(self):
        return dict(
            id=self.id,
            value=dict(
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
            ),
        )


class Verification(models.Model):
    """
    Model to store information for email address verification.
    Can also be used for other verifications as well.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.CharField(max_length=1024)
    expiry = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return u'%s' % self.information
