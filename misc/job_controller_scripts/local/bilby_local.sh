#!/bin/bash

# Source the bilby environment
. /home/lewis/bilby/bin/venv/bin/activate

# Make sure the output directory exists
mkdir -p %(job_output_directory)s

# Start bilby with the specified parameter file and output location
python /home/lewis/bilby/bin/json_interface.py %(job_parameter_file)s %(job_output_directory)s

# Finally tar up all output in to one file
tar cf bilby_job_%(ui_job_id)d.tar.gz *