from django.core import urlresolvers

from forms import WikiCommentForm
from models import WikiComment

def get_model():
    return WikiComment

def get_form():
    return WikiCommentForm

def get_form_target():
    return urlresolvers.reverse('comments-post-comment')
