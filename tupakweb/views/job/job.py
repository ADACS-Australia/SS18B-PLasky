from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from ...utility.display_names import SKIP
from ...utility.utils import get_enabled_tabs
from ...models import (
    Job,
)

from ...utility.job import TupakJob
from ...utility.constants import (
    START,
    DATA,
    DATA_OPEN,
    DATA_SIMULATED,
    SIGNAL,
    SIGNAL_PARAMETER_BBH,
    PRIOR,
    SAMPLER,
    SAMPLER_DYNESTY,
    SAMPLER_NESTLE,
    SAMPLER_EMCEE,
    LAUNCH,
    MODELS,
    FORMS_NEW,
    TAB_FORMS,
    TABS,
    TABS_INDEXES,
)


def get_to_be_active_tab(active_tab, previous=False):
    no_more_tabs = False  # keep track of out of index tab, might be beneficial to detect the last page

    active_tab_index = TABS_INDEXES.get(active_tab)

    if previous:
        active_tab_index -= 1
    else:
        active_tab_index += 1

    try:
        active_tab = TABS[active_tab_index]
    except IndexError:
        no_more_tabs = True

    return active_tab, no_more_tabs


def generate_forms(job=None, request=None, forms=None):
    if not forms:
        forms = {
            START: None,
            DATA: None,
            DATA_OPEN: None,
            DATA_SIMULATED: None,
            SIGNAL: None,
            SIGNAL_PARAMETER_BBH: None,
            PRIOR: None,
            SAMPLER: None,
            SAMPLER_DYNESTY: None,
            SAMPLER_NESTLE: None,
            SAMPLER_EMCEE: None,
            LAUNCH: None,
        }

    if job:
        for model in MODELS:
            try:
                # START Form is the Job instance, for other forms it is referenced
                instance = job if model in [START, ] else MODELS[model].objects.get(job=job)

                if not forms.get(model, None):
                    forms.update({
                        model: FORMS_NEW[model](instance=instance, job=job, prefix=model)
                    })
            except MODELS[model].DoesNotExist:
                pass

    for name in FORMS_NEW.keys():
        if not forms.get(name, None):
            forms.update({
                name: FORMS_NEW[name](job=job, prefix=name)
            })

    if job:
        # non-model forms update
        forms[DATA_OPEN].update_from_database(job=job)
        forms[DATA_SIMULATED].update_from_database(job=job)
        forms[SIGNAL_PARAMETER_BBH].update_from_database(job=job)
        forms[SIGNAL].update_from_database(job=job)
        forms[PRIOR].update_from_database(job=job)
        forms[SAMPLER_DYNESTY].update_from_database(job=job)
        forms[SAMPLER_NESTLE].update_from_database(job=job)
        forms[SAMPLER_EMCEE].update_from_database(job=job)
        forms[LAUNCH].update_from_database(job=job)

        # because of too much dynamic nature, fields are by default set as non-required
        # once everything is processed with the form, all the fields are marked as required
        # this can be done in an alternate way:
        # Using dynamic form for each prior
        # then use the same approach for job to decide which forms are going to be saved
        # the rest of the forms should be returned as initial
        forms[PRIOR].update_fields_to_required()

    return forms


def filter_as_per_input(forms_to_save, request):

    # returning the corrected forms need to be saved for DATA tab
    if DATA in forms_to_save:
        data_choice = request.POST.get('data-data_choice', None)

        if data_choice in DATA_SIMULATED:
            forms_to_save = [DATA, DATA_SIMULATED, ]
        else:
            forms_to_save = [DATA, DATA_OPEN, ]

    # returning the corrected forms need to be saved for SIGNAL tab
    if SIGNAL in forms_to_save:
        signal_choice = request.POST.get('signal-signal_choice', None)

        if signal_choice == SKIP:
            forms_to_save = [SIGNAL, ]
        elif signal_choice in SIGNAL_PARAMETER_BBH:
            forms_to_save = [SIGNAL, SIGNAL_PARAMETER_BBH, ]

    # returning the corrected forms need to be saved for SAMPLER tab
    if SAMPLER in forms_to_save:
        sampler_choice = request.POST.get('sampler-sampler_choice', None)

        if sampler_choice in SAMPLER_DYNESTY:
            forms_to_save = [SAMPLER, SAMPLER_DYNESTY, ]
        elif sampler_choice in SAMPLER_NESTLE:
            forms_to_save = [SAMPLER, SAMPLER_NESTLE, ]
        elif sampler_choice in SAMPLER_EMCEE:
            forms_to_save = [SAMPLER, SAMPLER_EMCEE, ]

    return forms_to_save


def save_tab(request, active_tab):
    submitted = False
    try:
        job = Job.objects.get(id=request.session['draft_job'].get('id', None))
    except (KeyError, AttributeError, Job.DoesNotExist):
        job = None

    # generating the forms for the UI
    forms = dict()

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
        active_tab, submitted = get_to_be_active_tab(active_tab, previous=request.POST.get('previous', False))

    # don't process further for submitted jobs
    if not submitted:
        forms = generate_forms(job, request=request, forms=forms)

    return active_tab, forms, submitted


@login_required
def new_job(request):
    if request.method == 'POST':
        active_tab = request.POST.get('form-tab', START)
        active_tab, forms, submitted = save_tab(request, active_tab)
        if submitted:
            return redirect('jobs')
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

    try:
        tupak_job = TupakJob(job_id=request.session['draft_job'].get('id', None))
    except (KeyError, AttributeError):
        tupak_job = None

    enabled_tabs = get_enabled_tabs(tupak_job, active_tab)

    return render(
        request,
        "tupakweb/job/edit-job.html",
        {
            'active_tab': active_tab,
            'enabled_tabs': enabled_tabs,
            'disable_other_tabs': False,
            'new_job': False,

            'start_form': forms[START],
            'data_form': forms[DATA],
            'data_simulated_form': forms[DATA_SIMULATED],
            'data_open_form': forms[DATA_OPEN],
            'signal_form': forms[SIGNAL],
            'signal_parameter_bbh_form': forms[SIGNAL_PARAMETER_BBH],
            'prior_form': forms[PRIOR],
            'sampler_form': forms[SAMPLER],
            'sampler_dynesty_form': forms[SAMPLER_DYNESTY],
            'sampler_nestle_form': forms[SAMPLER_NESTLE],
            'sampler_emcee_form': forms[SAMPLER_EMCEE],
            'submit_form': forms[LAUNCH],

            # job so far...
            'drafted_job': tupak_job,
        }
    )

