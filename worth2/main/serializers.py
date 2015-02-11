from django.contrib.auth.models import User
from rest_framework import serializers

from worth2.main.auth import generate_random_username, generate_password
from worth2.main.models import Participant


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = ('pk', 'is_archived', 'study_id', 'cohort_id',)

    def create(self, validated_data):
        # Create an inactive User for the participant
        username = generate_random_username()
        password = generate_password(username)
        participant_user = User.objects.create(
            username=username, is_active=False)
        participant_user.set_password(password)
        participant_user.save()
        validated_data['user'] = participant_user
        validated_data['created_by'] = self.context['request'].user

        return Participant.objects.create(**validated_data)
