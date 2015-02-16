from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django import forms
from ordered_model.models import OrderedModel
from pagetree.models import PageBlock

from worth2.main.generic.models import BasePageBlock


class GoalSettingBlock(models.Model):
    """A PageBlock for allowing participants to set goals.

    Participants set goals in each session. These goals are persistent -
    they are revisited by the participant at the end of each session to
    reflect on whether they've reached their goals.

    You can customize this block by adding questions and options to it
    in the admin interface.
    """

    pageblocks = GenericRelation(PageBlock)
    display_name = 'Goal Setting Block'
    template_file = 'goals/goal_setting_block.html'

    session_num = models.PositiveSmallIntegerField(
        default=1,
        help_text='The session this is associated with (i.e. 1 through 5).',
        db_index=True,
    )

    goal_type = models.CharField(
        max_length=255,
        choices=(
            ('services', 'Services'),
            ('risk reduction', 'Risk Reduction'),
            ('social support', 'Social Support')),
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

    def pageblock(self):
        return self.pageblocks.first()

    def needs_submit(self):
        return True

    @classmethod
    def add_form(cls):
        return GoalSettingBlockForm()

    def edit_form(self):
        return GoalSettingBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = GoalSettingBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create()

    def edit(self, vals, files):
        form = GoalSettingBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True

    def __unicode__(self):
        return unicode('Goal Setting Block ' + self.goal_type + ' ' +
                       unicode(self.pk))

    def submit(self, user, request_data):
        pass


class GoalSettingBlockForm(forms.ModelForm):
    class Meta:
        model = GoalSettingBlock


class GoalOption(OrderedModel):
    """GoalSettingBlock dropdowns are populated by GoalOptions."""

    goal_setting_block = models.ForeignKey(GoalSettingBlock)
    text = models.TextField(
        help_text='An option for the dropdowns in a specific ' +
        'GoalSetting pageblock.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.text)


class GoalSettingResponse(models.Model):
    """Participant responses to 'main' and 'extra' goals."""

    goal_setting_block = models.ForeignKey(GoalSettingBlock)
    user = models.ForeignKey(User)
    option = models.ForeignKey(GoalOption)
    text = models.TextField(blank=True, null=True)

    # Correspond this response with a specific form on the block. This
    # can't be higher than self.goal_setting_block.goal_amount - 1.
    form_id = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('goal_setting_block', 'user', 'form_id'),)


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

    goal_setting_response = models.ForeignKey(GoalSettingResponse, unique=True)
    i_will_do_this = models.CharField(
        max_length=255,
        choices=(
            ('yes', 'Yes'),
            ('no', 'No'),
            ('in progress', 'In Progress'),
        ))
    what_got_in_the_way = models.ForeignKey(GoalOption)
    other = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GoalReviewPageBlock(BasePageBlock):
    display_name = 'Goal Review Block'
    template_file = 'goals/goal_review_block.html'

    session_num = models.PositiveSmallIntegerField(
        default=1,
        help_text='The session this is associated with (i.e. 1 through 5).'
    )

    @classmethod
    def add_form(cls):
        return GoalReviewPageBlockForm()

    def edit_form(self):
        return GoalReviewPageBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = GoalReviewPageBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = GoalReviewPageBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class GoalReviewPageBlockForm(forms.ModelForm):
    class Meta:
        model = GoalReviewPageBlock


class GoalCheckInPageBlock(BasePageBlock):
    display_name = 'Goal Check In Block'
    template_file = 'goals/goal_check_in_block.html'

    session_num = models.PositiveSmallIntegerField(
        default=1,
        help_text='The session this is associated with (i.e. 1 through 5).'
    )

    def needs_submit(self):
        return True

    @classmethod
    def add_form(cls):
        return GoalCheckInPageBlockForm()

    def edit_form(self):
        return GoalCheckInPageBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = GoalCheckInPageBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = GoalCheckInPageBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def submit(self, user, request_data):
        pass


class GoalCheckInPageBlockForm(forms.ModelForm):
    class Meta:
        model = GoalCheckInPageBlock
