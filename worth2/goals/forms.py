from django import forms
from django.forms.formsets import formset_factory

from worth2.goals.models import GoalCheckInOption


class GoalCheckInForm(forms.Form):
    i_will_do_this = forms.ChoiceField(
        label='I will do this.',
        choices=(
            ('yes', 'Yes'),
            ('no', 'No'),
            ('in progress', 'In Progress'),
        ),
        widget=forms.RadioSelect,
    )

    what_got_in_the_way = forms.ModelChoiceField(
        label='What got in the way?',
        queryset=GoalCheckInOption.objects.all(),
    )

    other = forms.CharField()


GoalCheckInFormSet = formset_factory(GoalCheckInForm, min_num=1)
