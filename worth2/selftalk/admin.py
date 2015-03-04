from django.contrib import admin

from worth2.selftalk.models import (
    Statement, Refutation,
    StatementBlock, RefutationBlock
)


admin.site.register(Statement)
admin.site.register(Refutation)
admin.site.register(StatementBlock)
admin.site.register(RefutationBlock)
