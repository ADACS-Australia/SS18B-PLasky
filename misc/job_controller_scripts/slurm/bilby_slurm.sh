#!/bin/bash
#SBATCH -o slurm-%%j.out
#SBATCH -e slurm-%%j.err
#SBATCH --nodes=%(nodes)d
#SBATCH --ntasks-per-node=%(tasks_per_node)d
#SBATCH --mem-per-cpu=%(mem)dM
#SBATCH --time=%(wt_hours)02d:%(wt_minutes)02d:%(wt_seconds)02d
#SBATCH --job-name=%(job_name)s

# Source the bilby environment
. /fred/oz006/bilby/bin/environment

# Make sure the output directory exists
mkdir -p %(job_output_directory)s

# Start bilby with the specified parameter file and output location
python /fred/oz006/bilby/bin/json_interface.py %(job_parameter_file)s %(job_output_directory)s

# Finally tar up all output in to one file
tar cf bilby_job_%(ui_job_id)d.tar.gz *