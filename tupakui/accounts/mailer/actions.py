from __future__ import unicode_literals

from . import templates, email


def email_verify_request(to_addresses, first_name, last_name, link):
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'link': link,
    }

    email.Email(
        subject=templates.VERIFY_EMAIL_ADDRESS['subject'],
        to_addresses=to_addresses,
        template=templates.VERIFY_EMAIL_ADDRESS['message'],
        context=context,
    ).send_email()
