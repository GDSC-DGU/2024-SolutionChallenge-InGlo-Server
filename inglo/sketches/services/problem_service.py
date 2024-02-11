from ..models import Problem, Sketch
from datetime import datetime

class ProblemService:
    @staticmethod
    def get_problems_by_sdgs(sdgs):
        if not 1 <= int(sdgs) <= 17:
            return Problem.objects.none()
        try:
            return Problem.objects.filter(sdgs=sdgs).order_by('-created_at')[:10]
        except Problem.DoesNotExist:
            return Problem.objects.none()

    @staticmethod
    def create_problem(sdgs, content):
        try:
            problem = Problem.objects.create(sdgs=sdgs, content=content)
            return problem
        except (ValueError, TypeError):
            return None
        
    @staticmethod
    def create_sketch(problem_id, user):
        try:
            problem = Problem.objects.get(id = problem_id)
            sketch = Sketch.objects.create(user = user, problem = problem)
            return sketch
        except (Problem.DoesNotExist, ValueError, TypeError):
            return None