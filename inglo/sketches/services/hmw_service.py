from ..models import HMW
from ..models import Problem
from ..models import Sketch
from django.db import transaction

class HMWService:

    @staticmethod
    def get_hmws_by_problem(problem_id):
        try:
            problem = Problem.objects.get(id = problem_id)
            hmw = HMW.objects.filter(problem = problem)
            return hmw
        except (Problem.DoesNotExist, HMW.DoesNotExist, ValueError, TypeError):
            return HMW.objects.none()
    
    @staticmethod
    @transaction.atomic
    def create_hmw(problem_id, content):
        try:
            problem = Problem.objects.get(id = problem_id)
            hmw = HMW.objects.create(problem = problem, content = content)
            return hmw
        except (Problem.DoesNotExist, ValueError, TypeError):
            return None
    def update_hmw(user, hmw_id, problem_id):
        try:
            problem = Problem.objects.get(id = problem_id)
            hmw = HMW.objects.get(id = hmw_id)
            sketch = Sketch.objects.filter(user=user, problem=problem).order_by('-created_at').first() # 가장 최근에 추가된 해당 문제와 관련되어 사용자가 만든 스케치를 가져옴
            if sketch:
                sketch.hmw = hmw
                sketch.save()
                return hmw
        except (HMW.DoesNotExist, ValueError, TypeError):
            return None
        return None