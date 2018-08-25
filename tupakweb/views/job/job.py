import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from ...utility.job import TupakJob
from ...utility.constants import *
from ...utility.job_utils import *


def get_to_be_active_tab(active_tab, previous=False):
    error = False  # keep tract of out of index tab, might be beneficial to detect the last page

    active_tab_index = TABS_INDEXES.get(active_tab)

    if previous:
        active_tab_index -= 1
    else:
        active_tab_index += 1

    try:
        active_tab = TABS[active_tab_index]
    except IndexError:
        error = True

    return active_tab, error


def generate_forms(job=None, request=None):
    forms = {
        START: StartJobForm(prefix=START),
        DATA: DataForm(prefix=DATA),
        DATA_OPEN: DataOpenForm(prefix=DATA_OPEN),
        DATA_SIMULATED: DataSimulatedForm(prefix=DATA_SIMULATED),
        SIGNAL: SignalForm(prefix=SIGNAL),
        SIGNAL_PARAMETER_BBH: SignalParameterBbhForm(prefix=SIGNAL_PARAMETER_BBH),
        PRIOR: PriorForm(prefix=PRIOR),
        PRIOR_FIXED: PriorFixedForm(prefix=PRIOR_FIXED),
        PRIOR_UNIFORM: PriorUniformForm(prefix=PRIOR_UNIFORM),
        SAMPLER: SamplerForm(prefix=SAMPLER),
        SAMPLER_DYNESTY: SamplerDynestyForm(prefix=SAMPLER_DYNESTY),
    }

    if job:
        for model in MODELS:

            if model in [PRIOR, PRIOR_FIXED, PRIOR_UNIFORM, SAMPLER_DYNESTY,
                         SAMPLER_NESTLE, SAMPLER_EMCEE]:
                continue

            try:
                # START Form is the Job instance, for other forms it is referenced
                instance = job if model == START else MODELS[model].objects.get(job=job)

                forms.update({
                    model: FORMS_NEW[model](instance=instance, job=job, prefix=model)
                })
            except MODELS[model].DoesNotExist:
                pass

        # non-model forms update
        forms[SIGNAL_PARAMETER_BBH].update_from_database(job=job)
    return forms


def filter_as_per_input(forms_to_save, request):

    # returning the corrected forms needs to be saved for DATA tab
    if DATA in forms_to_save:
        data_choice = request.POST.get('data-data_choice', None)

        if data_choice in DATA_SIMULATED:
            forms_to_save = [DATA, DATA_SIMULATED, ]
        else:
            forms_to_save = [DATA, DATA_OPEN, ]

    return forms_to_save


def save_tab(request, active_tab):
    try:
        job = Job.objects.get(id=request.session['draft_job'].get('id', None))
    except (KeyError, AttributeError, Job.DoesNotExist):
        job = None

    # generating the forms for the UI
    forms = generate_forms(job, request=request)

    # do we need to skip the form save? or remove whatever the form has in the database?
    # lets determine it here by checking the skip button.
    skip_or_remove = request.POST.get('skip', None)

    # here, the forms are saved in the database as required.
    # not all of them are saved, only the forms that are in the tab are considered.
    # additionally, it is based on the user input
    # filtering the required forms to be save based on user input
    forms_to_save = filter_as_per_input(TAB_FORMS.get(active_tab), request)

    error_in_form = False

    for form_to_save in forms_to_save:

        forms[form_to_save] = FORMS_NEW[form_to_save](request.POST, request=request, job=job, prefix=form_to_save)

        if not forms[form_to_save].is_valid():
            error_in_form = True

    if not error_in_form:
        # save the forms
        for form_to_save in forms_to_save:
            forms[form_to_save].save()

        # update the job
        if job:
            job.refresh_from_db()
            job.last_updated = timezone.now()
            job.save()

        # get the active tab
        active_tab, error = get_to_be_active_tab(
            active_tab,
            previous=request.POST.get('previous', False),
        )

    return active_tab, forms


@login_required
def new_job(request):
    if request.method == 'POST':
        active_tab = request.POST.get('form-tab', START)
        active_tab, forms = save_tab(request, active_tab)
    else:
        active_tab = START

        try:
            request.session['draft_job'] = request.session['to_load']
        except (AttributeError, KeyError):
            request.session['draft_job'] = None

        request.session['to_load'] = None

        try:
            job = Job.objects.get(id=request.session['draft_job'].get('id', None))
        except (KeyError, AttributeError, Job.DoesNotExist):
            job = None

        forms = generate_forms(job=job)

    # print(active_tab)
    try:
        tupak_job = TupakJob(job_id=request.session['draft_job'].get('id', None))
    except (KeyError, AttributeError):
        tupak_job = None

    return render(
        request,
        "tupakweb/job/edit-job.html",
        {
            'active_tab': active_tab,
            'disable_other_tabs': False,
            'new_job': False,

            'start_form': forms[START],
            'data_form': forms[DATA],
            'data_simulated_form': forms[DATA_SIMULATED],
            'data_open_form': forms[DATA_OPEN],
            'signal_form': forms[SIGNAL],
            'signal_parameter_bbh_form': forms[SIGNAL_PARAMETER_BBH],
            'prior_form': forms[PRIOR],
            'prior_uniform_form': forms[PRIOR_UNIFORM],
            'prior_fixed_form': forms[PRIOR_FIXED],
            'sampler_form': forms[SAMPLER],
            'sampler_dynesty_form': forms[SAMPLER_DYNESTY],

            # job so far...
            'drafted_job': tupak_job,

        }
    )

