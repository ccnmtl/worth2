from django import forms
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from pagetree.models import PageBlock


class BasePageBlock(models.Model):
    """An abstract pageblock to be used for custom pageblocks."""

    display_name = 'Unimplemented BasePageBlock'
    pageblocks = GenericRelation(PageBlock)

    def pageblock(self):
        return self.pageblocks.first()

    def needs_submit(self):
        return False

    @classmethod
    def add_form(cls):
        return BasePageBlockForm()

    def edit_form(self):
        return BasePageBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = BasePageBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create()

    def edit(self, vals, files):
        form = BasePageBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        return True

    class Meta:
        abstract = True


class BasePageBlockForm(forms.ModelForm):
    """Example ModelForm for the BasePageBlock.

    This is just an example. It should always be replaced with your
    own ModelForm pointing to the custom pageblock.
    """

    class Meta:
        model = BasePageBlock
