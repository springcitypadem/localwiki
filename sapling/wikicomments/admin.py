from django.contrib import admin
from django.contrib.contenttypes import generic
from django.db import models
from models import WikiComment

class WikiCommentAdmin(admin.ModelAdmin):
    readonly_fields = ('submit_date', 'ip_address', 'get_content_object_link',
                       'get_history_list',)
    fieldsets = (
        (None, {
            'fields': (('user', 'ip_address', 'site', 'submit_date',),
                       'get_content_object_link',
                       'comment', ('is_public', 'is_removed',),
                       'get_history_list',
                      ),
        }),
    )

class WikiCommentInline(generic.GenericStackedInline):
    model = WikiComment
    ordering = ('-submit_date',)
    can_delete = False
    ct_fk_field = 'object_pk'

    verbose_name = 'Comment'

    readonly_fields = ('submit_date', 'ip_address', 'get_history_list',
                       'get_admin_edit_link',)
    fieldsets = (
        (None, {
            'fields': ('get_admin_edit_link', 'get_history_list',)
        }),
        ('Comment information', {
            'classes': ('collapse',),
            'fields': (('user', 'ip_address', 'site', 'submit_date',),
                       'comment', ('is_public', 'is_removed',),),
        }),
    )

    extra = 0
    max_num = 0

try:
    admin.site.register(WikiComment, WikiCommentAdmin)
except admin.sites.AlreadyRegistered:
    pass
