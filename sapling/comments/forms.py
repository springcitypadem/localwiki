from django import forms
from django.conf import settings
from django.contrib.comments.forms import CommentForm
from django.utils.translation import ungettext, ugettext_lazy as _

from comments.models import VersionedComment

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

class VersionedCommentForm(CommentForm):
    comment = forms.CharField(label=_('Comment'),
                              widget=forms.Textarea(attrs={'cols':80,'rows':3}),
                              max_length=COMMENT_MAX_LENGTH)

    def get_comment_object(self):
        """
        Either return a new comment object, or update an old one.
        """
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        CommentModel = self.get_comment_model()
        data = self.get_comment_create_data()
        if data.has_key('comment_pk'):
            try:
                obj = CommentModel.objects.get(pk=data['comment_pk'])
            except CommentModel.DoesNotExist:
                return None
        else:
            obj = CommentModel(**data)

        obj = self.check_for_duplicate_comment(obj)
        return obj

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return VersionedComment

    def get_comment_create_data(self):
        data = super(VersionedCommentForm, self).get_comment_create_data()
        # Strip the user_* data, since it should not be needed here.
        for key in ['user_name', 'user_email', 'user_url']:
            try:
                data.pop(key)
            except KeyError:
                pass

        # Check for the pk field
        if 'comment_pk' in self.cleaned_data:
            data['comment_pk'] = self.cleaned_data['comment_pk']

        return data

    def check_for_duplicate_comment(self, new):
        """
        Check that a submitted comment isn't a duplicate. This might be caused
        by someone posting a comment twice. If it is a dup, silently return the 
*previous* comment.
        """
        possible_duplicates = self.get_comment_model()._default_manager.using(
            self.target_object._state.db
        ).filter(
            content_type = new.content_type,
            object_pk = new.object_pk,
            user = new.user,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.comment == new.comment:
                return old

        return new

