from __future__ import unicode_literals

import re
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_str
from ordered_model.models import OrderedModel
from pagetree.generic.models import BasePageBlock

from worth2.main.utils import get_module_number


class Statement(OrderedModel):
    """A negative statement.

    Each Statement has multiple Refutations for the participant to pick
    from.
    """

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Refutation(OrderedModel):
    """A Refutation is an option used to refute a negative statement.

    Each Refutation is tied to a Statement.
    """

    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class StatementBlock(BasePageBlock):
    """A PageBlock for choosing negative statements to refute.

    This block can be either "internal" or "external". Internal refers to
    "My Self Talk", where the subject of the negative statements is the
    user themselves. "External" indicates that this is a scenario based
    around a video, rather than a self-reflective excercise.

    This block gives the participant a list of statements to check off
    either:
      * What they remember hearing in the video they just watched. (If
        is_internal is False).
      * Or, what negative statements they might say to themselves (If
        is_internal is True).

    The statements the participant chooses will populate the fields in
    the next page, which will be a RefutationBlock.
    """

    display_name = 'Self-Talk Negative Statement Block'
    template_file = 'selftalk/statement_block.html'
    css_template_file = 'selftalk/selftalk_css.html'

    statements = models.ManyToManyField(Statement)
    is_internal = models.BooleanField(
        default=True,
        help_text='If True, this will be rendered as a "My Self Talk" ' +
        'block. Otherwise this block\'s subject is a video.')
    subject_name = models.TextField(
        blank=True, null=True,
        help_text='(optional) The name of the video subject for this ' +
        'block, e.g. "Jane"')

    def allow_redo(self):
        return True

    def css_class(self):
        s = 'internal' if self.is_internal else 'external'
        return 'selftalk-statement-%s' % s

    def needs_submit(self):
        return True

    def unlocked(self, user):
        qs = StatementResponse.objects.filter(
            user=user,
            statement_block=self,
        )
        return qs.count() > 0

    def submit(self, user, request_data):
        for k, v in request_data.items():
            statement = Statement.objects.get(pk=int(k))
            if v:
                StatementResponse.objects.update_or_create(
                    statement=statement,
                    statement_block=self,
                    user=user,
                )
            else:
                try:
                    to_delete = StatementResponse.objects.get(
                        statement=statement,
                        statement_block=self,
                        user=user)
                    to_delete.delete()
                except StatementResponse.DoesNotExist:
                    pass

    def clear_user_submissions(self, user):
        StatementResponse.objects.filter(
            user=user, statement_block=self
        ).delete()

    def __str__(self):
        session_num = get_module_number(self.pageblock())

        if self.is_internal:
            block_subtype = 'Internal'
        else:
            block_subtype = 'External'
            if self.subject_name:
                block_subtype = self.subject_name + '\'s'
        return '%s Statement Block [Session %d] id: %d' % (
            block_subtype, session_num, self.pk)

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
        return cls.objects.create(**d)

    def edit(self, vals, files):
        form = StatementBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class StatementBlockForm(forms.ModelForm):
    class Meta:
        model = StatementBlock
        fields = '__all__'
        widgets = {
            'subject_name': forms.TextInput()
        }


class RefutationBlock(BasePageBlock):
    """A PageBlock for refuting negative statements.

    A RefutationBlock is a custom pageblock containing any number of
    statements and their corresponding refutations for participants to
    fill out.

    This block is preceded by the StatementBlock.
    """

    display_name = 'Self-Talk Refutation Block'
    template_file = 'selftalk/refutation_block.html'
    css_template_file = 'selftalk/selftalk_css.html'

    statement_block = models.ForeignKey(StatementBlock,
                                        on_delete=models.CASCADE)

    def allow_redo(self):
        return True

    def css_class(self):
        s = 'internal' if self.is_internal else 'external'
        return 'selftalk-refutation-%s' % s

    @property
    def subject_name(self):
        return self.statement_block.subject_name

    @property
    def is_internal(self):
        return self.statement_block.is_internal

    def needs_submit(self):
        return True

    def unlocked(self, user):
        qs = RefutationResponse.objects.filter(
            user=user,
            refutation_block=self,
        )
        return qs.count() > 0

    def submit(self, user, request_data):
        # Loop through the refutations the user chose
        for k, v in request_data.items():
            match = re.match(r'^refutation-(\d+)$', k)
            if not match:
                continue

            statement_pk = int(match.groups()[0])
            refutation_pk = int(v)

            # Find the optional 'other' text to attach to this response.
            other_text = ''
            if ('other-%d' % statement_pk) in request_data:
                other_text = request_data['other-%d' % statement_pk]

            refutation = Refutation.objects.filter(pk=refutation_pk).first()
            statement = Statement.objects.get(pk=statement_pk)
            RefutationResponse.objects.update_or_create(
                refutation=refutation,
                statement=statement,
                refutation_block=self,
                user=user,
                other_text=other_text,
            )

    def clear_user_submissions(self, user):
        RefutationResponse.objects.filter(
            user=user, refutation_block=self
        ).delete()

    def __str__(self):
        session_num = get_module_number(self.pageblock())

        return '%s [%d] id: %d' % (self.display_name, session_num, self.pk)

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
        return cls.objects.create(**d)

    def edit(self, vals, files):
        form = RefutationBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class RefutationBlockForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = RefutationBlock


class StatementResponse(models.Model):
    """User's statements they chose, for any self-talk scenario."""

    class Meta:
        unique_together = ('statement', 'statement_block', 'user')

    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    statement_block = models.ForeignKey(StatementBlock,
                                        on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    other_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.other_text:
            return self.other_text

        return smart_str(self.statement)


class RefutationResponse(models.Model):
    """User's responses to the self-talk quizzes."""

    class Meta:
        unique_together = ('refutation', 'refutation_block', 'user')

    # refutation is null if this is an 'Other' option
    refutation = models.ForeignKey(Refutation, null=True,
                                   on_delete=models.CASCADE)
    statement = models.ForeignKey(Statement, null=True,
                                  on_delete=models.CASCADE)
    refutation_block = models.ForeignKey(RefutationBlock,
                                         on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    other_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.other_text:
            return self.other_text

        return smart_str(self.refutation)
