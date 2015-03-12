from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from worth2.goals.models import GoalCheckInOption, GoalOption


class GoalCheckInOptionAdmin(OrderedModelAdmin):
    list_display = ('text', 'move_up_down_links')
    model = GoalCheckInOption


class GoalOptionAdmin(OrderedModelAdmin):
    list_display = ('text', 'goal_type', 'move_up_down_links')
    model = GoalOption


admin.site.register(GoalCheckInOption, GoalCheckInOptionAdmin)
admin.site.register(GoalOption, GoalOptionAdmin)
