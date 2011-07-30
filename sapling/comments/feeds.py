from comments import VersionedComment

import recentchanges
from recentchanges import RecentChanges

class CommentChanges(RecentChanges):
    classname = 'comment'

    def queryset(self, start_at=None):
        if start_at:
            return VersionedComment.history.filter(history_info__date__gte=start_at)
        return VersionedComment.history.all()

    def page(self, obj):
        return obj.content_object

    def title(self, obj):
        return unicode(obj)

    def diff_url(self, obj):
        return None
    def as_of_url(self, obj):
        return None

recentchanges.register(CommentChanges)

