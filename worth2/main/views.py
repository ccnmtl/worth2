from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'


class ManageParticipantsView(TemplateView):
    template_name = 'main/facilitator_manage_participants.html'
