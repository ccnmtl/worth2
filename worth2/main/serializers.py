from rest_framework import serializers

from worth2.main.models import WatchedVideo


class WatchedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedVideo
        fields = ('video_id',)
