from django.contrib import admin
from models import VersionedComment

class VersionedCommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(VersionedComment, VersionedCommentAdmin)
