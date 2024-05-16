from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str
from ordered_model.models import OrderedModel
from pagetree.generic.models import BasePageBlock


class Avatar(OrderedModel):
    """An image that the user can choose for their profile."""

    image = models.ImageField()
    alt_text = models.TextField()

    is_default = models.BooleanField(
        default=False,
        help_text='If this is the initial avatar for all participants, ' +
        'set this option to True. There can only be one default avatar ' +
        'in the system.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return smart_str(self.image.url)

    def clean(self):
        if self.is_default:
            qs = Avatar.objects.filter(is_default=True)
            if qs.count() > 0 and self.pk != qs.first().pk:
                raise ValidationError(
                    '%s is already set as the default.' % qs.first())


class AvatarBlock(BasePageBlock):
    """A PageBlock for displaying the current participant's avatar."""

    display_name = 'Avatar Block'
    template_file = 'main/avatar_block.html'

    @classmethod
    def add_form(cls):
        return AvatarBlockForm()

    def edit_form(self):
        return AvatarBlockForm(instance=self)

    @classmethod
    def create(cls, request):
        form = AvatarBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = AvatarBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class AvatarBlockForm(forms.ModelForm):
    class Meta:
        model = AvatarBlock
        fields = '__all__'


class AvatarSelectorBlock(BasePageBlock):
    """A PageBlock for displaying the Avatar Selector."""

    display_name = 'Avatar Selector Block'
    template_file = 'main/avatar_selector_block.html'

    def needs_submit(self):
        return True

    def allow_redo(self):
        return True

    def unlocked(self, user):
        return user.profile2.avatar is not None

    def submit(self, user, request_data):
        avatar_id = request_data.get('avatar-id')
        avatar = get_object_or_404(Avatar, pk=avatar_id)
        user.profile2.avatar = avatar
        user.profile2.save()

    def clear_user_submissions(self, user):
        user.profile2.avatar = None
        user.profile2.save()

    def avatars(self):
        """Returns a queryset of all the available avatars in WORTH."""
        return Avatar.objects.all()

    @staticmethod
    def add_form():
        return AvatarSelectorBlockForm()

    def edit_form(self):
        return AvatarSelectorBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = AvatarSelectorBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create()

    def edit(self, vals, files):
        form = AvatarSelectorBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class AvatarSelectorBlockForm(forms.ModelForm):
    class Meta:
        model = AvatarSelectorBlock
        fields = '__all__'


class SimpleImageBlock(BasePageBlock):
    image = models.ImageField(upload_to="images")
    caption = models.TextField(blank=True)
    alt = models.CharField(max_length=100, null=True, blank=True)
    template_file = "main/simpleimageblock.html"
    display_name = "Simple Image Block"

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            caption = forms.CharField(initial=self.caption,
                                      widget=forms.widgets.Textarea())
            alt = forms.CharField(initial=self.alt)
        return EditForm()

    @classmethod
    def add_form(cls):
        class AddForm(forms.Form):
            image = forms.FileField(label="select image")
            caption = forms.CharField(widget=forms.widgets.Textarea())
            alt = forms.CharField()
        return AddForm()

    @classmethod
    def create(cls, request):
        if 'image' in request.FILES:
            ib = cls.objects.create(
                alt=request.POST.get('alt', ''),
                caption=request.POST.get('caption', ''),
                image="")
            ib.save_image(request.FILES['image'])
            return ib
        return None

    @classmethod
    def create_from_dict(cls, d):
        # since it's coming from a dict, not a request
        # we assume that some other part is handling the writing of
        # the image file to disk and we just get a path to it
        return cls.objects.create(
            image=d.get('image', ''),
            alt=d.get('alt', ''),
            caption=d.get('caption', ''))

    def as_dict(self):
        return dict(image=self.image.name,
                    alt=self.alt,
                    caption=self.caption)

    def edit(self, vals, files):
        self.caption = vals.get('caption', '')
        self.alt = vals.get('alt', '')
        if 'image' in files:
            self.save_image(files['image'])
        self.save()

    def save_image(self, f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg', 'jpeg', 'gif', 'png']:
            # unsupported image format
            return None
        full_filename = "%s/%s.%s" % (
            self.image.field.upload_to, basename, ext)
        fd = self.image.storage.open(
            settings.MEDIA_ROOT + "/" + full_filename, 'wb')

        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()


class VideoBlock(BasePageBlock):
    display_name = 'YouTube Video Block'
    template_file = 'main/video_block.html'
    js_template_file = 'main/video_block_js.html'

    video_id = models.CharField(
        max_length=255, null=True,
        help_text='The YouTube video id, e.g. "M7lc1UVf-VE"'
    )

    @staticmethod
    def add_form():
        return VideoBlockForm()

    def edit_form(self):
        return VideoBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = VideoBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = VideoBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class VideoBlockForm(forms.ModelForm):
    class Meta:
        model = VideoBlock
        fields = '__all__'


class WatchedVideo(models.Model):
    """This model records which users have viewed which videos."""

    class Meta:
        unique_together = ('user', 'video_id')

    user = models.ForeignKey(User, related_name='watched_videos',
                             on_delete=models.CASCADE)
    video_id = models.CharField(max_length=255, db_index=True,
                                help_text='The youtube video ID',
                                null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile2', on_delete=models.CASCADE)

    # Users can choose an avatar after their user is created.
    avatar = models.ForeignKey(Avatar, blank=True, null=True,
                               on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw, **kwargs):
    if not raw and created:
        UserProfile.objects.get_or_create(user=instance)
