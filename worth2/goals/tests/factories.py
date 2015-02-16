import factory
from factory.fuzzy import FuzzyText

from worth2.goals.models import (
    GoalCheckInOption, GoalOption, GoalSettingBlock
)


class GoalSettingBlockFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalSettingBlock

    session = 1
    goal_amount = 3


class GoalOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalOption

    goal_setting_block = factory.SubFactory(GoalSettingBlockFactory)
    text = FuzzyText()


class GoalCheckInFactory(factory.DjangoModelFactory):
    class Meta:
        model = GoalCheckInOption

    text = FuzzyText()
