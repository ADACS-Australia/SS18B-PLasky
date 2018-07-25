from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.index, name='about'),
    path('new_job/', views.index, name='job_start'),
    path('jobs/', views.index, name='job_list'),
]
