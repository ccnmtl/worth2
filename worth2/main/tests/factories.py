import factory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from factory.fuzzy import FuzzyText
from pagetree.tests.factories import HierarchyFactory, RootSectionFactory
from pagetree.models import UserPageVisit

from worth2.goals.models import (
    GoalCheckInPageBlock, GoalOption, GoalSettingBlock
)
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
    study_id = factory.Sequence(lambda n: '15040%03d1245' % n)


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

    likert_quizblock = {
        'show_submit_state': True,
        'css_extra': 'feelings-scale likert',
        'allow_redo': False,
        'description': '',
        'label': '',
        'questions': [
            {
                'css_extra': 'lead',
                'question_type': 'single choice',
                'text': 'How are you feeling right now?',
                'intro_text': '',
                'explanation': 'Thanks for checking in. ' +
                'You\'ll check in again later, too.',
                'answers': [
                    {
                        'explanation': '',
                        'css_extra': 'not-an-issue',
                        'correct': False,
                        'value': '0',
                        'label': 'Extremely Comfortable'
                    },
                    {
                        'explanation': '',
                        'css_extra': 'somewhat-an-issue',
                        'correct': False,
                        'value': '1',
                        'label': 'Comfortable'
                    },
                    {
                        'explanation': '',
                        'css_extra': 'an-issue',
                        'correct': False,
                        'value': '2',
                        'label': 'Somewhat Comfortable'
                    },
                    {
                        'explanation': '',
                        'css_extra': 'a-big-issue',
                        'correct': False,
                        'value': '3',
                        'label': 'Not at all comfortable'
                    }
                ]
            }
        ],
        'block_type': 'Quiz',
        'rhetorical': False
    }

    i_am_worth_it_quizblock = {
        'show_submit_state': False,
        'css_extra': 'i-am-worth-it-quiz quizblock-required',
        'allow_redo': False,
        'description': '',
        'label': '',
        'questions': [
            {
                'css_extra': '',
                'question_type': 'multiple choice',
                'text': 'I am: ',
                'intro_text': '',
                'explanation': '',
                'answers': [
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '1',
                        'label': 'Honest'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '2',
                        'label': 'Vulnerable'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '3',
                        'label': 'Shy'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '4',
                        'label': 'Outspoken'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '5',
                        'label': 'Priceless'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '6',
                        'label': 'Loyal'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '7',
                        'label': 'Loving'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '8',
                        'label': 'Caring'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '9',
                        'label': 'Supportive'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '10',
                        'label': 'A mentor'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '11',
                        'label': 'Beautiful'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '12',
                        'label': 'Sexy'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '13',
                        'label': 'A student'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '14',
                        'label': 'Funny'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '15',
                        'label': 'A good friend'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '16',
                        'label': 'A hard worker'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '17',
                        'label': 'Kind'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '18',
                        'label': 'Strong'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '19',
                        'label': 'Intelligent'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '20',
                        'label': 'One of a kind'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': 'Responsible',
                        'label': 'Responsible'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '22',
                        'label': 'Capable'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '23',
                        'label': 'Passionate'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '24',
                        'label': 'A good parent'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '25',
                        'label': 'A phenomenal woman'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '26',
                        'label': 'A good grandchild'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '27',
                        'label': 'A good grandparent'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '28',
                        'label': 'Compassionate'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '29',
                        'label': 'A good sister/daughter'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '30',
                        'label': 'Spiritual/Religious'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '31',
                        'label': 'A strong Black woman'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '32',
                        'label': 'A good neighbor'
                    },
                    {
                        'explanation': '',
                        'css_extra': '',
                        'correct': False,
                        'value': '33',
                        'label': 'A good niece/aunt/cousin'
                    }
                ]
            }
        ],
        'block_type': 'Quiz',
        'rhetorical': False
    }

    def __init__(self, hname='main', base_url='/pages/'):
        AvatarFactory()
        AvatarFactory()
        LocationFactory()
        GoalOption.objects.create(text='Goal Option 1')
        GoalOption.objects.create(text='Goal Option 2')
        GoalOption.objects.create(text='Goal Option 3')

        hierarchy = HierarchyFactory(name=hname, base_url=base_url)
        root = hierarchy.get_root()
        root.add_child_section_from_dict({
            'label': 'Welcome to Session 1',
            'slug': 'session-1',
            'children': [
                {
                    'label': 'Orientation Video',
                    'slug': 'orientation',
                    'pageblocks': [{
                        # Using text blocks instead of youtube video
                        # blocks here to get around video gating, and
                        # we're not testing that functionality with
                        # behave anyways.
                        'block_type': 'Text Block'
                    }]
                },
                {
                    'label': 'How to use this tablet',
                    'slug': 'how-to-use-this-tablet',
                    'pageblocks': [{
                        'block_type': 'Text Block'
                    }]
                },
                {
                    'label': 'Choose Your Avatar',
                    'slug': 'choose-your-avatar',
                    'pageblocks': [{
                        'block_type': 'Avatar Selector Block'
                    }]
                },
                {
                    'label': 'Introduction to "Feelings Scale"',
                    'slug': 'feelings-scale-intro',
                    'pageblocks': [{
                        'block_type': 'Text Block'
                    }]
                },
                {
                    'label': 'Feelings Scale',
                    'slug': 'feelings-scale',
                    'pageblocks': [
                        self.likert_quizblock
                    ]
                },
            ]
        })

        root.add_child_section_from_dict({
            'label': 'Welcome to Session 2',
            'slug': 'session-2',
            'children': [
                {
                    'label': 'Welcome to Session 2',
                    'slug': 'welcome-to-session-2',
                    'pageblocks': [{
                        'block_type': 'Text Block',
                    }],
                },
                {
                    'label': 'I am WORTH It!',
                    'slug': 'i-am-worth-it',
                    'pageblocks': [
                        self.i_am_worth_it_quizblock
                    ],
                },
                {
                    'label': 'Ground Rules',
                    'slug': 'ground-rules',
                    'pageblocks': [{
                        'block_type': 'Text Block',
                    }],
                },
                {
                    'label': 'Goal Setting Section',
                    'slug': 'goal-setting-section',
                    'pageblocks': [{
                        'block_type': 'Goal Setting Block',
                    }],
                },
                {
                    'label': 'Goal Check In Section',
                    'slug': 'goal-check-in-section',
                    'pageblocks': [{
                        'block_type': 'Goal Check In Block',
                    }],
                },
            ]
        })
        b = GoalCheckInPageBlock.objects.first()
        b.goal_setting_block = GoalSettingBlock.objects.first()
        b.save()
        assert(b.goal_setting_block is not None)

        root.add_child_section_from_dict({
            'label': 'Welcome to Session 3',
            'slug': 'session-3',
            'children': [
                {
                    'label': 'Welcome to Session 3',
                    'slug': 'welcome-to-session-3',
                    'pageblocks': [{
                        'block_type': 'Text Block',
                    }],
                },
                {
                    'label': 'Risk Reduction Goal Review',
                    'slug': 'risk-goal-review',
                    'pageblocks': [{
                        'block_type': 'Goal Check In Block',
                    }],
                },
            ],
        })
        b = GoalCheckInPageBlock.objects.all()[1]
        b.goal_setting_block = GoalSettingBlock.objects.first()
        b.save()
        assert(b.goal_setting_block is not None)

        root.add_child_section_from_dict({
            'label': 'Welcome to Session 4',
            'slug': 'session-4',
            'pageblocks': [{
                'label': 'Welcome to E-WORTH',
                'css_extra': '',
                'block_type': 'Test Block',
                'body': 'You should now use the edit link to add content'
            }]
        })

        root.add_child_section_from_dict({
            'label': 'Welcome to Session 5',
            'slug': 'session-5'
        })

        self.root = root
