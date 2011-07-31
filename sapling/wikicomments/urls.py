from django.conf.urls.defaults import *

from feeds import *

# Override particular URLs
urlpatterns = patterns('sapling.wikicomments.views',
    url(r'^post/$', 'post_comment', name='comments-post-comment'),
    url(r'^edit/$', 'edit_comment', name='comments-edit-comment'),
    url(r'^delete/$', 'delete_comment', name='comments-delete-comment'),
    url(r'^fetch/$', 'fetch_comment', name='comments-fetch-comment'),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)
