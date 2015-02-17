from pagetree.models import UserPageVisit


def unlock_hierarchy(section, user):
    """Visit all sections in a Pagetree node to unlock everything.

    Get around 'gated = True' by creating a UserPageVisit for each
    section.
    """

    if section is None:
        return

    UserPageVisit.objects.create(
        user=user,
        section=section,
        status='complete')

    unlock_hierarchy(section.get_first_child(), user)
