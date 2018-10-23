# The path to the pid file of the daemon
HPC_DAEMON_PID_FILE = '/tmp/bilby_job_controller.pid'

# The remote web address of the websocket server (ws(s)://host:port)
HPC_WEBSOCKET_SERVER = 'wss://supercomputing.swin.edu.au/projects/bilby/live/ws/'

# The scheduler class
HPC_SCHEDULER_CLASS = 'settings.bilby_slurm.Bilby'

# The location of job working directory
HPC_JOB_WORKING_DIRECTORY = '/fred/oz006/bilby/jobs/'