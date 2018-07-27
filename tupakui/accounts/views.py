from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms.profile import EditProfileForm
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


@login_required
def profile(request):
    data = {}
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            messages.success(request, 'Information successfully updated', 'alert alert-success')
            return render(
                request,
                "accounts/profile.html",
                {
                    'form': form,
                    'type': 'update_profile_success',
                    'data': data,
                },
            )
        else:
            messages.error(request, 'Please correct the error(s) below.', 'alert alert-warning')
    else:
        form = EditProfileForm(instance=request.user)

    return render(
        request,
        "accounts/profile.html",
        {
            'form': form,
            'data': data,
            'submit_text': 'Update',
        },
    )
