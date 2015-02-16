from worth2.goals.forms import GoalCheckInFormSet


class GoalCheckInViewMixin(object):
    """Mixin for GoalCheckInPageBlock form functionality.

    This mixin should be attached to your custom PageView.
    """

    def create_goal_check_in_formset(self, request, goalcheckinblock):
        self.checkin_formset = GoalCheckInFormSet(
            prefix='pageblock-%s' % goalcheckinblock.pk)

    def handle_goal_check_in_submission(self, request, goalcheckinblock):
        pass
