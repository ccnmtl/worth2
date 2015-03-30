import csv
from zipfile import ZipFile
from StringIO import StringIO

from django import http
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import redirect, render

from pagetree.generic.views import PageView
from pagetree.models import PageBlock, Hierarchy
from quizblock.models import Quiz

from worth2.goals.mixins import GoalCheckInViewMixin, GoalSettingViewMixin
from worth2.protectivebehaviors.utils import remove_empty_submission
from worth2.selftalk.mixins import (
    SelfTalkStatementViewMixin, SelfTalkRefutationViewMixin
)
from worth2.main.auth import generate_password, user_is_participant
from worth2.main.forms import SignInParticipantForm
from worth2.main.models import Participant, Session, WorthRawDataReport


def get_quiz_blocks(css_class):
    quiz_type = ContentType.objects.get_for_model(Quiz)
    blocks = PageBlock.objects.filter(css_extra__contains=css_class,
                                      content_type=quiz_type)
    return blocks


def has_responses(section):
    quizzes = [p.block() for p in section.pageblock_set.all()
               if hasattr(p.block(), 'needs_submit')
               and p.block().needs_submit()]
    return quizzes != []


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user_is_participant(user):
            last_location = user.profile.last_location_url()
            if last_location == '/':
                # To prevent a redirect loop, if the participant's last
                # location is this index page, then default to showing them
                # the pagetree root.
                return http.HttpResponseRedirect('/pages/')
            else:
                return http.HttpResponseRedirect(last_location)

        return super(IndexView, self).dispatch(*args, **kwargs)


class ManageParticipants(ListView):
    model = Participant

    def get_queryset(self):
        return Participant.objects.order_by('study_id')

    def get_context_data(self, **kwargs):
        ctx = super(ManageParticipants, self).get_context_data(**kwargs)
        ctx['active_participants'] = [p for p in ctx['object_list']
                                      if not p.is_archived]
        ctx['archived_participants'] = [p for p in ctx['object_list']
                                        if p.is_archived]
        ctx['cohorts'] = Participant.objects.cohort_ids()
        return ctx


class SignInParticipant(FormView):
    template_name = 'main/facilitator_sign_in_participant.html'
    form_class = SignInParticipantForm

    def get_context_data(self, **kwargs):
        ctx = super(SignInParticipant, self).get_context_data(**kwargs)
        ctx.update({'cohorts': Participant.objects.cohort_ids()})
        return ctx

    def form_valid(self, form):
        participant = form.cleaned_data.get('participant_id')
        facilitator = self.request.user
        password = generate_password(participant.user.username)
        user = authenticate(
            username=participant.user.username, password=password)

        if user is not None:
            # Create a Session and log in the participant
            # TODO: a new Session needs to get created for each "session"
            # in pagetree (i.e. module)? Because we need to track whether
            # this participant session is make-up or not.
            Session.objects.get_or_create(
                participant=participant,
                defaults={
                    'facilitator': facilitator,
                    'location': form.cleaned_data.get('participant_location'),
                    'session_type': form.cleaned_data.get('session_type'),
                }
            )

            login(self.request, user)

            dest = form.cleaned_data.get('participant_destination')

            if dest == 'last_completed_activity':
                # TODO: redirect to the last completed activity
                pass
            elif dest == 'next_new_session':
                # TODO: redirect to the next new session
                pass
            elif dest == 'already_completed_session':
                # TODO redirect to the session that the user chose
                # session = request.POST['already_completed_session']
                pass

            # Go to the first session in pagetree
            return redirect('/pages/session-1/')

        return http.HttpResponse('Unauthorized', status=401)


