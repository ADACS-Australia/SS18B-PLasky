"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

# Templates for different emails
VERIFY_EMAIL_ADDRESS = dict()
VERIFY_EMAIL_ADDRESS['subject'] = '[BILBY-WEB] Please verify your email address'
VERIFY_EMAIL_ADDRESS['message'] = '<p>Dear {{first_name}} {{last_name}}: </p>' \
                                  '<p>We have received a new account request with our BILBY-WEB system from this ' \
                                  'email address. Please verify your email address by clicking on the following ' \
                                  '<a href="{{link}}" target="_blank">link</a>: </p>' \
                                  '<p><a href="{{link}}" target="_blank">{{link}}</a> </p>' \
                                  '<p>If you believe that the email has been sent by mistake or you have not ' \
                                  'requested for an account please <strong>do not</strong> click on the link. </p>' \
                                  '<p>Alternatively you can report this incident to <a ' \
                                  'href="mailto:paul.lasky@monash.edu" target="_top">paul.lasky@monash.edu</a> for ' \
                                  'investigation. </p>' \
                                  '<p> </p>' \
                                  '<p>Regards, </p>' \
                                  '<p>BILBY Team</p>'
