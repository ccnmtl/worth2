from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from pagetree.models import Hierarchy, Section

from worth2.main.models import Avatar, Location, Participant

admin.site.register(Hierarchy)
admin.site.register(Section)
admin.site.register(Location)
admin.site.register(Participant)


class AvatarAdmin(OrderedModelAdmin):
    list_display = ('image', 'move_up_down_links')


admin.site.register(Avatar, AvatarAdmin)
