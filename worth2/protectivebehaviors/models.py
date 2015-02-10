from django import forms
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from pagetree.models import PageBlock
from quizblock.models import Quiz


class ProtectiveBehaviorsResults(models.Model):
    pageblocks = GenericRelation(
        PageBlock,
        related_query_name='protective_behaviors_results')
    quiz_class = models.CharField(max_length=255, help_text='Required')
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


class RateMyRiskQuiz(Quiz):
    quiz_class = models.CharField(max_length=255, help_text='Required')
    display_name = 'Rate My Risk Quiz'
    template_file = 'protectivebehaviors/quizblock.html'

    @classmethod
    def create(cls, request):
        return cls.objects.create(
            description=request.POST.get('description', ''),
            rhetorical=request.POST.get('rhetorical', ''),
            allow_redo=request.POST.get('allow_redo', ''),
            show_submit_state=request.POST.get('show_submit_state', False))

    @classmethod
    def create_from_dict(cls, d):
        q = cls.objects.create(
            description=d.get('description', ''),
            rhetorical=d.get('rhetorical', False),
            allow_redo=d.get('allow_redo', True),
            show_submit_state=d.get('show_submit_state', True)
        )
        q.import_from_dict(d)
        return q
