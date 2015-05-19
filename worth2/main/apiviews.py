from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from worth2.main.auth import AnySessionAuthentication
from worth2.main.models import Participant
from worth2.main.serializers import (
    ParticipantSerializer, WatchedVideoSerializer
)


class LoginCheck(APIView):
    """View to check if a facilitator's password if valid."""

    authentication_classes = (AnySessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        """
        Params:
          facilitator_username
          facilitator_password

        On successful check, the current user gets logged out and the
        facilitator gets logged in.
        """

        username = request.data.get('facilitator_username')
        password = request.data.get('facilitator_password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User "%s" not found' % username},
                            status=404)

        login_check = user.check_password(password)
        status = 400

        if login_check:
            status = 200
            user = authenticate(username=username, password=password)
            login(request, user)

        return Response({'login_check': login_check}, status=status)


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
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            # TODO: is there something we can raise here
            # to get DRF to return a 304 in this case?
            pass
