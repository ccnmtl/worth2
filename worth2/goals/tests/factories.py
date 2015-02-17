import factory
from factory.fuzzy import FuzzyText

from worth2.goals.models import (
    GoalCheckInOption, GoalCheckInPageBlock, GoalOption, GoalSettingBlock,
    GoalSettingResponse
)
from worth2.main.tests.factories import UserFactory


class GoalSettingBlockFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalSettingBlock

    session_num = 1
    goal_amount = 3


class GoalOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalOption

    goal_setting_block = factory.SubFactory(GoalSettingBlockFactory)
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

    session_num = 1


class GoalCheckInOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalCheckInOption

    text = FuzzyText()
