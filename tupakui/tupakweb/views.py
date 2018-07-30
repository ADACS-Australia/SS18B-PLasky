from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .views import job_globals

def index(request):
    return render(
        request,
        "tupakweb/welcome.html",
    )

@login_required
def job_start(request):
    return render(
        request,
        "tupakweb/welcome.html",
    )
