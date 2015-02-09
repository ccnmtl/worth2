from django.contrib import admin
from pagetree.models import Hierarchy, Section

from worth2.main.models import Avatar, Location, Participant

admin.site.register(Avatar)
admin.site.register(Hierarchy)
admin.site.register(Section)
admin.site.register(Location)
admin.site.register(Participant)
