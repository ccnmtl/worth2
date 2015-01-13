from django.db import models

from worth2.main.models import Participant


class Supporter(models.Model):
    participant = models.ForeignKey(Participant)
    name = models.TextField()

    closeness = models.CharField(
        max_length=2,
        choices=(
            ('VC', 'Very Close'),
            ('C', 'Close'),
            ('NC', 'Not Close'),
        ),
        default='VC'
    )

    influence = models.CharField(
        max_length=2,
        choices=(
            ('P', 'Positive'),
            ('MP', 'Mostly Positive'),
            ('MN', 'Mostly Negative'),
            ('N', 'Negative'),
        ),
        default='P'
    )

    provides_emotional_support = models.BooleanField(default=False)
    provides_practical_support = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
