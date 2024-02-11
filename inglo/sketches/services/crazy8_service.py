from ..models import Crazy8Stack, Crazy8Content
from ..models import Problem
from ..models import Sketch
from django.db import transaction

class Crazy8Service:
    def get_crazy8s_by_problem(problem_id):
        try:
            problem = Problem.objects.get(id = problem_id)
            crazy8 = Crazy8Stack.objects.filter(problem = problem)
            return crazy8
        except (Problem.DoesNotExist, Crazy8Stack.DoesNotExist, ValueError, TypeError):
            return Crazy8Stack.objects.none()

    @staticmethod
    @transaction.atomic
    def create_crazy8(problem_id, content, user):
        problem = Problem.objects.get(id = problem_id)
        sketch = Sketch.objects.filter(user=user, problem=problem_id).order_by('-created_at').first()
        if sketch.crazy8stack == None:
            crazy8stack = Crazy8Stack.objects.create(problem=problem)
            sketch.crazy8stack = crazy8stack
            sketch.save()
        if Crazy8Content.objects.filter(crazy8stack=sketch.crazy8stack).count() >= 8:
            return None #일단 8개 초과하여 crazy8content를 생성할 수 없도록 함
        crazy8content = Crazy8Content.objects.create(crazy8stack=sketch.crazy8stack, content=content)
        return crazy8content
    

        