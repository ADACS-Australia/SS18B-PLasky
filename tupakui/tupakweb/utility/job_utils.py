from .constants import TABS, TABS_INDEXES
from ..models import Job

def set_list(l, i, v):
    """Set a value v at index i in list l.

    Parameters
    ----------
    l:
        list
    i:
        index
    v:
        value

    Returns
    -------
    appended list
    """
    try:
        l[i] = v
    except IndexError:
        for _ in range(i - len(l) + 1):
            l.append(None)
        l[i] = v

def previous_tab(active_tab):
    return TABS[TABS_INDEXES[active_tab] - 1]

def next_tab(active_tab):
    return TABS[TABS_INDEXES[active_tab] + 1]

def check_permission_save(form, request, active_tab, id):
    job = Job.objects.get(id=id)
    if job.user_id == request.user.id:
        active_tab = save_form(form, request, active_tab, id)

    return active_tab

def save_form(form, request, active_tab, id=None):
    if 'skip' in request.POST:
        active_tab = next_tab(active_tab)
    elif form.is_valid():
        form.save()
        if 'next' in request.POST:
            active_tab = next_tab(active_tab)
        if 'previous' in request.POST:
            active_tab = previous_tab(active_tab)
    return active_tab