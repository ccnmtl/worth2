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
        return unicode('Goal Setting Block ' + unicode(self.pk))

    def submit(self, user, request_data):
        if user_is_participant(user):
            return


class GoalSettingBlockForm(forms.ModelForm):
    class Meta:
        model = GoalSettingBlock


class GoalSlot(OrderedModel):
    """A model for specifying the goal categories for a GoalSettingBlock.

    GoalSlots are editable in the admin interface. After creating a
    Goal Setting pageblock, you can customize it by adding GoalSlots to
    it.
    """

    class Meta(OrderedModel.Meta):
        pass

    GOAL_SLOT_TYPES = (
        ('general services', 'General Services'),
        ('risk reduction', 'Risk Reduction'),
        ('social support', 'Social Support'),
    )

    goal_setting_block = models.ForeignKey(GoalSettingBlock)
    goal_type = models.CharField(max_length=255, choices=GOAL_SLOT_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def has_not_any_option(self):
        """Returns True if this goal slot has a n/a option."""

        return self.goal_type == 'general services' or \
            self.goal_type == 'social support'

    def __unicode__(self):
        return unicode(self.goal_type) + ' for ' + \
            unicode(self.goal_setting_block)


class GoalSlotOption(OrderedModel):
    """GoalSlot dropdowns are populated by GoalSlotOptions."""

    goal_slot = models.ForeignKey(GoalSlot)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GoalSlotSubmission(models.Model):
    """A participant's goal submission for a goal slot."""

    goal_slot = models.ForeignKey(GoalSlot)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GoalSlotResponse(models.Model):
    """Participant responses to 'main' and 'extra' GoalSlot goals."""

    goal_slot_submission = models.ForeignKey(GoalSlotSubmission)
    option = models.ForeignKey(GoalSlotOption)
    text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
