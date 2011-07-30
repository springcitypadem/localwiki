from django.conf import settings
from django.contrib.comments.models import Comment
from django.core.urlresolvers import reverse
from django.utils.formats import localize
from versionutils.versioning import TrackChanges

class VersionedComment(Comment):
    history = TrackChanges()

    class Meta:
        verbose_name = 'comment'

    def __unicode__(self):
        return "%s on %s %s: %s%s" % (
            self.name, self.content_type, self.content_object,
            self.comment[:50], '...' if len(self.comment) > 50 else '',)

    def get_history_list(self):
        try:
            return u'<ul>%s</ul>' % (
                u'\n'.join(
                    u'<li>Version %i by %s from %s, %s, %s</li>' % (
                        r.history_info.version_number(),
                        r.history_info.user,
                        r.history_info.user_ip,
                        localize(r.history_info.date),
                        r.history_info.comment or 'no comment',
                        ) for r in self.history.all()
                    )
            )
        except Exception as err:
            return u'(not available)'
    get_history_list.short_description = 'History'
    get_history_list.allow_tags = True

    def get_admin_edit_link(self):
        return '<a href="%s">View admin page and history for comment</a>' % reverse('admin:comments_versionedcomment_change', args=(self.id,))
    get_admin_edit_link.short_description = 'Link'
    get_admin_edit_link.allow_tags = True

    def get_content_object_link(self):
        viewname = 'admin:%s_%s_change' % (self.content_type.app_label, self.content_type.model)
        return '<a href="%s">View admin page for %s %s</a>' % (reverse(viewname, args=(self.object_pk,)), self.content_type, self.content_object)
    get_content_object_link.short_description = 'Content admin'
    get_content_object_link.allow_tags = True
