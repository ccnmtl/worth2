from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_text

from pagetree.generic.models import BasePageBlock
from pagetree.reports import ReportColumnInterface, StandaloneReportColumn, \
    ReportableInterface


class Supporter(models.Model):
    CLOSENESS_CHOICES = (
        ('VC', 'Very Close'),
        ('C', 'Close'),
        ('NC', 'Not Close'),
    )

    INFLUENCE_CHOICES = (
        ('P', 'Positive'),
        ('MP', 'Mostly Positive'),
        ('MN', 'Mostly Negative'),
        ('N', 'Negative'),
    )

    user = models.ForeignKey(User, null=True, related_name='supporters',
                             on_delete=models.CASCADE)
    name = models.TextField()

    closeness = models.CharField(
        max_length=2,
        choices=CLOSENESS_CHOICES,
        default='VC'
    )

    influence = models.CharField(
        max_length=2,
        choices=INFLUENCE_CHOICES,
        default='P'
    )

    provides_emotional_support = models.BooleanField(default=False)
    provides_practical_support = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return smart_text(self.name)


class SsnmPageBlock(BasePageBlock):
    display_name = 'Social Support Network Map'
    template_file = 'ssnm/ssnm_page_block.html'
    js_template_file = 'ssnm/ssnm_js.html'
    css_template_file = 'ssnm/ssnm_css.html'

    @staticmethod
    def add_form():
        return SsnmPageBlockForm()

    def edit_form(self):
        return SsnmPageBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = SsnmPageBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = SsnmPageBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class SsnmPageBlockForm(forms.ModelForm):
    class Meta:
        model = SsnmPageBlock
        fields = '__all__'


class SupporterReportColumn(ReportColumnInterface):

    def __init__(self, idx, field, field_type, value=None, label=None):
        self.idx = idx
        self.field = field
        self.field_type = field_type
        self.answer_value = value or ''
        self.answer_label = label or ''

    def description(self):
        return "Supporter %s %s" % (self.idx + 1, self.field.capitalize())

    def identifier(self):
        return 'supporter_%s_%s' % (self.idx + 1, self.field)

    def metadata(self):
        return ['', self.identifier(), 'Social Support Network Map',
                self.field_type, self.description(), self.answer_value,
                self.answer_label]

    def user_value(self, user):
        supporters = Supporter.objects.filter(user=user)
        supporters = supporters.order_by('created_at', 'id')

        if supporters.count() <= self.idx:
            return ''

        supporter = supporters[self.idx]
        return getattr(supporter, self.field, '')


class SsnmReport(ReportableInterface):

    def standalone_columns(self):
        return [
            StandaloneReportColumn(
                'supporter_count', 'Social Support Network',
                'count', 'Supporter Count',
                lambda x: Supporter.objects.filter(user=x).count())]

    def report_metadata(self):
        cols = self.standalone_columns()
        for idx in range(0, 5):
            for choice in Supporter.CLOSENESS_CHOICES:
                cols.append(SupporterReportColumn(idx, 'closeness',
                                                  'single choice',
                                                  choice[0], choice[1]))
            for choice in Supporter.INFLUENCE_CHOICES:
                cols.append(SupporterReportColumn(idx, 'influence',
                                                  'single choice',
                                                  choice[0], choice[1]))

            cols.append(SupporterReportColumn(idx,
                                              'provides_emotional_support',
                                              'boolean'))
            cols.append(SupporterReportColumn(idx,
                                              'provides_practical_support',
                                              'boolean'))

        return cols

    def report_values(self):
        columns = self.standalone_columns()

        for idx in range(0, 5):
            columns.append(
                SupporterReportColumn(idx, 'closeness', 'single choice'))
            columns.append(
                SupporterReportColumn(idx, 'influence', 'single choice'))
            columns.append(
                SupporterReportColumn(idx, 'provides_emotional_support',
                                      'boolean'))
            columns.append(
                SupporterReportColumn(idx, 'provides_practical_support',
                                      'boolean'))

        return columns
