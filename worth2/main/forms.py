from django import forms


class SignInParticipantForm(forms.Form):
    participant_id = forms.ChoiceField()
    location = forms.ChoiceField()
    participant_destination = forms.RadioSelect()

    def sign_in(self):
        pass
