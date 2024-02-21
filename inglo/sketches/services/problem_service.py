from ..models import Problem, Sketch
from datetime import datetime

class ProblemService:
    @staticmethod
    def get_problems_by_sdgs(sdgs):
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
            sketch = Sketch.objects.create(user = user, problem = problem, title = "Untitled", description = "No description", image_url = "", content = "", created_at = datetime.now())
            return sketch
        except (Problem.DoesNotExist, ValueError, TypeError):
            return None
        
    def get_problem_by_id(problem_id):
        try:
            return Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return None