from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from pagetree.generic.views import PageView
from pagetree.models import PageBlock, Section
from quizblock.models import Quiz

from worth2.goals.mixins import GoalCheckInViewMixin, GoalSettingViewMixin
from worth2.goals.models import GoalSettingResponse
from worth2.main.utils import (
    get_first_block_of_type, get_quiz_responses_by_css_in_module,
    last_location_url, percent_complete_by_module,
    percent_complete_hierarchy
)
from worth2.protectivebehaviors.utils import remove_empty_submission
from worth2.selftalk.mixins import (
    SelfTalkStatementViewMixin, SelfTalkRefutationViewMixin
)
from worth2.ssnm.models import Supporter


def get_quiz_blocks(css_class):
    quiz_type = ContentType.objects.get_for_model(Quiz)
    blocks = PageBlock.objects.filter(css_extra__contains=css_class,
                                      content_type=quiz_type)
    return blocks


def has_responses(section):
    quizzes = [p.block() for p in section.pageblock_set.all()
               if hasattr(p.block(), 'needs_submit') and
               p.block().needs_submit()]
    return quizzes != []


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['last_location'] = last_location_url(self.request.user)
        ctx['percent_complete'] = percent_complete_hierarchy(self.request.user)

        ctx['completed'] = 0
        for x in range(1, 6):
            if percent_complete_by_module(self.request.user, x) == 100:
                ctx['completed'] += 1

        return ctx


class JournalView(LoginRequiredMixin, TemplateView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        try:
            session_num = int(kwargs.get('session_num'))
        except TypeError:
            raise http.Http404

        context['session_num'] = session_num
        slug = 'session-%d' % session_num
        context['section'] = get_object_or_404(Section, slug=slug)

        context['my_services_issue'] = get_quiz_responses_by_css_in_module(
            user, 'services-quiz', session_num).first()

        if session_num > 1:
            context['i_am_worth_it_responses'] = \
                map(lambda x: x.answer(),
                    get_quiz_responses_by_css_in_module(
                        user, 'i-am-worth-it-quiz', session_num))
        if session_num == 5:
            context['i_am_proud_responses'] = \
                map(lambda x: x.answer(),
                    get_quiz_responses_by_css_in_module(
                        user, 'i-am-proud-quiz', session_num))

        # Add module-specific context data to the response here.
        dispatch = {
            1: session_1_context,
            2: session_2_context,
            3: session_3_context,
            4: session_4_context,
            5: session_5_context,
        }
        if session_num not in dispatch:
            raise http.Http404

        context.update(dispatch[session_num](user, session_num))

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            session_num = int(kwargs.get('session_num'))
        except TypeError:
            raise http.Http404

        try:
            return render(request,
                          'main/session_%d_journal.html' % session_num,
                          context)
        except TemplateDoesNotExist:
            raise http.Http404


def session_1_context(user, session_num):
    # Find the first 'services' type goal setter in Session 1
    return {
        'session_title': 'Let\'s Talk: Sister to Sister',
        'goals_services_responses':
        GoalSettingResponse.objects.find_by_module(
            user, 'services', session_num),
    }


def session_2_context(user, session_num):
    reflection_responses = get_quiz_responses_by_css_in_module(
        user, 'post-video-quiz', 2)
    return {
        'session_title': 'What\'s the 411?',
        'reflection_big_issues': filter(
            lambda x: x.value == '1',
            reflection_responses),
        'reflection_issues': filter(
            lambda x: (x.value == '1' or x.value == '2'),
            reflection_responses),
        'i_am_worth_it_responses':
            get_quiz_responses_by_css_in_module(
                user, 'i-am-worth-it-quiz', session_num),
        'rate_my_risk_response':
            get_quiz_responses_by_css_in_module(
                user, 'rate-my-risk', session_num).first(),
        'goals_risk_responses':
            GoalSettingResponse.objects.find_by_module(
                user, 'risk reduction', session_num),
        'goals_services_responses':
            GoalSettingResponse.objects.find_by_module(
                user, 'services', session_num),
    }


def session_3_context(user, session_num):
    return {
        'session_title': 'Protecting Myself. Protecting my community.',
        'supporters': Supporter.objects.filter(user=user),
        'goals_support_responses':
        GoalSettingResponse.objects.find_by_module(
            user, 'social support', session_num),
        'goals_risk_responses':
        GoalSettingResponse.objects.find_by_module(
            user, 'risk reduction', session_num),
        'goals_services_responses':
        GoalSettingResponse.objects.find_by_module(
            user, 'services', session_num),
        'i_am_worth_it_responses':
        get_quiz_responses_by_css_in_module(
            user, 'i-am-worth-it-quiz', session_num),
    }


def session_4_context(user, session_num):
    safety_plan_quiz_responses = get_quiz_responses_by_css_in_module(
        user, 'safety-plan-quiz', session_num)
    return {
        'session_title': 'Staying Safe and Strong',
        'goals_support_responses':
        GoalSettingResponse.objects.find_by_module(
            user, 'social support', session_num),
        'goals_risk_responses':
        GoalSettingResponse.objects.find_by_module(
            user, 'risk reduction', session_num),
        'goals_services_responses':
        GoalSettingResponse.objects.find_by_module(
            user, 'services', session_num),
        'i_am_worth_it_responses':
        get_quiz_responses_by_css_in_module(
            user, 'i-am-worth-it-quiz', session_num),
        'safety_plan_quiz_responses': safety_plan_quiz_responses,
    }


def session_5_context(user, session_num):
    return {
        'session_title': 'Because I am WORTH it!',
        'goals_risk_responses':
            GoalSettingResponse.objects.find_by_module(
                user, 'risk reduction', session_num),
        'i_am_worth_it_responses':
            get_quiz_responses_by_css_in_module(
                user, 'i-am-worth-it-quiz', session_num),
    }


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
            self.section, 'goals', 'goalsettingblock')
        self.goalcheckinblock = get_first_block_of_type(
            self.section, 'goals', 'goalcheckinpageblock')
        self.selftalkstatementblock = get_first_block_of_type(
            self.section, 'selftalk', 'statementblock')
        self.selftalkrefutationblock = get_first_block_of_type(
            self.section, 'selftalk', 'refutationblock')

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
            self.section, 'main', 'avatarselectorblock')
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
