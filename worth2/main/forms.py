from django import forms

from worth2.main.models import Location, Participant


class SignInParticipantForm(forms.Form):
    # See full definition for this field in self.__init__()
    filter_by_cohort = forms.ChoiceField()

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
            (1, 'Session 1'),
            (2, 'Session 2'),
            (3, 'Session 3'),
            (4, 'Session 4'),
            (5, 'Session 5'),
        )
    )

    session_type = forms.ChoiceField(
        label='Session Type',
        widget=forms.RadioSelect,
        choices=(('regular', 'Regular'), ('makeup', 'Make-Up')),
    )

    def __init__(self, *args, **kwargs):
        super(SignInParticipantForm, self).__init__(*args, **kwargs)

        # This field's choices are re-generated each time the form is
        # initialized. That's because it needs to change if the
        # participants' cohort IDs are updated.
        cohort_choices = [
            ('all', 'All Cohorts'),
            (None, 'Unassigned')
        ] + map(lambda x: (x, x), Participant.objects.cohort_ids())
        self.fields['filter_by_cohort'] = forms.ChoiceField(
            label='Filter by Cohort',
            initial='all',
            required=False,
            choices=cohort_choices,
        )
