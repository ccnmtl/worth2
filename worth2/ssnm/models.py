from django import forms
from django.db import models

from worth2.main.models import BasePageBlock, Participant


class Supporter(models.Model):
    participant = models.ForeignKey(Participant, related_name='supporters')
    name = models.TextField()

    closeness = models.CharField(
        max_length=2,
        choices=(
            ('VC', 'Very Close'),
            ('C', 'Close'),
            ('NC', 'Not Close'),
        ),
        default='VC'
    )

    influence = models.CharField(
        max_length=2,
        choices=(
            ('P', 'Positive'),
            ('MP', 'Mostly Positive'),
            ('MN', 'Mostly Negative'),
            ('N', 'Negative'),
        ),
        default='P'
    )

    provides_emotional_support = models.BooleanField(default=False)
    provides_practical_support = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.name)


class SsnmPageBlock(BasePageBlock):
    display_name = 'Social Support Network Map'
    template_file = 'ssnm/ssnm_page_block.html'
    js_template_file = 'ssnm/ssnm_js.html'
    css_template_file = 'ssnm/ssnm_css.html'

    @classmethod
    def add_form(cls):
        return SsnmPageBlockForm()

    def edit_form(self):
        return SsnmPageBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = SsnmPageBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = SsnmPageBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class SsnmPageBlockForm(forms.ModelForm):
    class Meta:
        model = SsnmPageBlock
