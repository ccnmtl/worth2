from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django import forms
from ordered_model.models import OrderedModel
from pagetree.models import PageBlock

from worth2.main.auth import user_is_participant


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

    session = models.CharField(max_length=255, choices=(
        ('session 1', 'Session 1'),
        ('session 2', 'Session 2'),
        ('session 3', 'Session 3'),
        ('session 4', 'Session 4'),
        ('session 5', 'Session 5'),
    ))

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
        if user_is_participant(user):
            return


class GoalSettingBlockForm(forms.ModelForm):
    class Meta:
        model = GoalSettingBlock


class GoalOption(OrderedModel):
    """GoalSettingBlock dropdowns are populated by GoalOptions."""

    goal_setting_block = models.ForeignKey(GoalSettingBlock)
    text = models.TextField()

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
