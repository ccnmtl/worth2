from django import forms

from worth2.main.models import Location, Participant


class RawModelChoiceIterator(forms.models.ModelChoiceIterator):
    def choice(self, obj):
        return obj


class RawModelChoiceField(forms.ModelChoiceField):
    """
    A ModelChoiceField that returns the model instance instead of
    a single field.
    """

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices

        return RawModelChoiceIterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)


class SignInParticipantForm(forms.Form):
    participant_id = RawModelChoiceField(
        label='Participant ID #',
        empty_label=None,
        queryset=Participant.objects.filter(
            is_archived=False).order_by('study_id'),
        initial='Choose a Participant',
    )

    participant_location = forms.ModelChoiceField(
        label='Location',
        empty_label=None,
        queryset=Location.objects.order_by('name'))

    participant_destination = forms.ChoiceField(
        label='Take participant to:',
        widget=forms.RadioSelect,
        choices=(
            ('last_completed_activity', 'The last completed activity.'),
            ('next_new_session', 'The next, new session.'),
            ('already_completed_session',
             'An already completed session for review.')),
        initial='last_completed_activity',
    )

    already_completed_session = forms.ChoiceField(
        choices=(
            ('1', 'Session 1'),
            ('2', 'Session 2'),
            ('3', 'Session 3'),
            ('4', 'Session 4'),
            ('5', 'Session 5')),
        required=False)

    session_type = forms.ChoiceField(
        label='Session Type',
        widget=forms.RadioSelect,
        choices=(('regular', 'Regular'), ('makeup', 'Make-Up')),
    )
