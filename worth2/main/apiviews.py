from django.db import IntegrityError
from rest_framework import viewsets, permissions

from worth2.main.auth import AnySessionAuthentication
from worth2.main.serializers import WatchedVideoSerializer


class WatchedVideoViewSet(viewsets.ModelViewSet):
    serializer_class = WatchedVideoSerializer
    authentication_classes = (AnySessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.watched_videos.all()

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            # TODO: is there something we can raise here
            # to get DRF to return a 304 in this case?
            pass
