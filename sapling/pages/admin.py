from django.contrib import admin
from models import Page

from sapling.comments.admin import VersionedCommentInline

class PageAdmin(admin.ModelAdmin):
    inlines = [
        VersionedCommentInline,
    ]

admin.site.register(Page, PageAdmin)
