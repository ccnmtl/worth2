import re
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_str
from pagetree.models import Section


def get_first_block_in_module(content_type, session_num, blocktest=None):
    """Returns the first block of given type in the given session.

    :param content_type: The pageblock ContentType, e.g. 'goal
    setting block'.
    :param session_num: The session to look in.
    :param blocktest: Optional test for block filtering.

    :type content_type: str
    :type session_num: int
    :type blocktest: function

    :rtype: A pageblock.
    """
    slug = 'session-%d' % session_num
    topsection = Section.objects.get(slug=slug)
    for section in topsection.get_children():
        block = get_first_block_of_type(section, content_type, blocktest)
        if block:
            return block

    # Finally, try searching the topsection itself
    block = get_first_block_of_type(topsection, content_type, blocktest)
    if block:
        return block

    return None


def get_first_block_of_type(section, blocktype, blocktest=None):
    """Get the first block of type `blocktype` on this page.

    Returns the block if this page contains it. Otherwise, returns None.
    If blocktest is passed in, the first block that passes that
    additional test is returned, instead of the first block of the given
    type.

    Example usage:
      self.get_first_block_of_type(section, 'goal setting block')

    :param section: The section to look in.
    :param blocktype: The block type to search for.
    :param blocktest: An optional function to test on the pageblock.

    :type section: pagetree.models.Section
    :type blocktype: str
    :type blocktest: function

    :rtype: A pageblock.
    """
    contenttype = ContentType.objects.get(name=blocktype)
    pageblocks = section.pageblock_set.filter(content_type=contenttype)

    if hasattr(blocktest, '__call__'):
        pageblocks = filter(blocktest, pageblocks)
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
    if section.depth == 1:
        # This is the 'Root' section, so there's no module associated
        # with it.
        return -1
    elif section.depth == 2:
        # depth == 2 is the expected depth for modules.
        module_section = section
    else:
        # Find closest parent whose depth == 2
        module_section = section
        while module_section.depth > 2:
            module_section = module_section.get_parent()

    n = -1
    match = re.match(r'session-(\d)', module_section.slug)
    if match:
        n = int(match.groups()[0])

    return n


def get_module_number(pageblock):
    """Returns the module number that the given pageblock is in.

    When no module is found, this function returns -1.

    :rtype: int
    """
    if pageblock is None:
        return -1

    return get_module_number_from_section(pageblock.section)


def get_verbose_section_name(section):
    """Returns a string."""

    s = smart_str(section)
    module_num = get_module_number_from_section(section)

    # Only append the module number if it's valid.
    if module_num > -1:
        return smart_str('%s [Session %d]' % (s, module_num))
    else:
        return s
