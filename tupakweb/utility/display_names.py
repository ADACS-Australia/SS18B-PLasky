# VARIABLES of this file must be unique
DISPLAY_NAME_MAP = dict()

# Job Status
DRAFT = 'draft'
DRAFT_DISPLAY = 'Draft'
SUBMITTED = 'submitted'
SUBMITTED_DISPLAY = 'Submitted'
QUEUED = 'queued'
QUEUED_DISPLAY = 'Queued'
IN_PROGRESS = 'in_progress'
IN_PROGRESS_DISPLAY = 'In Progress'
COMPLETED = 'completed'
COMPLETED_DISPLAY = 'Completed'
ERROR = 'error'
ERROR_DISPLAY = 'Error'
SAVED = 'saved'
SAVED_DISPLAY = 'Saved'
WALL_TIME_EXCEEDED = 'wall_time_exceeded'
WALL_TIME_EXCEEDED_DISPLAY = 'Wall Time Exceeded'
DELETED = 'deleted'
DELETED_DISPLAY = 'Deleted'

# Data Choice
DATA_CHOICE = 'data_choice'
DATA_CHOICE_DISPLAY = 'Type of Data'
SIMULATED_DATA = 'simulated'
SIMULATED_DATA_DISPLAY = 'Simulated'
OPEN_DATA = 'open'
OPEN_DATA_DISPLAY = 'Open'

DISPLAY_NAME_MAP.update({
    DATA_CHOICE: DATA_CHOICE_DISPLAY,
    SIMULATED_DATA: SIMULATED_DATA_DISPLAY,
    OPEN_DATA: OPEN_DATA_DISPLAY,
})

# Signal Choice
SIGNAL_CHOICE = 'signal_choice'
SIGNAL_CHOICE_DISPLAY = 'Type of Signal'
SKIP = 'skip'
SKIP_DISPLAY = 'None'
BINARY_BLACK_HOLE = 'binary_black_hole'
BINARY_BLACK_HOLE_DISPLAY = 'Binary Black Hole'


# Signal Parameter Choice
MASS1 = 'mass_1'
MASS1_DISPLAY = 'Mass 1 (M☉)'
MASS2 = 'mass_2'
MASS2_DISPLAY = 'Mass 2 (M☉)'
LUMINOSITY_DISTANCE = 'luminosity_distance'
LUMINOSITY_DISTANCE_DISPLAY = 'Luminosity Distance (Mpc)'
IOTA = 'iota'
IOTA_DISPLAY = 'iota'
PSI = 'psi'
PSI_DISPLAY = 'psi'
PHASE = 'phase'
PHASE_DISPLAY = 'Phase'
MERGER_TIME = 'merger_time'
MERGER_TIME_DISPLAY = 'Merger Time (GPS Time)'
RA = 'ra'
RA_DISPLAY = 'Right Ascension'
DEC = 'dec'
DEC_DISPLAY = 'Declination'

# Prior Choice
FIXED = 'fixed'
FIXED_DISPLAY = 'Fixed'
UNIFORM = 'uniform'
UNIFORM_DISPLAY = 'Uniform'

# Sampler Choice
DYNESTY = 'dynesty'
DYNESTY_DISPLAY = 'Dynesty'
NESTLE = 'nestle'
NESTLE_DISPLAY = 'Nestle'
EMCEE = 'emcee'
EMCEE_DISPLAY = 'Emcee'
