from django import forms


class RefutationForm(forms.Form):
    class Media:
        extend = False
        css = {
            'all': ('/media/css/selftalk-refutationform.css',)
        }
        js = ('/media/js/src/forms/selftalk-refutationform.js',)
