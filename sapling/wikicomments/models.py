from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _

from versionutils.versioning import TrackChanges

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class CommentManager(models.Manager):
    def in_moderation(self):
        """
        QuerySet for all comments currently in the moderation queue.
        """
        return self.get_query_set().filter(is_public=False, is_removed=False)

    def for_model(self, model):
        """
        QuerySet for all comments for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_query_set().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()))
        return qs

class WikiComment(models.Model):
    """
    A comment about an object, with version tracking.

    Note: This is based on django.contrib.comments.models.Comment and
    BaseCommentAbstractModel.  For various reasons, just inheriting
    BaseCommentAbstractModel tweaks out versionutils.
    """
    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            )
    object_pk      = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type",
                                               fk_field="object_pk")

    # User-provided comment content
    comment     = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)

    # Metadata about the comment
    site        = models.ForeignKey(Site)
    user        = models.ForeignKey(User, blank=True, null=True,
                                    related_name='+')
    submit_date = models.DateTimeField(_('date/time submitted'),
                                       auto_now_add=True)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public   = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the comment ' \
                                'effectively disappear from the site.'))
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is ' \
                                'inappropriate. A "This comment has been ' \
                                'removed" message will be displayed instead.'))

    objects = CommentManager()
    history = TrackChanges()

    class Meta:
        ordering = ('submit_date',)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = _('wiki comment')
        verbose_name_plural = _('wiki comments')

    def __unicode__(self):
        return "%s on %s %s: %s%s" % (
            self.name, self.content_type, self.content_object,
            self.comment[:50], '...' if len(self.comment) > 50 else '',)

    def get_history_list(self):
        try:
            return u'<ul>%s</ul>' % (
                u'\n'.join(
                    u'<li>%s by %s from %s, %s, %s</li>' % (
                        r.history_type_verbose(),
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
        return '<a href="%s">View admin page and history for comment</a>' % reverse('admin:wikicomments_wikicomment_change', args=(self.id,))
    get_admin_edit_link.short_description = 'Link'
    get_admin_edit_link.allow_tags = True

    def get_content_object_link(self):
        viewname = 'admin:%s_%s_change' % (self.content_type.app_label, self.content_type.model)
        return '<a href="%s">View admin page for %s %s</a>' % (reverse(viewname, args=(self.object_pk,)), self.content_type, self.content_object)
    get_content_object_link.short_description = 'Content admin'
    get_content_object_link.allow_tags = True

    def _get_userinfo(self):
        """
        Get a dictionary that pulls together information about the poster
        safely for both authenticated and non-authenticated comments.

        This dict will have ``name`` and ``email`` fields.
        """
        if not hasattr(self, "_userinfo"):
            self._userinfo = {
                "name"  : 'unknown',
                "email" : None,
            }
            if self.user:
                u = self.user
                if u.email:
                    self._userinfo["email"] = u.email

                # If the user has a full name, use that for the user name.
                if u.get_full_name():
                    self._userinfo["name"] = self.user.get_full_name()
                else:
                    self._userinfo["name"] = u.username
        return self._userinfo
    userinfo = property(_get_userinfo, doc=_get_userinfo.__doc__)

    def _get_name(self):
        return self.userinfo["name"]
    name = property(_get_name, doc="The name of the user who posted this comment")

    def _get_email(self):
        return self.userinfo["email"]
    email = property(_get_email, doc="The email of the user who posted this comment")

    def get_absolute_url(self, anchor_pattern="#c%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        d = {
            'user': self.name,
            'date': self.submit_date,
            'comment': self.comment,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d
