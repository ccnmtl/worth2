from rest_framework import viewsets

from worth2.ssnm.auth import InactiveUserSessionAuthentication
from worth2.ssnm.models import Supporter
from worth2.ssnm.serializers import SupporterSerializer


class SupporterViewSet(viewsets.ModelViewSet):
    authentication_classes = (InactiveUserSessionAuthentication,)
    # TODO: filter for user
    queryset = Supporter.objects.all()
    serializer_class = SupporterSerializer
