from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views

from .forms.password_reset import PasswordResetCustomForm
from .forms.password_change import PasswordChangeCustomForm
from .views import registration, profile, verify

urlpatterns = [
    path('register/', registration, name='register'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'),
         name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('profile/', profile, name='profile'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             form_class=PasswordChangeCustomForm,
             template_name='accounts/registration/password_change.html',
         ), name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/registration/password_change_done.html',
         ), name='password_change_done'),
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
         ), name='password_reset_done', ),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             form_class=PasswordResetCustomForm,
             template_name='accounts/registration/password_reset_confirm.html',
         ), name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/registration/password_reset_complete.html',
         ), name='password_reset_complete'),
    path('verify/', verify, name='verify_account'),
]
