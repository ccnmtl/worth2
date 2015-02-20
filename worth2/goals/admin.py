from django.contrib import admin

from worth2.goals.models import GoalSettingBlock, GoalCheckInOption, GoalOption

admin.site.register(GoalSettingBlock)
admin.site.register(GoalCheckInOption)
admin.site.register(GoalOption)
