from django import forms

from worth2.main.models import Location, Participant


class SignInParticipantForm(forms.Form):
    participant_id = forms.ModelChoiceField(
        label='Participant ID #',
        empty_label=None,
        queryset=Participant.objects.filter(
            is_archived=False).order_by('study_id'),
    )

    participant_location = forms.ModelChoiceField(
        label='Location',
        empty_label='Choose a Location',
        queryset=Location.objects.order_by('name'),
    )

    participant_destination = forms.ChoiceField(
        label='Take participant to:',
        widget=forms.RadioSelect,
        choices=(
            ('last_completed_activity', 'The last completed activity.'),
            ('next_new_session', 'The next, new session.'),
            ('already_completed_session',
             'An already completed session for review.')),
        initial='next_new_session',
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
