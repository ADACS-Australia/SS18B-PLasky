"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.shortcuts import render


def index(request):
    """
    Render the index view.
    :param request: Django request object.
    :return: Rendered template
    """
    return render(
        request,
        "bilbyweb/welcome.html",
    )


def about(request):
    """
    Render the about view.
    :param request: Django request object.
    :return: Rendered template
    """
    return render(
        request,
        'bilbyweb/about.html',
    )


def error_404_view(request, exception):
    """
    Render custom 404 page.
    :param request: Django request object.
    :return: Rendered template
    """
    data = {"name": "not used yet"}
    return render(request, 'bilbyweb/error_404.html', data)
