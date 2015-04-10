from django import forms
from django.contrib import messages
from django.shortcuts import render

from worth2.selftalk.forms import RefutationForm
from worth2.selftalk.models import RefutationResponse, StatementResponse


class SelfTalkStatementViewMixin(object):
    """Mixin for StatementBlock form functionality."""

    def _make_statement_form_for_block(self, statementblock):
        """Make the Form class based on the statements in the block.

        :returns: a class
        """

        class DynamicStatementForm(forms.Form):
            def __init__(self, *args, **kwargs):
                super(DynamicStatementForm, self).__init__(
                    *args, **kwargs)
                for statement in statementblock.block().statements.all():
                    self.fields['%d' % statement.pk] = forms.BooleanField(
                        label='"' + statement.text + '"',
                        required=False)

        return DynamicStatementForm

    def create_selftalk_statement_form(self, request, statementblock):
        initial_data = {}
        # If there's existing responses to this pageblock, use them
        # to bind the formset.
        responses = StatementResponse.objects.filter(
            user=request.user,
            statement_block=statementblock.block())
        for i, r in enumerate(responses.all()):
            initial_data[unicode(i)] = r.statement.text

        DynamicStatementForm = self._make_statement_form_for_block(
            statementblock)
        prefix = 'pageblock-%s' % statementblock.pk
        self.statement_form = DynamicStatementForm(
            prefix=prefix, initial=initial_data)

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
            messages.success(request, 'Saved.')
            statementblock.block().submit(request.user, form.cleaned_data)
            ctx = self.get_context_data()
            ctx.update({'statement_form': form})
        else:
            messages.error(request, 'Error.')

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
                                'placeholder': 'Other',
                            }),
                        label='',
                        required=False)

        return DynamicRefutationForm

    def create_selftalk_refutation_form(self, request, refutationblock):
        # If there's existing responses to this pageblock, use them
        # to bind the form.
        initial_data = {}
        responses = RefutationResponse.objects.filter(
            user=request.user,
            refutation_block=refutationblock.block())
        for r in responses.all():
            statement_pk = r.statement.pk
            try:
                initial_data['refutation-%d' % statement_pk] = r.refutation.pk
            except:
                # If r.refutation is None, this is an 'Other' answer, so give
                # it pk=0.
                initial_data['refutation-%d' % statement_pk] = 0
            initial_data['other-%d' % statement_pk] = r.other_text

        DynamicRefutationForm = self._make_refutation_form_for_block(
            request.user, refutationblock)
        prefix = 'pageblock-%s' % refutationblock.pk
        self.refutation_form = DynamicRefutationForm(
            prefix=prefix,
            initial=initial_data)

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
            messages.success(request, 'Saved.')
            refutationblock.block().submit(request.user, form.cleaned_data)
            ctx = self.get_context_data()
            ctx.update({'refutation_form': form})
        else:
            messages.error(request, 'Error.')

        return render(request, self.template_name, ctx)
