from ..models import Feedback
from django.db import transaction
from ..models import Post


class FeedbackService:

    @staticmethod
    @transaction.atomic
    def create_feedback(user, post_id, content, parent_id):
        """
        user, post_id, content를 받아 Feedback을 생성
        """
        post = Post.objects.get(id=post_id)
        if parent_id:
            parent_feedback = Feedback.objects.filter(id=parent_id).first()
        else:
            parent_feedback = None
        return Feedback.objects.create(user=user, post=post, content=content, parent_feedback=parent_feedback)
    
    @staticmethod
    @transaction.atomic
    def update_feedback(user, feedback_id, content):
        """
        user, feedback_id, content를 받아 Feedback을 수정
        """
        feedback = Feedback.objects.get(id=feedback_id)
        if feedback.user != user:
            return None
        feedback.content = content
        feedback.save()
        return feedback
    
    @staticmethod
    @transaction.atomic
    def delete_feedback(user, feedback_id):
        """
        user, feedback_id를 받아 Feedback을 삭제
        """
        feedback = Feedback.objects.get(id=feedback_id)
        if feedback.user != user:
            return None
        feedback.delete()
        return feedback
    
    