class ParticipantSessionPageView(
        GoalCheckInViewMixin, GoalSettingViewMixin,
        SelfTalkStatementViewMixin, SelfTalkRefutationViewMixin,
        PageView):
    """WORTH version of pagetree's PageView."""

    gated = False

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        path = kwargs['path']
        self.section = self.get_section(path)
        self.goalsettingblock = self.get_first_block_of_type(
            'goal setting block')
        self.goalcheckinblock = self.get_first_block_of_type(
            'goal check in page block')
        self.selftalkstatementblock = self.get_first_block_of_type(
            'statement block')
        self.selftalkrefutationblock = self.get_first_block_of_type(
            'refutation block')

        if self.goalsettingblock:
            self.create_goal_setting_formset(
                request, self.goalsettingblock)
        elif self.goalcheckinblock:
            self.create_goal_check_in_formset(
                request, self.goalcheckinblock)
        elif self.selftalkstatementblock:
            self.create_selftalk_statement_form(
                request, self.selftalkstatementblock)
        elif self.selftalkrefutationblock:
            self.create_selftalk_refutation_form(
                request, self.selftalkrefutationblock)

        return super(ParticipantSessionPageView, self).dispatch(
            request, *args, **kwargs)

    def get_first_block_of_type(self, blocktype):
        """Get the first block of type `blocktype` on this page.

        Returns the block if this page contains it. Otherwise, returns
        None.

        Example usage:
            self.get_first_block_of_type('goal setting block')
        """

        contenttype = ContentType.objects.get(name=blocktype)
        return self.section.pageblock_set.filter(
            content_type=contenttype).first()

    def get_extra_context(self):
        ctx = super(ParticipantSessionPageView, self).get_extra_context()

        if self.goalsettingblock:
            ctx.update({'setting_formset': self.setting_formset})
        elif self.goalcheckinblock:
            ctx.update({
                'checkin_formset': self.checkin_formset,
                'goal_checkin_context': self.goal_checkin_context,
            })
        elif self.selftalkstatementblock:
            ctx.update({
                'statement_form': self.statement_form,
            })
        elif self.selftalkrefutationblock:
            ctx.update({
                'refutation_form': self.refutation_form,
            })

        avatarselectorblock = self.get_first_block_of_type(
            'avatar selector block')
        ctx.update({'avatarselectorblock': avatarselectorblock})

        return ctx

    def get_context_data(self, **kwargs):
        allow_redo = False
        needs_submit = self.section.needs_submit()
        if needs_submit:
            allow_redo = self.section.allow_redo()
        context = dict(
            section=self.section,
            module=self.module,
            needs_submit=needs_submit,
            allow_redo=allow_redo,
            is_submitted=self.section.submitted(self.request.user),
            modules=self.root.get_children(),
            root=self.section.hierarchy.get_root(),
        )
        context.update(self.get_extra_context())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.upv.visit()
        instructor_link = has_responses(self.section)

        # This flag is always False on non-protective behaviors quizzes.
        is_submission_empty = remove_empty_submission(request.user,
                                                      self.section)
        context.update({
            'is_submission_empty': is_submission_empty,
            'instructor_link': instructor_link,
        })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if self.goalsettingblock:
            return self.goal_setting_post(request, self.goalsettingblock)
        elif self.goalcheckinblock:
            return self.goal_check_in_post(request, self.goalcheckinblock)
        elif self.selftalkstatementblock:
            return self.selftalk_statement_post(
                request, self.selftalkstatementblock)
        elif self.selftalkrefutationblock:
            return self.selftalk_refutation_post(
                request, self.selftalkrefutationblock)

        return super(ParticipantSessionPageView, self).post(
            request, *args, **kwargs)


class ParticipantReportView(View):

    def get(self, request):
        report = WorthRawDataReport()

        # setup zip file for the key & value file
        response = HttpResponse(content_type='application/zip')

        disposition = 'attachment; filename=worth.zip'
        response['Content-Disposition'] = disposition

        z = ZipFile(response, 'w')

        output = StringIO()  # temp output file
        writer = csv.writer(output)

        # report on all hierarchies
        hierarchies = Hierarchy.objects.all()

        # Key file
        for row in report.metadata(hierarchies):
            writer.writerow(row)

        z.writestr("worth_key.csv", output.getvalue())

        # Results file
        output.truncate(0)
        output.seek(0)

        writer = csv.writer(output)

        for row in report.values(hierarchies):
            writer.writerow(row)

        z.writestr("worth_values.csv", output.getvalue())

        return response
