"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from __future__ import unicode_literals

from . import templates, email


def email_verify_request(to_addresses, first_name, last_name, link):
    """
    Sends out the email address verification email
    :param to_addresses: A list of addresses, in this case the user
    :param first_name: String
    :param last_name: String
    :param link: String containing the url to verify email address
    :return: Nothing
    """

    # setting up the context
    context = {
        'first_name': first_name,
        'last_name': last_name,
        'link': link,
    }

    # Building and sending emails
    email.Email(
        subject=templates.VERIFY_EMAIL_ADDRESS['subject'],
        to_addresses=to_addresses,
        template=templates.VERIFY_EMAIL_ADDRESS['message'],
        context=context,
    ).send_email()
