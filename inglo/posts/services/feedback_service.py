from ..models import Feedback
from django.db import transaction
from ..models import Post


class FeedbackService:

    @staticmethod
    def get_feedback_list(post_id):
        try:
            feedback_list = Feedback.objects.filter(post_id=post_id)
            return feedback_list
        except Feedback.DoesNotExist:
            return Feedback.objects.none()

    @staticmethod
    @transaction.atomic
    def create_feedback(user, post_id, content, parent_id):
        """
        user, post_id, content를 받아 Feedback을 생성
        """
        try:
            post = Post.objects.get(id=post_id)
            if parent_id:
                parent_feedback = Feedback.objects.filter(id=parent_id).first()
            else:
                parent_feedback = None
            user.feedback_total += 1
            user.save()
            feedback = Feedback.objects.create(user=user, post=post, content=content, parent_feedback=parent_feedback)
            return feedback
        except (ValueError, TypeError, Post.DoesNotExist):
            return None
    
    @staticmethod
    @transaction.atomic
    def update_feedback(user, feedback_id, content):
        """
        user, feedback_id, content를 받아 Feedback을 수정
        """
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            if feedback.user != user:
                return None
            feedback.content = content
            feedback.save()
            return feedback
        except Feedback.DoesNotExist:
            return None
    
    @staticmethod
    @transaction.atomic
    def delete_feedback(user, feedback_id):
        """
        user, feedback_id를 받아 Feedback을 삭제
        """
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            if feedback.user != user:
                return None
            feedback.delete()
            return feedback
        except Feedback.DoesNotExist:
            return None
        
        
    