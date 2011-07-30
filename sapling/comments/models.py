from django.contrib.comments.models import Comment
from versionutils.versioning import TrackChanges

class VersionedComment(Comment):
    history = TrackChanges()

    class Meta:
        verbose_name = 'comment'

    def __unicode__(self):
        return u'Comment by %s on %r: %s...' % (self.name, self.content_object, self.comment[:50])
