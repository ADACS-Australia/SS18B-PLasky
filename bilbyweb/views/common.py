from django.shortcuts import render


def index(request):
    return render(
        request,
        "bilbyweb/welcome.html",
    )


def about(request):
    return render(
        request,
        'bilbyweb/about.html',
        {
            'start_form': None,
        }
    )


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, 'bilbyweb/error_404.html', data)
