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

* `virtualenv -p python3.6 venv` (create the virtual environment, e.g. with https://docs.python.org/3/library/venv.html or https://github.com/pyenv/pyenv)
* `git pull` (clone the code)
* `cd SS18B-PLasky` (enter to the directory)
* `git submodule foreach --recursive git pull origin master` (pulls any submodules (django_hpc_job_controller))
* `source ../venv/bin/activate` (activate the virtual environment)
* `cd bilbyui/settings` (enter the settings directory)
* `touch local.py` (create the file for local settings - refer to the Local Settings section for setting up a local settings file)
* `cd ../../` (enter the root directory of the project)
* `pip3 install -r requirements.txt` (install required python packages)
* `pip3 install -r django_hpc_job_controller/server/requirements.txt` (install required python packages for the django_hpc_job_controller server)
* `./development-manage.py migrate` (migrate, for staging or production)
* `./development-manage.py createsuperuser` (create an admin account) (specify the required manage.py file instead)
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

### Database Settings for Docker ###

To run using docker and MySQL, modify the `local.py` configuration file. 
Instead of using the database settings described above, use something in 
the lines of the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bilby',
        'HOST': 'db',
        'USER': 'django',
        'PORT': 3306,
        'PASSWORD': 'test-docker_#1',
    },
}
```

The USER and PASSWORD should be in accordance with the information provided in the file `docker-compose.yml` 
included at the root of the project repository.

## Local Job Submission Setup

Local job submission setup is relatively simple:

* Create a Python 3.6 virtual environment in the local `django_hpc_job_controller/client/venv` and install the client requirements as described in https://github.com/ADACS-Australia/django_hpc_job_controller#installation-steps
* Configure a new cluster in the Django admin that uses `localhost` for the host name as described in https://github.com/ADACS-Australia/django_hpc_job_controller#configure-a-cluster and also has the client path set to the absolute path to the job controller client folder, eg: `/home/user/projects/ADACS-SS18B-PLasky/django_hpc_job_controller/client`
* Create a python virtual environment for Bilby and install Bilby in to it. eg: `/home/user/bilby/venv`
* Copy the three files from `misc/job_controller_scripts/local/` to `django_hpc_job_controller/client/settings/`
* Copy the Bilby json wrapper (`misc/bilby_json_wrapper`) somewhere, eg: to `/home/user/bilby/`
* Configure the local submission script paths in `django_hpc_job_controller/client/settings/bilby_local.sh` to match the paths on your system.
* Configure the local job working directory (where job output folders will be created) in `django_hpc_job_controller/client/settings/local.py`, eg: `HPC_JOB_WORKING_DIRECTORY = '/home/user/bilby/jobs/'`

## Slurm Job Submission Setup

Slurm job submission is similar to the local job submission steps.

* Follow the client setup instructions in https://github.com/ADACS-Australia/django_hpc_job_controller#installation-steps on the remote cluster
* Configure a new cluster in the Django admin for the remote cluster as described in https://github.com/ADACS-Australia/django_hpc_job_controller#configure-a-cluster 
* Create a python virtual environment on the remote cluster for Bilby and install Bilby in to it. eg: `/home/user/bilby/venv`
* Copy the three files from `misc/job_controller_scripts/slurm/` to `.../django_hpc_job_controller/client/settings/` on the remote cluster
* Copy the Bilby json wrapper (`misc/bilby_json_wrapper`) somewhere on the remote cluster, eg: to `/home/user/bilby/`
* Configure the slurm submission script paths in `.../django_hpc_job_controller/client/settings/bilby_slurm.sh`, on the remote cluster, to match the correct paths on the remote cluster.
* Configure the slurm job working directory on the remote cluster (where job output folders will be created) in `.../django_hpc_job_controller/client/settings/local.py`, eg: `HPC_JOB_WORKING_DIRECTORY = '/home/user/bilby/jobs/'`

## Nginx Configuration

The Django server currently exports two ports, one for handling HTTP, and the other for handling Websocket connections. Typically, we would recommend running the web app with gunicorn in a production environment (as configured in the provided docker configurations). By default the Websocket server will listen on port 8001. For the Swinburne/OzSTAR deployment, we use an nginx reverse proxy to map the incoming Websocket connections on /ws/ to the websocket server, and all other requests are sent to the normal Django port.

The nginx config for our docker release at Swinburne looks like this:

```nginx
server {
  location /projects/bilby/live/static/ {
    autoindex on;
    alias /static/;
  }

  location /projects/bilby/live/ws/ {
    proxy_pass http://web:8001/;
 
    proxy_http_version  1.1;
    proxy_set_header    Upgrade $http_upgrade;
    proxy_set_header    Connection "upgrade";
    
    proxy_connect_timeout 7d;
    proxy_send_timeout 7d;
    proxy_read_timeout 7d;
  }

  location / {
    proxy_pass http://web:8000;
  }
 
  listen 8000;
  server_name localhost;
}
```

The connection upgrade configuration is very important for successful websocket connection.

## License ##

The project is licensed under the MIT License. For more information, please refer to the `LICENSE` included in
the root of the project.


## Authors ##
* [Shibli Saleheen](https://github.com/shiblisaleheen) (as part of [ADACS](https://adacs.org.au/))
* [Lewis Lakerink](https://github.com/retsimx) (as part of [ADACS](https://adacs.org.au/))
* [Dany Vohl](https://github.com/macrocosme) (as part of [ADACS](https://adacs.org.au/))
