from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from worth2.main.models import Participant


class IndexView(TemplateView):
    template_name = 'main/index.html'


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
