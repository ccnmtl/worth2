from collections import OrderedDict
from django import forms
from django.contrib import messages
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import pluralize

from worth2.goals.forms import GoalCheckInForm, GoalSettingForm
from worth2.goals.models import (
    GoalCheckInResponse, GoalOption, GoalSettingResponse
)


class GoalCheckInViewMixin(object):
    """Mixin for GoalCheckInPageBlock form functionality.

    This mixin should be attached to your custom PageView.
    """

    def create_goal_check_in_formset(self, request, goalcheckinblock):
        """Attach the formset's class and instance to this view."""

        goalsettingblock = goalcheckinblock.block().goal_setting_block

        self.goal_setting_responses = GoalSettingResponse.objects.filter(
            user=request.user,
            goal_setting_block=goalsettingblock,
        ).filter(~Q(option__text__iexact='n/a'))

        self.GoalCheckInFormSet = formset_factory(
            GoalCheckInForm,
            min_num=self.goal_setting_responses.count())

        self.checkin_formset = self.GoalCheckInFormSet(
            prefix='pageblock-%s' % goalcheckinblock.pk)

        # Populate the hidden goal_setting_response fields
        for i, resp in enumerate(self.goal_setting_responses):
            self.checkin_formset.forms[i].initial[
                'goal_setting_response_id'] = resp.pk

        self.goal_checkin_context = zip(
            self.goal_setting_responses, self.checkin_formset)

    def _goal_check_in_submit(self, request, goalcheckinblock):
        formset = self.GoalCheckInFormSet(
            request.POST,
            prefix='pageblock-%s' % goalcheckinblock.pk)

        if formset.is_valid():
            for formdata in formset.cleaned_data:
                if formdata == {}:
                    continue

                resp_id = formdata.pop('goal_setting_response_id')
                resp = get_object_or_404(GoalSettingResponse, pk=resp_id)
                updated_values = formdata.copy()
                try:
                    GoalCheckInResponse.objects.create_or_update(
                        goal_setting_response=resp,
                        defaults=updated_values)
                except:
                    GoalCheckInResponse.objects.filter(
                        goal_setting_response=resp,
                    ).delete()

                    updated_values.update({'goal_setting_response': resp})
                    GoalCheckInResponse.objects.create(**updated_values)

        return formset

    def goal_check_in_post(self, request, goalcheckinblock):
        """This is meant to be called from a django view's post() method."""
        formset = self._goal_check_in_submit(request, goalcheckinblock)
        ctx = self.get_context_data()
        ctx.update({
            'checkin_formset': formset,
            'goal_checkin_context': zip(
                self.goal_setting_responses, formset),
        })

        if formset.is_valid():
            if formset.has_changed():
                checkins_saved = len([f for f in formset.cleaned_data
                                      if f != {}])
                messages.success(
                    request, str(checkins_saved) + ' goal check-in' +
                    pluralize(checkins_saved) + ' saved.')

        return render(request, self.template_name, ctx)


class GoalSettingViewMixin(object):
    """Mixin for GoalSettingBlock form functionality.

    This mixin should be attached to your custom PageView.
    """

    def create_goal_setting_formset(self, request, goalsettingblock):
        """Create the goal setting formset.

        To be used by both GET and POST.
        """

        class DynamicGoalSettingForm(GoalSettingForm):

            option = forms.ModelChoiceField(
                label='Main services goal',
                queryset=GoalOption.objects.filter(
                    goal_type=goalsettingblock.block().goal_type),
                widget=forms.Select(
                    attrs={'class': 'form-control goal-option'}),
            )

        # Put the form's fields in the right order.
        DynamicGoalSettingForm.base_fields = OrderedDict(
            (k, DynamicGoalSettingForm.base_fields[k])
            for k in ['option', 'other_text', 'text']
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
            DynamicGoalSettingForm,
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

        self.setting_formset = self.GoalSettingFormSet(
            prefix='pageblock-%s' % goalsettingblock.pk,
            initial=tuple(initial_data),
        )

    def _goal_setting_submit(self, request, goalsettingblock):
        """Handle a submission for the goal setting activity.

        This method returns the populated formset.
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

                updated_values = formdata.copy()
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

                    updated_values.update({
                        'form_id': i,
                        'user': request.user,
                        'goal_setting_block': block,
                    })
                    GoalSettingResponse.objects.create(**updated_values)

        return formset

    def goal_setting_post(self, request, goalsettingblock):
        """This is meant to be called from a django view's post() method."""
        formset = self._goal_setting_submit(request, goalsettingblock)
        ctx = self.get_context_data()
        ctx.update({'setting_formset': formset})

        if formset.is_valid():
            if formset.has_changed():
                goals_saved = len([f for f in formset.cleaned_data
                                   if f != {}])
                messages.success(
                    request, str(goals_saved) + ' goal' +
                    pluralize(goals_saved) + ' saved.')

        return render(request, self.template_name, ctx)
