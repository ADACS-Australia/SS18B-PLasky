from django.shortcuts import render


def index(request):
    return render(
        request,
        "tupakweb/welcome.html",
    )


def about(request):

    from ..forms.job import StartJobForm

    start_form = StartJobForm()

    if request.method == 'POST':
        start_form = StartJobForm(request.POST, request=request)

    return render(
        request,
        'tupakweb/about.html',
        {
            'start_form': start_form,
        }
    )
