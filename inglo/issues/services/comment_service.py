from django.shortcuts import get_object_or_404
from issues.models import IssueComment, Issue
from django.core.exceptions import PermissionDenied
from django.db import transaction

class CommentService:

    @staticmethod
    def get_all_comments():
        return IssueComment.objects.all()
        

    @staticmethod
    @transaction.atomic
    def create_comment(user, issue_id, data):
        issue = get_object_or_404(Issue, pk=issue_id)
        parent_comment_id = data['parent_comment']
        if parent_comment_id and parent_comment_id.isdigit():
            parent_comment_id = int(parent_comment_id)
        else:
            parent_comment_id = None
        comment = IssueComment.objects.create(
            user=user,
            issue=issue,
            content=data['content'],
            parent_comment_id=parent_comment_id
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
