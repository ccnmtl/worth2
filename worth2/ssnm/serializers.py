from rest_framework import serializers

from worth2.ssnm.models import Supporter


class SupporterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supporter
        fields = (
            # ember-data expects id, not pk. Fortunately in Django these
            # terms are interchangeable.
            'id',
            'participant',
            'name',
            'closeness',
            'influence',
            'get_influence_display',
            'provides_emotional_support',
            'provides_practical_support'
        )
