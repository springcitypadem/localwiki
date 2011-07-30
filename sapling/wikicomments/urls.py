from django.conf.urls.defaults import *

from feeds import *

# Override particular URLs
urlpatterns = patterns('sapling.wikicomments.views',
    url(r'^post/$', 'post_comment', name='comments-post-comment'),
    url(r'^edit/$', 'edit_comment', name='comments-edit-comment'),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)
