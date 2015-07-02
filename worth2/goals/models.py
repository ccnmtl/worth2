from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str
from ordered_model.models import OrderedModel
from pagetree.generic.models import BasePageBlock
from pagetree.reports import ReportColumnInterface, ReportableInterface

from worth2.main.utils import get_first_block_in_module, get_module_number


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
        session_num = get_module_number(self.pageblock())
        return unicode('%s goals [Session %d] id: %d' % (
            self.get_goal_type_display(),
            session_num,
            self.pk))

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

    def report_metadata(self):
        rows = []
        options = GoalOption.objects.filter(goal_type=self.goal_type)
        for idx in xrange(0, self.goal_amount):
            for option in options:  # 1 row per option
                col = GoalSettingColumn(self, idx, 'option', option)
                rows.append(col)
            rows.append(GoalSettingColumn(self, idx, 'other_text'))
            rows.append(GoalSettingColumn(self, idx, 'text'))
        return rows

    def report_values(self):
        rows = []
        for idx in xrange(0, self.goal_amount):
            rows.append(GoalSettingColumn(self, idx, 'option'))
            rows.append(GoalSettingColumn(self, idx, 'other_text'))
            rows.append(GoalSettingColumn(self, idx, 'text'))
        return rows


class GoalSettingBlockForm(forms.ModelForm):
    class Meta:
        model = GoalSettingBlock
        fields = '__all__'


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


class GoalSettingResponseManager(models.Manager):
    def find_by_module(self, user, goaltype, module):
        """Get a queryset of goal responses.

        :param goaltype: See worth2.goals.models.GOAL_TYPES

        :type user: User
        :type goaltype: string
        :type module: int

        :rtype: queryset
        """
        goalsettingblock = get_first_block_in_module(
            'goals',
            'goalsettingblock',
            module,
            lambda (b): b.block().goal_type == goaltype)
        if goalsettingblock:
            return self.filter(
                goal_setting_block=goalsettingblock.block(),
                user=user)
        else:
            self.none()


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

    objects = GoalSettingResponseManager()

    class Meta:
        unique_together = (('goal_setting_block', 'user', 'form_id'),)

    def __unicode__(self):
        return unicode('"%s" from %s' % (unicode(self.option),
                                         unicode(self.user)))


class GoalSettingColumn(ReportColumnInterface):

    def __init__(self, block, goal_idx, field, option=None):
        self.block = block
        self.hierarchy = block.pageblock().section.hierarchy
        self.description = "%s %s %s" % (
            block.goal_type.capitalize(), goal_idx, field.capitalize())
        self.field = field
        self.option = option
        self.goal_idx = goal_idx

    def identifier(self):
        return "%s_%s_%s_%s" % (self.block.id, slugify(self.block.goal_type),
                                self.goal_idx, self.field)

    def metadata(self):
        metadata = [self.hierarchy.name, self.identifier(),
                    self.block.display_name]
        if self.field == 'option':
            metadata.append('single choice')
            metadata.append(self.description)
            metadata.append(self.option.id)
            metadata.append(smart_str(self.option.text))
        else:
            metadata.append('string')
            metadata.append(self.description)

        return metadata

    def user_value(self, user):
        # retrieve last response. (though there should be just 1)
        response = GoalSettingResponse.objects.filter(
            user=user, goal_setting_block=self.block,
            form_id=self.goal_idx).order_by('-updated_at').first()

        if response is None:
            return ''
        elif self.field == 'option':
            return response.option.id
        else:
            return getattr(response, self.field) or ''  # replace None with ''


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

    goal_setting_response = models.OneToOneField(
        GoalSettingResponse,
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

    PROGRESS_CHOICES = (
        ('yes', 'I did it!'),
        ('in progress', 'I\'m still working on it.'),
        ('no', 'I haven\'t started this goal.'),
    )

    def needs_submit(self):
        return True

    def goal_setting_responses(self, user):
        return self.goal_setting_block.goal_setting_responses.filter(user=user)

    def unlocked(self, user):
        # Find out if this user has created any GoalCheckinResponses for
        # this GoalCheckinBlock.
        setting_responses = self.goal_setting_responses(user=user)

        if setting_responses.count() == 0:
            return True

        for setting_response in setting_responses:
            checkin_response = None
            try:
                checkin_response = setting_response.goal_checkin_response
            except ObjectDoesNotExist:
                continue

            if checkin_response is not None:
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

    def report_metadata(self):
        rows = []
        for idx in xrange(0, self.goal_setting_block.goal_amount):
            for chc in self.PROGRESS_CHOICES:
                col = GoalCheckInColumn(self, idx, "progress", chc[0], chc[1])
                rows.append(col)
            for opt in GoalCheckInOption.objects.all():
                col = GoalCheckInColumn(self, idx, "barrier", opt.id, opt.text)
                rows.append(col)
            rows.append(GoalCheckInColumn(self, idx, "other"))
        return rows

    def report_values(self):
        rows = []
        for idx in xrange(0, self.goal_setting_block.goal_amount):
            rows.append(GoalCheckInColumn(self, idx, "progress"))
            rows.append(GoalCheckInColumn(self, idx, "barrier"))
            rows.append(GoalCheckInColumn(self, idx, "other"))
        return rows


class GoalCheckInPageBlockForm(forms.ModelForm):
    class Meta:
        model = GoalCheckInPageBlock
        fields = '__all__'


class GoalCheckInColumn(ReportColumnInterface):

    def __init__(self, block, goal_idx, field, value=None, label=None):
        self.block = block
        self.hierarchy = block.pageblock().section.hierarchy
        self.goal_idx = goal_idx
        self.answer_value = value
        self.answer_label = label
        self.field = field

        goal_setting_block = block.goal_setting_block
        self.progress_identifier = "%s_%s_%s_%s" % (
            goal_setting_block.id, slugify(goal_setting_block.goal_type),
            goal_idx, field)

        self.description = "%s %s Checkin %s" % (
            goal_setting_block.goal_type.capitalize(),
            goal_idx, field.capitalize())

    def identifier(self):
        return self.progress_identifier

    def metadata(self):
        metadata = [self.hierarchy.name, self.progress_identifier,
                    self.block.display_name]

        if self.answer_value is None:
            metadata.append('string')
            metadata.append(self.description)
        else:
            metadata.append('single choice')
            metadata.append(self.description)
            metadata.append(self.answer_value)
            metadata.append(smart_str(self.answer_label))

        return metadata

    def user_value(self, user):
        responses = GoalSettingResponse.objects.filter(
            user=user, form_id=self.goal_idx,
            goal_setting_block=self.block.goal_setting_block)

        response = GoalCheckInResponse.objects.filter(
            goal_setting_response=responses).order_by('-updated_at').first()

        if response is None:
            return ''
        elif self.field == 'progress':
            return response.i_will_do_this
        elif self.field == 'barrier':
            return response.what_got_in_the_way.id if \
                response.what_got_in_the_way else ''
        else:
            return response.other or ''

ReportableInterface.register(GoalSettingBlock)
ReportableInterface.register(GoalCheckInPageBlock)
