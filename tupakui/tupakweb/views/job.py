from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..utility.job_utils import *

@login_required
def job_start(request):
    active_tab = START
    if request.method == 'POST':
        form = FORMS[active_tab](request.POST, request=request)
        #active_tab = save_form(form, request, active_tab)
    else:
        form = FORMS[active_tab](request=request)

    if active_tab == START:
        return render(
            request,
            "tupakweb/job/job-start.html",
            {
                'active_tab': active_tab,
                'disable_other_tabs': True,
                'start_form': form,
            }
        )
    else:
        return redirect('job_data_model_edit', id=request.session['draft_job']['id'])