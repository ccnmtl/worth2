from django import forms, http
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import redirect, render

from pagetree.generic.views import PageView
from pagetree.models import PageBlock
import quizblock
from quizblock.models import Quiz

from worth2.goals.models import GoalOption, GoalSettingResponse
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
        return ctx


class SignInParticipant(FormView):
    template_name = 'main/facilitator_sign_in_participant.html'
    form_class = SignInParticipantForm

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


class ParticipantSessionPageView(PageView):
    """WORTH version of pagetree's PageView"""

    gated = True

    def _create_goal_setting_formset(self, **kwargs):
        """Create the goal setting formset.

        To be used by GET and POST.
        """

        path = kwargs['path']
        self.section = self.get_section(path)
        goalsettingblock = self._get_goal_setting_block()
        if goalsettingblock:
            # I'd like to be define the GoalSettingForm instead in
            # goals/forms.py, but the goal field depends on data I can
            # only get here.
            class GoalSettingForm(forms.Form):
                goal = forms.ModelChoiceField(
                    label='Main services goal',
                    queryset=GoalOption.objects.filter(
                        goal_setting_block=goalsettingblock.block()),
                )
                text = forms.CharField(
                    widget=forms.Textarea(attrs={'rows': 3}),
                    label='How will you make this happen?',
                )

            self.GoalSettingFormSet = formset_factory(
                GoalSettingForm,
                extra=goalsettingblock.block().goal_amount - 1,
                # min_num is 1 because there's always a 'Main' goal form.
                min_num=1,
                validate_min=True,
            )
            self.formset = self.GoalSettingFormSet(
                prefix='pageblock-%s' % goalsettingblock.pk,
            )

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self._create_goal_setting_formset(**kwargs)
        return super(ParticipantSessionPageView, self).dispatch(
            request, *args, **kwargs)

    def _get_goal_setting_block(self):
        """Get the first goal setting block on this page.

        Returns the goal setting block if this page contains it.
        Otherwise, returns None.
        """

        pageblocks = self.section.pageblock_set.all()
        goalsettingtype = ContentType.objects.get(name='goal setting block')
        goalsettingblocks = pageblocks.filter(content_type=goalsettingtype)
        if goalsettingblocks.count() > 0:
            return goalsettingblocks.first()
        else:
            return None

    def get_extra_context(self):
        ctx = super(ParticipantSessionPageView, self).get_extra_context()

        goalsettingblock = self._get_goal_setting_block()
        if goalsettingblock:
            ctx.update({'formset': self.formset})

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

    def _handle_goal_submission(self, request, goalsettingblock):
        """Handle a submission for the goal setting activity.

        This method returns the formset populated formset.
        """

        block = goalsettingblock.block()
        formset = self.GoalSettingFormSet(
            request.POST,
            prefix='pageblock-%s' % goalsettingblock.pk)

        if formset.is_valid():
            for formdata in formset.cleaned_data:
                goaloption = formdata.get('goal')
                text = formdata.get('text')

                GoalSettingResponse.objects.create(
                    user=request.user,
                    goal_setting_block=block,
                    option=goaloption,
                    text=text)

        return formset

    def post(self, request, *args, **kwargs):
        goalsettingblock = self._get_goal_setting_block()

        if goalsettingblock:
            formset = self._handle_goal_submission(request, goalsettingblock)
            if not formset.is_valid():
                ctx = self.get_context_data()
                ctx.update({'formset': formset})
                return render(request, self.template_name, ctx)

        return super(ParticipantSessionPageView, self).post(
            request, *args, **kwargs)
