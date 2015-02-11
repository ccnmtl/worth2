from django import forms

from worth2.main.models import Location, Participant


class SignInParticipantForm(forms.Form):
    participant_id = forms.ModelChoiceField(
        label='Participant ID #',
        empty_label=None,
        queryset=Participant.objects.filter(is_archived=False),)

    participant_location = forms.ModelChoiceField(
        label='Location',
        empty_label=None,
        queryset=Location.objects.all(),)

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

    already_completed_session = forms.ChoiceField(required=False)

    session_type = forms.ChoiceField(
        label='Session Type',
        widget=forms.RadioSelect,
        choices=(('regular', 'Regular'), ('makeup', 'Make-Up')),
    )
