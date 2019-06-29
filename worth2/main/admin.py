from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from pagetree.models import Hierarchy, Section

from worth2.main.models import Avatar

admin.site.register(Hierarchy)
admin.site.register(Section)


class AvatarAdmin(OrderedModelAdmin):
    list_display = ('id', 'image', 'is_default', 'move_up_down_links')


admin.site.register(Avatar, AvatarAdmin)
