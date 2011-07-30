from django.contrib import admin
from models import Page

from wikicomments.admin import WikiCommentInline

class PageAdmin(admin.ModelAdmin):
    inlines = [
        WikiCommentInline,
    ]

admin.site.register(Page, PageAdmin)
