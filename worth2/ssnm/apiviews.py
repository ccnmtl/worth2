from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_json_api import parsers, renderers

from worth2.ssnm.serializers import SupporterSerializer


class SupporterViewSet(viewsets.ModelViewSet):
    serializer_class = SupporterSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    resource_name = 'supporters'

    def get_queryset(self):
        return self.request.user.supporters.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
