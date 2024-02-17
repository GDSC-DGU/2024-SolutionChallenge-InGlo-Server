from django.db import transaction


class UserService:

    @staticmethod
    @transaction.atomic
    def update_global_impact(user):
        global_impact = (user.liked_total + user.sketch_num*7 + user.post_total*7 + user.feedback_total*3)/10
        if global_impact > 100:
            user.global_impact = 100
        user.global_impact = global_impact
        user.save()

    @staticmethod
    @transaction.atomic
    def update_language(user, language):
        user.language = language
        user.save()
        return user