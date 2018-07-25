from django.shortcuts import render

from .forms.registation import RegistrationForm


def registration(request):
    data = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()

            # # generating verification link
            # verification_link = get_absolute_site_url(request) + \
            #                     '/verify?verification_code=' + \
            #                     get_token(
            #                         information='type=user&username={}'.format(data.get('username')),
            #                         validity=constants.EMAIL_VERIFY_EXPIRY,
            #                     )
            #
            # # Sending email to the potential user to verify the email address
            # email_verify_request(
            #     to_addresses=[data.get('email')],
            #     title=data.get('title'),
            #     first_name=data.get('first_name'),
            #     last_name=data.get('last_name'),
            #     link=verification_link,
            # )

            return render(
                request,
                "accounts/notification.html",
                {
                    'type': 'registration_submitted',
                    'data': data,
                },
            )
    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/registration.html",
        {
            'form': form,
            'data': data,
            'submit_text': 'Register',
        },
    )


def profile(request):
    return render(
        request,
        "accounts/registration.html",
        {
            'submit_text': 'Register',
        },
    )
