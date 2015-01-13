from django.views.generic.base import TemplateView


class SSNM(TemplateView):
    """Social Support Network Map activity"""
    template_name = 'ssnm/ssnm.html'
