from comments.forms import VersionedCommentForm
from comments.models import VersionedComment

def get_model():
    return VersionedComment

def get_form():
    return VersionedCommentForm
