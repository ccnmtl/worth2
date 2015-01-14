from rest_framework import viewsets

from worth2.ssnm.auth import (
    InactiveUserSessionAuthentication, ParticipantPermission
)
from worth2.ssnm.serializers import SupporterSerializer


class SupporterViewSet(viewsets.ModelViewSet):
    serializer_class = SupporterSerializer
    authentication_classes = (InactiveUserSessionAuthentication,)
    permission_classes = (ParticipantPermission,)

    def get_queryset(self):
        return self.request.user.profile.participant.supporters.all()
