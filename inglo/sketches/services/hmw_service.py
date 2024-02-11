from ..models import HMW
from ..models import Problem

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
    def create_hmw(problem_id, content):
        try:
            problem = Problem.objects.get(id = problem_id)
            hmw = HMW.objects.create(problem = problem, content = content)
            return hmw
        except (Problem.DoesNotExist, ValueError, TypeError):
            return None
        