from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from six.moves.urllib import parse

from .forms.profile import EditProfileForm
from .forms.registation import RegistrationForm
from . import utility
from .models import User

from .mailer import actions


def registration(request):
    data = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()

            # generating verification link
            verification_link = utility.get_absolute_site_url(request) + '/accounts/verify?code=' + utility.get_token(
                                    information='type=user&username={}'.format(data.get('username')),
                                    validity=utility.get_email_verification_expiry(),
                                )

            # Sending email to the potential user to verify the email address
            actions.email_verify_request(
                to_addresses=[data.get('email')],
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                link=verification_link,
            )

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


def verify(request):
    data = {}
    code_encrypted = request.GET.get('code', None)
    if code_encrypted:
        try:
            code = utility.get_information(code_encrypted)
            params = dict(parse.parse_qsl(code))
            verify_type = params.get('type', None)
            if verify_type == 'user':
                username = params.get('username', None)
                try:
                    user = User.objects.get(username=username)
                    user.status = user.VERIFIED
                    user.is_active = True
                    user.save()
                    data.update(
                        success=True,
                        message='The email address has been verified successfully',
                    )
                except User.DoesNotExist:
                    data.update(
                        success=False,
                        message='The requested user account to verify does not exist',
                    )
        except ValueError as e:
                data.update(
                    success=False,
                    message=e if e else 'Invalid verification code',
                )
    else:
        data.update(
            success=False,
            message='Invalid Verification Code',
        )
    return render(
        request,
        "accounts/notification.html",
        {
            'type': 'email_verify',
            'data': data,
        },
    )
