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
    pass

def act_on_request_method(request, active_tab, id):
    tab_checker = active_tab
    instance = None
    get_instance = False

    # ACTIVE TAB
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
                job = Job.objects.get(id=id)

                # Check write permission
                if job.user_id == request.user.id:
                    # Create the task json descriptor
                    task_json = {}
                    task_json['mode'] = 'fit'
                    task_json['dmodel'] = job.job_data_model.as_json()
                    task_json['datasets'] = job.job_data_set.as_array()
                    # PSF and LSF are optional.
                    try:
                        task_json['psf'] = job.job_psf.as_json()
                    except:
                        pass
                    try:
                        task_json['lsf'] = job.job_lsf.as_json()
                    except:
                        pass
                    task_json['gmodel'] = job.job_gmodel.as_json()
                    task_json['fitter'] = job.job_fitter.as_json()
                    task_json['params'] = job.job_parameter_set.as_array()

                    # Make sure the directory exists to write the json output
                    os.makedirs(os.path.dirname(user_job_input_file_directory_path(job)), exist_ok=True)

                    # Write the input json file
                    with open(user_job_input_file_directory_path(job), 'w') as outfile:
                        json.dump(task_json, outfile)

                    # Now actually update the job as submitted
                    job.user = request.user
                    job.status = Job.SUBMITTED
                    job.submission_time = now()
                    job.save()
                    return Job.SUBMITTED, [], []

    # OTHER TABS
    forms = []
    views = []

    job = None
    data = None
    data_simulated = None
    data_open = None
    signal = None
    prior = None
    prior_fixed = None
    prior_uniform = None
    sampler = None
    sampler_dynesty = None
    sampler_emcee = None

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
    set_list(forms, TABS_INDEXES[START], start_form)
    set_list(views, TABS_INDEXES[START], model_instance_to_iterable(job) if job else None)

    if tab_checker != DATA:
        try:
            data = Data.objects.get(job_id=id)
            data_form = FORMS_EDIT[DATA](instance=data, request=request, job_id=id)
        except:
            data_form = FORMS_EDIT[DATA](request=request, job_id=id)
    else:
        data_form = form
        data = instance
    set_list(forms, TABS_INDEXES[DATA], data_form)
    set_list(views, TABS_INDEXES[DATA], model_instance_to_iterable(data,
                                                                   model=DATA,
                                                                   views=views) if data else None)

    if tab_checker != SIGNAL:
        try:
            signal = Signal.objects.get(job_id=id)
            signal_form = FORMS_EDIT[SIGNAL](instance=signal, request=request, job_id=id)
        except:
            signal_form = FORMS_EDIT[SIGNAL](request=request, job_id=id)
    else:
        signal_form = form
        signal = instance
    set_list(forms, TABS_INDEXES[SIGNAL], signal_form)
    set_list(views, TABS_INDEXES[SIGNAL], model_instance_to_iterable(signal,
                                                                     model=SIGNAL,
                                                                     views=views) if signal else None)

    if tab_checker != PRIOR:
        try:
            prior = Prior.objects.get(job_id=id)
            prior_form = FORMS_EDIT[PRIOR](instance=prior, request=request, job_id=id)
        except:
            prior_form = FORMS_EDIT[PRIOR](request=request, job_id=id)
    else:
        prior_form = form
        prior = instance
    set_list(forms, TABS_INDEXES[PRIOR], prior_form)
    set_list(views, TABS_INDEXES[PRIOR], model_instance_to_iterable(prior,
                                                                    model=PRIOR,
                                                                    views=views) if prior else None)

    if tab_checker != SAMPLER:
        try:
            sampler = Sampler.objects.get(job_id=id)
            sampler_form = FORMS_EDIT[SAMPLER](instance=sampler, request=request, job_id=id)
        except:
            sampler_form = FORMS_EDIT[SAMPLER](request=request, job_id=id)
    else:
        sampler_form = form
        sampler = instance
    set_list(forms, TABS_INDEXES[SAMPLER], sampler_form)
    set_list(views, TABS_INDEXES[SAMPLER], model_instance_to_iterable(sampler,
                                                                      model=SAMPLER,
                                                                      views=views) if sampler else None)

    request.session['task'] = build_task_json(request)

    return active_tab, forms, views

@login_required
def new_job(request):
    active_tab = START
    if request.method == 'POST':
        form = FORMS_NEW[active_tab](request.POST, request=request)
        active_tab = save_form(form, request, active_tab)
    else:
        form = FORMS_NEW[active_tab](request=request)

    if active_tab == START:
        return render(
            request,
            "tupakweb/job/new-job.html",
            {
                'active_tab': active_tab,
                'disable_other_tabs': True,
                'start_form': form,
                'new_job': True,
            }
        )
    else:
        return redirect('job_data_model_edit', id=request.session['draft_job']['id'])

@login_required
def edit_job(request, id):
    active_tab = START
    active_tab, forms, views = act_on_request_method(request, active_tab, id)

    return render(
        request,
        "tupakweb/job/edit-job.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,
            'new_job': False,

            'start_form': forms[TABS_INDEXES[START]],
            'data_form': forms[TABS_INDEXES[DATA]],
            # 'data_simulated_form': forms[TABS_INDEXES[DATA_SIMULATED]],
            # 'data_open_form': forms[TABS_INDEXES[DATA_OPEN]],
            'signal_form': forms[TABS_INDEXES[SIGNAL]],
            'prior': forms[TABS_INDEXES[PRIOR]],
            # 'prior_uniform': forms[TABS_INDEXES[PRIOR_UNIFORM]],
            # 'prior_fixed': forms[TABS_INDEXES[PRIOR_FIXED]],
            'sampler': forms[TABS_INDEXES[SAMPLER]],
            # 'sampler_dynesty': forms[TABS_INDEXES[SAMPLER_DYNESTY]],

            'start_view': views[TABS_INDEXES[START]],
            'data_view': views[TABS_INDEXES[DATA]],
            # 'data_simulated_view': views[TABS_INDEXES[DATA_SIMULATED]],
            # 'data_open_view': views[TABS_INDEXES[DATA_OPEN]],
            'signal_view': views[TABS_INDEXES[SIGNAL]],
            'prior': views[TABS_INDEXES[PRIOR]],
            # 'prior_uniview': views[TABS_INDEXES[PRIOR_UNIFORM]],
            # 'prior_fixed': views[TABS_INDEXES[PRIOR_FIXED]],
            'sampler': views[TABS_INDEXES[SAMPLER]],
            # 'sampler_dynesty': views[TABS_INDEXES[SAMPLER_DYNESTY]],
        }
    )

def job_data(request, id):
    pass

def job_signal(request, id):
    pass

def job_prior(request, id):
    pass

def job_sampler(request, id):
    pass

def job_launch(request, id):
    pass


