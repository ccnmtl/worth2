from rest_framework import viewsets, permissions

from worth2.main.auth import AnySessionAuthentication
from worth2.main.models import Participant
from worth2.main.serializers import (
    ParticipantSerializer, WatchedVideoSerializer
)


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class WatchedVideoViewSet(viewsets.ModelViewSet):
    serializer_class = WatchedVideoSerializer
    authentication_classes = (AnySessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.watched_videos.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
