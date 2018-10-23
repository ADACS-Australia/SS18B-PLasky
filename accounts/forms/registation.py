"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from ..models import User

FIELDS = ['first_name', 'last_name', 'email', 'institution', 'username', ]

WIDGETS = {
    'first_name': forms.TextInput(
        attrs={'class': "form-control", 'tabindex': '1'},
    ),
    'last_name': forms.TextInput(
        attrs={'class': "form-control", 'tabindex': '2'},
    ),
    'email': forms.TextInput(
        attrs={'class': "form-control", 'tabindex': '3'},
    ),
    'institution': forms.TextInput(
        attrs={'class': "form-control", 'tabindex': '4'},
    ),
    'username': forms.TextInput(
        attrs={'class': "form-control", 'tabindex': '5'},
    ),
}

LABELS = {
    'first_name': _('First name'),
    'last_name': _('Last name'),
    'email': _('Email'),
    'institution': _('Institution'),
    'username': _('Username'),
}


class RegistrationForm(UserCreationForm):
    """
    Customise the User Registration form from default Django UserCreationForm
    """
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'tabindex': '6'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'tabindex': '7'})
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = get_user_model()
        fields = FIELDS
        labels = LABELS
        widgets = WIDGETS

    def clean_email(self):
        """
        Checks email address uniqueness which is not present in Django
        :return: Validation Error or email address
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This email address is already taken by some other user.')
        return email

    def save(self, commit=True):
        """
        Overrides the save method of Super class
        :param commit: Whether the User would be saved directly or not.
        :return: The saved user.
        """
        # Save the user as an inactive user
        # It will be active once the email address is verified by the User
        user = super(RegistrationForm, self).save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user
