from django import forms
from django.contrib.auth.models import User
from django.db import models
from ordered_model.models import OrderedModel

from worth2.main.generic.models import BasePageBlock


class Statement(OrderedModel):
    """A negative statement.

    Each Statement has multiple Refutations for the participant to pick
    from.
    """

    text = models.TextField()
    other_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.other_text:
            return self.other_text

        return self.text


class Refutation(OrderedModel):
    """A Refutation is an option used to refute a negative statement.

    Each Refutation is tied to a Statement.
    """

    statement = models.ForeignKey(Statement)
    text = models.TextField()
    other_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.other_text:
            return self.other_text

        return self.text


class StatementBlock(BasePageBlock):
    """A PageBlock for choosing negative statements to refute.

    This block can be either "internal" or "external". Internal refers to
    "My Self Talk", where the subject of the negative statements is the
    user themselves. "External" indicates that this is a scenario based
    around a video, rather than a self-reflective excercise.

    If this block is "external", it gives the participant a list of
    statements to check off what they remember hearing in the video they
    just watched.

    The statements the participant chooses will populate the fields in
    the next page, which will be a RefutationBlock.
    """

    display_name = 'Self-Talk Negative Statement Block'
    template_file = 'selftalk/statement_block.html'

    statements = models.ManyToManyField(Statement)
    is_internal = models.BooleanField(
        default=True,
        help_text='If True, this will be rendered as a "My Self Talk" ' +
        'block. Otherwise this block\'s subject is a video.')
    subject_name = models.TextField(
        blank=True, null=True,
        help_text='(optional) The name of the video subject for this ' +
        'block, e.g. "Jane"')

    def needs_submit(self):
        return True

    def unlocked(self, user):
        # TODO create logic here
        return False

    def __unicode__(self):
        try:
            slug = self.pageblock().section.get_parent().slug
        except AttributeError:
            slug = 'no section'

        return unicode(self.display_name + '[' + slug + '] id: ' +
                       unicode(self.pk))

    @staticmethod
    def add_form():
        return StatementBlockForm()

    def edit_form(self):
        return StatementBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = StatementBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create()

    def edit(self, vals, files):
        form = StatementBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class StatementBlockForm(forms.ModelForm):
    class Meta:
        model = StatementBlock

    subject_name = forms.CharField()


class RefutationBlock(BasePageBlock):
    """A PageBlock for refuting negative statements.

    A RefutationBlock is a custom pageblock containing any number of
    statements and their corresponding refutations for participants to
    fill out.

    This block is preceded by the StatementBlock.
    """

    display_name = 'Self-Talk Refutation Block'
    template_file = 'selftalk/refutation_block.html'

    statement_block = models.ForeignKey(StatementBlock)

    @property
    def subject_name(self):
        return self.statement_block.subject_name

    @property
    def is_internal(self):
        return self.statement_block.is_internal

    def needs_submit(self):
        return True

    def unlocked(self, user):
        # TODO create logic here
        return False

    def __unicode__(self):
        try:
            slug = self.pageblock().section.get_parent().slug
        except AttributeError:
            slug = 'no section'

        return unicode(self.display_name + '[' + slug + '] id: ' +
                       unicode(self.pk))

    @staticmethod
    def add_form():
        return RefutationBlockForm()

    def edit_form(self):
        return RefutationBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = RefutationBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create()

    def edit(self, vals, files):
        form = RefutationBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class RefutationBlockForm(forms.ModelForm):
    class Meta:
        model = RefutationBlock


class StatementResponse(models.Model):
    """User's statements they chose, for any self-talk scenario."""

    class Meta:
        unique_together = ('statement', 'statement_block', 'user')

    statement = models.ForeignKey(Statement)
    statement_block = models.ForeignKey(StatementBlock)
    user = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RefutationResponse(models.Model):
    """User's responses to the self-talk quizzes."""

    class Meta:
        unique_together = ('refutation', 'refutation_block', 'user')

    refutation = models.ForeignKey(Refutation)
    refutation_block = models.ForeignKey(RefutationBlock)
    user = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
