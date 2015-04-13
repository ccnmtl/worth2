from django import forms
from django.contrib.auth.models import User
from django.db import models
from ordered_model.models import OrderedModel

from pagetree.generic.models import BasePageBlock


GOAL_TYPES = (
    ('services', 'Services'),
    ('risk reduction', 'Risk Reduction'),
    ('social support', 'Social Support'),
)


class GoalSettingBlock(BasePageBlock):
    """A PageBlock for allowing participants to set goals.

    Participants set goals in each session. These goals are persistent -
    they are revisited by the participant at the end of each session to
    reflect on whether they've reached their goals.

    You can customize this block by adding questions and options to it
    in the admin interface.
    """

    display_name = 'Goal Setting Block'
    template_file = 'goals/goal_setting_block.html'

    goal_type = models.CharField(
        max_length=255,
        choices=GOAL_TYPES,
        default='services',
    )

    # goal_amount controls how many goals the participants are expected
    # to fill out on this block. It needs to be at least 1, and the first
    # goal is always a required 'main' goal, while any remaining questions
    # will be optional 'extra' goals.
    goal_amount = models.PositiveSmallIntegerField(
        default=1,
        help_text='The number of goals on this block, including the main one.')

    def has_na_option(self):
        """Returns True if this block has a n/a option."""

        return self.goal_type == 'services' or \
            self.goal_type == 'social support'

    def needs_submit(self):
        return True

    def unlocked(self, user):
        # Find out if this user has created any GoalSettingResponses for
        # this GoalSettingBlock.
        c = self.goal_setting_responses.filter(user=user).count()
        return c > 0

    def __unicode__(self):
        try:
            slug = unicode(self.pageblock().section.get_parent().slug)
        except AttributeError:
            slug = 'no section'

        return unicode(self.get_goal_type_display() + ' goals ' +
                       '[' + slug + '] id: ' +
                       unicode(self.pk))

    @staticmethod
    def add_form():
        return GoalSettingBlockForm()

    def edit_form(self):
        return GoalSettingBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = GoalSettingBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create()

    def edit(self, vals, files):
        form = GoalSettingBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class GoalSettingBlockForm(forms.ModelForm):
    class Meta:
        model = GoalSettingBlock


class GoalOption(OrderedModel):
    """GoalSettingBlock dropdowns are populated by GoalOptions.

    The contents of each GoalSettingBlock's dropdown depends on its
    goal_type.
    """

    goal_type = models.CharField(
        max_length=255,
        choices=GOAL_TYPES,
        default='services',
        db_index=True,
    )
    text = models.TextField(
        help_text='An option for the dropdowns in a specific ' +
        'GoalSetting pageblock.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.text)


class GoalSettingResponse(models.Model):
    """Participant responses to 'main' and 'extra' goals."""

    goal_setting_block = models.ForeignKey(
        GoalSettingBlock, related_name='goal_setting_responses')
    user = models.ForeignKey(User)

    option = models.ForeignKey(GoalOption)
    other_text = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    # Correspond this response with a specific form on the block. This
    # can't be higher than self.goal_setting_block.goal_amount - 1.
    form_id = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('goal_setting_block', 'user', 'form_id'),)

    def __unicode__(self):
        return unicode('"%s" from %s' % (unicode(self.option),
                                         unicode(self.user)))


class GoalCheckInOption(OrderedModel):
    """Editable options for the goal check-in form."""

    text = models.TextField(
        help_text='An option for the ' +
        '"What got in the way" dropdown for goal check-in.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.text)


class GoalCheckInResponse(models.Model):
    """Participant responses for the Check In page.

    These are for reflecting on the goals they've set for themselves.
    This is only used on sessions 2 through 5.
    """

    goal_setting_response = models.ForeignKey(
        GoalSettingResponse,
        unique=True,
        related_name='goal_checkin_response'
    )

    # This field is actually "How did it go?"
    i_will_do_this = models.CharField(
        max_length=255,
        choices=(
            ('yes', 'I did it!'),
            ('in progress', 'I\'m still working on it.'),
            ('no', 'I haven\'t started this goal.'),
        ))

    what_got_in_the_way = models.ForeignKey(GoalCheckInOption, null=True)
    other = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode('"%s" from %s' % (
            unicode(self.get_i_will_do_this_display()),
            unicode(self.goal_setting_response.user)))


class GoalCheckInPageBlock(BasePageBlock):
    display_name = 'Goal Check In Block'
    template_file = 'goals/goal_check_in_block.html'

    goal_setting_block = models.ForeignKey(GoalSettingBlock, null=True)

    def needs_submit(self):
        return True

    def unlocked(self, user):
        # Find out if this user has created any GoalCheckinResponses for
        # this GoalCheckinBlock.
        setting_responses = \
            self.goal_setting_block.goal_setting_responses.filter(
                user=user)

        if setting_responses.count() == 0:
            return True

        for setting_response in setting_responses:
            if setting_response.goal_checkin_response.count() > 0:
                return True

        return False

    @staticmethod
    def add_form():
        return GoalCheckInPageBlockForm()

    def edit_form(self):
        return GoalCheckInPageBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = GoalCheckInPageBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = GoalCheckInPageBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class GoalCheckInPageBlockForm(forms.ModelForm):
    class Meta:
        model = GoalCheckInPageBlock
