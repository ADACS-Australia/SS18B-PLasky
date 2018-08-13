import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ...models import user_job_input_file_directory_path
from ...utility.constants import *
from ...utility.job_utils import *
from ...utility.job_iterables import model_instance_to_iterable
from django.utils.timezone import now
import json


def build_task_json(request):
    return None


def process_active_tab(request, active_tab, id):
    instance = None
    get_instance = False
    form = None

    if active_tab != LAUNCH:
        if request.method == 'POST':
            if active_tab == START:
                instance = MODELS[active_tab].objects.get(id=id)
                form = FORMS_EDIT[active_tab](request.POST,
                                              instance=instance,
                                              request=request,
                                              job_id=id)
            else:
                try:
                    # Update
                    instance = MODELS[active_tab].objects.get(job_id=id)
                    form = FORMS_EDIT[active_tab](request.POST,
                                                  instance=instance,
                                                  request=request,
                                                  job_id=id)

                # We should catch something better... This is what was in GBKFIT
                except:
                    # Create
                    form = FORMS_NEW[active_tab](request.POST, request=request, id=id)
                    get_instance = True

            active_tab = check_permission_save(form, request, active_tab, id)
            if get_instance:
                if 'next' in request.POST:
                    instance = MODELS[previous_tab(active_tab)].objects.get(job_id=id)
                if 'previous' in request.POST:
                    instance = MODELS[next_tab(active_tab)].objects.get(job_id=id)

        else:
            if active_tab == START:
                instance = MODELS[active_tab].objects.get(id=id)
                form = FORMS_EDIT[active_tab](instance=instance, request=request, job_id=id)
            else:
                try:
                    instance = MODELS[active_tab].objects.get(job_id=id)
                    form = FORMS_EDIT[active_tab](instance=instance, request=request, job_id=id)
                except:
                    form = FORMS_NEW[active_tab](request=request, id=id)
    else:
        if 'previous' in request.POST:
            active_tab = previous_tab(active_tab)
        else:
            if request.method == 'POST':
                # Job is being submitted, write the json descriptor for this job
                # Create the task json descriptor here
                pass

    return instance, form, active_tab


def act_on_request_method(request, active_tab):
    tab_checker = active_tab

    # ACTIVE TAB
    instance, form, active_tab = process_active_tab(request, active_tab)

    # OTHER TABS
    forms = {}
    views = {}

    if tab_checker != START:
        try:
            job = Job.objects.get(id=id)
            start_form = FORMS_EDIT[START](instance=job, request=request, job_id=id)

        except:
            # If the job is not found, let's go where we can create one!
            return redirect('job_start')
    else:
        start_form = form
        job = instance

    forms[START] = start_form
    views[START] = model_instance_to_iterable(job) if job else None

    for model in MODELS:
        if model not in [START, SIGNAL_BBH_PARAMETERS]:  # Not yet handling BBH_PARAMETERS...
            if tab_checker != model:
                try:
                    variables[model] = MODELS[model].objects.get(job_id=id)
                    form_variables[model] = FORMS_EDIT[model](instance=variables[model], request=request, job_id=id)
                except:
                    form_variables[model] = FORMS_EDIT[model](request=request, job_id=id)
            else:
                form_variables[model] = form
                variables[model] = instance

            forms[model] = form_variables[model]
            views[model] = model_instance_to_iterable(variables[model],
                                                      model=model,
                                                      views=views) if variables[model] else None

    request.session['task'] = build_task_json(request)

    return active_tab, forms, views


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
        START: StartJobForm(),
        DATA: DataForm(),
        DATA_OPEN: DataOpenForm(),
        DATA_SIMULATED: DataSimulatedForm(),
        SIGNAL: SignalForm(),
        PRIOR: PriorForm(),
        PRIOR_FIXED: PriorFixedForm(),
        PRIOR_UNIFORM: PriorUniformForm(),
        SAMPLER: SamplerForm(),
        SAMPLER_DYNESTY: SamplerDynestyForm(),
    }

    if job:
        forms.update({
            START: StartJobForm(instance=job),
        })

        # try:
        #     data_object = Data.objects.get(job=job)
        #
        #     forms.update({
        #         DATA: DataForm(instance=data_object, job=job),
        #     })
        # except Data.DoesNotExist:
        #     pass

        for model in MODELS:
            print(model)

            if model in [START, SIGNAL_BBH_PARAMETERS, PRIOR, PRIOR_FIXED, PRIOR_UNIFORM, SAMPLER_DYNESTY,
                         SAMPLER_NESTLE, SAMPLER_EMCEE]:
                continue

            try:
                instance = MODELS[model].objects.get(job=job)

                forms.update({
                    model: FORMS_NEW[model](instance=instance, job=job)
                })
            except MODELS[model].DoesNotExist:
                pass

    return forms


