from rest_framework import viewsets

from worth2.main.models import Participant
from worth2.main.serializers import ParticipantSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
