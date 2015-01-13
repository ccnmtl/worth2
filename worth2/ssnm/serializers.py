from rest_framework import serializers

from worth2.ssnm.models import Supporter


class SupporterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supporter
        fields = ('pk', 'participant', 'name', 'closeness', 'influence',
                  'provides_emotional_support', 'provides_practical_support')
