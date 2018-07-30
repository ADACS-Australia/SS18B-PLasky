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
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.text_content,
            from_email=self.from_address,
            to=self.to_addresses,
            bcc=self.bcc,
            cc=self.cc,
            reply_to=[self.from_address, ],
        )

        email.attach_alternative(self.html_content, 'text/html')
        email.send(fail_silently=False)
