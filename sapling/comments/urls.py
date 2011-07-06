from django.conf.urls.defaults import *
from django.contrib.comments import urls

# Override particular URLs
urlpatterns = patterns('sapling.comments.views',
    url(r'^post/$', 'post_comment', name='comments-post-comment'),
)

# Fall back to pages.
urlpatterns.extend(urls.urlpatterns)
