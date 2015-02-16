from django import forms
from django.forms.formsets import formset_factory

from worth2.goals.forms import GoalCheckInForm
from worth2.goals.models import (
    GoalOption, GoalSettingBlock, GoalSettingResponse
)


class GoalCheckInViewMixin(object):
    """Mixin for GoalCheckInPageBlock form functionality.

    This mixin should be attached to your custom PageView.
    """

    def create_goal_check_in_formset(self, request, goalcheckinblock):
        """Attach the formset's class and instance to this view."""

        # Find the goal setting block by the goal checkin block's session
        # number.
        goalsettingblock = GoalSettingBlock.objects.get(
            session_num=goalcheckinblock.block().session_num)

        goal_setting_responses = GoalSettingResponse.objects.filter(
            user=request.user,
            goal_setting_block=goalsettingblock)

        # goal_check_in_responses = GoalCheckInResponse.objects.filter(
        #    goal_setting_response__in=goal_setting_responses)

        # Adapt to the strange behavior of formset_factory's "extra"
        # param. The formset displays a different number of forms
        # based on how many elements of initial data we give it, so
        # we need to adjust "extra" based on "responses".
        extra = goalsettingblock.goal_amount - 1
        extra -= goal_setting_responses.count() - 1

        extra = 2
        self.GoalCheckInFormSet = formset_factory(
            GoalCheckInForm,
            min_num=1,
            extra=extra)

        self.checkin_formset = self.GoalCheckInFormSet(
            prefix='pageblock-%s' % goalcheckinblock.pk)

        self.goal_checkin_context = zip(
            goal_setting_responses, self.checkin_formset)

    def handle_goal_check_in_submission(self, request, goalcheckinblock):
        formset = self.GoalCheckInFormSet(
            request.POST,
            prefix='pageblock-%s' % goalcheckinblock.pk)

        if formset.is_valid():
            pass

        return formset


class GoalSettingViewMixin(object):
    """Mixin for GoalSettingBlock form functionality.

    This mixin should be attached to your custom PageView.
    """

    def create_goal_setting_formset(self, request, goalsettingblock):
        """Create the goal setting formset.

        To be used by GET and POST.
        """

        # I'd like to define the GoalSettingForm instead in
        # goals/forms.py, but the goal field depends on data I can
        # only get here.
        class GoalSettingForm(forms.Form):
            option = forms.ModelChoiceField(
                label='Main services goal',
                queryset=GoalOption.objects.filter(
                    goal_setting_block=goalsettingblock.block()),
                widget=forms.Select(attrs={'class': 'form-control'}),
            )
            text = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 3}),
                label='How will you make this happen?',
            )

        # If there's existing responses to this pageblock, use them
        # to bind the formset.
        responses = GoalSettingResponse.objects.filter(
            user=request.user,
            goal_setting_block=goalsettingblock.block())

        # Adapt to the strange behavior of formset_factory's "extra"
        # param. The formset displays a different number of forms
        # based on how many elements of initial data we give it, so
        # we need to adjust "extra" based on "responses".
        extra = goalsettingblock.block().goal_amount - 1
        extra -= responses.count() - 1

        self.GoalSettingFormSet = formset_factory(
            GoalSettingForm,
            extra=extra,
            # min_num is 1 because there's always a 'Main' goal form.
            min_num=1,
            validate_min=True,
        )

        initial_data = []
        for r in responses.order_by('form_id'):
            initial_data.append({
                'option': r.option,
                'text': r.text,
            })

        self.formset = self.GoalSettingFormSet(
            prefix='pageblock-%s' % goalsettingblock.pk,
            initial=tuple(initial_data),
        )

    def handle_goal_setting_submission(self, request, goalsettingblock):
        """Handle a submission for the goal setting activity.

        This method returns the formset populated formset.
        """

        block = goalsettingblock.block()
        formset = self.GoalSettingFormSet(
            request.POST,
            prefix='pageblock-%s' % goalsettingblock.pk)

        if formset.is_valid():
            for i, formdata in enumerate(formset.cleaned_data):
                # Formsets with multiple forms put an empty dictionary in
                # the cleaned data for unpopulated forms. We don't want
                # to attempt to make a GoalSettingResponse for these
                # optional, empty forms.
                if formdata == {}:
                    continue

                option = formdata.get('option')
                text = formdata.get('text')

                updated_values = dict(option=option, text=text)
                try:
                    GoalSettingResponse.objects.update_or_create(
                        form_id=i,
                        user=request.user,
                        goal_setting_block=block,
                        defaults=updated_values)
                except:
                    # In case there's a unique_together exception, or something
                    # similar, (which is unlikely, but possible if you have
                    # stale data), we can handle it by refreshing the data.
                    GoalSettingResponse.objects.filter(
                        form_id=i,
                        user=request.user,
                        goal_setting_block=block,
                    ).delete()

                    updated_values['form_id'] = i
                    updated_values['user'] = request.user
                    updated_values['goal_setting_block'] = block
                    GoalSettingResponse.objects.create(**updated_values)

        return formset
