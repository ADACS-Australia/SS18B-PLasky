Project Overview
================

This project serves as a user-interface and job controller for the BILBY. The UI is responsible for controlling
and managing user input, download job information and job data, etc.

Prerequisites
=============
* Python 3.6+
* MySQL 5.7+ (tested with 5.7)

Optional

* Docker and Docker-Compose (If you want to use skip manual setup steps and just want to run the UI as a
docker container)

# Setup #

You might need to install `python-dev`, `python3-dev` and `libmysqlclient-dev` using the following
commands:

```shell
sudo apt-get install python-dev python3-dev
sudo apt-get install libmysqlclient-dev
```

beforehand for successful completion of the command:

```shell
pip install -r requirements.txt
```

## Configuration Steps ##

The required steps include the following:

* `virtualenv venv` (create the virtual environment, e.g. with https://docs.python.org/3/library/venv.html or https://github.com/pyenv/pyenv)
* `git pull` (clone the code)
* `git submodule update --init --recursive` (pulls any submodules (django_hpc_job_controller))
* `source venv/bin/activate` (activate the virtual environment)
* `cd ADACS-SS18B-PLasky/bilbyui/settings` (enter the settings directory)
* `touch local.py` (create the file for local settings - refer to the Local Settings section for setting up a local settings file)
* `cd ../../` (enter the root directory of the project)
* `pip3 install -r requirements.txt` (install required python packages)
* `pip3 install -r django_hpc_job_controller/server/requirements.txt` (install required python packages for the django_hpc_job_controller server)
* `./development-manage.py migrate` (migrate, for staging or production
* `./development-manage.py createsuperuser` (create an admin account) specify the required manage.py file instead)
* `./development-manage.py runserver 8000` (running the server)

## Local Settings ##

The project is required to have customised machine specific settings. Those settings need to be included or overridden 
in the local settings file. Create one local.py in the settings module next to the other settings files (`base.py`, 
`development.py`, `production.py` etc.)

The following settings needs to be present in the `local.py` settings file.

* The secret key used to authenticate the workflow with the UI API (can be generated with e.g. https://www.miniwebtool.com/django-secret-key-generator/)
```python
SECRET_KEY = 'some really long string with $YMb0l$'
```

* The admins of the site who will receive error emails.
```python
ADMINS = [
    ('Your Name', 'youremail@dd.ress'),
]

MANAGERS = ADMINS
```
* The address from where the server emails will be sent.
```python
SERVER_EMAIL = 'serveremail@dd.ress'
```

* The address from where the notification emails will be sent.

```python
EMAIL_FROM = 'mail@dd.ress'
```

* Other email settings can also be provided.
```python
EMAIL_HOST = 'gpo.dd.res'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

* Database settings. For example, a simple MySQL database can be configured using
```python
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'bilby',
    'USER': 'django',
    'PASSWORD': 'test-password#1',
    'HOST': 'db',
    'PORT': 3306,
    }
}
```

## Local Job Submission Setup

Local job submission setup is relatively simple:

* Create a Python 3.6 virtual environment in the local `django_hpc_job_controller/client/venv` and install the client requirements as described in https://github.com/ASVO-TAO/django_hpc_job_controller#installation-steps
* Configure a new cluster in the Django admin that uses `localhost` for the host name as described in https://github.com/ASVO-TAO/django_hpc_job_controller#configure-a-cluster and also has the client path set to the absolute path to the job controller client folder, eg: `/home/user/projects/ADACS-SS18B-PLasky/django_hpc_job_controller/client`
* Create a python virtual environment for Bilby and install Bilby in to it. eg: `/home/user/bilby/venv`
* Copy the three files from `misc/job_controller_scripts/local/` to `django_hpc_job_controller/client/settings/`
* Copy the Bilby json wrapper (`misc/bilby_json_wrapper`) somewhere, eg: to `/home/user/bilby/`
* Configure the local submission script paths in `django_hpc_job_controller/client/settings/bilby_local.sh` to match the paths on your system.
* Configure the local job working directory (where job output folders will be created) in `django_hpc_job_controller/client/settings/local.py`, eg: `HPC_JOB_WORKING_DIRECTORY = '/home/user/bilby/jobs/'`

## Slurm Job Submission Setup

## Nginx Configuration

