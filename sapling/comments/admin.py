from django.contrib import admin
from django.contrib.contenttypes import generic
from models import VersionedComment

class VersionedCommentHistoryInline(admin.StackedInline):
    model = VersionedComment.history.model
    ordering = ('-history_date',)
    can_delete = False

    verbose_name = 'Comment history'
    verbose_name_plural = 'Comment histories'

    readonly_fields = model._meta.get_all_field_names()

    fieldsets = (
        (None, {
            'fields': (
                       ('history_user', 'history_user_ip', 'history_date',),
                       ('history_type', 'history_comment',),
                      ),
        }),
        ('Content', {
            'classes': ('collapse',),
            'fields': ('history_reverted_to_version', 'comment',),
        }),
    )
    extra = 0
    max_num = 0

class VersionedCommentAdmin(admin.ModelAdmin):
    inlines = [VersionedCommentHistoryInline]

    readonly_fields = ('submit_date', 'ip_address', 'get_content_object_link',)
    fieldsets = (
        (None, {
            'fields': (('user', 'ip_address', 'site', 'submit_date',),
                       'get_content_object_link',
                       'comment', ('is_public', 'is_removed',),),
        }),
    )

class VersionedCommentInline(generic.GenericStackedInline):
    model = VersionedComment
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
    admin.site.register(VersionedComment, VersionedCommentAdmin)
except admin.sites.AlreadyRegistered:
    pass
