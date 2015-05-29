from django import forms
from django.forms.formsets import formset_factory
from worth2.goals.models import GoalCheckInOption, GoalCheckInPageBlock


class GoalCheckInForm(forms.Form):
    goal_setting_response_id = forms.IntegerField(widget=forms.HiddenInput())

    i_will_do_this = forms.ChoiceField(
        label='How did it go?',
        choices=GoalCheckInPageBlock.PROGRESS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'how-it-went'}),
    )

    what_got_in_the_way = forms.ModelChoiceField(
        label='What got in the way?',
        queryset=GoalCheckInOption.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'what-got-in-the-way'}),
    )

    other = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'goal-checkin-other',
                   'placeholder': 'Please type your response here'}),
    )

    def clean(self):
        cleaned_data = super(GoalCheckInForm, self).clean()
        how_it_went = cleaned_data.get('i_will_do_this')
        what_got_in_the_way = cleaned_data.get('what_got_in_the_way')
        other = cleaned_data.get('other')

        if how_it_went != 'yes':
            if not what_got_in_the_way:
                self.add_error('what_got_in_the_way',
                               u'This field is required.')

        if hasattr(what_got_in_the_way, 'text') and (
                what_got_in_the_way.text.lower() == 'other'):
            if not other:
                self.add_error('other', u'This field is required.')


GoalCheckInFormSet = formset_factory(GoalCheckInForm, min_num=1)


class GoalSettingForm(forms.Form):
    other_text = forms.CharField(
        label='Other',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'other-text',
                   'placeholder': 'Please type your response here'}),
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='How will you make this happen?',
        required=False,
    )

    def clean(self):
        cleaned_data = super(GoalSettingForm, self).clean()
        option = cleaned_data.get('option')
        other_text = cleaned_data.get('other_text')
        text = cleaned_data.get('text')

        if hasattr(option, 'text') and option.text.lower() == 'n/a':
            pass
        elif not text:
            self.add_error('text', u'This field is required.')

        if hasattr(option, 'text') and option.text.lower() == 'other':
            if not other_text:
                # 'Other' text is required if 'Other' is selected from
                # the dropdown.
                self.add_error('other_text', u'This field is required.')
