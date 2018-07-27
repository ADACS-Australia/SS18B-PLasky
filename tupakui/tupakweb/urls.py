from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.index, name='about'),
    path('new_job/', login_required(views.index), name='job_start'),
    path('jobs/', views.index, name='job_list'),
]
