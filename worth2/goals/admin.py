from django.contrib import admin

from worth2.goals.models import GoalSettingBlock, GoalSlot, GoalSlotOption

admin.site.register(GoalSettingBlock)
admin.site.register(GoalSlot)
admin.site.register(GoalSlotOption)
