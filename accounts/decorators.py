"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.core.exceptions import PermissionDenied


def admin_or_system_admin_required(func):
    """
    Decorator to check whether a user is admin or staff or system admin
    :param func: Function to check
    :return: Wrap
    """
    def wrap(request, *args, **kwargs):
        if not request.user.is_admin() or not request.user.is_staff or not request.user.is_superuser:
            raise PermissionDenied
        else:
            return func(request, *args, **kwargs)

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    return wrap
