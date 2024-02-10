from django.shortcuts import get_object_or_404
from issues.models import IssueComment, Issue
from django.core.exceptions import PermissionDenied
from django.db import transaction

class CommentService:
    @staticmethod
    @transaction.atomic
    def create_comment(user, issue_id, data):
        issue = get_object_or_404(Issue, pk=issue_id)
        comment = IssueComment.objects.create(
            user=user,
            issue=issue,
            content=data['content'],
            parent_comment_id=data.get('parent_comment_id')
        )
        return comment

    @staticmethod
    @transaction.atomic
    def update_comment(user, comment_id, data):
        comment = get_object_or_404(IssueComment, pk=comment_id)
        if comment.user != user:
            raise PermissionDenied("You do not have permission to edit this comment.")
        comment.content = data['content']
        comment.save()
        return comment

    @staticmethod
    @transaction.atomic
    def delete_comment(user, comment_id):
        comment = get_object_or_404(IssueComment, pk=comment_id)
        if comment.user != user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        comment.delete()
