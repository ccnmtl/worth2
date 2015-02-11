from rest_framework import viewsets

from worth2.ssnm.auth import (
    InactiveUserSessionAuthentication, IsParticipantPermission
)
from worth2.ssnm.serializers import SupporterSerializer


class SupporterViewSet(viewsets.ModelViewSet):
    serializer_class = SupporterSerializer
    authentication_classes = (InactiveUserSessionAuthentication,)
    permission_classes = (IsParticipantPermission,)

    def get_queryset(self):
        return self.request.user.profile.participant.supporters.all()

    def perform_create(self, serializer):
        serializer.save(participant=self.request.user.profile.participant)
