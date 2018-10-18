import json
import os
import shutil
import uuid

from scheduler.local import Local


class Bilby(Local):
    def __init__(self, settings, ui_id, job_id):
        """
        Initialises the local scheduler class for Bilby

        :param settings: The settings from settings.py
        :param ui_id: The UI id of the job
        :param job_id: The Slurm id of the Job
        """
        # Call the original constructor
        super().__init__(settings, ui_id, job_id)

        # Set the local template
        self.local_template = 'settings/bilby_local.sh'
        # Set our job parameter path
        self.job_parameter_file = os.path.join(self.get_working_directory(), 'json_params.json')
        # Set the job output directory
        self.job_output_directory = os.path.join(self.get_working_directory(), 'output')

    def generate_template_dict(self):
        """
        Called before a job is submitted before writing the local script

        We add in our custom local arguments

        :return: A dict of key/value pairs used in the local script template
        """
        # Get the existing parameters
        params = super().generate_template_dict()

        # Add our custom parameters
        params['job_parameter_file'] = self.job_parameter_file
        params['job_output_directory'] = self.job_output_directory

        # Return the updated params
        return params

    def submit(self, job_parameters):
        """
        Called when a job is submitted

        :param job_parameters: The parameters for this job, this is a string representing a json dump
        :return: The super call return to submit
        """
        # FIX: Don't pass through the real job name. Bilby outputs the job files by whatever this parameter is, that
        # means that names containing special characters will break. Uniqueness is guaranteed by the folder structure
        job_parameters = json.loads(job_parameters)
        job_parameters['name'] = 'bilby'

        # Write the job parameters to a file
        json.dump(job_parameters, open(self.job_parameter_file, 'w'))

        # Run the job
        return super().submit(job_parameters)