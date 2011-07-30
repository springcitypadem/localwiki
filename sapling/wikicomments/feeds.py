from models import WikiComment

import recentchanges
from recentchanges import RecentChanges

class WikiCommentChanges(RecentChanges):
    classname = 'wikicomment'

    def queryset(self, start_at=None):
        if start_at:
            return WikiComment.history.filter(history_info__date__gte=start_at)
        return WikiComment.history.all()

    def page(self, obj):
        return obj.content_object

    def title(self, obj):
        return unicode(obj)

    def diff_url(self, obj):
        # TODO
        return None

    def as_of_url(self, obj):
        # TODO
        return None

recentchanges.register(WikiCommentChanges)
