from django import http
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.webdesign import lorem_ipsum
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect, render

from pagetree.generic.views import PageView
from pagetree.models import PageBlock, Section
from quizblock.models import Quiz

from worth2.goals.mixins import GoalCheckInViewMixin, GoalSettingViewMixin
from worth2.goals.models import GoalSettingResponse
from worth2.protectivebehaviors.utils import remove_empty_submission
from worth2.selftalk.mixins import (
    SelfTalkStatementViewMixin, SelfTalkRefutationViewMixin
)
from worth2.main.auth import generate_password, user_is_participant
from worth2.main.forms import SignInParticipantForm
from worth2.main.models import Encounter, Participant
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

    @staticmethod
    def _render_goals(goalsettingblock, user):
        """Render a goalsettingblock's responses.

        :param goalsettingblock: The Goal Setting block to render.

        :rtype: string
        """
        out = [u'']
        responses = []
        if goalsettingblock:
            responses = GoalSettingResponse.objects.filter(
                goal_setting_block=goalsettingblock.block(),
                user=user)

        for response in responses:
            s = [u'']
            # I will (goal field)
            # My plan (details field)
            s.append(u'<div>Goal option: ' +
                     u'<strong>%s</strong></div>' % response.option)
            if response.other_text:
                s.append(u'<div>Other: ' +
                         u'<strong>%s</strong></div>' % response.other_text)
            s.append(
                u'<div>My plan: <strong>%s</strong></div>' % response.text)

            out.append(u''.join(s))

        return u''.join(out)

    def _render_session_1(self, user):
        """Render info for session 1 summary.

        :param user: The user to report on.

        :returns: An array.
        """
        # 'info' is the array of strings that's returned at the end of
        # this function. Make sure the strings are unicode, because
        # there could be unicode data in participant's responses, and
        # adding unicode data to a non-unicode string causes an error.
        info = [
            u'<h3>General Info About WORTH</h3>' +
            u'<p>' + lorem_ipsum.paragraph() + u'</p>',

            u'<h3>General info about HIV Testing</h3>' +
            u'<p>' + lorem_ipsum.paragraph() + u'</p>',
        ]

        # Find the first 'services' type goal setter in Session 1
        goalsettingblock = get_first_block_in_session(
            'goal setting block', 1,
            lambda (b): b.block().goal_type == 'services')

        info.append(u'<h3>Goals set for Services</h3>')
        info.append(self._render_goals(goalsettingblock, user))

        info += [
            u'<h3>Services info selected to view (participant answers)</h3>' +
            u'<strong>TODO: implement this once the services activity is ' +
            u'in place: ' +
            u'https://worth2.ccnmtl.columbia.edu/' +
            u'pages/edit/session-1/services/',
            u'My issue (issue selected)',

            u'List of organizations with name/address/contact ' +
            u'info for above issue',
        ]

        return info

    def _render_session_2(self, user):
        info = [
            u'<h3>Introduction to Session 2 Road Map</h3>' +
            u'<p>Here is your personal road map for this week. It lists ' +
            u'information you learned this week, as well as your ' +
            u'answers to some of the questions from the session, the ' +
            u'goals you set, and service organizations you can reach ' +
            u'out to for help meeting your goals.</p>',

            u'<h3>I am WORTH it!</h3>' +
            u'<p>It is important to take a moment out of our busy lives to ' +
            u'remind ourselves why we are WORTH it. Here are some words ' +
            u'that describe why you are worth it:</p>' +

            u'<p>I am worth it selected words (participant answers) ' +
            u'<strong>TODO: Implement this when activity here is filled in: ' +
            u'https://worth2.ccnmtl.columbia.edu/' +
            u'pages/edit/session-2/i-am-worth-it/' +
            u'</strong></p>',

            u'<h3>Info from montage 2</h3>' +
            u'<em>Karen/Blondell to write</em>',

            # TODO
            u'<h3>Reflect on the characters answers ' +
            u'(participant answers)</h3>' +
            u'<p>This week you learned about five ' +
            u'women and listened to them talk about issues in their ' +
            u'lives. Here are some of the issues they raised and how ' +
            u'important you think they are in your life:</p>' +
            u'<p>question text</p>' +
            u'<p>participant answer</p>' +
            u'<p>example: "Sometimes it is just too hard to cope" ' +
            u'This is [a big issue] for me.</p>',

            u'<h3>Myth/Fact Info</h3>' +
            u'<p>' + lorem_ipsum.paragraph() + u'</p>',

            # TODO
            u'<h3>Protective behaviors (participant answers)</h3>' +
            u'<p>This week you thought about ' +
            u'activities you do and how risky they are. Here is the ' +
            u'list you wrote of things you do ranked by risk level."',
            u'list of behaviors participant does ranked/coded by risk ' +
            u'level</p>' +
            u'<p>Here is how you rated your own risk level:</p>' +
            u'<p>participant\'s self risk rating</p>',

            # TODO
            u'<h3>Goals set in session 2 (participant answers)</h3>' +
            u'<p>In this session you set goals to ' +
            u'reduce your risk of contracting HIV or other sexually ' +
            u'transmitted infections and goals to access a service.</p>',
        ]

        # Find the first 'risk reduction' goal setter in Session 2
        risk_goalsettingblock = get_first_block_in_session(
            'goal setting block', 2,
            lambda (b): b.block().goal_type == 'risk reduction')

        info.append('<h3>My risk reduction goals</h3>')
        info.append(self._render_goals(risk_goalsettingblock, user))

        # Find the first 'services' goal setter in Session 2
        services_goalsettingblock = get_first_block_in_session(
            'goal setting block', 2,
            lambda (b): b.block().goal_type == 'services')

        info.append('<h3>My services goals</h3>')
        info.append(self._render_goals(services_goalsettingblock, user))

        info += [
            # TODO
            u'<h3>Services info selected to view (participant answers)</h3>' +
            u'<p>My issue (issue selected)</p>' +
            u'<p>List of organizations with name/address/contact info ' +
            u'for above issue.</p>' +
            u'<p>example: "This week you looked for information on ' +
            u'[selected issue]. Here is a list of organizations you ' +
            u'can contact to help you with this issue."</p>',

            u'<h3>Wrap Up</h3>' +
            u'<p>Congratulations on completing session two of E-WORTH! ' +
            u'Remember that your homework for the week is to work on ' +
            u'the goals you set today.</p>' +
            u'<p>I am WORTH IT! And I will stay healthy.</p>' +
            u'<p>I am WORTH IT! And I will protect myself.</p>' +
            u'<p>I am WORTH IT! And I will find support for my health</p>',
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
        context['participant'] = get_object_or_404(Participant,
                                                   pk=kwargs['pk'])
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

        # I'm explicitly setting the participant's password each time
        # they log in. In reality, this shouldn't have any effect. I'm
        # doing this because when I don't, the authenticate() call
        # below returns False during the tests.
        participant.user.set_password(password)
        participant.user.save()

        user = authenticate(
            username=participant.user.username, password=password)

        if user is not None:
            login(self.request, user)

            dest = form.cleaned_data.get('participant_destination')

            # Go to the first session in pagetree by default.
            section = get_object_or_404(Section, slug='session-1')

            if dest == 'last_completed_activity':
                section = participant.last_location()
            elif dest == 'next_new_session':
                section = participant.last_location().get_next()
            elif dest == 'already_completed_session':
                session_num = form.cleaned_data.get(
                    'already_completed_session')
                slug = 'session-%s' % session_num
                section = get_object_or_404(Section, slug=slug)

            Encounter.objects.create(
                participant=participant,
                facilitator=facilitator,
                location=form.cleaned_data.get('participant_location'),
                session_type=form.cleaned_data.get('session_type'),
                section=section)
            return redirect(section.get_absolute_url())

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
