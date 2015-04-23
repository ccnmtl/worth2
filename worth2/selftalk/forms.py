from django import forms
from django.conf import settings


class StatementForm(forms.Form):
    class Media:
        extend = False
        css = {
            'all': (settings.STATIC_URL +
                    'css/selftalk-internalstatementform.css',)
        }
        js = (settings.STATIC_URL +
              'js/src/forms/selftalk-internalstatementform.js',)

    def clean(self):
        cleaned_data = super(StatementForm, self).clean()
        if not any(cleaned_data.values()):
            raise forms.ValidationError(
                'Please select at least one negative statement.')


class RefutationForm(forms.Form):
    class Media:
        extend = False
        css = {
            'all': (settings.STATIC_URL + 'css/selftalk-refutationform.css',)
        }
        js = (settings.STATIC_URL +
              'js/src/forms/selftalk-refutationform.js',)
