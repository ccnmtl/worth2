from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from worth2.goals.models import GoalSettingBlock, GoalCheckInOption, GoalOption


admin.site.register(GoalCheckInOption)


class GoalOptionAdmin(OrderedModelAdmin):
    list_display = ('text', 'move_up_down_links')
    model = GoalOption


class GoalOptionInline(admin.TabularInline):
    model = GoalOption


class GoalSettingBlockAdmin(admin.ModelAdmin):
    inlines = [GoalOptionInline]


admin.site.register(GoalOption, GoalOptionAdmin)
admin.site.register(GoalSettingBlock, GoalSettingBlockAdmin)
