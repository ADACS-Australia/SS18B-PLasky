FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN pip install -r django_hpc_job_controller/server/requirements.txt
RUN mkdir -p /code/bilbyui/logs/
