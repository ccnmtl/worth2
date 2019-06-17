import re

from django.contrib.contenttypes.models import ContentType
from pagetree.models import PageBlock, Section, Hierarchy, UserPageVisit
from quizblock.models import Response


def default_location():
    hierarchy = Hierarchy.get_hierarchy('main')
    return hierarchy.get_root()


def last_access_hierarchy(user):
    """Returns the most recent location this user accessed.

    :rtype: UserPageVisit
    """
    return UserPageVisit.objects.filter(
        user=user).order_by('-last_visit').first()


def percent_complete_by_pages(user, pages):
    page_count = float(pages.count())

    if page_count > 0:
        visits = UserPageVisit.objects.filter(
            user=user, section__in=pages).count()
        return int(visits / page_count * 100)
    else:
        return 0


def percent_complete_hierarchy(user):
    hierarchy = Hierarchy.get_hierarchy('main')
    pages = hierarchy.get_root().get_descendants()
    return percent_complete_by_pages(user, pages)


def last_location_url(user):
    if percent_complete_hierarchy(user) == 0:
        return default_location()
    else:
        return last_access_hierarchy(user).section.get_absolute_url()


def percent_complete_by_module(user, module_num):
    """
    Return the percentage of the given module that has been completed
    by this participant. Sections are considered "completed" if they
    have been accessed, (i.e., if there is a UserPageVisit)

    :rtype: int
    """
    main = Hierarchy.get_hierarchy('main')
    module_section = main.find_section_from_path(
        'session-{:d}'.format(module_num))
    if not module_section:
        return 0

    pages = module_section.get_descendants()
    return percent_complete_by_pages(user, pages)


def get_first_block_in_module(app_label, model, session_num, blocktest=None):
    """Returns the first block of given type in the given session.

    :param app_label: The app label, e.g. 'goals'
    :param model: The pageblock ContentType, e.g. 'goalsettingblock'.
    :param session_num: The session to look in.
    :param blocktest: Optional test for block filtering.

    :type app_label: str
    :type model: str
    :type session_num: int
    :type blocktest: function

    :rtype: A pageblock.
    """
    slug = 'session-%d' % session_num
    topsection = Section.objects.get(slug=slug)
    for section in topsection.get_children():
        block = get_first_block_of_type(section, app_label, model, blocktest)
        if block:
            return block

    # Finally, try searching the topsection itself
    block = get_first_block_of_type(topsection, app_label, model, blocktest)
    if block:
        return block

    return None


def get_first_block_of_type(section, app_label, model, blocktest=None):
    """Get the first block of type `blocktype` on this page.

    Returns the block if this page contains it. Otherwise, returns None.
    If blocktest is passed in, the first block that passes that
    additional test is returned, instead of the first block of the given
    type.

    Example usage:
      self.get_first_block_of_type(section, 'goal setting block')

    :param section: The section to look in.
    :param app_label: The app to search for.
    :param model: The model name in the given app to search for.
    :param blocktest: An optional function to test on the pageblock.

    :type section: pagetree.models.Section
    :type app_label: str
    :type model: str
    :type blocktest: function

    :rtype: A pageblock.
    """
    contenttype = ContentType.objects.get(app_label=app_label, model=model)
    pageblocks = section.pageblock_set.filter(content_type=contenttype)

    if hasattr(blocktest, '__call__'):
        pageblocks = list(filter(blocktest, pageblocks))
        if len(pageblocks) > 0:
            return pageblocks[0]
        else:
            return None
    else:
        return pageblocks.first()


def get_module_number_from_section(section):
    """Returns the module number that the given section is in.

    When no module is found, this function returns -1.

    :rtype: int
    """
    if section is None or section.depth == 1:
        return -1
    elif section.depth == 2:
        # depth == 2 is the expected depth for modules.
        module_section = section
    else:
        # Find closest parent whose depth == 2
        module_section = section
        while module_section.depth > 2:
            module_section = module_section.get_parent()

    match = re.match(r'session-(\d)', module_section.slug)
    if match:
        return int(match.groups()[0])
    else:
        return -1


def get_module_number(pageblock):
    """Returns the module number that the given pageblock is in.

    When no module is found, this function returns -1.

    :rtype: int
    """
    if pageblock is None:
        return -1

    return get_module_number_from_section(pageblock.section.get_module())


def get_quiz_responses_by_css_in_module(user, css_class, module):
    """Get quiz responses for a pageblock.

    :type user: User
    :type css_class: string
    :type module: int

    :rtype: queryset
    """
    pageblocks = PageBlock.objects.filter(css_extra__contains=css_class)

    # Filter non-QuizBlocks out of the queryset, and store them in
    # the "quizblocks" list.
    quiztype = ContentType.objects.get(app_label='quizblock',
                                       model='quiz')
    blocks = map(lambda x: x.block(), pageblocks)
    mapping = ContentType.objects.get_for_models(*blocks)
    quizblocks = []
    for k, v in mapping.items():
        if v == quiztype:
            quizblocks.append(k)

    # Filter out the quizblocks that aren't in the queried module.
    quizblocks_in_module = []
    for quizblock in quizblocks:
        if get_module_number_from_section(
                quizblock.pageblock().section) == module:
            quizblocks_in_module.append(quizblock)

    if len(quizblocks_in_module) == 0:
        return Response.objects.none()
    else:
        return Response.objects.filter(
            submission__user=user,
            question__quiz__in=quizblocks_in_module
        ).order_by('question__quiz__pageblocks__section__path')
