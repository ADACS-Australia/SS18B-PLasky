from django.db.models import Q

from accounts.models import User


PASSWORD_ADMIN = '@dM1nP@55W0rd'
PASSWORD_MEMBER = 'M3mbErP@55W0rd'


def get_admins():
    return User.objects.filter(Q(username='admin'))


def get_members():
    return User.objects.filter(~Q(username='admin'))


class TestData:
    def __init__(self):
        self.username_list = [
            'admin',
            'member',
            'member_two',
        ]

        self._create_users()

    def _create_users(self):
        users = []
        for username in self.username_list:
            user = User.objects.create(
                username=username,
                first_name=username + ' First Name',
                last_name=username + ' Last Name',
                email=username + '@localhost.com',
            )
            user.set_password(PASSWORD_ADMIN if username in ['admin', ] else PASSWORD_MEMBER)
            if username == 'admin':
                user.role = 'Admin'
            user.save()
            users.append(user)
