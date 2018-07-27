import logging

from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from ..accounts import constants
from .models import Verification

logger = logging.getLogger(__name__)


def get_email_verification_expiry():
    """Finds the email verification expiry and then returns it.

    :return:
    """
    return settings.EMAIL_VERIFICATION_EXPIRY


def get_absolute_site_url(request):
    site_name = request.get_host()
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = settings.HTTP_PROTOCOL
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
