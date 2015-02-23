from django import forms
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from pagetree.models import PageBlock


class ProtectiveBehaviorsResults(models.Model):
    pageblocks = GenericRelation(PageBlock)
    quiz_class = models.CharField(max_length=255, help_text='Required',
                                  default='protective-behaviors')
    display_name = 'Protective Behaviors Results'
    template_file = 'protectivebehaviors/protective_behaviors_results.html'

    def pageblock(self):
        return self.pageblocks.first()

    def __unicode__(self):
        return "%s -- %s" % (unicode(self.pageblock()), self.quiz_category)

    @classmethod
    def add_form(self):
        return ProtectiveBehaviorsResultsForm()

    def edit_form(self):
        return ProtectiveBehaviorsResultsForm(instance=self)

    @classmethod
    def create(self, request):
        form = ProtectiveBehaviorsResultsForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = ProtectiveBehaviorsResultsForm(
            data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def needs_submit(self):
        return False

    def unlocked(self, user):
        return True


class ProtectiveBehaviorsResultsForm(forms.ModelForm):
    class Meta:
        model = ProtectiveBehaviorsResults
