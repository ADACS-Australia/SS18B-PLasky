from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
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

    def __str__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.username)

    def as_json(self):
        return dict(
            user=self,
            id=self.id,
            value=dict(
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
            ),
        )
