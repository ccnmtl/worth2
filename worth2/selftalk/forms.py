from django import forms
from django.conf import settings


class InternalStatementForm(forms.Form):
    class Media:
        extend = False
        css = {
            'all': (settings.STATIC_URL +
                    '/css/selftalk-internalstatementform.css',)
        }
        js = (settings.STATIC_URL +
              '/js/src/forms/selftalk-internalstatementform.js',)


class RefutationForm(forms.Form):
    class Media:
        extend = False
        css = {
            'all': (settings.STATIC_URL + '/css/selftalk-refutationform.css',)
        }
        js = (settings.STATIC_URL +
              '/js/src/forms/selftalk-refutationform.js',)
