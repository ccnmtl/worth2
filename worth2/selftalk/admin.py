from django.contrib import admin

from worth2.selftalk.models import (
    Statement, Refutation,
    StatementBlock
)


class RefutationInline(admin.StackedInline):
    model = Refutation


class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'refutations')
    inlines = [RefutationInline]

    def refutations(self, obj):
        return ', '.join([r.text for r in obj.refutation_set.all()])


admin.site.register(Statement, StatementAdmin)
admin.site.register(StatementBlock)
