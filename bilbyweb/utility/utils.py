from .constants import (
    START,
    DATA,
    SIGNAL,
    PRIOR,
    SAMPLER,
    LAUNCH,
)


def get_enabled_tabs(bilby_job, active_tab):
    enabled_tabs = [START, DATA]
    if not bilby_job:
        return enabled_tabs[:1]

    if bilby_job.data:
        if DATA not in enabled_tabs:
            enabled_tabs.append(DATA)
        if SIGNAL not in enabled_tabs:
            enabled_tabs.append(SIGNAL)

    if bilby_job.signal:
        if SIGNAL not in enabled_tabs:
            enabled_tabs.append(SIGNAL)
        if PRIOR not in enabled_tabs:
            enabled_tabs.append(PRIOR)

    if bilby_job.priors:
        if PRIOR not in enabled_tabs:
            enabled_tabs.append(PRIOR)
        if SAMPLER not in enabled_tabs:
            enabled_tabs.append(SAMPLER)

    if bilby_job.sampler:
        if SAMPLER not in enabled_tabs:
            enabled_tabs.append(SAMPLER)
        if LAUNCH not in enabled_tabs:
            enabled_tabs.append(LAUNCH)

    if active_tab not in enabled_tabs:
        enabled_tabs.append(active_tab)

    return enabled_tabs
