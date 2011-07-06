from django.contrib.comments.models import Comment
from versionutils.versioning import TrackChanges

class VersionedComment(Comment):
    history = TrackChanges()
