import factory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from factory.fuzzy import FuzzyText
from pagetree.tests.factories import HierarchyFactory, RootSectionFactory
from pagetree.models import UserPageVisit

from worth2.main.auth import generate_password
from worth2.main.models import (
    Avatar, Encounter, Location, Participant, VideoBlock, WatchedVideo
)


class InactiveUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText()
    password = factory.LazyAttribute(lambda u: generate_password(u.username))
    is_active = False


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText()
    password = factory.PostGenerationMethodCall('set_password', 'test')


class AvatarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Avatar

    image = SimpleUploadedFile('test.png', '')


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = FuzzyText()


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participant

    created_by = factory.SubFactory(UserFactory)
    is_archived = False
    user = factory.SubFactory(InactiveUserFactory)
    first_location = factory.SubFactory(LocationFactory)
    location = factory.SubFactory(LocationFactory)
    study_id = FuzzyText(prefix='15040',
                         suffix='1245',
                         length=3,
                         chars='1234567890')


class EncounterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Encounter

    facilitator = factory.SubFactory(UserFactory)
    participant = factory.SubFactory(ParticipantFactory)
    location = factory.SubFactory(LocationFactory)
    section = factory.SubFactory(RootSectionFactory)


class VideoBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoBlock

    video_id = FuzzyText()


class WatchedVideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WatchedVideo

    user = factory.SubFactory(UserFactory)
    video_id = FuzzyText()


# TODO: Move this to django-pagetree
class UserPageVisitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserPageVisit

    user = factory.SubFactory(UserFactory)
    section = factory.SubFactory(RootSectionFactory)


class WorthModuleFactory(object):
    """A customized version of Pagetree's ModuleFactory."""

    def __init__(self, hname='main', base_url='/pages/'):
        hierarchy = HierarchyFactory(name=hname, base_url=base_url)
        root = hierarchy.get_root()
        root.add_child_section_from_dict({
            'label': 'Welcome to Session 1',
            'slug': 'session-1',
            'children': [
                {'label': 'Orientation Video',
                 'slug': 'orientation'}
            ]})
        root.add_child_section_from_dict({
            'label': 'Welcome to Session 2',
            'slug': 'session-2'
        })
        root.add_child_section_from_dict({
            'label': 'Welcome to Session 3',
            'slug': 'session-3'
        })

        blocks = [{
            'label': 'Welcome to E-WORTH',
            'css_extra': '',
            'block_type': 'Test Block',
            'body': 'You should now use the edit link to add content'
        }]
        root.add_child_section_from_dict({
            'label': 'Welcome to Session 4',
            'slug': 'session-4',
            'pageblocks': blocks
        })

        root.add_child_section_from_dict({
            'label': 'Welcome to Session 5',
            'slug': 'session-5'
        })

        self.root = root
