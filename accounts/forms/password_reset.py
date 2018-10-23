"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.contrib.auth.forms import SetPasswordForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation


class PasswordResetCustomForm(SetPasswordForm):
    """
    Extends Django default SetPasswordForm to apply bootstrap styles
    """
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("Re-type Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
