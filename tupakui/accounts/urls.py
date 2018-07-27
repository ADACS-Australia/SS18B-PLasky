from django.urls import path
from django.contrib.auth import views as auth_views

from .views import registration, profile

urlpatterns = [
    path('register/', registration, name='register'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/', profile, name='change_password'),
]
