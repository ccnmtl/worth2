from rest_framework import viewsets, permissions

from worth2.ssnm.auth import AnySessionAuthentication
from worth2.ssnm.serializers import SupporterSerializer


class SupporterViewSet(viewsets.ModelViewSet):
    serializer_class = SupporterSerializer
    authentication_classes = (AnySessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.supporters.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
