import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import user_job_input_file_directory_path
from ..utility.job_utils import *
from ..utility.job_iterables import model_instance_to_iterable
from django.utils.timezone import now
import json

def act_on_request_method(request, active_tab, id):
    tab_checker = active_tab
    instance = None
    get_instance = False

    # ACTIVE TAB
    if active_tab != LAUNCH:
        if request.method == 'POST':
            if active_tab == START:
                instance = MODELS[active_tab].objects.get(id=id)
                form = FORMS[active_tab](request.POST,
                                              instance=instance,
                                              request=request,
                                              job_id=id)
            else:
                if active_tab == DATA:
                    try:
                        if request.FILES['datafile1']:
                            form = FORMS[active_tab](request.POST, request.FILES, request=request, id=id)
                        else:
                            form = FORMS[active_tab](request=request, id=id)
                    except:
                        form = FORMS[active_tab](request=request, id=id)
                else:
                    try:
                        # Update
                        instance = MODELS[active_tab].objects.get(job_id=id)
                        form = FORMS[active_tab](request.POST,
                                                      instance=instance,
                                                      request=request,
                                                      job_id=id)
                    except:
                        # Create
                        form = FORMS[active_tab](request.POST, request=request, id=id)
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
                form = FORMS[active_tab](instance=instance, request=request, job_id=id)
            else:
                try:
                    instance = MODELS[active_tab].objects.get(job_id=id)
                    form = FORMS[active_tab](instance=instance, request=request, job_id=id)
                except:
                    form = FORMS[active_tab](request=request, id=id)
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
    data_model = None
    dataset = None
    psf = None
    lsf = None
    galaxy_model = None
    fitter = None
    params = None

    if tab_checker != START:
        try:
            job = Job.objects.get(id=id)
            start_form = FORMS[START](instance=job, request=request, job_id=id)

        except:
            # If the job is not found, let's go where we can create one!
            return redirect('job_start')
    else:
        start_form = form
        job = instance
    set_list(forms, TABS_INDEXES[START], start_form)
    set_list(views, TABS_INDEXES[START], model_instance_to_iterable(job) if job else None)

    if tab_checker != DMODEL:
        try:
            data_model = DataModel.objects.get(job_id=id)
            data_model_form = FORMS[DMODEL](instance=data_model, request=request, job_id=id)
        except:
            data_model_form = FORMS[DMODEL](request=request, job_id=id)
    else:
        data_model_form = form
        data_model = instance
    set_list(forms, TABS_INDEXES[DMODEL], data_model_form)
    set_list(views, TABS_INDEXES[DMODEL], model_instance_to_iterable(data_model,
                                                                     model=DMODEL,
                                                                     views=views) if data_model else None)

    if tab_checker != DATASET or tab_checker == DATASET:
        # Always get in here.
        try:
            dataset = DataSet.objects.get(job_id=id)
            dataset_form = FORMS[DATASET](instance=dataset, request=request, job_id=id)
        except:
            dataset_form = FORMS[DATASET](request=request, job_id=id)
    else:
        dataset_form = form
        dataset = instance
    set_list(forms, TABS_INDEXES[DATASET], dataset_form)
    set_list(views, TABS_INDEXES[DATASET], model_instance_to_iterable(dataset,
                                                                      model=DATASET,
                                                                      views=views) if dataset else None)

    if tab_checker != PSF:
        try:
            psf = PSF_model.objects.get(job_id=id)
            psf_form = FORMS[PSF](instance=psf, request=request, job_id=id)
        except:
            psf_form = FORMS[PSF](request=request, job_id=id)
    else:
        psf_form = form
        psf = instance
    set_list(forms, TABS_INDEXES[PSF], psf_form)
    set_list(views, TABS_INDEXES[PSF], model_instance_to_iterable(psf,
                                                                  model=PSF,
                                                                  views=views) if psf else None)

    if tab_checker != LSF:
        try:
            lsf = LSF_model.objects.get(job_id=id)
            lsf_form = FORMS[LSF](instance=lsf, request=request, job_id=id)
        except:
            lsf_form = FORMS[LSF](request=request, job_id=id)
    else:
        lsf_form = form
        lsf = instance
    set_list(forms, TABS_INDEXES[LSF], lsf_form)
    set_list(views, TABS_INDEXES[LSF], model_instance_to_iterable(lsf,
                                                                  model=LSF,
                                                                  views=views) if lsf else None)

    if tab_checker != GMODEL:
        try:
            galaxy_model = GalaxyModel.objects.get(job_id=id)
            galaxy_model_form = FORMS[GMODEL](instance=galaxy_model, request=request, job_id=id)
        except:
            galaxy_model_form = FORMS[GMODEL](request=request, job_id=id)
    else:
        galaxy_model_form = form
        galaxy_model = instance
    set_list(forms, TABS_INDEXES[GMODEL], galaxy_model_form)
    set_list(views, TABS_INDEXES[GMODEL], model_instance_to_iterable(galaxy_model,
                                                                     model=GMODEL,
                                                                     views=views) if galaxy_model else None)

    if tab_checker != FITTER:
        try:
            fitter = Fitter_model.objects.get(job_id=id)
            fitter_form = FORMS[FITTER](instance=fitter, request=request, job_id=id)
        except:
            fitter_form = FORMS[FITTER](request=request, job_id=id)
    else:
        fitter_form = form
        fitter = instance
    set_list(forms, TABS_INDEXES[FITTER], fitter_form)
    set_list(views, TABS_INDEXES[FITTER], model_instance_to_iterable(fitter,
                                                                     model=FITTER,
                                                                     views=views) if fitter else None)

    if tab_checker != PARAMS:
        try:
            params = Params.objects.get(job_id=id)
            params_form = FORMS[PARAMS](instance=params, request=request, job_id=id)
        except:
            params_form = FORMS[PARAMS](request=request, job_id=id)
    else:
        params_form = form
        params = instance
    set_list(forms, TABS_INDEXES[PARAMS], params_form)
    set_list(views, TABS_INDEXES[PARAMS], model_instance_to_iterable(params,
                                                                     model=PARAMS,
                                                                     views=views) if params else None)

    request.session['task'] = build_task_json(request)

    return active_tab, forms, views

@login_required
def job_start(request):
    active_tab = START
    active_tab, forms, views = act_on_request_method(request, active_tab, id)

    return render(
        request,
        "tupakweb/job/new-job.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'data_form': forms[TABS_INDEXES[DATA]],
            'data_simulated_form': forms[TABS_INDEXES[DATA_SIMULATED]],
            'data_open_form': forms[TABS_INDEXES[DATA_OPEN]],
            'signal_form': forms[TABS_INDEXES[SIGNAL]],
            'prior': forms[TABS_INDEXES[PRIOR]],
            'prior_uniform': forms[TABS_INDEXES[PRIOR_UNIFORM]],
            'prior_fixed': forms[TABS_INDEXES[PRIOR_FIXED]],
            'sampler': forms[TABS_INDEXES[SAMPLER]],
            'sampler_dynesty': forms[TABS_INDEXES[SAMPLER_DYNESTY]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )