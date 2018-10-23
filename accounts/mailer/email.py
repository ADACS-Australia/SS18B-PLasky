"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Template
from django.template.context import Context
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

import logging

logger = logging.getLogger(__name__)


class Email:
    """
    Class for sending emails
    """

    def __init__(self, subject, to_addresses, template, context=None, from_address=None, cc=None, bcc=None):
        """
        Initializes an Email object
        :param subject: Subject of the email
        :param to_addresses: A list of email addresses
        :param template: A template of the email body
        :param context: A dictionary to render the template variables
        :param from_address: Sender of the email (email address)
        :param cc: A list of email addresses
        :param bcc: A list of email addresses
        """
        self.subject = subject
        self.to_addresses = to_addresses

        if type(context) == dict:
            context = Context(context)
            self.html_content = Template(template).render(context)
        else:
            self.html_content = template

        self.text_content = mark_safe(strip_tags(self.html_content))

        self.from_address = settings.EMAIL_FROM if not from_address else from_address
        self.cc = cc
        self.bcc = bcc

    def send_email(self):
        """
        Sends the actual email
        :return: Nothing
        """

        # creates the email
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.text_content,
            from_email=self.from_address,
            to=self.to_addresses,
            bcc=self.bcc,
            cc=self.cc,
            reply_to=[self.from_address, ],
        )

        # set the email as an HTML email
        email.attach_alternative(self.html_content, 'text/html')

        # sends the email
        email.send(fail_silently=False)
