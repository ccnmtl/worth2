from django.contrib.contenttypes.models import ContentType
from pagetree.models import Section


def get_first_block_in_session(content_type, session_num, blocktest=None):
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
