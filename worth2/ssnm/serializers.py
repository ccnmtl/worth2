from rest_framework_json_api import serializers

from worth2.ssnm.models import Supporter


class SupporterSerializer(serializers.ModelSerializer):
    influence_display = serializers.SerializerMethodField()

    class Meta:
        model = Supporter
        fields = (
            # ember-data expects id, not pk. Fortunately in Django these
            # terms are interchangeable.
            'id',
            'name',
            'closeness',
            'influence',
            'influence_display',
            'provides_emotional_support',
            'provides_practical_support'
        )

    # Because 'influence' is a Django CharField with 'choices' defined,
    # the get_influence_display() method gets the values of the keys.
    def get_influence_display(self, obj):
        return obj.get_influence_display()