def save_tab(request, active_tab):
    try:
        job = Job.objects.get(id=request.session['draft_job'].get('id', None))
    except (KeyError, AttributeError, Job.DoesNotExist):
        job = None

    forms = generate_forms(job, request=request)

    forms[active_tab] = FORMS_NEW[active_tab](request.POST, request=request, job=job)

    if forms[active_tab].is_valid():
        forms[active_tab].save()
        active_tab, error = get_to_be_active_tab(active_tab, )

    return active_tab, forms


@login_required
def new_job(request):
    if request.method == 'POST':
        active_tab = request.POST.get('form-tab', START)
        active_tab, forms = save_tab(request, active_tab)
    else:
        active_tab = START
        forms = generate_forms()

        request.session['draft_job'] = None

    # print(active_tab)

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
            'prior_form': forms[PRIOR],
            'prior_uniform_form': forms[PRIOR_UNIFORM],
            'prior_fixed_form': forms[PRIOR_FIXED],
            'sampler_form': forms[SAMPLER],
            'sampler_dynesty_form': forms[SAMPLER_DYNESTY],

        }
    )

# @login_required
# def new_job(request):
#     active_tab = START
#     if request.method == 'POST':
#         form = FORMS_NEW[active_tab](request.POST, request=request)
#         active_tab = save_form(form, request, active_tab)
#     else:
#         form = FORMS_NEW[active_tab](request=request)
#
#     if active_tab == START:
#         return render(
#             request,
#             "tupakweb/job/new-job.html",
#             {
#                 'active_tab': active_tab,
#                 'disable_other_tabs': True,
#                 'start_form': form,
#                 'new_job': True,
#             }
#         )
#     else:
#         return redirect('job_data_edit', id=request.session['draft_job']['id'])


# def job_data(request, id):
#     active_tab = DATA
#     active_tab, forms, views = act_on_request_method(request, active_tab, id)
#
#     return render(
#         request,
#         "tupakweb/job/edit-job.html",
#         {
#             'job_id': id,
#             'active_tab': active_tab,
#             'disable_other_tabs': False,
#             'new_job': False,
#
#             'start_form': forms[START],
#             'data_form': forms[DATA],
#             'data_simulated_form': forms[DATA_SIMULATED],
#             'data_open_form': forms[DATA_OPEN],
#             'signal_form': forms[SIGNAL],
#             'prior_form': forms[PRIOR],
#             'prior_uniform_form': forms[PRIOR_UNIFORM],
#             'prior_fixed_form': forms[PRIOR_FIXED],
#             'sampler_form': forms[SAMPLER],
#             'sampler_dynesty_form': forms[SAMPLER_DYNESTY],
#
#             'start_view': views[START],
#             'data_view': views[DATA],
#             'data_simulated_view': views[DATA_SIMULATED],
#             'data_open_view': views[DATA_OPEN],
#             'signal_view': views[SIGNAL],
#             'prior_view': views[PRIOR],
#             'prior_uniform_view': views[PRIOR_UNIFORM],
#             'prior_fixed_view': views[PRIOR_FIXED],
#             'sampler_view': views[SAMPLER],
#             'sampler_dynesty_view': views[SAMPLER_DYNESTY],
#         }
#     )
#
#
# def job_signal(request, id):
#     active_tab = SIGNAL
#     active_tab, forms, views = act_on_request_method(request, active_tab, id)
#
#     return render(
#         request,
#         "tupakweb/job/edit-job.html",
#         {
#             'job_id': id,
#             'active_tab': active_tab,
#             'disable_other_tabs': False,
#             'new_job': False,
#
#             'start_form': forms[START],
#             'data_form': forms[DATA],
#             'data_simulated_form': forms[DATA_SIMULATED],
#             'data_open_form': forms[DATA_OPEN],
#             'signal_form': forms[SIGNAL],
#             'prior_form': forms[PRIOR],
#             'prior_uniform_form': forms[PRIOR_UNIFORM],
#             'prior_fixed_form': forms[PRIOR_FIXED],
#             'sampler_form': forms[SAMPLER],
#             'sampler_dynesty_form': forms[SAMPLER_DYNESTY],
#
#             'start_view': views[START],
#             'data_view': views[DATA],
#             'data_simulated_view': views[DATA_SIMULATED],
#             'data_open_view': views[DATA_OPEN],
#             'signal_view': views[SIGNAL],
#             'prior_view': views[PRIOR],
#             'prior_uniform_view': views[PRIOR_UNIFORM],
#             'prior_fixed_view': views[PRIOR_FIXED],
#             'sampler_view': views[SAMPLER],
#             'sampler_dynesty_view': views[SAMPLER_DYNESTY],
#         }
#     )
#
#
# def job_prior(request, id):
#     pass
#
#
# def job_sampler(request, id):
#     pass
#
#
# def job_launch(request, id):
#     pass
