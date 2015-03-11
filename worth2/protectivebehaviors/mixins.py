from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

import quizblock


class ProtectiveBehaviorsMixin(object):
    """A mixin for Protective Behaviors form functionality."""

    def protectivebehaviors_remove_empty_submission(self, user):
        """Remove an empty submission for validation purposes.

        Returns True if any empty submissions were removed, and this
        is a Protective Behaviors page. Otherwise, returns False.
        """

        # Only pay attention to pageblocks that are part of the
        # Protective Behaviors activity. The quizzes here will always
        # have a 'protective-behaviors' css class. The special likert
        # quiz at the end has a 'rate-my-risk' class.
        pageblocks = self.section.pageblock_set.filter(
            Q(css_extra__icontains='protective-behaviors') |
            Q(css_extra__icontains='rate-my-risk')
        )
        quiztypes = ContentType.objects.filter(
            Q(name='quiz') | Q(name='rate my risk quiz'))
        quizblocks_on_this_page = [
            page.block() for page in
            pageblocks.filter(content_type__in=quiztypes)]

        # Was the form submitted with no values selected?
        is_submission_empty = False
        for submission in quizblock.models.Submission.objects.filter(
                user=user, quiz__in=quizblocks_on_this_page):
            if quizblock.models.Response.objects.filter(
                    submission=submission).count() == 0:
                # Delete empty submission, and tell the template that it was
                # empty, so it can display an error message.
                submission.delete()
                is_submission_empty = True

        return is_submission_empty
