from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views

from .forms.password_reset import PasswordResetCustomForm
from .views import registration, profile, verify

urlpatterns = [
    path('register/', registration, name='register'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'),
         name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/', profile, name='change_password'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             from_email=settings.EMAIL_FROM,
             template_name='accounts/registration/password_reset_form.html',
             email_template_name='accounts/registration/password_reset_email.html',
             subject_template_name='accounts/registration/password_reset_subject.txt',
             html_email_template_name='accounts/registration/password_reset_email_html.html',

         ), name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/registration/password_reset_done.html',
         ), name='password_reset_done',),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             form_class=PasswordResetCustomForm,
             template_name='accounts/registration/password_reset_confirm.html',
         ), name='password_reset_confirm'),
    path('reset/done', auth_views.password_reset_complete, name='password_reset_complete'),
    path('verify/', verify, name='verify_account'),
]
