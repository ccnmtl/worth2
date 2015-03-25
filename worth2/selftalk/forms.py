from django import forms


class InternalStatementForm(forms.Form):
    class Media:
        extend = False
        css = {
            'all': ('/media/css/selftalk-internalstatementform.css',)
        }
        js = ('/media/js/src/forms/selftalk-internalstatementform.js',)


class RefutationForm(forms.Form):
    class Media:
        extend = False
        css = {
            'all': ('/media/css/selftalk-refutationform.css',)
        }
        js = ('/media/js/src/forms/selftalk-refutationform.js',)
