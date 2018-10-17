"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import logging

from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from . import constants
from .models import Verification

logger = logging.getLogger(__name__)


def get_email_verification_expiry():
    """Finds the email verification expiry and then returns it.

    :return: Number
    """
    try:
        return settings.EMAIL_VERIFICATION_EXPIRY
    except AttributeError:
        return constants.EMAIL_VERIFICATION_EXPIRY


def get_absolute_site_url(request=None):
    """
    Finds the site url that will be used to generate links
    :param request: A Django request object
    :return: String of the absolute url
    """

    # check whether forcefully using a specific url from the settings
    if settings.SITE_URL != '':
        return settings.SITE_URL

    # If no request, an absolute url cannot be generated
    if not request:
        return None

    # find the site name and protocol
    site_name = request.get_host()
    if request.is_secure():
        protocol = 'https'
    else:
        try:
            # Look for protocol forcefully defined in the settings
            protocol = settings.HTTP_PROTOCOL
        except AttributeError:
            protocol = 'http'
    return protocol + '://' + site_name


def get_token(information, validity=None):
    """
    Stores the information in the database and generates a corresponding token
    :param information: information that needs to be stored and corresponding token to be generated
    :param validity: for how long the token will be valid (in seconds)
    :return: token to be encoded in the url
    """
    if validity:
        now = timezone.localtime(timezone.now())
        expiry = now + timedelta(seconds=validity)
    else:
        expiry = None
    try:
        verification = Verification.objects.create(information=information, expiry=expiry)
        return verification.id.__str__()
    except:
        logger.info("Failure generating Verification token with {}".format(information))
        raise


def get_information(token):
    """
    Retrieves the information from the database for a particular token

    :param token: encoded token from email
    :return: the actual information
    """
    now = timezone.localtime(timezone.now())
    try:
        verification = Verification.objects.get(id=token, expiry__gte=now)
        if verification.verified:
            raise ValueError('Already verified')
        else:
            verification.verified = True
            verification.save()
        return verification.information
    except Verification.DoesNotExist:
        raise ValueError('Invalid or expired verification code')
    except Exception as e:
        logger.exception(e)  # should notify admins via email
        raise
