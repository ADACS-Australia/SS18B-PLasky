"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...utility.display_names import SKIP
from ...utility.utils import get_enabled_tabs
from ...models import (
    Job,
)

from ...utility.job import BilbyJob
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
    """
    Finds out the next active tab based on user input
    :param active_tab: Current active tab
    :param previous: Whether or not previous is pressed
    :return: To be Active tab, Whether it is the last tab or not
    """

    # keep track of out of index tab, beneficial to detect the last tab
    no_more_tabs = False

    # find the current active tab index
    active_tab_index = TABS_INDEXES.get(active_tab)

    # next active tab index based on the button pressed
    if previous:
        active_tab_index -= 1
    else:
        active_tab_index += 1

    # checks out the last tab or not
    try:
        active_tab = TABS[active_tab_index]
    except IndexError:
        no_more_tabs = True

    return active_tab, no_more_tabs


def generate_forms(job=None, forms=None):
    """
    Generates all the forms for the job and the user inputs.
    :param job: the job information to be rendered in the forms
    :param forms: forms already generated during save tab
    :return: A dictionary of forms
    """

    # initialise all blank if no forms are generated, usually this will happen for a get request
    # the new job page, or job copied or loaded for editing.
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

    # if there is a job, update the model forms
    if job:
        for model in MODELS:
            try:
                # START Form is the Job instance, for other forms it is referenced
                instance = job if model in [START, ] else MODELS[model].objects.get(job=job)

                # do not override already generated forms.
                # otherwise, this would wipe out all errors from the form.
                if not forms.get(model, None):
                    # generate a form if there is none generated for this
                    forms.update({
                        model: FORMS_NEW[model](instance=instance, job=job, prefix=model)
                    })
            except MODELS[model].DoesNotExist:
                pass

    # Do a check for all forms as well,
    # i.e., for Dynamic forms here, others will be skipped.
    for name in FORMS_NEW.keys():

        # generate a form if there is none generated for this
        # Model forms would be automatically ignored here as they have been taken
        # care of in the previous section
        if not forms.get(name, None):
            forms.update({
                name: FORMS_NEW[name](job=job, prefix=name)
            })

    # if there is a job, update the forms based on job information
    # to pre-fill their input fields like the model forms
    # extra processing is needed because Dynamic Form does not
    # have easy update option by passing the instance.
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
    """
    Filters out irrelevant forms from the to save list based on user input
    :param forms_to_save: list of forms to save for a tab
    :param request: Django request object
    :return: new list of forms to save
    """

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
    """
    Saves the forms in a tab.
    :param request: Django request object
    :param active_tab: Currently active tab
    :return: active tab, forms for all the tabs, whether or not the form is submitted
    """

    submitted = False

    # check whether job exists
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
        # should not submit job if previous is pressed on the submit page
        previous = request.POST.get('previous', False)

        # save the forms
        for form_to_save in forms_to_save:
            if not (previous and form_to_save == LAUNCH):
                forms[form_to_save].save()

        # update the job
        if job:
            job.refresh_from_db()
            # saving the job here again will call signal to update the last updated
            # it is left to the signal because of potential change of Job model to
            # extend the HpcJob model.
            job.save()

        # get the active tab
        active_tab, submitted = get_to_be_active_tab(active_tab, previous=previous)

    # don't process further for submitted jobs
    if not submitted:

        # now generate the other forms.
        forms = generate_forms(job, forms=forms)

    return active_tab, forms, submitted


@login_required
def new_job(request):
    """
    Process request and returns all the forms for a draft job
    :param request: Django request object
    :return: Rendered template or redirects to relevant view
    """

    # Processing if the request is post, that means things to be saved here
    if request.method == 'POST':

        # Get the active tab
        active_tab = request.POST.get('form-tab', START)

        # find out new active tab, forms to render, and whether submitted or not
        active_tab, forms, submitted = save_tab(request, active_tab)

        # if submitted, nothing more to do with drafts
        # redirect to the page where the job can be viewed with other jobs
        if submitted:
            return redirect('jobs')

    # Processing if the request is get,
    # Can happen for new draft, copy or edit
    else:

        # set the active tab as start
        active_tab = START

        # Coming with copy or edit request: load the correct job id as draft
        try:
            request.session['draft_job'] = request.session['to_load']
        except (AttributeError, KeyError):
            request.session['draft_job'] = None

        # clear the to_load session variable, so that next time it does not load
        # this job automatically
        request.session['to_load'] = None

        # Now, check whether a job exists or not
        try:
            job = Job.objects.get(id=request.session['draft_job'].get('id', None))
        except (KeyError, AttributeError, Job.DoesNotExist):
            job = None

        # generate forms
        forms = generate_forms(job=job)

    # Create a bilby job for this job
    try:
        bilby_job = BilbyJob(job_id=request.session['draft_job'].get('id', None))
    except (KeyError, AttributeError):
        bilby_job = None

    # Get enabled Tabs based on the bilby job and active job
    enabled_tabs = get_enabled_tabs(bilby_job, active_tab)

    return render(
        request,
        "bilbyweb/job/edit-job.html",
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
            'drafted_job': bilby_job,
        }
    )
