from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from worth2.main.auth import generate_random_username, generate_password
from worth2.main.models import Participant


class IndexView(TemplateView):
    template_name = 'main/index.html'


class ParticipantCreate(CreateView):
    model = Participant
    fields = ['study_id']

    def form_valid(self, form):
        # Study ID was valid, so create an inactive django user for this
        # participant.
        username = generate_random_username()
        password = generate_password(username)
        participant_user = User(username=username, is_active=False)
        participant_user.set_password(password)
        participant_user.save()

        form.instance.user = participant_user
        form.instance.created_by = self.request.user
        return super(ParticipantCreate, self).form_valid(form)


class ParticipantUpdate(UpdateView):
    model = Participant
    fields = ['study_id']

    def form_valid(self, form):
        if 'is_archived' in self.request.POST and \
           self.request.POST['is_archived'] == 'true':
            form.instance.is_archived = True

        return super(ParticipantUpdate, self).form_valid(form)


class ManageParticipants(ListView):
    model = Participant

    def get_context_data(self, **kwargs):
        ctx = super(ManageParticipants, self).get_context_data(**kwargs)
        ctx['active_participants'] = [p for p in ctx['object_list']
                                      if not p.is_archived]
        ctx['archived_participants'] = [p for p in ctx['object_list']
                                        if p.is_archived]
        return ctx


class SignInParticipant(TemplateView):
    template_name = 'main/facilitator_sign_in_participant.html'
