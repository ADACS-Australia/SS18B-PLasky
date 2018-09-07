from django.shortcuts import render


def index(request):
    return render(
        request,
        "tupakweb/welcome.html",
    )


def about(request):
    return render(
        request,
        'tupakweb/about.html',
        {
            'start_form': None,
        }
    )


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, 'tupakweb/error_404.html', data)
