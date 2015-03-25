import factory
from factory.fuzzy import FuzzyText

from worth2.goals.models import (
    GoalCheckInOption, GoalCheckInPageBlock, GoalCheckInResponse,
    GoalOption, GoalSettingBlock, GoalSettingResponse
)
from worth2.main.tests.factories import UserFactory


class GoalSettingBlockFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalSettingBlock

    goal_amount = 3


class GoalOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalOption

    text = FuzzyText()


class GoalSettingResponseFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalSettingResponse

    goal_setting_block = factory.SubFactory(GoalSettingBlockFactory)
    user = factory.SubFactory(UserFactory)
    option = factory.SubFactory(GoalOptionFactory)
    text = FuzzyText()


class GoalCheckInBlockFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalCheckInPageBlock

    goal_setting_block = factory.SubFactory(GoalSettingBlockFactory)


class GoalCheckInOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalCheckInOption

    text = FuzzyText()


class GoalCheckInResponseFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalCheckInResponse

    goal_setting_response = factory.SubFactory(GoalSettingResponseFactory)
    i_will_do_this = 'no'
    what_got_in_the_way = factory.SubFactory(GoalCheckInOptionFactory)
