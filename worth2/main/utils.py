from django.contrib.contenttypes.models import ContentType
from pagetree.models import Section


def get_first_block_in_session(content_type, session_num):
    """Returns the first block of given type in the given session.

    :param content_type: The pageblock ContentType, e.g. 'goal
    setting block'.
    :param session_num: The session to look in.
    :type content_type: str
    :type session_num: int

    :returns: A pageblock.
    """

    slug = 'session-%d' % session_num
    topsection = Section.objects.get(slug=slug)
    for section in topsection.get_children():
        block = get_first_block_of_type(section, content_type)
        if block:
            return block

    return None


def get_first_block_of_type(section, blocktype):
    """Get the first block of type `blocktype` on this page.

    Returns the block if this page contains it. Otherwise, returns
    None.

    Example usage:
      self.get_first_block_of_type(section, 'goal setting block')

    :param section: The section to look in.
    :param blocktype: The block type to search for.
    :type section: pagetree.models.Section
    :type blocktype: str

    :returns: A pageblock.
    """

    contenttype = ContentType.objects.get(name=blocktype)
    return section.pageblock_set.filter(content_type=contenttype).first()
