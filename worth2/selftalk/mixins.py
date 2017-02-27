from django import forms
from django.contrib import messages
from django.shortcuts import render

from worth2.selftalk.forms import RefutationForm, StatementForm
from worth2.selftalk.models import RefutationResponse, StatementResponse
from worth2.selftalk.utils import disable_form_fields


class SelfTalkStatementViewMixin(object):
    """Mixin for StatementBlock form functionality."""

    def _make_statement_form_for_block(self, statementblock):
        """Make the Form class based on the statements in the block.

        :returns: a class
        """

        class DynamicStatementForm(StatementForm):
            def __init__(self, *args, **kwargs):
                super(DynamicStatementForm, self).__init__(
                    *args, **kwargs)
                for statement in statementblock.block().statements.all():
                    self.fields['%d' % statement.pk] = forms.BooleanField(
                        label='"' + statement.text + '"',
                        required=False)

        return DynamicStatementForm

    def create_selftalk_statement_form(self, request, statementblock):
        p = 'pageblock-{:d}'.format(statementblock.pk)

        bound_data = {}
        # If there's existing responses to this pageblock, use them
        # to bind the formset.
        responses = StatementResponse.objects.filter(
            user=request.user,
            statement_block=statementblock.block())
        for r in responses.all():
            bound_data['{}-{}'.format(p, r.statement.pk)] = True
        if bound_data == {}:
            bound_data = None

        DynamicStatementForm = self._make_statement_form_for_block(
            statementblock)
        self.statement_form = DynamicStatementForm(
            data=bound_data, prefix=p)

        if bound_data is not None:
            disable_form_fields(self.statement_form)

    def selftalk_statement_post(self, request, statementblock):
        """This is meant to be called from a django view's post() method.

        :returns: an HttpResponse
        """

        ctx = self.get_context_data()

        DynamicStatementForm = self._make_statement_form_for_block(
            statementblock)
        prefix = 'pageblock-%s' % statementblock.pk
        form = DynamicStatementForm(request.POST, prefix=prefix)
        if form.is_valid():
            disable_form_fields(form)
            self.upv.visit(status="complete")
            messages.success(request, 'Saved.')
            statementblock.block().submit(request.user, form.cleaned_data)
            ctx = self.get_context_data()
            ctx.update({'statement_form': form})
        else:
            msg = 'Error.'
            if form.non_field_errors():
                msg = form.non_field_errors()[0]
            messages.error(request, msg)

        return render(request, self.template_name, ctx)


class SelfTalkRefutationViewMixin(object):
    """Mixin for RefutationBlock form functionality."""

    def _make_refutation_form_for_block(self, user, refutationblock):
        """Make the Form class based on the statement responses in the block.

        :returns: a class
        """

        class DynamicRefutationForm(RefutationForm):
            def __init__(self, *args, **kwargs):
                super(DynamicRefutationForm, self).__init__(
                    *args, **kwargs)

                statement_block = refutationblock.block().statement_block
                responses = statement_block.statementresponse_set.filter(
                    user=user)

                for response in responses:
                    statement = response.statement
                    choices = list(statement.refutation_set.all())
                    choice_ids = [r.pk for r in choices]

                    choices.insert(0, 'Select')
                    choice_ids.insert(0, None)

                    choices.append('Other')
                    choice_ids.append(0)

                    self.fields['refutation-%d' % statement.pk] = \
                        forms.ChoiceField(
                            widget=forms.Select(
                                attrs={'class': 'refutation-dropdown'}),
                            label=statement.text,
                            choices=zip(choice_ids, choices))

                    self.fields['other-%d' % statement.pk] = forms.CharField(
                        widget=forms.TextInput(
                            attrs={
                                'class': 'refutation-other',
                                'placeholder':
                                    'Type how you would turn this around',
                            }),
                        label='',
                        required=False)

        return DynamicRefutationForm

    def create_selftalk_refutation_form(self, request, refutationblock):
        p = 'pageblock-{:d}'.format(refutationblock.pk)

        # If there's existing responses to this pageblock, use them
        # to bind the form.
        bound_data = {}
        responses = RefutationResponse.objects.filter(
            user=request.user,
            refutation_block=refutationblock.block())
        for r in responses.all():
            statement_pk = r.statement.pk
            rkey = '{:s}-refutation-{:d}'.format(p, statement_pk)
            otherkey = '{:s}-other-{:d}'.format(p, statement_pk)
            try:
                bound_data[rkey] = r.refutation.pk
            except AttributeError:
                # If r.refutation is None, this is an 'Other' answer, so give
                # it pk=0.
                bound_data[rkey] = 0
            bound_data[otherkey] = r.other_text
        if bound_data == {}:
            bound_data = None

        DynamicRefutationForm = self._make_refutation_form_for_block(
            request.user, refutationblock)
        self.refutation_form = DynamicRefutationForm(
            data=bound_data, prefix=p)

        if bound_data is not None:
            disable_form_fields(self.refutation_form)

    def selftalk_refutation_post(self, request, refutationblock):
        """This is meant to be called from a django view's post() method.

        :returns: an HttpResponse
        """

        ctx = self.get_context_data()

        DynamicRefutationForm = self._make_refutation_form_for_block(
            request.user, refutationblock)
        prefix = 'pageblock-%s' % refutationblock.pk
        form = DynamicRefutationForm(request.POST, prefix=prefix)
        if form.is_valid():
            disable_form_fields(form)
            self.upv.visit(status="complete")
            messages.success(request, 'Saved.')
            refutationblock.block().submit(request.user, form.cleaned_data)
            ctx = self.get_context_data()
            ctx.update({'refutation_form': form})
        else:
            messages.error(request, 'Error.')

        return render(request, self.template_name, ctx)
