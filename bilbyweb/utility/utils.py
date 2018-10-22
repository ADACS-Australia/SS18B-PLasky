"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from .constants import (
    START,
    DATA,
    SIGNAL,
    PRIOR,
    SAMPLER,
    LAUNCH,
)


# Units of file size
B = 'B'
KB = 'KB'
MB = 'MB'
GB = 'GB'
TB = 'TB'
PB = 'PB'


def get_readable_size(size, unit=B):
    """
    Converts a size into human readable format: ex: 1024 MB -> 1.0 GB
    :param size: float number
    :param unit: unit of measurement
    :return: human readable format
    """
    units = [B, KB, MB, GB, TB, PB]

    # invalid inputs should return 0.0 B
    # 0 B, 0 KB, 0 ... should also return 0.0 B
    if size <= 0 or unit not in units:
        return '0.0 B'

    # checking whether we need go for another step
    # that is unit is not already in PB and size = 1024
    if unit in units[:-1] and size >= 1024:

        # get new size
        size = size / 1024

        # get next unit
        unit = units[units.index(unit) + 1]

        # call the function again for further checking
        return get_readable_size(size, unit)

    else:

        # return the string format to 2 decimal point
        return ' '.join([str(round(size / 1, 2)), unit])


def get_enabled_tabs(bilby_job, active_tab):
    """
    Calculates and finds which tabs should be enabled in the UI
    :param bilby_job: Bilby job instance for which the tabs will be calculated
    :param active_tab: Currently active tab
    :return: list of enabled tabs
    """

    # for any bilby job at least First Two tabs should be enabled
    # because, Start tab must have been submitted before a Job is created
    # and as a result the user should be able to see Data Tab
    enabled_tabs = [START, DATA]

    # if nothing has been saved yet, that means, no form has been submitted yet,
    # the user should see only the Start Tab.
    if not bilby_job:
        return enabled_tabs[:1]

    # if data has been entered for it
    # enable Data and Signal Tabs
    if bilby_job.data:
        if DATA not in enabled_tabs:
            enabled_tabs.append(DATA)
        if SIGNAL not in enabled_tabs:
            enabled_tabs.append(SIGNAL)

    # if signal has been entered for it
    # enable Signal and Prior Tabs
    if bilby_job.signal:
        if SIGNAL not in enabled_tabs:
            enabled_tabs.append(SIGNAL)
        if PRIOR not in enabled_tabs:
            enabled_tabs.append(PRIOR)

    # if priors has been entered for it
    # enable Prior and Sampler Tabs
    if bilby_job.priors:
        if PRIOR not in enabled_tabs:
            enabled_tabs.append(PRIOR)
        if SAMPLER not in enabled_tabs:
            enabled_tabs.append(SAMPLER)

    # if sampler has been entered for it
    # enable Sampler and Launch Tabs
    if bilby_job.sampler:
        if SAMPLER not in enabled_tabs:
            enabled_tabs.append(SAMPLER)
        if LAUNCH not in enabled_tabs:
            enabled_tabs.append(LAUNCH)

    # always make sure to include the active tab
    if active_tab not in enabled_tabs:
        enabled_tabs.append(active_tab)

    return enabled_tabs
