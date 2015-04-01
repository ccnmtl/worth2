from django import http
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.webdesign import lorem_ipsum
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import redirect, render

from pagetree.generic.views import PageView
from pagetree.models import PageBlock
from quizblock.models import Quiz

from worth2.goals.mixins import GoalCheckInViewMixin, GoalSettingViewMixin
from worth2.goals.models import GoalSettingResponse
from worth2.protectivebehaviors.utils import remove_empty_submission
from worth2.selftalk.mixins import (
    SelfTalkStatementViewMixin, SelfTalkRefutationViewMixin
)
from worth2.main.auth import generate_password, user_is_participant
from worth2.main.forms import SignInParticipantForm
from worth2.main.models import Participant, Session
from worth2.main.utils import (
    get_first_block_in_session, get_first_block_of_type
)


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


class ParticipantJournalView(TemplateView):
    model = Participant
    template_name = 'main/participant_journal.html'

    def _render_session_1(self, user):
        """Render info for session 1 summary.

        :param user: The user to report on.

        :returns: An array.
        """

        info = [
            u'<h3>General Info About WORTH (static)</h3>' +
            u'<p>' + lorem_ipsum.paragraph() + u'</p>',

            u'<h3>General info about HIV Testing (static)</h3>' +
            u'<p>' + lorem_ipsum.paragraph() + u'</p>',
        ]

        goalsettingblock = get_first_block_in_session(
            'goal setting block', 1)
        if goalsettingblock:
            r = GoalSettingResponse.objects.filter(
                goal_setting_block=goalsettingblock.block(),
                user=user)
        else:
            r = []

        info.append(u'<h3>Goals set for "services"</h3>')
        for response in r:
            # Goals set for Services (participant answers)

            s = u''
            # I will (goal field)
            # My plan (details field)
            s += u'<div>Goal option: ' + \
                 u'<strong>%s</strong></div>' % response.option
            if response.other_text:
                s += u'<div><strong>%s</strong></div>' % response.other_text
            s += u'<div>My plan: <strong>%s</strong></div>' % response.text

            info.append(s)

        info += [
            u'Services info selected to view (participant answers)',
            u'My issue (issue selected)',

            u'List of organizations with name/address/contact ' +
            u'info for above issue',
        ]

        return info

    def _render_session_2(self, user):
        info = [
            'Introduction to Session 2 Road map (static)',
            'Here is your personal road map for this week. It lists ' +
            'information you learned this week, as well as your ' +
            'answers to some of the questions from the session, the ' +
            'goals you set, and service organizations you can reach ' +
            'out to for help meeting your goals.',

            'I am WORTH it!',
            'It is important to take a moment out of our busy lives to ' +
            'remind ourselves why we are WORTH it. Here are some words ' +
            'that describe why you are worth it:',
            'I am worth it selected words (participant answers)',
            'Info from montage 2(static)',
            'Karen/Blondell to write',
            'Reflect on the characters answers (participant answers)',
            'static intro paragraph: "This week you learned about five ' +
            'women and listened to them talk about issues in their ' +
            'lives. Here are some of the issues they raised and how ' +
            'important you think they are in your life:"',
            'question text',
            'participant answer',
            'example: "Sometimes it is just too hard to cope" ' +
            'This is [a big issue] for me.',
            'Myth/fact info (static)'
            'Protective behaviors (participant answers)',
            'static intro paragraph "This week you thought about ' +
            'activities you do and how risky they are. Here is the ' +
            'list you wrote of things you do ranked by risk level."',
            'list of behaviors participant does ranked/coded by risk ' +
            'level',
            'Static intro paragraph to rating: "Here is how you rated ' +
            'your own risk level:"',
            'participant\'s self risk rating',
            'Goals set in session 2(participant answers)',
            'Static intro paragraph: "In this session you set goals to ' +
            'reduce your risk of contracting HIV or other sexually ' +
            'transmitted infections and goals to access a service."',
            'My risk reduction goals',
            'I will (goal field)',
            'My plan (details field)',
            'My services goals',
            'I will (goal field)',
            'My plan (details field)',
            'Services info selected to view (participant answers)',
            'My issue (issue selected)',
            'List of organizations with name/address/contact info ' +
            'for above issue',
            'example: "This week you looked for information on ' +
            '[selected issue]. Here is a list of organizations you ' +
            'can contact to help you with this issue."',
            'Wrap up(static)',
            'Congratulations on completing session two of E-WORTH! ' +
            'Remember that your homework for the week is to work on ' +
            'the goals you set today.',
            'I am WORTH IT! and I will stay healthy',
            'I am WORTH IT! and I will protect myself',
            'I am WORTH IT! and I will find support for my health',
        ]
        return info

    def _render_session_3(self, user):
        return []

    def _render_session_4(self, user):
        return []

    def _render_session_5(self, user):
        return []

    def get_context_data(self, **kwargs):
        context = super(ParticipantJournalView, self).get_context_data(
            **kwargs)

        # Participant's pk is in the URL
        context['participant'] = Participant.objects.get(pk=kwargs['pk'])
        user = context['participant'].user

        context['journal_info'] = []

        session_num = int(kwargs['session_num'])
        if session_num == 1:
            context['journal_info'] = self._render_session_1(user)
        elif session_num == 2:
            context['journal_info'] = self._render_session_2(user)
        elif session_num == 3:
            context['journal_info'] = self._render_session_3(user)
        elif session_num == 4:
            context['journal_info'] = self._render_session_4(user)
        elif session_num == 5:
            context['journal_info'] = self._render_session_5(user)

        return context


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
        self.goalsettingblock = get_first_block_of_type(
            self.section, 'goal setting block')
        self.goalcheckinblock = get_first_block_of_type(
            self.section, 'goal check in page block')
        self.selftalkstatementblock = get_first_block_of_type(
            self.section, 'statement block')
        self.selftalkrefutationblock = get_first_block_of_type(
            self.section, 'refutation block')

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

        avatarselectorblock = get_first_block_of_type(
            self.section, 'avatar selector block')
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
        if request.POST.get('action') != 'reset':
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
