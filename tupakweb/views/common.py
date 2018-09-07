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
