from django import http
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import redirect, render

from pagetree.generic.views import PageView
from pagetree.models import PageBlock
import quizblock
from quizblock.models import Quiz

from worth2.goals.mixins import GoalCheckInViewMixin, GoalSettingViewMixin
from worth2.main.auth import generate_password, user_is_participant
from worth2.main.forms import SignInParticipantForm
from worth2.main.models import Participant, Session


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
        PageView):
    """WORTH version of pagetree's PageView."""

    gated = True

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        path = kwargs['path']
        self.section = self.get_section(path)
        goalsettingblock = self.get_first_block_of_type('goal setting block')
        goalcheckinblock = self.get_first_block_of_type(
            'goal check in page block')

        if goalsettingblock:
            self.create_goal_setting_formset(request, goalsettingblock)
        elif goalcheckinblock:
            self.create_goal_check_in_formset(request, goalcheckinblock)

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
        blocks = self.section.pageblock_set.filter(content_type=contenttype)
        return blocks.first()

    def get_extra_context(self):
        ctx = super(ParticipantSessionPageView, self).get_extra_context()

        goalsettingblock = self.get_first_block_of_type('goal setting block')
        goalcheckinblock = self.get_first_block_of_type(
            'goal check in page block')
        if goalsettingblock:
            ctx.update({'setting_formset': self.setting_formset})
        elif goalcheckinblock:
            ctx.update({
                'checkin_formset': self.checkin_formset,
                'goal_checkin_context': self.goal_checkin_context,
            })

        return ctx

    def get_context_data(self, **kwargs):
        context = dict(
            section=self.section,
            module=self.module,
            is_submitted=self.section.submitted(self.request.user),
            modules=self.root.get_children(),
            root=self.section.hierarchy.get_root(),
        )
        context.update(self.get_extra_context())
        return context

    def get(self, request, *args, **kwargs):
        allow_redo = False
        needs_submit = self.section.needs_submit()
        if needs_submit:
            allow_redo = self.section.allow_redo()
        self.upv.visit()
        instructor_link = has_responses(self.section)

        pageblocks = self.section.pageblock_set.all()
        quiztypes = ContentType.objects.filter(
            Q(name='quiz') | Q(name='rate my risk quiz'))
        quizblocks_on_this_page = [
            page.block() for page in
            pageblocks.filter(content_type__in=quiztypes)]

        # Was the form submitted with no values selected?
        # TODO: move this logic to a RateMyRiskViewMixin.
        is_submission_empty = False
        for submission in quizblock.models.Submission.objects.filter(
                user=request.user, quiz__in=quizblocks_on_this_page):
            if quizblock.models.Response.objects.filter(
                    submission=submission).count() == 0:
                # Delete empty submission, and tell the template that it was
                # empty, so it can display an error message.
                submission.delete()
                is_submission_empty = True

        context = self.get_context_data(**kwargs)
        context.update({
            'allow_redo': allow_redo,
            'is_submission_empty': is_submission_empty,
            'needs_submit': needs_submit,
            'instructor_link': instructor_link,
        })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        goalsettingblock = self.get_first_block_of_type('goal setting block')
        goalcheckinblock = self.get_first_block_of_type(
            'goal check in page block')

        if goalsettingblock:
            return self.goal_setting_post(request, goalsettingblock)
        elif goalcheckinblock:
            return self.goal_check_in_post(request, goalcheckinblock)

        return super(ParticipantSessionPageView, self).post(
            request, *args, **kwargs)
