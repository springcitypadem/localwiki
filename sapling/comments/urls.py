from django.conf.urls.defaults import *
from django.contrib.comments import urls

from feeds import *

# Override particular URLs
urlpatterns = patterns('sapling.comments.views',
    url(r'^post/$', 'post_comment', name='comments-post-comment'),
    url(r'^edit/$', 'edit_comment', name='comments-edit-comment'),
)

# Fall back to pages.
urlpatterns.extend(urls.urlpatterns)
