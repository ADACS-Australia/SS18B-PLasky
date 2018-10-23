"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

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
                attrs={'class': "form-control", 'tabindex': '5', 'readonly': True, },
            ),
        }

LABELS = {
    'first_name': _('First name'),
    'last_name': _('Last name'),
    'email': _('Email'),
    'institution': _('Institution'),
    'username': _('Username'),
}


class EditProfileForm(forms.ModelForm):
    """
    Model form to Edit Profile information
    """
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = get_user_model()
        fields = FIELDS
        labels = LABELS
        widgets = WIDGETS
