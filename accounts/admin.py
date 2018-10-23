"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Verification

# Registering the models for the admin interface to view.
admin.site.register(get_user_model())
admin.site.register(Verification)
